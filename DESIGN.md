# Liqueo Design Architecture

## Component Classification

**Liqueo is a TOOLKIT** with elements of an **ARCHITECTURAL PATTERN LIBRARY**

### Precise Definition

Liqueo is a **reusable, composable toolkit** that provides:
- Modular building blocks for knowledge management in consulting
- Pluggable interfaces for different embedding and LLM providers
- Extensible architecture for custom use cases
- Pre-built patterns for common consulting workflows

**NOT a framework** because it doesn't enforce project structure or invert control
**NOT a prototype** because it's production-ready with proper error handling
**NOT pure architecture pattern** because it includes concrete implementations

---

## Overall Design Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  (User applications using Liqueo toolkit)                    │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ (imports)
┌─────────────────────────────────────────────────────────────┐
│                    PUBLIC API LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ KnowledgeBase│  │ Recommender  │  │ Synthesizer  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│                  SERVICE LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         EmbeddingsManager (Semantic Search)          │   │
│  │  - Embedding generation                              │   │
│  │  - Similarity computation                            │   │
│  │  - Cache management                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Document    │  │  Embeddings  │  │    Index     │       │
│  │  (Core)      │  │  (NumPy)     │  │  (JSON)      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│                STORAGE LAYER                                 │
│  └──────────────────────────────────────────────────────────┘
│  Filesystem (.liqueo/)                                      │
│  └──────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

---

## Architectural Layers & Components

### 1. **DATA MODEL LAYER** (`liqueo/core.py`)

**Purpose**: Define domain concepts and data structures

**Components**:
- `Document`: Core data class representing consulting engagements
- `SearchResult`: Search response with relevance scoring
- `KnowledgeBase`: Repository pattern for document management

**Design Patterns Used**:
- **Data Class Pattern**: Immutable-ish document objects
- **Repository Pattern**: Abstraction over storage
- **Domain-Driven Design**: Document reflects consulting domain

**Characteristics**:
```python
Document
├── Identity: id (unique, content-addressed)
├── Content: title, content, doc_type
├── Domain Fields: industry, transaction_type
├── Metrics: engagement_value, duration_months
├── Metadata: tags, custom fields
└── Lifecycle: created_at, updated_at
```

**Extensibility**: Easy to add new fields without breaking existing code

---

### 2. **SERVICE LAYER** (`liqueo/embeddings.py`)

**Purpose**: Provide semantic understanding and similarity matching

**Components**:
- `EmbeddingsManager`: Vector space operations

**Design Patterns Used**:
- **Strategy Pattern**: Pluggable embedding providers (OpenAI, Anthropic)
- **Adapter Pattern**: Normalizes different API responses
- **Caching Pattern**: Local embedding storage

**Key Responsibilities**:
```
Input (text) → Embedding Model → Vector (768D)
                                 ↓
                            Cache (disk)
                                 ↓
Query Vector → Cosine Similarity → Results
```

**Pluggable Interfaces**:
```python
if model == "openai":
    # Use OpenAI API
elif model == "anthropic":
    # Use Anthropic API
```

---

### 3. **BUSINESS LOGIC LAYER** (`liqueo/recommender.py`, `liqueo/synthesizer.py`)

**Purpose**: Generate actionable insights from knowledge base

**Components**:

#### A. RecommendationEngine
- `recommend_similar_engagements()`: Semantic matching
- `recommend_by_industry()`: Categorical matching
- `recommend_by_transaction_type()`: Pattern matching
- `find_patterns()`: Aggregate pattern discovery

**Design Patterns Used**:
- **Strategy Pattern**: Different recommendation algorithms
- **Facade Pattern**: Unified interface for complex operations
- **Template Method**: Common structure for recommendations

#### B. KnowledgeSynthesizer
- `synthesize_recommendations()`: LLM-based synthesis
- `generate_engagement_summary()`: Content generation
- `extract_learnings()`: Pattern extraction
- `analyze_industry_trends()`: Aggregate analysis

**Design Patterns Used**:
- **Adapter Pattern**: Normalizes different LLM APIs
- **Decorator Pattern**: Enhances search results with LLM insights
- **Chain of Responsibility**: Multi-step synthesis pipeline

---

### 4. **INTERFACE LAYER** (`liqueo/cli.py`)

**Purpose**: Provide user-friendly access to toolkit

**Components**:
- Click-based CLI commands
- Rich terminal formatting
- Interactive prompts

**Design Patterns Used**:
- **Command Pattern**: CLI commands as first-class objects
- **Facade Pattern**: Simplifies toolkit complexity
- **Factory Pattern**: Creates proper objects from CLI args

