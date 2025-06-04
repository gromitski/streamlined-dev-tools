# Streamlined Dev Tools

A collection of development-related tools designed for use with Stream Decks and other productivity tools.

## Overview

This repository contains various utility scripts and tools to enhance developer productivity, particularly focused on integration with Stream Deck devices. Each tool is designed to be modular and can be used independently or as part of a larger workflow.

## Project Structure

```
streamlined-dev-tools/
├── src/
│   └── tools/         # Individual tool implementations
├── docs/
│   └── tools/         # Individual tool documentation
├── tests/             # Tool-specific tests
└── README.md         # This file
```

## Features

The package includes tools for:

### Accessibility
- **Lighthouse Audit**: Run accessibility audits on web pages directly from your Stream Deck
  - Gets URLs from active browser windows or clipboard
  - Generates comprehensive HTML reports
  - Shows results through modal dialogs
  - Handles all dependencies automatically

## Requirements

- Python 3.7 or higher
- Additional requirements are listed in each tool's documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gromitski/streamlined-dev-tools.git
cd streamlined-dev-tools
```

2. Follow the setup instructions in each tool's README file for specific requirements and configuration.

## Stream Deck Setup

Each tool comes with its own launcher script that handles all dependencies and environment setup. To use a tool:

1. Create a new button in Stream Deck
2. Choose "System: Open" action
3. Set the path to the tool's launcher script (e.g., `path/to/repo/src/tools/accessibility/lighthouse/run_lighthouse.sh`)

That's it! The launcher scripts handle everything else automatically.

## Usage

Each tool in the package is documented separately. See the `docs/tools/` directory for detailed documentation on individual tools.

### Quick Start

See individual tool documentation in `docs/tools/` for quick start guides.

## Documentation

- Tool-specific documentation can be found in the `docs/tools/` directory
- Each tool includes its own README with setup and usage instructions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

When contributing:
1. Create a new branch for your feature
2. Follow the existing code style
3. Add tests for any new functionality
4. Update documentation as needed
5. Submit a pull request with a clear description of your changes 