# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-31

### Added
- Initial release of Threat Intelligence Platform
- Phishing detection with Vision Transformer (ViT)
- Malware analysis with multi-modal ensemble (CNN+RNN+GNN)
- FastAPI backend with OAuth2 authentication
- Gradio interactive UI
- Streamlit analytics dashboard
- Docker Compose infrastructure
- Comprehensive test suite (80%+ coverage)
- CI/CD pipeline with GitHub Actions
- Railway and Vercel deployment configurations
- Prometheus + Grafana monitoring setup
- Complete documentation (README, API docs, deployment guide)

### Features
- `/scan/phishing` - URL threat detection
- `/scan/malware` - Binary file analysis
- `/auth/*` - JWT-based authentication
- Rate limiting (100 req/min)
- Real-time analytics dashboard
- Mock predictions for demo purposes
- Comprehensive error handling
- Input validation and sanitization

### Infrastructure
- Multi-container Docker setup
- PostgreSQL database
- Redis caching and queue
- MLflow experiment tracking
- Prometheus metrics collection
- Grafana dashboards

### Security
- OAuth2 password flow
- JWT token authentication
- Rate limiting middleware
- Input sanitization
- CORS configuration

### Documentation
- Comprehensive README with badges
- API documentation with examples
- Deployment guide for multiple platforms
- Contributing guidelines
- Code of conduct

---

## [Unreleased]

### Planned
- Real model training with GPU support
- PhishTank dataset integration
- VirusShare malware samples
- Next.js production dashboard
- SHAP/LIME explainability
- Active learning pipeline
- ONNX model export
- Kubernetes deployment manifests
- Custom domain setup
- Production monitoring alerts

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements
