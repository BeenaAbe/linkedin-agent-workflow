# 🔑 Quick Guide: Setting Up API Keys Securely

**Time needed:** 2 minutes

---

## Step 1: Create Your `.env` File

```bash
# Copy the example file
copy .env.example .env
```

## Step 2: Add Your Real API Keys

Open `.env` in any text editor and replace the placeholders:

```env
# Replace YOUR_XXXXX with your actual keys:

NOTION_TOKEN=secret_abc123xyz...
NOTION_DATABASE_ID=32characterid...
TAVILY_API_KEY=tvly-abc123...
OPENROUTER_API_KEY=sk-or-v1-abc123...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

**Where to get each key:**

| Key | Get It Here | Format |
|-----|-------------|--------|
| `NOTION_TOKEN` | https://www.notion.so/my-integrations | `secret_...` |
| `NOTION_DATABASE_ID` | Notion database URL (32 chars) | No dashes |
| `TAVILY_API_KEY` | https://app.tavily.com | `tvly-...` |
| `OPENROUTER_API_KEY` | https://openrouter.ai/settings/keys | `sk-or-v1-...` |
| `SLACK_WEBHOOK_URL` | Slack app settings | Full URL |

## Step 3: Verify Security

```bash
# Run security check
verify_security.bat

# Should show all [OK] messages
```

## Step 4: Test Locally

```bash
# Run Streamlit app
run_streamlit.bat

# OR run command line
run.bat single
```

---

## ✅ Your Keys Are Safe Because:

1. ✅ `.gitignore` prevents `.env` from being committed
2. ✅ `.env` only exists on your computer
3. ✅ Streamlit Cloud uses separate secrets manager
4. ✅ No keys in Python code files

---

## 🌍 For Streamlit Cloud Deployment

**Don't upload `.env` to cloud!** Instead:

1. Push code to GitHub (without `.env`)
2. Add keys in Streamlit Cloud dashboard
3. Go to: App Settings → Secrets
4. Paste your keys there

**Format for Streamlit Secrets:**
```toml
NOTION_TOKEN = "secret_..."
NOTION_DATABASE_ID = "..."
TAVILY_API_KEY = "tvly-..."
OPENROUTER_API_KEY = "sk-or-v1-..."
SLACK_WEBHOOK_URL = "https://..."
```

---

## 🚨 Never Do This:

❌ Commit `.env` to Git
❌ Share `.env` via email/Slack
❌ Put keys directly in `.py` files
❌ Push secrets to public GitHub

---

## ✅ Always Do This:

✅ Use `.env` for local development
✅ Use Streamlit secrets for cloud
✅ Run `verify_security.bat` before pushing
✅ Check `git status` doesn't show `.env`

---

## 🆘 Quick Troubleshooting

**"Missing environment variables"**
→ Create `.env` file and add your keys

**"Can't find .env"**
→ Run: `copy .env.example .env`

**".env appears in git status"**
→ Run: `git reset HEAD .env` (it should be ignored)

**"Want to deploy to Streamlit Cloud"**
→ Add secrets in dashboard, not in code

---

## 📚 More Info

- **Full security guide:** [SECURITY.md](SECURITY.md)
- **Deployment guide:** [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md)
- **Quick start:** [HOW_TO_RUN.md](HOW_TO_RUN.md)

---

**That's it!** Your keys are now secure. 🔒
