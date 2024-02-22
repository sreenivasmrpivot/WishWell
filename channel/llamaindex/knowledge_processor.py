from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, ServiceContext, set_global_service_context, LLMPredictor
from llama_index.llms import HuggingFaceLLM, LlamaCPP
from llama_index.prompts.prompts import SimpleInputPrompt
# from sentence_transformers import SentenceTransformer
# from llama_index.embeddings import HuggingFaceEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from helper import get_document_path, get_embedding_model_path, get_model_path, get_tokenizer_path

from models import EmbeddingModelEnum, Information, ModelLocationEnum, Wish

from common.logging_decorator import auto_log_entry_exit

@auto_log_entry_exit()
class KnowledgeProcessor:
    vectorStorePath = "./vector-store/llama-index"

    def __init__(self,  information: Information):
        self.information = information

    # def _load_embbedding(self):
    #     # self.embedding = HuggingFaceEmbedding(model_name=get_embedding_model_path(self.wish))
    #     # self.embedding = SentenceTransformer(get_embedding_model_path(self.wish))
    #     self.embedding = HuggingFaceEmbeddings(model_name=get_embedding_model_path(self.information.modelName))
    
    def _load_document(self):
        self.document = SimpleDirectoryReader(input_files=[get_document_path(self.information)]).load_data()

    # def _persist_document_inmemory(self):
    #     self.index = VectorStoreIndex.from_documents(self.document, service_context=self.service_context) # this is just in memory

    def _persist_document_ondisk(self):
        self.index.storage_context.persist(persist_dir=KnowledgeProcessor.vectorStorePath) # this enables storing vector store on disk

    def _load_index_from_disk(self):
        self.storage_context = StorageContext.from_defaults(persist_dir=KnowledgeProcessor.vectorStorePath)
        self.index = load_index_from_storage(storage_context=self.storage_context)

    def _load_query_engine(self):
        self.db = self.index.as_query_engine()

    # def _load_chat_bot(self):
        # self.query_chat_bot = self.index.as_chat_bot()

    def learn(self):
        # self._load_embbedding()
        self._load_document()
        # self._persist_document_inmemory()
        self._persist_document_ondisk()
        return self.db
    
# if __name__ == '__main__':
#     wish = Wish(location="local", documentName="Business Conduct.pdf", modelName="Llama", channel="Llamaindex", whisper="what is Legal Holds?")
#     run(wish)