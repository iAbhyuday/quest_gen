class BaseIndexer:
    
    def __init__(
        self,
        db_url: str, 
        embedding_model,
        chunking_method,
        chunk_size
        ):
        
        self.db_url = db_url
        self.embeddin_model = embedding_model
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        
    def _parse_doc(self, doc):
        pass
    
    def _chunk_docs(self, doc):
        pass
    
    def _index(self):
        pass
    def add_to_collection(self, file_name, collection_name: str):
        pass