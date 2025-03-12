import os
import uuid
import chromadb
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings as Hf_embeddings


class VectorDB:
    def __init__(self, client, collection_name:str, embedding_func):
        self.store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embedding_func
        )
    
    @staticmethod
    def add_to_collection(file_path, collection_name, collection_type, doc_type="pdf"):
        msg=""
        if doc_type == "pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        try:
            embedding_function = Hf_embeddings(model="sentence-transformers/all-MiniLM-l6-v2",\
                                                huggingfacehub_api_token=os.environ.get('HF_TOKEN'))
            client = chromadb.HttpClient(host='vector-store', port=8000)
            collections = [c.name for c in client.list_collections()]
            collection_name = collection_name.replace(" ","-")
            if collection_name in collections:
                msg = f"Overwriting exixting collection with name {collection_name}"
                client.delete_collection(collection_name)
                
            collection = client.create_collection(collection_name)
            
            for doc in docs:
                collection.add(
                            ids=[str(uuid.uuid1())],
                            metadatas=doc.metadata,
                            documents=doc.page_content,
                            embeddings=embedding_function.embed_query(doc.page_content)
                            )
            
        except Exception as e:
            raise(e)
            return False,msg
        return True, msg

    @staticmethod
    def get_retriever(cls, collection_name):
        client = chromadb.HttpClient(host='vector-store', port=8000)
        embedding_function = Hf_embeddings(model="sentence-transformers/all-MiniLM-l6-v2",\
                                                huggingfacehub_api_token=os.environ.get('HF_TOKEN'))
        return VectorDB(
                    client=client,
                    collection_name=collection_name,
                    embedding_func=embedding_function
                )

    def get_retriever(self):
        return self.store.as_retriever()

    def sim_search(self, query):
        return self.store.similarity_search(query)
    
    
        
