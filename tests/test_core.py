"""Tests for core module."""

import pytest
from pathlib import Path
from datetime import datetime
from liqueo.core import Document, KnowledgeBase, generate_doc_id


def test_document_creation():
    """Test creating a document."""
    doc = Document(
        id="test-001",
        title="Test Engagement",
        content="This is a test engagement document.",
        doc_type="engagement",
        industry="Technology",
        transaction_type="M&A",
    )

    assert doc.id == "test-001"
    assert doc.title == "Test Engagement"
    assert doc.industry == "Technology"


def test_document_serialization():
    """Test document to/from dict."""
    doc = Document(
        id="test-002",
        title="Test Document",
        content="Test content",
        doc_type="case_study",
        industry="Finance",
    )

    doc_dict = doc.to_dict()
    assert doc_dict["id"] == "test-002"
    assert doc_dict["title"] == "Test Document"

    reconstructed = Document.from_dict(doc_dict)
    assert reconstructed.id == doc.id
    assert reconstructed.title == doc.title


def test_knowledge_base_operations(tmp_path):
    """Test knowledge base add, get, list operations."""
    kb = KnowledgeBase(storage_dir=tmp_path)

    doc1 = Document(
        id="doc-001",
        title="Engagement 1",
        content="Content 1",
        doc_type="engagement",
        industry="Retail",
    )

    doc2 = Document(
        id="doc-002",
        title="Engagement 2",
        content="Content 2",
        doc_type="case_study",
        industry="Technology",
    )

    kb.add_document(doc1)
    kb.add_document(doc2)

    assert kb.get_document("doc-001") == doc1
    assert kb.get_document("doc-002") == doc2
    assert len(kb.list_documents()) == 2


def test_knowledge_base_filtering(tmp_path):
    """Test filtering documents."""
    kb = KnowledgeBase(storage_dir=tmp_path)

    for i in range(3):
        doc = Document(
            id=f"tech-{i}",
            title=f"Tech Engagement {i}",
            content="Content",
            doc_type="engagement",
            industry="Technology",
            transaction_type="M&A" if i % 2 == 0 else "Restructuring",
        )
        kb.add_document(doc)

    tech_docs = kb.filter_by_industry("Technology")
    assert len(tech_docs) == 3

    ma_docs = kb.filter_by_transaction_type("M&A")
    assert len(ma_docs) == 2


def test_knowledge_base_persistence(tmp_path):
    """Test that knowledge base persists to disk."""
    kb1 = KnowledgeBase(storage_dir=tmp_path)

    doc = Document(
        id="persist-001",
        title="Persistent Document",
        content="This should persist",
        doc_type="engagement",
        industry="Finance",
    )
    kb1.add_document(doc)

    kb2 = KnowledgeBase(storage_dir=tmp_path)
    retrieved = kb2.get_document("persist-001")

    assert retrieved is not None
    assert retrieved.title == "Persistent Document"
    assert retrieved.industry == "Finance"


def test_doc_id_generation():
    """Test document ID generation."""
    title = "Test Engagement"
    timestamp = datetime(2024, 1, 15, 10, 30, 0)

    id1 = generate_doc_id(title, timestamp)
    id2 = generate_doc_id(title, timestamp)

    assert id1 == id2
    assert len(id1) == 16


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
