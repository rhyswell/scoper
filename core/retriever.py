import json
import os
from typing import List, Dict, Tuple

from core.embedding_manager import EmbeddingManager
from core.faiss_manager import FAISSManager


class Retriever:
    def __init__(self, config):
        self.config = config

        self.data_dir = self.config.get_data_directory()
        self.index_path = os.path.join(self.data_dir, "vector.index")
        self.chunks_path = os.path.join(self.data_dir, "chunks.json")

        self.embedding_manager = EmbeddingManager(
            api_key=self.config.get_api_key(),
            model_name=self.config.get_embedding_model()
        )

        self.faiss_manager = FAISSManager(self.index_path)
        self.faiss_manager.load_index()

        self.chunks = self._load_chunks()

    def _load_chunks(self) -> List[Dict]:
        if not os.path.exists(self.chunks_path):
            raise FileNotFoundError("chunks.json not found. Please re-index literature.")

        with open(self.chunks_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def retrieve(self, claim: str, top_k: int = None) -> List[Dict]:
        if top_k is None:
            top_k = self.config.get_top_k()

        query_vector = self.embedding_manager.embed_single(claim)
        scores, indices = self.faiss_manager.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores, indices):
            if idx == -1:
                continue

            chunk_data = self.chunks[idx]
            results.append({
                "score": float(score),
                "text": chunk_data["text"],
                "metadata": chunk_data["metadata"]
            })

        return results
