#!/usr/bin/env python3
"""Generate comprehensive PDF from Liqueo demo materials."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, PageTemplate, Frame
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime

# Create PDF
pdf_path = "Liqueo_Demo_Package.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1a5490'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2d5aa6'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

# Title Page
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("LIQUEO", title_style))
story.append(Paragraph("Knowledge Discovery & Reuse", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, textColor=colors.HexColor('#555555'))))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Complete Demo Package", ParagraphStyle('subtitle2', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#777777'))))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("September 30, 2026", ParagraphStyle('date', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER)))
story.append(Spacer(1, 1*inch))
story.append(Paragraph("For Financial & Business Consultants", ParagraphStyle('desc', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, fontStyle='italic', textColor=colors.HexColor('#666666'))))

story.append(PageBreak())

# Table of Contents
story.append(Paragraph("TABLE OF CONTENTS", heading_style))
story.append(Spacer(1, 0.2*inch))

toc_items = [
    "1. Executive Summary",
    "2. Problem & Solution",
    "3. 9-Step Workflow Overview",
    "4. Demo Scenario (30-minute walkthrough)",
    "5. System Features",
    "6. Architecture Overview",
    "7. Sample Data",
    "8. Setup Instructions",
    "9. Known Limitations",
    "10. Production Roadmap",
    "11. Next Steps"
]

for item in toc_items:
    story.append(Paragraph(item, normal_style))

story.append(PageBreak())

# 1. Executive Summary
story.append(Paragraph("1. EXECUTIVE SUMMARY", heading_style))
story.append(Spacer(1, 0.1*inch))

exec_summary = """
Liqueo is a knowledge discovery and reuse system that enables financial and business
consultants to search, discover, synthesize, and reuse insights from past engagements.
The system demonstrates a complete 9-step workflow for capturing consulting knowledge
and making it available for future projects.

<b>Key Value Proposition:</b><br/>
• Reduce proposal development time from 3-5 days to 1 hour<br/>
• Preserve institutional knowledge through systematic capture<br/>
• Improve proposal quality by building on proven approaches<br/>
• Enable team learning through continuous knowledge reuse<br/>
"""
story.append(Paragraph(exec_summary, normal_style))
story.append(Spacer(1, 0.2*inch))

story.append(PageBreak())

# 2. Problem & Solution
story.append(Paragraph("2. THE PROBLEM & SOLUTION", heading_style))
story.append(Spacer(1, 0.1*inch))

problem = """
<b>The Challenge:</b><br/>
Consulting firms face a knowledge fragmentation problem. When a consultant receives an RFP
for a new engagement, they:
<br/>• Don't know if similar work was done before<br/>
• Can't easily find relevant past engagements<br/>
• Must reinvent approaches from scratch<br/>
• Lose institutional learning with staff turnover<br/>
<br/><b>The Cost:</b><br/>
A fintech client RFP due Monday requires 70 hours of proposal work over the weekend.

