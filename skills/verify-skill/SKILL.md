---
name: verify-skill
description: Scan an OpenClaw skill for security issues
metadata:
  openclaw:
    emoji: 🔒
---

# Verify Skill

Scan an OpenClaw skill for security vulnerabilities and return structured results.

## When to Use

Use this skill when:
- Installing a new skill from an untrusted source
- Auditing existing skills
- Checking skill safety before execution

## Input

- `skill_path`: Path to the skill directory (required)
- `model`: AI model for analysis (optional: local, qwen-coding, gpt-4)

## Workflow

1. Check if SKILL.md exists
2. Scan all files for malicious patterns
3. Calculate security score (0-100)
4. Return structured JSON result

## Output Format

```json
{
  "safe": true,
  "score": 85,
  "risk_level": "LOW",
  "files_scanned": 5,
  "issues": [
    {
      "severity": "medium",
      "category": "external_api",
      "description": "External API calls detected",
      "file": "SKILL.md",
      "line": 15
    }
  ],
  "recommendation": "Safe to install"
}
```

## Risk Levels

| Level | Score | Action |
|-------|-------|--------|
| LOW | 90-100 | Safe to install |
| MEDIUM | 70-89 | Review recommended |
| HIGH | 50-69 | Install with caution |
| CRITICAL | 0-49 | Do not install |

## Example Usage

```
Agent: I want to install skill from /downloads/new-skill
Agent calls: verify-skill(skill_path="/downloads/new-skill")
Result: {"safe": true, "score": 95, ...}
Agent: Safe to install, proceeding...
```

## Detection Categories

1. **eval_exec** (CRITICAL) - Dynamic code execution
2. **external_api** (HIGH) - External API calls
3. **file_access** (MEDIUM) - File system access
4. **network** (HIGH) - Network operations
5. **crypto_keys** (CRITICAL) - API keys/secrets
