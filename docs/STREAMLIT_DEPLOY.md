# Streamlit Cloud Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

---

## 📋 Deployment Steps

### Step 1: Push to GitHub

1. **Initialize Git Repository** (if not already done)
```bash
git init
git add .
git commit -m "Initial commit - Job Scam Detector"
```

2. **Create GitHub Repository**
- Go to github.com
- Create new repository: `job-scam-detector`
- Don't initialize with README

3. **Push Code**
```bash
git remote add origin https://github.com/YOUR_USERNAME/job-scam-detector.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `job-scam-detector`
   - Main file path: `frontend/streamlit_app.py`
   - Click "Deploy!"

3. **Wait for Deployment** (2-5 minutes)
   - Streamlit will install dependencies
   - App will automatically start

---

## ⚙️ Configuration

### Environment Variables (Optional)

In Streamlit Cloud dashboard, you can set:

```bash
STANDALONE_MODE=true        # Use standalone detector (recommended)
API_URL=https://your-api.com  # If using external API
```

**Note**: Standalone mode is recommended for Streamlit Cloud as it doesn't require a separate API server.

---

## 📦 Required Files for Deployment

Streamlit Cloud looks for these files (already created):

✅ `requirements-streamlit.txt` - Python dependencies (lighter than full requirements.txt)
✅ `.streamlit/config.toml` - Streamlit configuration
✅ `packages.txt` - System dependencies (if needed)
✅ `frontend/streamlit_app.py` - Main application

---

## 🔧 Troubleshooting

### Issue: "Module not found"

**Solution**: Make sure requirements-streamlit.txt includes all needed packages

```bash
# In Streamlit Cloud settings, use:
# requirements-streamlit.txt instead of requirements.txt
```

### Issue: "Model not loaded"

**Solution**: This is normal! The app works in standalone mode without pre-trained model

- Uses rule-based detection (still effective)
- Trains lightweight model on first run (uses sample data)
- Or deploy with pre-trained model (see below)

### Issue: App is slow on first load

**Solution**: This is normal for first deployment

- Streamlit installs all dependencies
- Subsequent loads are faster (cached)
- Consider using lighter dependencies

---

## 📊 Deployment with Pre-trained Model

To deploy with your trained model:

1. **Train model locally**
```bash
python train_model.py
```

2. **Commit model file** (if size < 100MB)
```bash
git add models/saved_models/scam_detector.pkl
git commit -m "Add trained model"
git push
```

3. **For larger models** (>100MB):
   - Use Git LFS
   - Or use external storage (S3, Google Cloud Storage)
   - Download model on app startup

---

## 🎨 Customization for Deployment

### Change App Title/Icon
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"  # Change accent color
```

### Add Secrets (API Keys, etc.)
In Streamlit Cloud dashboard:
- Settings → Secrets
- Add TOML format:
```toml
[api]
key = "your-api-key"
url = "https://your-api.com"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["api"]["key"]
```

---

## 📈 Performance Optimization

### 1. Use Caching
Already implemented with `@st.cache_resource` for model loading

### 2. Minimize Dependencies
Use `requirements-streamlit.txt` instead of full `requirements.txt`

### 3. Optimize Imports
Import heavy libraries inside functions if possible

### 4. Use Session State
Store detector in session state (already implemented)

---

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit API keys
- Use Streamlit Cloud secrets

### 2. Rate Limiting
Add to app:
```python
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0

if st.session_state.analysis_count > 100:
    st.warning("Rate limit reached. Please try again later.")
    return

st.session_state.analysis_count += 1
```

### 3. Input Validation
Already implemented with text length checks

---

## 🌐 Custom Domain (Optional)

### Free Subdomain
Your app gets: `https://your-app-name.streamlit.app`

### Custom Domain
1. Upgrade to Streamlit Cloud Team plan
2. Add CNAME record in your DNS
3. Configure in Streamlit Cloud settings

---

## 📊 Monitoring

### Streamlit Cloud Dashboard
- View logs
- Monitor resource usage
- Check uptime
- View analytics

### Add Usage Analytics
```python
import streamlit as st

# Track analyses
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0

st.session_state.total_analyses += 1

# Show in sidebar
st.sidebar.metric("Analyses Today", st.session_state.total_analyses)
```

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push
Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Streamlit Cloud will auto-deploy (2-3 minutes)
```

### Manual Deploy
In Streamlit Cloud dashboard:
- Click "Reboot app"
- Or "Manage app" → "Reboot"

---

## 💰 Pricing

### Free Tier (Community Cloud)
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ 1 GB resources
- ✅ Community support

### Paid Tiers
- More resources
- More apps
- Priority support
- Custom domains

---

## 📱 Sharing Your App

Once deployed:
1. Get your URL: `https://your-app.streamlit.app`
2. Share on social media
3. Embed in website
4. Add to portfolio

---

## 🚀 Alternative Deployment Options

### 1. Heroku
```bash
# Create Procfile
echo "web: streamlit run frontend/streamlit_app.py --server.port=\$PORT" > Procfile

# Deploy
heroku create job-scam-detector
git push heroku main
```

### 2. Docker
```bash
# Use docker-compose.yml (already created)
docker-compose up -d
```

### 3. Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### 4. Google Cloud Run
```bash
gcloud run deploy job-scam-detector \
  --source . \
  --platform managed \
  --allow-unauthenticated
```

---

## 📋 Pre-Deployment Checklist

Before deploying to Streamlit Cloud:

- [ ] Code pushed to GitHub
- [ ] `requirements-streamlit.txt` tested locally
- [ ] `.streamlit/config.toml` created
- [ ] App works in standalone mode
- [ ] Sensitive data removed from code
- [ ] README.md updated with deployment info
- [ ] License file added
- [ ] Disclaimer visible in app

---

## 🎯 Quick Commands

```bash
# Test standalone mode locally
STANDALONE_MODE=true streamlit run frontend/streamlit_app.py

# Test with minimal requirements
pip install -r requirements-streamlit.txt
streamlit run frontend/streamlit_app.py

# Check app works without API
# (API server should be off)
streamlit run frontend/streamlit_app.py
```

---

## 🆘 Support

**Streamlit Documentation**
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Configuration](https://docs.streamlit.io/library/advanced-features/configuration)

**Community**
- [Streamlit Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

## 🎉 Success!

Your app is now live and accessible to the world!

**Share your deployed app:**
- Add link to README.md
- Tweet about it
- Post on LinkedIn
- Add to your portfolio

**Example URLs:**
- https://job-scam-detector.streamlit.app
- https://scam-detector-ai.streamlit.app
- https://safe-job-finder.streamlit.app

---

**Ready to protect job seekers worldwide! 🛡️**
