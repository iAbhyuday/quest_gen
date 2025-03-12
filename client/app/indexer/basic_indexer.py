import os
from base import BaseIndexer
from llama_index.readers.file import PyMuPDFReader, TextReader, MarkdownReader
from llama_index.readers.llama

class BasicIndexer(BaseIndexer):
    
    def __init__(
        self,
        db_url,
        embedding_model,
        chunking_method,
        chunk_size
        ):
        
        self.db_url = db_url
        self.embeddin_model = embedding_model
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        
    def _parse_doc(self, file_name):
        ext = file_name.split(".")[-1].lower()
        assert ext in ["pdf", "txt", "md"]
        # Load a single PDF file
        pdf_path = os.path.join("uploads", file_name)
        
        if ext == "pdf":
            reader = PyMuPDFReader()
        elif ext == "md":
            reader = MarkdownReader()
        else:
            reader = TextReader()
            
        docs = reader.load_data(pdf_path)
        
        return docs
        
        
        
    
    def _chunk_docs(self, doc):
        pass
    
    def _index(self):
        pass
    def add_to_collection(self, file_name, collection_name: str):

        contents = self._parse_doc(file_name)
        chunked_contents = self._chunk_docs(content)
        
        return self._index(chunked_contents)