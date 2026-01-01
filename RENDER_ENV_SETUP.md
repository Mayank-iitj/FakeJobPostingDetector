# Render Environment Setup

## 🔑 Environment Variables for Render

Add these environment variables in Render Dashboard → Your Service → Environment

---

## Required Variables

### 1. SECRET_KEY (CRITICAL)
```
SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU
```
> ⚠️ **Already generated for you!** Keep this secret.

### 2. ALLOWED_ORIGINS (Update for Production)
```
ALLOWED_ORIGINS=*
```
> 📝 **For testing:** `*` allows all origins  
> 🔒 **For production:** Replace with actual domains:
> ```
> ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://yourdomain.com
> ```

---

## Recommended Variables

### Performance
```
WORKERS=1
LOG_LEVEL=info
```

### Security
```
RATE_LIMIT_PER_MINUTE=100
MAX_UPLOAD_SIZE_MB=50
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Feature Flags
```
ENABLE_EXPLAINABILITY=true
ENABLE_ACTIVE_LEARNING=false
ENABLE_DRIFT_DETECTION=false
```

---

## Optional: Database & Cache

### If using Render PostgreSQL
Render automatically sets `DATABASE_URL` when you add a PostgreSQL database.

**To add:**
1. Render Dashboard → New → PostgreSQL
2. Create database
3. Link to your web service
4. `DATABASE_URL` is auto-set ✅

### If using Render Redis
Render automatically sets `REDIS_URL` when you add Redis.

**To add:**
1. Render Dashboard → New → Redis
2. Create Redis instance
3. Link to your web service
4. `REDIS_URL` is auto-set ✅

---

## How to Add Environment Variables

### Method 1: Via Dashboard (Recommended)
1. Go to your service in Render
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Enter **Key** and **Value**
5. Click **"Save Changes"**
6. Service auto-redeploys ✅

### Method 2: Via render.yaml (Already configured!)
If deploying with `render.yaml`, all variables are pre-configured.  
Just click the deploy button!

---

## 📋 Quick Copy-Paste

**Copy all these into Render Environment:**

```
SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU
ALLOWED_ORIGINS=*
WORKERS=4
LOG_LEVEL=info
RATE_LIMIT_PER_MINUTE=100
MAX_UPLOAD_SIZE_MB=50
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENABLE_EXPLAINABILITY=true
ENABLE_ACTIVE_LEARNING=false
ENABLE_DRIFT_DETECTION=false
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep `SECRET_KEY` private
- Update `ALLOWED_ORIGINS` with actual domains for production
- Use different keys for staging/production
- Rotate secrets regularly

### ❌ DON'T:
- Commit `.env` files to Git (already prevented by `.gitignore`)
- Share secrets in logs or public channels
- Use default demo passwords in production

---

## 🧪 Testing Your Deployment

After setting environment variables:

```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test API documentation
# Visit: https://your-app.onrender.com/docs

# Test phishing endpoint
curl -X POST https://your-app.onrender.com/scan/phishing \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","capture_screenshot":true}'
```

---

## 📊 Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | - | JWT secret key |
| `ALLOWED_ORIGINS` | ✅ Yes | `*` | CORS origins |
| `WORKERS` | ⚪ No | `4` | Uvicorn workers |
| `LOG_LEVEL` | ⚪ No | `info` | Logging level |
| `RATE_LIMIT_PER_MINUTE` | ⚪ No | `100` | Rate limit |
| `MAX_UPLOAD_SIZE_MB` | ⚪ No | `50` | Max file upload |
| `DATABASE_URL` | ⚪ No | - | PostgreSQL URL (auto-set) |
| `REDIS_URL` | ⚪ No | - | Redis URL (auto-set) |

---

**Your environment is configured! Deploy and test.** 🚀
