# 🚀 Quick Start Guide

Get your LinkedIn Content Engine running in 5 minutes.

---

## Prerequisites

- Python 3.10+ installed
- API keys ready (see below)
- Notion database set up (same as n8n workflow)

---

## Step 1: Install Python Dependencies (2 minutes)

```bash
# Navigate to the project folder
cd d:\Claude Code Projects\Random\linkedin-agent-workflow

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

You should see packages installing (langgraph, langchain, anthropic, etc.)

---

## Step 2: Configure Environment Variables (2 minutes)

### Copy the example file:
```bash
# On Windows:
copy .env.example .env
# On Mac/Linux:
# cp .env.example .env
```

### Edit `.env` file with your API keys:

Open `.env` in any text editor and fill in:

```env
# Notion (same as your n8n workflow)
NOTION_TOKEN=secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
NOTION_DATABASE_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Tavily (same as your n8n workflow)
TAVILY_API_KEY=tvly-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# OpenRouter (same as your n8n workflow!)
OPENROUTER_API_KEY=sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Slack (optional - for notifications)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WORKSPACE/YOUR_CHANNEL/YOUR_TOKEN
```

**Important:** This uses **OpenRouter** (same as your n8n workflow). Uses `anthropic/claude-3.5-sonnet` model via OpenRouter.

---

## Step 3: Test with a Single Run (1 minute)

```bash
python main.py single
```

### What happens:
1. ✅ Script checks for environment variables
2. 🔍 Queries Notion for entries with Status = "Idea"
3. 📊 Runs research → writing workflow
4. 💾 Updates Notion with results
5. 📬 Sends Slack notification

### Expected output:
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

---

## Step 4: Check Results

### In Notion:
1. Open your LinkedIn Content database
2. Find the entry you just processed
3. Status should be **"Ready"**
4. Check these fields are filled:
   - ✅ Research Brief
   - ✅ Hook Option 1, 2, 3
   - ✅ Draft Body
   - ✅ CTA
   - ✅ Hashtags
   - ✅ Image Suggestion

### In Slack:
- Check your channel for a notification with draft preview

---

## Step 5: Run Continuously (Optional)

Once testing works, run in continuous mode:

```bash
# Poll every 2 minutes (default)
python main.py continuous

# Or custom interval (300 seconds = 5 minutes)
python main.py continuous 300
```

Press `Ctrl+C` to stop.

---

## Troubleshooting

### Error: "Missing required environment variables"

**Fix:** Check your `.env` file has all required keys (no placeholders like `YOUR_API_KEY`)

```bash
# Test if env vars load correctly:
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Anthropic:', os.getenv('ANTHROPIC_API_KEY')[:20])"
```

### Error: "No module named 'langgraph'"

**Fix:** Make sure virtual environment is activated and packages installed:

```bash
# Activate venv first
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Then install
pip install -r requirements.txt
```

### Error: "No new ideas found with status 'Idea'"

**Fix:** Add a test entry to Notion:

1. Open your Notion database
2. Click "+ New"
3. Fill in:
   - **Name:** "Test post about AI trends"
   - **Goal:** Thought Leadership
   - **Context/Notes:** "Focus on recent developments"
   - **Status:** **Idea** (important!)

### Error: "401 Unauthorized" from Notion

**Fix:**
1. Check your `NOTION_TOKEN` is correct
2. Make sure your Notion database is shared with the integration
3. Verify `NOTION_DATABASE_ID` is 32 characters (no dashes)

### Error: "401 Unauthorized" from OpenRouter

**Fix:**
1. Get API key from: https://openrouter.ai/settings/keys
2. Make sure it starts with `sk-or-v1-`
3. Check you have credits in your OpenRouter account

### Workflow runs but output is empty

**Fix:** Check LangGraph workflow selection in `main.py`:

```python
# Line 16 in main.py - try the simple workflow first:
workflow = LinkedInWorkflow()  # Simple sequential

# Once working, switch to adaptive:
# workflow = AdaptiveLinkedInWorkflow()
```

---

## What's Different from n8n?

| n8n | LangGraph (This) |
|-----|------------------|
| OpenRouter API | OpenRouter API (same!) |
| Runs every 2 min (cron) | Runs every 2 min (Python loop) |
| Visual workflow editor | Code-based workflow |
| Fixed sequence | Adaptive with quality checks |
| Inline prompts | Production-grade structured prompts |

---

## Next Steps

Once your first run succeeds:

1. ✅ **Try the adaptive workflow** (edit `main.py` line 16)
2. ✅ **Customize prompts** (see [prompts/README.md](prompts/README.md))
3. ✅ **Adjust quality thresholds** (see [README.md](README.md) customization section)
4. ✅ **Compare output** with your n8n workflow
5. ✅ **Add more ideas** to Notion and watch them process automatically

---

## Getting Help

**Check logs first:** The script prints detailed progress messages

**Common fixes:**
- Restart virtual environment: `deactivate` then `venv\Scripts\activate`
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`
- Verify Notion database properties match exactly (case-sensitive)

**Still stuck?** Review the full [README.md](README.md) for detailed troubleshooting.

---

## Cost Estimate

Running this workflow:

- **OpenRouter (Claude 3.5 Sonnet):** ~$0.015-0.03 per post (research + writing)
- **Tavily:** Free (1,000 searches/month)
- **Notion:** Free
- **Slack:** Free

**Total:** ~$5-10/month for 300-500 posts

**Same cost as your n8n workflow!** Uses the same OpenRouter account and Claude 3.5 Sonnet model.

---

**You're all set! 🎉**

Run `python main.py single` and watch the magic happen.
