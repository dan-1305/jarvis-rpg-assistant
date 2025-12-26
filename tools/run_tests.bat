@echo off
REM Change to project root directory (parent of tools/)
cd /d "%~dp0.."

echo Running tests with coverage...

REM Install test dependencies
pip install pytest pytest-cov pytest-asyncio -q

REM Run tests with coverage
pytest tests/ -v --cov=jarvis_core --cov-report=html --cov-report=term-missing

echo.
echo Tests completed! Check htmlcov/index.html for detailed coverage report.
pause
