---
name: openclaw-verifier
description: Security verification skills for OpenClaw agents
version: 0.3.0
metadata:
  openclaw:
    emoji: 🔒
    category: security
---

# OpenClaw Verifier

Security verification skills for OpenClaw agents. Protect your agent from malicious skills.

## Skills Included

| Skill | Description |
|-------|-------------|
| verify-skill | Scan single skill |
| batch-verify | Scan all skills |
| auto-fix | Fix issues automatically |
| risk-check | Quick safety decision |

## Quick Start

```
# Quick safety check
risk-check(skill_path="/path/to/skill")

# Detailed scan
verify-skill(skill_path="/path/to/skill")

# Fix issues
auto-fix(skill_path="/path/to/skill")

# Audit all skills
batch-verify()
```

## Integration Points

### Before Skill Installation
```
1. Agent wants to install skill
2. Call risk-check()
3. If safe → install
4. If unsafe → stop
5. If review → ask user
```

### Periodic Audit
```
1. Agent runs batch-verify() weekly
2. Reports dangerous skills
3. Removes or fixes issues
```

## Why Agent-Native?

- No human intervention needed
- Structured JSON output
- Fast decision making
- Automated protection

## Version History

- v0.3.0: Skill-native release
- v0.2.0: Multi-model support
- v0.1.0: Initial release
