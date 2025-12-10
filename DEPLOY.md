# 🚀 Streamlit Cloud Deployment Guide

## Pre-Deployment Checklist

Before pushing to GitHub, verify these files:

### ✅ Files to Commit
- [x] `streamlit_app.py` - Enhanced UI with modern design
- [x] `requirements.txt` - Lightweight dependencies (no streamlit-extras)
- [x] `.streamlit/config.toml` - Theme configuration
- [x] `.streamlit/secrets.toml.example` - Secrets template
- [x] `.gitignore` - Excludes `.env`, `venv/`, `.last_processed`
- [x] All agent files (`agents/`, `integrations/`, `workflow.py`, `main.py`)
- [x] `README.md` - Updated documentation

### ❌ Files to NEVER Commit
- [ ] `.env` - Contains actual API keys (gitignored)
- [ ] `.streamlit/secrets.toml` - Actual secrets (gitignored)
- [ ] `venv/` - Virtual environment (gitignored)
- [ ] `.last_processed` - State file (gitignored)
- [ ] `__pycache__/` - Python cache (gitignored)

---

## Step 1: Verify Git Status

```bash
cd "d:\Claude Code Projects\Random\linkedin-agent-workflow"
git status
```

**Expected output:** Should NOT see `.env` or `venv/` in the list

---

## Step 2: Commit and Push

```bash
# Add all changes
git add .

# Check what will be committed
git status

# Commit with descriptive message
git commit -m "Add enhanced UI with smart polling and analytics"

# Push to GitHub
git push origin main
```

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Go to Streamlit Cloud
https://share.streamlit.io

### 3.2 Create New App
Click **"New app"** button

### 3.3 Configuration
- **Repository:** Select your GitHub repo
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`
- Click **"Advanced settings"** if needed (usually not required)

### 3.4 Add Secrets
Click **"Advanced settings"** > **"Secrets"**

Paste your API keys in TOML format:
```toml
NOTION_TOKEN = "secret_YOUR_ACTUAL_TOKEN_HERE"
NOTION_DATABASE_ID = "YOUR_32_CHARACTER_DATABASE_ID"
TAVILY_API_KEY = "tvly-YOUR_ACTUAL_KEY_HERE"
OPENROUTER_API_KEY = "sk-or-v1-YOUR_ACTUAL_KEY_HERE"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Note:** Replace ALL placeholder values with your actual API keys from your `.env` file

### 3.5 Deploy
Click **"Deploy!"**

Wait 2-3 minutes for deployment to complete

---

## Step 4: Access Your App

Your app will be live at:
```
https://[your-app-name].streamlit.app
```

Example: `https://linkedin-content-engine.streamlit.app`

---

## Features Available on Streamlit Cloud

✅ **Enhanced UI Features:**
- LinkedIn-branded gradient header
- Beautiful hook cards with color-coded badges
- One-click clipboard copy
- Real-time character counter
- Quality score analytics
- LinkedIn mobile preview
- Plotly charts (character gauge)
- Session history tracking
- Notion queue preview
- Activity logs

✅ **Three Modes:**
- Manual Input (test with custom topics)
- Notion Integration (pull from database)
- Batch Preview (view pending ideas)

✅ **Analytics Dashboard:**
- Quality score (0-100)
- Character count gauge
- Content breakdown metrics
- Smart suggestions

---

## Troubleshooting

### Issue: "Missing environment variables"
**Solution:** Check that all secrets are added correctly in Streamlit Cloud dashboard (Settings > Secrets)

### Issue: "Module not found"
**Solution:** Verify `requirements.txt` is committed and contains all dependencies

### Issue: App crashes on startup
**Solution:** Check logs in Streamlit Cloud (click "Manage app" > "Logs")

### Issue: Notion connection fails
**Solution:**
1. Verify `NOTION_TOKEN` and `NOTION_DATABASE_ID` are correct
2. Ensure Notion integration has access to your database
3. Database ID should be 32 characters (no dashes)

### Issue: OpenRouter errors
**Solution:**
1. Check API key starts with `sk-or-v1-`
2. Verify you have credits in your OpenRouter account
3. Test API key manually: https://openrouter.ai/settings/keys

---

## Local Testing Before Deploy

Test locally to catch issues before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run streamlit_app.py
```

Should open at: http://localhost:8501

---

## Updating Your Deployment

After making changes:

```bash
# Commit changes
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will auto-deploy within 1-2 minutes

---

## Cost

- **Streamlit Cloud:** Free tier (unlimited public apps)
- **OpenRouter (Claude):** ~$0.015-0.03 per post
- **Tavily:** Free (1,000 searches/month)
- **Notion:** Free
- **Slack:** Free

**Estimated cost:** $5-10/month for 300-500 posts

---

## Security Notes

✅ **Safe:** Secrets stored in Streamlit Cloud dashboard (encrypted)
✅ **Safe:** `.env` file gitignored (never committed)
✅ **Safe:** `.streamlit/secrets.toml` gitignored
❌ **Never:** Commit API keys to Git
❌ **Never:** Share your `.env` file
❌ **Never:** Hardcode secrets in code

---

## Support

If deployment fails:
1. Check Streamlit Cloud logs
2. Verify all secrets are set
3. Test locally first
4. Review [README.md](README.md) for full documentation

---

**🎉 Your LinkedIn Content Engine is now live!**
