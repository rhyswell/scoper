import json
from typing import Dict

from openai import OpenAI


class StanceClassifier:
    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def classify(self, claim: str, chunk: Dict) -> Dict:
        """
        Returns:
        {
            "stance": "support" | "oppose" | "neutral",
            "confidence": float
        }
        """

        prompt = f"""
You are an expert scientific stance classifier.

Claim:
"{claim}"

Passage:
"{chunk['text']}"

Metadata:
Title: {chunk['metadata'].get('title')}
Author: {chunk['metadata'].get('author')}
Year: {chunk['metadata'].get('year')}

Determine whether the passage SUPPORTS, OPPOSES, or is NEUTRAL toward the claim.

Respond strictly in valid JSON format:
{{
  "stance": "support" | "oppose" | "neutral",
  "confidence": float between 0 and 1
}}
"""

        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
            max_output_tokens=200
        )

        content = response.output[0].content[0].text.strip()

        try:
            result = json.loads(content)
        except Exception:
            result = {
                "stance": "neutral",
                "confidence": 0.0
            }

        return result
