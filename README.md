# OpenClaw Verifier

[![PyPI version](https://badge.fury.io/py/openclaw-verifier.svg)](https://badge.fury.io/py/openclaw-verifier)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🔒 **Security verification tool for OpenClaw Skills**

OpenClaw Verifier scans your OpenClaw skills for security vulnerabilities, malicious code, and potential risks before installation.

## Why OpenClaw Verifier?

- **32.6% of ClawHub skills are CRITICAL** - Don't install blindly
- **341 malicious skills discovered** in 2026 (ClawHavoc attack)
- **5.2% show malicious intent** - Protect your API keys and data

## Features

- 🔍 **Static Code Analysis** - Detect malicious patterns
- 🎯 **5 Detection Categories** - eval/exec, external API, file access, network, crypto keys
- 📊 **Security Score** - 0-100 score with risk level
- 🖥️ **CLI + Web UI** - Use however you prefer
- 🔄 **CI/CD Integration** - GitHub Actions ready

## Installation

```bash
pip install openclaw-verifier
```

## Quick Start

### Scan a single skill

```bash
openclaw-verifier scan /path/to/skill
```

### Batch scan

```bash
openclaw-verifier batch /path/to/skills/directory
```

### Output formats

```bash
# JSON output
openclaw-verifier scan /path/to/skill --json

# Minimal output
openclaw-verifier scan /path/to/skill --quiet
```

## Example Output

```
============================================================
OpenClaw Skill Security Report
============================================================

Skill: ./skills/example-skill
Files Scanned: 3
Security Score: 85/100
Risk Level: LOW

Issues Found:
------------------------------------------------------------

1. [MEDIUM] External API calls detected
   Category: external_api
   File: SKILL.md
   Line: 15
   Recommendation: Review external API endpoints

============================================================
```

## Detection Categories

| Category | Severity | Description |
|----------|----------|-------------|
| `eval_exec` | CRITICAL | Dynamic code execution (eval, exec) |
| `external_api` | HIGH | External API calls |
| `file_access` | MEDIUM | File system access |
| `network` | HIGH | Network/subprocess access |
| `crypto_keys` | CRITICAL | API keys or secrets |

## GitHub Actions Integration

Add to your `.github/workflows/security.yml`:

```yaml
name: OpenClaw Skill Security Scan

on:
  push:
    paths:
      - 'skills/**'
      - 'SKILL.md'

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install OpenClaw Verifier
        run: pip install openclaw-verifier
      - name: Scan Skills
        run: openclaw-verifier batch ./skills
```

## API Usage

```python
from verify_skill import SkillVerifier

verifier = SkillVerifier("/path/to/skill")
results = verifier.scan()

print(f"Score: {results['score']}")
print(f"Risk Level: {verifier.get_risk_level()}")
```

## Roadmap

- [ ] More detection rules
- [ ] Real-time monitoring
- [ ] VS Code extension
- [ ] Enterprise features

## Contributing

Contributions welcome! Please read our contributing guidelines.

## License

MIT License - see [LICENSE](LICENSE)

## Security

If you discover a security vulnerability, please email security@example.com

---

**Protect your OpenClaw installation. Scan before you install.**
