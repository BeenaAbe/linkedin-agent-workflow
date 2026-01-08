"""Main execution script - Poll Notion and run workflow"""

import os
import time
from dotenv import load_dotenv
from workflow import LinkedInWorkflow
from integrations.notion_client import NotionClient
from integrations.slack_notifier import SlackNotifier


def process_single_idea(notion, slack, workflow, idea):
    """Process a single idea through the workflow"""
    try:
        print(f"✅ Processing: {idea['topic']}")

        # 1. Update status to Researching
        notion.update_status(idea["page_id"], "Researching")

        # 2. Run the workflow
        result = workflow.run(idea)

        # 3. Update Notion with research
        notion.update_with_research(
            result["page_id"],
            result["research_brief"]
        )

        # 4. Update Notion with final draft
        notion.update_with_draft(
            result["page_id"],
            result
        )

        # 5. Send Slack notification
        slack.send_draft_notification(result)

        print("\n" + "="*60)
        print(f"🎉 SUCCESS! Draft ready: {idea['topic']}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Workflow failed for '{idea['topic']}': {e}")
        notion.update_status(idea["page_id"], "Idea")  # Reset status
        slack.send_error_notification(str(e), idea["topic"])
        return False


def run_workflow_once(use_change_detection=True):
    """Execute workflow for new ideas from Notion"""

    # Initialize
    notion = NotionClient()
    slack = SlackNotifier()

    # Initialize the 6-Agent Workflow
    workflow = LinkedInWorkflow()

    print("\n🔍 Checking Notion for new ideas...")

    # Get new ideas (with change detection if enabled)
    if use_change_detection:
        ideas = notion.get_new_ideas()
        last_check = notion.get_last_processed_time()
        if last_check:
            print(f"📅 Checking for ideas created after {last_check[:19]}")
    else:
        # Fallback: get one idea at a time (legacy behavior)
        idea = notion.get_next_idea()
        ideas = [idea] if idea else []

    if not ideas:
        print("📭 No new ideas found with status 'Idea'")
        return False

    print(f"✨ Found {len(ideas)} new idea(s)")

    # Process all ideas in batch
    success_count = 0
    for idea in ideas:
        if process_single_idea(notion, slack, workflow, idea):
            success_count += 1

    # Update timestamp after processing
    notion.update_last_processed_time()

    print(f"\n{'='*60}")
    print(f"📊 Batch complete: {success_count}/{len(ideas)} successful")
    print(f"{'='*60}\n")

    return success_count > 0


def run_continuous(interval_seconds=30):
    """Run workflow continuously with smart polling (fast when active, slower when idle)"""

    print("\n" + "="*60)
    print("🚀 LinkedIn Content Engine Started (Smart Polling Mode)")
    print(f"⏰ Idle polling: {interval_seconds}s | Active polling: 5s")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    try:
        while True:
            has_new_ideas = run_workflow_once(use_change_detection=True)

            if has_new_ideas:
                # Fast recheck for batch processing
                print(f"\n⚡ Quick recheck in 5 seconds for more ideas...\n")
                time.sleep(5)
            else:
                # Standard polling interval when idle
                print(f"\n⏳ No new ideas. Checking again in {interval_seconds} seconds...\n")
                time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")


def run_single():
    """Run workflow once for testing"""
    run_workflow_once(use_change_detection=False)


def run_batch():
    """Process all pending ideas immediately (batch mode)"""
    notion = NotionClient()
    slack = SlackNotifier()
    workflow = LinkedInWorkflow()

    print("\n" + "="*60)
    print("🔥 BATCH MODE: Processing all pending ideas")
    print("="*60 + "\n")

    ideas = notion.get_all_pending_ideas()

    if not ideas:
        print("📭 No pending ideas found with status 'Idea'")
        return

    print(f"✨ Found {len(ideas)} pending idea(s)\n")

    success_count = 0
    for idx, idea in enumerate(ideas, 1):
        print(f"\n{'='*60}")
        print(f"Processing {idx}/{len(ideas)}")
        print(f"{'='*60}\n")

        if process_single_idea(notion, slack, workflow, idea):
            success_count += 1

    # Update timestamp after batch
    notion.update_last_processed_time()

    print(f"\n{'='*60}")
    print(f"🎉 BATCH COMPLETE: {success_count}/{len(ideas)} successful")
    print(f"{'='*60}\n")


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
        # Run once for testing (no change detection)
        run_single()
    elif mode == "batch":
        # Process all pending ideas immediately
        run_batch()
    elif mode == "continuous":
        # Run continuously with smart polling (default 30s)
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        run_continuous(interval)
    else:
        print("Usage: python main.py [single|batch|continuous] [interval_seconds]")
        print("\nModes:")
        print("  single     - Process one idea (legacy, no change detection)")
        print("  batch      - Process all pending ideas immediately")
        print("  continuous - Smart polling mode (default: 30s idle, 5s active)")
        print("\nExamples:")
        print("  python main.py single")
        print("  python main.py batch")
        print("  python main.py continuous")
        print("  python main.py continuous 15  # Poll every 15 seconds when idle")
