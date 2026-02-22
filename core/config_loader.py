import json
import os


class ConfigLoader:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def get_api_key(self) -> str:
        api_key = self.config.get("openai_api_key")
        if not api_key or api_key == "YOUR_OPENAI_API_KEY":
            raise ValueError("OpenAI API key is missing or not set in config.json")
        return api_key

    def get_embedding_model(self) -> str:
        return self.config.get("embedding_model")

    def get_generation_model(self) -> str:
        return self.config.get("generation_model")

    def get_chunk_size(self) -> int:
        return int(self.config.get("chunk_size", 800))

    def get_chunk_overlap(self) -> int:
        return int(self.config.get("chunk_overlap", 150))

    def get_top_k(self) -> int:
        return int(self.config.get("top_k", 15))

    def get_data_directory(self) -> str:
        return self.config.get("data_directory", "data")

    def get_literature_directory(self) -> str:
        return self.config.get("literature_directory", "literature")
