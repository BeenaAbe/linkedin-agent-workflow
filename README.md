# LinkedIn Content Engine - LangGraph Multi-Agent System

An intelligent multi-agent system for automating LinkedIn content creation using LangGraph, Claude, and Tavily.

## 🌟 Key Advantages Over n8n Workflow

### **Agentic Features**
- ✅ **Adaptive Research**: Automatically conducts additional research if initial results are insufficient
- ✅ **Quality Checks**: Validates post length and completeness before finishing
- ✅ **Self-Correction**: Regenerates content that doesn't meet quality standards
- ✅ **Dynamic Routing**: Workflow adapts based on intermediate results

### **Better for Complex Logic**
- ✅ **Conditional branching** based on content quality
- ✅ **Loop-back mechanisms** for iterative improvement
- ✅ **State management** across agents
- ✅ **Error recovery** and retry logic

---

## 📁 Project Structure

```
linkedin-agent-workflow/
├── agents/
│   ├── research_agent.py    # Tavily + Claude research (PRODUCTION-READY PROMPTS ⭐)
│   └── writer_agent.py       # LinkedIn ghostwriter (DETAILED PROMPTS ⭐)
├── integrations/
│   ├── notion_client.py      # Notion API wrapper
│   └── slack_notifier.py     # Slack notifications
├── prompts/
│   └── README.md             # 📖 Complete prompt engineering guide
├── workflow.py               # LangGraph orchestrator (Simple + Adaptive modes)
├── main.py                   # Command-line execution script
├── streamlit_app.py          # Web UI interface
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .streamlit/
│   └── secrets.toml.example  # Streamlit Cloud secrets template
└── README.md                # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ installed
- API keys from Notion, Tavily, and OpenRouter
- Notion database set up (see [SECURITY.md](SECURITY.md) for setup)

### 1. Install Dependencies

```bash
# Navigate to project directory
cd linkedin-agent-workflow

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Keys 🔑

**Copy the example environment file:**

```bash
# On Windows:
copy .env.example .env
# On Mac/Linux:
cp .env.example .env
```

**Edit `.env` with your API keys:**

```env
# Notion
NOTION_TOKEN=secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
NOTION_DATABASE_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Tavily (web search)
TAVILY_API_KEY=tvly-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# OpenRouter (for Claude access)
OPENROUTER_API_KEY=sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Slack (optional - for notifications)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WORKSPACE/YOUR_CHANNEL/YOUR_TOKEN
```

**Where to get API keys:**

| Key | Get It Here | Format |
|-----|-------------|--------|
| `NOTION_TOKEN` | https://www.notion.so/my-integrations | `secret_...` |
| `NOTION_DATABASE_ID` | Notion database URL (32 chars) | No dashes |
| `TAVILY_API_KEY` | https://app.tavily.com | `tvly-...` |
| `OPENROUTER_API_KEY` | https://openrouter.ai/settings/keys | `sk-or-v1-...` |
| `SLACK_WEBHOOK_URL` | Slack app settings | Full URL |

**⚠️ Security:** Your `.env` file is protected by `.gitignore` and will never be committed to Git. See [SECURITY.md](SECURITY.md) for full security details.

### 3. Run the Workflow

**Option A: Command Line**

```bash
# Test with single run (no change detection)
python main.py single

# Process all pending ideas immediately
python main.py batch

# Run continuously with smart polling (default: 30s idle, 5s when active)
python main.py continuous

# Custom polling interval (in seconds)
python main.py continuous 15  # Poll every 15 seconds when idle
```

**Smart Polling Features:**
- ⚡ **Instant batch processing**: When multiple ideas are added, processes all within seconds
- 📅 **Change detection**: Only queries ideas created since last check
- 🔄 **Adaptive timing**: Fast (5s) when active, slower (30s) when idle
- 💾 **Persistent state**: Tracks last processed time across restarts

**Option B: Web Interface (Streamlit)**

```bash
# Start the Streamlit web UI
streamlit run streamlit_app.py
```

The app will open at http://localhost:8501 with:
- **Manual Mode**: Test with custom input
- **Notion Mode**: Process ideas from your database
- **Real-time progress tracking**
- **Interactive results display**

---

## 🔄 How It Works

### Simple Sequential Workflow (`LinkedInWorkflow`)

```
[Notion Idea] → [Research Agent] → [Writer Agent] → [Notion Update] → [Slack]
```

