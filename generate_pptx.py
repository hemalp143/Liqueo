#!/usr/bin/env python3
"""Generate PowerPoint presentation from Liqueo demo materials."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from datetime import datetime

# Create presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Define colors
PRIMARY_COLOR = RGBColor(26, 84, 144)  # #1a5490
SECONDARY_COLOR = RGBColor(45, 90, 166)  # #2d5aa6
ACCENT_COLOR = RGBColor(76, 175, 80)  # Green
TEXT_COLOR = RGBColor(51, 51, 51)

def add_title_slide(prs, title, subtitle):
    """Add title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = PRIMARY_COLOR

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4), Inches(9), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    subtitle_frame.paragraphs[0].font.size = Pt(28)
    subtitle_frame.paragraphs[0].font.color.rgb = RGBColor(200, 220, 255)
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Date
    date_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.5))
    date_frame = date_box.text_frame
    date_frame.text = "September 30, 2026"
    date_frame.paragraphs[0].font.size = Pt(16)
    date_frame.paragraphs[0].font.color.rgb = RGBColor(200, 220, 255)
    date_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    return slide

def add_content_slide(prs, title, content_items, item_type='bullet'):
    """Add content slide with title and bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(40)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR

    # Separator line
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(1.3), Inches(9), Inches(0))
    line.line.color.rgb = SECONDARY_COLOR
    line.line.width = Pt(2)

    # Content
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.6), Inches(8.6), Inches(5.5))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True

    for i, item in enumerate(content_items):
        if i > 0:
            text_frame.add_paragraph()

        p = text_frame.paragraphs[i]
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_COLOR
        p.level = 0
        p.space_before = Pt(6)
        p.space_after = Pt(6)

        if item_type == 'bullet':
            p.level = 0

    return slide

def add_two_column_slide(prs, title, left_items, right_items):
    """Add slide with two columns."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(40)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR

    # Left column
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.2), Inches(5.5))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True

    for i, item in enumerate(left_items):
        if i > 0:
            left_frame.add_paragraph()
        p = left_frame.paragraphs[i]
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_COLOR
        p.space_after = Pt(8)

    # Right column
    right_box = slide.shapes.add_textbox(Inches(5.3), Inches(1.5), Inches(4.2), Inches(5.5))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True

    for i, item in enumerate(right_items):
        if i > 0:
            right_frame.add_paragraph()
        p = right_frame.paragraphs[i]
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_COLOR
        p.space_after = Pt(8)

    return slide

# Slide 1: Title
add_title_slide(prs, "LIQUEO", "Knowledge Discovery & Reuse for Consultants")

# Slide 2: Agenda
add_content_slide(prs, "AGENDA", [
    "The Problem: Knowledge Fragmentation",
    "The Solution: Liqueo System",
    "9-Step Workflow Overview",
    "30-Minute Demo Walkthrough",
    "System Features & Architecture",
    "Production Roadmap",
    "Q&A"
])

# Slide 3: The Problem
add_two_column_slide(prs, "THE PROBLEM", [
    "• RFP arrives Friday 4pm",
    "• Due Monday 9am",
    "• Only 70 hours to deliver",
    "• Team doesn't know:",
    "  - Similar work done before",
    "  - Which approach worked",
    "  - How long it took",
    "  - What cost was"
], [
    "• Result: Reinvent from scratch",
    "",
    "• Cost: 3-5 days of work",
    "",
    "• Risk: Miss opportunities",
    "",
    "• Loss: Knowledge disappears",
    "  when staff leaves"
])

# Slide 4: The Solution
add_two_column_slide(prs, "THE SOLUTION: LIQUEO", [
    "SEARCH",
    "Find 3 similar past",
    "engagements in seconds",
    "",
    "ANALYZE",
    "AI extracts patterns,",
    "approaches, lessons"
], [
    "ADAPT",
    "Customize proven",
    "approach for new context",
    "",
    "STORE",
    "Save for next consultant",
    "to discover & reuse"
])

# Slide 5: The Impact
add_content_slide(prs, "THE IMPACT", [
    "70 hours → 70 minutes (60x speedup)",
    "80% of content from past engagements",
    "Based on proven approaches, not invented",
    "Knowledge preserved for future reuse",
    "Team learns from every project"
])

