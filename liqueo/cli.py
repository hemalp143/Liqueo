"""Command-line interface for Liqueo."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from liqueo.core import Document, KnowledgeBase, generate_doc_id
from liqueo.embeddings import EmbeddingsManager
from liqueo.recommender import RecommendationEngine
from liqueo.synthesizer import KnowledgeSynthesizer

console = Console()


@click.group()
def main():
    """Liqueo: Knowledge Discovery & Reuse for Financial Consultants."""
    pass


@main.command()
@click.option("--title", prompt="Document title", help="Title of the engagement/document")
@click.option("--type", "doc_type", default="engagement", help="Type of document")
@click.option("--industry", default=None, help="Industry")
@click.option("--transaction-type", default=None, help="Transaction type (e.g., M&A)")
@click.option("--value", type=float, default=None, help="Engagement value in millions")
@click.option("--duration", type=int, default=None, help="Duration in months")
@click.option("--client", default=None, help="Client name")
@click.option("--file", type=click.File("r"), default=None, help="Content from file")
def add(
    title: str,
    doc_type: str,
    industry: Optional[str],
    transaction_type: Optional[str],
    value: Optional[float],
    duration: Optional[int],
    client: Optional[str],
    file: Optional[object],
):
    """Add a new document to the knowledge base."""
    kb = KnowledgeBase()

    if file:
        content = file.read()
    else:
        click.echo("Paste document content (press Ctrl+D when done):")
        content = click.get_text_stream("stdin").read()

    doc_id = generate_doc_id(title, datetime.now())
    document = Document(
        id=doc_id,
        title=title,
        content=content,
        doc_type=doc_type,
        industry=industry,
        transaction_type=transaction_type,
        engagement_value=value,
        duration_months=duration,
        client_name=client,
    )

    kb.add_document(document)
    console.print(f"✓ Document added: {doc_id}", style="green")

    # Try to generate embeddings
    try:
        embeddings = EmbeddingsManager(kb)
        embeddings.embed_document(document)
        console.print("✓ Embeddings generated", style="green")
    except Exception as e:
        console.print(f"⚠ Could not generate embeddings: {e}", style="yellow")


@main.command()
@click.option("--query", prompt="Search query", help="What to search for")
@click.option("--top-k", default=5, help="Number of results to return")
@click.option("--industry", default=None, help="Filter by industry")
@click.option("--type", "transaction_type", default=None, help="Filter by transaction type")
def search(query: str, top_k: int, industry: Optional[str], transaction_type: Optional[str]):
    """Search the knowledge base."""
    kb = KnowledgeBase()
    embeddings = EmbeddingsManager(kb)

    filters = {}
    if industry:
        filters["industry"] = industry
    if transaction_type:
        filters["transaction_type"] = transaction_type

    results = embeddings.semantic_search(query, top_k=top_k, filters=filters)

    if not results:
        console.print("No results found", style="yellow")
        return

    table = Table(title="Search Results")
    table.add_column("Title", style="cyan")
    table.add_column("Industry", style="magenta")
    table.add_column("Type", style="yellow")
    table.add_column("Relevance", style="green")

    for result in results:
        doc = result.document
        table.add_row(
            doc.title[:40],
            doc.industry or "-",
            doc.transaction_type or "-",
            f"{result.similarity_score:.0%}",
        )

    console.print(table)


@main.command()
@click.option("--query", prompt="Engagement description", help="Current engagement details")
@click.option("--top-k", default=3, help="Number of recommendations")
def recommend(query: str, top_k: int):
    """Get recommendations for an engagement."""
    kb = KnowledgeBase()
    embeddings = EmbeddingsManager(kb)
    recommender = RecommendationEngine(embeddings)

    recommendations = recommender.recommend_similar_engagements(query, top_k=top_k)

    if not recommendations:
        console.print("No recommendations found", style="yellow")
        return

    console.print(Panel("Recommended Similar Engagements", style="bold blue"))

    for i, rec in enumerate(recommendations, 1):
        doc = rec.reference_document
        console.print(
            f"\n[bold]{i}. {doc.title}[/bold]\n"
            f"Industry: {doc.industry}\n"
            f"Type: {doc.transaction_type}\n"
            f"Relevance: {rec.relevance_score:.0%}\n"
            f"Reasoning: {rec.reasoning}"
        )
        if rec.suggested_approach:
            console.print(f"Approach: {rec.suggested_approach}")
        if rec.potential_challenges:
            console.print(f"Challenges: {rec.potential_challenges}")
        if rec.estimated_effort:
            console.print(f"Effort: {rec.estimated_effort}")


@main.command()
@click.option("--engagement", prompt="Engagement description", help="Engagement details")
@click.option("--top-k", default=3, help="Number of recommendations to analyze")
def synthesize(engagement: str, top_k: int):
    """Synthesize insights and recommendations."""
    kb = KnowledgeBase()
    embeddings = EmbeddingsManager(kb)
    recommender = RecommendationEngine(embeddings)
    synthesizer = KnowledgeSynthesizer(kb, recommender)

    console.print(Panel("Synthesizing Insights...", style="bold blue"))
    insights = synthesizer.synthesize_recommendations(engagement, top_k=top_k)
    console.print(insights)


@main.command()
@click.option("--industry", default=None, help="Filter by industry")
def analyze(industry: Optional[str]):
    """Analyze industry trends."""
    kb = KnowledgeBase()
    embeddings = EmbeddingsManager(kb)
    recommender = RecommendationEngine(embeddings)
    synthesizer = KnowledgeSynthesizer(kb, recommender)

    if not industry:
        industries = set(doc.industry for doc in kb.list_documents() if doc.industry)
        if not industries:
            console.print("No industries in knowledge base", style="yellow")
            return
        industry = click.prompt("Select industry", type=click.Choice(list(industries)))

    console.print(Panel(f"Industry Analysis: {industry}", style="bold blue"))
    analysis = synthesizer.analyze_industry_trends(industry)
    console.print(analysis)


@main.command()
def list():
    """List all documents in the knowledge base."""
    kb = KnowledgeBase()
    documents = kb.list_documents()

    if not documents:
        console.print("No documents in knowledge base", style="yellow")
        return

    table = Table(title="Knowledge Base Documents")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="cyan")
    table.add_column("Industry", style="magenta")
    table.add_column("Type", style="yellow")
    table.add_column("Date", style="green")

    for doc in sorted(documents, key=lambda d: d.created_at, reverse=True):
        table.add_row(
            doc.id[:8],
            doc.title[:40],
            doc.industry or "-",
            doc.transaction_type or "-",
            doc.created_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


@main.command()
@click.argument("doc_id")
def view(doc_id: str):
    """View a document details."""
    kb = KnowledgeBase()

    matching = [doc for doc in kb.list_documents() if doc.id.startswith(doc_id)]
    if not matching:
        console.print(f"Document not found: {doc_id}", style="red")
        return

    doc = matching[0]
    console.print(Panel(doc.title, style="bold blue"))
    console.print(f"ID: {doc.id}")
    console.print(f"Type: {doc.doc_type}")
    console.print(f"Industry: {doc.industry}")
    console.print(f"Transaction Type: {doc.transaction_type}")
    if doc.engagement_value:
        console.print(f"Value: ${doc.engagement_value}M")
    if doc.duration_months:
        console.print(f"Duration: {doc.duration_months} months")
    if doc.client_name:
        console.print(f"Client: {doc.client_name}")
    console.print(f"Created: {doc.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    if doc.content:
        console.print("\n[bold]Content:[/bold]")
        console.print(doc.content[:1000])
        if len(doc.content) > 1000:
            console.print("...\n[dim](content truncated)[/dim]")

    if doc.key_outcomes:
        console.print(f"\n[bold]Key Outcomes:[/bold]\n{doc.key_outcomes}")


@main.command()
def export():
    """Export knowledge base to JSON."""
    kb = KnowledgeBase()
    documents = kb.list_documents()

    export_data = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "document_count": len(documents),
        "documents": [doc.to_dict() for doc in documents],
    }

    output_file = Path("liqueo_export.json")
    with open(output_file, "w") as f:
        json.dump(export_data, f, indent=2)

    console.print(f"✓ Exported {len(documents)} documents to {output_file}", style="green")


if __name__ == "__main__":
    main()