1. **Research Agent**:
   - Searches web with Tavily
   - Synthesizes insights with Claude

2. **Writer Agent**:
   - Generates 3 hook options
   - Writes post body
   - Suggests visuals

### Adaptive Workflow (`AdaptiveLinkedInWorkflow`)

```
[Notion Idea] → [Research] ──→ [Quality Check] ──→ [Write] ──→ [Quality Check] ──→ [Done]
                    ↑              │                   ↑              │
                    └──────────────┘                   └──────────────┘
                   (loop if too short)             (loop if incomplete)
```

**Features:**
- **Research Quality Check**: Loops back if research brief is too short (<500 chars)
- **Writing Quality Check**: Regenerates if post is too short (<200 chars) or missing hooks
- **Self-improving**: Can iterate multiple times until quality standards are met

**Switch workflow types in `main.py` line 20:**

```python
# Simple workflow
workflow = LinkedInWorkflow()

# OR adaptive workflow (default - recommended)
workflow = AdaptiveLinkedInWorkflow()
```

---

## 🧪 Testing with Sample Data

### 1. Add a Test Entry to Notion

In your Notion database, create:
- **Name:** "Why most AI agents are just fancy chatbots"
- **Goal:** Thought Leadership
- **Context/Notes:** "Lead with the 83% Gartner stat. Contrast chatbots vs real agents."
- **Status:** **Idea**

### 2. Run a Test

```bash
python main.py single
```

### 3. Expected Output

```
============================================================
🚀 Starting LinkedIn Content Workflow
📝 Topic: Why most AI agents are just fancy chatbots
🎯 Goal: Thought Leadership
============================================================

🔍 Researching: Why most AI agents are just fancy chatbots
📊 Found 5 sources
✅ Research complete (1234 chars)
✍️  Writing post for: Why most AI agents are just fancy chatbots
✅ Draft generated with 3 hooks

============================================================
🎉 SUCCESS! Draft is ready in Notion
============================================================
```

### 4. Check Results

**In Notion:**
- Status should be "Ready"
- All fields filled:
  - ✅ Research Brief
  - ✅ Hook Option 1, 2, 3
  - ✅ Draft Body
  - ✅ CTA
  - ✅ Hashtags
  - ✅ Image Suggestion

**In Slack:**
- Notification with draft preview

---

## 📊 What Gets Generated

The workflow creates:

- ✅ **3 Hook Options**: Controversial, Question, and Story hooks
- ✅ **Post Body**: 200-1,500 character LinkedIn post with proper formatting
- ✅ **Call-to-Action**: Goal-specific engagement prompt
- ✅ **Hashtags**: 3-5 relevant tags (mix of broad and niche)
- ✅ **Visual Suggestion**: Carousel, video, photo, or poll recommendation
- ✅ **Format Type**: Content format based on goal type

---

## 🔧 Customization & Prompts

### 📖 Complete Prompt Engineering Guide

See [prompts/README.md](prompts/README.md) for the full guide on:
- How to customize research strategies by goal type
- Adjusting hook formulas and writing style
- Adding few-shot examples
- Temperature/token settings
- Debugging prompt issues
- Multi-model strategies

### Production-Ready Prompts Included ⭐

**Research Agent** ([agents/research_agent.py](agents/research_agent.py)) features:
- ✅ Goal-specific research strategies (6 types: Thought Leadership, Product, Educational, Personal Brand, Interactive, Inspirational)
- ✅ Source quality hierarchy (Academic > Industry reports > News)
- ✅ Citation discipline (URLs + dates mandatory)
- ✅ Contrarian angle detection
- ✅ Structured JSON output with validation

**Writer Agent** ([agents/writer_agent.py](agents/writer_agent.py)) features:
- ✅ 3 hook formulas (Controversial, Question, Story)
- ✅ Goal-specific CTAs (6 types)
- ✅ Visual asset recommendations by goal
- ✅ LinkedIn best practices (character limits, formatting, hashtags)
- ✅ Platform rule enforcement (no external links, 1,500 char limit)

### Quick Customization Examples

**Adjust Research Depth:**
```python
# In agents/research_agent.py, line 117
search_results = self.tavily.search(
    query=query,
    search_depth="advanced",  # or "basic"
    max_results=10,           # Increase for more sources
    include_answer=True
)
```

