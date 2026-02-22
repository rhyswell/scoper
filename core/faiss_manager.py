import faiss
import numpy as np
import os


class FAISSManager:
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.index = None

    def build_index(self, embeddings: np.ndarray):
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings.astype("float32"))

        self.index = index

    def save_index(self):
        if self.index is None:
            raise ValueError("No index to save.")
        faiss.write_index(self.index, self.index_path)

    def load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("FAISS index file not found.")
        self.index = faiss.read_index(self.index_path)

    def search(self, query_vector: np.ndarray, top_k: int):
        if self.index is None:
            raise ValueError("FAISS index not loaded.")

        query_vector = query_vector.astype("float32").reshape(1, -1)
        scores, indices = self.index.search(query_vector, top_k)

        return scores[0], indices[0]
