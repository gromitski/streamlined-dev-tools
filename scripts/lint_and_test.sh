#!/bin/bash

# Exit on any error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Running code quality checks..."

# Format with Black
echo -e "\n${GREEN}Running Black formatter...${NC}"
black .

# Sort imports
echo -e "\n${GREEN}Sorting imports with isort...${NC}"
isort .

# Run Flake8
echo -e "\n${GREEN}Running Flake8 linter...${NC}"
flake8 .

# Run MyPy
echo -e "\n${GREEN}Running MyPy type checker...${NC}"
mypy src/

# Run tests with coverage
echo -e "\n${GREEN}Running tests with coverage...${NC}"
pytest --cov=src/ tests/ --cov-report=term-missing

echo -e "\n${GREEN}All checks completed successfully!${NC}"