**Change Writing Temperature:**
```python
# In agents/writer_agent.py, line 18
temperature=0.7,  # Higher (0.9) = more creative, Lower (0.4) = more consistent
```

**Adjust Quality Thresholds:**
```python
# In workflow.py, AdaptiveLinkedInWorkflow
def _should_research_more(self, state):
    research = state.get("research_brief", "")
    if len(research) < 1000:  # Increase for more thorough research
        return "research"
    return "write"
```

---

## 🌐 Streamlit Web Interface

### Running Locally

```bash
streamlit run streamlit_app.py
```

Opens at http://localhost:8501

### Features

- **Manual Mode**: Test with custom topics
- **Notion Mode**: Process ideas from database automatically
- **Real-time Logs**: Activity tracking in sidebar
- **Interactive Results**: Tabbed view with hooks, post, research, visual suggestions
- **Download Options**: Export complete post as text file

### Deploying to Streamlit Cloud (Free)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add enhanced UI with smart polling"
   git push origin main
   ```

2. **Go to Streamlit Cloud:** https://share.streamlit.io

3. **Create new app**
   - Repository: `your-username/linkedin-agent-workflow`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Add secrets** (Settings > Secrets)
   ```toml
   NOTION_TOKEN = "secret_YOUR_TOKEN"
   NOTION_DATABASE_ID = "YOUR_32_CHAR_ID"
   TAVILY_API_KEY = "tvly-YOUR_KEY"
   OPENROUTER_API_KEY = "sk-or-v1-YOUR_KEY"
   SLACK_WEBHOOK_URL = "https://hooks.slack.com/YOUR_URL"
   ```

5. **Deploy** - Live at `your-app.streamlit.app`

**Note:** The enhanced UI with LinkedIn branding, hook cards, analytics, and smart features will work automatically on Streamlit Cloud!

---

## 🆚 n8n vs LangGraph Comparison

| Feature | n8n Workflow | LangGraph Workflow |
|---------|-------------|-------------------|
| **Setup** | Visual UI, easier | Code-based, more control |
| **Prompts** | Inline strings | ⭐ Production-grade, structured |
| **Conditional Logic** | Limited | Full Python logic |
| **Quality Checks** | Manual nodes | Built-in adaptive loops |
| **Error Handling** | Basic retry | Smart recovery |
| **Adaptability** | Fixed sequence | Dynamic routing |
| **Testing** | Manual execution | Unit testable |
| **Prompt Version Control** | Manual copy/paste | Git-tracked, diffable |
| **Local Development** | Needs n8n server | Pure Python |
| **Cost** | n8n cloud $20/mo | Just API costs (~$5/mo) |
| **Prompt Customization** | Edit each node | Centralized in agent files |

---

## 🚀 Smart Polling & Batch Processing

### How It Works

The workflow now includes **smart polling** with **change detection** for instant responsiveness:

1. **First Run**: Processes all pending ideas with status "Idea"
2. **Subsequent Runs**: Only queries ideas created after the last processed timestamp
3. **Batch Detection**: When ideas are found, quickly rechecks (5s) for more
4. **Idle Mode**: When no ideas found, waits longer (30s default) before next check

**State File**: `.last_processed` tracks the timestamp of the last check (gitignored)

### Usage Modes

| Mode | Command | Use Case |
|------|---------|----------|
| **Single** | `python main.py single` | Test one idea (no timestamp tracking) |
| **Batch** | `python main.py batch` | Process all pending ideas immediately |
| **Continuous** | `python main.py continuous` | Smart polling (30s idle, 5s active) |
| **Fast Continuous** | `python main.py continuous 10` | Very responsive (10s idle, 5s active) |

### Response Time Examples

**Scenario 1: Add 3 ideas at once**
- First idea: Detected within 30s (or less if already polling)
- Ideas 2-3: Detected within 5s after first completes
- Total time: ~35s + processing time

**Scenario 2: Add ideas throughout the day**
- Each idea: Detected within 30s max
- Change detection prevents re-processing old ideas

**Scenario 3: Urgent batch**
- Run `python main.py batch` to process all immediately
- No waiting for polling interval

## 🐛 Troubleshooting

### "Missing required environment variables"

**Fix:** Check your `.env` file exists and has all required keys (no placeholders like `YOUR_API_KEY`)

```bash
# Test if env vars load correctly
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenRouter:', os.getenv('OPENROUTER_API_KEY')[:20])"
```

### "No module named 'langgraph'"

**Fix:** Make sure virtual environment is activated and packages installed

```bash
# Activate venv first
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Then install
pip install -r requirements.txt
```

### "No new ideas found with status 'Idea'"

**Fix:** Add a test entry to Notion with Status = **"Idea"** (exact spelling, case-sensitive)

### "401 Unauthorized" from Notion

**Fix:**
1. Check your `NOTION_TOKEN` is correct
2. Make sure your Notion database is shared with the integration
3. Verify `NOTION_DATABASE_ID` is 32 characters (no dashes)

### "401 Unauthorized" from OpenRouter

**Fix:**
1. Get API key from https://openrouter.ai/settings/keys
2. Make sure it starts with `sk-or-v1-`
3. Check you have credits in your OpenRouter account

### Workflow Loops Forever

**Fix:** Check quality thresholds in `workflow.py`. If too strict, it may never pass:

```python
# Lower threshold for testing
if len(research) < 100:  # Instead of 500
```

### Notion 404 Errors

**Fix:**
1. Share database with your integration
2. Check database ID is correct (32 chars)
3. Verify property names match exactly (case-sensitive)

### Import Errors

**Fix:** Make sure you're in the virtual environment:

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

## 📈 Monitoring & Costs

### API Usage & Costs

- **OpenRouter (Claude 3.5 Sonnet)**: ~$0.015-0.03 per post
- **Tavily**: Free for 1,000 searches/month
- **Notion**: Free
- **Slack**: Free

**Total**: ~$5-10/month for 300-500 posts

### Workflow Logs

The workflow prints detailed logs:

```
🔍 Researching: [topic]
📊 Found 5 sources
✅ Research complete (1234 chars)
✍️  Writing post for: [topic]
✅ Draft generated with 3 hooks
```

---

## 💡 Advanced Features

### 1. Human-in-the-Loop

Add approval step before publishing:

```python
def _needs_approval(state) -> str:
    # Pause workflow and wait for approval
    approval = input("Approve this draft? (y/n): ")
    return "publish" if approval == "y" else "write"
