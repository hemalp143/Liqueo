"""
Knowledge Discovery & Reuse Workflow Engine.

Implements the 9-step workflow for discovering and reusing knowledge:
1. User identifies a task or problem
2. User searches for relevant knowledge
3. System identifies related documents
4. AI assists by summarizing and recommending
5. User reviews and evaluates results
6. User selects content to reuse/adapt
7. User creates new output using discovered knowledge
8. New output is classified, tagged and stored
9. Future users can discover and reuse that knowledge
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from liqueo.core import Document


@dataclass
class WorkflowStep:
    """Represents a step in the knowledge workflow."""
    step_number: int
    title: str
    description: str
    status: str = "pending"  # pending, in_progress, completed
    timestamp: Optional[datetime] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LessonLearned:
    """Represents a lesson learned from an engagement."""
    id: str
    document_id: str
    lesson: str
    category: str  # e.g., "success", "challenge", "process", "technique"
    applicability: str  # e.g., "high", "medium", "low"
    related_industries: List[str] = field(default_factory=list)
    related_types: List[str] = field(default_factory=list)


@dataclass
class EngagementTemplate:
    """Template extracted from similar engagements for reuse."""
    id: str
    title: str
    description: str
    approach: str
    success_factors: List[str]
    challenges: List[str]
    timeline: str
    estimated_resources: str
    source_documents: List[str]  # IDs of documents this was extracted from
    tags: List[str] = field(default_factory=list)
    industry: Optional[str] = None
    transaction_type: Optional[str] = None


@dataclass
class WorkflowSession:
    """Tracks a complete knowledge workflow session."""
    id: str
    problem_statement: str
    created_at: datetime
    updated_at: datetime
    steps: List[WorkflowStep] = field(default_factory=list)
    selected_documents: List[str] = field(default_factory=list)  # Document IDs
    extracted_lessons: List[LessonLearned] = field(default_factory=list)
    selected_template: Optional[EngagementTemplate] = None
    created_output: Optional[Document] = None
    tags: List[str] = field(default_factory=list)
    notes: str = ""

    def get_current_step(self) -> Optional[WorkflowStep]:
        """Get the current active step."""
        for step in self.steps:
            if step.status in ["pending", "in_progress"]:
                return step
        return None

    def get_progress(self) -> dict:
        """Get workflow progress statistics."""
        total = len(self.steps)
        completed = sum(1 for step in self.steps if step.status == "completed")
        in_progress = sum(1 for step in self.steps if step.status == "in_progress")
        pending = sum(1 for step in self.steps if step.status == "pending")

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "percentage": (completed / total * 100) if total > 0 else 0
        }


class WorkflowEngine:
    """Engine to manage knowledge discovery and reuse workflows."""

    def __init__(self):
        self.sessions: Dict[str, WorkflowSession] = {}
        self.templates: Dict[str, EngagementTemplate] = {}
        self.lessons_learned: Dict[str, List[LessonLearned]] = {}

    def create_workflow(self, problem_statement: str) -> WorkflowSession:
        """Create a new workflow session."""
        from liqueo.core import generate_doc_id

        workflow_id = generate_doc_id(f"workflow_{problem_statement}", datetime.now())

        steps = [
            WorkflowStep(1, "Identify Problem", "Define the task or problem you need to solve"),
            WorkflowStep(2, "Search Knowledge", "Search for relevant past engagements"),
            WorkflowStep(3, "Identify Related Docs", "System identifies related documents and templates"),
            WorkflowStep(4, "AI Summarize & Recommend", "AI provides summaries and recommendations"),
            WorkflowStep(5, "Review & Evaluate", "Review and evaluate the recommended content"),
            WorkflowStep(6, "Select Content", "Select content to reuse or adapt"),
            WorkflowStep(7, "Create Output", "Create new output using discovered knowledge"),
            WorkflowStep(8, "Tag & Classify", "Classify and tag the new output"),
            WorkflowStep(9, "Store Knowledge", "Store for future discovery and reuse"),
        ]

        session = WorkflowSession(
            id=workflow_id,
            problem_statement=problem_statement,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            steps=steps
        )

        self.sessions[workflow_id] = session
        return session

    def update_step(self, workflow_id: str, step_number: int, status: str, data: Dict[str, Any] = None) -> WorkflowStep:
        """Update a workflow step."""
        if workflow_id not in self.sessions:
            raise ValueError(f"Workflow {workflow_id} not found")

        session = self.sessions[workflow_id]
        for step in session.steps:
            if step.step_number == step_number:
                step.status = status
                step.timestamp = datetime.now()
                if data:
                    step.data = data
                session.updated_at = datetime.now()
                return step

        raise ValueError(f"Step {step_number} not found in workflow")

    def extract_lessons(self, document: Document) -> List[LessonLearned]:
        """Extract lessons learned from an engagement document."""
        from liqueo.core import generate_doc_id

        lessons = []

        # Extract from key outcomes
        if document.key_outcomes:
            lesson = LessonLearned(
                id=generate_doc_id(f"lesson_{document.id}_outcomes", datetime.now()),
                document_id=document.id,
                lesson=f"Success Factor: {document.key_outcomes}",
                category="success",
                applicability="high",
                related_industries=[document.industry] if document.industry else [],
                related_types=[document.transaction_type] if document.transaction_type else []
            )
            lessons.append(lesson)

        # Extract from consulting approach
        if document.consulting_approach:
            lesson = LessonLearned(
                id=generate_doc_id(f"lesson_{document.id}_approach", datetime.now()),
                document_id=document.id,
                lesson=f"Process: {document.consulting_approach}",
                category="process",
                applicability="high",
                related_industries=[document.industry] if document.industry else [],
                related_types=[document.transaction_type] if document.transaction_type else []
            )
            lessons.append(lesson)

        self.lessons_learned[document.id] = lessons
        return lessons

    def create_template(self, title: str, documents: List[Document]) -> EngagementTemplate:
        """Create a reusable template from similar documents."""
        from liqueo.core import generate_doc_id

        template_id = generate_doc_id(f"template_{title}", datetime.now())

        # Extract common approach
        approaches = [d.consulting_approach for d in documents if d.consulting_approach]
        common_approach = approaches[0] if approaches else "Standard consulting approach"

        # Extract success factors
        success_factors = []
        for doc in documents:
            if doc.key_outcomes:
                success_factors.append(doc.key_outcomes)

        # Infer challenges (opposite of outcomes)
        challenges = ["Risk management", "Stakeholder alignment", "Timeline adherence"]

        template = EngagementTemplate(
            id=template_id,
            title=title,
            description=f"Template based on {len(documents)} similar engagements",
            approach=common_approach,
            success_factors=success_factors,
            challenges=challenges,
            timeline="3-6 months",
            estimated_resources="Senior consultant + 2 analysts",
            source_documents=[d.id for d in documents],
            tags=["reusable", "template"],
            industry=documents[0].industry if documents else None,
            transaction_type=documents[0].transaction_type if documents else None
        )

        self.templates[template_id] = template
        return template

    def get_workflow_insights(self, workflow_id: str) -> Dict[str, Any]:
        """Get insights about a workflow."""
        if workflow_id not in self.sessions:
            raise ValueError(f"Workflow {workflow_id} not found")

        session = self.sessions[workflow_id]
        progress = session.get_progress()

        return {
            "workflow_id": workflow_id,
            "problem": session.problem_statement,
            "progress": progress,
            "documents_selected": len(session.selected_documents),
            "lessons_extracted": len(session.extracted_lessons),
            "template_available": session.selected_template is not None,
            "output_created": session.created_output is not None,
            "current_step": session.get_current_step().title if session.get_current_step() else "Completed",
            "tags": session.tags,
            "notes": session.notes
        }
