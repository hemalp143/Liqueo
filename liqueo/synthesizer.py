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
        self.client = None
        self._client_error = None
        self._init_client()

    def _init_client(self):
        """Initialize LLM client (lazy - will retry on use)."""
        try:
            if self.model == "anthropic":
                from anthropic import Anthropic
                self.client = Anthropic()
            elif self.model == "openai":
                from openai import OpenAI
                self.client = OpenAI()
            else:
                self._client_error = f"Unknown model: {self.model}"
        except ImportError as e:
            self._client_error = f"SDK not installed: {e}"
        except Exception as e:
            self._client_error = str(e)

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

        # If no LLM available, provide manual synthesis
        if not self.client:
            return self._manual_synthesis(engagement_description, recommendations)

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

        try:
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
        except Exception as e:
            print(f"Warning: LLM synthesis failed: {e}")
            return self._manual_synthesis(engagement_description, recommendations)

    def generate_engagement_summary(self, document: Document) -> str:
        """Generate a concise summary of an engagement."""
        if not self.client:
            return self._manual_summary(document)

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

        try:
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
        except Exception as e:
            print(f"Warning: Summary generation failed: {e}")
            return self._manual_summary(document)

    def _manual_summary(self, document: Document) -> str:
        """Generate summary without LLM."""
        summary = f"{document.title}. "
        if document.industry:
            summary += f"Industry: {document.industry}. "
        if document.transaction_type:
            summary += f"Type: {document.transaction_type}. "
        if document.key_outcomes:
            summary += f"Outcomes: {document.key_outcomes}"
        return summary

    def extract_learnings(self, document: Document) -> list[str]:
        """Extract key learnings from an engagement."""
        if not self.client:
            return self._manual_learnings(document)

        prompt = f"""Extract the top 5 reusable learnings from this consulting engagement.
Each learning should be actionable and applicable to future engagements.

Title: {document.title}
Industry: {document.industry}
Content: {document.content[:2000]}
Key Outcomes: {document.key_outcomes}

Return each learning on a new line, numbered 1-5. Be concise (1-2 sentences per learning)."""

        try:
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
        except Exception as e:
            print(f"Warning: Learning extraction failed: {e}")
            return self._manual_learnings(document)

    def _manual_learnings(self, document: Document) -> list[str]:
        """Extract learnings without LLM."""
        learnings = []

        if document.key_outcomes:
            learnings.append(f"Key outcome: {document.key_outcomes[:100]}")

        if document.consulting_approach:
            learnings.append(f"Approach used: {document.consulting_approach[:100]}")

        if document.industry:
            learnings.append(f"Industry {document.industry} - evaluate market conditions early")

        if document.transaction_type:
            learnings.append(f"For {document.transaction_type} engagements - focus on stakeholder alignment")

        if document.duration_months:
            learnings.append(f"Timeline: Similar engagements took ~{document.duration_months} months")

        return learnings[:5]

    def analyze_industry_trends(self, industry: str) -> str:
        """Analyze trends and patterns in an industry."""
        documents = self.kb.filter_by_industry(industry)
        if not documents:
            return f"No engagements found for industry: {industry}"

        if not self.client:
            return self._manual_industry_analysis(industry, documents)

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

        try:
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
        except Exception as e:
            print(f"Warning: Industry analysis failed: {e}")
            return self._manual_industry_analysis(industry, documents)

    def _manual_industry_analysis(self, industry: str, documents) -> str:
        """Analyze industry without LLM."""
        output = [f"\n📊 INDUSTRY ANALYSIS: {industry}\n"]

        output.append("1. INDUSTRY TRENDS:")
        output.append(f"   • Active market with {len(documents)} engagements on record")
        transaction_types = set(d.transaction_type for d in documents if d.transaction_type)
        if transaction_types:
            output.append(f"   • Primary activity types: {', '.join(list(transaction_types)[:3])}")
        output.append(f"   • Average engagement value: ${sum(d.engagement_value or 0 for d in documents) / max(len(documents), 1):.1f}M")

        output.append("\n2. COMMON CHALLENGES:")
        outcomes = [d.key_outcomes for d in documents if d.key_outcomes]
        if "cost" in str(outcomes).lower():
            output.append("   • Cost optimization and operational efficiency")
        if "technology" in str(outcomes).lower():
            output.append("   • Technology modernization and integration")
        output.append("   • Change management and stakeholder alignment")

        output.append("\n3. SUCCESS FACTORS:")
        approaches = set(d.consulting_approach for d in documents if d.consulting_approach)
        for approach in list(approaches)[:3]:
            output.append(f"   • {approach}")
        if not approaches:
            output.append("   • Structured analytical approach")
            output.append("   • Stakeholder engagement strategy")

        output.append("\n4. FUTURE OUTLOOK:")
        avg_duration = sum(d.duration_months or 0 for d in documents) / max(len(documents), 1)
        output.append(f"   • Engagements typically span {int(avg_duration)}-{int(avg_duration*1.5)} months")
        output.append("   • Continued focus on operational and digital transformation")
        output.append("   • Increased emphasis on sustainability and ESG considerations")

        output.append("\n📝 Note: Analysis based on metadata. LLM synthesis not available.")
        return "\n".join(output)

    def _manual_synthesis(self, description: str, recommendations) -> str:
        """Provide synthesis without LLM when API unavailable."""
        output = [
            "📊 SYNTHESIS REPORT (Generated from similar engagements)\n",
            f"Engagement: {description}\n",
        ]

        if recommendations:
            output.append(f"✓ Found {len(recommendations)} similar engagement(s)\n")

            output.append("\n1. KEY INSIGHTS:")
            for rec in recommendations:
                if rec.reference_document.key_outcomes:
                    output.append(f"   • {rec.reference_document.key_outcomes[:100]}...")

            output.append("\n2. RECOMMENDED APPROACH:")
            approaches = [rec.suggested_approach for rec in recommendations if rec.suggested_approach]
            if approaches:
                for approach in list(set(approaches))[:3]:
                    output.append(f"   • {approach}")
            else:
                output.append("   • Data-driven analysis and stakeholder engagement")

            output.append("\n3. POTENTIAL RISKS:")
            challenges = [rec.potential_challenges for rec in recommendations if rec.potential_challenges]
            if challenges:
                for challenge in list(set(challenges))[:3]:
                    output.append(f"   • {challenge}")
            else:
                output.append("   • Resource availability and timeline pressure")

            output.append("\n4. RESOURCE ALLOCATION:")
            efforts = [rec.estimated_effort for rec in recommendations if rec.estimated_effort]
            if efforts:
                output.append(f"   • {efforts[0]}")
            else:
                output.append("   • Recommend 3-4 senior consultants, 6-9 month timeline")

            output.append("\n5. TIMELINE:")
            durations = [rec.reference_document.duration_months for rec in recommendations
                        if rec.reference_document.duration_months]
            if durations:
                avg_duration = sum(durations) / len(durations)
                output.append(f"   • Based on {len(durations)} similar cases: ~{int(avg_duration)} months")
            else:
                output.append("   • Recommend 6-9 month engagement timeline")

        output.append("\n📝 Note: LLM synthesis not available. Results based on metadata analysis.")
        return "\n".join(output)

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
