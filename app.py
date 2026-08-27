"""Streamlit web UI for Liqueo - Knowledge Discovery & Reuse System."""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
import requests
from io import BytesIO

from liqueo.core import Document, KnowledgeBase, generate_doc_id
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer


# File parsing functions
def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file):
    """Extract text from Word document."""
    try:
        from docx import Document as DocxDocument
        doc = DocxDocument(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"Error reading Word document: {str(e)}"

def extract_text_from_xlsx(file):
    """Extract text from Excel file."""
    try:
        df = pd.read_excel(file)
        text = df.to_string()
        return text[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"

def extract_text_from_txt(file):
    """Extract text from text file."""
    try:
        text = file.read().decode('utf-8')
        return text[:5000]
    except Exception as e:
        return f"Error reading text file: {str(e)}"

def extract_text_from_csv(file):
    """Extract text from CSV file."""
    try:
        df = pd.read_csv(file)
        text = df.to_string()
        return text[:5000]
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"

def parse_uploaded_file(file):
    """Parse uploaded file and extract content."""
    filename = file.name.lower()

    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        return extract_text_from_docx(file)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return extract_text_from_xlsx(file)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(file)
    elif filename.endswith('.csv'):
        return extract_text_from_csv(file)
    else:
        return f"Unsupported file type: {filename}"

def download_file_from_url(url):
    """Download and parse file from URL (OneDrive, SharePoint, etc.)."""
    try:
        # For OneDrive links, modify URL to get direct download
        if 'onedrive.live.com' in url or 'sharepoint.com' in url:
            # Remove ?download=1 and add it
            url = url.split('?')[0]
            if '?download=1' not in url:
                url = url + '?download=1'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Get filename from URL or use generic name
        filename = url.split('/')[-1].split('?')[0] or "downloaded_file"

        # Create a file-like object
        file_content = BytesIO(response.content)
        file_content.name = filename

        return file_content, filename
    except Exception as e:
        return None, f"Error downloading file: {str(e)}"


# Configure page
st.set_page_config(
    page_title="Liqueo - Knowledge Discovery",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase()
    st.session_state.embeddings = EmbeddingsManager(st.session_state.kb)
    st.session_state.recommender = RecommendationEngine(st.session_state.embeddings)
    st.session_state.synthesizer = KnowledgeSynthesizer(
        st.session_state.kb, st.session_state.recommender
    )


def render_header():
    """Render page header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧠 Liqueo")
        st.markdown("**Knowledge Discovery & Reuse for Financial Consultants**")
    with col2:
        st.info("v1.0.0")


def render_home():
    """Render home/dashboard page."""
    render_header()

    st.markdown("---")

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    docs = st.session_state.kb.list_documents()
    industries = set(d.industry for d in docs if d.industry)
    types = set(d.transaction_type for d in docs if d.transaction_type)
    total_value = sum(d.engagement_value or 0 for d in docs)

    with col1:
        st.metric("Total Documents", len(docs))
    with col2:
        st.metric("Industries", len(industries))
    with col3:
        st.metric("Transaction Types", len(types))
    with col4:
        st.metric("Total Value ($M)", f"${total_value:.1f}")

    st.markdown("---")

    # Key features
    st.subheader("Key Features")

    feature_cols = st.columns(3)

    with feature_cols[0]:
        st.info("""
        ### 📚 Knowledge Base
        Store and organize consulting engagements with rich metadata
        """)

    with feature_cols[1]:
        st.success("""
        ### 🔍 Semantic Search
        Find similar cases using embeddings or keyword matching
        """)

    with feature_cols[2]:
        st.warning("""
        ### 💡 AI Synthesis
        Generate insights from similar engagements
        """)

    st.markdown("---")

    # Sample data
    if len(docs) == 0:
        st.info("👉 Get started by adding documents from the sidebar!")
    else:
        st.subheader("Recent Engagements")

        df_data = []
        for doc in sorted(docs, key=lambda d: d.created_at, reverse=True)[:5]:
            df_data.append({
                "Title": doc.title[:50],
                "Industry": doc.industry,
                "Type": doc.transaction_type,
                "Value ($M)": doc.engagement_value,
                "Duration (months)": doc.duration_months
            })

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


def render_add_document():
    """Render add document page."""
    render_header()
    st.subheader("Add New Engagement")

    st.markdown("---")

    # Tab selection: Manual entry or file upload
    tab1, tab2 = st.tabs(["📝 Manual Entry", "📤 Upload File"])

    with tab1:
        with st.form("add_doc_form"):
            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Engagement Title *", placeholder="e.g., SaaS Acquisition")
                industry = st.text_input("Industry *", placeholder="e.g., Technology")
                transaction_type = st.text_input("Transaction Type", placeholder="e.g., M&A, Restructuring")

            with col2:
                value = st.number_input("Engagement Value ($M)", min_value=0.0, step=0.1)
                duration = st.number_input("Duration (months)", min_value=1, max_value=60)
                client = st.text_input("Client Name", placeholder="e.g., ABC Corporation")

            content = st.text_area(
                "Engagement Details *",
                height=150,
                placeholder="Describe the engagement, approach, and key activities..."
            )

            outcomes = st.text_area(
                "Key Outcomes",
                height=100,
                placeholder="Summary of outcomes and impact..."
            )

            approach = st.text_area(
                "Consulting Approach",
                height=80,
                placeholder="Methodology and key approach..."
            )

            if st.form_submit_button("Add Engagement", use_container_width=True):
                if not title or not industry or not content:
                    st.error("Please fill in Title, Industry, and Details (marked with *)")
                else:
                    doc_id = generate_doc_id(title, datetime.now())
                    doc = Document(
                        id=doc_id,
                        title=title,
                        content=content,
                        doc_type="engagement",
                        industry=industry,
                        transaction_type=transaction_type or None,
                        engagement_value=value if value > 0 else None,
                        duration_months=duration,
                        client_name=client or None,
                        key_outcomes=outcomes or None,
                        consulting_approach=approach or None
                    )

                    st.session_state.kb.add_document(doc)

                    # Try to generate embeddings
                    try:
                        st.session_state.embeddings.embed_document(doc)
                        st.success(f"✓ Document added: **{title}**\n\nEmbeddings generated successfully")
                    except Exception as e:
                        st.warning(f"✓ Document added: **{title}**\n\n⚠️ Embeddings not available (using keyword search instead)")

    with tab2:
        st.markdown("### Step 1️⃣: Enter Company Information")
        st.markdown("Supported file formats: PDF, Word (.docx), Excel (.xlsx), CSV, Text")

        # Step 1: Get company/engagement details
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name *", placeholder="e.g., Acme Corp, TechStart Inc")
            industry = st.text_input("Industry *", placeholder="e.g., Technology, Healthcare, Retail")
            transaction_type = st.text_input("Transaction Type", placeholder="e.g., M&A, Restructuring, Digital Transformation")

        with col2:
            engagement_value = st.number_input("Engagement Value ($M)", min_value=0.0, step=0.1)
            duration = st.number_input("Duration (months)", min_value=1, max_value=60)
            client_contact = st.text_input("Contact Person", placeholder="e.g., John Smith (Optional)")

        # Step 2: Upload files
        st.markdown("---")
        st.markdown("### Step 2️⃣: Upload Supporting Files")

        # Option A: Local file upload
        st.markdown("**Option A: Local Files**")
        uploaded_files = st.file_uploader(
            "Upload one or more files",
            type=["pdf", "docx", "doc", "xlsx", "xls", "csv", "txt"],
            accept_multiple_files=True
        )

        # Option B: URL download
        st.markdown("**Option B: Download from URL (OneDrive, SharePoint, etc.)**")
        file_url = st.text_input(
            "Paste direct file URL",
            placeholder="e.g., https://onedrive.live.com/... or https://sharepoint.com/...",
            help="Enter a direct download link to a file in OneDrive, SharePoint, or other cloud storage"
        )

        downloaded_files = []
        if file_url:
            if st.button("📥 Download File from URL"):
                with st.spinner("Downloading file..."):
                    file_content, filename = download_file_from_url(file_url)
                    if file_content is None:
                        st.error(f"❌ {filename}")
                    else:
                        st.success(f"✅ Downloaded: {filename}")
                        # Store in session state for processing
                        if "downloaded_files" not in st.session_state:
                            st.session_state.downloaded_files = []
                        st.session_state.downloaded_files.append((file_content, filename))

        # Retrieve downloaded files from session state
        if "downloaded_files" in st.session_state and st.session_state.downloaded_files:
            downloaded_files = st.session_state.downloaded_files

        # Combine local and downloaded files
        all_files = []
        file_list = []

        if uploaded_files:
            st.markdown(f"✅ **{len(uploaded_files)} local file(s) selected**")
            all_files.extend([(f, f.name) for f in uploaded_files])
            file_list.extend([f.name for f in uploaded_files])

        if downloaded_files:
            st.markdown(f"✅ **{len(downloaded_files)} file(s) downloaded from URL**")
            all_files.extend(downloaded_files)
            file_list.extend([fname for _, fname in downloaded_files])

        if all_files:
            st.markdown(f"✅ **{len(all_files)} total file(s) ready for processing**")

            # Extract and combine content from all files
            all_content = []

            for file, filename in all_files:
                st.info(f"📄 {filename}")
                extracted = parse_uploaded_file(file)
                all_content.append(f"\n--- From {filename} ---\n{extracted}")

            combined_content = "\n".join(all_content)

            # Step 3: Review and submit
            st.markdown("---")
            st.markdown("### Step 3️⃣: Review & Submit")

            # Create form for final submission
            with st.form("upload_with_files_form"):
                st.markdown("**Engagement Summary:**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Company", company_name or "Not set")
                with col2:
                    st.metric("Industry", industry or "Not set")
                with col3:
                    st.metric("Files", len(uploaded_files))

                st.markdown("**Files uploaded:**")
                for fname in file_list:
                    st.caption(f"✓ {fname}")

                # Edit extracted content if needed
                content = st.text_area(
                    "Combined Content (auto-extracted from files - edit if needed)",
                    value=combined_content[:3000] if combined_content else "No content extracted",
                    height=200
                )

                outcomes = st.text_area(
                    "Key Outcomes/Notes",
                    height=80,
                    placeholder="Summary of outcomes or important notes..."
                )

                if st.form_submit_button("✅ Save Engagement with Files", use_container_width=True):
                    if not company_name or not industry:
                        st.error("Please enter Company Name and Industry (marked with *)")
                    else:
                        # Create title from company name and type
                        title = f"{company_name} - {transaction_type if transaction_type else 'Engagement'}"

                        doc_id = generate_doc_id(title, datetime.now())
                        doc = Document(
                            id=doc_id,
                            title=title,
                            content=content,
                            doc_type="engagement",
                            industry=industry,
                            transaction_type=transaction_type or None,
                            engagement_value=engagement_value if engagement_value > 0 else None,
                            duration_months=duration,
                            client_name=client_contact or None,
                            key_outcomes=outcomes or None,
                            metadata={
                                "uploaded_files": file_list,
                                "file_count": len(all_files),
                                "local_files": len(uploaded_files) if uploaded_files else 0,
                                "url_files": len(downloaded_files) if downloaded_files else 0,
                                "file_sources": {
                                    "local": [f.name for f in uploaded_files] if uploaded_files else [],
                                    "urls": [fname for _, fname in downloaded_files] if downloaded_files else []
                                }
                            }
                        )

                        st.session_state.kb.add_document(doc)

                        # Clear downloaded files from session state after saving
                        if "downloaded_files" in st.session_state:
                            st.session_state.downloaded_files = []

                        try:
                            st.session_state.embeddings.embed_document(doc)
                            st.success(f"✅ **{title}** saved successfully!\n\n📁 Files: {', '.join(file_list)}")
                        except Exception as e:
                            st.warning(f"✅ Document saved: **{title}**\n\n⚠️ Using keyword search mode")
        else:
            st.info("📤 Upload local files or paste a URL in Step 2️⃣ to continue")


def render_search():
    """Render search page."""
    render_header()
    st.subheader("Search Knowledge Base")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        query = st.text_input("Search Query", placeholder="e.g., cloud infrastructure optimization")
    with col2:
        top_k = st.slider("Top Results", 1, 10, 5)
    with col3:
        industry_filter = st.text_input("Filter by Industry", placeholder="Leave blank for no filter")

    if st.button("Search", use_container_width=True):
        if not query:
            st.warning("Please enter a search query")
        else:
            with st.spinner("Searching..."):
                filters = {}
                if industry_filter:
                    filters["industry"] = industry_filter

                results = st.session_state.embeddings.semantic_search(
                    query, top_k=top_k, filters=filters
                )

                if not results:
                    st.info("No results found")
                else:
                    st.success(f"Found {len(results)} matching engagement(s)")

                    for i, result in enumerate(results, 1):
                        doc = result.document
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**{i}. {doc.title}**")
                                st.markdown(f"*{doc.industry} • {doc.transaction_type}*")

                            with col2:
                                st.metric("Relevance", f"{result.similarity_score:.0%}")

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.caption(f"Value: ${doc.engagement_value}M" if doc.engagement_value else "Value: N/A")
                            with col2:
                                st.caption(f"Duration: {doc.duration_months}m" if doc.duration_months else "Duration: N/A")
                            with col3:
                                st.caption(f"Client: {doc.client_name}" if doc.client_name else "Client: N/A")

                            if doc.key_outcomes:
                                st.markdown(f"**Outcomes:** {doc.key_outcomes}")


def render_recommendations():
    """Render recommendations page."""
    render_header()
    st.subheader("Get Recommendations")

    st.markdown("---")

    engagement = st.text_area(
        "Describe the Current Engagement",
        height=150,
        placeholder="Describe the client situation, challenges, and desired outcomes...",
        value="We need to optimize our cloud infrastructure and reduce operational costs"
    )

    top_k = st.slider("Number of Recommendations", 1, 10, 3)

    if st.button("Get Recommendations", use_container_width=True):
        if not engagement:
            st.warning("Please describe the engagement")
        else:
            with st.spinner("Analyzing similar engagements..."):
                recommendations = st.session_state.recommender.recommend_similar_engagements(
                    engagement, top_k=top_k
                )

                if not recommendations:
                    st.info("No recommendations found")
                else:
                    st.success(f"Found {len(recommendations)} similar engagement(s)")

                    for i, rec in enumerate(recommendations, 1):
                        doc = rec.reference_document
                        with st.container(border=True):
                            st.markdown(f"**{i}. {doc.title}**")
                            st.markdown(f"*Relevance: {rec.relevance_score:.0%} • {rec.reasoning}*")

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if rec.suggested_approach:
                                    st.info(f"**Approach:** {rec.suggested_approach}")
                            with col2:
                                if rec.potential_challenges:
                                    st.warning(f"**Challenges:** {rec.potential_challenges[:100]}...")
                            with col3:
                                if rec.estimated_effort:
                                    st.success(f"**Effort:** {rec.estimated_effort}")


def render_synthesize():
    """Render synthesis page."""
    render_header()
    st.subheader("Synthesize Insights")

    st.markdown("---")

    engagement = st.text_area(
        "Engagement Description",
        height=150,
        placeholder="Describe the engagement and what insights you need...",
        value="We need to optimize our technology infrastructure and reduce operational costs"
    )

    top_k = st.slider("Consider Top Similar Cases", 1, 10, 3)

    if st.button("Generate Insights", use_container_width=True):
        if not engagement:
            st.warning("Please describe the engagement")
        else:
            with st.spinner("Generating synthesis and insights..."):
                synthesis = st.session_state.synthesizer.synthesize_recommendations(
                    engagement, top_k=top_k
                )

                st.markdown("---")
                st.markdown(synthesis)


def render_analysis():
    """Render industry analysis page."""
    render_header()
    st.subheader("Industry Analysis")

    st.markdown("---")

    docs = st.session_state.kb.list_documents()
    industries = sorted(set(d.industry for d in docs if d.industry))

    if not industries:
        st.info("Add documents first to analyze industries")
    else:
        industry = st.selectbox("Select Industry", industries)

        if st.button("Analyze Trends", use_container_width=True):
            with st.spinner(f"Analyzing {industry} industry trends..."):
                analysis = st.session_state.synthesizer.analyze_industry_trends(industry)
                st.markdown(analysis)


def render_documents():
    """Render documents management page."""
    render_header()
    st.subheader("Knowledge Base Documents")

    st.markdown("---")

    docs = st.session_state.kb.list_documents()

    if not docs:
        st.info("No documents in knowledge base. Add documents to get started!")
    else:
        st.info(f"Total: {len(docs)} document(s)")

        # Create dataframe
        data = []
        for doc in sorted(docs, key=lambda d: d.created_at, reverse=True):
            data.append({
                "ID": doc.id[:12],
                "Title": doc.title,
                "Industry": doc.industry or "-",
                "Type": doc.transaction_type or "-",
                "Value": f"${doc.engagement_value}M" if doc.engagement_value else "-",
                "Duration": f"{doc.duration_months}m" if doc.duration_months else "-",
                "Created": doc.created_at.strftime("%Y-%m-%d")
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export option
        st.markdown("---")
        if st.button("Export Knowledge Base (JSON)", use_container_width=True):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "document_count": len(docs),
                "documents": [doc.to_dict() for doc in docs]
            }

            st.json(export_data)

            # Download button
            st.download_button(
                "Download JSON",
                json.dumps(export_data, indent=2, default=str),
                "liqueo_export.json"
            )


def main():
    """Main app entry point."""
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## Navigation")
        selected = option_menu(
            menu_title=None,
            options=["Home", "Search", "Recommendations", "Synthesize", "Analysis", "Documents", "Add Engagement"],
            icons=["house", "search", "lightbulb", "sparkles", "chart-line", "folder", "plus"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#FF6B35"},
            }
        )

        st.markdown("---")

        # Info section
        st.markdown("### About Liqueo")
        st.markdown("""
        **Knowledge Discovery & Reuse System** for financial consultants.

        - 🧠 Semantic search with embeddings
        - 💡 AI-powered recommendations
        - 📊 Industry trend analysis
        - 📈 Strategic insights synthesis
        """)

        # Status
        docs_count = len(st.session_state.kb.list_documents())
        st.markdown(f"**Status:** {docs_count} documents loaded")

    # Route to selected page
    if selected == "Home":
        render_home()
    elif selected == "Add Engagement":
        render_add_document()
    elif selected == "Search":
        render_search()
    elif selected == "Recommendations":
        render_recommendations()
    elif selected == "Synthesize":
        render_synthesize()
    elif selected == "Analysis":
        render_analysis()
    elif selected == "Documents":
        render_documents()


if __name__ == "__main__":
    main()
