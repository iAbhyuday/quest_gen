import os
import google.generativeai as genai
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.bridge.pydantic import Field
from typing import List


class GeminiEmbedding(BaseEmbedding):
    """
    Custom embedding model using Google Gemini API.
    """
    def __init__(self, api_key: str = None, model_name: str = None):
        if api_key:
            self.api_key = api_key
        if model_name:
            self.model_name = model_name

        if not self.api_key:
            raise ValueError("API key for Gemini is missing. Set it in the environment or pass it explicitly.")

        genai.configure(api_key=self.api_key)
        super().__init__()

    def get_text_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a single text string.
        """
        response = genai.embed_content(model=self.model_name, content=text, task_type="retrieval_document")
        return response["embedding"]

    async def aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronous version of get_text_embedding."""
        return self.get_text_embedding(text)

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of text strings.
        """
        return [self.get_text_embedding(text) for text in texts]

    async def aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous version of get_text_embeddings."""
        return self.get_text_embeddings(texts)
