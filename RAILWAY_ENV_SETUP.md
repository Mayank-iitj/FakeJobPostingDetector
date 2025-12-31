# Railway Environment Variable Setup

## 🔑 Required Environment Variables

After deploying to Railway, you **MUST** add these environment variables in your Railway project settings:

### Step 1: Access Environment Variables

1. Go to your Railway project dashboard
2. Click on your service
3. Navigate to the **"Variables"** tab
4. Click **"New Variable"**

---

### Step 2: Add Required Variables

Copy and paste these **one by one** into Railway:

#### **SECRET_KEY** (CRITICAL - Already Generated!)
```
SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU
```
> ⚠️ **Important:** This is a cryptographically secure key already generated for you. Keep it secret!

#### **ALLOWED_ORIGINS** (Update for Production!)
```
ALLOWED_ORIGINS=*
```
> 📝 **Note:** `*` allows all origins (for testing). For production, replace with:
> ```
> ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://yourdomain.com
> ```

---

### Step 3: Optional but Recommended Variables

#### **Performance & Scaling**
```
WORKERS=4
LOG_LEVEL=info
RATE_LIMIT_PER_MINUTE=100
```

#### **Feature Flags**
```
ENABLE_EXPLAINABILITY=true
ENABLE_ACTIVE_LEARNING=false
ENABLE_DRIFT_DETECTION=false
```

#### **Security**
```
MAX_UPLOAD_SIZE_MB=50
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🗄️ Optional: Add Database & Redis

### PostgreSQL Database (Recommended for Production)

1. In Railway, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway automatically sets `DATABASE_URL` environment variable
3. No manual configuration needed!

### Redis Cache (Optional - for Celery tasks)

1. Click **"New"** → **"Database"** → **"Redis"**
2. Railway automatically sets `REDIS_URL` environment variable
3. Used for async background tasks and caching

---

## 🌐 Custom Domain Setup

### Option 1: Free Railway Subdomain

1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"**
3. You'll get: `https://your-app-name.up.railway.app`

### Option 2: Custom Domain

1. Click **"Custom Domain"**
2. Enter your domain: `api.yourdomain.com`
3. Add CNAME record to your DNS provider:
   - **Type:** CNAME
   - **Name:** api
   - **Value:** (Railway provides this)
   - **TTL:** 3600

---

## ✅ Verification Checklist

After deployment, verify everything works:

### 1. Health Check
```bash
curl https://your-app.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "threat-intel-api",
  "version": "1.0.0"
}
```

### 2. API Documentation
Visit: `https://your-app.railway.app/docs`

You should see the interactive Swagger UI.

### 3. Test Endpoints

**Phishing Scan:**
```bash
curl -X POST https://your-app.railway.app/scan/phishing \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "capture_screenshot": true,
    "analyze_dom": true
  }'
```

**Authentication:**
```bash
curl -X POST https://your-app.railway.app/auth/token \
  -d "username=demo&password=demopassword"
```

---

## 🚨 Important Security Notes

### 🔒 **Never commit .env files to Git!**
The `.gitignore` is already configured to exclude `.env` files.

### 🔑 **Rotate SECRET_KEY regularly**
Generate a new one:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 🌐 **Update ALLOWED_ORIGINS for production**
Don't use `*` in production! Specify exact domains:
```
ALLOWED_ORIGINS=https://app.yourdomain.com,https://www.yourdomain.com
```

### 🔐 **Update default credentials**
The demo auth credentials are for testing only. Implement proper user management for production.

---

## 📊 Monitoring & Logs

### View Real-time Logs

**Railway Dashboard:**
1. Go to your service
2. Click **"Deployments"**
3. Select active deployment
4. View live logs

**Railway CLI:**
```bash
railway logs -f
```

### Check Build Logs

If deployment fails:
```bash
railway logs --deployment
```

---

## 🐛 Troubleshooting

### Build Fails

**Symptom:** Deployment fails during build
**Solution:**
- Check `requirements.txt` for invalid packages
- Verify Python version in `runtime.txt`
- Check Railway build logs

### App Crashes on Startup

**Symptom:** App deploys but immediately crashes
**Solution:**
- Verify `SECRET_KEY` is set in Railway variables
- Check if `PORT` environment variable is being used (Railway sets this automatically)
- Review startup logs for errors

### Health Check Fails

**Symptom:** `/health` endpoint returns error
**Solution:**
- Verify app is listening on `0.0.0.0:$PORT`
- Check if all dependencies installed correctly
- Review app logs for startup errors

### Models Not Loading

**Symptom:** Warnings about missing model files
**Solution:**
- This is **EXPECTED** behavior! The app will use mock predictions
- To use real models, upload them to Railway volumes or cloud storage
- The API will work perfectly in demo mode for testing

---

## 🎯 Quick Reference

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `SECRET_KEY` | `wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU` | ✅ Yes | JWT secret key |
| `ALLOWED_ORIGINS` | `*` or specific domains | ✅ Yes | CORS configuration |
| `WORKERS` | `4` | ⚪ Optional | Uvicorn workers |
| `LOG_LEVEL` | `info` | ⚪ Optional | Logging level |
| `DATABASE_URL` | Auto-set by Railway | ⚪ Optional | PostgreSQL connection |
| `REDIS_URL` | Auto-set by Railway | ⚪ Optional | Redis connection |

---

## 📝 Complete Environment Variable Template

Copy this entire block and paste into Railway (update domains as needed):

```env
SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU
ALLOWED_ORIGINS=*
WORKERS=4
LOG_LEVEL=info
RATE_LIMIT_PER_MINUTE=100
MAX_UPLOAD_SIZE_MB=50
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENABLE_EXPLAINABILITY=true
```

---

🚀 **You're ready to deploy!** Follow the deployment steps in `RAILWAY.md`.
