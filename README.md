# LinkedIn Content Engine - LangGraph Multi-Agent Version

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
├── main.py                   # Main execution script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd linkedin-agent-workflow
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
NOTION_TOKEN=secret_YOUR_NOTION_INTEGRATION_TOKEN
NOTION_DATABASE_ID=YOUR_32_CHARACTER_DATABASE_ID
TAVILY_API_KEY=tvly-YOUR_TAVILY_KEY
ANTHROPIC_API_KEY=sk-ant-YOUR_ANTHROPIC_KEY
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. Run the Workflow

**Single execution (for testing):**
```bash
python main.py single
```

**Continuous mode (polls every 2 minutes):**
```bash
python main.py continuous
```

**Custom polling interval (in seconds):**
```bash
python main.py continuous 300  # Poll every 5 minutes
```

---

## 🔄 Workflow Explained

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

---

## 🎯 How to Switch Workflow Types

Edit `main.py` line 16:

```python
# Simple workflow
workflow = LinkedInWorkflow()

# OR adaptive workflow (default)
workflow = AdaptiveLinkedInWorkflow()
```

---

## 🧪 Testing

### Test with a Sample Idea

1. **Add to Notion:**
   - Name: "Why most AI agents are just fancy chatbots"
   - Goal: Thought Leadership
   - Context: "Lead with the 83% Gartner stat. Contrast chatbots vs real agents."
   - Status: **Idea**

2. **Run:**
   ```bash
   python main.py single
   ```

3. **Check Results:**
   - Notion status should be "Ready"
   - All hooks and draft body filled
   - Slack notification received

---

## 📊 What Gets Generated

The workflow creates:

- ✅ **3 Hook Options**: Different opening lines to test
- ✅ **Post Body**: 200-500 word LinkedIn post
- ✅ **Call-to-Action**: Engagement prompt
- ✅ **Hashtags**: Relevant tags (3-5)
- ✅ **Visual Suggestion**: What image/carousel to create
- ✅ **Format Type**: text, carousel, infographic, or video

---

## 🔧 Customization & Prompts

### 📖 **Complete Prompt Engineering Guide**

See [prompts/README.md](prompts/README.md) for the full guide on:
- How to customize research strategies by goal type
- Adjusting hook formulas and writing style
- Adding few-shot examples
- Temperature/token settings
- Debugging prompt issues
- Multi-model strategies

### Production-Ready Prompts Included ⭐

Both agents include detailed, production-ready prompts:

**Research Agent** features:
- ✅ Goal-specific research strategies (6 types: Thought Leadership, Product, Educational, Personal Brand, Interactive, Inspirational)
- ✅ Source quality hierarchy (Academic > Industry reports > News)
- ✅ Citation discipline (URLs + dates mandatory)
- ✅ Contrarian angle detection
- ✅ Structured JSON output with validation

**Writer Agent** features:
- ✅ 3 hook formulas (Controversial, Question, Story)
- ✅ Goal-specific CTAs (6 types)
- ✅ Visual asset recommendations by goal
- ✅ LinkedIn best practices (character limits, formatting, hashtags)
- ✅ Platform rule enforcement (no external links, 1,500 char limit)

### Quick Customization Examples

**Adjust Research Depth:**
```python
# In agents/research_agent.py, line 50
search_results = self.tavily.search(
    query=query,
    search_depth="advanced",  # or "basic"
    max_results=10,           # More sources
    include_answer=True
)
```

**Change Writing Temperature:**
```python
# In agents/writer_agent.py, line 15
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

## 💡 Advanced Features to Add

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
research_llm = ChatAnthropic(model="claude-3-haiku-20240307")

# Best model for writing
writer_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

### 3. A/B Testing

Generate multiple versions and track performance:

```python
workflow.add_node("generate_variants", create_ab_test_versions)
```

### 4. Scheduled Publishing

Integrate with LinkedIn API to auto-post at optimal times.

---

## 🐛 Troubleshooting

### Import Errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### API Errors

Check your `.env` file:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Notion 404 Errors

Verify database access:
1. Share database with your integration
2. Check database ID is correct (32 chars)
3. Verify property names match exactly (case-sensitive)

### Workflow Loops Forever

Check quality thresholds in `workflow.py`. If too strict, it may never pass:

```python
if len(research) < 100:  # Lower threshold for testing
```

---

## 📈 Monitoring & Costs

### API Usage

- **Claude (via Anthropic)**: ~$0.015-0.03 per post
- **Tavily**: Free for 1,000 searches/month
- **Notion**: Free
- **Slack**: Free

**Total**: ~$5-10/month for 300-500 posts

### Logs

The workflow prints detailed logs:
```
🔍 Researching: [topic]
📊 Found 5 sources
✅ Research complete (1234 chars)
✍️  Writing post for: [topic]
✅ Draft generated with 3 hooks
```

---

## 🎉 Next Steps

1. **Test the basic workflow** with `python main.py single`
2. **Try the adaptive workflow** and watch it self-correct
3. **Customize prompts** to match your writing style
4. **Add custom quality checks** for your specific needs
5. **Integrate with LinkedIn API** for auto-publishing

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
