# Contributing to Threat Intelligence Platform

Thank you for your interest in contributing! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/threat-intel-platform.git`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run tests: `python run_tests.py`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

```bash
# Run setup script
python setup.py

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Start development server
python -m api.main
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting: `black .`
- Lint with flake8: `flake8 .`
- Add type hints where possible

## Testing

- Write tests for new features
- Maintain 80%+ code coverage
- Run full test suite before submitting PR

```bash
pytest tests/ -v --cov=.
```

## Pull Request Process

1. Update README.md if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Bug Reports

Use GitHub Issues with the bug template. Include:
- Python version
- OS version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Feature Requests

Use GitHub Issues with the feature template. Include:
- Use case description
- Proposed solution
- Alternative approaches considered

## Questions?

Open a discussion on GitHub or reach out to maintainers.

Happy contributing! 🚀
