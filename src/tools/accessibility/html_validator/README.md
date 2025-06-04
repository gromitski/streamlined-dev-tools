# HTML Validator Tool

A streamlined HTML validation tool that checks web pages for HTML compliance and best practices. The tool can grab URLs from your active Chrome window, clipboard, or command line arguments.

## Features

- Automatic URL collection from multiple sources:
  - Command line arguments (highest priority)
  - Active Chrome window (macOS only)
  - Clipboard (URLs only)
- Clean, focused validation reports
- Automatic virtual environment management
- Minimal dependencies
- Cross-platform compatibility (URL collection optimized for macOS)

## Requirements

- Python 3.7 or higher
- Google Chrome (for active window URL collection on macOS)
- Internet connection (for validation)

## Installation

The tool comes with an automatic setup script that handles all dependencies. No manual installation is required.

## Usage

1. Run the validator:
   ```bash
   ./run_validator.sh
   ```

2. The tool will attempt to get a URL in this order:
   - Command line argument if provided
   - Active Chrome window URL (macOS only)
   - URL from clipboard

3. To validate a specific URL:
   ```bash
   ./run_validator.sh "https://example.com"
   ```

## Stream Deck Integration

1. Create a new button in Stream Deck
2. Choose "System: Open" action
3. Set the path to: `path/to/repo/src/tools/accessibility/html_validator/run_validator.sh`
4. Optional: Add an icon and title for the button

Now you can validate any webpage with a single button press!

## Error Messages

- "No URL found!": The tool couldn't find a URL from any source
- "Virtual environment is broken or missing packages": The virtual environment needs to be rebuilt (happens automatically)

## Development

The tool follows the URL collection pattern documented in `methodologies/url_collection_pattern.txt`. Key files:

- `validate.py`: Main validation script
- `run_validator.sh`: Environment setup and launcher script

## Contributing

1. Follow the URL collection pattern for any URL-related changes
2. Maintain the existing error handling patterns
3. Keep dependencies minimal
4. Test all URL collection methods before submitting changes

## License

This tool is part of the Streamlined Dev Tools collection and is licensed under the MIT License.
