# OpenClaw Verifier

[![PyPI version](https://badge.fury.io/py/openclaw-verifier.svg)](https://badge.fury.io/py/openclaw-verifier)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-LegionZYX%2Fopenclaw--verifier-blue)](https://github.com/LegionZYX/openclaw-verifier)

🔒 **OpenClaw Skills 安全验证工具** | **Security verification tool for OpenClaw Skills**

[English](#english) | [中文](#中文)

---

## 中文

### 为什么需要 OpenClaw Verifier？

- **32.6% 的 ClawHub skills 是高危** - 不要盲目安装
- **341 个恶意 skills 被发现**（2026 年 ClawHavoc 攻击）
- **5.2% 存在恶意意图** - 保护你的 API 密钥和数据

### 功能特性

- 🔍 **静态代码分析** - 检测恶意模式
- 🎯 **5 大检测类别** - eval/exec、外部 API、文件访问、网络、密钥
- 📊 **安全评分** - 0-100 分 + 风险等级
- 🖥️ **CLI + Web UI** - 命令行和网页界面
- 🔄 **CI/CD 集成** - GitHub Actions 支持
- 🤖 **多模型支持** - 支持 GPT、Claude、千问等多种 AI 模型

### 安装

```bash
pip install openclaw-verifier
```

### 快速开始

```bash
# 扫描单个 skill
openclaw-verifier scan /path/to/skill

# 批量扫描
openclaw-verifier batch /path/to/skills/directory

# JSON 输出
openclaw-verifier scan /path/to/skill --json
```

### 检测类别

| 类别 | 严重程度 | 说明 |
|------|---------|------|
| `eval_exec` | 严重 | 动态代码执行 (eval, exec) |
| `external_api` | 高 | 外部 API 调用 |
| `file_access` | 中 | 文件系统访问 |
| `network` | 高 | 网络/子进程访问 |
| `crypto_keys` | 严重 | API 密钥或机密 |

### 多模型支持

OpenClaw Verifier 支持多种 AI 模型进行深度分析：

#### 配置方式

```bash
# 设置环境变量
export OPENAI_API_KEY="your-openai-key"        # GPT-4
export ANTHROPIC_API_KEY="your-claude-key"     # Claude
export DASHSCOPE_API_KEY="your-dashscope-key"  # 千问
```

#### 支持的模型

| 模型 | 环境变量 | 说明 |
|------|---------|------|
| GPT-4/GPT-4o | `OPENAI_API_KEY` | OpenAI 模型 |
| Claude | `ANTHROPIC_API_KEY` | Anthropic 模型 |
| 千问 | `DASHSCOPE_API_KEY` | 阿里千问模型 |
| DeepSeek | `DEEPSEEK_API_KEY` | DeepSeek 模型 |
| 本地模型 | 无需 | QMD 本地向量搜索 |

#### 在代码中使用

```python
from verify_skill import SkillVerifier

# 使用默认模型
verifier = SkillVerifier("/path/to/skill")

# 指定模型
verifier = SkillVerifier("/path/to/skill", model="qwen")

# 使用千问 Coding Plan
verifier = SkillVerifier("/path/to/skill", model="qwen-coding")
```

### GitHub Actions 集成

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Verifier
        run: pip install openclaw-verifier
      - name: Scan
        run: openclaw-verifier batch ./skills
```

---

## English

### Why OpenClaw Verifier?

- **32.6% of ClawHub skills are CRITICAL** - Don't install blindly
- **341 malicious skills discovered** (2026 ClawHavoc attack)
- **5.2% show malicious intent** - Protect your API keys and data

### Features

- 🔍 **Static Code Analysis** - Detect malicious patterns
- 🎯 **5 Detection Categories** - eval/exec, external API, file access, network, crypto keys
- 📊 **Security Score** - 0-100 score with risk level
- 🖥️ **CLI + Web UI** - Use however you prefer
- 🔄 **CI/CD Integration** - GitHub Actions ready
- 🤖 **Multi-Model Support** - GPT, Claude, Qwen, and more

### Installation

```bash
pip install openclaw-verifier
```

### Quick Start

```bash
# Scan a single skill
openclaw-verifier scan /path/to/skill

# Batch scan
openclaw-verifier batch /path/to/skills/directory

# JSON output
openclaw-verifier scan /path/to/skill --json
```

### Detection Categories

| Category | Severity | Description |
|----------|----------|-------------|
| `eval_exec` | CRITICAL | Dynamic code execution (eval, exec) |
| `external_api` | HIGH | External API calls |
| `file_access` | MEDIUM | File system access |
| `network` | HIGH | Network/subprocess access |
| `crypto_keys` | CRITICAL | API keys or secrets |

### Multi-Model Support

Configure AI models for deep analysis:

```bash
# Set environment variables
export OPENAI_API_KEY="your-key"        # GPT-4
export ANTHROPIC_API_KEY="your-key"     # Claude
export DASHSCOPE_API_KEY="your-key"     # Qwen (千问)
```

| Model | Env Variable | Provider |
|-------|-------------|----------|
| GPT-4/GPT-4o | `OPENAI_API_KEY` | OpenAI |
| Claude | `ANTHROPIC_API_KEY` | Anthropic |
| Qwen (千问) | `DASHSCOPE_API_KEY` | Alibaba |
| DeepSeek | `DEEPSEEK_API_KEY` | DeepSeek |
| Local | None | QMD Vector Search |

---

## Roadmap

- [x] Core security scanner
- [x] CLI tool
- [x] Web UI
- [x] GitHub Actions integration
- [x] Multi-model support
- [ ] VS Code extension
- [ ] Real-time monitoring
- [ ] Enterprise features

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)

## Security

Report vulnerabilities to security@example.com

---

**保护你的 OpenClaw 安装。安装前先扫描。**

**Protect your OpenClaw installation. Scan before you install.**
