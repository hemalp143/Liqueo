# Liqueo Architecture Visualization

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           USER APPLICATIONS                                 │
│  (CLI, Web App, Python Scripts, Integration Code)                          │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ imports
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                        LIQUEO TOOLKIT (Public API)                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      ORCHESTRATION LAYER                              │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │  KnowledgeSynthesizer                                          │  │  │
│  │  │  - Orchestrates discovery & synthesis workflows               │  │  │
│  │  │  - Combines search + recommendations + LLM                    │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      BUSINESS LOGIC LAYER                             │  │
│  │  ┌─────────────────────────┐  ┌─────────────────────────────────┐   │  │
│  │  │ RecommendationEngine    │  │ KnowledgeBase                  │   │  │
│  │  │ - Similar engagements   │  │ - Document repository          │   │  │
│  │  │ - Pattern matching      │  │ - Filtering & indexing         │   │  │
│  │  │ - Effort estimation     │  │ - Persistence management       │   │  │
│  │  └─────────────────────────┘  └─────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      SERVICE LAYER                                    │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │ EmbeddingsManager (Semantic Search Core)                       │  │  │
│  │  │ - Embedding generation                                        │  │  │
│  │  │ - Vector similarity computation                               │  │  │
│  │  │ - Embedding cache management                                  │  │  │
│  │  │ - Multi-provider support                                      │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      DATA MODEL LAYER                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │  │  Document    │  │SearchResult  │  │Recommendation│               │  │
│  │  │              │  │              │  │              │               │  │
│  │  │- id          │  │- document    │  │- reference   │               │  │
│  │  │- title       │  │- similarity  │  │- relevance   │               │  │
│  │  │- content     │  │- sections    │  │- reasoning   │               │  │
│  │  │- industry    │  │- reasoning   │  │- approach    │               │  │
│  │  │- type        │  │              │  │- challenges  │               │  │
│  │  │- value       │  │              │  │- effort      │               │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      INTERFACE LAYER                                 │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │ CLI Commands (liqueo/cli.py)                                  │  │  │
│  │  │ add | search | recommend | synthesize | analyze | list | view │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
        │ External APIs    │ │ Local Storage│ │ Cache Layer  │
        ├──────────────────┤ ├──────────────┤ ├──────────────┤
        │ • OpenAI         │ │ • .liqueo/   │ │ • Embeddings │
        │ • Anthropic      │ │ • documents/ │ │ • Metadata   │
        │                  │ │ • embeddings/│ │ • Index      │
        └──────────────────┘ └──────────────┘ └──────────────┘
```

---

## Component Dependency Graph

```
        ┌─────────────────────────────────────────────┐
        │    User Application Code                    │
        │    (Your consulting tools)                  │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────┴───────────────────────┐
        │                                           │
        ▼                                           ▼
    ┌─────────────────┐                  ┌──────────────────┐
    │  KnowledgeBase  │                  │ CLI Interface    │
    │                 │                  │                  │
    │ - add_document()│                  │ - add command    │
    │ - get_document()│                  │ - search command │
    │ - filter_*()    │                  │ - recommend cmd  │
    │ - list_docs()   │                  └────────┬─────────┘
    └────────┬────────┘                           │
             │                                     │
             │                    ┌────────────────┘
             │                    │
             ▼                    ▼
    ┌──────────────────────────────────────┐
    │      RecommendationEngine            │
    │                                      │
    │ - recommend_similar_engagements()   │
    │ - recommend_by_industry()            │
    │ - recommend_by_transaction_type()   │
    │ - find_patterns()                    │
    └────────────┬───────────────┬────────┘
                 │               │
                 │               │
                 ▼               ▼
    ┌──────────────────────────────────────┐
    │      EmbeddingsManager               │
    │                                      │
    │ - embed_document()                   │
    │ - semantic_search()                  │
    │ - cosine_similarity()                │
    │ - cache management                   │
    └────────┬──────────────────┬──────────┘
             │                  │
    ┌────────▼────┐    ┌────────▼────────┐
    │ OpenAI API  │    │ Anthropic API   │
    │ (pluggable) │    │ (pluggable)     │
    └─────────────┘    └─────────────────┘
             │                  │
             └────────┬─────────┘
                      ▼
          ┌───────────────────────┐
          │ Vector Embeddings     │
          │ (768-dim vectors)     │
          └───────────────────────┘


    ┌──────────────────────────────────────┐
    │      KnowledgeSynthesizer            │
    │                                      │
    │ - synthesize_recommendations()       │
    │ - generate_engagement_summary()      │
    │ - extract_learnings()                │
    │ - analyze_industry_trends()          │
    └────┬──────────────────────┬──────────┘
         │                      │
    ┌────▼─────┐        ┌───────▼────────┐
    │OpenAI GPT│        │ Anthropic      │
    │(pluggable)│       │ Claude API     │
    └──────────┘        │ (pluggable)    │
                        └────────────────┘
