# Contributing to OpenClaw Verifier

Thanks for your interest in contributing!

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 🔍 Add detection rules
- 📝 Improve documentation
- 🌍 Translations

## Development Setup

\\\ash
git clone https://github.com/your-username/openclaw-verifier.git
cd openclaw-verifier
pip install -e .
\\\

## Running Tests

\\\ash
pytest test_verifier.py -v
\\\

## Adding Detection Rules

Edit \erify_skill.py\ and add to \MALICIOUS_PATTERNS\:

\\\python
\"new_category\": {
    \"patterns\": [
        r\"your_regex_pattern\",
    ],
    \"severity\": \"high\",
    \"description\": \"What this detects\"
}
\\\

## Pull Request Process

1. Fork the repo
2. Create a branch
3. Make changes
4. Add tests
5. Submit PR

## Code Style

- Follow PEP 8
- Add docstrings
- Keep functions small

## License

By contributing, you agree your code will be MIT licensed.
