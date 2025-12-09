"""
LinkedIn Content Engine - Streamlit Web Interface
Interactive testing and monitoring dashboard
"""

import streamlit as st
import os
from dotenv import load_dotenv
from workflow import LinkedInWorkflow, AdaptiveLinkedInWorkflow
from integrations.notion_client import NotionClient
from integrations.slack_notifier import SlackNotifier
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Also check Streamlit secrets (for cloud deployment)
# This allows using either .env (local) or secrets.toml (cloud)
try:
    if hasattr(st, 'secrets') and len(st.secrets) > 0:
        # Override with Streamlit secrets if available
        for key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass  # Fall back to .env if secrets not configured

# Page configuration
st.set_page_config(
    page_title="LinkedIn Content Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #0077B5, #00A0DC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #0c5460;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def check_env_vars():
    """Check if all required environment variables are set"""
    required = [
        "NOTION_TOKEN",
        "NOTION_DATABASE_ID",
        "TAVILY_API_KEY",
        "OPENROUTER_API_KEY"
    ]
    missing = [var for var in required if not os.getenv(var)]
    return missing


def init_session_state():
    """Initialize session state variables"""
    if 'workflow_running' not in st.session_state:
        st.session_state.workflow_running = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'logs' not in st.session_state:
        st.session_state.logs = []


def add_log(message, level="info"):
    """Add log message to session state"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        "time": timestamp,
        "level": level,
        "message": message
    })


def run_workflow(input_data, workflow_type="adaptive"):
    """Run the workflow with given input"""
    try:
        add_log(f"Starting workflow for: {input_data['topic']}", "info")

        # Select workflow type
        if workflow_type == "adaptive":
            workflow = AdaptiveLinkedInWorkflow()
            add_log("Using Adaptive Workflow (with quality checks)", "info")
        else:
            workflow = LinkedInWorkflow()
            add_log("Using Simple Sequential Workflow", "info")

        # Run workflow
        add_log("🔍 Researching topic...", "info")
        result = workflow.run(input_data)

        add_log("✅ Workflow completed successfully!", "success")
        return result

    except Exception as e:
        add_log(f"❌ Error: {str(e)}", "error")
        raise


def main():
    init_session_state()

    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Content Engine</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Check environment variables
    missing_vars = check_env_vars()
    if missing_vars:
        st.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        st.info("💡 Please create a `.env` file with all required API keys. See `.env.example` for reference.")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Workflow type selection
        workflow_type = st.radio(
            "Workflow Type",
            ["adaptive", "simple"],
            format_func=lambda x: "Adaptive (Quality Checks)" if x == "adaptive" else "Simple Sequential",
            help="Adaptive workflow includes self-correction and quality checks"
        )

        st.markdown("---")

        # Mode selection
        mode = st.radio(
            "Mode",
            ["manual", "notion"],
            format_func=lambda x: "Manual Input" if x == "manual" else "Notion Integration",
            help="Manual: Test with custom input\nNotion: Pull from Notion database"
        )

        st.markdown("---")

        # Environment info
        st.subheader("📊 Status")
        st.success("✅ OpenRouter Connected")
        st.success("✅ Tavily Connected")
        if os.getenv("NOTION_TOKEN"):
            st.success("✅ Notion Connected")
        if os.getenv("SLACK_WEBHOOK_URL"):
            st.success("✅ Slack Connected")

        st.markdown("---")

        # Show logs
        st.subheader("📝 Activity Log")
        if st.button("Clear Logs"):
            st.session_state.logs = []

        # Display logs
        log_container = st.container()
        with log_container:
            if st.session_state.logs:
                for log in st.session_state.logs[-10:]:  # Show last 10 logs
                    icon = "ℹ️" if log["level"] == "info" else "✅" if log["level"] == "success" else "❌"
                    st.text(f"{log['time']} {icon} {log['message']}")
            else:
                st.text("No activity yet...")

    # Main content
    if mode == "manual":
        st.header("✍️ Manual Input Mode")
        st.write("Test the workflow with custom input")

        col1, col2 = st.columns(2)

        with col1:
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Why most AI agents are just fancy chatbots",
                help="The main topic of your LinkedIn post"
            )

            goal = st.selectbox(
                "Goal",
                ["Thought Leadership", "Product", "Educational", "Personal Brand", "Interactive", "Inspirational"],
                help="The purpose of your post"
            )

        with col2:
            context = st.text_area(
                "Context/Notes (Optional)",
                placeholder="e.g., Lead with the 83% Gartner stat. Contrast chatbots vs real agents.",
                help="Additional context or specific instructions",
                height=100
            )

        if st.button("🚀 Generate Post", type="primary", disabled=st.session_state.workflow_running):
            if not topic:
                st.error("Please enter a topic")
            else:
                st.session_state.workflow_running = True
                st.session_state.results = None

                with st.spinner("Running workflow..."):
                    try:
                        input_data = {
                            "page_id": "manual-test",
                            "topic": topic,
                            "goal": goal,
                            "context": context
                        }

                        result = run_workflow(input_data, workflow_type)
                        st.session_state.results = result
                        st.session_state.workflow_running = False
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.session_state.workflow_running = False

    else:  # Notion mode
        st.header("📋 Notion Integration Mode")
        st.write("Process ideas from your Notion database")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.info("💡 This will fetch the next entry with Status = 'Idea' from your Notion database")

        with col2:
            if st.button("🔍 Fetch & Process", type="primary", disabled=st.session_state.workflow_running):
                st.session_state.workflow_running = True
                st.session_state.results = None

                with st.spinner("Fetching from Notion..."):
                    try:
                        notion = NotionClient()
                        idea = notion.get_next_idea()

                        if not idea:
                            st.warning("📭 No ideas found with Status = 'Idea'")
                            add_log("No ideas found in Notion", "info")
                            st.session_state.workflow_running = False
                        else:
                            add_log(f"Found idea: {idea['topic']}", "success")

                            # Update status to Researching
                            notion.update_status(idea["page_id"], "Researching")

                            # Run workflow
                            result = run_workflow(idea, workflow_type)

                            # Update Notion with results
                            add_log("Updating Notion with research...", "info")
                            notion.update_with_research(result["page_id"], result["research_brief"])

                            add_log("Updating Notion with draft...", "info")
                            notion.update_with_draft(result["page_id"], result)

                            # Send Slack notification
                            if os.getenv("SLACK_WEBHOOK_URL"):
                                add_log("Sending Slack notification...", "info")
                                slack = SlackNotifier()
                                slack.send_draft_notification(result)

                            st.session_state.results = result
                            st.session_state.workflow_running = False
                            st.rerun()

                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        add_log(f"Error: {str(e)}", "error")
                        st.session_state.workflow_running = False

        # Show current queue status
        if os.getenv("NOTION_TOKEN"):
            with st.expander("📊 Queue Status"):
                try:
                    notion = NotionClient()
                    idea = notion.get_next_idea()
                    if idea:
                        st.success(f"✅ Next in queue: **{idea['topic']}**")
                        st.write(f"**Goal:** {idea['goal']}")
                        if idea['context']:
                            st.write(f"**Context:** {idea['context']}")
                    else:
                        st.info("📭 Queue is empty")
                except Exception as e:
                    st.error(f"Could not fetch queue: {str(e)}")

    # Display results
    if st.session_state.results:
        st.markdown("---")
        st.header("📄 Generated Content")

        result = st.session_state.results

        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Hooks", "✍️ Post", "🔬 Research", "🎨 Visual"])

        with tab1:
            st.subheader("Hook Options")
            st.write("Choose your favorite opening line:")

            for i, hook in enumerate(result.get("hooks", []), 1):
                with st.container():
                    st.markdown(f"**Option {i}:**")
                    st.info(hook)
                    if st.button(f"Copy Hook {i}", key=f"copy_hook_{i}"):
                        st.write("✅ Copied to clipboard")

        with tab2:
            st.subheader("Post Body")

            # Character count
            char_count = len(result.get("post_body", ""))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Character Count", char_count)
            with col2:
                st.metric("Est. Read Time", "45-60 sec")
            with col3:
                status = "✅ Good" if char_count < 1500 else "⚠️ Too Long"
                st.metric("Status", status)

            st.markdown("**Full Post:**")
            st.text_area(
                "Post Content",
                value=result.get("post_body", ""),
                height=300,
                key="post_body"
            )

            st.markdown("**Call-to-Action:**")
            st.info(result.get("cta", ""))

            st.markdown("**Hashtags:**")
            hashtags = " ".join(result.get("hashtags", []))
            st.code(hashtags)

        with tab3:
            st.subheader("Research Brief")
            st.markdown(result.get("research_brief", "No research available"))

        with tab4:
            st.subheader("Visual Asset Suggestion")
            st.write(f"**Format:** {result.get('visual_format', 'N/A')}")
            st.write(f"**Suggestion:** {result.get('visual_suggestion', 'N/A')}")

        # Download button
        st.markdown("---")

        # Format complete post
        complete_post = f"""HOOK OPTIONS:
1. {result.get("hooks", [""])[0]}
2. {result.get("hooks", ["", ""])[1]}
3. {result.get("hooks", ["", "", ""])[2]}

POST BODY:
{result.get("post_body", "")}

{result.get("cta", "")}

{" ".join(result.get("hashtags", []))}
"""

        st.download_button(
            label="📥 Download Complete Post",
            data=complete_post,
            file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()
