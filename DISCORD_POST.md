# Discord 发布内容

## 频道: #showcase 或 #tools

---

🔒 **OpenClaw Verifier - Security Scanner for OpenClaw Skills**

Hey OpenClaw community! 👋

I built a security scanner after seeing the ClawHavoc attack (341 malicious skills, 32.6% CRITICAL rate on ClawHub).

**What it does:**
- Scans skills before installation
- Detects malicious code patterns
- Provides security score (0-100)
- CLI + Web UI

**Detection categories:**
- eval/exec (CRITICAL)
- External API calls (HIGH)
- File access (MEDIUM)
- Network access (HIGH)
- Crypto keys/secrets (CRITICAL)

**Installation:**
```bash
pip install openclaw-verifier
openclaw-verifier scan /path/to/skill
```

**GitHub:** (link after upload)
**PyPI:** (link after upload)

Open source, MIT license. Feedback welcome! 🦞

---

## 附加信息（如果有人问）

**Q: Why build this?**
A: After ClawHavoc, I realized we need a tool to verify skills before installing. OpenClaw is amazing, but the skill ecosystem has security issues.

**Q: How does it work?**
A: Static analysis + pattern matching. It scans SKILL.md and any Python/shell scripts for malicious patterns.

**Q: Is it free?**
A: Yes! Open source, MIT license. Free forever for the core scanner.

**Q: Enterprise version?**
A: Planning to add: API access, CI/CD integration, custom rules, team management.

**Q: How can I help?**
A: Star on GitHub, report bugs, suggest detection rules, spread the word!
