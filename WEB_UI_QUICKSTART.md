# Liqueo Web UI - Quick Start Guide

## Run Locally (2 minutes)

### 1. Install Dependencies
```bash
pip install streamlit streamlit-option-menu
```

### 2. Navigate to Project
```bash
cd path/to/Liqueo
```

### 3. Start Web Server
```bash
streamlit run app.py
```

### 4. Open Browser
- Automatically opens at `http://localhost:8501`
- Or manually navigate to that URL

### 5. Start Using
- Add documents from "Add Engagement" tab
- Search knowledge base
- Get recommendations
- Generate insights

---

## Run on Google Colab (3 minutes)

### Method 1: Using ngrok (Recommended)

```python
# Install dependencies
!pip install streamlit streamlit-option-menu pyngrok -q

# Clone repository
!git clone https://github.com/hemalp143/Liqueo.git -q
```

```python
# Setup ngrok tunnel
from pyngrok import ngrok
import threading
import subprocess
import time

# Create tunnel
public_url = ngrok.connect(8501)
print(f"🌐 Web UI available at: {public_url}")

# Run Streamlit
subprocess.Popen(["streamlit", "run", "/content/Liqueo/app.py", "--server.port=8501"])
time.sleep(3)

# Keep tunnel open
try:
    input("Press Ctrl+C to stop...")
except KeyboardInterrupt:
    print("Stopping...")
```

### Method 2: Direct Port Access

If ngrok doesn't work, use Colab's built-in port forwarding:

```python
# Install and run Streamlit
!pip install streamlit streamlit-option-menu -q
!git clone https://github.com/hemalp143/Liqueo.git -q

# Run app
!streamlit run /content/Liqueo/app.py --server.port 8501
```

Then use Colab's port forwarding tools to access it.

---

## Web UI Layout

### Sidebar Navigation
- **Home**: Dashboard with statistics
- **Search**: Find similar engagements
- **Recommendations**: Get suggestions for new cases
- **Synthesize**: Generate strategic insights
- **Analysis**: Industry trend analysis
- **Documents**: View and export knowledge base
- **Add Engagement**: Add new consulting cases

### Key Features

#### 🏠 Home Dashboard
- **Metrics**: Total documents, industries, types, total value
- **Features**: Overview of capabilities
- **Recent**: List of latest engagements

#### 🔍 Search
- Free-text semantic search
- Filter by industry
- Adjustable result count
- Shows relevance scores

#### 💡 Recommendations
- Describe current engagement
- Get similar case recommendations
- View approaches and challenges
- See effort estimates

#### ✨ Synthesize
- Generate strategic insights
- AI-powered analysis
- Consider multiple cases
- Professional synthesis reports

#### 📊 Analysis
- Select industry
- View trend analysis
- Identify challenges
- See success factors

#### 📁 Documents
- View complete inventory
- Filter and sort
- Export to JSON
- Download capability

#### ➕ Add Engagement
- Simple form interface
- Fields: title, industry, type, value, duration, client
- Description and outcomes
- Consulting approach

---

## Screen-by-Screen Guide

### 1. First Run
When you first open the Web UI:
1. You'll see the Home dashboard
2. Zero documents initially
3. Click "Add Engagement" to add documents

### 2. Adding Documents
```
Step 1: Fill in the form
  - Title: "SaaS Acquisition - Tech Stack"
  - Industry: "Technology"
  - Type: "M&A"
  - Value: 2.5 (millions)
  - Duration: 8 (months)
  - Client: "Growth Equity Firm"

Step 2: Add details
  - Engagement Details: Describe what happened
  - Key Outcomes: What was achieved
  - Consulting Approach: How did you approach it

Step 3: Click "Add Engagement"
  - Confirms document was saved
  - Shows "Embeddings generated" or warning about API keys
```

### 3. Searching
```
Step 1: Go to Search tab
Step 2: Enter query: "technology infrastructure optimization"
Step 3: Set top results: 5
Step 4: Optional: filter by "Technology" industry
Step 5: Click Search
Step 6: View results with relevance scores
```

