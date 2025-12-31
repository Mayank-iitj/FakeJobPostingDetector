# Railway Deployment Guide

Complete guide for deploying Threat Intelligence Platform to Railway.

## 🚀 Quick Deploy (Recommended)

### Option 1: One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/threat-intel-platform)

### Option 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Option 3: Deploy Script

**Windows:**
```cmd
deploy_railway.bat
```

**Linux/Mac:**
```bash
chmod +x deploy_railway.sh
./deploy_railway.sh
```

---

## 📋 Step-by-Step Deployment

### 1. Prerequisites

- Railway account (free tier available)
- GitHub account (for automatic deployments)
- Railway CLI installed (optional)

### 2. Project Setup

#### A. From GitHub (Recommended)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will auto-detect Python and deploy

#### B. From CLI

```bash
cd threat-intel-platform
railway login
railway init
railway up
```

### 3. Configure Environment Variables

Go to your Railway project → Variables → Add the following:

**Required:**
```env
SECRET_KEY=your-random-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Optional but Recommended:**
```env
LOG_LEVEL=info
WORKERS=4
RATE_LIMIT_PER_MINUTE=100
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 4. Add Database (Optional)

If you need persistent storage:

1. In Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically sets `DATABASE_URL` environment variable

### 5. Add Redis (Optional)

For caching and Celery queue:

1. Click "New" → "Database" → "Redis"
2. Railway automatically sets `REDIS_URL`

### 6. Configure Custom Domain

1. Go to Settings → Domains
2. Click "Generate Domain" (free .railway.app subdomain)
3. Or add custom domain:
   - Click "Custom Domain"
   - Enter your domain
   - Add CNAME record to your DNS

---

## 🔧 Post-Deployment Configuration

### Verify Deployment

```bash
# Check health endpoint
curl https://your-app.railway.app/health

# Should return:
# {"status":"healthy","service":"threat-intel-api","version":"1.0.0"}
```

### Access API Documentation

Visit: `https://your-app.railway.app/docs`

### Test Authentication

```bash
curl -X POST https://your-app.railway.app/auth/token \
  -d "username=demo&password=demopassword"
```

---

## 📊 Monitoring & Logs

### View Logs

**Railway Dashboard:**
- Go to your project → Deployments
- Click on active deployment
- View real-time logs

**Railway CLI:**
```bash
railway logs
```

### Metrics

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Network traffic
- Deployment history

Access: Project → Deployments → Metrics

---

## 🔄 Automatic Deployments

### GitHub Integration

Railway automatically deploys when you push to main branch:

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update API"
   git push origin main
   ```

2. Railway detects changes and deploys automatically
3. View deployment status in Railway dashboard

### Branch Deployments

Deploy specific branches:

1. Go to Settings → Environments
2. Add new environment
3. Link to specific branch
4. Each branch gets its own deployment URL

---

## 💰 Pricing & Limits

### Free Tier (Starter Plan)
- $5 credit per month
- ~500 hours of usage
- 512MB RAM
- 1GB storage
- Perfect for demos and testing

### Paid Tiers
- **Hobby:** $5/month per environment
- **Pro:** $20/month per environment
- Higher resources and limits

---

## 🐛 Troubleshooting

### Build Fails

**Check build logs:**
```bash
railway logs --deployment
```

**Common issues:**
- Missing dependencies → Check `requirements.txt`
- Python version mismatch → Check `runtime.txt`
- Build timeout → Reduce dependencies

### App Crashes

**Check runtime logs:**
```bash
railway logs
```

**Common issues:**
- Missing environment variables → Add in Railway dashboard
- Port configuration → Use `$PORT` environment variable
- Memory limit exceeded → Upgrade plan or optimize code

### Health Check Fails

**Verify endpoint:**
```bash
curl https://your-app.railway.app/health
```

**If fails:**
- Check logs for startup errors
- Verify port is `$PORT`
- Ensure `/health` endpoint exists

### Database Connection Issues

**If using Railway PostgreSQL:**
- Verify `DATABASE_URL` is set automatically
- Check database is running
- Test connection:
  ```bash
  railway run psql $DATABASE_URL
  ```

---

## 🔒 Security Best Practices

### Environment Variables

✅ **DO:**
- Use Railway's environment variables for secrets
- Rotate `SECRET_KEY` regularly
- Use different keys for staging/production

❌ **DON'T:**
- Commit `.env` files to Git
- Share secrets in logs or public channels
- Use default demo credentials in production

### CORS Configuration

Update `ALLOWED_ORIGINS`:
```env
ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

### Rate Limiting

Adjust based on your needs:
```env
RATE_LIMIT_PER_MINUTE=100  # Increase for production
```

---

## 📈 Scaling

### Horizontal Scaling

Railway supports multiple instances:

1. Go to Settings → Scaling
2. Increase replica count
3. Railway handles load balancing automatically

### Vertical Scaling

Upgrade resources:

1. Settings → Resources
2. Increase RAM/CPU allocation
3. Available on paid plans

---

## 🔄 Rolling Back

### Revert to Previous Deployment

1. Go to Deployments
2. Find stable deployment
3. Click "Redeploy"
4. Confirm rollback

### Via CLI

```bash
railway rollback
```

---

## 🌐 Multiple Environments

### Setup Staging Environment

1. Go to Environments → New Environment
2. Name it "Staging"
3. Link to `develop` branch
4. Configure separate variables

### Production Environment

Keep `production` environment on `main` branch

---

## 📝 Checklist

Before going live:

- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_ORIGINS` with real domains
- [ ] Add custom domain
- [ ] Enable HTTPS (automatic with Railway)
- [ ] Set up monitoring/alerts
- [ ] Configure database backups
- [ ] Test all endpoints
- [ ] Set up CI/CD
- [ ] Document API for users
- [ ] Configure rate limiting
- [ ] Add error tracking (Sentry)

---

## 🆘 Support

**Railway Documentation:** https://docs.railway.app  
**Railway Discord:** https://discord.gg/railway  
**Project Issues:** GitHub Issues  

---

## 📊 Example Railway Project Structure

```
Railway Project: Threat Intelligence Platform
├── threat-intel-api (Main service)
│   └── Environment Variables
│       ├── SECRET_KEY
│       ├── ALLOWED_ORIGINS
│       └── LOG_LEVEL
├── PostgreSQL (Optional)
│   └── DATABASE_URL (auto-set)
├── Redis (Optional)
│   └── REDIS_URL (auto-set)
└── Custom Domain
    └── threat-intel.yourdomain.com
```

---

**Ready to deploy! 🚀**

For questions, see DEPLOYMENT.md or open an issue on GitHub.
