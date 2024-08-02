from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

class VectorDB:
    def __init__(self, client, collection_name, embedding_func):
        self.store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embedding_func
        )
    
    def get_retriever(self):
        return self.store.as_retriever()

    def sim_search(self, query):
        return self.store.similarity_search(query)
    
    
        
