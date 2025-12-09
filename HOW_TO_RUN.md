# 🚀 How to Run - Simple Guide

Three ways to run your LinkedIn Content Engine:

---

## Option 1: Windows Quick Run (Easiest)

### First Time Setup:
```bash
# 1. Double-click or run:
setup.bat

# 2. Edit .env file with your API keys (same as n8n!)

# 3. Run a test:
run.bat single
```

### After Setup:
```bash
# Test single run:
run.bat single

# Run continuously (every 2 minutes):
run.bat continuous

# Run continuously (custom interval - 5 minutes):
run.bat continuous 300
```

---

## Option 2: Manual Setup (Any OS)

```bash
# 1. Create virtual environment
cd linkedin-agent-workflow
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Copy and edit .env
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env with your API keys

# 5. Run
python main.py single          # Test run
python main.py continuous      # Every 2 min
python main.py continuous 300  # Every 5 min
```

---

## Option 3: One-Line Test (After Setup)

```bash
venv\Scripts\activate && python main.py single
```

---

## ✅ What You Need

All the same keys from your n8n workflow:

| Variable | Where to Get It | Same as n8n? |
|----------|----------------|--------------|
| `NOTION_TOKEN` | Notion integration | ✅ Yes |
| `NOTION_DATABASE_ID` | Notion database URL | ✅ Yes |
| `TAVILY_API_KEY` | app.tavily.com | ✅ Yes |
| `OPENROUTER_API_KEY` | openrouter.ai/settings/keys | ✅ Yes |
| `SLACK_WEBHOOK_URL` | Slack webhook | ✅ Yes |

**No new accounts needed!** Use your existing API keys.

---

## 📋 Quick Checklist

Before running:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and filled
- [ ] At least one Notion entry with Status = "Idea"

---

## 🧪 Test Run

```bash
# Activate environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Run once
python main.py single
```

**Expected output:**
```
============================================================
🚀 Starting LinkedIn Content Workflow
📝 Topic: Your topic name
🎯 Goal: Thought Leadership
============================================================

🔍 Researching: Your topic name
📊 Found 5 sources
✅ Research complete (1234 chars)
✍️  Writing post for: Your topic name
✅ Draft generated with 3 hooks
✅ Updated with research brief
✅ Updated with complete draft
✅ Slack notification sent

============================================================
🎉 SUCCESS! Draft is ready in Notion
============================================================
```

---

## 🐛 Common Issues

### "python: command not found"
**Fix:** Use `python3` instead of `python`

### "cannot activate venv"
**Fix (Windows):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Missing required environment variables"
**Fix:**
1. Check `.env` file exists
2. Verify no placeholders like `YOUR_API_KEY`
3. Restart terminal after editing `.env`

### "No new ideas found"
**Fix:** Add test entry to Notion with Status = **"Idea"** (exact spelling)

---

## 📂 Where Everything Is

```
linkedin-agent-workflow/
├── agents/
│   ├── research_agent.py    ← Edit prompts here
│   └── writer_agent.py       ← Edit prompts here
├── main.py                   ← Main script
├── .env                      ← Your API keys (DO NOT COMMIT!)
├── setup.bat                 ← Windows setup script
└── run.bat                   ← Windows run script
```

---

## 🎯 What It Does

1. ✅ Polls Notion every X minutes
2. ✅ Finds entries with Status = "Idea"
3. ✅ Researches topic with Tavily
4. ✅ Synthesizes research with Claude (via OpenRouter)
5. ✅ Generates 3 hooks + post body with Claude
6. ✅ Updates Notion with results
7. ✅ Sends Slack notification
8. ✅ Changes Status to "Ready"

---

## 💡 Tips

**For testing:**
```bash
python main.py single
```

**For production:**
```bash
python main.py continuous
```

**Keep it running:**
- Windows: Use Task Scheduler
- Mac/Linux: Use cron or systemd
- Cloud: Deploy to AWS Lambda or Google Cloud Run

---

## 🆘 Need Help?

1. Check [QUICKSTART.md](QUICKSTART.md) for detailed troubleshooting
2. Review [README.md](README.md) for full documentation
3. See [prompts/README.md](prompts/README.md) for customizing agents

---

**Ready? Run this:**

```bash
setup.bat              # First time only
run.bat single         # Test it
run.bat continuous     # Let it run!
```
