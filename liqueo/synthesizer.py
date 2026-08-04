"""Knowledge synthesis using LLMs."""

from typing import Optional
from liqueo.core import Document, SearchResult, KnowledgeBase
from liqueo.recommender import RecommendationEngine


class KnowledgeSynthesizer:
    """Synthesizes insights from knowledge base using LLMs."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        recommendation_engine: RecommendationEngine,
        model: str = "anthropic",
    ):
        """Initialize knowledge synthesizer."""
        self.kb = knowledge_base
        self.recommendation_engine = recommendation_engine
        self.model = model

        if model == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic()
            except ImportError:
                raise ImportError(
                    "Anthropic SDK required. Install with: pip install anthropic"
                )
        elif model == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI()
            except ImportError:
                raise ImportError(
                    "OpenAI SDK required. Install with: pip install openai"
                )

    def synthesize_recommendations(
        self, engagement_description: str, top_k: int = 3
    ) -> str:
        """Generate synthesis of recommendations with insights."""
        recommendations = self.recommendation_engine.recommend_similar_engagements(
            engagement_description, top_k=top_k
        )

        if not recommendations:
            return "No similar engagements found in knowledge base."

        recommendation_text = self._format_recommendations(recommendations)

        prompt = f"""You are a senior financial consultant. Based on the following similar past engagements,
provide strategic insights and recommendations for the current engagement.

Current Engagement:
{engagement_description}

Similar Past Engagements:
{recommendation_text}

Please provide:
1. Key Insights: What patterns do you see in these similar engagements?
2. Recommended Approach: What approach worked best in similar cases?
3. Potential Risks: What challenges should we anticipate?
4. Resource Allocation: How should we allocate resources based on historical data?
5. Timeline: What is a realistic timeline based on similar engagements?

Keep your response concise and actionable."""

        if self.model == "anthropic":
            response = self.client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        elif self.model == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

    def generate_engagement_summary(self, document: Document) -> str:
        """Generate a concise summary of an engagement."""
        prompt = f"""Summarize the following consulting engagement in a concise, professional manner.
Focus on: key outcomes, methodology, industry insights, and reusable learnings.

Title: {document.title}
Industry: {document.industry}
Transaction Type: {document.transaction_type}
Engagement Value: ${document.engagement_value}M
Duration: {document.duration_months} months

Content:
{document.content[:2000]}

Key Outcomes:
{document.key_outcomes}

Provide a 3-4 sentence executive summary that captures the essence of this engagement."""

        if self.model == "anthropic":
            response = self.client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        elif self.model == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

    def extract_learnings(self, document: Document) -> list[str]:
        """Extract key learnings from an engagement."""
        prompt = f"""Extract the top 5 reusable learnings from this consulting engagement.
Each learning should be actionable and applicable to future engagements.

Title: {document.title}
Industry: {document.industry}
Content: {document.content[:2000]}
Key Outcomes: {document.key_outcomes}

Return each learning on a new line, numbered 1-5. Be concise (1-2 sentences per learning)."""

        if self.model == "anthropic":
            response = self.client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text
        elif self.model == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.choices[0].message.content

        learnings = []
        for line in text.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                cleaned = line.lstrip("0123456789.-) ").strip()
                if cleaned:
                    learnings.append(cleaned)

        return learnings

    def analyze_industry_trends(self, industry: str) -> str:
        """Analyze trends and patterns in an industry."""
        documents = self.kb.filter_by_industry(industry)
        if not documents:
            return f"No engagements found for industry: {industry}"

        engagement_summaries = "\n\n".join(
            [
                f"- {doc.title} ({doc.created_at.year}): {doc.key_outcomes}"
                for doc in documents[:10]
            ]
        )

        prompt = f"""Analyze the following consulting engagements in the {industry} industry
and identify key trends, recurring challenges, and success factors.

Engagements:
{engagement_summaries}

Provide insights on:
1. Industry Trends: What are the key trends in {industry}?
2. Common Challenges: What recurring issues do companies face?
3. Success Factors: What approaches have been most successful?
4. Future Outlook: What should we expect going forward?

Keep the analysis concise and focused."""

        if self.model == "anthropic":
            response = self.client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        elif self.model == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

    def _format_recommendations(self, recommendations) -> str:
        """Format recommendations for display."""
        formatted = []
        for i, rec in enumerate(recommendations, 1):
            formatted.append(
                f"{i}. {rec.reference_document.title}\n"
                f"   Industry: {rec.reference_document.industry}\n"
                f"   Type: {rec.reference_document.transaction_type}\n"
                f"   Relevance: {rec.relevance_score:.0%}\n"
                f"   Approach: {rec.suggested_approach or 'N/A'}\n"
                f"   Outcome: {rec.reference_document.key_outcomes}"
            )
        return "\n".join(formatted)
