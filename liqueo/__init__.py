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
from liqueo.workflow import (
    WorkflowEngine,
    WorkflowSession,
    WorkflowStep,
    LessonLearned,
    EngagementTemplate,
)

__all__ = [
    "Document",
    "KnowledgeBase",
    "SearchResult",
    "EmbeddingsManager",
    "RecommendationEngine",
    "KnowledgeSynthesizer",
    "WorkflowEngine",
    "WorkflowSession",
    "WorkflowStep",
    "LessonLearned",
    "EngagementTemplate",
]
