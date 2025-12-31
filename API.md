# API Documentation

## Base URL
```
Production: https://your-domain.railway.app
Development: http://localhost:8000
```

## Authentication

All API endpoints (except `/health`) require authentication using JWT tokens.

### Get Token
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=demo&password=demopassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Use Token
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Endpoints

### 🎣 Phishing Detection

#### Scan URL
```bash
POST /scan/phishing
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://suspicious-site.com",
  "capture_screenshot": true,
  "analyze_dom": true
}
```

**Response:**
```json
{
  "scan_id": "phish_1704009600",
  "url": "https://suspicious-site.com",
  "verdict": "PHISH",
  "risk_score": 0.94,
  "confidence": 0.97,
  "explanation": "Suspicious form detected, SSL certificate mismatch",
  "features": {
    "vit_score": 0.92,
    "dom_score": 0.96,
    "fusion_score": 0.94
  },
  "screenshot_url": "https://screenshots.example.com/...",
  "scan_time_ms": 487,
  "timestamp": "2025-12-31T09:00:00Z"
}
```

#### Bulk Scan
```bash
POST /scan/phishing/bulk
Authorization: Bearer {token}

{
  "urls": [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com"
  ]
}
```

**Response:**
```json
{
  "task_id": "bulk_1704009600",
  "total_urls": 3,
  "estimated_time_seconds": 6
}
```

---

### 🦠 Malware Analysis

#### Analyze Binary
```bash
POST /scan/malware
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <binary file>
```

**Response:**
```json
{
  "scan_id": "malware_1704009600",
  "filename": "suspicious.exe",
  "file_type": "PE",
  "sha256": "abc123...",
  "file_size_kb": 2048,
  "family": "Emotet",
  "confidence": 0.97,
  "threat_score": 9.2,
  "behaviors": ["ransomware", "trojan", "backdoor"],
  "features": {
    "cnn_score": 0.95,
    "rnn_score": 0.98,
    "gnn_score": 0.99,
    "ensemble_score": 0.97
  },
  "indicators": {
    "persistence": true,
    "network_activity": true,
    "file_operations": true,
    "registry_modifications": true
  },
  "scan_time_ms": 1243,
  "timestamp": "2025-12-31T09:00:00Z"
}
```

#### Query by Hash
```bash
GET /scan/malware/hash/{sha256}
Authorization: Bearer {token}
```

#### List Families
```bash
GET /scan/malware/families
```

**Response:**
```json
{
  "total": 15,
  "families": [
    "BadRabbit",
    "BlackMatter",
    "Cerber",
    "DarkSide",
    "Dridex",
    "Emotet",
    "Locky",
    "Maze",
    "NotPetya",
    "Petya",
    "REvil",
    "Ryuk",
    "TrickBot",
    "WannaCry",
    "Zeus"
  ]
}
```

---

## Rate Limiting

**Default Limits:**
- 100 requests per minute per IP
- Bulk scans: Max 100 URLs per request

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1704009660
```

**429 Response:**
```json
{
  "error": "Rate limit exceeded",
  "max_requests": 100,
  "window_seconds": 60,
  "retry_after": 60
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 413 | Payload Too Large |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Examples

### Python
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/token",
    data={"username": "demo", "password": "demopassword"}
)
token = response.json()["access_token"]

# Scan phishing
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/scan/phishing",
    json={"url": "https://suspicious.com"},
    headers=headers
)
print(response.json())
```

### cURL
```bash
# Get token
TOKEN=$(curl -X POST http://localhost:8000/auth/token \
  -d "username=demo&password=demopassword" \
  | jq -r .access_token)

# Scan URL
curl -X POST http://localhost:8000/scan/phishing \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious.com"}'
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=demo&password=demopassword'
});
const { access_token } = await loginResponse.json();

// Scan URL
const scanResponse = await fetch('http://localhost:8000/scan/phishing', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ url: 'https://suspicious.com' })
});
const result = await scanResponse.json();
console.log(result);
```

---

## Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-31
