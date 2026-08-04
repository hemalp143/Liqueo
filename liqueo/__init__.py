"""Liqueo: Knowledge Discovery & Reuse Component for Financial Consulting."""

__version__ = "0.1.0"
__author__ = "Liqueo Team"

from liqueo.core import (
    Document,
    KnowledgeBase,
    SearchResult,
)
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer

__all__ = [
    "Document",
    "KnowledgeBase",
    "SearchResult",
    "EmbeddingsManager",
    "RecommendationEngine",
    "KnowledgeSynthesizer",
]
