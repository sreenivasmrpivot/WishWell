import os
from langchain_community.llms import CTransformers, VLLM, VLLMOpenAI
#from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Milvus
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from helper import get_embedding_model_path, get_model_path
from models import InferenceServerEnum, VectorDatabaseEnum, Wish

from common.logging_decorator import auto_log_entry_exit
from server.vmwarevllmapi.VmwareVllmApiWrapper import VmwareVllmApiWrapper

@auto_log_entry_exit()
class WishProcessor:

    def __init__(self, wish: Wish):
        self.template = """Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Context: {context}
        Question: {question}
        Only return the helpful answer below and nothing else.
        Helpful answer:
        """
        self.wish = wish
        self.faiss_path = os.path.join(self.wish.rootPath, "vector-store/langchain/faiss")
        print(self.faiss_path)
        self._load_embbedding()
        # self._load_document()
        # self._split_document()
        # self._save_document_in_vdb()
        self._load_document_from_vdb()
        self._load_llm()

    def _load_embbedding(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=get_embedding_model_path(self.wish.modelName),
            model_kwargs={'device': self.wish.device})
        
    # def _load_document(self):
    #     # load the document    
    #     loader = PyPDFLoader(get_document_path(self.wish))
    #     # interpret information in the documents
    #     self.document = loader.load()

    # def _split_document(self):
    #     # split the document into chunks
    #     splitter = RecursiveCharacterTextSplitter(chunk_size=500,
    #                                               chunk_overlap=50)
    #     self.texts = splitter.split_documents(self.document)

    # def _save_document_in_vdb(self):
    #     # create vector db and save the document in vector database
    #     if self.wish.vectorDatabase == VectorDatabaseEnum.FAISS:
    #         # FAISS as a vector database
    #         self.db = FAISS.from_documents(
    #             self.texts, 
    #             self.embedding
    #         )
    #         self.db.save_local(self.faiss_path)
    #     elif self.wish.vectorDatabase == VectorDatabaseEnum.Milvus:
    #         # Milvus as a vector database
    #         self.db = Milvus.from_documents(
    #             self.texts, 
    #             self.embedding, 
    #             collection_name=self.wish.knowledgeBaseId,
    #             connection_args={"host": "127.0.0.1", "port": "19530"}
    #         )

    def _load_document_from_vdb(self):
        # load the document from vector database
        if self.wish.vectorDatabase == VectorDatabaseEnum.FAISS:
            # FAISS as a vector database
            self.db = FAISS.load_local(
                self.faiss_path, 
                self.embedding
            )
        elif self.wish.vectorDatabase == VectorDatabaseEnum.Milvus:
            # Milvus as a vector database
            self.db = Milvus(
                self.embedding,
                collection_name=self.wish.knowledgeBaseId,
                connection_args={"host": "127.0.0.1", "port": "19530"}
            )

    def _load_llm(self):
        if self.wish.inferenceServer == InferenceServerEnum.VmwareVllmApi:
            vmwareVllmApiWrapper = VmwareVllmApiWrapper(self.wish)
            self.llm = VLLMOpenAI(
                openai_api_key = vmwareVllmApiWrapper.api_key,
                openai_api_base = vmwareVllmApiWrapper.endpoint,
                model_name = get_model_path(self.wish),
                # model_kwargs = {"stop": ["."]},                
            )
            # self.llm = ChatOpenAI(
                # openai_api_key = vmwareVllmApiWrapper.api_key,
                # openai_api_base = vmwareVllmApiWrapper.endpoint,
                # model = get_model_path(self.wish),
                # max_tokens=256,
                # temperature=0.01,
            # )
        elif self.wish.inferenceServer == InferenceServerEnum.Vllm:
            self.llm = VLLM(
                model=get_model_path(self.wish),
                trust_remote_code=True,  # mandatory for hf models
                max_new_tokens=256,
                temperature=0.01,
            )
        # elif self.wish.server == ServerEnum.NvidiaTriton:
            # self.llm = ChatNVIDIA(
                # client="http://localhost:8000/v2/models/llm/versions/1/infer",
                # top_p=0.95,
                # model=get_model_path(self.wish),
                # max_tokens=256,
                # temperature=0.01,
            # )
        else:
            self.llm = CTransformers(
                model=get_model_path(self.wish),
                model_type=self.wish.modelName,
                config={'max_new_tokens': 256, 'temperature': 0.01}
            )

        retriever = self.db.as_retriever(search_kwargs={'k': 2})
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=['context', 'question'])
        self.qa_llm = RetrievalQA.from_chain_type(llm=self.llm,
                                            chain_type='stuff',
                                            retriever=retriever,
                                            return_source_documents=True,
                                            chain_type_kwargs={'prompt': self.prompt})

    def run(self):
        response = self.qa_llm({'query': self.wish.whisper})
        return response["result"]
