# Liqueo Repository Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.8+
- Git
- pip or conda

### Step 1: Clone Repository

```bash
git clone https://github.com/hemalp143/liqueo.git
cd liqueo
```

### Step 2: Create Virtual Environment

**Using venv (macOS/Linux):**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Using venv (Windows):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n liqueo python=3.9
conda activate liqueo
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys (Optional)

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

**Note:** API keys are optional. System works with keyword search fallback if not provided.

### Step 5: Run Web UI

```bash
streamlit run app.py
```

Open browser: `http://localhost:8501`

---

## Detailed Setup by Environment

### Local Development (macOS/Linux)

```bash
# 1. Clone
git clone https://github.com/hemalp143/liqueo.git
cd liqueo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install with dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# 4. Verify installation
python -c "import liqueo; print(liqueo.__version__)"

# 5. Run tests
pytest tests/ -v

# 6. Start web UI
streamlit run app.py
```

### Local Development (Windows)

```bash
# 1. Clone
git clone https://github.com/hemalp143/liqueo.git
cd liqueo

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install with dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# 4. Verify installation
python -c "import liqueo; print(liqueo.__version__)"

# 5. Run tests
pytest tests/ -v

# 6. Start web UI
streamlit run app.py
```

### Google Colab

```python
# 1. Clone repository
!git clone https://github.com/hemalp143/liqueo.git
%cd liqueo

# 2. Install dependencies
!pip install -r requirements.txt

# 3. Set up API keys (optional)
import os
os.environ['ANTHROPIC_API_KEY'] = 'your_key_here'
os.environ['OPENAI_API_KEY'] = 'your_key_here'

# 4. Import and use
from liqueo import KnowledgeBase, EmbeddingsManager
kb = KnowledgeBase()

# 5. Alternative: Run demo script
!python colab_demo.py
```

**Note on Colab:** Streamlit web UI is not available in Colab. Use Python API directly or run `colab_demo.py` for interactive tutorial.

### Docker

```bash
# 1. Build image
docker build -t liqueo .

# 2. Run container
docker run -p 8501:8501 liqueo

# 3. Access
# Open browser: http://localhost:8501
```

### Production Server

```bash
# 1. Clone
git clone https://github.com/hemalp143/liqueo.git
cd liqueo

# 2. Create virtual environment
python3 -m venv /opt/liqueo/venv
source /opt/liqueo/venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install gunicorn

# 4. Configure secrets
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...

# 5. Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:st_app

# 6. Or run streamlit in production mode
streamlit run app.py --server.port 8080 --server.headless true
```

---

## Project Structure

```
liqueo/
├── liqueo/
│   ├── __init__.py           # Package initialization
│   ├── core.py               # Document & KnowledgeBase classes
│   ├── embeddings.py         # Semantic search with embeddings
│   ├── recommender.py        # Recommendation engine
│   ├── synthesizer.py        # LLM-powered synthesis
│   ├── workflow.py           # 9-step workflow engine
│   └── cli.py                # Command-line interface
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py          # Core functionality tests
│   ├── test_embeddings.py    # Embedding tests
│   ├── test_recommender.py   # Recommendation tests
│   └── test_workflow.py      # Workflow tests
│
├── examples/
│   └── basic_usage.py        # Usage examples
│
├── app.py                    # Streamlit web UI
├── colab_demo.py             # Google Colab demo
│
├── README.md                 # Project overview
├── TECHNICAL_FLOW.md         # Technical architecture
├── WORKFLOW_GUIDE.md         # User workflow guide
├── DEMO_SCENARIO.md          # Demo scenario & data
├── ARCHITECTURE.md           # System architecture
├── SETUP.md                  # This file
│
├── requirements.txt          # Python dependencies
├── .env.example              # API key template
└── .gitignore
```

---

## Dependency Installation Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'liqueo'`

**Solution:** Reinstall package in development mode:
```bash
pip install -e .
```

### Issue: OpenAI API import error

**Solution:** Reinstall OpenAI SDK:
```bash
pip install --upgrade openai
```

### Issue: Anthropic API import error

**Solution:** Install Anthropic SDK:
```bash
pip install anthropic
```

### Issue: Streamlit not found

**Solution:**
```bash
pip install streamlit
```

---

## API Key Configuration

