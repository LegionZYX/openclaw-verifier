# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-26

### Added
- **Multi-model AI support** - Support for multiple AI providers
  - Qwen (千问) - Alibaba's Qwen model
  - Qwen Coding (千问编程) - Specialized for code analysis
  - GPT-4 / GPT-4o - OpenAI models
  - Claude - Anthropic models
  - DeepSeek - DeepSeek models
- **Model Manager CLI** - Easy model switching
  - `python model_manager.py list` - List available models
  - `python model_manager.py use <model>` - Switch model
  - `python model_manager.py set-key <env> <key>` - Set API key
- **Configuration file support** - `config.yaml.example`
- **Chinese documentation** - Full Chinese README
- **AI-enhanced analysis** - Optional deep analysis using AI models

### Changed
- Refactored `verify_skill.py` with modular AI client
- Improved error handling for API calls
- Better model availability detection

### Fixed
- Git push authentication issues
- Branch synchronization (master/main)

## [0.1.0] - 2026-02-25

### Added
- Initial release
- Core security scanner (`verify_skill.py`)
- CLI tool (`cli.py`)
- Web UI (`web/index.html`)
- GitHub Actions integration
- 5 detection categories:
  - `eval_exec` (CRITICAL) - Dynamic code execution
  - `external_api` (HIGH) - External API calls
  - `file_access` (MEDIUM) - File system access
  - `network` (HIGH) - Network/subprocess access
  - `crypto_keys` (CRITICAL) - API keys or secrets
- Security score (0-100)
- Risk level assessment
- JSON and HTML report generation
- MIT License

### Security
- Initial pattern database based on ClawHavoc analysis
- Detection of 341 known malicious patterns

---

## Roadmap

### [0.3.0] - Planned
- VS Code extension
- Real-time file monitoring
- Auto-scan on skill installation

### [0.4.0] - Planned
- Web dashboard
- Team collaboration
- Custom rule editor

### [1.0.0] - Planned
- Enterprise features
- SSO integration
- Audit logs
- Priority support
