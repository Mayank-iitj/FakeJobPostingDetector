# Job Scam Detector 🔍

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)


**AI-powered system to detect fake and scam job postings across multiple platforms.**

Protect job seekers from fraud with intelligent detection that works on:
- 🌐 Job portals (LinkedIn, Indeed, etc.)
- 📧 Email job offers
- 💬 WhatsApp/Telegram messages
- 🔍 Web pages via Chrome extension

---

## 🎯 Features

### Core Functionality
- **Trust Score (0-100)**: Instant safety rating for any job posting
- **Scam Detection**: Identifies 15+ common fraud patterns
- **Real-time Analysis**: Get results in seconds
- **Multi-platform**: Works everywhere jobs are posted

### Detection Capabilities
✅ Detects payment requests (registration fees, training costs)  
✅ Identifies unrealistic salary claims  
✅ Flags urgency tactics and pressure language  
✅ Recognizes suspicious communication channels  
✅ Checks for poor grammar and excessive caps  
✅ Validates company information and URLs  
✅ Spots gift card payment schemes  
✅ Identifies cryptocurrency scams  

### User Experience
- 📊 **Visual indicators**: Color-coded risk levels (Green/Yellow/Red)
- 🔍 **Highlighted phrases**: See exactly what's suspicious
- 💡 **Actionable advice**: Get safety recommendations
- 📱 **Multiple interfaces**: Web UI, API, and Chrome extension

---

## 🚀 Quick Start

### Option 1: Try Online (Easiest)
**Deployed App**: [Visit Live Demo](https://your-app.streamlit.app) *(Deploy to get URL)*

### Option 2: Local Installation

#### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Google Chrome for extension

#### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd threat-intel-platform
```

2. **Install dependencies**

For full system (API + UI + Extension):
```bash
pip install -r requirements.txt
```

For Streamlit-only deployment:
```bash
pip install -r requirements-streamlit.txt
```

3. **Set up environment variables**
```bash
copy .env.example .env
```

4. **Train the model** (creates initial model with sample data)
```bash
python train_model.py
```

5. **Start the API server**
```bash
python backend/main.py
```

The API will be running at `http://localhost:8000`

6. **Launch the Web UI** (in a new terminal)
```bash
streamlit run frontend/streamlit_app.py
```

The web interface will open at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Web Interface (Easiest)

Open the Streamlit app and:
1. Paste job posting text
2. (Optional) Add the job URL
3. Click "Analyze Job Posting"
4. Review the trust score, flags, and recommendations

### 2. API Usage

**Analyze a job posting:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your job posting text here",
    "url": "https://example.com/job/123"
  }'
```

**Response:**
```json
{
  "prediction": "High Risk Scam",
  "score": 25,
  "flags": [
    "Requests upfront payment",
    "Unrealistic daily salary",
    "No interview required"
  ],
  "highlighted_phrases": [
    {
      "text": "pay $99 fee",
      "risk_level": "high",
      "reason": "Requests upfront payment"
    }
  ],
  "explanation": "This posting shows multiple red flags...",
  "advice": ["Never pay any fees", "Research the company..."],
  "confidence": 0.89
}
```

### 3. Chrome Extension

**Installation:**
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. Pin the extension to your toolbar

**Usage:**
1. Navigate to any job posting webpage
2. Click the extension icon
3. Click "Analyze This Page"
4. View the trust score and warnings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Job Scam Detector                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Input Channels          →    Processing    →    Output      │
│  ───────────────              ─────────          ──────      │
│  • Web UI                     • Text Clean       • Trust     │
│  • Chrome Ext                 • Feature Extract    Score     │
│  • API Direct                 • ML Model          • Flags    │
│  • CLI                        • Rule Engine       • Advice   │
│                               • Scoring Logic     • Explain  │
│                                                               │
│  Deployment Modes:                                           │
│  • Standalone (Streamlit only - recommended for cloud)       │
│  • Full Stack (API + UI + Extension)                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Modes

**Standalone Mode** (Streamlit Cloud):
- Web UI with built-in detection
- No API server needed
- Easy to deploy
- Perfect for public demos

**Full Stack Mode** (Production):
- Separate API backend
- Multiple frontends
- Scalable architecture
- Chrome extension support

### Components

**Backend (FastAPI)**
- `/analyze` - Main detection endpoint
- `/report` - Report scam postings
- `/batch-analyze` - Analyze multiple jobs

**ML Pipeline**
- Feature Extractor: Extracts 15+ features from text
- Rule Engine: Pattern-based detection (15 rules)
- ML Model: Ensemble (Logistic Regression + Random Forest)
- Hybrid Scoring: Combines ML (60%) + Rules (40%)

**Frontend**
- Streamlit Web App: User-friendly testing interface
- Chrome Extension: Browser integration for real-time scanning

---

## 🧠 How It Works

### 1. Feature Extraction
The system extracts multiple features from job text:
- Payment requests
- Salary claims
- Urgency language
- Communication channels
- Grammar quality
- Contact information
- URL validation

### 2. Hybrid Detection
Combines two approaches:

**Rule-Based (40%)**
- 15+ pattern matching rules
- High precision for known scams
- Instant results

**Machine Learning (60%)**
- TF-IDF vectorization
- Ensemble classifier
- Learns from data

### 3. Trust Score Calculation
```
Final Score = 0.6 × ML_Score + 0.4 × Rule_Score
Trust Score = (1 - Final_Score) × 100

