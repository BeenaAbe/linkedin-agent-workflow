"""
LinkedIn Content Engine - Enhanced 6-Agent Workflow
Complete production pipeline: Admin → Research → Strategist → Writer → Editor → Formatter
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.admin_agent import AdminAgent
from agents.research_agent import ResearchAgent
from agents.strategist_agent import StrategistAgent
from agents.writer_agent import WriterAgent
from agents.editor_agent import EditorAgent
from agents.formatter_agent import FormatterAgent


class WorkflowState(TypedDict):
    """State shared across all agents"""
    # Input
    page_id: str
    topic: str
    goal: str
    context: str

    # Admin metadata
    workflow_id: str
    start_time: str
    time_allocation: int
    completed_at: str
    duration_minutes: float

    # Research phase
    research_brief: str
    search_results: str

    # Strategy phase
    content_strategy: dict
    outline: list[str]

    # Writing phase
    hooks: list[str]
    post_body: str
    cta: str

    # Editor phase
    quality_score: int
    editor_feedback: str
    editor_decision: str
    revision_count: int

    # Formatting phase
    hashtags: list[str]
    visual_suggestion: str
    visual_format: str
    visual_specs: dict
    character_count: int
    word_count: int
    estimated_read_time: str
    first_comment: str

    # Final checklist
    checklist: dict

    # Status tracking
    status: str  # validated, researching, strategizing, drafting, editing, formatting, ready, error


class LinkedInWorkflow:
    """
    Complete 6-agent workflow: Admin → Research → Strategist → Writer → Editor → Formatter
    Includes quality checks and revision loops
    """

    def __init__(self):
        # Initialize all 6 agents
        self.admin_agent = AdminAgent()
        self.research_agent = ResearchAgent()
        self.strategist_agent = StrategistAgent()
        self.writer_agent = WriterAgent()
        self.editor_agent = EditorAgent()
        self.formatter_agent = FormatterAgent()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build complete 6-agent workflow with editor revision loop"""

        workflow = StateGraph(WorkflowState)

        # Add all agent nodes
        workflow.add_node("admin_validate", self.admin_agent.validate_input)
        workflow.add_node("research", self.research_agent.research)
        workflow.add_node("strategize", self.strategist_agent.create_strategy)
        workflow.add_node("write", self.writer_agent.write)
        workflow.add_node("edit", self.editor_agent.review)
        workflow.add_node("format", self.formatter_agent.finalize)
        workflow.add_node("admin_finalize", self.admin_agent.finalize)

        # Set entry point
        workflow.set_entry_point("admin_validate")

        # Sequential flow
        workflow.add_edge("admin_validate", "research")
        workflow.add_edge("research", "strategize")
        workflow.add_edge("strategize", "write")
        workflow.add_edge("write", "edit")

        # Conditional: Editor can loop back to Writer
        workflow.add_conditional_edges(
            "edit",
            self._editor_decision,
            {
                "approve": "format",
                "revise": "write"  # Loop back for revision
            }
        )

        workflow.add_edge("format", "admin_finalize")
        workflow.add_edge("admin_finalize", END)

        return workflow.compile()

    def _editor_decision(self, state: WorkflowState) -> str:
        """Route based on editor's decision"""
        return state.get("editor_decision", "approve")

    def run(self, input_data: dict) -> dict:
        """Execute the complete 6-agent workflow"""

        print(f"\n{'='*60}")
        print(f"🚀 Starting LinkedIn Content Workflow")
        print(f"📝 Topic: {input_data['topic']}")
        print(f"🎯 Goal: {input_data['goal']}")
        print(f"{'='*60}\n")

        # Minimal initial state (agents will enrich it)
        initial_state = {
            "page_id": input_data["page_id"],
            "topic": input_data["topic"],
            "goal": input_data["goal"],
            "context": input_data.get("context", ""),
            # All other fields will be initialized by agents
            "workflow_id": "",
            "start_time": "",
            "time_allocation": 0,
            "completed_at": "",
            "duration_minutes": 0.0,
            "research_brief": "",
            "search_results": "",
            "content_strategy": {},
            "outline": [],
            "hooks": [],
            "post_body": "",
            "cta": "",
            "quality_score": 0,
            "editor_feedback": "",
            "editor_decision": "",
            "revision_count": 0,
            "hashtags": [],
            "visual_suggestion": "",
            "visual_format": "",
            "visual_specs": {},
            "character_count": 0,
            "word_count": 0,
            "estimated_read_time": "",
            "first_comment": "",
            "checklist": {},
            "status": "idea"
        }

        # Run workflow
        try:
            result = self.graph.invoke(initial_state)
            print(f"\n{'='*60}")
            print(f"✅ Workflow Completed Successfully!")
            print(f"{'='*60}\n")
            return result

        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            import traceback
            traceback.print_exc()
            initial_state["status"] = "error"
            raise