```

---

## Data Flow Sequences

### Sequence 1: Document Ingestion & Embedding

```
User/Application
        │
        │ add_document(doc)
        ├──────────────────────────────────────────┐
        │                                           │
        ▼                                           │
    KnowledgeBase                                   │
        │                                           │
        ├─ Validate document                       │
        ├─ Add to memory index                     │
        ├─ Persist to disk (.liqueo/documents/)    │
        ├─ Update index.json                       │
        │                                           │
        └──────────────────────┬──────────────────┘
                               │
                               │ (optional) embed_document(doc)
                               ▼
                        EmbeddingsManager
                               │
                               ├─ Extract text from document
                               ├─ Call embedding API (OpenAI/Anthropic)
                               ├─ Get 768-dim vector
                               ├─ Cache in memory
                               ├─ Persist to disk (.liqueo/embeddings/)
                               │
                               └─ ✓ Document is searchable
```

### Sequence 2: Semantic Search

```
User Query
    │
    │ "technology valuation acquisition"
    │
    ▼
EmbeddingsManager.semantic_search()
    │
    ├─ Generate query embedding (API or cache)
    │
    ├─ For each document in knowledge base:
    │   ├─ Load/generate embedding (cached)
    │   ├─ Compute: cos_sim(query_vec, doc_vec)
    │   ├─ Score document
    │   ├─ Apply filters (industry, type, etc.)
    │   └─ Track result
    │
    ├─ Sort by similarity score (DESC)
    ├─ Return top-k results
    │
    ▼
SearchResult[] 
    {
        document: Document,
        similarity_score: 0.89,
        matched_sections: [...]
    }
```

### Sequence 3: Recommendation Generation

```
User Request (engagement description)
    │
    │ "Optimize fintech backend infrastructure"
    │
    ▼
RecommendationEngine.recommend_similar_engagements()
    │
    ├─ Call EmbeddingsManager.semantic_search()
    │   └─ Get similar documents
    │
    ├─ For each result:
    │   ├─ Extract consulting_approach field
    │   ├─ Extract key_outcomes field
    │   ├─ Estimate effort from duration/value
    │   ├─ Generate reasoning
    │   └─ Create Recommendation object
    │
    ├─ Sort by relevance_score
    ├─ Return top-k recommendations
    │
    ▼
Recommendation[]
    {
        reference_document: Document,
        reasoning: "Same industry, similar challenges",
        relevance_score: 0.87,
        suggested_approach: "..."
        estimated_effort: "High (8 months, $2.5M)"
    }
```

### Sequence 4: Knowledge Synthesis

```
User Engagement Details + Context
    │
    │ KnowledgeSynthesizer.synthesize_recommendations()
    │
    ▼
Get Recommendations
    │
    ├─ Call RecommendationEngine
    ├─ Get top-k similar engagements
    │
    ▼
Format Context
    │
    ├─ Title, industry, transaction type
    ├─ Engagement details from similar cases
    ├─ Historical outcomes and metrics
    │
    ▼
Prompt LLM
    │
    ├─ Send to Claude/GPT-4 with:
    │   ├─ Current engagement description
    │   ├─ Similar past engagements
    │   └─ Structured prompt template
    │
    ▼
LLM Generates Response
    │
    ├─ Key insights from patterns
    ├─ Recommended approach
    ├─ Risk mitigation strategies
    ├─ Resource allocation guidance
    ├─ Timeline estimates
    │
    ▼
Return Structured Insights
    │
    └─ String (formatted markdown)
```

---

## Technology Stack

### Core Dependencies

```
liqueo/
├── Core Data Structures
│   └── No external dependencies (pure Python)
│
├── EmbeddingsManager
│   ├── numpy (vector operations)
│   ├── OpenAI SDK (embedding provider)
│   └── Anthropic SDK (embedding provider)
│
├── Recommender & Synthesizer
│   ├── Anthropic SDK (Claude API)
│   ├── OpenAI SDK (GPT-4 API)
│   └── No external DB (optional)
│
├── CLI Interface
│   ├── Click (CLI framework)
│   ├── Rich (terminal formatting)
│   └── Python standard library
│
└── Storage
    └── Filesystem (JSON files)
        No database required
