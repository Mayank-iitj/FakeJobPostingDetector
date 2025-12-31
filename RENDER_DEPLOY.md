# 🚀 Deploy to Render in 5 Minutes

## ✅ Your App is Render-Ready!

All configuration is complete. Choose your deployment method below.

---

## 🎯 Option 1: One-Click Deploy (Recommended)

Click the button below to deploy with pre-configured settings:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Mayank-iitj/threat-intel-platform)

**What happens:**
- ✅ Automatic service creation
- ✅ All environment variables pre-set
- ✅ Build and deployment starts immediately
- ⏱️ Live in ~10 minutes

---

## 🔧 Option 2: Manual Deployment

### Step 1: Create Render Account (1 min)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Create Web Service (2 min)
1. Click **"New +"** → **"Web Service"**
2. Connect your repository: `Mayank-iitj/threat-intel-platform`
3. Configure:
   - **Name:** `threat-intel-api`
   - **Region:** Choose closest to you (Oregon, Frankfurt, Singapore)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:**
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 4
     ```

### Step 3: Set Environment Variables (1 min)

Click **"Advanced"** → Add these environment variables:

```env
SECRET_KEY=wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU
ALLOWED_ORIGINS=*
WORKERS=4
LOG_LEVEL=info
RATE_LIMIT_PER_MINUTE=100
```

### Step 4: Deploy! (1 min)
1. Click **"Create Web Service"**
2. Render builds and deploys automatically
3. ✅ Done!

---

## ✅ Verify Deployment

Once deployed, test your API:

```bash
# Replace YOUR-APP-NAME with your Render service name
curl https://YOUR-APP-NAME.onrender.com/health
```

**Expected Response:**
```json
{"status":"healthy","service":"threat-intel-api","version":"1.0.0"}
```

### API Documentation
Visit: `https://YOUR-APP-NAME.onrender.com/docs`

---

## 🆓 Free Tier Details

**What you get FREE:**
- ✅ 750 hours/month (enough for 24/7 operation)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Auto-deploy from GitHub
- ✅ Free SSL certificate
- ✅ Custom domains (free)

**Limitations:**
- ⏸️ Spins down after 15 min of inactivity
- ⏱️ ~30 sec cold start (first request after sleep)
- 💾 512 MB RAM (sufficient for demo)

---

## 🔄 Automatic Deployments

**Render auto-deploys when you push to GitHub:**

```bash
git add .
git commit -m "Update API"
git push origin main
# Render automatically deploys! 🚀
```

---

## 📊 Optional: Add Database & Redis

### Add PostgreSQL (Free)
1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name: `threat-intel-db`
3. Plan: **Free**
4. Click **"Create Database"**
5. In your web service → **Environment** → Add:
   - Key: `DATABASE_URL`
   - Value: Click **"Insert"** → Select your database → `Internal Database URL`

### Add Redis (Free)
1. Click **"New +"** → **"Redis"**
2. Name: `threat-intel-redis`
3. Plan: **Free**
4. In your web service → **Environment** → Add:
   - Key: `REDIS_URL`
   - Value: Select your Redis instance

---

## 🌐 Custom Domain

### Add Your Domain (Free SSL!)
1. Go to your service → **Settings** → **Custom Domains**
2. Click **"Add Custom Domain"**
3. Enter: `api.yourdomain.com`
4. Add CNAME record to your DNS:
   - **Type:** CNAME
   - **Name:** api
   - **Value:** (Render provides this)
5. ✅ Free SSL auto-configured!

---

## 🔒 Production Security Checklist

Before going live:

- [ ] Update `ALLOWED_ORIGINS` to your actual frontend domain
  ```env
  ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://yourdomain.com
  ```
- [ ] Rotate `SECRET_KEY` if exposed
- [ ] Enable database backups (paid plans)
- [ ] Add monitoring (Sentry)
- [ ] Review rate limits
- [ ] Test all endpoints

---

## 💰 Upgrade to Paid Plan

**When you outgrow free tier:**

**Starter Plan ($7/month):**
- ✅ Always-on (no spin down)
- ✅ 512 MB RAM, 0.5 CPU
- ✅ Better performance

**Standard Plan ($25/month):**
- ✅ 2 GB RAM, 1 CPU
- ✅ Perfect for production ML workloads

---

## 📝 Monitoring & Logs

### View Logs
1. Go to your service
2. Click **"Logs"** tab
3. View real-time logs

### Metrics
- Click **"Metrics"** tab
- View CPU, Memory, HTTP metrics
- Set up alerts (paid plans)

---

## 🐛 Troubleshooting

### Build Fails
**Check logs for:**
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Out of memory during build

**Solution:** Large ML dependencies might need paid plan for build

### App Crashes
**Check logs for:**
- Missing environment variables
- Import errors
- PORT not configured

**Fix:** Ensure `--port $PORT` in start command

### Slow Performance
**Free tier limitations:**
- Cold starts (15 min inactivity)
- Limited RAM

**Solution:** Upgrade to Starter plan ($7/month)

---

## 🎯 Your Render Service URLs

After deployment, you'll get:
- **API:** `https://threat-intel-api.onrender.com`
- **Docs:** `https://threat-intel-api.onrender.com/docs`
- **Health:** `https://threat-intel-api.onrender.com/health`

---

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-fastapi)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Auto-Deploy](https://render.com/docs/deploys)

---

**Ready to deploy! 🚀**

Choose Option 1 (One-Click) or Option 2 (Manual) above.
