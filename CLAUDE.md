# Liqueo Development Guide

## Project Overview

Liqueo is a knowledge discovery and reuse component for financial and business consultants. It enables:
- Storing consulting engagements and case studies
- Semantic search using embeddings
- Recommendations for similar past engagements
- AI-powered synthesis of insights and strategies

## Project Structure

```
liqueo/
├── core.py           # Core data structures (Document, KnowledgeBase)
├── embeddings.py     # Semantic search with embeddings
├── recommender.py    # Recommendation engine
├── synthesizer.py    # LLM-powered insight generation
├── cli.py            # Command-line interface
└── __init__.py       # Package initialization

tests/
├── test_core.py      # Core functionality tests
└── __init__.py

examples/
└── basic_usage.py    # Usage examples
```

## Key Components

### Document Model
- Structured data for consulting engagements
- Fields: title, content, industry, transaction_type, value, duration, etc.
- JSON serialization for persistence

### KnowledgeBase
- Persistent storage of documents
- Supports filtering by industry, transaction type, tags
- JSON-based indexing

### EmbeddingsManager
- Generates vector embeddings for semantic search
- Supports OpenAI and Anthropic APIs
- Caches embeddings locally

### RecommendationEngine
- Finds similar past engagements
- Suggests consulting approaches
- Identifies industry patterns

### KnowledgeSynthesizer
- Uses LLMs to generate insights
- Extracts learnings from engagements
- Analyzes industry trends

## Development Guidelines

### Adding New Features

1. **New field to Document**: Update `core.py` Document class
2. **New search capability**: Add to `embeddings.py` or `recommender.py`
3. **New analysis**: Add method to `synthesizer.py`
4. **CLI command**: Add command to `cli.py` using Click

### API Key Management

- Uses `.env` file (copy from `.env.example`)
- Supports OPENAI_API_KEY and ANTHROPIC_API_KEY
- Falls back gracefully when keys not available

### Testing

Run tests with: `pytest tests/ -v`

Key test scenarios:
- Document CRUD operations
- Knowledge base persistence
- Filtering functionality
- Serialization/deserialization

### Performance Considerations

- Embeddings cached locally (~100 KB per document)
- Semantic search is O(n) where n = document count
- Suitable for up to 10,000 documents on single machine
- Consider vector DB (Pinecone, Weaviate) for scale

## Common Tasks

### Adding a New Document Type

```python
# In core.py, Document class already supports flexible doc_type
doc = Document(
    ...,
    doc_type="template",  # or "proposal", "template", etc.
    ...
)
```

### Customizing Search Filters

```python
# In embeddings.py, semantic_search method
filters = {
    "industry": "Technology",
    "transaction_type": "M&A",
    "min_similarity": 0.7
}
results = embeddings.semantic_search(query, filters=filters)
```

### Adding New Synthesis Capabilities

```python
# In synthesizer.py, add method:
def new_analysis_method(self, param: str) -> str:
    prompt = f"""..."""
    response = self.client.messages.create(...)
    return response.content[0].text
```

## Dependencies

- **LangChain**: Potential for future integration
- **OpenAI**: For embeddings and synthesis
- **Anthropic**: For synthesis and embeddings
- **Click**: CLI framework
- **Rich**: Terminal formatting
- **Pydantic**: Data validation (optional)
- **Pytest**: Testing

## Known Limitations

1. In-memory indexing (not scalable past ~100k documents)
2. No built-in document parsing (upload JSON only)
3. No multi-user/collaboration features
4. Single-machine deployment only
5. Embeddings API costs for large knowledge bases

## Future Enhancements

- [ ] Vector database integration (FAISS, Pinecone)
- [ ] PDF/Word document parsing
- [ ] Web UI dashboard
- [ ] Multi-user collaboration with permissions
- [ ] Continuous learning from new engagements
- [ ] Integration with CRM/project management tools
- [ ] Custom embedding models
- [ ] Industry-specific templates
- [ ] Benchmark comparisons
- [ ] Export to various formats (PDF, PPT)

## API Conventions

- Use Anthropic API by default (available to users)
- Graceful degradation when API keys missing
- Return empty lists/None instead of raising for missing data
- Use type hints throughout

## Contact & Support

- Questions: hemalp1434@gmail.com
- Issue tracker: GitHub Issues