# Slide 6: 9-Step Workflow
slide = prs.slides.add_slide(prs.slide_layouts[6])
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
title_frame = title_box.text_frame
title_frame.text = "9-STEP KNOWLEDGE REUSE WORKFLOW"
title_frame.paragraphs[0].font.size = Pt(32)
title_frame.paragraphs[0].font.bold = True
title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR

content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.6), Inches(5.5))
text_frame = content_box.text_frame
text_frame.word_wrap = True

steps = [
    "1️⃣  Identify Problem  →  Define challenge",
    "2️⃣  Search Knowledge  →  Find similar cases",
    "3️⃣  Identify Docs  →  Extract templates & lessons",
    "4️⃣  AI Summarize  →  Get analysis & recommendations",
    "5️⃣  Review & Evaluate  →  Assess applicability",
    "6️⃣  Select Content  →  Choose what to reuse",
    "7️⃣  Create Output  →  Build new engagement",
    "8️⃣  Tag & Classify  →  Add metadata",
    "9️⃣  Store Knowledge  →  Available for next user"
]

for i, step in enumerate(steps):
    if i > 0:
        text_frame.add_paragraph()
    p = text_frame.paragraphs[i]
    p.text = step
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_COLOR
    p.space_before = Pt(6)
    p.space_after = Pt(6)

# Slide 7: Demo Scenario
add_content_slide(prs, "DEMO SCENARIO", [
    "Fintech RFP: Core Banking Optimization",
    "Goal: 30% cost reduction",
    "Constraint: 70 hours to proposal",
    "",
    "Question: Have we solved this before?",
    "",
    "Liqueo Answer: Yes! 3 relevant cases found",
    "(Banking restructuring + cost optimization)"
])

# Slide 8: Demo Flow
add_content_slide(prs, "30-MINUTE DEMO FLOW", [
    "Part 1 (2 min): Show RFP & challenge",
    "Part 2 (3 min): Search → Find 3 cases",
    "Part 3 (4 min): View → Explore full details",
    "Part 4 (6 min): AI Synthesis → Pattern analysis",
    "Part 5 (8 min): Workflow → Create adapted proposal",
    "Part 6 (3 min): Complete → Ready for Monday submission"
])

# Slide 9: Key Features
add_two_column_slide(prs, "SYSTEM FEATURES", [
    "Knowledge Base",
    "✓ Document storage",
    "✓ Rich metadata",
    "✓ Smart filtering",
    "",
    "Search Engine",
    "✓ Semantic search",
    "✓ Keyword fallback",
    "✓ Relevance scoring"
], [
    "Recommendations",
    "✓ Similar cases",
    "✓ Pattern matching",
    "✓ Industry trends",
    "",
    "Web Interface",
    "✓ 4 main tabs",
    "✓ File upload",
    "✓ Modal details"
])

# Slide 10: Architecture
add_content_slide(prs, "ARCHITECTURE", [
    "USER → Web UI (Streamlit)",
    "↓",
    "CORE → KnowledgeBase, Search, Recommendations, Synthesis",
    "↓",
    "SERVICES → Embeddings, LLM APIs, File Parsing",
    "↓",
    "STORAGE → Local JSON files (.liqueo/ directory)",
    "",
    "Three Operating Modes: Full (APIs) → Hybrid (partial) → Manual (no API)"
])

# Slide 11: Sample Data
add_content_slide(prs, "SAMPLE DATA (3 Engagements)", [
    "🏦 Investment Bank Back-Office",
    "   $2.8M | 12 months | 40% cost reduction",
    "",
    "🏦 Retail Bank Technology Consolidation",
    "   $1.5M | 9 months | 35% cost reduction",
    "",
    "💳 Payment Processor Cost Optimization",
    "   $0.8M | 6 months | 28% cost reduction"
])

# Slide 12: Quick Setup
add_content_slide(prs, "QUICK START (5 minutes)", [
    "$ git clone https://github.com/hemalp143/Liqueo.git",
    "$ cd Liqueo",
    "$ pip install -r requirements.txt",
    "$ python load_sample_data.py",
    "$ streamlit run app.py",
    "",
    "✅ Ready for demo!"
])

# Slide 13: Supported Environments
add_content_slide(prs, "DEPLOYMENT OPTIONS", [
    "✓ Local Development (Mac/Windows/Linux)",
    "✓ Google Colab (browser-based)",
    "✓ Docker Container (isolated)",
    "✓ Production Server (gunicorn/streamlit)",
    "",
    "Optional: ANTHROPIC_API_KEY or OPENAI_API_KEY",
    "(System works without keys - uses keyword search fallback)"
])

