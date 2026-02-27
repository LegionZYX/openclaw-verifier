---
name: auto-fix
description: Automatically fix security issues in skills
metadata:
  openclaw:
    emoji: 🔧
---

# Auto Fix

Automatically fix detected security issues in OpenClaw skills.

## When to Use

Use this skill when:
- verify-skill detected fixable issues
- Want to harden skill security
- Preparing skill for production use

## Input

- `skill_path`: Path to the skill (required)
- `issues`: List of issues to fix (from verify-skill)
- `backup`: Create backup before fixing (default: true)

## Fixable Issues

| Issue Type | Fix Method |
|------------|------------|
| Hardcoded secrets | Replace with environment variables |
| Unsafe eval | Replace with safer alternatives |
| Exposed API keys | Move to config file |
| Dangerous commands | Add safety wrappers |

## Output

```json
{
  "fixed": 3,
  "skipped": 1,
  "backup_path": "/backups/skill-backup-20260226.zip",
  "changes": [
    {"file": "SKILL.md", "line": 15, "type": "secret_replacement"},
    {"file": "script.py", "line": 8, "type": "eval_removal"}
  ]
}
```

## Safety

- Always creates backup by default
- Only fixes known-safe patterns
- Skips complex issues requiring human review