**Commands**:
```
add         → Create documents
search      → Query knowledge base
recommend   → Get recommendations
synthesize  → Generate insights
analyze     → Industry analysis
list        → Browse documents
view        → Inspect details
export      → Export data
```

---

## Data Flow Architecture

### Workflow 1: Adding Knowledge

```
User Input
   ↓
Document Creation (core.py)
   ↓
KnowledgeBase.add_document()
   ↓
Filesystem Storage (.liqueo/documents/)
   ↓
Index Update (.liqueo/index.json)
   ↓
Optional: EmbeddingsManager.embed_document()
   ↓
Embedding Storage (.liqueo/embeddings/)
   ↓
✓ Document Persisted
```

### Workflow 2: Semantic Search

```
User Query
   ↓
EmbeddingsManager.semantic_search()
   ↓
Query Embedding (API or cache)
   ↓
For each document in KB:
  ├─ Load embedding (cache or generate)
  ├─ Compute cosine similarity
  └─ Score & filter
   ↓
Sort by relevance
   ↓
Return top-k SearchResults
```

### Workflow 3: Generating Recommendations

```
User Request (query text or document)
   ↓
RecommendationEngine.recommend_similar_engagements()
   ↓
Semantic Search (via EmbeddingsManager)
   ↓
Filter by industry/type (optional)
   ↓
For each result:
  ├─ Extract consulting approach
  ├─ Extract challenges
  ├─ Estimate effort
  └─ Generate reasoning
   ↓
Return Recommendations with context
```

### Workflow 4: Synthesizing Insights

```
User Engagement Description
   ↓
KnowledgeSynthesizer.synthesize_recommendations()
   ↓
Get recommendations (via RecommendationEngine)
   ↓
Format recommendation context
   ↓
Prompt LLM with:
  ├─ Current engagement details
  ├─ Similar past engagements
  └─ Template questions
   ↓
LLM generates insights:
  ├─ Key patterns
  ├─ Recommended approach
  ├─ Risk mitigation
  ├─ Resource allocation
  └─ Timeline
   ↓
Return structured insights
```

---

## Design Principles

### 1. **Separation of Concerns**
- Core data model isolated from services
- Services independent of UI/CLI
- Embeddings decoupled from recommendations

**Benefit**: Each layer can be tested and modified independently

### 2. **Pluggable Dependencies**
- Embedding models (OpenAI, Anthropic)
- Storage backends (filesystem, could extend to DB)
- LLM providers (OpenAI, Anthropic)

**Benefit**: Easy to swap implementations without API changes

### 3. **Progressive Enhancement**
- Works without embeddings (keyword search possible)
- Works without LLM (recommendations from metadata)
- Works without API keys (uses cached embeddings)

**Benefit**: Graceful degradation

### 4. **Domain-Driven Design**
- Entities reflect consulting domain (Document, Engagement, Transaction)
- Business logic organized around use cases
- Ubiquitous language: engagement, industry, transaction type

**Benefit**: Code reflects domain knowledge

### 5. **SOLID Principles**

| Principle | Implementation |
|-----------|-----------------|
| **S**ingle Responsibility | Each class has one reason to change |
| **O**pen/Closed | Pluggable embedding/LLM providers |
| **L**iskov Substitution | Different embedding models interchangeable |
| **I**nterface Segregation | Minimal required interfaces |
| **D**ependency Inversion | Depends on abstractions (models) not implementations |

---

## Toolkit vs Framework Comparison

| Aspect | Liqueo (Toolkit) | Would Be Framework |
|--------|-----------------|-------------------|
| **Structure** | Modular components | Prescriptive structure |
| **Control** | Your code calls Liqueo | Framework calls your code |
| **Flexibility** | Mix/match components | Follow framework patterns |
| **Learning Curve** | Component-by-component | Whole framework upfront |
| **Use Cases** | Multiple specialized | Specific domain |
| **Integration** | Drop into existing projects | Project built on framework |

**Liqueo Example**:
```python
# You control the flow
kb = KnowledgeBase()
kb.add_document(doc)
results = embeddings.semantic_search(query)
recommendations = recommender.recommend_similar_engagements(query)
```

