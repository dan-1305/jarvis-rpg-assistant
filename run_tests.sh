#!/bin/bash

echo "Running tests with coverage..."

# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run tests with coverage
pytest tests/ -v --cov=jarvis_core --cov-report=html --cov-report=term-missing --cov-fail-under=80

# Open coverage report (optional)
# python -m webbrowser htmlcov/index.html

echo "Tests completed! Check htmlcov/index.html for detailed coverage report."
