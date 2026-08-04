"""Basic usage example of Liqueo."""

from pathlib import Path
from liqueo.core import Document, KnowledgeBase
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer


def main():
    """Demonstrate Liqueo functionality."""

    # Initialize knowledge base
    kb = KnowledgeBase(storage_dir=".liqueo")

    # Create sample documents
    sample_docs = [
        Document(
            id="tech-ma-2024-001",
            title="SaaS Company Acquisition - Tech Stack Valuation",
            content="""
            Engagement: Valuation and due diligence for enterprise SaaS acquisition

            Approach: Deep dive into technology stack, security posture, scalability
            - Analyzed 500+ code repositories
            - Evaluated architectural decisions
            - Assessed technical debt and refactoring needs

            Key Metrics:
            - Tech score: 8.5/10
            - Scalability rating: High
            - Security assessment: Robust

            Outcome: Valuation adjustment of $50M based on technology premium
            """,
            doc_type="engagement",
            industry="Technology",
            transaction_type="M&A",
            engagement_value=2.5,
            duration_months=8,
            client_name="Global Equity Partners",
            consulting_approach="Deep-dive technical analysis with cloud infrastructure focus",
            key_outcomes="Identified $50M technology premium; secured favorable valuation; reduced risk through technical due diligence",
            tags=["SaaS", "cloud", "due-diligence"],
        ),
        Document(
            id="retail-restr-2023-001",
            title="Retail Chain Restructuring - Technology Consolidation",
            content="""
            Engagement: Organizational restructuring and technology rationalization

            Challenge: Legacy systems across 200+ stores, redundant platforms

            Solution:
            1. Consolidate POS systems into unified platform
            2. Migrate data warehouses to cloud
            3. Optimize workforce through automation

            Impact:
            - Reduced IT costs by 35%
            - Improved customer experience
            - Faster decision-making
            """,
            doc_type="case_study",
            industry="Retail",
            transaction_type="Restructuring",
            engagement_value=1.8,
            duration_months=12,
            client_name="RetailCo Inc",
            consulting_approach="Process optimization with technology modernization",
            key_outcomes="35% IT cost reduction; improved omnichannel capabilities; workforce redeployment",
            tags=["restructuring", "cost-reduction", "digital-transformation"],
        ),
        Document(
            id="finance-reorg-2024-001",
            title="Investment Bank Back-Office Reorganization",
            content="""
            Engagement: Back-office reorganization for efficiency

            Starting State:
            - 500 FTE in back-office
            - 15% manual processes
            - Siloed departments

            Transformation:
            1. Automated 80% of manual processes
            2. Centralized operations
            3. Implemented shared service model

            Results:
            - 25% headcount reduction
            - 40% faster processing
            - 50% error reduction
            """,
            doc_type="engagement",
            industry="Financial Services",
            transaction_type="Restructuring",
            engagement_value=3.0,
            duration_months=10,
            client_name="Global Investment Bank",
            consulting_approach="Lean six sigma with automation focus",
            key_outcomes="25% headcount reduction; 40% faster processing; robust controls",
            tags=["automation", "lean", "operations"],
        ),
    ]

    # Add documents to knowledge base
    for doc in sample_docs:
        kb.add_document(doc)
        print(f"Added: {doc.title}")

    # Initialize embeddings manager
    try:
        embeddings = EmbeddingsManager(kb, model="anthropic")
        print("\nGenerating embeddings...")
        for doc in sample_docs:
            embeddings.embed_document(doc)
        print("✓ Embeddings generated")
    except Exception as e:
        print(f"Note: Embeddings require API key: {e}")
        return

    # Perform semantic search
    print("\n--- Semantic Search Example ---")
    query = "We need to streamline our technology infrastructure and reduce costs"
    search_results = embeddings.semantic_search(query, top_k=2)

    for result in search_results:
        print(f"\n{result.document.title}")
        print(f"Relevance: {result.similarity_score:.0%}")

    # Get recommendations
    print("\n--- Recommendations Example ---")
    recommender = RecommendationEngine(embeddings)

    engagement_desc = """
    We have a fintech startup that needs to optimize its core banking system
    and reduce operational costs while maintaining security and compliance.
    Industry: Financial Services, Transaction Type: Restructuring
    """

    recommendations = recommender.recommend_similar_engagements(engagement_desc, top_k=2)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.reference_document.title}")
        print(f"   Relevance: {rec.relevance_score:.0%}")
        print(f"   Reasoning: {rec.reasoning}")
        if rec.estimated_effort:
            print(f"   Effort: {rec.estimated_effort}")

    # Synthesize insights (requires LLM API)
    print("\n--- Knowledge Synthesis Example ---")
    try:
        synthesizer = KnowledgeSynthesizer(kb, recommender, model="anthropic")
        insights = synthesizer.synthesize_recommendations(engagement_desc, top_k=2)
        print(insights)
    except Exception as e:
        print(f"Note: Synthesis requires API key: {e}")

    # List all documents
    print("\n--- Knowledge Base Summary ---")
    print(f"Total documents: {len(kb.list_documents())}")
    industries = set(doc.industry for doc in kb.list_documents())
    print(f"Industries: {', '.join(industries)}")

    transaction_types = set(
        doc.transaction_type for doc in kb.list_documents() if doc.transaction_type
    )
    print(f"Transaction types: {', '.join(transaction_types)}")


if __name__ == "__main__":
    main()
