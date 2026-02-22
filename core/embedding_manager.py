import numpy as np
from openai import OpenAI
from typing import List


class EmbeddingManager:
    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Returns normalized embeddings as numpy array (n, d)
        """
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )

        embeddings = np.array([item.embedding for item in response.data])
        return self._normalize(embeddings)

    def embed_single(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            model=self.model_name,
            input=[text]
        )

        embedding = np.array(response.data[0].embedding)
        return self._normalize(embedding.reshape(1, -1))[0]

    def save_embeddings(self, embeddings: np.ndarray, path: str):
        np.save(path, embeddings)

    def load_embeddings(self, path: str) -> np.ndarray:
        return np.load(path)

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms
