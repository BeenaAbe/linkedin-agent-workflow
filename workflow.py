"""LangGraph Multi-Agent Workflow for LinkedIn Content Generation"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent


class WorkflowState(TypedDict):
    """State shared across all agents"""
    # Input
    page_id: str
    topic: str
    goal: str
    context: str

    # Research phase
    research_brief: str
    search_results: str

    # Writing phase
    hooks: list[str]
    post_body: str
    cta: str
    hashtags: list[str]
    visual_suggestion: str
    visual_format: str

    # Status tracking
    status: str  # researching, drafting, ready, error


class LinkedInWorkflow:
    """Multi-agent workflow orchestrator using LangGraph"""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""

        # Create graph
        workflow = StateGraph(WorkflowState)

        # Add nodes (agents)
        workflow.add_node("research", self.research_agent.research)
        workflow.add_node("write", self.writer_agent.write)

        # Define edges (workflow flow)
        workflow.set_entry_point("research")
        workflow.add_edge("research", "write")
        workflow.add_edge("write", END)

        return workflow.compile()

    def run(self, input_data: dict) -> dict:
        """Execute the workflow"""

        print(f"\n{'='*60}")
        print(f"🚀 Starting LinkedIn Content Workflow")
        print(f"📝 Topic: {input_data['topic']}")
        print(f"🎯 Goal: {input_data['goal']}")
        print(f"{'='*60}\n")

        # Initialize state
        initial_state = {
            "page_id": input_data["page_id"],
            "topic": input_data["topic"],
            "goal": input_data["goal"],
            "context": input_data.get("context", ""),
            "research_brief": "",
            "search_results": "",
            "hooks": [],
            "post_body": "",
            "cta": "",
            "hashtags": [],
            "visual_suggestion": "",
            "visual_format": "",
            "status": "idea"
        }

        # Run workflow
        try:
            result = self.graph.invoke(initial_state)
            result["status"] = "ready"
            print(f"\n✅ Workflow completed successfully!")
            return result

        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            initial_state["status"] = "error"
            raise


class AdaptiveLinkedInWorkflow(LinkedInWorkflow):
    """
    Enhanced workflow with conditional logic and quality checks.
    This demonstrates the power of LangGraph over fixed pipelines.
    """

    def _should_research_more(self, state: WorkflowState) -> str:
        """Decide if more research is needed"""
        research = state.get("research_brief", "")

        # Simple heuristic: if research is too short, do another pass
        if len(research) < 500:
            print("⚠️  Research brief too short, conducting additional research...")
            return "research"
        return "write"

    def _quality_check(self, state: WorkflowState) -> str:
        """Check if post meets quality standards"""
        post = state.get("post_body", "")

        # Check if post is substantial
        if len(post) < 200:
            print("⚠️  Post too short, regenerating...")
            return "write"

        # Check if hooks are present
        if len(state.get("hooks", [])) < 3:
            print("⚠️  Missing hooks, regenerating...")
            return "write"

        return "end"

    def _build_graph(self) -> StateGraph:
        """Build adaptive workflow with conditional routing"""

        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("research", self.research_agent.research)
        workflow.add_node("write", self.writer_agent.write)

        # Entry point
        workflow.set_entry_point("research")

        # Conditional edges
        workflow.add_conditional_edges(
            "research",
            self._should_research_more,
            {
                "research": "research",  # Loop back if needed
                "write": "write"
            }
        )

        workflow.add_conditional_edges(
            "write",
            self._quality_check,
            {
                "write": "write",  # Regenerate if needed
                "end": END
            }
        )

        return workflow.compile()
