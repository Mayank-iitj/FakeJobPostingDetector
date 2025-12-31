# Deployment Guide

## 🚀 Deployment Options

### Option 1: Railway (Recommended for Backend)

**Quick Deploy:**
```bash
# Windows
deploy_railway.bat

# Linux/Mac
chmod +x deploy_railway.sh
./deploy_railway.sh
```

**Manual Steps:**
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`
5. Add environment variables in Railway dashboard

**Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `MLFLOW_TRACKING_URI` - MLflow server URL

---

### Option 2: Vercel (Frontend/API)

**Quick Deploy:**
```bash
npm install -g vercel
vercel login
vercel deploy --prod
```

**Configuration:**
- Uses `vercel.json` for routing
- Supports serverless Python functions
- Good for Gradio UI hosting

---

### Option 3: Docker Compose (Local/VPS)

**Start All Services:**
```bash
cd docker
docker-compose up -d
```

**Services Available:**
- API: http://localhost:8000
- Gradio: http://localhost:7860
- Streamlit: http://localhost:8501
- MLflow: http://localhost:5000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

**Update Services:**
```bash
docker-compose pull
docker-compose up -d --force-recreate
```

---

### Option 4: Kubernetes (Production)

**Coming Soon** - Helm charts and K8s manifests

---

## 🔧 Post-Deployment Setup

### 1. Database Migration
```bash
# Run migrations
alembic upgrade head
```

### 2. Load Demo Data
```bash
# Load sample phishing URLs
python scripts/load_demo_data.py
```

### 3. Test Endpoints
```bash
# Health check
curl https://your-domain.railway.app/health

# API docs
curl https://your-domain.railway.app/docs
```

### 4. Configure Monitoring
- Set up Sentry DSN for error tracking
- Configure Prometheus targets
- Import Grafana dashboards

---

## 🎨 Frontend Deployments

### Gradio UI
```bash
# Standalone deployment
python ui/gradio_app.py

# Or use Docker
docker build -f docker/gradio.Dockerfile -t threat-intel-gradio .
docker run -p 7860:7860 threat-intel-gradio
```

### Streamlit Dashboard
```bash
# Standalone
streamlit run ui/streamlit_app.py

# Or Docker
docker build -f docker/streamlit.Dockerfile -t threat-intel-streamlit .
docker run -p 8501:8501 threat-intel-streamlit
```

---

## 🔒 Security Checklist

- [ ] Change default `SECRET_KEY` in `.env`
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS allowed origins
- [ ] Set up rate limiting (default: 100 req/min)
- [ ] Enable OAuth2 authentication
- [ ] Review and update firewall rules
- [ ] Set up backup schedules

---

## 📊 Monitoring Setup

### Prometheus + Grafana

1. Access Grafana: http://localhost:3000
2. Default credentials: admin/admin
3. Add Prometheus datasource: http://prometheus:9090
4. Import dashboards from `config/grafana/dashboards/`

### Custom Metrics

API automatically exposes metrics at `/metrics`:
- Request count
- Response time
- Error rate
- Model inference time

---

## 🐛 Troubleshooting

### API won't start
```bash
# Check logs
docker-compose logs api

# Common issues:
# - Missing environment variables
# - Database connection failed
# - Port already in use
```

### Models not loading
```bash
# Check model paths
ls -l models/checkpoints/

# Download pretrained models
python scripts/download_models.py
```

### Database connection errors
```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Test connection
psql $DATABASE_URL
```

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow automatically:
1. Runs tests on every push
2. Builds Docker images
3. Deploys to Railway on main branch

**Setup:**
1. Add `RAILWAY_TOKEN` to GitHub Secrets
2. Push to main branch
3. Monitor deployment in Actions tab

---

## 📈 Scaling Tips

### Horizontal Scaling
- Use Railway's autoscaling
- Deploy multiple API instances behind load balancer
- Separate read/write database replicas

### Performance Optimization
- Enable Redis caching
- Use CDN for static assets
- Implement request queuing with Celery
- Use ONNX models for faster inference

---

## 🆘 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Review documentation: `/docs`
3. GitHub Issues: [github.com/yourname/threat-intel-platform/issues](https://github.com)

---

**Last Updated:** 2025-12-31