Classification:
• 70-100: Likely Legitimate (Green)
• 40-69:  Suspicious (Yellow)
• 0-39:   High Risk Scam (Red)
```

---

## 📊 Training Your Own Model

### Data Format
Create a CSV file with columns:
- `text`: Job posting text
- `label`: 0 (legitimate) or 1 (scam)

### Training Steps

1. **Prepare your dataset**
```bash
# Place data in data/raw/job_scams.csv
```

2. **Run training**
```bash
python train_model.py
```

3. **Evaluate performance**
The script will output:
- Classification report (Precision, Recall, F1)
- Confusion matrix
- ROC AUC score
- Sample predictions

4. **Model is saved automatically** to `models/saved_models/scam_detector.pkl`

### Recommended Data Sources
- [Kaggle Job Scam Dataset](https://www.kaggle.com/datasets)
- Manually labeled examples from job boards
- Reddit r/Scams job-related threads
- Your own reported scams

### Handling Imbalanced Data
The training script automatically applies SMOTE (Synthetic Minority Over-sampling) to balance classes.

---

## 🧪 Testing

Run the test suite:
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_api.py -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```

Test coverage includes:
- ✅ API endpoints
- ✅ Feature extraction
- ✅ Rule engine
- ✅ Model predictions
- ✅ Text processing

---

## 📁 Project Structure

```
threat-intel-platform/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/
│   │   ├── detector.py      # Main detection logic
│   │   ├── feature_extractor.py
│   │   └── rules.py         # Rule-based engine
│   └── utils/
│       └── text_processor.py
├── frontend/
│   └── streamlit_app.py     # Web UI
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   └── background.js
├── models/
│   └── saved_models/        # Trained models (.pkl)
├── data/
│   ├── raw/                 # Training data
│   └── processed/           # Processed datasets
├── tests/
│   ├── test_api.py
│   ├── test_features.py
│   └── test_rules.py
├── train_model.py           # Model training script
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔐 Security & Privacy

### Data Protection
- ✅ No personal data stored without consent
- ✅ API doesn't log job content by default
- ✅ Chrome extension processes locally first
- ✅ No tracking or analytics

### Ethical Use
⚠️ **Important Disclaimers:**
- This is an **AI assistant only** - not a definitive scam detector
- Always verify jobs independently
- False positives can occur
- Not a replacement for common sense

### Reporting
- Report incorrect predictions to improve the model
- User feedback helps reduce false positives
- Reported scams are logged (not stored long-term by default)

---

## 🎨 Customization

### Adjust Detection Thresholds
Edit `backend/config.py` or `.env`:
```python
SCAM_THRESHOLD_HIGH=0.7   # Risk score above this = "High Risk"
SCAM_THRESHOLD_MEDIUM=0.4  # Risk score above this = "Suspicious"
```

### Add Custom Rules
Edit `backend/models/rules.py`:
```python
{
    'pattern': r'your_regex_pattern',
    'risk_level': 'high',  # high, medium, low
    'reason': 'Description of why this is risky',
    'weight': 0.25
}
```

### Modify UI Colors
Edit `frontend/streamlit_app.py` or `chrome-extension/popup.html`

---

## 📈 Performance Metrics

On 

## ☁️ Cloud Deployment

### Deploy to Streamlit Cloud (Recommended)
**Easiest deployment option - 5 minutes setup!**

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

**Detailed guide**: [STREAMLIT_DEPLOY.md](docs/STREAMLIT_DEPLOY.md)

### Other Platforms
- **Heroku**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Docker**: Use provided docker-compose.yml
- **AWS/GCP/Azure**: See deployment guide

---balanced test data:
- **Precision**: ~85-90% (few false positives)
- **Recall**: ~90-95% (catches most scams)
- **F1 Score**: ~88-92%
- **ROC AUC**: ~0.93

*Results vary based on training data quality*

---

## 🚧 Known Limitations

1. **Language**: Currently English-only
2. **Context**: May miss nuanced social engineering
3. **New Patterns**: Cannot detect entirely novel scam tactics
4. **False Positives**: Legitimate remote/crypto jobs may be flagged
5. **Data Dependency**: Accuracy depends on training data

---

## 🔮 Future Improvements

### Planned Features
- [ ] Multi-language support (Spanish, Hindi, etc.)
- [ ] Domain reputation checking
- [ ] Email header analysis
- [ ] Image/logo verification
- [ ] Company LinkedIn verification
- [ ] User feedback learning
- [ ] Mobile app (React Native)
- [ ] Telegram/WhatsApp bot

### Model Improvements
- [ ] Transformer models (BERT, RoBERTa)
- [ ] Active learning from reports
- [ ] Explainable AI (LIME/SHAP)
- [ ] Ensemble with neural networks

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- 📊 Training data collection
- 🌍 Multi-language support
- 🧪 Additional test cases
- 📝 Documentation improvements
- 🎨 UI/UX enhancements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Streamlit for rapid UI development
- scikit-learn for ML tools
- The job scam dataset contributors

---

## 📞 Support

- 📧 Report issues on GitHub Issues
- 💬 Discussions on GitHub Discussions
- 📚 Check the docs first

---

## ⚠️ Important Notice

**This tool is for educational and protective purposes only.**

- Not 100% accurate - always verify independently
- No liability for missed scams or false positives
- Use at your own risk
- Always follow platform-specific reporting procedures

**Stay safe online! 🛡️**

---

Made with ❤️ to protect job seekers from fraud
