import os
import fitz  # PyMuPDF


class PDFLoader:
    def __init__(self, literature_directory: str):
        self.literature_directory = literature_directory

    def load_pdfs(self):
        """
        Returns a list of dictionaries:
        [
            {
                "text": full_text,
                "metadata": {
                    "title": ...,
                    "author": ...,
                    "year": ...,
                    "doi": ...,
                    "source_file": ...
                }
            }
        ]
        """
        documents = []

        if not os.path.exists(self.literature_directory):
            raise FileNotFoundError(
                f"Literature directory not found: {self.literature_directory}"
            )

        for filename in os.listdir(self.literature_directory):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.literature_directory, filename)
                doc_data = self._extract_pdf(file_path)
                documents.append(doc_data)

        return documents

    def _extract_pdf(self, file_path: str):
        doc = fitz.open(file_path)
        full_text = ""

        for page in doc:
            full_text += page.get_text()

        metadata = self._extract_metadata(doc, file_path)
        doc.close()

        return {
            "text": full_text,
            "metadata": metadata
        }

    def _extract_metadata(self, doc, file_path: str):
        meta = doc.metadata or {}

        return {
            "title": meta.get("title", "Unknown Title"),
            "author": meta.get("author", "Unknown Author"),
            "year": self._extract_year(meta),
            "doi": meta.get("subject", "Unknown DOI"),
            "source_file": os.path.basename(file_path)
        }

    def _extract_year(self, meta: dict):
        creation_date = meta.get("creationDate", "")
        if creation_date and len(creation_date) >= 6:
            return creation_date[2:6]
        return "Unknown Year"
