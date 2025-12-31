# Render Deployment Troubleshooting

## Issue: Port Timeout Error

**Error Message:**
```
Timed out: Port scan timeout reached, no open ports detected.
Bind your service to at least one port.
```

## ✅ Fixes Applied

### 1. Reduced Workers (Most Common Fix)
**Problem:** Free tier has limited RAM (512MB). 4 workers can cause out-of-memory crashes.

**Fix:** Changed from 4 workers to 1 worker in `render.yaml`:
```yaml
startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 1
```

### 2. Added Debug Logging
```yaml
startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level debug
```

---

## 🔍 Common Causes & Solutions

### Cause 1: Out of Memory (Most Likely)
**Symptoms:**
- Port timeout
- App crashes during startup
- No logs after build completes

**Solution:**
- ✅ Use 1 worker (already done)
- Reduce ML dependencies if possible
- Upgrade to paid plan ($7/month for more RAM)

### Cause 2: App Crashes During Startup
**Check Render logs for:**
- Import errors
- Missing dependencies
- Environment variable issues

**Common fixes:**
```bash
# Missing dependency
pip install email-validator  # Already added ✅

# Import error
# Check all imports in api/main.py work

# Environment variable
# Ensure SECRET_KEY is set in Render
```

### Cause 3: Slow Startup
**Problem:** Large ML dependencies take time to import.

**Solution:**
- Wait 2-3 minutes (PyTorch, Transformers are large)
- Check Render logs for "Application startup complete"
- Increase health check timeout in Render settings

---

## 📋 Deployment Checklist

### Before Deploy:
- [ ] Push latest code to GitHub
- [ ] Verify `render.yaml` has workers=1
- [ ] Check all dependencies in `requirements.txt` are valid

### During Deploy:
- [ ] Watch Render logs in real-time
- [ ] Look for "Application startup complete" message
- [ ] Wait at least 2-3 minutes for ML dependencies to load

### After Deploy:
- [ ] Test `/health` endpoint
- [ ] Check `/docs` for API documentation
- [ ] Monitor memory usage in Render metrics

---

## 🚀 Current Configuration

**Your `render.yaml` is now configured as:**
```yaml
buildCommand: pip install --upgrade pip && pip install -r requirements.txt
startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level debug
healthCheckPath: /health
```

** Environment Variables:**
- `SECRET_KEY`: Auto-generated or set manually
- `ALLOWED_ORIGINS`: `*`
- `WORKERS`: 1 (for free tier)

---

## 🔧 Manual Deployment (If Blueprint Fails)

If using `render.yaml` doesn't work, try manual configuration:

1. **New Web Service**
2. **Connect your repo**
3. **Basic Settings:**
   - Name: `threat-intel-api`
   - Region: Oregon (or closest)
   - Branch: `main`
   - Runtime: Python 3
   
4. **Build & Deploy:**
   - Build: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   
5. **Environment:**
   - Add: `SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU`
   - Add: `ALLOWED_ORIGINS=*`

6. **Advanced:**
   - Health Check Path: `/health`
   - Auto-Deploy: Yes

---

## 📊 Expected Startup Time

**Free Tier:**
- Build: 5-7 minutes (PyTorch, Transformers)
- Startup: 30-60 seconds
- **Total: ~8 minutes**

**Be patient!** ML dependencies are large.

---

## 🐛 Debug Steps

### Step 1: Check Render Logs
Look for these messages:

**Good Signs:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXXX
```

**Bad Signs:**
```
Killed (Out of memory)
ModuleNotFoundError: ...
ImportError: ...
```

### Step 2: Test Health Endpoint
Once deployed, test immediately:
```bash
curl https://your-app.onrender.com/health
```

### Step 3: Check Memory Usage
In Render Dashboard → Metrics:
- Memory should be < 500MB
- If near 512MB, reduce workers or upgrade plan

---

## 💡 Quick Fixes

### Fix 1: Out of Memory
```yaml
# Use fewer workers (already done)
startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Fix 2: Import Errors
```bash
# Check your local environment
python -c "from api.main import app; print('OK')"
```

### Fix 3: Port Not Binding
```python
# Verify PORT env var is used (already correct)
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

---

## 🆘 Still Not Working?

### Option 1: Simplify Dependencies
Create `requirements-minimal.txt`:
```txt
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
pydantic>=2.0.0
email-validator>=2.0.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

Temporarily remove PyTorch/Transformers to test basic deployment.

### Option 2: Use Different Platform
- **Fly.io**: Better for large ML apps
- **Heroku**: More expensive but reliable ($7/month)
- **Google Cloud Run**: Pay-as-you-go

### Option 3: Upgrade Render Plan
**Starter Plan ($7/month):**
- 512MB RAM → Still tight for PyTorch
- Always-on (no cold starts)

**Standard Plan ($25/month):**
- 2GB RAM → Perfect for ML workloads
- 1 CPU

---

## ✅ Next Steps

1. **Push updated `render.yaml` to GitHub** (with workers=1)
2. **Redeploy in Render** (wait 8-10 minutes)
3. **Watch logs** for startup completion
4. **Test health endpoint** once deployed

**Updated config is ready - proceed with redeployment!** 🚀
