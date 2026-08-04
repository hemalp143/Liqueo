# Liqueo

**Knowledge Discovery & Reuse Component for Financial and Business Consultants**

Liqueo is a Python library that helps financial and business consultants discover, organize, and reuse knowledge from past engagements. It enables semantic search across engagement archives, recommends similar solutions, and synthesizes insights using LLMs.

## Features

- **Document Ingestion & Storage**: Import and organize financial documents, case studies, engagement records, and templates
- **Semantic Search**: Find relevant past engagements using intelligent, meaning-based search
- **Reuse Recommendations**: Automatically suggest similar solutions and approaches from historical data
- **Knowledge Synthesis**: Generate strategic insights and recommendations using AI
- **Industry & Transaction Analysis**: Analyze trends within specific industries or deal types
- **Flexible Filtering**: Search by industry, transaction type, engagement value, duration, and more

## Quick Start

### Installation

```bash
pip install -e .
```

### Usage via CLI

```bash
# Add a new engagement to the knowledge base
liqueo add --title "SaaS Acquisition Analysis" --industry "Technology" --type engagement

# Search for similar engagements
liqueo search --query "technology valuation m&a" --industry "Technology"

# Get recommendations for a new engagement
liqueo recommend --query "fintech back-office optimization"

# Analyze industry trends
liqueo analyze --industry "Technology"

# List all documents
liqueo list

# View a specific document
liqueo view doc-001
```

### Usage via Python

```python
from liqueo.core import Document, KnowledgeBase
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer

# Initialize knowledge base
kb = KnowledgeBase()

# Add a document
doc = Document(
    id="engagement-001",
    title="SaaS Company Valuation",
    content="Engagement details...",
    doc_type="engagement",
    industry="Technology",
    transaction_type="M&A",
    engagement_value=5.0,
    duration_months=8
)
kb.add_document(doc)

# Search for similar engagements
embeddings = EmbeddingsManager(kb, model="anthropic")
results = embeddings.semantic_search("technology acquisition valuation", top_k=5)

# Get recommendations
recommender = RecommendationEngine(embeddings)
recommendations = recommender.recommend_similar_engagements(
    "New SaaS due diligence engagement",
    top_k=3
)

# Synthesize insights
synthesizer = KnowledgeSynthesizer(kb, recommender)
insights = synthesizer.synthesize_recommendations(
    "Fintech platform optimization engagement"
)
```

## Architecture

### Core Components

1. **KnowledgeBase** (`liqueo.core`)
   - Document storage and retrieval
   - Filtering and indexing
   - Persistent storage with JSON

2. **EmbeddingsManager** (`liqueo.embeddings`)
   - Generate embeddings for documents
   - Semantic search using cosine similarity
   - Support for OpenAI and Anthropic APIs

3. **RecommendationEngine** (`liqueo.recommender`)
   - Find similar past engagements
   - Suggest consulting approaches
   - Identify industry patterns and trends

4. **KnowledgeSynthesizer** (`liqueo.synthesizer`)
   - Generate strategic insights from engagement data
   - Summarize learnings and best practices
   - Analyze industry trends using LLMs

### Data Model

```python
Document:
  - id: unique identifier
  - title: engagement name
  - content: detailed description
  - doc_type: "engagement", "case_study", "template", etc.
  - industry: e.g., "Technology", "Finance", "Retail"
  - transaction_type: e.g., "M&A", "Restructuring", "Valuation"
  - engagement_value: in millions
  - duration_months: project duration
  - client_name: anonymized or actual client name
  - consulting_approach: methodology used
  - key_outcomes: results and impact
  - tags: searchable tags
  - metadata: custom fields
```

## Configuration

### Environment Variables

```bash
# For OpenAI embeddings
export OPENAI_API_KEY="your-key-here"

# For Anthropic API (synthesis and embeddings)
export ANTHROPIC_API_KEY="your-key-here"
```

### Storage

Knowledge base data is stored in `.liqueo/` directory by default:
```
.liqueo/
  ├── documents/       # Document JSON files
  ├── embeddings/      # Vector embeddings
  ├── index.json       # Document index
  └── embedding_index.json  # Embedding metadata
```

## Examples

See `examples/basic_usage.py` for a complete working example demonstrating:
- Creating and storing documents
- Semantic search
- Generating recommendations
- Synthesizing insights
- Analyzing industry trends

## Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=liqueo
```

## API Reference

### KnowledgeBase

```python
kb = KnowledgeBase(storage_dir=".liqueo")

# Add/retrieve documents
kb.add_document(document)
doc = kb.get_document(doc_id)
docs = kb.list_documents()

# Filtering
kb.filter_by_industry("Technology")
kb.filter_by_transaction_type("M&A")
kb.filter_by_tags(["cloud", "architecture"])
```

### EmbeddingsManager

```python
embeddings = EmbeddingsManager(kb, model="anthropic")

# Generate embeddings
embeddings.embed_document(doc)

# Search
results = embeddings.semantic_search(
    query="technology valuation",
    top_k=5,
    filters={"industry": "Technology"}
)
```

### RecommendationEngine

```python
recommender = RecommendationEngine(embeddings)

# Get recommendations
recs = recommender.recommend_similar_engagements(query, top_k=5)
recs = recommender.recommend_by_industry("Technology", top_k=5)
recs = recommender.recommend_by_transaction_type("M&A", top_k=5)

# Find patterns
patterns = recommender.find_patterns(industry="Finance")
```

### KnowledgeSynthesizer

```python
synthesizer = KnowledgeSynthesizer(kb, recommender)

# Generate insights
insights = synthesizer.synthesize_recommendations(engagement_desc)

# Extract learnings
learnings = synthesizer.extract_learnings(document)

# Analyze industry
analysis = synthesizer.analyze_industry_trends("Technology")
```

## Supported Embedding Models

- **OpenAI** (`text-embedding-3-small`): High accuracy, API-based
- **Anthropic**: Uses Claude API for flexible embedding generation

## Performance Considerations

- Embeddings are cached locally for faster searches
- Documents are indexed in memory for quick filtering
- Semantic search is O(n) where n is number of documents
- Use filters to reduce search scope for large knowledge bases

## Limitations & Future Work

- Current implementation uses in-memory index (scalable to ~100k documents)
- Supports single-machine deployment only
- Would benefit from vector database integration (FAISS, Pinecone)
- Could add multi-language support
- Possible integration with document parsing (PDF, Word, etc.)

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run linting
ruff check .
black .

# Type checking
mypy liqueo/

# Build documentation
sphinx-build -b html docs/ docs/_build/
```

## License

MIT

## Contact

For questions or feedback: hemalp1434@gmail.com
