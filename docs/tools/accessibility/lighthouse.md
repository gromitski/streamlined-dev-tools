# Lighthouse Accessibility Audit Tool

## Overview
A Stream Deck-optimized tool that runs Lighthouse audits on web pages using the official Lighthouse CLI. It can take a URL from the active browser window, clipboard, or command line, making it perfect for quick accessibility checks while browsing. The tool provides visual feedback through modal dialogs and maintains detailed logs for troubleshooting.

## Requirements
- Python 3.7 or higher
- Node.js and npm
- Chrome/Chromium browser
- Stream Deck software
- Platform-specific requirements:
  - macOS: No additional requirements
  - Linux: xclip for clipboard support (`sudo apt-get install xclip` on Ubuntu/Debian)
  - Windows: No additional requirements

## Installation
1. Clone this repository
2. Install Node.js and npm from [nodejs.org](https://nodejs.org)
3. Install Lighthouse CLI globally:
   ```bash
   npm install -g lighthouse
   ```
4. (Linux only) Install xclip:
   ```bash
   sudo apt-get install xclip  # Ubuntu/Debian
   sudo dnf install xclip      # Fedora
   ```

## Stream Deck Setup

1. Create a new button in Stream Deck
2. Choose "System: Open" action
3. Set the path to: `/path/to/repo/src/tools/accessibility/lighthouse/run_lighthouse.sh`

That's it! The script handles everything else automatically, including:
- Setting up the Python environment
- Installing required dependencies
- Running the audit
- Opening the report

## Usage

The button will:
1. Look for a URL in this order:
   - Active browser window
   - Clipboard (if no browser window found)
   - Command line argument (if provided)
2. Run a Lighthouse audit
3. Generate an HTML report in `~/lighthouse_reports/`
4. Open the report in your default browser

If there's an error (no URL found, Lighthouse not installed, etc.), a dialog will appear with instructions.

### Command Line Usage
```bash
/path/to/repo/src/tools/accessibility/lighthouse/run_lighthouse.sh [URL]
```

### Configuration
The tool can be configured through environment variables:

```bash
# Optional: Custom directory for storing reports
# Default: ~/lighthouse_reports
LIGHTHOUSE_REPORTS_DIR=/path/to/custom/directory
```

### Output
- Reports are saved in `~/lighthouse_reports/` by default
- Logs are saved in `~/lighthouse_reports/logs/`
- Filename formats:
  - Reports: `lighthouse_domain_YYYYMMDD_HHMMSS.html`
  - Logs: `lighthouse_audit_YYYYMMDD_HHMMSS.log`
- Reports include scores for:
  - Accessibility
  - Best Practices
  - Performance
  - PWA
  - SEO

## Features
- URL detection from:
  1. Active browser window
  2. Clipboard content
  3. Command line arguments
- Cross-platform support (macOS, Windows, Linux)
- User-friendly error dialogs
- Detailed logging system
- Headless Chrome operation
- Comprehensive HTML reports
- Local report storage
- Progress indication
- Automatic dependency management

## Troubleshooting

### No URL Found
- Make sure you have an active browser window with a URL
- Or copy a URL to your clipboard before pressing the button

### Lighthouse Not Found
If you see "Lighthouse not found":
1. Open Terminal
2. Run: `npm install -g lighthouse`
3. Try the button again

### Other Issues
- Check the logs in `~/lighthouse_reports/logs/`
- Make sure Node.js and npm are installed
- Ensure Chrome/Chromium is installed

## Notes
- The script creates and manages its own Python virtual environment
- All dependencies are installed automatically
- Reports and logs are stored locally for future reference
- The tool uses the official Lighthouse CLI
- Chrome runs in headless mode during audits
- Error messages appear in modal dialogs for better visibility 