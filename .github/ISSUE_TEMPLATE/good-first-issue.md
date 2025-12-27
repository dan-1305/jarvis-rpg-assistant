---
name: Good First Issue
about: Perfect issue for newcomers to the project
title: '[GOOD FIRST ISSUE] '
labels: 'good first issue, help wanted'
assignees: ''
---

## 🎯 Good First Issue: Improve Test Coverage for Utility Modules

**Difficulty:** Easy  
**Time Estimate:** 2-4 hours  
**Skills Required:** Python, pytest  

### 📋 Description

We need to improve test coverage for utility modules in `jarvis_core/`. This is a great first issue for newcomers to get familiar with the codebase!

### 🎯 Goal

Increase test coverage for the following modules to **70%+**:

- [ ] `jarvis_core/db_sync.py` (current: ~40%)
- [ ] `jarvis_core/error_notifier.py` (current: ~30%)

### 📝 Tasks

1. **Review existing tests** in `tests/test_core.py` and `tests/test_new_features.py`
2. **Write new test cases** for uncovered functions:
   - `db_sync.py`: Test git sync operations, commit message generation, error handling
   - `error_notifier.py`: Test error formatting, Telegram sending, admin user filtering
3. **Run tests locally** to ensure they pass
4. **Update coverage report** and verify improvement

### 🛠️ Getting Started

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/jarvis-rpg-assistant.git
cd jarvis-rpg-assistant

# 2. Set up development environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Run existing tests to understand structure
python -m pytest tests/ -v

# 4. Check current coverage
python -m pytest tests/ --cov=jarvis_core --cov=src --cov-report=html
# Open htmlcov/index.html to see uncovered lines

# 5. Write new tests in tests/test_new_features.py or create new test file

# 6. Verify your tests pass
python -m pytest tests/ -v
```

### ✅ Example Test Structure

```python
# tests/test_db_sync.py (new file)
import pytest
from unittest.mock import Mock, patch
from jarvis_core.db_sync import sync_database, generate_commit_message

def test_generate_commit_message():
    """Test commit message generation"""
    message = generate_commit_message("test_table", "INSERT")
    assert "test_table" in message
    assert "INSERT" in message

@patch('subprocess.run')
def test_sync_database_success(mock_run):
    """Test successful database sync"""
    mock_run.return_value = Mock(returncode=0)
    result = sync_database()
    assert result == True
    mock_run.assert_called()

@patch('subprocess.run')
def test_sync_database_failure(mock_run):
    """Test database sync failure handling"""
    mock_run.side_effect = Exception("Git error")
    result = sync_database()
    assert result == False
```

### 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Project contribution guidelines
- Existing tests in `tests/` directory for reference

### 💡 Tips

- Read the module code first to understand what it does
- Look at existing tests for similar modules as examples
- Use `unittest.mock` to mock external dependencies (git commands, Telegram API)
- Test both success and failure scenarios
- Add docstrings to your test functions

### ✅ Definition of Done

- [ ] New tests written for target modules
- [ ] All tests pass: `python -m pytest tests/ -v`
- [ ] Coverage increased to 70%+: `python -m pytest tests/ --cov=jarvis_core`
- [ ] Code follows project style guidelines
- [ ] Pull request created with clear description

### 🆘 Need Help?

- Comment on this issue if you have questions
- Check [CONTRIBUTING.md](../../CONTRIBUTING.md) for development workflow
- Review existing tests in `tests/` directory for examples

### 🎉 Your First Contribution!

Thank you for considering contributing to Jarvis RPG Assistant! This issue is specifically designed for newcomers. Don't hesitate to ask questions - we're here to help! 🚀
