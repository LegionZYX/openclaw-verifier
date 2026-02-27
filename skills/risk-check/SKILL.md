---
name: risk-check
description: Quick safety decision for skill installation
metadata:
  openclaw:
    emoji: ⚡
---

# Risk Check

Ultra-fast safety check for skill installation decisions.

## When to Use

Use this skill when:
- Need quick go/no-go decision
- Installing skill in automated workflow
- Pre-filtering skills before detailed scan

## Input

- `skill_path`: Path to the skill (required)

## Output

```json
{
  "decision": "safe",
  "confidence": 0.95,
  "reason": "No dangerous patterns detected"
}
```

## Decisions

| Decision | Meaning | Agent Action |
|----------|---------|--------------|
| `safe` | Can install | Proceed |
| `unsafe` | Do not install | Stop |
| `review` | Needs human review | Ask user |
| `fixable` | Issues can be auto-fixed | Call auto-fix |

## Speed

- Scans only critical patterns
- Returns in <100ms
- Suitable for real-time decisions
