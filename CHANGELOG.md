# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-25

### Added
- Initial release
- Core security scanner (verify_skill.py)
- CLI tool (cli.py)
- Web UI (web/index.html)
- GitHub Actions integration
- 5 detection categories:
  - eval_exec (CRITICAL)
  - external_api (HIGH)
  - file_access (MEDIUM)
  - network (HIGH)
  - crypto_keys (CRITICAL)
- Security score (0-100)
- Risk level assessment
- JSON and HTML report generation

### Security
- Initial pattern database based on ClawHavoc analysis
