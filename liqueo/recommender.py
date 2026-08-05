"""Recommendation engine for suggesting similar engagements and patterns."""

from dataclasses import dataclass
from typing import Optional
from liqueo.core import Document, SearchResult, KnowledgeBase
from liqueo.embeddings import EmbeddingsManager


@dataclass
class Recommendation:
    """A recommended engagement or pattern."""

    reference_document: Document
    reasoning: str
    relevance_score: float
    suggested_approach: Optional[str] = None
    potential_challenges: Optional[str] = None
    estimated_effort: Optional[str] = None


class RecommendationEngine:
    """Generates recommendations for current engagements."""

    def __init__(self, embeddings_manager: EmbeddingsManager):
        """Initialize recommendation engine."""
        self.embeddings_manager = embeddings_manager
        self.kb = embeddings_manager.kb

    def recommend_similar_engagements(
        self,
        query_document: Document | str,
        top_k: int = 5,
        industry_specific: bool = True,
    ) -> list[Recommendation]:
        """Recommend similar past engagements."""
        if isinstance(query_document, Document):
            query_text = f"{query_document.title}\n{query_document.content}"
            query_industry = query_document.industry
            query_type = query_document.transaction_type
        else:
            query_text = query_document
            query_industry = None
            query_type = None

        filters = {}
        if industry_specific and query_industry:
            filters["industry"] = query_industry

        try:
            search_results = self.embeddings_manager.semantic_search(
                query_text, top_k=top_k * 2, filters=filters
            )
        except Exception as e:
            print(f"Warning: Semantic search failed, using fallback: {e}")
            search_results = self._fallback_recommendations(query_industry, top_k)

        recommendations = []
        for result in search_results:
            if isinstance(query_document, Document):
                if result.document.id == query_document.id:
                    continue

            reasoning = self._generate_reasoning(result, query_industry, query_type)
            suggested_approach = self._extract_approach(result.document)
            potential_challenges = self._extract_challenges(result.document)
            estimated_effort = self._estimate_effort(result.document)

            recommendation = Recommendation(
                reference_document=result.document,
                reasoning=reasoning,
                relevance_score=result.similarity_score,
                suggested_approach=suggested_approach,
                potential_challenges=potential_challenges,
                estimated_effort=estimated_effort,
            )
            recommendations.append(recommendation)

        return recommendations[:top_k]

    def _fallback_recommendations(self, industry: Optional[str], top_k: int) -> list:
        """Fallback: return recent documents from same industry."""
        docs = self.kb.filter_by_industry(industry) if industry else self.kb.list_documents()
        docs = sorted(docs, key=lambda d: d.created_at, reverse=True)[:top_k]
        return [SearchResult(document=doc, similarity_score=0.5) for doc in docs]

    def recommend_by_industry(self, industry: str, top_k: int = 5) -> list[Recommendation]:
        """Get recommendations for all engagements in an industry."""
        industry_docs = self.kb.filter_by_industry(industry)
        if not industry_docs:
            return []

        recommendations = []
        for doc in industry_docs[:top_k]:
            recommendation = Recommendation(
                reference_document=doc,
                reasoning=f"Recent {industry} engagement",
                relevance_score=1.0,
                suggested_approach=self._extract_approach(doc),
                potential_challenges=self._extract_challenges(doc),
                estimated_effort=self._estimate_effort(doc),
            )
            recommendations.append(recommendation)

        return recommendations

    def recommend_by_transaction_type(
        self, transaction_type: str, top_k: int = 5
    ) -> list[Recommendation]:
        """Get recommendations for a specific transaction type."""
        type_docs = self.kb.filter_by_transaction_type(transaction_type)
        if not type_docs:
            return []

        recommendations = []
        for doc in type_docs[:top_k]:
            recommendation = Recommendation(
                reference_document=doc,
                reasoning=f"Similar {transaction_type} engagement",
                relevance_score=1.0,
                suggested_approach=self._extract_approach(doc),
                potential_challenges=self._extract_challenges(doc),
                estimated_effort=self._estimate_effort(doc),
            )
            recommendations.append(recommendation)

        return recommendations

    def find_patterns(self, industry: Optional[str] = None) -> dict[str, list[Document]]:
        """Identify patterns in consulting approaches."""
        if industry:
            documents = self.kb.filter_by_industry(industry)
        else:
            documents = self.kb.list_documents()

        patterns = {}
        for doc in documents:
            if doc.consulting_approach:
                approach = doc.consulting_approach
                if approach not in patterns:
                    patterns[approach] = []
                patterns[approach].append(doc)

        return {k: v for k, v in patterns.items() if v}

    def _generate_reasoning(
        self, result: SearchResult, industry: Optional[str], transaction_type: Optional[str]
    ) -> str:
        """Generate reasoning for a recommendation."""
        reasons = []

        if result.document.industry == industry:
            reasons.append(f"Same industry ({industry})")
        if result.document.transaction_type == transaction_type:
            reasons.append(f"Same transaction type ({transaction_type})")

        reasons.append(f"High semantic similarity ({result.similarity_score:.2%})")

        return "; ".join(reasons) if reasons else "Semantically similar engagement"

    def _extract_approach(self, document: Document) -> Optional[str]:
        """Extract consulting approach from document."""
        if document.consulting_approach:
            return document.consulting_approach

        if "approach" in document.content.lower():
            lines = document.content.split("\n")
            for i, line in enumerate(lines):
                if "approach" in line.lower():
                    return " ".join(lines[i : min(i + 3, len(lines))]).strip()

        return None

    def _extract_challenges(self, document: Document) -> Optional[str]:
        """Extract challenges or risks from document."""
        for keyword in ["challenge", "risk", "obstacle", "issue", "problem"]:
            if keyword in document.content.lower():
                lines = document.content.split("\n")
                for i, line in enumerate(lines):
                    if keyword in line.lower():
                        return " ".join(lines[i : min(i + 2, len(lines))]).strip()

        return document.key_outcomes

    def _estimate_effort(self, document: Document) -> Optional[str]:
        """Estimate engagement effort based on historical data."""
        if not document.duration_months or not document.engagement_value:
            return None

        effort_level = "Low"
        if document.duration_months > 6:
            effort_level = "High"
        elif document.duration_months > 3:
            effort_level = "Medium"

        return f"{effort_level} effort (~{document.duration_months} months, ${document.engagement_value}M)"
