# Streamlined Dev Tools

A collection of development-related tools designed for use with Stream Decks and other productivity tools.

## Overview

This repository contains various utility scripts and tools to enhance developer productivity, particularly focused on integration with Stream Deck devices. Each tool is designed to be modular and can be used independently or as part of a larger workflow.

## Project Structure

```
streamlined-dev-tools/
├── src/
│   └── tools/         # Individual tool implementations
│       └── accessibility/
│           ├── axe/   # Axe Core accessibility audit tool
│           ├── html_validator/ # HTML validation tool
│           └── lighthouse/ # Lighthouse audit tool
└── README.md         # This file
```

## Features

The package includes tools for:

### Accessibility Testing
- **Axe Core Audit**: Focused accessibility testing with axe-core
  - Gets URLs from active browser windows or clipboard
  - Generates beautiful HTML reports
  - Shows results through terminal and browser
  - Focuses specifically on accessibility issues
  - Supports macOS, Windows, and Linux

- **HTML Validator**: Standards-compliant HTML validation
  - Validates web pages against HTML standards
  - Automatically grabs URLs from Chrome or clipboard
  - Simple, focused validation reports
  - Perfect for quick HTML compliance checks
  - Optimized for macOS, with cross-platform support

- **Lighthouse Audit**: Comprehensive web page auditing
  - Analyzes accessibility, performance, SEO, and best practices
  - Generates detailed HTML reports
  - Shows results in Chrome
  - Includes Progressive Web App (PWA) metrics
  - Perfect for general website health checks

## Requirements

- Python 3.7 or higher
- Node.js and npm (for axe-core CLI and Lighthouse)
- Additional requirements are listed in each tool's documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/streamlined-dev-tools.git
cd streamlined-dev-tools
```

2. Follow the setup instructions in each tool's README file for specific requirements and configuration.

## Stream Deck Setup

Each tool comes with its own launcher script that handles all dependencies and environment setup. To use a tool:

1. Create a new button in Stream Deck
2. Choose "System: Open" action
3. Set the path to the tool's launcher script:
   - For Axe: `path/to/repo/src/tools/accessibility/axe/run_axe.sh`
   - For Lighthouse: `path/to/repo/src/tools/accessibility/lighthouse/run_lighthouse.sh`

That's it! The launcher scripts handle everything else automatically.

## Usage

### Quick Start - Axe Core
1. Install Node.js and npm from [nodejs.org](https://nodejs.org)
2. Install axe-core CLI: `npm install -g @axe-core/cli`
3. Set up the Stream Deck button as described above
4. Press the button while viewing any webpage to run an accessibility audit

### Quick Start - Lighthouse
1. Install Node.js and npm from [nodejs.org](https://nodejs.org)
2. Install Lighthouse: `npm install -g lighthouse`
3. Set up the Stream Deck button as described above
4. Press the button while viewing any webpage to run a comprehensive audit

### Quick Start - HTML Validator
1. Navigate to the validator directory
2. Run the validator script: `./run_validator.sh`
3. The tool will automatically grab the URL from your active Chrome window or clipboard
4. View the validation results

## Tool Selection Guide

- Use **Axe Core** when you need:
  - Focused accessibility testing
  - Detailed WCAG compliance checks
  - Quick accessibility issue identification
  - Cross-browser compatibility

- Use **HTML Validator** when you need:
  - Quick HTML standards compliance checks
  - Simple, focused validation reports
  - Automatic URL collection from browser/clipboard
  - Minimal setup and dependencies

- Use **Lighthouse** when you need:
  - Comprehensive website audits
  - Performance metrics
  - SEO analysis
  - Progressive Web App validation
  - Best practices review

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
