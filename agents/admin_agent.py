"""Admin Agent - Validates inputs and orchestrates workflow"""

from typing import Dict, Any
from datetime import datetime
import uuid


class AdminAgent:
    """Agent responsible for input validation and workflow oversight"""

    # Valid content types
    VALID_GOALS = [
        "Thought Leadership",
        "Product",
        "Personal Brand",
        "Educational",
        "Interactive",
        "Inspirational"
    ]

    # Time allocation per content type (in minutes)
    TIME_ALLOCATIONS = {
        "Thought Leadership": 60,
        "Product": 50,
        "Personal Brand": 35,
        "Educational": 25,
        "Interactive": 10,
        "Inspirational": 33
    }

    def validate_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enrich input data"""

        print(f"🔍 Admin: Validating workflow input...")

        # Check required fields
        required_fields = ["page_id", "topic", "goal"]
        missing_fields = [f for f in required_fields if not state.get(f)]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate goal type
        goal = state["goal"]
        if goal not in self.VALID_GOALS:
            raise ValueError(
                f"Invalid goal type: '{goal}'. "
                f"Must be one of: {', '.join(self.VALID_GOALS)}"
            )

        # Enrich state with metadata
        workflow_id = str(uuid.uuid4())[:8]
        start_time = datetime.now().isoformat()
        time_allocation = self.TIME_ALLOCATIONS[goal]

        print(f"✅ Admin: Input validated")
        print(f"   Workflow ID: {workflow_id}")
        print(f"   Content Type: {goal}")
        print(f"   Time Budget: {time_allocation} minutes")

        # Update state
        return {
            **state,
            "workflow_id": workflow_id,
            "start_time": start_time,
            "time_allocation": time_allocation,
            "revision_count": 0,
            "status": "validated"
        }

    def finalize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Final validation before output"""

        print(f"\n🔍 Admin: Running pre-publish checklist...")

        # Pre-publish checklist
        checklist = self._run_checklist(state)

        # Calculate workflow duration
        start_time = datetime.fromisoformat(state["start_time"])
        duration_seconds = (datetime.now() - start_time).total_seconds()
        duration_minutes = round(duration_seconds / 60, 1)

        # Summary
        passed_checks = sum(checklist.values())
        total_checks = len(checklist)

        print(f"\n✅ Admin: Pre-publish checklist complete")
        print(f"   Passed: {passed_checks}/{total_checks} checks")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Quality Score: {state.get('quality_score', 'N/A')}")

        # Add completion metadata
        return {
            **state,
            "checklist": checklist,
            "duration_minutes": duration_minutes,
            "completed_at": datetime.now().isoformat(),
            "status": "ready"
        }

    def _run_checklist(self, state: Dict[str, Any]) -> Dict[str, bool]:
        """Run pre-publish validation checklist"""

        checklist = {}

        # 1. Strategy & Goal
        checklist["has_goal"] = bool(state.get("goal"))
        checklist["has_strategy"] = bool(state.get("content_strategy"))

        # 2. Content Quality
        checklist["has_hooks"] = len(state.get("hooks", [])) >= 3
        checklist["has_body"] = len(state.get("post_body", "")) > 100
        checklist["has_cta"] = bool(state.get("cta"))
        checklist["has_hashtags"] = 3 <= len(state.get("hashtags", [])) <= 5

        # 3. Format Optimization
        post_body = state.get("post_body", "")
        checklist["has_line_breaks"] = post_body.count('\n\n') >= 3

        # 4. Character count within limits
        char_count = len(post_body)
        goal = state.get("goal", "")

        max_chars = {
            "Thought Leadership": 1500,
            "Product": 1300,
            "Educational": 1200,
            "Personal Brand": 1000,
            "Interactive": 600,
            "Inspirational": 1000
        }

        limit = max_chars.get(goal, 1500)
        checklist["char_count_valid"] = char_count <= limit

        # 5. Quality score
        checklist["quality_score_pass"] = state.get("quality_score", 0) >= 70

        # 6. Visual specs
        checklist["has_visual_specs"] = bool(state.get("visual_specs"))

        # Print failed checks
        failed = [k for k, v in checklist.items() if not v]
        if failed:
            print(f"   ⚠️  Failed checks: {', '.join(failed)}")

        return checklist