**Framework Example** (if it were one):
```python
# Framework controls the flow
engine = ConsultingEngine(config)
# Engine calls your callbacks, plugins, handlers
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER CODE                                    │
│                   (Your application)                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
   │ KnowledgeBase│    │  Embeddings  │     │Recommender   │
   │              │    │   Manager    │     │              │
   └─────────────┘    └──────────────┘     └──────────────┘
        │                     │                     │
        │    ┌────────────────┼────────────────┐   │
        │    │                │                │   │
        │    ▼                ▼                ▼   │
        │  ┌─────────────────────────────────────┐ │
        │  │     KnowledgeSynthesizer            │ │
        │  │  (Orchestrates other components)    │ │
        │  └─────────────────────────────────────┘ │
        │                  │                       │
        └──────────────────┼───────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐       ┌──────────┐       ┌──────────┐
   │Document │       │Embedding │       │LLM APIs  │
   │Store    │       │Cache     │       │(OpenAI, │
   │(JSON)   │       │(NumPy)   │       │Anthropic)│
   └─────────┘       └──────────┘       └──────────┘
```

---

## Extension Points

### 1. Adding New Recommendation Strategy

```python
class RecommendationEngine:
    def recommend_by_custom_metric(self, metric: str) -> list[Recommendation]:
        # New method using existing components
        documents = self.kb.list_documents()
        # Custom logic
        return recommendations
```

### 2. Adding New Data Fields to Document

```python
@dataclass
class Document:
    # Existing fields...
    custom_field: Optional[str] = None  # Add easily
```

### 3. Implementing Custom Storage Backend

```python
class DatabaseKnowledgeBase(KnowledgeBase):
    def __init__(self, db_url: str):
        self.db = Database(db_url)
    
    def add_document(self, document: Document):
        self.db.insert(document.to_dict())
    
    def get_document(self, doc_id: str):
        return Document.from_dict(self.db.query_one(doc_id))
```

### 4. Adding New Embedding Provider

```python
class EmbeddingsManager:
    def __init__(self, model: str = "anthropic"):
        if model == "huggingface":
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("model-name")
        # ... rest of logic
```

---

## Architectural Trade-offs

### Chosen Design Decisions

| Trade-off | Choice | Reasoning |
|-----------|--------|-----------|
| **Storage** | Filesystem JSON | Simplicity, portability, no DB dependency |
| **Search** | In-memory similarity | Fast for <100k docs, no external service |
| **Embeddings** | External APIs | Better quality, user controls costs |
| **Synthesis** | LLM APIs | Latest models, no local compute needed |
| **Caching** | Local disk | Persistence, cost savings on repeated queries |

### Scalability Implications

| Component | Current Limit | Scaling Solution |
|-----------|---------------|------------------|
| Documents | ~100k (memory) | Switch to FAISS/Pinecone vector DB |
| Embeddings | ~50GB disk | Vector DB with compression |
| Concurrent users | Single machine | Add API server layer |
| Real-time synthesis | API latency | Queue-based processing |

---

## Quality Attributes

### Maintainability ⭐⭐⭐⭐⭐
- Clear separation of concerns
- Domain language in code
- Comprehensive type hints
- Modular structure

### Extensibility ⭐⭐⭐⭐⭐
- Pluggable providers
- Open architecture
- Well-documented extension points
- Minimal dependencies on internals

### Performance ⭐⭐⭐⭐
- Local caching of embeddings
- Efficient similarity computation
- Lazy loading of documents
- Could optimize with indexing

### Usability ⭐⭐⭐⭐⭐
- Simple Python API
- Rich CLI interface
- Sensible defaults
- Clear error messages

### Testability ⭐⭐⭐⭐⭐
- Pure functions where possible
- Dependency injection patterns
- Mockable external services
- Comprehensive test structure

---

## Summary: What is Liqueo?

**Liqueo is a Consulting Knowledge Toolkit** that provides:

1. **Modular Components** you use together or independently
2. **Semantic Intelligence** through pluggable embedding providers
3. **Domain-Specific Patterns** for consulting workflows
4. **Production-Ready Code** with proper error handling and testing
5. **Extensible Architecture** for customization and integration

**Key Characteristics**:
- ✅ Not prescriptive (you control architecture)
- ✅ Not heavyweight (minimal dependencies)
- ✅ Not locked-in (pluggable providers)
- ✅ Not experimental (production patterns)
- ✅ Not monolithic (composable pieces)

**Ideal for**:
- Consulting firms building knowledge platforms
- Teams needing semantic search + recommendations
- Organizations with rich historical engagement data
- Projects requiring flexible, extensible architecture

**Not ideal for**:
- Simple document storage (use cloud storage)
- Real-time systems (API latency)
- Large-scale deployments without DB (>100k docs)
- Applications needing strict data isolation
