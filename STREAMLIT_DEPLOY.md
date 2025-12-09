# 🌐 Streamlit Deployment Guide

Run your LinkedIn Content Engine with a beautiful web interface!

---

## 🚀 Quick Start (Local)

### 1. Install Streamlit

```bash
# Activate your virtual environment first
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install Streamlit (if not already installed)
pip install streamlit
# OR reinstall everything:
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at: `http://localhost:8501`

---

## 🎨 Features

### **Manual Input Mode**
- ✅ Test workflow with custom topics
- ✅ Choose from 6 goal types
- ✅ Add context/notes
- ✅ See results in real-time

### **Notion Integration Mode**
- ✅ Fetch ideas from Notion database
- ✅ Process automatically
- ✅ Update Notion with results
- ✅ Send Slack notifications
- ✅ See queue status

### **Real-Time Monitoring**
- ✅ Activity log sidebar
- ✅ Workflow progress
- ✅ Connection status
- ✅ Error messages

### **Results Display**
- ✅ 3 hook options
- ✅ Complete post body
- ✅ Character count
- ✅ Research brief
- ✅ Visual suggestions
- ✅ Download button

---

## 🌍 Deploy to Streamlit Cloud (Free!)

### Step 1: Secure Your Keys & Push to GitHub

**🔒 CRITICAL: Never commit `.env` file!**

✅ **Good news:** `.gitignore` is already set up to protect your keys!

```bash
cd linkedin-agent-workflow

# 1. Verify .gitignore protects your keys
cat .gitignore  # Should include .env and secrets.toml

# 2. Check git status (should NOT show .env)
git status

# 3. If .env appears, STOP! It should already be ignored.
# If you see it, run: git reset HEAD .env

# 4. Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit - LinkedIn Content Engine"

# 5. Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/linkedin-agent-workflow.git
git push -u origin main
```

**⚠️ DOUBLE CHECK on GitHub:**
- ✅ `.env.example` should be there (safe placeholders)
- ❌ `.env` should NOT be there (your real keys!)
- ✅ `.gitignore` should be there

**If you see `.env` on GitHub:** Follow [SECURITY.md](SECURITY.md) emergency recovery steps immediately!

### Step 2: Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Click "New app"**

3. **Fill in:**
   - **Repository:** `YOUR_USERNAME/linkedin-agent-workflow`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`

4. **Click "Advanced settings"** and add environment variables:
   ```
   NOTION_TOKEN=secret_XXXXX...
   NOTION_DATABASE_ID=XXXXX...
   TAVILY_API_KEY=tvly-XXXXX...
   OPENROUTER_API_KEY=sk-or-v1-XXXXX...
   SLACK_WEBHOOK_URL=https://hooks.slack.com/...
   ```

5. **Click "Deploy"**

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

---

## 🐳 Deploy with Docker (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build
docker build -t linkedin-content-engine .

# Run
docker run -p 8501:8501 \
  -e NOTION_TOKEN=$NOTION_TOKEN \
  -e NOTION_DATABASE_ID=$NOTION_DATABASE_ID \
  -e TAVILY_API_KEY=$TAVILY_API_KEY \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  -e SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL \
  linkedin-content-engine
```

---

## 🔧 Configuration

### Custom Port

```bash
streamlit run streamlit_app.py --server.port 8080
```

### Disable Auto-Open Browser

```bash
streamlit run streamlit_app.py --server.headless true
```

