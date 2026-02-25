# OpenClaw Verifier API

REST API for programmatic access

## Base URL

```
https://api.openclaw-verifier.com/v1
```

## Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.openclaw-verifier.com/v1/scan
```

## Endpoints

### POST /scan

Scan a skill for security issues.

**Request:**
```json
{
  "skill_url": "https://github.com/user/skill-name",
  "skill_path": "/path/to/skill",
  "options": {
    "deep_scan": true,
    "check_dependencies": true
  }
}
```

**Response:**
```json
{
  "scan_id": "scan_abc123",
  "status": "completed",
  "score": 85,
  "risk_level": "LOW",
  "files_scanned": 5,
  "issues": [
    {
      "severity": "medium",
      "category": "external_api",
      "description": "External API calls detected",
      "file": "SKILL.md",
      "line": 15,
      "recommendation": "Review external API endpoints for data privacy"
    }
  ],
  "recommendations": [
    "Add rate limiting to external API calls",
    "Implement input validation"
  ]
}
```

### GET /scan/{scan_id}

Get scan results.

### GET /skills/{skill_id}/history

Get historical scan results for a skill.

### POST /batch

Scan multiple skills.

**Request:**
```json
{
  "skills": [
    {"url": "https://github.com/user/skill1"},
    {"url": "https://github.com/user/skill2"}
  ]
}
```

### GET /reports/{scan_id}

Download scan report.

**Formats:** json, pdf, html

## Webhooks

### POST /webhooks

Register a webhook for scan completion.

```json
{
  "url": "https://your-server.com/webhook",
  "events": ["scan.completed", "scan.failed"]
}
```

## Rate Limits

| Plan | Requests/hour |
|------|---------------|
| Free | 10 |
| Basic | 100 |
| Pro | 1,000 |
| Enterprise | Unlimited |

## SDKs

### Python

```python
from openclaw_verifier import Verifier

client = Verifier(api_key="your_api_key")
result = client.scan("/path/to/skill")
print(f"Score: {result.score}")
```

### JavaScript

```javascript
import { Verifier } from 'openclaw-verifier';

const client = new Verifier({ apiKey: 'your_api_key' });
const result = await client.scan('/path/to/skill');
console.log(`Score: ${result.score}`);
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Rate limit exceeded |
| 404 | Skill not found |
| 500 | Server error |
