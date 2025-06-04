# Lighthouse Accessibility Audit Tool

A Stream Deck button that runs Lighthouse accessibility audits on URLs. It can get the URL from:
1. Active browser window
2. Clipboard
3. Command line argument

## Quick Start for Stream Deck

1. Clone this repository
2. Install Node.js and npm from [nodejs.org](https://nodejs.org)
3. Open Terminal and run:
   ```bash
   npm install -g lighthouse
   ```
4. In Stream Deck:
   - Create a new button
   - Choose "System: Open" action
   - Set the path to: `/path/to/repo/src/tools/accessibility/lighthouse/run_lighthouse.sh`
   - That's it! The script handles everything else automatically

The script will automatically:
- Set up its Python environment
- Install required dependencies
- Run the audit
- Open the report in your browser

## Usage

The button will:
1. Look for a URL in this order:
   - Active browser window
   - Clipboard (if no browser window found)
   - Command line argument (if provided)
2. Run a Lighthouse audit
3. Generate an HTML report in `~/lighthouse_reports/`
4. Open the report in your default browser

If no URL is found or there's an error, a dialog will appear with instructions.

## Requirements

- Node.js and npm
- Python 3.7 or higher
- Chrome/Chromium browser
- Stream Deck software

### System-Specific Requirements

- **macOS**: No additional requirements
- **Linux**: Install `xclip` for clipboard support:
  ```bash
  # Ubuntu/Debian:
  sudo apt-get install xclip
  # Fedora:
  sudo dnf install xclip
  ```
- **Windows**: No additional requirements

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

## Configuration

### Custom Reports Directory
Set the environment variable:
```bash
LIGHTHOUSE_REPORTS_DIR=/path/to/custom/directory
```

## Report Location

Reports are saved in:
- Default: `~/lighthouse_reports/`
- Logs: `~/lighthouse_reports/logs/` 