from typing import List, Dict
from openai import OpenAI


class ArgumentAggregator:
    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def aggregate(self, claim: str, chunks: List[Dict], stance: str) -> str:
        """
        stance: "support" or "oppose"
        Returns formatted bullet point arguments with citations.
        """

        if not chunks:
            return "No relevant arguments found."

        compiled_passages = ""
        for i, chunk in enumerate(chunks, 1):
            meta = chunk["metadata"]
            citation = f"({meta.get('author')}, {meta.get('year')})"

            compiled_passages += f"""
Passage {i} {citation}:
{chunk['text']}
"""

        prompt = f"""
You are an expert scientific argument synthesizer.

Claim:
"{claim}"

Below are passages that {stance.upper()} the claim.

{compiled_passages}

Task:
- Summarize the key {stance.upper()}ING arguments.
- Produce concise bullet points.
- Each bullet must end with citation in format (Author, Year).
- Do not fabricate sources.
- Only use provided passages.
"""

        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
            max_output_tokens=800
        )

        return response.output[0].content[0].text.strip()
