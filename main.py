"""Main execution script - Poll Notion and run workflow"""

import os
import time
from dotenv import load_dotenv
from workflow import LinkedInWorkflow, AdaptiveLinkedInWorkflow
from integrations.notion_client import NotionClient
from integrations.slack_notifier import SlackNotifier


def run_workflow_once():
    """Execute workflow for one idea from Notion"""

    # Initialize
    notion = NotionClient()
    slack = SlackNotifier()

    # Choose workflow type
    # workflow = LinkedInWorkflow()  # Simple sequential workflow
    workflow = AdaptiveLinkedInWorkflow()  # With quality checks

    # 1. Get next idea from Notion
    print("\n🔍 Checking Notion for new ideas...")
    idea = notion.get_next_idea()

    if not idea:
        print("📭 No new ideas found with status 'Idea'")
        return False

    print(f"✅ Found idea: {idea['topic']}")

    try:
        # 2. Update status to Researching
        notion.update_status(idea["page_id"], "Researching")

        # 3. Run the workflow
        result = workflow.run(idea)

        # 4. Update Notion with research
        notion.update_with_research(
            result["page_id"],
            result["research_brief"]
        )

        # 5. Update Notion with final draft
        notion.update_with_draft(
            result["page_id"],
            result
        )

        # 6. Send Slack notification
        slack.send_draft_notification(result)

        print("\n" + "="*60)
        print("🎉 SUCCESS! Draft is ready in Notion")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        notion.update_status(idea["page_id"], "Idea")  # Reset status
        slack.send_error_notification(str(e), idea["topic"])
        return False


def run_continuous(interval_seconds=120):
    """Run workflow continuously, polling every N seconds"""

    print("\n" + "="*60)
    print("🚀 LinkedIn Content Engine Started")
    print(f"⏰ Polling every {interval_seconds} seconds")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    try:
        while True:
            run_workflow_once()

            print(f"\n⏳ Waiting {interval_seconds} seconds before next check...\n")
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")


def run_single():
    """Run workflow once for testing"""
    run_workflow_once()


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Check required env vars
    required_vars = [
        "NOTION_TOKEN",
        "NOTION_DATABASE_ID",
        "TAVILY_API_KEY",
        "OPENROUTER_API_KEY"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        exit(1)

    import sys

    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else "continuous"

    if mode == "single":
        # Run once for testing
        run_single()
    else:
        # Run continuously (default)
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        run_continuous(interval)
