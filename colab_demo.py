#!/usr/bin/env python3
"""
Liqueo Demo - Run on Google Colab or locally
Copy this entire script and paste into Colab's code cell
"""

import subprocess
import sys

# Step 1: Install dependencies
print("📦 Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "anthropic", "openai", "click", "rich", "numpy", "pandas", "langchain"],
               check=False)

# Step 2: Clone Liqueo
print("📥 Cloning Liqueo...")
subprocess.run(["git", "clone", "-q", "https://github.com/hemalp143/Liqueo.git"],
               check=False)
sys.path.insert(0, '/content/Liqueo')

# Step 3: Import modules
print("📚 Importing Liqueo modules...")
from liqueo.core import Document, KnowledgeBase, generate_doc_id
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer
from datetime import datetime

print("✅ Setup complete!\n")

# Step 4: Create knowledge base
print("=" * 80)
print("STEP 1: Initialize Knowledge Base")
print("=" * 80)

kb = KnowledgeBase()

docs_data = [
    {
        'title': 'SaaS Company Acquisition - Tech Stack Valuation',
        'industry': 'Technology',
        'type': 'M&A',
        'value': 2.5,
        'duration': 8,
        'content': 'Acquired high-growth SaaS company. Identified $50M technology premium.',
        'outcomes': 'Secured favorable valuation; reduced risk'
    },
    {
        'title': 'Retail Chain Restructuring - Technology Consolidation',
        'industry': 'Retail',
        'type': 'Restructuring',
        'value': 1.8,
        'duration': 12,
        'content': 'Consolidated e-commerce, POS, and inventory systems.',
        'outcomes': '35% IT cost reduction; improved omnichannel'
    },
    {
        'title': 'Investment Bank Back-Office Reorganization',
        'industry': 'Financial Services',
        'type': 'Restructuring',
        'value': 3.2,
        'duration': 10,
        'content': 'Reorganized back-office operations across 5 continents.',
        'outcomes': '40% reduction in back-office costs'
    }
]

for doc_data in docs_data:
    doc = Document(
        id=generate_doc_id(doc_data['title'], datetime.now()),
        title=doc_data['title'],
        industry=doc_data['industry'],
        transaction_type=doc_data['type'],
        engagement_value=doc_data['value'],
        duration_months=doc_data['duration'],
        content=doc_data['content'],
        key_outcomes=doc_data['outcomes']
    )
    kb.add_document(doc)

print(f"✓ Loaded {len(kb.list_documents())} consulting engagements\n")

# Step 5: Semantic Search
print("=" * 80)
print("STEP 2: Semantic Search")
print("=" * 80)

embeddings = EmbeddingsManager(kb)
query = "We need to optimize technology infrastructure and reduce costs"
print(f"Query: {query}\n")

results = embeddings.semantic_search(query, top_k=3)
for i, result in enumerate(results, 1):
    doc = result.document
    print(f"{i}. {doc.title}")
    print(f"   Industry: {doc.industry}")
    print(f"   Relevance: {result.similarity_score:.0%}\n")

# Step 6: Recommendations
print("=" * 80)
print("STEP 3: Intelligent Recommendations")
print("=" * 80)

recommender = RecommendationEngine(embeddings)
engagement = "Fintech startup needs core banking optimization with cost reduction"
print(f"Engagement: {engagement}\n")

recommendations = recommender.recommend_similar_engagements(engagement, top_k=3)
for i, rec in enumerate(recommendations, 1):
    doc = rec.reference_document
    print(f"{i}. {doc.title}")
    print(f"   Relevance: {rec.relevance_score:.0%}")
    if rec.suggested_approach:
        print(f"   Approach: {rec.suggested_approach}")
    if rec.estimated_effort:
        print(f"   Effort: {rec.estimated_effort}")
    print()

# Step 7: Knowledge Synthesis
print("=" * 80)
print("STEP 4: Knowledge Synthesis & Insights")
print("=" * 80)

synthesizer = KnowledgeSynthesizer(kb, recommender)
new_engagement = "Healthcare provider digital transformation with 25% cost reduction goal"
print(f"Engagement: {new_engagement}\n")

synthesis = synthesizer.synthesize_recommendations(new_engagement, top_k=3)
print(synthesis)
print()

# Step 8: Industry Analysis
print("=" * 80)
print("STEP 5: Industry Analysis")
print("=" * 80)

analysis = synthesizer.analyze_industry_trends("Technology")
print(analysis)

print("\n" + "=" * 80)
print("✅ DEMO COMPLETE")
print("=" * 80)
print("\nLiqueo provides:")
print("  • Semantic search for similar consulting engagements")
print("  • Intelligent recommendations with effort estimates")
print("  • AI-powered synthesis and strategic insights")
print("  • Industry trend analysis")
print("\nAll features work WITHOUT API keys! 🚀")