### Config File

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0077B5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
```

---

## 📱 Using the App

### Manual Mode

1. **Select "Manual Input"** in sidebar
2. **Enter topic:** "Why most AI agents are just fancy chatbots"
3. **Choose goal:** Thought Leadership
4. **Add context (optional):** "Lead with 83% stat"
5. **Click "Generate Post"**
6. **View results** in tabs (Hooks, Post, Research, Visual)
7. **Download** complete post

### Notion Mode

1. **Select "Notion Integration"** in sidebar
2. **Click "Fetch & Process"**
3. **App pulls next "Idea"** from Notion
4. **Processes automatically**
5. **Updates Notion** with results
6. **Sends Slack** notification
7. **View results** in tabs

---

## 🎯 Workflow Types

### Simple Sequential
- Linear flow: Research → Write → Done
- Fast execution
- No quality checks

### Adaptive (Recommended)
- Quality checks at each step
- Loops back if output too short
- Self-correcting
- Slightly slower but better quality

**Switch in sidebar:** "Workflow Type" selector

---

## 🐛 Troubleshooting

### "Missing environment variables"
**Fix:** Create `.env` file with all required keys

### "Connection refused"
**Fix:** Make sure virtual environment is activated:
```bash
venv\Scripts\activate
```

### "Module not found"
**Fix:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "Port already in use"
**Fix:** Kill existing Streamlit process or use different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Results not showing
**Fix:** Click the workflow button again. Check activity log in sidebar for errors.

---

## 🎨 Screenshots

### Manual Mode
![Manual Input](https://placeholder.com/manual-mode.png)
- Clean input form
- Real-time generation
- Instant results

### Notion Mode
![Notion Integration](https://placeholder.com/notion-mode.png)
- Queue status
- One-click processing
- Automatic updates

### Results View
![Results Display](https://placeholder.com/results-view.png)
- Tabbed interface
- Character count
- Download button

---

## 💡 Tips

**For testing:**
- Use Manual Mode for quick experiments
- Try different goals and contexts
- Compare Adaptive vs Simple workflow

**For production:**
- Use Notion Mode with queue
- Enable Slack notifications
- Use Adaptive workflow for quality

**Performance:**
- Each run takes 30-60 seconds
- Adaptive mode may take 2x longer (but better quality)
- Streamlit caches results

---

## 🔒 Security

**Never commit `.env` file!**

Always use:
- `.gitignore` to exclude `.env`
- Streamlit Cloud secrets for deployment
- Environment variables for Docker

**Check before pushing:**
```bash
git status
# Make sure .env is not listed
```

---

## 🆚 Streamlit vs Command Line

| Feature | Command Line | Streamlit |
|---------|-------------|-----------|
| **Interface** | Terminal output | Web UI |
| **Testing** | Edit code each time | Form inputs |
| **Results** | Notion only | Visual display |
| **Monitoring** | Print statements | Activity log |
| **Sharing** | Need server access | Web URL |
| **Best For** | Production/automation | Testing/demos |

---

## 📊 Performance

**Local:**
- Cold start: ~5 seconds
- Workflow run: 30-60 seconds
- Results display: Instant

**Streamlit Cloud (Free):**
- Cold start: ~30 seconds
- Workflow run: 30-60 seconds
- Auto-sleep after 7 days inactivity

**Streamlit Cloud (Paid):**
- Always-on
- Faster cold starts
- More resources

---

## 🎉 Next Steps

1. ✅ **Test locally:** `streamlit run streamlit_app.py`
2. ✅ **Try both modes:** Manual and Notion
3. ✅ **Compare workflows:** Simple vs Adaptive
4. ✅ **Deploy to cloud:** Streamlit Cloud (free!)
5. ✅ **Share with team:** Send app URL

---

## 🆘 Need Help?

**Streamlit not starting:**
```bash
# Check if installed
pip list | grep streamlit

# Reinstall
pip uninstall streamlit
pip install streamlit
```

**App crashes:**
- Check activity log in sidebar
- Verify `.env` file exists and is correct
- Look for error messages in terminal

**Can't deploy to cloud:**
- Make sure repo is public
- Check all secrets are added
- Verify `requirements.txt` is complete

---

## 📚 Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Cloud:** https://share.streamlit.io
- **Streamlit Gallery:** https://streamlit.io/gallery

---

**Ready to launch? Run:**

```bash
venv\Scripts\activate
streamlit run streamlit_app.py
```

**Your app will open at:** http://localhost:8501 🚀
