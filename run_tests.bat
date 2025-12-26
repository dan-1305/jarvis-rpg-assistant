@echo off
echo Running tests with coverage...

REM Install test dependencies
pip install pytest pytest-cov pytest-asyncio

REM Run tests with coverage
pytest tests/ -v --cov=jarvis_core --cov-report=html --cov-report=term-missing --cov-fail-under=80

echo.
echo Tests completed! Check htmlcov/index.html for detailed coverage report.
pause
