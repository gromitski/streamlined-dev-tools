# Axe Core CLI Audit Tool

A Stream Deck button that runs axe-core CLI accessibility audits on URLs. It can get the URL from:
1. Active browser window
2. Clipboard
3. Command line argument

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
- Display results in terminal or open HTML report

## Usage

The button will:
1. Look for a URL in this order:
   - Active browser window
   - Clipboard (if no browser window found)
   - Command line argument (if provided)
2. Run an axe-core audit
3. Either:
   - Display results in terminal (default)
   - Generate an HTML report in `~/axe_reports/` (optional)
4. Show error dialogs if any issues occur

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

### Axe CLI Not Found
If you see "axe-core CLI not found":
1. Open Terminal
2. Run: `npm install -g @axe-core/cli`
3. Try the button again

### Other Issues
- Check the logs in `~/axe_reports/logs/`
- Make sure Node.js and npm are installed
- Ensure Chrome/Chromium is installed

## Configuration

### Output Format
Set the environment variable:
```bash
AXE_OUTPUT_FORMAT=html  # For HTML reports (default: terminal)
```

### Custom Reports Directory
Set the environment variable:
```bash
AXE_REPORTS_DIR=/path/to/custom/directory
```

## Report Location

Reports and logs are saved in:
- Default: `~/axe_reports/`
- Logs: `~/axe_reports/logs/` 