### Getting Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up for account
3. Navigate to API Keys section
4. Create new API key
5. Copy to `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Getting OpenAI API Key

1. Go to https://platform.openai.com
2. Sign up for account
3. Navigate to API Keys section
4. Create new API key
5. Copy to `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   ```

### Using System Without API Keys

If you don't have API keys:
- Knowledge base still works
- Search uses keyword fallback (basic but functional)
- Recommendations available without embeddings
- Synthesis falls back to pattern extraction
- Full vertical slice works, just with reduced functionality

---

## Running the Demo

### Demo Scenario Overview

The demo shows the complete 9-step workflow using a fintech RFP scenario.

### To Run Demo:

1. **Start web UI:**
   ```bash
   streamlit run app.py
   ```

2. **Go to "Knowledge Workflow" tab**

3. **Follow the 30-minute demo:**
   - **Step 1:** Problem identification (2 min)
   - **Step 2:** Search knowledge base (3 min)
   - **Step 3:** Identify related documents (1 min)
   - **Step 4:** AI summarization (2 min)
   - **Step 5:** Review & evaluate (4 min)
   - **Step 6:** Select content to reuse (2 min)
   - **Step 7:** Create new engagement (6 min)
   - **Step 8:** Tag & classify (2 min)
   - **Step 9:** Store & celebrate (3 min)

**Total Time:** ~30 minutes for complete workflow

See `DEMO_SCENARIO.md` for full scenario script and expected outputs.

---

## Verification: First Run Checklist

After installation, verify system works:

```bash
# 1. Import core module
python -c "from liqueo import Document; print('✓ Core module loads')"

# 2. Create knowledge base
python -c "from liqueo import KnowledgeBase; kb = KnowledgeBase(); print('✓ KnowledgeBase initializes')"

# 3. Add document
python << 'EOF'
from liqueo import Document, KnowledgeBase
kb = KnowledgeBase()
doc = Document(
    title="Test Engagement",
    content="Test content",
    industry="Technology",
    transaction_type="M&A",
    doc_type="engagement"
)
kb.add_document(doc)
print("✓ Document added successfully")
EOF

# 4. List documents
python << 'EOF'
from liqueo import KnowledgeBase
kb = KnowledgeBase()
docs = kb.list_documents()
print(f"✓ Knowledge base contains {len(docs)} documents")
EOF

# 5. Run tests
pytest tests/ -v --tb=short

# 6. Start web UI
streamlit run app.py
```

---

## Git Workflow

### Cloning the Feature Branch

```bash
# Clone main repository
git clone https://github.com/hemalp143/liqueo.git
cd liqueo

# Checkout feature branch
git checkout claude/knowledge-discovery-reuse-e3nr1n
# or
git checkout -b claude/knowledge-discovery-reuse-e3nr1n origin/claude/knowledge-discovery-reuse-e3nr1n
```

### Pulling Latest Changes

```bash
# Fetch latest changes
git fetch origin

# Update current branch
git pull origin claude/knowledge-discovery-reuse-e3nr1n
```

### Pushing Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: description"

# Push to feature branch
git push -u origin claude/knowledge-discovery-reuse-e3nr1n
```

---

## Environment Variables Reference

Create `.env` file with these optional variables:

```
# LLM Provider APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional: Embedding settings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_PROVIDER=openai  # or 'anthropic'

# Optional: Storage settings
KNOWLEDGE_BASE_PATH=.liqueo/knowledge
EMBEDDINGS_CACHE_PATH=.liqueo/embeddings

# Optional: Web UI settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

---

## Troubleshooting Common Issues

### "No API key provided" Warning

**This is OK!** System will use keyword search instead. To use embeddings, add API key to `.env`.

### Port 8501 Already in Use

```bash
streamlit run app.py --server.port 8502
```

### Knowledge base file not found

```bash
# Create directory
mkdir -p .liqueo/knowledge
mkdir -p .liqueo/embeddings
```

### Import errors on Colab

Run this first:
```python
!pip install --upgrade google-colab
```

### Windows: "pip is not recognized"

Use full path:
```bash
C:\Python39\Scripts\pip install -r requirements.txt
```

---

## Performance Benchmarks

### Expected Performance on Typical Machine

| Operation | Time | Notes |
|-----------|------|-------|
| Add document (10KB) | 50-100ms | Without embeddings |
| Add with embedding | 1-2s | Depends on API |
| Search (100 docs) | 100-500ms | Semantic search |
| Keyword search (100 docs) | 10-50ms | Fast fallback |
| Generate recommendation | 2-5s | Includes LLM call |
| Synthesize insights | 5-10s | LLM generation |

---

## Next Steps After Installation

1. **Run demo scenario** (see DEMO_SCENARIO.md)
2. **Add your own documents** via web UI
3. **Try semantic search** with different queries
4. **Explore recommendations** for similar engagements
5. **Read WORKFLOW_GUIDE.md** for structured 9-step process
6. **Integrate with your tools** using Python API

---

## Support & Questions

- **Documentation:** See README.md and TECHNICAL_FLOW.md
- **Issues:** Report on GitHub Issues
- **Email:** hemalp1434@gmail.com
- **Demo Questions:** See DEMO_SCENARIO.md Q&A section

Happy discovering knowledge! 🧠
