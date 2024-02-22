import os
from httpx import get
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader, UnstructuredHTMLLoader, DirectoryLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Milvus
from regex import B, P
from scipy.__config__ import show

from helper import get_document_path, get_embedding_model_path
from models import VectorDatabaseEnum, Information

from common.logging_decorator import auto_log_entry_exit

@auto_log_entry_exit()
class KnowledgeProcessor:

    def __init__(self, information: Information):
        self.information = information
        self.faiss_path = os.path.join(self.information.rootPath, "vector-store/langchain/faiss")

    def _load_embbedding(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=get_embedding_model_path(self.information.modelName),
            model_kwargs={'device': self.information.device})
        
    def _load_documents(self):
        
        # load all documents
        # loader_rest = DirectoryLoader(
        #     path = get_document_path(self.information), 
        #     glob = "**/[!.]*",
        #     show_progress = True,
        #     use_multithreading = True
        # )

        # load the html documents
        # loader_html = BSHTMLLoader(get_document_path(self.information))
        folderPath = get_document_path(self.information)
        print(folderPath)

        loader_html = DirectoryLoader(
            path = folderPath, 
            glob = "./*.html",
            loader_cls=BSHTMLLoader,
            show_progress = True,
            use_multithreading = True
        )
        # loader_html = UnstructuredHTMLLoader(get_document_path(self.information))

        # load the pdf documents    
        # loader_pdf = PyPDFLoader(get_document_path(self.information))
        # loader_pdf = DirectoryLoader(
        #     path = get_document_path(self.information), 
        #     glob = "./*.pdf",
        #     loader_cls=PyPDFLoader,
        #     show_progress = True,
        #     use_multithreading = True
        # )

        # loader_all = MergedDataLoader(loaders=[loader_html])
        # self.docs = loader_all.load()
        # self.docs = loader_html.load()
        # print(self.docs)

        # loader_html = BSHTMLLoader("./data/2-hidden-virtual-machine-gems-in.html")
        # loader_html = UnstructuredHTMLLoader("./data/2-hidden-virtual-machine-gems-in.html")

        self.docs = loader_html.load()
        print(len(self.docs))


    def _split_document(self):
        # split the document into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                  chunk_overlap=50)
        self.texts = splitter.split_documents(self.docs)

    def _save_document_in_vdb(self):
        # create vector db and save the document in vector database
        if self.information.vectorDatabase == VectorDatabaseEnum.FAISS:
            # FAISS as a vector database
            self.db = FAISS.from_documents(
                self.texts, 
                self.embedding
            )
            self.db.save_local(self.faiss_path)
        elif self.information.vectorDatabase == VectorDatabaseEnum.Milvus:
            # Milvus as a vector database
            self.db = Milvus.from_documents(
                self.texts, 
                self.embedding, 
                collection_name=self.information.knowledgeBaseId,
                connection_args={"host": "127.0.0.1", "port": "19530"}
            )

    def learn(self):
        self._load_embbedding()
        self._load_documents()
        self._split_document()
        self._save_document_in_vdb()
        # return self.db