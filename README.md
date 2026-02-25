# OpenClaw Verifier

OpenClaw Skill 安全验证工具

## 安装

```bash
pip install openclaw-verifier
```

## 使用

### 扫描单个 Skill

```bash
openclaw-verifier scan /path/to/skill
```

### 批量扫描

```bash
openclaw-verifier batch /path/to/skills/directory
```

### 生成报告

```bash
# JSON 格式
openclaw-verifier scan /path/to/skill --json

# HTML 格式
openclaw-verifier report /path/to/skill --format html
```

## API 使用

```python
from verify_skill import SkillVerifier

verifier = SkillVerifier("/path/to/skill")
results = verifier.scan()

print(f"Score: {results['score']}")
print(f"Risk Level: {verifier.get_risk_level()}")
```

## 检测的恶意模式

| 类别 | 严重程度 | 说明 |
|------|---------|------|
| external_api | 高 | 外部 API 调用 |
| eval_exec | 严重 | 动态代码执行 |
| file_access | 中 | 文件系统访问 |
| network | 高 | 网络/子进程访问 |
| crypto_keys | 严重 | API 密钥或机密 |

## 输出示例

```
============================================================
OpenClaw Skill Security Report
============================================================

Skill: ./skills/malicious-skill
Files Scanned: 3
Security Score: 25/100
Risk Level: CRITICAL

Issues Found:
------------------------------------------------------------

1. [CRITICAL] Dynamic code execution
   Category: eval_exec
   File: script.py
   Line: 42
   Match: eval(user_input)

2. [HIGH] External API calls detected
   Category: external_api
   File: SKILL.md
   Line: 15
   Match: https://malicious-server.com/api

============================================================
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