```

### 2. Multi-Model Testing

Try different models for different tasks:

```python
# Fast model for research
research_llm = ChatOpenAI(
    model="anthropic/claude-3-haiku",
    openai_api_base="https://openrouter.ai/api/v1"
)

# Best model for writing
writer_llm = ChatOpenAI(
    model="anthropic/claude-3.5-sonnet",
    openai_api_base="https://openrouter.ai/api/v1"
)
```

### 3. A/B Testing

Generate multiple versions and track performance:

```python
workflow.add_node("generate_variants", create_ab_test_versions)
```

### 4. Scheduled Publishing

Integrate with LinkedIn API to auto-post at optimal times.

---

## 🔒 Security

All API keys are stored securely:

- ✅ **Local Development:** `.env` file (gitignored, never committed)
- ✅ **Streamlit Cloud:** Secrets dashboard (encrypted)
- ✅ **GitHub:** Only `.env.example` with placeholders

**Before pushing to Git, always verify:**

```bash
git status
# Make sure .env is NOT listed
```

See [SECURITY.md](SECURITY.md) for complete security documentation.

---

## 🎉 Next Steps

1. ✅ **Test the basic workflow** with `python main.py single`
2. ✅ **Try the adaptive workflow** and watch it self-correct
3. ✅ **Launch Streamlit UI** with `streamlit run streamlit_app.py`
4. ✅ **Customize prompts** to match your writing style ([prompts/README.md](prompts/README.md))
5. ✅ **Add custom quality checks** for your specific needs
6. ✅ **Deploy to Streamlit Cloud** for team access

---

## 📚 Documentation

- **[SECURITY.md](SECURITY.md)**: Complete security and API key setup guide
- **[prompts/README.md](prompts/README.md)**: Prompt engineering and customization guide
- **[Future plan](Future%20plan)**: Upcoming UI enhancements and features

---

## 🆘 Support

For issues or questions:
1. Check the logs for specific error messages
2. Verify all environment variables are set correctly
3. Test each API separately to isolate issues
4. Review the LangGraph docs: https://langchain-ai.github.io/langgraph/

---

## 📄 License

MIT License - feel free to modify and extend!

---

**Happy automating! 🚀**
