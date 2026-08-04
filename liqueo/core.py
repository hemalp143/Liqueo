"""Core data structures and knowledge base management."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
import json
import hashlib


@dataclass
class Document:
    """Represents a consulting document or engagement record."""

    id: str
    title: str
    content: str
    doc_type: str  # e.g., "engagement", "case_study", "template", "proposal"
    industry: Optional[str] = None
    transaction_type: Optional[str] = None  # e.g., "M&A", "Restructuring", "Valuation"
    engagement_value: Optional[float] = None  # in millions
    duration_months: Optional[int] = None
    client_name: Optional[str] = None
    consulting_approach: Optional[str] = None
    key_outcomes: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "doc_type": self.doc_type,
            "industry": self.industry,
            "transaction_type": self.transaction_type,
            "engagement_value": self.engagement_value,
            "duration_months": self.duration_months,
            "client_name": self.client_name,
            "consulting_approach": self.consulting_approach,
            "key_outcomes": self.key_outcomes,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Document":
        """Create document from dictionary."""
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)


@dataclass
class SearchResult:
    """Result from a semantic search query."""

    document: Document
    similarity_score: float
    matched_sections: list[str] = field(default_factory=list)
    relevance_reasoning: Optional[str] = None


class KnowledgeBase:
    """Manages storage and retrieval of documents."""

    def __init__(self, storage_dir: Path | str = ".liqueo/knowledge"):
        """Initialize knowledge base with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir = self.storage_dir / "documents"
        self.docs_dir.mkdir(exist_ok=True)
        self.index_file = self.storage_dir / "index.json"
        self._documents: dict[str, Document] = {}
        self._load_index()

    def add_document(self, document: Document) -> None:
        """Add or update a document in the knowledge base."""
        self._documents[document.id] = document
        self._save_document(document)
        self._save_index()

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieve a document by ID."""
        return self._documents.get(doc_id)

    def list_documents(self) -> list[Document]:
        """List all documents."""
        return list(self._documents.values())

    def filter_by_industry(self, industry: str) -> list[Document]:
        """Filter documents by industry."""
        return [doc for doc in self._documents.values() if doc.industry == industry]

    def filter_by_transaction_type(self, transaction_type: str) -> list[Document]:
        """Filter documents by transaction type."""
        return [
            doc for doc in self._documents.values()
            if doc.transaction_type == transaction_type
        ]

    def filter_by_tags(self, tags: list[str]) -> list[Document]:
        """Filter documents by tags (any tag match)."""
        return [
            doc for doc in self._documents.values()
            if any(tag in doc.tags for tag in tags)
        ]

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document."""
        if doc_id not in self._documents:
            return False
        del self._documents[doc_id]
        doc_file = self.docs_dir / f"{doc_id}.json"
        if doc_file.exists():
            doc_file.unlink()
        self._save_index()
        return True

    def _save_document(self, document: Document) -> None:
        """Save document to file."""
        doc_file = self.docs_dir / f"{document.id}.json"
        with open(doc_file, "w") as f:
            json.dump(document.to_dict(), f, indent=2)

    def _load_index(self) -> None:
        """Load index and documents from storage."""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                doc_ids = json.load(f)
                for doc_id in doc_ids:
                    doc_file = self.docs_dir / f"{doc_id}.json"
                    if doc_file.exists():
                        with open(doc_file, "r") as df:
                            data = json.load(df)
                            self._documents[doc_id] = Document.from_dict(data)

    def _save_index(self) -> None:
        """Save index file."""
        with open(self.index_file, "w") as f:
            json.dump(list(self._documents.keys()), f, indent=2)


def generate_doc_id(title: str, timestamp: datetime) -> str:
    """Generate unique document ID."""
    content = f"{title}{timestamp.isoformat()}".encode()
    return hashlib.sha256(content).hexdigest()[:16]
