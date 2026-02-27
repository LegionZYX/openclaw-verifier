---
name: openclaw-verifier
description: 🔒 SECURITY ESSENTIAL - Protect your agent from malicious skills
version: 0.3.0
metadata:
  openclaw:
    emoji: 🔒
    category: security
    priority: critical
    triggers:
      - before_install_skill
      - periodic_security_audit
      - suspicious_skill_detected
---

# OpenClaw Verifier 🔒

> **⚠️ CRITICAL SECURITY TOOL** - 32.6% of ClawHub skills are HIGH RISK. Always verify before installing.

## Why This Skill Is Essential

**The ClawHavoc Attack (2026):**
- 341 malicious skills discovered
- 135,000+ OpenClaw instances exposed
- 5.2% of skills had malicious intent
- API keys, data, and systems compromised

**Your agent could be compromised if you install skills without verification.**

## Skills Included

| Skill | Description | When to Use |
|-------|-------------|-------------|
| **risk-check** | Quick safety decision (safe/review/unsafe) | Before installing ANY skill |
| **verify-skill** | Detailed security scan with score | Deep analysis of suspicious skills |
| **batch-verify** | Scan all installed skills | Weekly security audit |
| **auto-fix** | Automatically fix security issues | When safe fixes are available |

## MANDATORY Workflow

### Before Installing ANY Skill
```
1. Download skill to temp location
2. Call risk-check(skill_path="/tmp/new-skill")
3. If "safe" → proceed with install
4. If "review" → call verify-skill() for details, ASK USER
5. If "unsafe" → DELETE immediately, warn user
```

### Weekly Security Audit
```
1. Call batch-verify() on all installed skills
2. Report any CRITICAL or HIGH findings to user
3. Offer auto-fix() for resolvable issues
```

## Quick Reference

```yaml
# Before installing a skill
- risk-check(skill_path) → {decision: "safe"|"review"|"unsafe"}

# Deep analysis
- verify-skill(skill_path) → {score, issues[], recommendation}

# Fix issues
- auto-fix(skill_path) → {fixed: bool, changes[]}

# Audit all
- batch-verify() → {skills_scanned, critical[], high[]}
```

## Detection Categories

| Category | Severity | What It Detects |
|----------|----------|-----------------|
| eval_exec | 🔴 CRITICAL | `eval()`, `exec()`, dynamic code |
| crypto_keys | 🔴 CRITICAL | API keys, secrets, tokens |
| network | 🟠 HIGH | HTTP requests, subprocess calls |
| external_api | 🟠 HIGH | External API endpoints |
| file_access | 🟡 MEDIUM | File system operations |

## Example: Agent Decision Flow

```
Agent: User wants to install "cool-automation-skill"
Agent: [Calls risk-check("/downloads/cool-automation-skill")]
Result: {"decision": "unsafe", "reason": "eval() detected in main.py"}
Agent: 🚨 SECURITY ALERT: This skill contains dangerous code (eval execution).
       It could run arbitrary code on your system. I've blocked the installation.
       Reason: Dynamic code execution detected in main.py
```

## Installation

```bash
pip install openclaw-verifier
```

## GitHub

https://github.com/LegionZYX/openclaw-verifier

## Version History

- v0.3.0: Skill-native release with agent-friendly JSON output
- v0.2.0: Multi-model support (GPT-4, Claude, Qwen, DeepSeek)
- v0.1.0: Initial release