<b>The Solution:</b><br/>
Liqueo enables consultants to search for similar past engagements in seconds, analyze patterns
in proven approaches, and adapt them for new contexts. What takes 70 hours from scratch takes
70 minutes with Liqueo.
"""
story.append(Paragraph(problem, normal_style))
story.append(Spacer(1, 0.2*inch))

story.append(PageBreak())

# 3. 9-Step Workflow
story.append(Paragraph("3. THE 9-STEP WORKFLOW", heading_style))
story.append(Spacer(1, 0.1*inch))

workflow_steps = [
    ("Step 1: Identify Problem", "Consultant defines the challenge with context (industry, type, constraints)"),
    ("Step 2: Search Knowledge", "System searches knowledge base using semantic similarity"),
    ("Step 3: Identify Related Docs", "System finds templates, lessons learned, success patterns"),
    ("Step 4: AI Summarize", "LLM provides executive summary, approach, outcomes, recommendations"),
    ("Step 5: Review & Evaluate", "Consultant reviews relevance and takes notes on applicability"),
    ("Step 6: Select Content", "Consultant chooses consulting approach, timeline, team structure to reuse"),
    ("Step 7: Create New Output", "Consultant creates new engagement using auto-populated template"),
    ("Step 8: Tag & Classify", "Add metadata (industry, type, tags) for future discovery"),
    ("Step 9: Store Knowledge", "New engagement saved and indexed for future reuse"),
]

for step, description in workflow_steps:
    story.append(Paragraph(f"<b>{step}</b>", ParagraphStyle('step', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#2d5aa6'))))
    story.append(Paragraph(description, normal_style))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# 4. Demo Scenario
story.append(Paragraph("4. DEMO SCENARIO (30-minute walkthrough)", heading_style))
story.append(Spacer(1, 0.1*inch))

demo_scenario = """
<b>Scenario Setup:</b><br/>
It's Friday 4pm. A fintech client sends an RFP for core banking optimization with 30% cost
reduction. Proposal is due Monday 9am. Team has 70 hours to deliver.<br/>
<br/><b>Question:</b> Have we solved this before? What can we learn from past engagements?<br/>
<br/><b>Demo Timeline:</b><br/>
• Part 1 (2 min): Show RFP requirement and problem<br/>
• Part 2 (3 min): Search knowledge base for similar cases<br/>
• Part 3 (4 min): View details of Investment Bank engagement (78% relevant)<br/>
• Part 4 (6 min): Show AI synthesis of patterns from 3 cases<br/>
• Part 5 (8 min): Walk through workflow Steps 5-7 (evaluate, select, create)<br/>
• Part 6 (3 min): Show completed engagement ready for proposal<br/>
<br/><b>Expected Outcomes:</b><br/>
• Find 3 similar banking cases ranked by relevance<br/>
• See full engagement details (approach, outcomes, timeline, team)<br/>
• Get AI synthesis showing recommended 3-phase approach<br/>
• Create adapted fintech proposal in 70 minutes<br/>
• Store it for next consultant facing similar challenge<br/>
"""
story.append(Paragraph(demo_scenario, normal_style))

story.append(PageBreak())

# 5. System Features
story.append(Paragraph("5. SYSTEM FEATURES", heading_style))
story.append(Spacer(1, 0.1*inch))

features = """
<b>Knowledge Base:</b><br/>
• Store consulting engagements with rich metadata (industry, type, value, duration)<br/>
• Tag-based classification for discovery<br/>
• Flexible filtering by multiple dimensions<br/>
<br/><b>Semantic Search:</b><br/>
• Find relevant past engagements using AI embeddings<br/>
• Keyword-based fallback (no API required)<br/>
• Relevance scoring with explanation<br/>
<br/><b>Recommendation Engine:</b><br/>
• Suggest similar engagements automatically<br/>
• Pattern matching across similar cases<br/>
• Industry-specific recommendations<br/>
<br/><b>LLM-Powered Synthesis:</b><br/>
• AI generates insights from similar cases<br/>
• Visible source traceability<br/>
• Graceful degradation without APIs<br/>
<br/><b>Web Interface:</b><br/>
• 4 main tabs (Add, Search, Recommend, Workflow)<br/>
• File upload support (PDF, Word, Excel, CSV, Text)<br/>
• URL download (OneDrive, SharePoint)<br/>
• Modal detail views for engagement exploration<br/>
"""
story.append(Paragraph(features, normal_style))

story.append(PageBreak())

# 6. Architecture
story.append(Paragraph("6. ARCHITECTURE OVERVIEW", heading_style))
story.append(Spacer(1, 0.1*inch))

architecture = """
<b>System Layers:</b><br/>
<br/>User Applications<br/>
↓<br/>
Liqueo Toolkit (Public API)<br/>
├── Orchestration Layer (KnowledgeSynthesizer)<br/>
├── Business Logic (RecommendationEngine, KnowledgeBase)<br/>
├── Service Layer (EmbeddingsManager)<br/>
└── Data Model (Document, SearchResult, Recommendation)<br/>
↓<br/>
External Services<br/>
├── OpenAI / Anthropic APIs (embeddings, synthesis)<br/>
├── Local Storage (.liqueo/ directory)<br/>
└── Cache Layer (embeddings, metadata)<br/>
<br/><b>Data Flow:</b><br/>
1. <b>Ingestion:</b> Document → Validate → Store → Embed → Cache<br/>
2. <b>Search:</b> Query → Generate embedding → Compare (cosine similarity) → Rank<br/>
3. <b>Recommend:</b> Search results → Extract patterns → Generate reasoning<br/>
4. <b>Synthesize:</b> Similar cases → Format context → LLM → Generate insights<br/>
"""
story.append(Paragraph(architecture, normal_style))

story.append(PageBreak())

# 7. Sample Data
story.append(Paragraph("7. SAMPLE DATA (Pre-loaded for Demo)", heading_style))
story.append(Spacer(1, 0.1*inch))

sample_data = """
<b>Three Synthetic Engagements Ready to Load:</b><br/>
<br/><b>1. Investment Bank Back-Office Reorganization</b><br/>
   Industry: Financial Services<br/>
   Value: $2.8M | Duration: 12 months<br/>
   Outcome: 40% cost reduction<br/>
   Approach: 3-phase (assess → design → implement)<br/>
<br/><b>2. Retail Bank Technology Consolidation</b><br/>
   Industry: Financial Services<br/>
   Value: $1.5M | Duration: 9 months<br/>
   Outcome: 35% IT cost reduction<br/>
   Approach: Vendor assessment + solution design<br/>
<br/><b>3. Payment Processor Cost Optimization</b><br/>
   Industry: Financial Technology<br/>
   Value: $0.8M | Duration: 6 months<br/>
   Outcome: 28% cost reduction<br/>
   Approach: Cost analysis + vendor negotiation<br/>