# Slide 14: Known Limitations
add_two_column_slide(prs, "KNOWN LIMITATIONS", [
    "Current State:",
    "• Single machine only",
    "• 100-5,000 documents",
    "• In-memory session state",
    "• Single-user (no auth)",
    "• Limited file formats"
], [
    "Solutions Planned:",
    "• Phase 2: Database persistence",
    "• Phase 3: Vector database (50k+ docs)",
    "• Phase 5: Multi-user auth",
    "• Phase 4: Advanced parsing",
    "• Phase 6-8: Advanced features"
])

# Slide 15: Production Roadmap
slide = prs.slides.add_slide(prs.slide_layouts[6])
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
title_frame = title_box.text_frame
title_frame.text = "8-PHASE PRODUCTION ROADMAP (32 weeks)"
title_frame.paragraphs[0].font.size = Pt(32)
title_frame.paragraphs[0].font.bold = True
title_frame.paragraphs[0].font.color.rgb = PRIMARY_COLOR

content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.6), Inches(5.5))
text_frame = content_box.text_frame
text_frame.word_wrap = True

phases = [
    "Phase 1: Foundation ✅ (Complete)",
    "Phase 2: Database Persistence (4 wks) - Workflow resumption, audit logs",
    "Phase 3: Vector Database (4 wks) - Scale to 50k+ docs",
    "Phase 4: Document Processing (4 wks) - PowerPoint, OCR, chunking",
    "Phase 5: Team & Collaboration (4 wks) - Multi-user, auth, versioning",
    "Phase 6: Integrations (4 wks) - Salesforce, Monday.com, Slack",
    "Phase 7: Analytics (4 wks) - Dashboard, ROI metrics",
    "Phase 8: Governance (4 wks) - Quality scoring, approvals"
]

for i, phase in enumerate(phases):
    if i > 0:
        text_frame.add_paragraph()
    p = text_frame.paragraphs[i]
    p.text = phase
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_COLOR
    p.space_before = Pt(4)
    p.space_after = Pt(4)

# Slide 16: Success Metrics
add_content_slide(prs, "SUCCESS METRICS", [
    "✓ Time to Proposal: 70 hours → 70 minutes (60x faster)",
    "✓ Content Reuse: 80% from past engagements",
    "✓ Search Speed: <1 second for 100-doc corpus",
    "✓ Documentation: 300+ pages, all audiences covered",
    "✓ Code Quality: 6 unit tests, clean architecture",
    "✓ Demo Ready: 30-minute walkthrough with sample data"
])

# Slide 17: Next Steps
add_two_column_slide(prs, "NEXT STEPS", [
    "This Week",
    "✓ Review demo package",
    "✓ Install Liqueo",
    "✓ Load sample data",
    "✓ Run 30-min demo"
], [
    "Next Month",
    "• Collect feedback",
    "• Plan Phase 2",
    "• Start implementation",
    "• Expand to team"
])

# Slide 18: Contact & Resources
slide = prs.slides.add_slide(prs.slide_layouts[6])
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = SECONDARY_COLOR

contact_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2.5))
text_frame = contact_box.text_frame

title = text_frame.paragraphs[0]
title.text = "CONTACT & RESOURCES"
title.font.size = Pt(40)
title.font.bold = True
title.font.color.rgb = RGBColor(255, 255, 255)
title.alignment = PP_ALIGN.CENTER

text_frame.add_paragraph()
text_frame.add_paragraph()

p = text_frame.paragraphs[1]
p.text = "Email: hemalp1434@gmail.com"
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

p = text_frame.paragraphs[2]
p.text = "GitHub: https://github.com/hemalp143/Liqueo"
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

text_frame.add_paragraph()
p = text_frame.paragraphs[3]
p.text = "Documentation: SETUP.md | DEMO_SCENARIO.md | LIMITATIONS_AND_NEXT_STEPS.md"
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(200, 220, 255)
p.alignment = PP_ALIGN.CENTER

# Save presentation
pptx_path = "Liqueo_Demo_Presentation.pptx"
prs.save(pptx_path)
print(f"✅ PowerPoint created: {pptx_path}")
print(f"📊 File size: {len(open(pptx_path, 'rb').read()) / 1024:.1f} KB")
print(f"📊 Slides: 18")
