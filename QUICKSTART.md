# 🚀 Quick Start Guide

Get the Job Scam Detector running in 5 minutes!

---

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip package manager
- ✅ 500MB free disk space
- ✅ Internet connection (for dependencies)

---

## Installation (3 minutes)

### Option 1: Try Online (Instant)
**No installation needed!**
- Visit: [Your Deployed App](https://your-app.streamlit.app)
- Start analyzing jobs immediately
- Fully functional in browser

### Option 2: Streamlit Only (Quick)
For just the web interface:
```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

### Option 3: Automated Full Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

This script will:
1. Create virtual environment
2. Install all dependencies
3. Create config files
4. Train initial model

### Option 4: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create config
copy .env.example .env

# 5. Train model
python train_model.py
```

---

## Running the System (2 minutes)

### Step 1: Start the API Server

Open a terminal and run:
```bash
python backend\main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ API is ready when you see this!

### Step 2: Start the Web UI (Optional)

Open a **new** terminal and run:
```bash
streamlit run frontend\streamlit_app.py
```

Browser will automatically open to `http://localhost:8501`

---

## Quick Test

### Test 1: API Health Check
```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Test 2: Analyze a Scam Job

**Using CLI:**
```bash
python cli.py "URGENT!!! Earn $500/day! Pay $99 registration fee! WhatsApp only!!!"
```

**Using Web UI:**
1. Open `http://localhost:8501`
2. Click "Load Scam Example"
3. Click "Analyze Job Posting"
4. See the red warning! 🔴

**Using API:**
```bash
curl -X POST http://localhost:8000/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"URGENT!!! Earn $500/day! Pay $99 fee!\"}"
```

### Test 3: Analyze a Legitimate Job

```bash
python cli.py "Software Engineer at Microsoft. 3+ years Python experience required. Apply at careers.microsoft.com"
```

Should get high trust score! 🟢

---

## Chrome Extension Setup

1. Open Chrome and go to: `chrome://extensions/`

2. Enable "Developer mode" (toggle in top-right)

3. Click "Load unpacked"

4. Select the `chrome-extension` folder

5. Pin the extension to your toolbar

6. Navigate to any job posting and click the extension icon!

---

## What to Do Next

### For Users:
- 📝 Try the Web UI: Paste job postings and see results
- 🔍 Use Chrome Extension: Browse job sites safely
- 📖 Read the advice: Learn to spot scams yourself

### For Developers:
- 📊 Train with your data: Replace sample data in `data/raw/`
- 🎨 Customize UI: Edit `frontend/streamlit_app.py`
- 🔧 Adjust rules: Modify `backend/models/rules.py`
- 🧪 Run tests: `pytest tests/ -v`

---

## Common Issues

### "Python not found"
**Solution:** Install Python from https://python.org

### "pip not found"
**Solution:** Reinstall Python with "Add to PATH" checked

### "API connection failed"
**Solution:** Make sure API is running on port 8000
```bash
# Check if port is in use
netstat -ano | findstr :8000
```

### "Model not loaded"
**Solution:** Run training script
```bash
python train_model.py
```

### "Module not found"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

---

## Usage Examples

### Example 1: Check Email Job Offer
1. Copy job email text
2. Open Web UI
3. Paste text
4. Get instant analysis

### Example 2: Verify WhatsApp Job Message
1. Screenshot the message
2. Use OCR (future feature) or copy text
3. Run through CLI or Web UI
4. Share results to warn others

### Example 3: Browse Job Sites Safely
1. Install Chrome extension
2. Visit any job posting
3. Click extension icon
4. See trust score instantly

---

## Quick Command Reference

```bash
# Start API
python backend\main.py

# Start Web UI
streamlit run frontend\streamlit_app.py

# CLI analysis
python cli.py "job text here"

# Run tests
pytest tests/ -v

# Train model
python train_model.py
```

---

## Next Steps

✅ **System is running!** Here's what to explore:

1. **Read Full Documentation**
   - [README.md](README.md) - Complete guide
   - [API.md](docs/API.md) - API reference
   - [TRAINING.md](docs/TRAINING.md) - Model training

2. **Customize for Your Needs**
   - Add your own scam patterns
   - Train with your dataset
   - Adjust detection thresholds

3. **Deploy to Production**
   - [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
   - Choose cloud platform
   - Set up monitoring

4. **Contribute**
   - Report issues
   - Submit improvements
   - Share training data

---

## Getting Help

- 📖 Check documentation in `docs/` folder
- 🐛 Report bugs on GitHub Issues
- 💬 Ask questions in GitHub Discussions
- 📧 Contact maintainers

---

## Security Reminder

⚠️ **Important:**
- This is an AI assistant, not 100% accurate
- Always verify jobs independently
- Never pay fees before thorough verification
- Report scams to authorities

---

**You're all set! Stay safe from job scams! 🛡️**
