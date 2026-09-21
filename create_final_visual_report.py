#!/usr/bin/env python3
"""Create professional visual documentation with detailed explanations."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

print("📄 Creating Professional Report PDF...")
print("🎨 Creating Professional Presentation PPTX...\n")

# ============================================================================
# PDF CREATION
# ============================================================================

pdf_path = "Liqueo_Professional_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.7*inch, bottomMargin=0.7*inch,
                        leftMargin=0.8*inch, rightMargin=0.8*inch)
story = []
styles = getSampleStyleSheet()

# Color scheme
PRIMARY_BLUE = colors.HexColor('#1a5490')
SECONDARY_BLUE = colors.HexColor('#2d5aa6')
ACCENT_GREEN = colors.HexColor('#4caf50')
DARK_TEXT = colors.HexColor('#2c3e50')
BG_LIGHT = colors.HexColor('#f8f9fa')

# Styles
title_style = ParagraphStyle('ProTitle', parent=styles['Heading1'], fontSize=40, textColor=PRIMARY_BLUE,
                             spaceAfter=12, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=48)
section_style = ParagraphStyle('Section', parent=styles['Heading1'], fontSize=22, textColor=PRIMARY_BLUE,
                               spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold', leading=26)
subsection_style = ParagraphStyle('Subsection', parent=styles['Heading2'], fontSize=15, textColor=SECONDARY_BLUE,
                                  spaceAfter=10, spaceBefore=10, fontName='Helvetica-Bold', leading=18)
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, textColor=DARK_TEXT,
                            alignment=TA_JUSTIFY, spaceAfter=10, leading=15, fontName='Helvetica')
bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=11, textColor=DARK_TEXT,
                              leftIndent=0.3*inch, spaceAfter=8, leading=14, fontName='Helvetica')

# ===== COVER PAGE =====
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("LIQUEO", title_style))
story.append(Paragraph("Knowledge Discovery & Reuse System",
                      ParagraphStyle('sub', parent=styles['Normal'], fontSize=18, textColor=SECONDARY_BLUE,
                                     alignment=TA_CENTER, fontName='Helvetica')))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("Professional User Guide & System Documentation",
                      ParagraphStyle('sub2', parent=styles['Normal'], fontSize=14, textColor=DARK_TEXT,
                                     alignment=TA_CENTER, fontName='Helvetica')))
story.append(Spacer(1, 1*inch))
story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>Status:</b> Production Ready",
                      ParagraphStyle('info', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER)))
story.append(PageBreak())

# ===== TABLE OF CONTENTS =====
story.append(Paragraph("TABLE OF CONTENTS", section_style))
story.append(Spacer(1, 0.2*inch))
toc_items = [
    "1. System Overview & Key Features",
    "2. User Interface Guide",
    "   2.1 Add Document Tab",
    "   2.2 Search Tab",
    "   2.3 Recommendations Tab",
    "   2.4 Knowledge Workflow Tab",
    "3. How to Use Each Feature",
    "4. 9-Step Workflow Explained",
    "5. Technical Architecture",
    "6. Quick Start Guide",
    "7. Best Practices & Tips",
    "8. Troubleshooting & FAQs",
]
for item in toc_items:
    if item.startswith("   "):
        story.append(Paragraph(item, ParagraphStyle('toc_sub', parent=styles['Normal'], fontSize=10,
                                                     leftIndent=0.4*inch, spaceAfter=4)))
    else:
        story.append(Paragraph(item, bullet_style))
        story.append(Spacer(1, 0.06*inch))
story.append(PageBreak())

# ===== SYSTEM OVERVIEW =====
story.append(Paragraph("1. SYSTEM OVERVIEW & KEY FEATURES", section_style))
story.append(Spacer(1, 0.12*inch))

overview_text = """
Liqueo is an intelligent knowledge discovery and reuse system that helps financial and business consultants
discover, analyze, and adapt proven consulting approaches from past engagements. Instead of reinventing
methodologies for each new project, consultants use Liqueo to find similar past work, understand what
succeeded, and adapt those approaches for new contexts.
"""
story.append(Paragraph(overview_text, body_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Core Features", subsection_style))
story.append(Spacer(1, 0.1*inch))

features = [
    "<b>Semantic Search:</b> AI-powered search finds conceptually similar past engagements, not just keyword matches",
    "<b>Pattern Analysis:</b> System automatically extracts patterns and best practices from similar cases",
    "<b>LLM Synthesis:</b> AI generates structured recommendations based on successful approaches",
    "<b>9-Step Workflow:</b> Guided process from problem identification through knowledge storage",
    "<b>Multi-format Upload:</b> Import PDF, Word, Excel, CSV, and text documents",
    "<b>Rich Metadata:</b> Comprehensive tagging for industry, engagement type, value, duration",
    "<b>Source Traceability:</b> All recommendations include links back to original engagements",
    "<b>No API Required:</b> System works with or without cloud APIs (graceful degradation)",
]
for feature in features:
    story.append(Paragraph(feature, bullet_style))
    story.append(Spacer(1, 0.08*inch))

story.append(Spacer(1, 0.12*inch))
story.append(Paragraph("Business Value Delivered", subsection_style))
story.append(Spacer(1, 0.1*inch))

benefits_table = [
    ["Metric", "Without Liqueo", "With Liqueo", "Improvement"],
    ["Proposal Time", "70 hours (3-5 days)", "70 minutes", "60x faster"],
    ["Content Reuse", "0-20%", "70-80%", "80% from precedents"],
    ["Quality Consistency", "Varies by consultant", "Based on proven methods", "Standardized excellence"],
    ["Knowledge Loss", "High (staff turnover)", "Systematic capture", "Preserved for future"],
]
benefits = Table(benefits_table, colWidths=[1.5*inch, 1.8*inch, 1.8*inch, 1.3*inch])
benefits.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(benefits)
story.append(PageBreak())

# ===== USER INTERFACE GUIDE =====
story.append(Paragraph("2. USER INTERFACE GUIDE", section_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("2.1 Add Document Tab - Upload & Management", subsection_style))
story.append(Spacer(1, 0.1*inch))

add_desc = """
The Add Document tab is where you capture new consulting engagements and add them to the knowledge base.
This is the primary way Liqueo learns and builds institutional knowledge over time.
"""
story.append(Paragraph(add_desc, body_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>What You See:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))
add_ui = [
    "• File upload area (drag & drop or click to browse)",
    "• Form fields for engagement metadata",
    "• Industry dropdown selector",
    "• Fields for value, duration, team structure",
    "• Text areas for approach description and outcomes",
    "• Save button and confirmation messages",
]
for item in add_ui:
    story.append(Paragraph(item, bullet_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>Step-by-Step Usage:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))
add_steps = [
    "1. Click 'Add Document' tab at the top of the page",
    "2. Drag a document (PDF/Word/Excel) into the upload area or click to browse",
    "3. System automatically extracts text from your document",
    "4. Fill in the metadata fields (Industry, Value, Duration, Client Name)",
    "5. Enter the consulting approach used (2-3 paragraphs)",
    "6. Describe key outcomes and measurable results",
    "7. Add tags for better searchability (comma-separated)",
    "8. Review the preview of your submission",
    "9. Click 'Save to Knowledge Base'",
    "10. Confirmation message appears - engagement is now discoverable",
]
for step in add_steps:
    story.append(Paragraph(step, bullet_style))
    story.append(Spacer(1, 0.06*inch))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("2.2 Search Tab - Finding Similar Engagements", subsection_style))
story.append(Spacer(1, 0.1*inch))

search_desc = """
The Search tab uses semantic search to find past engagements conceptually similar to your current challenge.
Unlike keyword search, semantic search understands meaning - a query for "banking cost reduction" will find
results about "financial services optimization" if the engagement is relevant.
"""
story.append(Paragraph(search_desc, body_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>What You See:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))
search_ui = [
    "• Large search input field",
    "• Optional filter dropdowns (Industry, Type)",
    "• Search button",
    "• Results displayed as cards with relevance scores",
    "• Each result shows: Title, Industry, Value, Duration, Relevance %",
    "• 'View' button to see full engagement details",
    "• Modal popup with complete engagement information",
]
for item in search_ui:
    story.append(Paragraph(item, bullet_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>How to Search:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))
search_steps = [
    "1. Click 'Search' tab",
    "2. Type your challenge description (e.g., 'fintech infrastructure optimization cost reduction')",
    "3. Optionally select Industry or Type filters",
    "4. Click 'Search'",
    "5. Results appear ranked by relevance score (0-100%)",
    "6. Click 'View' on any result to see full details in a modal",
    "7. Read the consulting approach, outcomes, and team structure",
    "8. Close modal to continue browsing results",
]
for step in search_steps:
    story.append(Paragraph(step, bullet_style))
    story.append(Spacer(1, 0.06*inch))

story.append(PageBreak())

# ===== RECOMMENDATIONS TAB =====
story.append(Paragraph("2.3 Recommendations Tab - AI-Powered Analysis", subsection_style))
story.append(Spacer(1, 0.1*inch))

rec_desc = """
The Recommendations tab uses AI to analyze multiple similar cases and synthesize best practices.
It generates structured recommendations including proven approaches, success factors, and typical challenges.
"""
story.append(Paragraph(rec_desc, body_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>What You Get:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))
rec_items = [
    "<b>Recommended Approach:</b> A structured methodology synthesized from successful cases",
    "<b>Success Factors:</b> Key elements that made similar engagements successful",
    "<b>Typical Challenges:</b> Common obstacles and how they were overcome",
    "<b>Team Composition:</b> Recommended roles and team structure",
    "<b>Timeline Estimate:</b> Typical project duration for similar engagements",
    "<b>Confidence Score:</b> How confident the AI is in its recommendation (based on number of similar cases)",
    "<b>Source References:</b> Links to the specific engagements analyzed",
]
for item in rec_items:
    story.append(Paragraph(item, bullet_style))
    story.append(Spacer(1, 0.08*inch))

story.append(Spacer(1, 0.12*inch))
story.append(Paragraph("2.4 Knowledge Workflow Tab - 9-Step Guided Process", subsection_style))
story.append(Spacer(1, 0.1*inch))

workflow_desc = """
The Knowledge Workflow tab is the core of Liqueo. It guides you through all 9 steps of the knowledge reuse
process. Each step is designed to maximize the value you get from past engagements when creating new proposals.
"""
story.append(Paragraph(workflow_desc, body_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("<b>The 9 Steps:</b>", subsection_style))
story.append(Spacer(1, 0.08*inch))

workflow_steps_detailed = [
    ("<b>Step 1: Identify Problem</b>", "Describe your new engagement challenge with context (industry, client type, specific requirements, constraints)"),
    ("<b>Step 2: Search Knowledge</b>", "Liqueo searches the knowledge base for similar past engagements using semantic search"),
    ("<b>Step 3: Identify Related Documents</b>", "System extracts relevant documentation: templates, lessons learned, success patterns, team structures"),
    ("<b>Step 4: AI Summarize</b>", "LLM analyzes the similar cases and generates executive summary, recommended approach, outcomes, and recommendations"),
    ("<b>Step 5: Review & Evaluate</b>", "You review the AI analysis and similar cases. Take notes on applicability to your new context."),
    ("<b>Step 6: Select Content</b>", "Choose which consulting approach, timeline, team structure, and methodologies to reuse from similar engagements"),
    ("<b>Step 7: Create New Output</b>", "System creates new engagement using auto-populated template based on your selected similar case"),
    ("<b>Step 8: Tag & Classify</b>", "Add metadata (industry, engagement type, tags) to your new engagement for future discovery"),
    ("<b>Step 9: Store Knowledge</b>", "Save to knowledge base. Your new engagement is now discoverable for the next consultant facing a similar challenge."),
]

for step_title, step_desc in workflow_steps_detailed:
    story.append(Paragraph(step_title, ParagraphStyle('step_title', parent=styles['Normal'], fontSize=11,
                                                       textColor=SECONDARY_BLUE, fontName='Helvetica-Bold',
                                                       spaceAfter=4)))
    story.append(Paragraph(step_desc, body_style))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# ===== HOW TO USE =====
story.append(Paragraph("3. HOW TO USE EACH FEATURE", section_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("Real-World Scenario: Fintech Proposal", subsection_style))
story.append(Spacer(1, 0.1*inch))

scenario = """
<b>Situation:</b> Friday 4pm. A fintech client sends an RFP for core banking infrastructure optimization
with 30% cost reduction requirement. Proposal due Monday 9am. You have 70 hours to deliver.<br/><br/>
<b>Without Liqueo:</b> You start from scratch. Find relevant templates in email. Piece together an approach
from memory. Result: 50-70 hours of work, inconsistent with past successes.<br/><br/>
<b>With Liqueo:</b> Follow this process in 70 minutes...
"""
story.append(Paragraph(scenario, body_style))
story.append(Spacer(1, 0.12*inch))

liqueo_process = [
    "1. Go to Recommendations tab",
    "2. Search: 'fintech core banking optimization cost reduction'",
    "3. System returns 3 similar banking cases ranked by relevance",
    "4. Click 'View' on Investment Bank case (78% relevant, $2.8M value, 40% achieved)",
    "5. Read their 3-phase approach: Assess → Design → Implement",
    "6. Examine their team structure and timeline (12 months for $2.8M project)",
    "7. Go to Recommendations tab - see AI synthesis showing patterns across 3 cases",
    "8. Go to Knowledge Workflow tab, follow all 9 steps",
    "9. Step 7 auto-populates your proposal based on Investment Bank template",
    "10. Customize for your fintech client's specific requirements",
    "11. Add tags and store - it's now ready for next consultant facing similar challenge",
]
for step in liqueo_process:
    story.append(Paragraph(step, bullet_style))
    story.append(Spacer(1, 0.06*inch))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Result:</b> Proposal completed in 70 minutes using proven 3-phase approach from similar case. Quality based on successful precedent. Ready to submit.",
                      ParagraphStyle('highlight', parent=styles['Normal'], fontSize=11, textColor=ACCENT_GREEN,
                                     fontName='Helvetica-Bold', spaceAfter=10)))

story.append(PageBreak())

# ===== TECHNICAL DETAILS =====
story.append(Paragraph("4. TECHNICAL ARCHITECTURE", section_style))
story.append(Spacer(1, 0.12*inch))

arch_table_data = [
    ["Component", "Description"],
    ["Web UI (Streamlit)", "4-tab user interface: Add, Search, Recommendations, Workflow"],
    ["Semantic Search", "AI embeddings for meaning-based search (OpenAI/Anthropic)"],
    ["Recommendation Engine", "Pattern matching across similar engagements"],
    ["LLM Synthesis", "Claude/GPT analysis for best practice generation"],
    ["Knowledge Base", "JSON filesystem storage of all engagements"],
    ["Workflow Engine", "Tracks 9-step process and auto-populates templates"],
]

arch = Table(arch_table_data, colWidths=[2*inch, 4.5*inch])
arch.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(arch)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Operating Modes", subsection_style))
story.append(Spacer(1, 0.08*inch))

modes = [
    "<b>🔵 Full Mode:</b> OpenAI or Anthropic APIs available. Complete feature set: semantic search + LLM synthesis.",
    "<b>🟢 Hybrid Mode:</b> One API selected (your choice). Can do embeddings OR synthesis.",
    "<b>🟡 Manual Mode:</b> No APIs needed. Uses keyword search. Perfect for demos and testing.",
]
for mode in modes:
    story.append(Paragraph(mode, bullet_style))
    story.append(Spacer(1, 0.08*inch))

story.append(PageBreak())

# ===== QUICK START =====
story.append(Paragraph("5. QUICK START GUIDE (5 MINUTES)", section_style))
story.append(Spacer(1, 0.12*inch))

quick_install = [
    "$ git clone https://github.com/hemalp143/Liqueo.git",
    "$ cd Liqueo",
    "$ python3 -m venv venv",
    "$ source venv/bin/activate",
    "$ pip install -r requirements.txt",
    "$ python load_sample_data.py",
    "$ streamlit run app.py",
]
for cmd in quick_install:
    story.append(Paragraph(f"<i>{cmd}</i>",
                          ParagraphStyle('cmd', parent=styles['Normal'], fontSize=10, fontName='Courier',
                                        leftIndent=0.2*inch, textColor=DARK_TEXT)))
    story.append(Spacer(1, 0.08*inch))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("First Steps After Installation", subsection_style))
story.append(Spacer(1, 0.08*inch))

first = [
    "✓ Sample data pre-loaded (3 banking engagements)",
    "✓ Try Search tab: 'banking cost optimization'",
    "✓ Go to Recommendations to see AI analysis",
    "✓ Follow Knowledge Workflow for complete 9-step experience",
    "✓ Upload your first engagement in Add Document",
]
for item in first:
    story.append(Paragraph(item, bullet_style))
    story.append(Spacer(1, 0.08*inch))

story.append(PageBreak())

# ===== BEST PRACTICES =====
story.append(Paragraph("6. BEST PRACTICES & TIPS", section_style))
story.append(Spacer(1, 0.12*inch))

story.append(Paragraph("For Adding Documents", subsection_style))
story.append(Spacer(1, 0.08*inch))
practices = [
    "✓ Use consistent industry names (Financial Services, not 'Bank', not 'Finance')",
    "✓ Be specific about engagement type (M&A, Cost Optimization, Process Improvement, Digital Transformation)",
    "✓ Include measurable outcomes (% cost reduction, revenue increase, timeline improvement)",
    "✓ Write clear consulting approach (3-5 key phases or steps)",
    "✓ Add meaningful tags that future consultants might search for",
    "✓ Include team size and key roles",
]
for tip in practices:
    story.append(Paragraph(tip, bullet_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("For Effective Searching", subsection_style))
story.append(Spacer(1, 0.08*inch))
search_tips = [
    "✓ Be specific about your challenge (not just 'banking', but 'banking cost optimization')",
    "✓ Include measurable goals if known (e.g., '30% cost reduction')",
    "✓ Describe industry and company type for better matches",
    "✓ Try multiple search queries to see different angles",
    "✓ Use filters to narrow results if too many returned",
    "✓ Review top 3 results - patterns will emerge",
]
for tip in search_tips:
    story.append(Paragraph(tip, bullet_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("For Workflow Success", subsection_style))
story.append(Spacer(1, 0.08*inch))
workflow_tips = [
    "✓ Don't skip Step 5 - really evaluate applicability to your context",
    "✓ In Step 6, select multiple elements from different cases if helpful",
    "✓ Step 7 creates templates - customize heavily for your specific client",
    "✓ Spend time on Step 8 tagging - makes your engagement discoverable for future use",
    "✓ The goal is 70-80% reuse from past engagements, with customization",
]
for tip in workflow_tips:
    story.append(Paragraph(tip, bullet_style))

story.append(PageBreak())

# ===== FAQs =====
story.append(Paragraph("7. TROUBLESHOOTING & FAQs", section_style))
story.append(Spacer(1, 0.12*inch))

faqs_data = [
    ("Q: Do I need to provide API keys?",
     "A: No. Liqueo works without API keys using keyword search. Keys are optional for semantic search + AI synthesis."),

    ("Q: Why am I getting few search results?",
     "A: Knowledge base may be small. Start by uploading several engagements. Liqueo improves with more data."),

    ("Q: Can I upload PowerPoint files?",
     "A: Not yet. PowerPoint support is coming in Phase 4. Use PDF or Word documents for now."),

    ("Q: How long should documents be?",
     "A: Any length works, but 3-10 pages is typical. Focus on consulting approach and measurable outcomes."),

    ("Q: What if Liqueo suggests an irrelevant case?",
     "A: Just skip it. Go to the next result. Similarity scores show relevance (aim for >70%)."),

    ("Q: Can I delete or edit engagements?",
     "A: Currently read-only. Deletion feature comes in Phase 2. Edit by uploading a new version."),

    ("Q: How is data stored?",
     "A: In a .liqueo/ directory as JSON files. No database required. Can be backed up as a folder."),

    ("Q: Can multiple users access the same knowledge base?",
     "A: Phase 1 is single-user. Multi-user support with role-based access comes in Phase 5."),
]

for q, a in faqs_data:
    story.append(Paragraph(q, subsection_style))
    story.append(Paragraph(a, body_style))
    story.append(Spacer(1, 0.1*inch))

# ===== FOOTER =====
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("___________________________________________________________________",
                      ParagraphStyle('line', parent=styles['Normal'], fontSize=8, textColor=colors.lightgrey)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(f"Liqueo Professional User Guide | Generated {datetime.now().strftime('%B %d, %Y')} | www.github.com/hemalp143/Liqueo",
                      ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER,
                                     textColor=colors.grey)))

# Build PDF
doc.build(story)
print(f"✅ PDF Report Created: Liqueo_Professional_Report.pdf")

# ============================================================================
# POWERPOINT CREATION
# ============================================================================

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

PRIMARY = RGBColor(26, 84, 144)
SECONDARY = RGBColor(45, 90, 166)
ACCENT = RGBColor(76, 175, 80)

def add_title_slide(prs, title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = PRIMARY

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(2))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(9), Inches(1.5))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(200, 220, 255)
    p.alignment = PP_ALIGN.CENTER

def add_content_slide(prs, title, content_list):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Title bar
    title_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(1))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = PRIMARY
    title_shape.line.color.rgb = PRIMARY

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Content
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5.5))
    tf = content_box.text_frame
    tf.word_wrap = True

    for i, item in enumerate(content_list):
        if i > 0:
            tf.add_paragraph()
        p = tf.paragraphs[i]
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(12)
        p.level = 0

# Slides
add_title_slide(prs, "LIQUEO", "Knowledge Discovery & Reuse System\nProfessional User Guide")

add_content_slide(prs, "What is Liqueo?", [
    "✓ AI-powered knowledge discovery system",
    "✓ Find similar past engagements in seconds",
    "✓ Analyze patterns and best practices",
    "✓ Auto-populate proposals from templates",
    "✓ 60x faster: 70 hours → 70 minutes",
])

add_content_slide(prs, "Key Benefits", [
    "⚡ 60x Time Savings on Proposal Writing",
    "💡 Preserve Institutional Knowledge",
    "📈 Consistent Methodology Across Projects",
    "👥 Team Learning & Best Practice Sharing",
    "✅ Quality Based on Proven Approaches",
    "💰 Measurable ROI per Engagement",
])

add_content_slide(prs, "The 4 Main Tabs", [
    "📄 Add Document: Upload engagements & metadata",
    "🔍 Search: Find similar past work (AI-powered)",
    "💡 Recommendations: AI analysis of patterns",
    "🎯 Workflow: 9-step guided process",
])

add_content_slide(prs, "Add Document Tab", [
    "✓ Drag & drop or upload PDF/Word/Excel/CSV/Text",
    "✓ Fill engagement metadata (industry, value, duration)",
    "✓ Describe consulting approach & outcomes",
    "✓ Add tags for future discovery",
    "✓ Save to knowledge base",
])

add_content_slide(prs, "Search Tab", [
    "✓ Semantic search for similar engagements",
    "✓ Results ranked by relevance score (0-100%)",
    "✓ Click 'View' to see full details",
    "✓ Read consulting approach & outcomes",
    "✓ Optional filters (industry, type)",
])

add_content_slide(prs, "Recommendations Tab", [
    "✓ AI synthesizes patterns from similar cases",
    "✓ Generates recommended methodology",
    "✓ Lists success factors & typical challenges",
    "✓ Suggests team composition & timeline",
    "✓ Shows source references",
])

add_content_slide(prs, "Workflow Tab - The 9 Steps", [
    "1️⃣  Identify Problem | 2️⃣  Search | 3️⃣  Identify Docs",
    "4️⃣  AI Summarize | 5️⃣  Review | 6️⃣  Select Content",
    "7️⃣  Create Output | 8️⃣  Tag | 9️⃣  Store Knowledge",
    "",
    "Guided process from challenge to stored engagement",
])

add_content_slide(prs, "Real-World Scenario", [
    "Friday 4pm: Fintech RFP arrives (due Monday 9am)",
    "Challenge: 30% cost reduction for core banking",
    "Time available: 70 hours",
    "",
    "With Liqueo: Complete in 70 minutes using proven 3-phase approach from similar case",
])

add_content_slide(prs, "Sample Data Included", [
    "🏦 Investment Bank Back-Office: $2.8M, 12mo, 40% savings",
    "🏦 Retail Bank Technology: $1.5M, 9mo, 35% IT savings",
    "💳 Payment Processor: $0.8M, 6mo, 28% savings",
    "",
    "Ready to use for testing and learning",
])

add_content_slide(prs, "System Architecture", [
    "🎨 Web UI: Streamlit (4 tabs)",
    "🧠 Search: AI embeddings (OpenAI/Anthropic)",
    "🎯 Recommendations: Pattern engine",
    "💬 Synthesis: LLM analysis (Claude/GPT)",
    "💾 Storage: JSON filesystem",
])

add_content_slide(prs, "Operating Modes", [
    "🔵 Full Mode: Both APIs → complete features",
    "🟢 Hybrid Mode: One API → partial features",
    "🟡 Manual Mode: No APIs → keyword search",
    "",
    "Graceful degradation - always works",
])

add_content_slide(prs, "Quick Start (5 Minutes)", [
    "$ git clone https://github.com/hemalp143/Liqueo.git",
    "$ pip install -r requirements.txt",
    "$ python load_sample_data.py",
    "$ streamlit run app.py",
    "→ Opens http://localhost:8501",
])

add_content_slide(prs, "Best Practices", [
    "✓ Use consistent industry names",
    "✓ Write specific consulting approaches",
    "✓ Include measurable outcomes (%)",
    "✓ Add relevant tags",
    "✓ Search with specific challenges",
    "✓ Review top 3 results for patterns",
])

add_content_slide(prs, "Production Roadmap", [
    "Phase 1: ✅ Foundation (Complete)",
    "Phase 2: Database Persistence (4 weeks)",
    "Phase 3: Vector Database for Scale (4 weeks)",
    "Phases 4-8: Document processing, multi-user, integrations (16 weeks)",
    "",
    "Total: 8 months to full enterprise deployment",
])

add_content_slide(prs, "Support & Resources", [
    "📧 Email: hemalp1434@gmail.com",
    "🔗 GitHub: github.com/hemalp143/Liqueo",
    "📚 Documentation: Included in repository",
    "🎯 Branch: claude/knowledge-discovery-reuse-e3nr1n",
    "",
    "Questions? Check FAQs in full documentation",
])

prs.save("Liqueo_Professional_Presentation.pptx")
print(f"✅ PowerPoint Presentation Created: Liqueo_Professional_Presentation.pptx (16 slides)")

print("\n" + "="*70)
print("✨ PROFESSIONAL DOCUMENTATION WITH EXPLANATIONS COMPLETE")
print("="*70)
print("\n📄 PDF Report: Liqueo_Professional_Report.pdf")
print("   → 7 detailed sections with comprehensive explanations")
print("   → UI guide with step-by-step instructions")
print("   → Real-world scenario walkthrough")
print("   → Technical architecture and operating modes")
print("   → Complete FAQs and best practices")
print("\n🎨 PowerPoint: Liqueo_Professional_Presentation.pptx (16 slides)")
print("   → System overview and key benefits")
print("   → Tab-by-tab feature walkthrough")
print("   → 9-step workflow explanation")
print("   → Real-world scenario demo")
print("   → Quick start guide")
print("   → Production roadmap")
print("\n✅ Both files are ready for supervisor submission!\n")
