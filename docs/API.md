# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### 2. Analyze Job Posting
```http
POST /analyze
```

**Request Body:**
```json
{
  "text": "Job posting text to analyze",
  "url": "https://example.com/job/123" // optional
}
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
      "text": "pay $99 registration fee",
      "risk_level": "high",
      "reason": "Requests upfront payment"
    }
  ],
  "explanation": "This posting shows multiple red flags typical of job scams...",
  "advice": [
    "🚨 NEVER pay any fees - this is a major scam indicator",
    "🔍 Research the company on LinkedIn and Google",
    "❌ Never pay any fees or send money"
  ],
  "confidence": 0.89
}
```

**Field Descriptions:**
- `prediction`: Classification result (Likely Legitimate / Suspicious / High Risk Scam)
- `score`: Trust score 0-100 (higher = safer)
- `flags`: List of scam indicators detected
- `highlighted_phrases`: Risky text with explanations
- `explanation`: Natural language reasoning
- `advice`: Actionable safety recommendations
- `confidence`: Model confidence 0-1

---

### 3. Report Scam
```http
POST /report
```

**Request Body:**
```json
{
  "text": "Scam job posting text",
  "url": "https://scam-site.com/job",
  "user_feedback": "Optional user comment"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Thank you for reporting..."
}
```

---

### 4. Batch Analysis
```http
POST /batch-analyze
```

**Request Body:**
```json
[
  "First job posting text",
  "Second job posting text",
  "Third job posting text"
]
```

**Response:**
```json
{
  "results": [
    {
      "prediction": "Likely Legitimate",
      "score": 82,
      // ... full analysis for each
    }
  ]
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid input)
- `500`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limiting

No rate limiting by default. For production:
- Consider adding API key authentication
- Implement rate limiting middleware
- Use caching for repeated requests

---

## CORS

CORS is enabled for all origins by default. Configure in `.env`:
```
CORS_ORIGINS=http://localhost:3000,https://yourapp.com
```

---

## Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Job posting text here",
        "url": "https://example.com/job/123"
    }
)

result = response.json()
print(f"Trust Score: {result['score']}")
print(f"Prediction: {result['prediction']}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Job posting text here',
    url: 'https://example.com/job/123'
  })
});

const result = await response.json();
console.log(`Trust Score: ${result.score}`);
```

### cURL
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Job posting text here"}'
```