### 4. Getting Recommendations
```
Step 1: Go to Recommendations tab
Step 2: Describe your engagement: "We need to reduce IT costs..."
Step 3: Set number of recommendations: 3
Step 4: Click "Get Recommendations"
Step 5: Review similar cases and suggestions
```

### 5. Synthesizing Insights
```
Step 1: Go to Synthesize tab
Step 2: Describe the engagement
Step 3: Set top similar cases: 3
Step 4: Click "Generate Insights"
Step 5: Read professional synthesis report
```

### 6. Analyzing Industry
```
Step 1: Go to Analysis tab
Step 2: Select industry from dropdown
Step 3: Click "Analyze Trends"
Step 4: View industry-specific analysis
```

### 7. Exporting Data
```
Step 1: Go to Documents tab
Step 2: View all documents in table
Step 3: Click "Export Knowledge Base (JSON)"
Step 4: Click "Download JSON" button
Step 5: JSON file downloads to your computer
```

---

## Customization

### Change Port
```bash
streamlit run app.py --server.port 8502
```

### Hide Menu
```bash
streamlit run app.py --logger.level=error
```

### Full-Screen Mode
```bash
streamlit run app.py --client.toolbarPosition=bottom
```

### Disable Sidebar
Add to `app.py`:
```python
st.set_page_config(initial_sidebar_state="collapsed")
```

---

## Tips & Tricks

### 🚀 Performance
- Clear cache occasionally: Menu → Clear Cache
- Delete old embeddings if low on space
- Use filters to narrow search scope

### 📈 Best Results
- Add 10+ documents for better recommendations
- Use descriptive engagement details
- Include realistic outcomes and approaches
- Set consistent industry names

### 🎨 Customization
- Modify colors in CSS section of `app.py`
- Add company logo to header
- Change sidebar icon colors
- Adjust metric card styling

### 🔑 API Keys
To enable enhanced features:
1. Get Anthropic API key from https://console.anthropic.com
2. Get OpenAI API key from https://platform.openai.com
3. Set environment variables:
   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   export OPENAI_API_KEY="your_key_here"
   streamlit run app.py
   ```

---

## Troubleshooting

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill process using port 8501
lsof -ti :8501 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Data Not Showing
```bash
# Ensure .liqueo directory exists
mkdir -p .liqueo/knowledge

# Check permissions
chmod 755 .liqueo
```

### Slow Performance
```bash
# Clear cache
# Menu → Clear Cache

# Restart app
# Press Ctrl+C and run again
```

### Documents Lost
- Data is saved in `.liqueo/knowledge/` directory
- Make sure directory is writable
- Check file permissions

---

## Deployment to Production

### Heroku
```bash
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t liqueo .
docker run -p 8501:8501 liqueo
```

### Cloud Run
```bash
gcloud run deploy liqueo --source . --allow-unauthenticated
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop Streamlit server |
| `Ctrl+R` | Rerun page |
| `R` | Rerun page (when focused) |
| `C` | Clear cache |
| `I` | Open settings |
| `Ctrl+Shift+D` | Toggle developer mode |

---

## File Structure

```
Liqueo/
├── app.py                 # Web UI (Streamlit)
├── requirements.txt       # Dependencies
├── liqueo/
│   ├── core.py           # Data models
│   ├── embeddings.py     # Semantic search
│   ├── recommender.py    # Recommendations
│   ├── synthesizer.py    # Synthesis
│   └── cli.py            # CLI interface
├── .liqueo/
│   └── knowledge/        # Document storage
└── notebooks/
    └── liqueo_colab_demo.ipynb  # Colab notebook
```

---

## Next Steps

1. ✅ Run Web UI locally
2. Add your consulting engagements
3. Configure API keys for enhanced features
4. Share with team on cloud deployment
5. Integrate with CRM/project tools

---

## Support

- **Issues**: https://github.com/hemalp143/Liqueo/issues
- **Email**: hemalp1434@gmail.com
- **Docs**: See README.md and DEPLOYMENT_GUIDE.md

---

**Ready to go!** 🚀

Run `streamlit run app.py` and start exploring your consulting knowledge base.
