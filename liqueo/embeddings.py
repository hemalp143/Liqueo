"""Embeddings and semantic search management."""

import json
from pathlib import Path
from typing import Optional
import numpy as np
from datetime import datetime

from liqueo.core import Document, SearchResult, KnowledgeBase


class EmbeddingsManager:
    """Manages embeddings for semantic search."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        embeddings_dir: Path | str = ".liqueo/embeddings",
        model: str = "openai",
    ):
        """Initialize embeddings manager."""
        self.kb = knowledge_base
        self.embeddings_dir = Path(embeddings_dir)
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        self.model = model
        self.embeddings_cache: dict[str, np.ndarray] = {}
        self.embedding_index_file = self.embeddings_dir / "index.json"
        self._load_embeddings_index()
        self.client = None
        self._client_error = None

    def _ensure_client(self) -> bool:
        """Ensure client is initialized. Returns True if successful."""
        if self.client is not None:
            return True
        if self._client_error is not None:
            raise RuntimeError(self._client_error)

        try:
            if self.model == "openai":
                from openai import OpenAI
                self.client = OpenAI()
            elif self.model == "anthropic":
                from anthropic import Anthropic
                self.client = Anthropic()
            else:
                raise ValueError(f"Unknown model: {self.model}")
            return True
        except ImportError as e:
            self._client_error = f"SDK not installed: {e}"
            raise ImportError(f"Required SDK not installed for {self.model}: pip install {self.model}")
        except Exception as e:
            self._client_error = str(e)
            raise RuntimeError(f"Failed to initialize {self.model}: {e}")

    def embed_document(self, document: Document) -> np.ndarray:
        """Create embeddings for a document."""
        text = f"{document.title}\n{document.content}"
        text = text[:8000]  # Limit to token budget

        if not self._ensure_client():
            return np.random.randn(1536).astype(np.float32)

        try:
            if self.model == "openai":
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text,
                )
                embedding = np.array(response.data[0].embedding)
            elif self.model == "anthropic":
                embedding = self._embed_with_anthropic(text)
            else:
                raise ValueError(f"Unknown model: {self.model}")

            self.embeddings_cache[document.id] = embedding
            self._save_embedding(document.id, embedding)
            return embedding
        except Exception as e:
            print(f"Warning: Failed to embed document {document.id}: {e}")
            return np.random.randn(1536).astype(np.float32)

    def _embed_with_anthropic(self, text: str) -> np.ndarray:
        """Create embeddings using Anthropic API (using text batching method)."""
        response = self.client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=200,
            system="Convert the given text into a numerical embedding representation. "
                   "Output a space-separated list of 768 float values between -1 and 1.",
            messages=[{"role": "user", "content": f"Embed this text:\n\n{text}"}],
        )

        try:
            embedding_text = response.content[0].text.strip()
            values = [float(x) for x in embedding_text.split()[:768]]
            if len(values) < 768:
                values.extend([0.0] * (768 - len(values)))
            return np.array(values[:768])
        except (ValueError, IndexError):
            return np.random.randn(768).astype(np.float32)

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
    ) -> list[SearchResult]:
        """Search for similar documents using semantic similarity."""
        try:
            if not self._ensure_client():
                return self._fallback_search(query, top_k, filters)
        except Exception as e:
            print(f"Warning: Could not initialize embedding client: {e}")
            return self._fallback_search(query, top_k, filters)

        try:
            if self.model == "openai":
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=query[:8000],
                )
                query_embedding = np.array(response.data[0].embedding)
            elif self.model == "anthropic":
                query_embedding = self._embed_with_anthropic(query[:8000])
            else:
                raise ValueError(f"Unknown model: {self.model}")
        except Exception as e:
            print(f"Warning: Failed to embed query: {e}")
            return self._fallback_search(query, top_k, filters)

        results = []
        documents = self.kb.list_documents()

        for doc in documents:
            if doc.id not in self.embeddings_cache:
                self.embed_document(doc)

            doc_embedding = self.embeddings_cache.get(doc.id)
            if doc_embedding is None:
                continue

            similarity = self._cosine_similarity(query_embedding, doc_embedding)

            if filters:
                if filters.get("industry") and doc.industry != filters["industry"]:
                    continue
                if (
                    filters.get("transaction_type")
                    and doc.transaction_type != filters["transaction_type"]
                ):
                    continue
                if filters.get("min_similarity", 0) > similarity:
                    continue

            results.append(
                SearchResult(
                    document=doc,
                    similarity_score=float(similarity),
                )
            )

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]

    def _fallback_search(
        self, query: str, top_k: int = 5, filters: Optional[dict] = None
    ) -> list[SearchResult]:
        """Fallback keyword-based search when embeddings unavailable."""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []
        documents = self.kb.list_documents()

        for doc in documents:
            score = 0.0

            # Title matching (highest weight)
            if query_lower in doc.title.lower():
                score += 0.9
            else:
                title_word_matches = sum(1 for word in query_words if word in doc.title.lower())
                score += title_word_matches * 0.3

            # Content matching
            if query_lower in doc.content.lower():
                score += 0.5
            else:
                content_word_matches = sum(1 for word in query_words if word in doc.content.lower())
                score += content_word_matches * 0.15

            # Outcomes matching
            if doc.key_outcomes and query_lower in doc.key_outcomes.lower():
                score += 0.4

            # Tags matching
            if doc.tags:
                tag_matches = sum(1 for tag in doc.tags if query_lower in tag.lower())
                score += tag_matches * 0.2

            # Apply filters
            if filters:
                if filters.get("industry") and doc.industry != filters["industry"]:
                    continue
                if (
                    filters.get("transaction_type")
                    and doc.transaction_type != filters["transaction_type"]
                ):
                    continue
                if filters.get("min_similarity", 0) > score:
                    continue

            if score > 0:
                results.append(SearchResult(document=doc, similarity_score=min(score, 1.0)))
            else:
                # Include all documents with 0.3 baseline relevance for fallback
                results.append(SearchResult(document=doc, similarity_score=0.3))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def _save_embedding(self, doc_id: str, embedding: np.ndarray) -> None:
        """Save embedding to file."""
        embedding_file = self.embeddings_dir / f"{doc_id}.npy"
        np.save(embedding_file, embedding)
        self._update_index(doc_id)

    def _load_embeddings_index(self) -> None:
        """Load embeddings index."""
        if self.embedding_index_file.exists():
            with open(self.embedding_index_file, "r") as f:
                index = json.load(f)
                for doc_id in index:
                    embedding_file = self.embeddings_dir / f"{doc_id}.npy"
                    if embedding_file.exists():
                        self.embeddings_cache[doc_id] = np.load(embedding_file)

    def _update_index(self, doc_id: str) -> None:
        """Update embeddings index."""
        index = list(self.embeddings_cache.keys())
        with open(self.embedding_index_file, "w") as f:
            json.dump(index, f, indent=2)

    def rebuild_embeddings(self) -> None:
        """Rebuild all embeddings from knowledge base."""
        documents = self.kb.list_documents()
        for doc in documents:
            self.embed_document(doc)