<br/>Load all three with: <b>python load_sample_data.py</b>
"""
story.append(Paragraph(sample_data, normal_style))

story.append(PageBreak())

# 8. Setup Instructions
story.append(Paragraph("8. QUICK SETUP (5 minutes)", heading_style))
story.append(Spacer(1, 0.1*inch))

setup = """
<b>Installation:</b><br/>
<br/>$ git clone https://github.com/hemalp143/Liqueo.git<br/>
$ cd Liqueo<br/>
$ python3 -m venv venv<br/>
$ source venv/bin/activate<br/>
$ pip install -r requirements.txt<br/>
<br/><b>Load Sample Data:</b><br/>
$ python load_sample_data.py<br/>
<br/><b>Start Web UI:</b><br/>
$ streamlit run app.py<br/>
<br/>Browser opens: http://localhost:8501<br/>
<br/><b>Supported Environments:</b><br/>
• Local (macOS, Windows, Linux)<br/>
• Google Colab<br/>
• Docker Container<br/>
• Production Server<br/>
<br/><b>API Keys (Optional):</b><br/>
• ANTHROPIC_API_KEY (Claude embeddings/synthesis)<br/>
• OPENAI_API_KEY (OpenAI embeddings/synthesis)<br/>
• System works without keys (keyword search fallback)<br/>
"""
story.append(Paragraph(setup, normal_style))

story.append(PageBreak())

# 9. Known Limitations
story.append(Paragraph("9. KNOWN LIMITATIONS", heading_style))
story.append(Spacer(1, 0.1*inch))

limitations = """
<b>Scalability:</b> Current system handles 100-5,000 documents on single machine<br/>
<b>Persistence:</b> Workflow progress stored in-memory only (refreshing loses progress)<br/>
<b>File Formats:</b> PDF, Word, Excel, CSV, Text supported (no PowerPoint yet)<br/>
<b>API Costs:</b> Semantic search ~$0.02 per document (embeddings cached)<br/>
<b>Accuracy:</b> LLM synthesis can hallucinate (human review required)<br/>
<b>Multi-User:</b> No authentication or access control yet<br/>
<b>Analytics:</b> No usage tracking or ROI measurement<br/>
<b>Integration:</b> Manual data entry (no CRM/PM tool sync)<br/>
<br/><b>All limitations have documented workarounds and Phase 2+ solutions.</b>
"""
story.append(Paragraph(limitations, normal_style))

story.append(PageBreak())

# 10. Production Roadmap
story.append(Paragraph("10. PRODUCTION ROADMAP (8 Phases, 32 Weeks)", heading_style))
story.append(Spacer(1, 0.1*inch))

roadmap = """
<b>Phase 1: Foundation</b> ✅ COMPLETE<br/>
Working prototype with 9-step workflow<br/>
<br/><b>Phase 2: Database Persistence</b> (4 weeks)<br/>
Add PostgreSQL, workflow resumption, audit logging<br/>
<br/><b>Phase 3: Vector Database</b> (4 weeks)<br/>
Scale to 50k+ documents with FAISS or Pinecone<br/>
<br/><b>Phase 4: Document Processing</b> (4 weeks)<br/>
Add PowerPoint, OCR, text chunking, auto-summarization<br/>
<br/><b>Phase 5: Team & Collaboration</b> (4 weeks)<br/>
Multi-user auth, role-based access, versioning<br/>
<br/><b>Phase 6: Integrations</b> (4 weeks)<br/>
Salesforce, Monday.com, OneDrive sync, Slack bot<br/>
<br/><b>Phase 7: Analytics</b> (4 weeks)<br/>
Dashboard, trending, ROI calculator, team metrics<br/>
<br/><b>Phase 8: Governance</b> (4 weeks)<br/>
Quality scoring, duplicate detection, approval workflows<br/>
<br/><b>Timeline to Production: 8 months with full feature set</b>
"""
story.append(Paragraph(roadmap, normal_style))

story.append(PageBreak())

# 11. Next Steps
story.append(Paragraph("11. NEXT STEPS", heading_style))
story.append(Spacer(1, 0.1*inch))

next_steps = """
<b>Immediate (Today):</b><br/>
✓ Review this demo package<br/>
✓ Install Liqueo locally or in Colab<br/>
✓ Load sample data<br/>
✓ Run through 30-minute demo<br/>
<br/><b>Week 1 (Post-Demo):</b><br/>
• Collect stakeholder feedback<br/>
• Identify Phase 2 priority (likely: database persistence)<br/>
• Share documentation with team<br/>
<br/><b>Weeks 2-4:</b><br/>
• Implement database persistence layer<br/>
• Add workflow session resumption<br/>
• Begin user acceptance testing<br/>
<br/><b>Months 2-3:</b><br/>
• Vector database integration<br/>
• Multi-user architecture design<br/>
• Production security audit<br/>
<br/><b>For Questions:</b><br/>
Email: hemalp1434@gmail.com<br/>
GitHub: https://github.com/hemalp143/Liqueo<br/>
Branch: claude/knowledge-discovery-reuse-e3nr1n<br/>
"""
story.append(Paragraph(next_steps, normal_style))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("---", normal_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor('#999999'))))

# Build PDF
doc.build(story)
print(f"✅ PDF created: {pdf_path}")
print(f"📄 File size: {len(open(pdf_path, 'rb').read()) / 1024:.1f} KB")