```

### Optional Extensions

```
Vector Databases (for scale)
├── FAISS (local, CPU)
├── Pinecone (cloud)
├── Weaviate (open-source)
└── Milvus (cloud-native)

Document Parsers (for ingestion)
├── pdf2image + OCR
├── python-docx
└── python-pptx

Frameworks (for apps)
├── FastAPI (REST API)
├── Streamlit (web UI)
├── Django (full app)
└── Flask (lightweight server)
```

---

## Scalability Architecture

### Current Design (Development/Small Scale)

```
Single Machine
├── All documents in memory
├── Embeddings cached locally
├── Filesystem-based persistence
└── Suitable for: 100-10,000 documents
```

### Scaling to Production

```
Production Scale (10,000 - 1M documents)

┌─────────────────────────────────────────┐
│         Web API Layer                   │
│ (FastAPI/Flask servers, load balanced)  │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────┐
        │   Cache     │
        │  (Redis)    │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │                     │
    ▼                     ▼
┌─────────────┐    ┌──────────────────┐
│ Vector DB   │    │ Document Store   │
│ (Pinecone/  │    │ (PostgreSQL/     │
│  FAISS)     │    │  MongoDB)        │
└─────────────┘    └──────────────────┘
    │                     │
    └──────────────┬──────┘
                   │
          ┌────────▼────────┐
          │  External APIs  │
          │ (OpenAI, Claude)│
          └─────────────────┘
```

### Bottlenecks & Solutions

| Bottleneck | Current Impact | Solution |
|-----------|----------------|----------|
| Embedding generation | ~$0.02 per doc | Cache aggressively, batch requests |
| LLM synthesis | 2-5s latency | Queue + async processing, caching |
| Document storage | ~100KB per doc | S3/cloud storage, compression |
| Search speed | O(n) similarity | Vector DB indexing, FAISS |
| Memory usage | 768 floats/doc | Quantization, incremental loading |

---

## Security & Privacy Considerations

### Current Implementation

```
Local Storage (`.liqueo/`)
├── No encryption by default
├── Full access to filesystem
├── User responsible for access control
└── Risk: Sensitive client data exposure
```

### Production Hardening

```
Recommended Additions
├── Encryption at rest (AES-256)
├── API authentication (OAuth/JWT)
├── Access control (RBAC)
├── Audit logging (who did what)
├── Data retention policies
└── GDPR/compliance features
```

---

## Extension Patterns

### Pattern 1: Custom Recommendation Strategy

```python
class CustomRecommendationEngine(RecommendationEngine):
    def recommend_for_new_market_entry(self, target_industry: str):
        """Custom logic for market entry consulting"""
        similar_docs = self.embeddings_manager.semantic_search(
            f"market entry strategy {target_industry}",
            filters={"doc_type": "engagement"}
        )
        return [self._enrich_recommendation(r) for r in similar_docs]
```

### Pattern 2: Custom Storage Backend

```python
class DatabaseKnowledgeBase(KnowledgeBase):
    """Persist to PostgreSQL instead of filesystem"""
    
    def __init__(self, connection_string: str):
        self.db = Database(connection_string)
    
    def add_document(self, doc: Document):
        self.db.execute(
            "INSERT INTO documents (id, data) VALUES (?, ?)",
            doc.id, doc.to_json()
        )
```

### Pattern 3: Custom Embedding Provider

```python
class HuggingFaceEmbeddings(EmbeddingsManager):
    """Use local sentence-transformers instead of APIs"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def embed_document(self, doc: Document):
        # Local inference, no API cost
        embedding = self.model.encode(doc.content)
        # ... rest of logic
```

---

## Summary: Architecture Type

| Category | Classification |
|----------|-----------------|
| **Software Type** | **Toolkit** (reusable, modular, pluggable) |
| **Architecture Style** | Layered + Microservices-ready |
| **Design Patterns** | Repository, Strategy, Adapter, Facade, Factory |
| **Coupling** | Low (components can be used independently) |
| **Cohesion** | High (clear domain focus) |
| **Extensibility** | High (pluggable providers, clear interfaces) |
| **Testability** | High (separated concerns, no tight coupling) |
| **Scalability** | Medium (ready for horizontal scaling with extensions) |

**Best Described As**: A **modular, domain-driven consulting knowledge toolkit** with pluggable LLM and embedding providers, designed for semantic search and recommendation generation.
