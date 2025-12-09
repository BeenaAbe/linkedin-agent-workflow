# 🔒 Security Guide - Keep Your API Keys Private

**CRITICAL:** Never commit API keys to GitHub or any public repository!

---

## ✅ What's Protected

I've set up multiple layers of security:

### 1. `.gitignore` File Created ✅

The `.gitignore` file ensures these are **NEVER** committed:
- `.env` (your local API keys)
- `.streamlit/secrets.toml` (Streamlit cloud secrets)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)

**Location:** `.gitignore` in project root

---

### 2. Environment Variables Setup

**Two ways to store secrets:**

#### **Option A: Local Development** (`.env` file)
```env
# .env file - NEVER COMMIT THIS!
NOTION_TOKEN=secret_XXXXX...
NOTION_DATABASE_ID=XXXXX...
TAVILY_API_KEY=tvly-XXXXX...
OPENROUTER_API_KEY=sk-or-v1-XXXXX...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

✅ **Already protected** by `.gitignore`

#### **Option B: Streamlit Cloud** (secrets.toml)
```toml
# .streamlit/secrets.toml - NEVER COMMIT THIS!
NOTION_TOKEN = "secret_XXXXX..."
NOTION_DATABASE_ID = "XXXXX..."
TAVILY_API_KEY = "tvly-XXXXX..."
OPENROUTER_API_KEY = "sk-or-v1-XXXXX..."
SLACK_WEBHOOK_URL = "https://hooks.slack.com/..."
```

✅ **Already protected** by `.gitignore`

---

## 🛡️ Security Checklist

### Before First Run:

- [x] `.gitignore` file exists
- [ ] Copy `.env.example` to `.env`
- [ ] Add your real API keys to `.env`
- [ ] **DO NOT** commit `.env`

### Before Pushing to GitHub:

```bash
# ALWAYS CHECK before pushing:
git status

# Make sure .env is NOT listed!
# If you see .env, STOP and run:
git reset HEAD .env
```

### For Streamlit Cloud Deployment:

- [ ] Push code WITHOUT `.env` file
- [ ] Add secrets in Streamlit Cloud dashboard
- [ ] Never paste secrets in code files

---

## 🚨 Emergency: I Accidentally Committed Secrets!

### If you committed `.env` to Git:

**Step 1: Revoke all API keys IMMEDIATELY**
1. **OpenRouter:** https://openrouter.ai/settings/keys → Delete key → Create new one
2. **Tavily:** https://app.tavily.com → Regenerate key
3. **Notion:** https://www.notion.so/my-integrations → Regenerate token
4. **Slack:** Regenerate webhook URL

**Step 2: Remove from Git history**
```bash
# Remove file from Git (keeps local copy)
git rm --cached .env

# Add to .gitignore if not already there
echo ".env" >> .gitignore

# Commit the removal
git add .gitignore
git commit -m "Remove sensitive files and update gitignore"

# Force push (if already pushed to remote)
git push --force
```

**Step 3: Update with new keys**
```bash
# Edit .env with NEW keys
# NEVER commit it again!
```

---

## ✅ How to Safely Use API Keys

### Local Development:

1. **Create `.env` file:**
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Mac/Linux
   ```

2. **Edit `.env` with your keys**

3. **Run app:**
   ```bash
   run_streamlit.bat
   # OR
   python main.py single
   ```

4. **Keys load automatically** from `.env`

---

### Streamlit Cloud Deployment:

**Option 1: Using Streamlit Secrets Manager (Recommended)**

1. **Push code to GitHub** (without `.env`):
   ```bash
   git add .
   git commit -m "Add LinkedIn content engine"
   git push
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repo

3. **Add secrets in dashboard:**
   - Click "Advanced settings" → "Secrets"
   - Paste your keys:
   ```toml
   NOTION_TOKEN = "secret_XXXXX..."
   NOTION_DATABASE_ID = "XXXXX..."
   TAVILY_API_KEY = "tvly-XXXXX..."
   OPENROUTER_API_KEY = "sk-or-v1-XXXXX..."
   SLACK_WEBHOOK_URL = "https://hooks.slack.com/..."
   ```

4. **Deploy!** Keys are stored securely on Streamlit's servers.

**Option 2: Using `.streamlit/secrets.toml` (Local Testing)**

1. **Create secrets file:**
   ```bash
   mkdir .streamlit
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
   ```

2. **Edit `.streamlit/secrets.toml`** with your keys

3. **Already protected** by `.gitignore`

---

## 🔍 Verify Your Setup is Secure

### Check 1: Is `.gitignore` working?

```bash
git status

