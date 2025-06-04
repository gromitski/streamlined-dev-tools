# Development Guide

This guide explains how to set up your development environment and contribute to the project.

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlined-dev-tools.git
   cd streamlined-dev-tools
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following our coding standards:
   - Use type hints
   - Follow PEP 8 style guide
   - Add docstrings to functions and classes
   - Keep functions focused and small
   - Write tests for new functionality

3. Run the linting and test suite:
   ```bash
   ./scripts/lint_and_test.sh
   ```
   This will run:
   - Black (code formatting)
   - isort (import sorting)
   - Flake8 (style guide enforcement)
   - MyPy (type checking)
   - pytest (unit tests with coverage)

4. Commit your changes following our [commit convention](COMMIT_CONVENTION.md):
   ```bash
   git add .
   git commit -m "feat(component): add new feature"
   ```

5. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub following our [pull request template](../.github/pull_request_template.md).

## Code Quality Tools

### Black
- Formats Python code
- Configuration in `pyproject.toml`
- Run manually: `black .`

### isort
- Sorts imports
- Configuration in `setup.cfg`
- Run manually: `isort .`

### Flake8
- Lints Python code
- Configuration in `setup.cfg`
- Run manually: `flake8 .`

### MyPy
- Type checks Python code
- Configuration in `setup.cfg`
- Run manually: `mypy src/`

### pytest
- Runs unit tests
- Run manually: `pytest`
- With coverage: `pytest --cov=src/ tests/`

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality. They include:
- Trailing whitespace removal
- File ending fixes
- YAML/JSON validation
- Python syntax checking
- Code formatting (Black)
- Import sorting (isort)
- Linting (Flake8)
- Type checking (MyPy)

To run hooks manually on all files:
```bash
pre-commit run --all-files
```

## Branch Strategy

- `main`: Protected branch, only updated through PRs
- `dev`: Development branch, feature branches are created from here
- Feature branches: `feature/feature-name`
- Bugfix branches: `fix/bug-description`
- Release branches: `release/v1.x.x`

## Release Process

1. Create a release branch:
   ```bash
   git checkout -b release/v1.x.x dev
   ```

2. Update version numbers and changelogs

3. Run full test suite:
   ```bash
   ./scripts/lint_and_test.sh
   ```

4. Create a PR to `main`

5. After merge, tag the release:
   ```bash
   git tag -a v1.x.x -m "Version 1.x.x"
   git push origin v1.x.x
   ```

## Getting Help

- Check existing issues and pull requests
- Review the documentation
- Ask questions in pull requests or issues
