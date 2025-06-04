# Axe Core CLI Audit Tool

A Stream Deck button that runs axe-core CLI accessibility audits on URLs. It can get the URL from:
1. Active browser window (Chrome, Safari, or Firefox on macOS; Chrome on Windows/Linux)
2. Clipboard (if no browser window found)
3. Command line argument (if provided)

## Quick Start for Stream Deck

1. Clone this repository
2. Install Node.js and npm from [nodejs.org](https://nodejs.org)
3. Open Terminal and run:
   ```bash
   npm install -g @axe-core/cli
   ```
4. In Stream Deck:
   - Create a new button
   - Choose "System: Open" action
   - Set the path to: `/path/to/repo/src/tools/accessibility/axe/run_axe.sh`
   - That's it! The script handles everything else automatically

The script will automatically:
- Set up its Python environment
- Install required dependencies
- Run the audit
- Display results in terminal
- Open a beautiful HTML report in your browser

## Features

- **Smart URL Detection**: Automatically detects URLs from active browser windows
- **Beautiful Reports**: Generates clean, modern HTML reports with:
  - Clear violation summaries
  - Impact levels and descriptions
  - Code snippets and fixes
  - WCAG criteria references
- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Error Handling**: Clear error messages and logging
- **Zero Configuration**: Works out of the box

## Requirements

- Node.js and npm
- Python 3.7 or higher
- A modern web browser (Chrome, Safari, or Firefox on macOS; Chrome on Windows/Linux)
- Stream Deck software

### System-Specific Requirements

- **macOS**: No additional requirements
- **Linux**: Install `xdotool` for active window detection:
  ```bash
  # Ubuntu/Debian:
  sudo apt-get install xdotool
  # Fedora:
  sudo dnf install xdotool
  ```
- **Windows**: No additional requirements

## Troubleshooting

### No URL Found
- Make sure you have an active browser window with a URL
- Or copy a URL to your clipboard before pressing the button

### Axe CLI Not Found
If you see "axe-core CLI not found":
1. Open Terminal
2. Run: `npm install -g @axe-core/cli`
3. Try the button again

### Other Issues
- Check the logs in `~/axe_reports/logs/`
- Make sure Node.js and npm are installed
- Ensure you have a supported browser installed

## Configuration

### Custom Reports Directory
Set the environment variable:
```bash
AXE_REPORTS_DIR=/path/to/custom/directory
```

## Report Location

Reports and logs are saved in:
- Default: `~/axe_reports/`
- Logs: `~/axe_reports/logs/` 