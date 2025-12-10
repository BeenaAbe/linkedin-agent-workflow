"""
LinkedIn Content Engine - Enhanced Streamlit Web Interface
Production-grade UI with modern design and advanced features
"""

import streamlit as st
import os
import pyperclip
import plotly.graph_objects as go
from dotenv import load_dotenv
from workflow import LinkedInWorkflow, AdaptiveLinkedInWorkflow
from integrations.notion_client import NotionClient
from integrations.slack_notifier import SlackNotifier
import time
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Also check Streamlit secrets (for cloud deployment)
try:
    if hasattr(st, 'secrets') and len(st.secrets) > 0:
        for key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass

# Page configuration
st.set_page_config(
    page_title="LinkedIn Content Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main header with LinkedIn gradient */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 50%, #0077B5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hook cards */
    .hook-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #0077B5;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .hook-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 119, 181, 0.15);
    }

    .hook-type-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .badge-controversial {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
    }

    .badge-question {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
    }

    .badge-story {
        background: linear-gradient(135deg, #A8E6CF, #56AB91);
        color: white;
    }

    .hook-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2C3E50;
        font-weight: 500;
    }

    .char-count {
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-top: 0.5rem;
    }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Progress indicators */
    .progress-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .progress-step {
        display: flex;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid #e9ecef;
    }

    .progress-step:last-child {
        border-bottom: none;
    }

    .progress-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }

    .progress-text {
        flex: 1;
        font-size: 1rem;
        color: #495057;
    }

    /* Status boxes */
    .status-box {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
        color: #155724;
    }

    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left-color: #dc3545;
        color: #721c24;
    }

    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left-color: #ffc107;
        color: #856404;
    }

    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left-color: #17a2b8;
        color: #0c5460;
    }

    /* LinkedIn preview */
    .linkedin-preview {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        max-width: 600px;
        margin: 1rem auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .linkedin-preview-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    .linkedin-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0077B5, #00A0DC);
        margin-right: 12px;
    }

    .linkedin-preview-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: rgba(0, 0, 0, 0.9);
        white-space: pre-wrap;
    }

    /* Queue card */
    .queue-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }

    .queue-card:hover {
        border-color: #0077B5;
        box-shadow: 0 4px 8px rgba(0, 119, 181, 0.1);
    }

    /* Button enhancements */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 119, 181, 0.3);
    }

    /* Copy button */
    .copy-btn {
        background: linear-gradient(135deg, #0077B5, #00A0DC);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }

    .copy-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 119, 181, 0.4);
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
    if 'progress' not in st.session_state:
        st.session_state.progress = []
    if 'history' not in st.session_state:
        st.session_state.history = []


def add_log(message, level="info"):
    """Add log message to session state"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        "time": timestamp,
        "level": level,
        "message": message
    })


def add_progress(phase, status, details=""):
    """Add progress update"""
    st.session_state.progress.append({
        "phase": phase,
        "status": status,
        "details": details,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


def get_hook_type(index):
    """Get hook type based on index"""
    types = ["controversial", "question", "story"]
    labels = ["🔥 Controversial", "❓ Question", "📖 Story"]
    return types[index % 3], labels[index % 3]


def calculate_quality_score(result):
    """Calculate quality score based on best practices"""
    score = 100
    post_body = result.get("post_body", "")
    hooks = result.get("hooks", [])

    # Character count (optimal: 800-1300)
    char_count = len(post_body)
    if char_count < 200:
        score -= 30
    elif char_count > 1500:
        score -= 20
    elif char_count < 800 or char_count > 1300:
        score -= 10

    # Hook diversity
    if len(hooks) < 3:
        score -= 20

    # Line breaks check (should have multiple line breaks)
    line_breaks = post_body.count('\n\n')
    if line_breaks < 3:
        score -= 15

    # Hashtags
    hashtags = result.get("hashtags", [])
    if len(hashtags) < 3 or len(hashtags) > 5:
        score -= 10

    return max(0, score)


def create_character_gauge(char_count):
    """Create a gauge chart for character count"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=char_count,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Character Count", 'font': {'size': 20}},
        delta={'reference': 1200, 'increasing': {'color': "#FF6B6B"}},
        gauge={
            'axis': {'range': [None, 1500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#0077B5"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 800], 'color': '#FFE5E5'},
                {'range': [800, 1300], 'color': '#E5F5E5'},
                {'range': [1300, 1500], 'color': '#FFF5E5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 1400
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#2C3E50", 'family': "Arial"}
    )

    return fig


def render_hook_card(hook, index):
    """Render a beautiful hook card"""
    hook_type, hook_label = get_hook_type(index)
    char_count = len(hook)

    # Create badge class
    badge_class = f"badge-{hook_type}"

    hook_html = f"""
    <div class="hook-card">
        <span class="hook-type-badge {badge_class}">{hook_label}</span>
        <div class="hook-text">{hook}</div>
        <div class="char-count">📝 {char_count} characters</div>
    </div>
    """

    st.markdown(hook_html, unsafe_allow_html=True)

    # Copy button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button(f"📋 Copy", key=f"copy_hook_{index}", use_container_width=True):
            try:
                pyperclip.copy(hook)
                st.success("✅ Copied!")
            except:
                st.info("Copy the text above manually")
    with col3:
        if st.button(f"🔄 Regenerate", key=f"regen_hook_{index}", use_container_width=True):
            st.info("🚧 Regeneration coming soon!")


def render_linkedin_preview(post_body, hooks):
    """Render LinkedIn mobile preview"""
    preview_html = f"""
    <div class="linkedin-preview">
        <div class="linkedin-preview-header">
            <div class="linkedin-avatar"></div>
            <div>
                <div style="font-weight: 600; font-size: 0.95rem;">Your Name</div>
                <div style="font-size: 0.8rem; color: #666;">Your Title • Just now • 🌐</div>
            </div>
        </div>
        <div class="linkedin-preview-content">{hooks[0] if hooks else ''}\n\n{post_body[:300]}{'...' if len(post_body) > 300 else ''}</div>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)


def run_workflow(input_data, workflow_type="adaptive"):
    """Run the workflow with progress tracking"""
    try:
        st.session_state.progress = []
        add_progress("🚀 Starting", "active", f"Topic: {input_data['topic']}")
        add_log(f"Starting workflow for: {input_data['topic']}", "info")

        # Select workflow type
        if workflow_type == "adaptive":
            workflow = AdaptiveLinkedInWorkflow()
            add_log("Using Adaptive Workflow (with quality checks)", "info")
        else:
            workflow = LinkedInWorkflow()
            add_log("Using Simple Sequential Workflow", "info")

        # Research phase
        add_progress("🔍 Research", "active", "Searching web sources...")
        add_log("🔍 Researching topic...", "info")

        time.sleep(0.5)  # Brief pause for UI update

        # Run workflow
        result = workflow.run(input_data)

        add_progress("✅ Complete", "complete", "Draft generated successfully!")
        add_log("✅ Workflow completed successfully!", "success")

        return result

    except Exception as e:
        add_progress("❌ Error", "error", str(e))
        add_log(f"❌ Error: {str(e)}", "error")
        raise


def render_progress_tracker():
    """Render live progress tracker"""
    if st.session_state.progress:
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.subheader("⏳ Progress")

        for item in st.session_state.progress:
            status_icon = "✅" if item["status"] == "complete" else "❌" if item["status"] == "error" else "⏳"
            st.markdown(f"""
            <div class="progress-step">
                <div class="progress-icon">{status_icon}</div>
                <div class="progress-text">
                    <strong>{item["phase"]}</strong><br>
                    <small>{item["details"]}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def main():
    init_session_state()

    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Content Engine</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7F8C8D; font-size: 1.1rem; margin-top: -1rem;'>AI-Powered Content Generation with Research & Analytics</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Check environment variables
    missing_vars = check_env_vars()
    if missing_vars:
        st.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        st.info("💡 Please create a `.env` file with all required API keys. See `.env.example` for reference.")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")

        # Workflow type selection
        workflow_type = st.radio(
            "Workflow Type",
            ["adaptive", "simple"],
            format_func=lambda x: "✨ Adaptive (Quality Checks)" if x == "adaptive" else "⚡ Simple Sequential",
            help="Adaptive workflow includes self-correction and quality checks"
        )

        st.markdown("---")

        # Mode selection
        mode = st.radio(
            "Mode",
            ["manual", "notion"],
            format_func=lambda x: "✍️ Manual Input" if x == "manual" else "📋 Notion Queue",
            help="Manual: Test with custom input & optionally save to Notion\nNotion: Select and process ideas from database (single or batch)"
        )

        st.markdown("---")

        # Environment status
        st.markdown("### 📊 Connection Status")
        st.success("✅ OpenRouter")
        st.success("✅ Tavily")
        if os.getenv("NOTION_TOKEN"):
            st.success("✅ Notion")
        if os.getenv("SLACK_WEBHOOK_URL"):
            st.success("✅ Slack")

        st.markdown("---")

        # Activity log
        st.markdown("### 📝 Activity Log")
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.session_state.logs = []
            st.rerun()

        # Display logs in a scrollable container
        if st.session_state.logs:
            log_html = "<div style='height: 300px; overflow-y: auto; font-size: 0.85rem; background: #f8f9fa; padding: 0.5rem; border-radius: 8px;'>"
            for log in st.session_state.logs[-20:]:
                icon = "ℹ️" if log["level"] == "info" else "✅" if log["level"] == "success" else "❌"
                log_html += f"<div style='margin: 0.3rem 0;'><code>{log['time']}</code> {icon} {log['message']}</div>"
            log_html += "</div>"
            st.markdown(log_html, unsafe_allow_html=True)
        else:
            st.info("No activity yet...")

    # Main content area
    if mode == "manual":
        st.markdown("## ✍️ Manual Input Mode")
        st.markdown("Test the workflow with custom input for rapid iteration")

        col1, col2 = st.columns([2, 1])

        with col1:
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Why most AI agents are just fancy chatbots",
                help="The main topic of your LinkedIn post"
            )

        with col2:
            goal = st.selectbox(
                "Goal",
                ["Thought Leadership", "Product", "Educational", "Personal Brand", "Interactive", "Inspirational"],
                help="The purpose of your post determines CTA and visual suggestions"
            )

        context = st.text_area(
            "Context/Notes/Links (Optional)",
            placeholder="""You can include:
• Links to reference: https://example.com/article
• Rough notes: "mention 83% Gartner stat, target PM audience"
• Specific ideas: "lead with controversial take, compare X vs Y"
• Any instructions or direction for the content

Leave empty to let the AI research independently.""",
            help="Add links, rough notes, ideas, or specific instructions. The AI will use whatever you provide as guidance. Works with minimal or detailed input!",
            height=120
        )

        # Save to Notion checkbox
        save_to_notion = st.checkbox(
            "💾 Save to Notion after generation",
            value=False,
            help="Automatically create a new page in your Notion database with the generated content"
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            generate_btn = st.button("🚀 Generate Post", type="primary", disabled=st.session_state.workflow_running, use_container_width=True)
        with col2:
            if st.button("🎲 Random Example", use_container_width=True):
                st.info("🚧 Coming soon!")
        with col3:
            if st.session_state.results and st.button("💾 Save to Notion Now", use_container_width=True):
                try:
                    with st.spinner("Saving to Notion..."):
                        notion = NotionClient()
                        result = st.session_state.results
                        page_id = notion.create_new_page_with_draft(
                            topic=result.get("topic", topic),
                            goal=result.get("goal", goal),
                            context=result.get("context", context),
                            draft_data=result
                        )
                        st.success(f"✅ Saved to Notion! Page ID: {page_id[:8]}...")
                        add_log(f"Saved manual post to Notion: {topic}", "success")
                except Exception as e:
                    st.error(f"❌ Error saving to Notion: {str(e)}")
                    add_log(f"Error saving to Notion: {str(e)}", "error")

        if generate_btn:
            if not topic:
                st.error("⚠️ Please enter a topic")
            else:
                st.session_state.workflow_running = True
                st.session_state.results = None

                # Progress container
                progress_container = st.empty()

                try:
                    input_data = {
                        "page_id": "manual-test",
                        "topic": topic,
                        "goal": goal,
                        "context": context
                    }

                    with st.spinner("🔮 Generating your LinkedIn post..."):
                        result = run_workflow(input_data, workflow_type)

                        # Save to Notion if checkbox is checked
                        if save_to_notion:
                            try:
                                with st.spinner("💾 Saving to Notion..."):
                                    notion = NotionClient()
                                    page_id = notion.create_new_page_with_draft(
                                        topic=topic,
                                        goal=goal,
                                        context=context,
                                        draft_data=result
                                    )
                                    add_log(f"✅ Saved to Notion! Page ID: {page_id[:8]}...", "success")
                                    st.success(f"✅ Post generated AND saved to Notion!")
                            except Exception as e:
                                st.warning(f"⚠️ Post generated but failed to save to Notion: {str(e)}")
                                add_log(f"Error saving to Notion: {str(e)}", "error")

                        # Add to history
                        st.session_state.history.append({
                            "timestamp": datetime.now(),
                            "topic": topic,
                            "goal": goal,
                            "result": result
                        })

                        st.session_state.results = result
                        st.session_state.workflow_running = False
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.workflow_running = False

    elif mode == "notion":
        st.markdown("## 📋 Notion Queue")
        st.markdown("Select ideas from your database and process them (single or batch)")

        # Initialize selected_ideas in session state
        if 'selected_ideas' not in st.session_state:
            st.session_state.selected_ideas = []

        # Fetch ideas once
        try:
            notion = NotionClient()
            all_ideas = notion.get_all_pending_ideas()

            if not all_ideas:
                st.info("📭 No pending ideas found in Notion. Add ideas with Status = 'Idea' to your database.")
            else:
                st.success(f"✨ Found {len(all_ideas)} pending idea(s)")

                # Select All / Deselect All buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("☑️ Select All", use_container_width=True):
                        st.session_state.selected_ideas = [idea['page_id'] for idea in all_ideas]
                        st.rerun()
                with col2:
                    if st.button("⬜ Deselect All", use_container_width=True):
                        st.session_state.selected_ideas = []
                        st.rerun()
                with col3:
                    st.metric("Selected", len(st.session_state.selected_ideas))

                st.markdown("---")

                # Display ideas with checkboxes
                st.markdown("### ✅ Select Ideas to Process")
                st.info("💡 Tip: Select one for single processing or multiple for batch processing")

                for idx, idea in enumerate(all_ideas):
                    col1, col2 = st.columns([1, 20])

                    with col1:
                        is_selected = st.checkbox(
                            "",
                            value=idea['page_id'] in st.session_state.selected_ideas,
                            key=f"cb_{idea['page_id']}",
                            label_visibility="collapsed"
                        )

                        # Update selection state
                        if is_selected and idea['page_id'] not in st.session_state.selected_ideas:
                            st.session_state.selected_ideas.append(idea['page_id'])
                        elif not is_selected and idea['page_id'] in st.session_state.selected_ideas:
                            st.session_state.selected_ideas.remove(idea['page_id'])

                    with col2:
                        # Style based on selection
                        card_style = "border: 3px solid #0077B5; background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);" if is_selected else ""
                        st.markdown(f"""
                        <div class="queue-card" style="{card_style}">
                            <strong>{idx + 1}. {idea['topic']}</strong><br>
                            <small>🎯 Goal: {idea['goal']}</small>
                            {f"<br><small>📝 {idea.get('context', '')[:100]}...</small>" if idea.get('context') else ''}
                        </div>
                        """, unsafe_allow_html=True)

                # Process selected button
                if st.session_state.selected_ideas:
                    st.markdown("---")
                    num_selected = len(st.session_state.selected_ideas)

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        button_text = f"🚀 Process {num_selected} Idea{'s' if num_selected > 1 else ''}"
                        if st.button(
                            button_text,
                            type="primary",
                            disabled=st.session_state.workflow_running,
                            use_container_width=True
                        ):
                            st.session_state.workflow_running = True

                            # Get selected ideas
                            selected_ideas_data = [idea for idea in all_ideas if idea['page_id'] in st.session_state.selected_ideas]

                            # Process each selected idea
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            results_list = []

                            for idx, idea in enumerate(selected_ideas_data, 1):
                                try:
                                    status_text.markdown(f"**Processing {idx}/{len(selected_ideas_data)}: {idea['topic']}**")
                                    progress_bar.progress(idx / len(selected_ideas_data))

                                    add_log(f"Processing {idx}/{len(selected_ideas_data)}: {idea['topic']}", "info")

                                    # Update status
                                    notion.update_status(idea["page_id"], "Researching")

                                    # Run workflow
                                    result = run_workflow(idea, workflow_type)

                                    # Update Notion
                                    notion.update_with_research(result["page_id"], result["research_brief"])
                                    notion.update_with_draft(result["page_id"], result)

                                    # Slack notification
                                    if os.getenv("SLACK_WEBHOOK_URL"):
                                        slack = SlackNotifier()
                                        slack.send_draft_notification(result)

                                    results_list.append(result)
                                    add_log(f"✅ Completed: {idea['topic']}", "success")

                                except Exception as e:
                                    st.error(f"❌ Error processing {idea['topic']}: {str(e)}")
                                    add_log(f"Error: {str(e)}", "error")

                            # Complete
                            progress_bar.progress(1.0)
                            status_text.markdown(f"**✅ Completed {len(results_list)}/{len(selected_ideas_data)} ideas**")

                            st.success(f"🎉 Successfully processed {len(results_list)} idea(s)!")

                            # Show last result
                            if results_list:
                                st.session_state.results = results_list[-1]

                            # Clear selection
                            st.session_state.selected_ideas = []
                            st.session_state.workflow_running = False

                            time.sleep(2)
                            st.rerun()

                    with col2:
                        if st.button("🗑️ Clear Selection", use_container_width=True):
                            st.session_state.selected_ideas = []
                            st.rerun()

                else:
                    st.info("👆 Select at least one idea to process")

        except Exception as e:
            st.error(f"❌ Error fetching Notion queue: {str(e)}")

    # Display results
    if st.session_state.results:
        st.markdown("---")
        st.markdown("# 📄 Generated Content")

        result = st.session_state.results

        # Quality score
        quality_score = calculate_quality_score(result)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Quality Score", f"{quality_score}/100",
                     delta="Good" if quality_score >= 80 else "Needs work",
                     delta_color="normal" if quality_score >= 80 else "inverse")

        with col2:
            char_count = len(result.get("post_body", ""))
            st.metric("Characters", char_count,
                     delta=f"{1500 - char_count} left",
                     delta_color="normal" if char_count < 1500 else "inverse")

        with col3:
            hook_count = len(result.get("hooks", []))
            st.metric("Hooks", hook_count, delta="Complete" if hook_count == 3 else "Missing")

        with col4:
            hashtag_count = len(result.get("hashtags", []))
            st.metric("Hashtags", hashtag_count,
                     delta="Optimal" if 3 <= hashtag_count <= 5 else "Adjust")

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Hooks", "✍️ Post", "📊 Analytics", "🔬 Research", "🎨 Visual"])

        with tab1:
            st.markdown("### Hook Options")
            st.markdown("Choose your favorite opening line - each follows a proven formula:")

            hooks = result.get("hooks", [])
            for i, hook in enumerate(hooks):
                render_hook_card(hook, i)

        with tab2:
            st.markdown("### Post Body")

            # Editor
            post_body = st.text_area(
                "Edit your post",
                value=result.get("post_body", ""),
                height=300,
                help="Edit the post content directly. Changes are not saved automatically."
            )

            # Character counter
            char_count = len(post_body)
            if char_count > 1500:
                st.error(f"⚠️ Post is {char_count - 1500} characters over LinkedIn's limit!")
            elif char_count > 1300:
                st.warning(f"⚠️ Post is approaching the limit ({char_count}/1500)")
            else:
                st.success(f"✅ {char_count}/1500 characters ({1500 - char_count} remaining)")

            st.markdown("---")

            # CTA and Hashtags
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Call-to-Action:**")
                st.info(result.get("cta", ""))

            with col2:
                st.markdown("**Hashtags:**")
                hashtags = " ".join(result.get("hashtags", []))
                st.code(hashtags)

            st.markdown("---")

            # LinkedIn Preview
            st.markdown("### 📱 LinkedIn Preview")
            render_linkedin_preview(post_body, hooks)

            # Copy complete post
            complete_post = f"{hooks[0] if hooks else ''}\n\n{post_body}\n\n{result.get('cta', '')}\n\n{hashtags}"

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy Complete Post", use_container_width=True):
                    try:
                        pyperclip.copy(complete_post)
                        st.success("✅ Copied to clipboard!")
                    except:
                        st.code(complete_post)
                        st.info("👆 Copy the text above manually")

            with col2:
                st.download_button(
                    label="📥 Download as TXT",
                    data=complete_post,
                    file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        with tab3:
            st.markdown("### Analytics & Metrics")

            col1, col2 = st.columns(2)

            with col1:
                # Character gauge
                st.plotly_chart(create_character_gauge(char_count), use_container_width=True)

            with col2:
                st.markdown("#### Content Breakdown")

                # Line breaks
                line_breaks = post_body.count('\n\n')
                st.metric("Line Breaks", line_breaks,
                         delta="Good" if line_breaks >= 4 else "Add more",
                         delta_color="normal" if line_breaks >= 4 else "inverse")

                # Word count
                word_count = len(post_body.split())
                st.metric("Word Count", word_count)

                # Sentences
                sentence_count = post_body.count('.') + post_body.count('!') + post_body.count('?')
                st.metric("Sentences", sentence_count)

                # Avg words per sentence
                avg_words = round(word_count / sentence_count if sentence_count > 0 else 0, 1)
                st.metric("Avg Words/Sentence", avg_words,
                         delta="Good" if avg_words < 20 else "Too long",
                         delta_color="normal" if avg_words < 20 else "inverse")

            # Quality suggestions
            st.markdown("---")
            st.markdown("#### 💡 Quality Suggestions")

            suggestions = []
            if char_count < 800:
                suggestions.append("📝 Consider expanding your post to 800-1300 characters for optimal engagement")
            if line_breaks < 4:
                suggestions.append("↩️ Add more line breaks (aim for 4-6) for mobile readability")
            if hashtag_count < 3:
                suggestions.append("🏷️ Add more hashtags (aim for 3-5) to increase discoverability")
            if avg_words > 20:
                suggestions.append("✂️ Shorten sentences for better readability (aim for < 20 words per sentence)")

            if suggestions:
                for s in suggestions:
                    st.warning(s)
            else:
                st.success("🎉 Your post looks great! No major issues detected.")

        with tab4:
            st.markdown("### Research Brief")
            research = result.get("research_brief", "No research available")

            # Try to parse as JSON if it looks like JSON
            if research.strip().startswith('{'):
                try:
                    research_json = json.loads(research)

                    # Display structured research
                    if "key_insights" in research_json:
                        st.markdown("#### 🔑 Key Insights")
                        for insight in research_json["key_insights"]:
                            st.markdown(f"- {insight}")

                    if "statistics" in research_json:
                        st.markdown("#### 📊 Statistics")
                        for stat in research_json["statistics"]:
                            st.info(f"**{stat.get('stat')}**  \nSource: {stat.get('source')}")

                    if "contrarian_angles" in research_json:
                        st.markdown("#### 💡 Contrarian Angles")
                        for angle in research_json["contrarian_angles"]:
                            st.markdown(f"- {angle}")

                except json.JSONDecodeError:
                    st.markdown(research)
            else:
                st.markdown(research)

        with tab5:
            st.markdown("### Visual Asset Suggestion")

            visual_format = result.get('visual_format', 'N/A')
            visual_suggestion = result.get('visual_suggestion', 'N/A')

            st.markdown(f"**Recommended Format:** `{visual_format}`")
            st.markdown(visual_suggestion)

            st.markdown("---")
            st.info("🚧 Visual generation coming soon! For now, use this suggestion to create your asset manually.")

        # History section
        if len(st.session_state.history) > 1:
            st.markdown("---")
            with st.expander(f"📜 Session History ({len(st.session_state.history)} posts)"):
                for idx, item in enumerate(reversed(st.session_state.history), 1):
                    st.markdown(f"**{idx}. {item['topic']}** ({item['goal']}) - {item['timestamp'].strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
