# 🤝 CONTRIBUTING TO JARVIS RPG ASSISTANT

Thank you for your interest in contributing! This document provides guidelines for contributing to the Jarvis RPG Assistant project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment. Be kind, constructive, and professional in all interactions.

---

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of [github.com/dan-1305/jarvis-rpg-assistant](https://github.com/dan-1305/jarvis-rpg-assistant).

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-rpg-assistant.git
cd jarvis-rpg-assistant
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### 4. Add Upstream Remote

```bash
git remote add upstream https://github.com/dan-1305/jarvis-rpg-assistant.git
```

---

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
# Sync with upstream
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run test suite
python -m pytest tests/ --cov=jarvis_core --cov=src -v

# Run readiness check
python tools/public_readiness_check.py

# Test manually
python main.py [command]
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: Add your feature description"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request from your fork to the main repository.

---

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Maximum line length: 120 characters
- Use descriptive variable and function names

### Project Structure

```
jarvis_core/     # Core library modules (reusable logic)
src/             # Entry point scripts (CLI commands)
tests/           # Unit and integration tests
tools/           # Development utilities and scripts
docs/            # Documentation files
```

### Import Order

```python
# Standard library
import os
import sys

# Third-party
from telegram import Update
import google.generativeai as genai

# Local
from jarvis_core.config import Config
from jarvis_core.database import Database
```

### Documentation

- Add docstrings to all public functions and classes
- Use clear, concise comments for complex logic
- Update README.md for user-facing changes
- Update docs/ for architecture changes

---

## 🧪 Testing Guidelines

### Test Coverage Requirements

- **Core modules:** 70-80% coverage target
- **Entry points:** Basic functionality coverage
- **Utilities:** 50%+ coverage

### Writing Tests

```python
import pytest
from jarvis_core.config import Config

def test_config_loads_env():
    config = Config()
    assert config.TELEGRAM_BOT_TOKEN is not None
    assert config.CHAT_ID is not None

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=jarvis_core --cov=src

# Run specific test file
python -m pytest tests/test_core.py -v

# View HTML coverage report
# Open htmlcov/index.html in browser
```

---

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Build process or auxiliary tool changes

### Examples

```bash
feat(database): Add transaction lock mechanism

Implement 30s timeout with automatic rollback to prevent
concurrent write conflicts.

Closes #42

---

fix(ai_agent): Handle quota exceeded error

Add automatic key rotation when hitting quota limits.

---

docs(readme): Update installation instructions

Add Docker deployment section and troubleshooting guide.

---

test(core): Increase coverage for key_manager

Add tests for cooldown mechanism and key rotation.
```

---

## 🔀 Pull Request Process

### Before Submitting

1. ✅ Run tests: `python -m pytest tests/ -v`
2. ✅ Check readiness: `python tools/public_readiness_check.py`
3. ✅ Update documentation if needed
4. ✅ Ensure no `.env` or credentials committed
5. ✅ Rebase on latest `main` branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No security issues introduced
```

### Review Process

1. Maintainer will review within 48 hours
2. Address review comments
3. Once approved, maintainer will merge
4. Your contribution will be in the next release! 🎉

---

## 🐛 Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and stack traces

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Possible implementation approach

---

## 🎯 Good First Issues

Looking to contribute but not sure where to start? Look for issues labeled:

- `good first issue` - Perfect for newcomers
- `help wanted` - Community contributions welcome
- `documentation` - Improve docs and examples

### Current Good First Issues

- **Improve test coverage for utilities:**
  - `jarvis_core/db_sync.py`
  - `jarvis_core/error_notifier.py`
  - Target: 70%+ coverage

- **Add integration tests:**
  - Test end-to-end workflow
  - Test Docker deployment

---

## 📞 Getting Help

- **Questions:** Open a [GitHub Discussion](https://github.com/dan-1305/jarvis-rpg-assistant/discussions)
- **Bugs:** Open a [GitHub Issue](https://github.com/dan-1305/jarvis-rpg-assistant/issues)
- **Chat:** Join our community (link coming soon)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Jarvis RPG Assistant! 🚀**
