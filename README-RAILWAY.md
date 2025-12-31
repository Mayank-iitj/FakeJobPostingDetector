# 🚀 Railway Quick Start

**Deploy in under 5 minutes!**

## One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

---

## CLI Deploy

### Windows
```cmd
railway-up.bat
```

### Linux/Mac
```bash
chmod +x railway-up.sh
./railway-up.sh
```

---

## Environment Variables

After deployment, add these in Railway dashboard:

### Required
```env
SECRET_KEY=<generate-random-key>
```

Generate key:
```python
import secrets; print(secrets.token_urlsafe(32))
```

### Optional
```env
ALLOWED_ORIGINS=https://your-frontend.com
LOG_LEVEL=info
WORKERS=4
RATE_LIMIT_PER_MINUTE=100
```

---

## Test Deployment

```bash
# View live URL
railway open

# Test health endpoint
curl https://your-app.railway.app/health

# View logs
railway logs
```

---

## Troubleshooting

### Build fails
```bash
railway logs --deployment
```

### App crashes
```bash
railway logs
```

### Environment variables
```bash
railway variables
```

---

## Full Documentation

See [RAILWAY.md](RAILWAY.md) for complete guide.

---

**Need help?** Open an issue or check Railway docs.
