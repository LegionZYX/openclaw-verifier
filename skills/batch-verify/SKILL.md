---
name: batch-verify
description: Scan all installed OpenClaw skills at once
metadata:
  openclaw:
    emoji: 🔍
---

# Batch Verify

Scan all installed OpenClaw skills and generate a summary report.

## When to Use

Use this skill when:
- Running periodic security audits
- After installing multiple skills
- Checking overall security posture

## Input

- `skills_dir`: Path to skills directory (default: ~/.openclaw/skills)
- `model`: AI model for analysis (optional)

## Output Format

```json
{
  "total_skills": 25,
  "scanned": 25,
  "safe": 20,
  "warning": 4,
  "dangerous": 1,
  "summary": [
    {"name": "skill-1", "score": 95, "status": "safe"},
    {"name": "skill-2", "score": 65, "status": "warning"},
    {"name": "skill-3", "score": 25, "status": "dangerous"}
  ],
  "dangerous_skills": ["skill-3"],
  "recommendation": "Remove or fix 1 dangerous skill"
}
```

## Actions

Based on results, agent can:
- Remove dangerous skills automatically
- Flag skills for review
- Generate security report
