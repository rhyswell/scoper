from typing import Dict, List

from core.config_loader import ConfigLoader
from core.retriever import Retriever
from core.stance_classifier import StanceClassifier
from core.argument_aggregator import ArgumentAggregator
from core.index_builder import IndexBuilder


class ScoperEngine:
    def __init__(self):
        self.config = ConfigLoader()

        self.retriever = Retriever(self.config)

        self.stance_classifier = StanceClassifier(
            api_key=self.config.get_api_key(),
            model_name=self.config.get_generation_model()
        )

        self.aggregator = ArgumentAggregator(
            api_key=self.config.get_api_key(),
            model_name=self.config.get_generation_model()
        )

    def reindex_literature(self):
        builder = IndexBuilder(self.config)
        builder.build()

        # Reload retriever after reindex
        self.retriever = Retriever(self.config)

    def analyze_claim(self, claim: str) -> Dict[str, str]:
        if not claim.strip():
            return {
                "support": "Claim is empty.",
                "oppose": "Claim is empty."
            }

        retrieved_chunks = self.retriever.retrieve(claim)

        supporting_chunks: List[Dict] = []
        opposing_chunks: List[Dict] = []

        for chunk in retrieved_chunks:
            classification = self.stance_classifier.classify(claim, chunk)
            stance = classification.get("stance", "neutral")

            if stance == "support":
                supporting_chunks.append(chunk)
            elif stance == "oppose":
                opposing_chunks.append(chunk)

        support_summary = self.aggregator.aggregate(
            claim, supporting_chunks, "support"
        )

        oppose_summary = self.aggregator.aggregate(
            claim, opposing_chunks, "oppose"
        )

        return {
            "support": support_summary,
            "oppose": oppose_summary
        }
