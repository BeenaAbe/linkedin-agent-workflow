"""
LinkedIn Content Engine - Modern Gradient UI
Clean, professional design with LinkedIn brand colors and enhanced typography
"""

import streamlit as st
import os
import pyperclip
import plotly.graph_objects as go
from dotenv import load_dotenv
from workflow import LinkedInWorkflow
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

# Makepresentable-Inspired Design - Clean, Modern, Professional
st.markdown("""
<style>
    /* Import Outfit font (similar to makepresentable) */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Global reset and typography */
    * {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }

    /* Main app background - coral to black gradient */
    .stApp {
        background: linear-gradient(180deg, #e07856 0%, #d06850 25%, #a05048 50%, #704040 75%, #000000 100%) !important;
        min-height: 100vh;
    }

    /* Ensure main content area is transparent to show gradient */
    .main {
        background: transparent !important;
    }

    /* Main container spacing */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Main header - clean, bold, minimal */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #0a0a0a;
        letter-spacing: -0.04em;
        line-height: 1;
    }

    .subtitle {
        text-align: center;
        color: #737373;
        font-size: 1.1rem;
        margin-top: 0.8rem;
        margin-bottom: 3.5rem;
        font-weight: 400;
        letter-spacing: -0.005em;
    }

    /* LinkedIn accent color */
    .accent {
        color: #0077B5;
    }

    /* Hook cards - Muted color backgrounds with subtle variations */
    .hook-card {
        background: #f8f8f7;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e8e8e6;
        margin: 1.5rem 0;
        transition: all 0.2s ease;
        position: relative;
    }

    .hook-card:hover {
        background: #f3f3f1;
        border-color: #d4d4d2;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }

    /* Subtle color tints for visual variety */
    .hook-card:nth-child(1) {
        background: linear-gradient(135deg, #fff0f7 0%, #fff5fb 100%);
        border-left: 3px solid #c72a6e;
    }

    .hook-card:nth-child(2) {
        background: linear-gradient(135deg, #fffbeb 0%, #fffef5 100%);
        border-left: 3px solid #d97706;
    }

    .hook-card:nth-child(3) {
        background: linear-gradient(135deg, #fff7ed 0%, #fffcf5 100%);
        border-left: 3px solid #ea580c;
    }

    .hook-type-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .badge-controversial {
        background: #fff0f7;
        color: #c72a6e;
        border: 1px solid #ffd6eb;
    }

    .badge-question {
        background: #fffbeb;
        color: #d97706;
        border: 1px solid #fef3c7;
    }

    .badge-story {
        background: #fff7ed;
        color: #ea580c;
        border: 1px solid #fed7aa;
    }

    .hook-text {
        font-size: 1.1rem;
        line-height: 1.65;
        color: #171717;
        font-weight: 400;
    }

    .char-count {
        font-size: 0.85rem;
        color: #737373;
        margin-top: 1rem;
        font-weight: 400;
    }

    /* Metrics - Yellow and Pink accents */
    .metric-card {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.25);
        text-align: center;
        border: 1px solid #fde68a;
    }

    .metric-card:nth-child(2) {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.25);
        border: 1px solid #f9a8d4;
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

    /* Progress indicators - Muted style */
    .progress-container {
        background: #f8f8f7;
        border: 1px solid #e8e8e6;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }

    .progress-step {
        display: flex;
        align-items: center;
        padding: 0.9rem 0;
        border-bottom: 1px solid #f5f5f5;
    }

    .progress-step:last-child {
        border-bottom: none;
    }

    .progress-icon {
        font-size: 1.4rem;
        margin-right: 1.2rem;
    }

    .progress-text {
        flex: 1;
        font-size: 0.95rem;
        color: #404040;
    }

    /* Status boxes - Muted design */
    .status-box {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid;
    }

    .success-box {
        background: #f3f5f3;
        border-color: #d8e3d8;
        color: #5a7a5a;
    }

    .error-box {
        background: #f5f3f3;
        border-color: #e3d8d8;
        color: #8b6b6b;
    }

    .warning-box {
        background: #fffbeb;
        border-color: #fde047;
        color: #ca8a04;
    }

    .info-box {
        background: #f3f5f5;
        border-color: #d8e0e5;
        color: #5a6b7a;
    }

    /* LinkedIn preview - Muted card */
    .linkedin-preview {
        background: #f8f8f7;
        border: 1px solid #e8e8e6;
        border-radius: 12px;
        padding: 2rem;
        max-width: 650px;
        margin: 1.5rem auto;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
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
        background: #0077B5;
        margin-right: 14px;
    }

    .linkedin-preview-content {
        font-size: 0.95rem;
        line-height: 1.65;
        color: #171717;
        white-space: pre-wrap;
    }

    /* Queue card - Muted style */
    .queue-card {
        background: #f8f8f7;
        border: 1px solid #e8e8e6;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        transition: all 0.15s ease;
    }

    .queue-card:hover {
        background: #f3f3f1;
        border-color: #d4d4d2;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    /* Button styling - Clean and minimal */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.15s ease;
        border: 1px solid #e5e5e5;
        font-family: 'Outfit', sans-serif;
        padding: 0.6rem 1.5rem;
        letter-spacing: -0.01em;
    }

    .stButton>button:hover {
        border-color: #0077B5;
        background: #fafafa;
    }

    .stButton>button[kind="primary"] {
        background: #0077B5;
        color: white;
        border: 1px solid #0077B5;
    }

    .stButton>button[kind="primary"]:hover {
        background: #005a8a;
        border-color: #005a8a;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f8f8f7;
        border-right: 1px solid #e5e5e5;
    }

    [data-testid="stSidebar"] h2 {
        font-weight: 600;
        font-size: 1.1rem;
        color: #171717;
        letter-spacing: -0.01em;
    }

    [data-testid="stSidebar"] h3 {
        font-weight: 600;
        font-size: 0.95rem;
        color: #404040;
        letter-spacing: -0.01em;
    }

    /* Sidebar connection status - Round bubble boxes */
    [data-testid="stSidebar"] .stAlert {
        background: #ffffff !important;
        border: 1px solid #e8e8e6 !important;
        border-radius: 20px !important;
        padding: 0.8rem 1.2rem !important;
        color: #404040 !important;
        font-weight: 500 !important;
    }

    /* Input fields - Clean styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #0077B5;
        box-shadow: 0 0 0 1px #0077B5;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        color: #737373;
        font-size: 0.95rem;
        padding: 0.6rem 1.2rem;
    }

    .stTabs [aria-selected="true"] {
        color: #0077B5;
        font-weight: 600;
    }

    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0a0a0a;
    }

    [data-testid="stMetricLabel"] {
        color: #737373;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 2.5rem 0;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        font-weight: 500;
    }

    /* Remove default Streamlit padding on certain elements */
    .element-container {
        margin-bottom: 0.5rem;
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
    """Calculate quality score - use Editor Agent's score if available, otherwise calculate"""

    # Use Editor Agent's quality score if available (from Enhanced workflow)
    if "quality_score" in result and result.get("quality_score", 0) > 0:
        return result["quality_score"]

    # Fallback: Calculate score based on best practices
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
    """Create a clean, muted gauge chart for character count"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=char_count,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "Character Count",
            'font': {'size': 18, 'family': 'Outfit, sans-serif', 'color': '#404040'}
        },
        delta={
            'reference': 1200,
            'increasing': {'color': "#8b6b6b"},
            'font': {'size': 14, 'family': 'Outfit, sans-serif'}
        },
        number={
            'font': {'size': 48, 'family': 'Outfit, sans-serif', 'color': '#0a0a0a'}
        },
        gauge={
            'axis': {
                'range': [None, 1500],
                'tickwidth': 1,
                'tickcolor': "#d4d4d2",
                'tickfont': {'size': 11, 'color': '#737373', 'family': 'Outfit, sans-serif'}
            },
            'bar': {'color': "#0077B5", 'thickness': 0.7},
            'bgcolor': "#fafafa",
            'borderwidth': 1,
            'bordercolor': "#e8e8e6",
            'steps': [
                {'range': [0, 800], 'color': '#f5f3f3'},
                {'range': [800, 1300], 'color': '#f3f5f3'},
                {'range': [1300, 1500], 'color': '#f5f4f3'}
            ],
            'threshold': {
                'line': {'color': "#8b6b6b", 'width': 3},
                'thickness': 0.7,
                'value': 1400
            }
        }
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#404040", 'family': "Outfit, sans-serif"}
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


def run_workflow(input_data):
    """Run the 6-agent workflow with progress tracking"""
    try:
        st.session_state.progress = []
        add_progress("🚀 Starting", "active", f"Topic: {input_data['topic']}")
        add_log(f"Starting workflow for: {input_data['topic']}", "info")

        # Initialize the Enhanced 6-Agent Workflow
        workflow = LinkedInWorkflow()
        add_log("Using 6-Agent Workflow (Admin → Research → Strategist → Writer → Editor → Formatter)", "info")

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
    st.markdown('<div class="main-header">LinkedIn Content Engine</div>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-powered content generation with research & analytics</p>", unsafe_allow_html=True)
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
                        result = run_workflow(input_data)

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
                                    result = run_workflow(idea)

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

        # Tabs (add new tab for Enhanced workflow info)
        has_enhanced_data = result.get("content_strategy") or result.get("editor_feedback") or result.get("workflow_id")
        if has_enhanced_data:
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 Hooks", "✍️ Post", "📊 Analytics", "🔬 Research", "🎨 Visual", "🤖 Workflow"])
        else:
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

            # Display visual specs if available (from Formatter Agent)
            visual_specs = result.get('visual_specs', {})
            if visual_specs:
                st.markdown("---")
                st.markdown("#### 📐 Visual Specifications")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Format", visual_specs.get('format', 'N/A'))
                    st.metric("Aspect Ratio", visual_specs.get('aspect_ratio', 'N/A'))
                with col2:
                    if 'slides' in visual_specs:
                        st.metric("Slides", visual_specs.get('slides', 'N/A'))
                    if 'duration' in visual_specs:
                        st.metric("Duration", visual_specs.get('duration', 'N/A'))

                # Carousel outline
                if 'carousel_outline' in visual_specs:
                    st.markdown("**Carousel Outline:**")
                    for slide in visual_specs['carousel_outline']:
                        st.markdown(f"- {slide}")

                # Generation prompt for AI tools
                if 'generation_prompt' in visual_specs:
                    st.markdown("**AI Generation Prompt:**")
                    st.code(visual_specs['generation_prompt'], language="text")

            st.markdown("---")
            st.info("🚧 Visual generation coming soon! For now, use this suggestion to create your asset manually.")

        # New Workflow tab (only for Enhanced workflow)
        if has_enhanced_data:
            with tab6:
                st.markdown("### 🤖 Enhanced Workflow Details")

                # Workflow metadata
                if result.get("workflow_id"):
                    st.markdown("#### 📋 Workflow Metadata")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Workflow ID", result.get("workflow_id", "N/A"))
                    with col2:
                        st.metric("Duration", f"{result.get('duration_minutes', 0):.1f} min")
                    with col3:
                        st.metric("Revisions", result.get("revision_count", 0))

                    st.markdown("---")

                # Content Strategy (from Strategist Agent)
                strategy = result.get("content_strategy", {})
                if strategy:
                    st.markdown("#### 🎯 Content Strategy")

                    st.success(f"**Chosen Angle:** {strategy.get('chosen_angle', 'N/A')}")

                    if strategy.get("outline"):
                        st.markdown("**Outline:**")
                        for i, section in enumerate(strategy.get("outline", []), 1):
                            st.markdown(f"{i}. {section}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if strategy.get("structure_type"):
                            st.info(f"**Structure:** {strategy.get('structure_type').title()}")
                        if strategy.get("target_length"):
                            st.info(f"**Target Length:** {strategy.get('target_length')}")

                    with col2:
                        if strategy.get("hook_approach"):
                            st.info(f"**Hook Approach:** {strategy.get('hook_approach').title()}")

                    # Key points
                    if strategy.get("key_points"):
                        st.markdown("**Key Points:**")
                        for point in strategy.get("key_points", []):
                            st.markdown(f"- {point}")

                    st.markdown("---")

                # Editor Feedback
                if result.get("editor_feedback"):
                    st.markdown("#### 📝 Editor Feedback")

                    quality_score = result.get("quality_score", 0)
                    editor_decision = result.get("editor_decision", "unknown")

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("Quality Score", f"{quality_score}/100")
                        if editor_decision == "approve":
                            st.success("✅ Approved")
                        else:
                            st.warning("🔄 Revised")

                    with col2:
                        st.markdown("**Feedback:**")
                        st.text_area(
                            "Editor's assessment",
                            value=result.get("editor_feedback", ""),
                            height=150,
                            disabled=True,
                            label_visibility="collapsed"
                        )

                    st.markdown("---")

                # Pre-publish checklist (from Admin Agent)
                if result.get("checklist"):
                    st.markdown("#### ✅ Pre-Publish Checklist")

                    checklist = result.get("checklist", {})
                    passed = sum(checklist.values())
                    total = len(checklist)

                    st.progress(passed / total if total > 0 else 0)
                    st.markdown(f"**{passed}/{total} checks passed** ({int(passed/total*100) if total > 0 else 0}%)")

                    # Display checks
                    col1, col2 = st.columns(2)
                    items = list(checklist.items())
                    mid = len(items) // 2

                    with col1:
                        for key, value in items[:mid]:
                            if value:
                                st.success(f"✅ {key.replace('_', ' ').title()}")
                            else:
                                st.error(f"❌ {key.replace('_', ' ').title()}")

                    with col2:
                        for key, value in items[mid:]:
                            if value:
                                st.success(f"✅ {key.replace('_', ' ').title()}")
                            else:
                                st.error(f"❌ {key.replace('_', ' ').title()}")

                # Agent pipeline visualization
                st.markdown("---")
                st.markdown("#### 🔄 Agent Pipeline")

                pipeline_html = """
                <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 1.5rem; border-radius: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #0077B5; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">🔍</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Admin</div>
                        </div>
                        <div style="color: #0077B5; font-size: 1.5rem;">→</div>
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #00A0DC; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">📚</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Research</div>
                        </div>
                        <div style="color: #0077B5; font-size: 1.5rem;">→</div>
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #0077B5; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">🎯</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Strategist</div>
                        </div>
                        <div style="color: #0077B5; font-size: 1.5rem;">→</div>
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #00A0DC; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">✍️</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Writer</div>
                        </div>
                        <div style="color: #0077B5; font-size: 1.5rem;">→</div>
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #0077B5; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">📝</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Editor</div>
                        </div>
                        <div style="color: #0077B5; font-size: 1.5rem;">→</div>
                        <div style="text-align: center; margin: 0.5rem;">
                            <div style="background: #00A0DC; color: white; padding: 1rem; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 1.5rem;">✨</div>
                            <div style="margin-top: 0.5rem; font-weight: 600;">Formatter</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(pipeline_html, unsafe_allow_html=True)

        # History section
        if len(st.session_state.history) > 1:
            st.markdown("---")
            with st.expander(f"📜 Session History ({len(st.session_state.history)} posts)"):
                for idx, item in enumerate(reversed(st.session_state.history), 1):
                    st.markdown(f"**{idx}. {item['topic']}** ({item['goal']}) - {item['timestamp'].strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