# You should see:
# - README.md (staged)
# - streamlit_app.py (staged)
# - workflow.py (staged)

# You should NOT see:
# - .env
# - .streamlit/secrets.toml
# - venv/
```

### Check 2: Are keys in tracked files?

```bash
# Search for potential secrets in tracked files
git grep -E "(secret_|tvly-|sk-or-v1-|sk-ant-)"

# Should only return .env.example (placeholders)
# NOT actual keys!
```

### Check 3: GitHub Safety Check

After pushing to GitHub:
1. Go to your repo on GitHub
2. Check files:
   - ✅ `.env.example` should be there (with placeholders)
   - ❌ `.env` should NOT be there
   - ❌ `secrets.toml` should NOT be there

---

## 🎯 Best Practices

### ✅ DO:
- Use `.env` for local development
- Use Streamlit Secrets Manager for cloud deployment
- Keep `.gitignore` up to date
- Rotate keys periodically (every 3-6 months)
- Use different keys for dev/staging/prod

### ❌ DON'T:
- Hard-code API keys in `.py` files
- Commit `.env` or `secrets.toml`
- Share `.env` file via email/Slack
- Use production keys in development
- Push keys to public GitHub repos

---

## 🔐 Key Storage Options (Ranked)

| Method | Security | Ease | Best For |
|--------|----------|------|----------|
| **Streamlit Cloud Secrets** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Cloud deployment |
| **`.env` (gitignored)** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Local development |
| **Environment variables** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Server deployment |
| **Hard-coded (DON'T!)** | ⭐ | ⭐⭐⭐⭐⭐ | NEVER! |

---

## 🚀 Quick Setup (Secure)

### For Local Testing:
```bash
# 1. Setup (one time)
setup.bat
copy .env.example .env
# Edit .env with your keys

# 2. Run
run_streamlit.bat

# 3. Verify .env is gitignored
git status  # Should NOT show .env
```

### For Streamlit Cloud:
```bash
# 1. Push code (WITHOUT .env)
git add .
git commit -m "Initial commit"
git push

# 2. Deploy on Streamlit Cloud
# 3. Add secrets in dashboard (NOT in code)
# 4. Done! Keys are safe on Streamlit's servers
```

---

## 📋 Deployment Security Checklist

Before deploying:

- [ ] `.gitignore` includes `.env` and `secrets.toml`
- [ ] No API keys in `.py` files
- [ ] `.env.example` has placeholders only
- [ ] Ran `git status` to verify `.env` not staged
- [ ] Tested locally with `.env`
- [ ] Added secrets to Streamlit Cloud dashboard
- [ ] Deleted any test keys from previous attempts

---

## 🆘 Support

**If you accidentally exposed keys:**
1. Revoke ALL keys immediately
2. Follow "Emergency" steps above
3. Create new keys
4. Update `.env` with new keys
5. Never commit `.env` again

**Check if your repo is safe:**
```bash
# Look for secrets in Git history
git log -p | grep -E "(secret_|tvly-|sk-or-v1-)"

# If found, you MUST revoke those keys!
```

---

## ✅ Summary

**Your setup is secure if:**
1. ✅ `.gitignore` exists and includes `.env`
2. ✅ `.env` file exists locally but NOT on GitHub
3. ✅ `git status` does NOT show `.env`
4. ✅ No API keys in `.py` files
5. ✅ Streamlit Cloud secrets added via dashboard

**Test it:**
```bash
# This should work (keys from .env):
run_streamlit.bat

# This should show NO .env:
git status
```

---

## 🎉 You're Protected!

Your API keys are now secure. The app will:
- ✅ Load from `.env` locally
- ✅ Load from Streamlit secrets in cloud
- ✅ Never commit secrets to Git
- ✅ Keep keys private

**Ready to deploy safely!** 🚀
