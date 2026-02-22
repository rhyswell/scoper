import uuid
from typing import List, Dict


class TextChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Input:
            [
                {
                    "text": "...",
                    "metadata": {...}
                }
            ]

        Output:
            [
                {
                    "id": str,
                    "text": str,
                    "metadata": {...}
                }
            ]
        """
        all_chunks = []

        for doc in documents:
            text = doc["text"]
            metadata = doc["metadata"]

            chunks = self._chunk_text(text)

            for chunk_text in chunks:
                all_chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "metadata": metadata
                })

        return all_chunks

    def _chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        return chunks
