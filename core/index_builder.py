import os
import json
from typing import List, Dict

from core.pdf_loader import PDFLoader
from core.chunker import TextChunker
from core.embedding_manager import EmbeddingManager
from core.faiss_manager import FAISSManager


class IndexBuilder:
    def __init__(self, config):
        self.config = config

        self.data_dir = self.config.get_data_directory()
        self.literature_dir = self.config.get_literature_directory()

        os.makedirs(self.data_dir, exist_ok=True)

        self.index_path = os.path.join(self.data_dir, "vector.index")
        self.embeddings_path = os.path.join(self.data_dir, "embeddings.npy")
        self.chunks_path = os.path.join(self.data_dir, "chunks.json")

    def build(self):
        print("Loading PDFs...")
        loader = PDFLoader(self.literature_dir)
        documents = loader.load_pdfs()

        print("Chunking documents...")
        chunker = TextChunker(
            chunk_size=self.config.get_chunk_size(),
            chunk_overlap=self.config.get_chunk_overlap()
        )
        chunks = chunker.chunk_documents(documents)

        print("Generating embeddings...")
        embedding_manager = EmbeddingManager(
            api_key=self.config.get_api_key(),
            model_name=self.config.get_embedding_model()
        )

        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_manager.embed_texts(texts)

        print("Saving embeddings...")
        embedding_manager.save_embeddings(embeddings, self.embeddings_path)

        print("Building FAISS index...")
        faiss_manager = FAISSManager(self.index_path)
        faiss_manager.build_index(embeddings)
        faiss_manager.save_index()

        print("Saving chunk metadata...")
        self._save_chunks(chunks)

        print("Indexing complete.")

    def _save_chunks(self, chunks: List[Dict]):
        with open(self.chunks_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
