# Training Guide

## Overview
This guide explains how to train custom job scam detection models.

---

## Data Preparation

### 1. Data Format
Create a CSV file with these columns:
- `text`: Job posting text (required)
- `label`: 0 = legitimate, 1 = scam (required)

**Example:**
```csv
text,label
"Software Engineer at Google. 5 years experience required.",0
"Pay $99 to start! Earn $500/day! No interview!!!",1
```

### 2. Data Collection Sources

**Legitimate Jobs:**
- LinkedIn job postings
- Indeed job descriptions
- Company career pages
- Government job boards

**Scam Jobs:**
- Reported scams from r/Scams
- Federal Trade Commission (FTC) reports
- Kaggle scam datasets
- User-reported examples

### 3. Data Quality Guidelines

✅ **Do:**
- Include diverse job types
- Balance legitimate vs scam samples
- Include various scam tactics
- Use real-world examples
- Clean and preprocess text

❌ **Don't:**
- Use duplicates
- Include incomplete data
- Have extreme class imbalance
- Use synthetic-only data

---

## Training Process

### Step 1: Place Your Data
```bash
# Create directory structure
mkdir -p data/raw

# Place your CSV file
# data/raw/job_scams.csv
```

### Step 2: Run Training Script
```bash
python train_model.py
```

### Step 3: Review Results
The script will output:
- Training/test split sizes
- Feature count
- Classification metrics
- Sample predictions
- Model save location

**Example Output:**
```
==================================================
CLASSIFICATION REPORT
==================================================
              precision    recall  f1-score

Legitimate       0.87      0.92      0.89
Scam             0.91      0.85      0.88

ROC AUC Score: 0.9345
```

---

## Training Configuration

### Model Types
Edit `train_model.py` to choose model:

```python
# Options: 'logistic', 'random_forest', 'ensemble'
trainer.train_model(model_type='ensemble')
```

**Model Comparison:**

| Model | Speed | Accuracy | Interpretability |
|-------|-------|----------|------------------|
| Logistic Regression | ⚡⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Random Forest | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Ensemble | ⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### Hyperparameters

**TF-IDF Vectorizer:**
```python
TfidfVectorizer(
    max_features=5000,      # Maximum vocabulary size
    ngram_range=(1, 3),     # Use unigrams, bigrams, trigrams
    min_df=1,               # Minimum document frequency
    max_df=0.9              # Maximum document frequency
)
```

**Logistic Regression:**
```python
LogisticRegression(
    C=1.0,                  # Regularization strength
    max_iter=1000,          # Maximum iterations
    class_weight='balanced' # Handle imbalance
)
```

**Random Forest:**
```python
RandomForestClassifier(
    n_estimators=100,       # Number of trees
    max_depth=20,           # Maximum tree depth
    class_weight='balanced'
)
```

---

## Handling Class Imbalance

The script automatically applies SMOTE:
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)
```

**Alternative strategies:**
- Collect more minority class samples
- Use class weights
- Try other sampling methods (ADASYN, BorderlineSMOTE)

---

## Evaluation Metrics

### Primary Metrics

**Precision**: Of predicted scams, how many are actually scams?
- Goal: > 85% (minimize false positives)

**Recall**: Of actual scams, how many did we catch?
- Goal: > 90% (maximize scam detection)

**F1 Score**: Harmonic mean of precision and recall
- Goal: > 88%

**ROC AUC**: Overall classification quality
- Goal: > 0.90

### Confusion Matrix Interpretation
```
                 Predicted
               Legit  Scam
Actual Legit    TN     FP   ← False Positive (worst)
       Scam     FN     TP   ← False Negative (bad)
```

**For job scams:**
- False Negative (FN): Missed a scam - BAD
- False Positive (FP): Flagged legitimate job - WORST

---

## Improving Model Performance

### 1. More Data
- Collect 5,000+ samples minimum
- Include recent scam tactics
- Balance legitimate/scam ratio (40-60%)

### 2. Better Features
Add domain-specific features:
```python
# In feature_extractor.py
- Job board reputation
- Employer domain age
- Email verification
- LinkedIn profile checks
```

### 3. Advanced Models
Try transformer models:
```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=2
)
```

### 4. Ensemble Methods
Combine multiple models:
```python
VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier()),
        ('gb', GradientBoostingClassifier())
    ],
    voting='soft'
)
```

### 5. Feature Engineering
Create new features:
- Text statistics (length, caps ratio)
- Sentiment analysis
- Named entity recognition
- URL reputation scores

---

## Production Deployment

### 1. Model Versioning
```bash
models/saved_models/
├── scam_detector_v1.pkl
├── scam_detector_v2.pkl
└── scam_detector_latest.pkl  # symlink
```

### 2. A/B Testing
Test new models before full deployment:
```python
# Route 10% of traffic to new model
if random.random() < 0.1:
    model = load_model('v2.pkl')
else:
    model = load_model('v1.pkl')
```

### 3. Monitoring
Track metrics in production:
- Prediction distribution
- Average confidence
- Response times
- User feedback

### 4. Retraining Schedule
- Retrain monthly with new data
- Update rules for new scam patterns
- Incorporate user feedback

---

## Advanced: BERT Fine-tuning

For better accuracy, fine-tune BERT:

```python
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments

# Load pretrained model
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize data
train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=512
)

# Training arguments
training_args = TrainingArguments(
    output_dir='./models/bert',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch"
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

---

## Troubleshooting

### Low Accuracy
- ✅ Check data quality
- ✅ Increase dataset size
- ✅ Try different models
- ✅ Adjust hyperparameters

### Overfitting
- ✅ Reduce model complexity
- ✅ Add regularization
- ✅ Get more training data
- ✅ Use cross-validation

### High False Positives
- ✅ Adjust decision threshold
- ✅ Add more legitimate examples
- ✅ Review feature importance
- ✅ Implement confidence filtering

### Slow Training
- ✅ Reduce max_features
- ✅ Use simpler models
- ✅ Sample large datasets
- ✅ Use GPU (for deep learning)

---

## Best Practices

1. **Version Control**: Track model versions and training data
2. **Documentation**: Document model changes and performance
3. **Testing**: Always test on held-out data
4. **Monitoring**: Track production performance
5. **Updates**: Regular retraining with new patterns
6. **Ethics**: Minimize harm from false positives/negatives

---

## Resources

- [scikit-learn Documentation](https://scikit-learn.org/)
- [Imbalanced-learn Guide](https://imbalanced-learn.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [MLflow for Experiment Tracking](https://mlflow.org/)
