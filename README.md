# Streamlined Dev Tools

A collection of development-related Python scripts designed for use with Stream Decks and other productivity tools.

## Overview

This repository contains various utility scripts and tools to enhance developer productivity, particularly focused on integration with Stream Deck devices. Each tool is designed to be modular and can be used independently or as part of a larger workflow.

## Project Structure

```
streamlined-dev-tools/
├── src/
│   ├── tools/         # Individual tool implementations
│   └── __init__.py    # Package initialization
├── docs/
│   ├── tools/         # Individual tool documentation
│   └── README.md      # Documentation guidelines
├── tests/
│   └── tools/         # Tool-specific tests
├── examples/          # Example scripts and configurations
├── scripts/          # Setup and utility scripts
├── pyproject.toml     # Project configuration
└── README.md         # This file
```

## Features

The package includes (or will include) various tools for:

- Stream Deck Integration
- Development Workflow Automation
- Project Management
- System Monitoring
- Custom Utility Scripts

### Available Tools

#### Accessibility
- **Lighthouse Audit**: Run accessibility audits on web pages directly from your Stream Deck

(More tools will be listed here as they are developed)

## Requirements

- Python 3.8 or higher
- Additional requirements will be listed in requirements.txt

## Installation

### For Development

1. Clone the repository:
```bash
git clone https://github.com/gromitski/streamlined-dev-tools.git
cd streamlined-dev-tools
```

2. Install dependencies in a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### For Stream Deck Usage

To use the tools directly with Stream Deck buttons (recommended):

1. Clone the repository:
```bash
git clone https://github.com/gromitski/streamlined-dev-tools.git
cd streamlined-dev-tools
```

2. Run the global setup script:
```bash
./scripts/setup_global.sh
```

This will install all necessary dependencies globally, making the tools ready to use with Stream Deck buttons.

## Stream Deck Setup

1. Create a new button in Stream Deck
2. Choose 'System: Open' action
3. Set the path to the script you want to run (e.g., `path/to/streamlined-dev-tools/src/tools/accessibility/lighthouse/lighthouse_audit.py`)
4. Set 'Open with' to: python3

Each tool's documentation includes specific Stream Deck setup instructions.

## Usage

Each tool in the package is documented separately. See the `docs/tools/` directory for detailed documentation on individual tools.

### Quick Start

See individual tool documentation in `docs/tools/` for quick start guides.

## Documentation

- Tool-specific documentation can be found in the `docs/tools/` directory
- Example usage can be found in the `examples/` directory
- For contribution guidelines, see `docs/README.md`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

When contributing:
1. Create a new branch for your feature
2. Follow the existing code style
3. Add tests for any new functionality
4. Update documentation following the templates in `docs/README.md`
5. Submit a pull request with a clear description of your changes 