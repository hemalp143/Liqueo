#!/usr/bin/env python3
"""
Load Sample Data into Liqueo Knowledge Base

This script loads the three synthetic sample engagements from sample_data.json
into the Liqueo knowledge base. Use this before the September 30th demo to
populate the system with example data.

Usage:
    python load_sample_data.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from liqueo.core import Document, KnowledgeBase


def load_sample_data():
    """Load sample engagements from sample_data.json into knowledge base."""

    # Load sample data
    sample_file = Path(__file__).parent / "sample_data.json"

    if not sample_file.exists():
        print(f"❌ Error: sample_data.json not found at {sample_file}")
        return False

    print(f"📂 Loading sample data from {sample_file}")

    try:
        with open(sample_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return False

    if not isinstance(data, list):
        print("❌ Error: sample_data.json should contain a list of documents")
        return False

    # Initialize knowledge base
    kb = KnowledgeBase()
    print(f"📚 Knowledge base initialized at {kb.storage_dir}")

    # Add each document
    added_count = 0
    for item in data:
        try:
            # Parse dates if they're strings
            created_at = item.get("created_at")
            updated_at = item.get("updated_at")

            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            if isinstance(updated_at, str):
                updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))

            # Create Document from JSON
            doc = Document(
                id=item.get("id", f"doc-{added_count}"),
                title=item.get("title", "Untitled"),
                content=item.get("content", ""),
                doc_type=item.get("doc_type", "engagement"),
                industry=item.get("industry", ""),
                transaction_type=item.get("transaction_type", ""),
                engagement_value=item.get("engagement_value", 0.0),
                duration_months=item.get("duration_months", 0),
                client_name=item.get("client_name", ""),
                consulting_approach=item.get("consulting_approach", ""),
                key_outcomes=item.get("key_outcomes", ""),
                tags=item.get("tags", []),
                created_at=created_at,
                updated_at=updated_at,
                metadata=item.get("metadata", {})
            )

            # Add to knowledge base
            kb.add_document(doc)
            print(f"✅ Added: {doc.title}")
            added_count += 1

        except Exception as e:
            print(f"⚠️  Error adding document: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"✨ Successfully loaded {added_count}/{len(data)} sample documents")
    print(f"{'='*60}\n")

    if added_count == 0:
        return False

    # Verify documents were added
    all_docs = kb.list_documents()
    print(f"📊 Total documents in knowledge base: {len(all_docs)}\n")

    print("📋 Loaded Engagements:")
    for doc in all_docs:
        print(f"  • {doc.title}")
        print(f"    Industry: {doc.industry}")
        print(f"    Value: ${doc.engagement_value}M | Duration: {doc.duration_months} months")
        print()

    return True


def verify_installation():
    """Verify Liqueo is installed and working."""
    try:
        from liqueo import KnowledgeBase, Document
        print("✅ Liqueo modules imported successfully\n")
        return True
    except ImportError as e:
        print(f"❌ Error importing Liqueo: {e}")
        print("\n💡 Fix: Install Liqueo first")
        print("   pip install -e .")
        return False


def main():
    """Main entry point."""
    print(f"{'='*60}")
    print("🧠 Liqueo Sample Data Loader")
    print(f"{'='*60}\n")

    # Verify installation
    if not verify_installation():
        sys.exit(1)

    # Load sample data
    success = load_sample_data()

    if success:
        print("🎉 Ready for demo!")
        print("\n📖 Next steps:")
        print("  1. Start web UI: streamlit run app.py")
        print("  2. Go to 'Knowledge Workflow' tab")
        print("  3. Follow DEMO_SCENARIO.md script for 30-minute demo")
        sys.exit(0)
    else:
        print("❌ Failed to load sample data")
        sys.exit(1)


if __name__ == "__main__":
    main()
