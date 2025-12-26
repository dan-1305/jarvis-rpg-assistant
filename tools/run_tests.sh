#!/bin/bash

# Change to project root directory (parent of tools/)
cd "$(dirname "$0")/.."

echo "Running tests with coverage..."

# Install test dependencies
pip install pytest pytest-cov pytest-asyncio -q

# Run tests with coverage
pytest tests/ -v --cov=jarvis_core --cov-report=html --cov-report=term-missing

# Open coverage report (optional)
# python -m webbrowser htmlcov/index.html

echo "Tests completed! Check htmlcov/index.html for detailed coverage report."
