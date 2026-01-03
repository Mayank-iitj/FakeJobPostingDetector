# Deployment Guide

## Overview
This guide covers deploying the Job Scam Detector to production environments.

---

## Deployment Options

### 1. Local Development
```bash
# Already configured - see README.md
python backend/main.py
streamlit run frontend/streamlit_app.py
```

### 2. Docker Deployment

**Create Dockerfile for API:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY models/ ./models/
COPY train_model.py .

EXPOSE 8000

CMD ["python", "backend/main.py"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./models:/app/models

  frontend:
    image: python:3.9-slim
    working_dir: /app
    command: streamlit run frontend/streamlit_app.py
    ports:
      - "8501:8501"
    volumes:
      - ./frontend:/app/frontend
    depends_on:
      - api
```

**Run:**
```bash
docker-compose up -d
```

### 3. Cloud Platforms

#### **Heroku**
```bash
# Install Heroku CLI
heroku login
heroku create job-scam-detector

# Add Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

#### **AWS EC2**
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone and setup
git clone <repo>
cd threat-intel-platform
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/jobscam.service
```

#### **Google Cloud Run**
```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/job-scam-detector

# Deploy
gcloud run deploy job-scam-detector \
  --image gcr.io/PROJECT_ID/job-scam-detector \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### **Azure App Service**
```bash
# Login to Azure
az login

# Create resource group
az group create --name JobScamRG --location eastus

# Create app service plan
az appservice plan create --name JobScamPlan --resource-group JobScamRG --sku B1 --is-linux

# Deploy
az webapp up --name job-scam-detector --resource-group JobScamRG
```

---

## Production Configuration

### Environment Variables
```bash
# .env.production
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

MODEL_PATH=models/saved_models/scam_detector.pkl
MODEL_TYPE=ensemble

SCAM_THRESHOLD_HIGH=0.7
SCAM_THRESHOLD_MEDIUM=0.4

# Security
API_KEY_ENABLED=True
API_KEY=your-secure-api-key-here

# CORS - restrict to your domains
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com

LOG_LEVEL=WARNING
```

### Security Hardening

**1. Add API Key Authentication:**
```python
# backend/middleware/auth.py
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

**2. Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_job_post(request: JobAnalysisRequest):
    # ... existing code
```

**3. HTTPS Only:**
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

---

## Scaling Considerations

### Horizontal Scaling
Use load balancer with multiple API instances:
```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: job-scam-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: job-scam-api
  template:
    metadata:
      labels:
        app: job-scam-api
    spec:
      containers:
      - name: api
        image: job-scam-detector:latest
        ports:
        - containerPort: 8000
```

### Caching
Add Redis for frequently analyzed jobs:
```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def get_cached_result(text_hash):
    return redis_client.get(f"analysis:{text_hash}")

def cache_result(text_hash, result):
    redis_client.setex(f"analysis:{text_hash}", 3600, result)
```

### Database for Reports
Use PostgreSQL to store reported scams:
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScamReport(Base):
    __tablename__ = 'scam_reports'
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    url = Column(String)
    reported_at = Column(DateTime)
```

---

## Monitoring & Logging

### Application Monitoring
```python
# backend/monitoring.py
from prometheus_client import Counter, Histogram

# Metrics
analysis_counter = Counter('job_analysis_total', 'Total analyses')
scam_detected = Counter('scams_detected', 'Scams detected')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis duration')

@app.post("/analyze")
async def analyze_job_post(request: JobAnalysisRequest):
    with analysis_duration.time():
        result = detector.analyze(request.text)
        analysis_counter.inc()
        if result['score'] < 40:
            scam_detected.inc()
        return result
```

### Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10000000,
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)
```

### Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

---

## Chrome Extension Distribution

### Chrome Web Store
1. Create developer account ($5 fee)
2. Prepare store listing:
   - Icon (128x128)
   - Screenshots
   - Description
3. Create ZIP of chrome-extension folder
4. Upload to Chrome Web Store
5. Submit for review

### Update Manifest for Production
```json
{
  "manifest_version": 3,
  "name": "Job Scam Detector",
  "version": "1.0.0",
  "host_permissions": [
    "https://your-api-domain.com/*"
  ]
}
```

---

## Backup & Recovery

### Model Backups
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backups/models_$DATE.tar.gz models/saved_models/
aws s3 cp backups/models_$DATE.tar.gz s3://your-bucket/models/
```

### Database Backups
```bash
# PostgreSQL backup
pg_dump dbname > backups/db_$(date +%Y%m%d).sql
```

---

## Performance Optimization

### Model Optimization
1. **Convert to ONNX** for faster inference:
```python
import onnx
import skl2onnx

onnx_model = skl2onnx.convert_sklearn(model, initial_types=[...])
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

2. **Quantization** for smaller model size

3. **Model serving** with TensorFlow Serving or TorchServe

### API Optimization
- Enable Gzip compression
- Use async database queries
- Implement connection pooling
- Cache static responses

---

## Continuous Integration/Deployment

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest tests/
      
      - name: Deploy to production
        run: |
          # Your deployment commands
```

---

## Maintenance Schedule

**Daily:**
- Monitor error logs
- Check API uptime
- Review user reports

**Weekly:**
- Analyze prediction distribution
- Update scam patterns
- Review false positives/negatives

**Monthly:**
- Retrain model with new data
- Update dependencies
- Security audit

**Quarterly:**
- Performance review
- User feedback analysis
- Feature planning

---

## Rollback Plan

If deployment fails:
```bash
# Revert to previous version
git revert HEAD
git push

# Or restore from backup
aws s3 cp s3://your-bucket/models/backup.pkl models/saved_models/
systemctl restart jobscam
```

---

## Cost Estimation

**Small Scale (1000 requests/day):**
- Cloud hosting: $20-30/month
- Database: $10/month
- Total: ~$40/month

**Medium Scale (50k requests/day):**
- Cloud hosting: $100-150/month
- Database: $50/month
- CDN: $20/month
- Total: ~$200/month

**Large Scale (1M+ requests/day):**
- Kubernetes cluster: $500+/month
- Database: $200/month
- Caching: $100/month
- Total: $1000+/month

---

Stay secure in production! 🔒
