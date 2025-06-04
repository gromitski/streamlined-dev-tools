# Lighthouse Accessibility Audit Tool

## Overview
A Stream Deck-optimized tool that runs Lighthouse audits on web pages using the official Lighthouse CLI. It can take a URL from the active browser window, command line, or clipboard, making it perfect for quick accessibility checks while browsing. The tool provides visual feedback through Stream Deck and maintains detailed logs for troubleshooting.

## Requirements
- Python 3.8 or higher
- Node.js and npm
- Required Python packages (automatically installed with the package):
  - pyperclip
  - rich
  - python-dotenv
- Lighthouse CLI (installed globally via npm):
  ```bash
  npm install -g lighthouse
  ```
- Platform-specific requirements:
  - macOS: None (uses built-in AppleScript)
  - Windows: PowerShell (pre-installed)
  - Linux: xdotool (`sudo apt-get install xdotool` on Ubuntu/Debian)

## Installation
1. Ensure Node.js and npm are installed
2. Install Lighthouse CLI globally:
   ```bash
   npm install -g lighthouse
   ```
3. Install the Python package and dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Linux only) Install xdotool:
   ```bash
   sudo apt-get install xdotool  # Ubuntu/Debian
   sudo dnf install xdotool      # Fedora
   sudo pacman -S xdotool        # Arch Linux
   ```

## Stream Deck Setup

### Basic Setup
1. Install the "System: Open" action
2. Configure the button:
   - Set the script path to the `lighthouse_audit.py` script
   - Set up success/fail states:
     - Success: When script outputs "success"
     - Fail: When script outputs "fail"
   - (Optional) Add icons for success/fail states
   - (Optional) Add a title like "Audit Page"

### Status Returns
The script will return one of two values:
- `success`: Audit completed successfully
- `fail`: Audit failed (check logs for details)

### Logging
- All actions are logged to: `~/lighthouse_reports/logs/`
- Log filename format: `lighthouse_audit_YYYYMMDD_HHMMSS.log`
- Logs include:
  - URL detection attempts
  - Command execution details
  - Error messages
  - Success/failure status

## Usage
### Basic Usage
1. Navigate to the webpage you want to audit in your browser
2. Press the Stream Deck button
3. The script will:
   1. Try to get the URL from the active browser window
   2. If that fails, try to get it from your clipboard
   3. If both fail, show an error and return "fail"
4. Wait for the audit to complete
5. The report will automatically open in your browser
6. Stream Deck button will show success/fail state

### Command Line Usage
```bash
python lighthouse_audit.py [URL]
```

### Configuration
The tool can be configured through environment variables in a `.env` file:

```env
# Optional: Custom directory for storing reports
# Default: ~/lighthouse_reports
LIGHTHOUSE_REPORTS_DIR=/path/to/custom/reports/directory
```

### Output
- Reports are saved in `~/lighthouse_reports/` by default (can be customized via `LIGHTHOUSE_REPORTS_DIR`)
- Logs are saved in `~/lighthouse_reports/logs/`
- Filename formats:
  - Reports: `lighthouse_domain_YYYYMMDD_HHMMSS.html`
  - Logs: `lighthouse_audit_YYYYMMDD_HHMMSS.log`
- Reports include scores for:
  - Accessibility
  - Performance
  - Best Practices
  - PWA
  - SEO

## Features
- URL detection from:
  1. Active browser window (Chrome, Safari, Firefox)
  2. Command line arguments
  3. Clipboard content
- Cross-platform support (macOS, Windows, Linux)
- Stream Deck integration:
  - Visual success/fail feedback
  - Status-based icons
- Detailed logging system
- Headless Chrome operation
- Comprehensive HTML reports
- Local report storage
- Progress indication
- Error handling with logs

## Troubleshooting
Common issues and solutions:

1. **No URL Found**
   - Make sure your browser window is in focus
   - Try copying the URL to your clipboard
   - Check the logs for URL detection attempts

2. **Chrome Not Found**
   - Ensure Chrome is installed on your system
   - Check the logs for specific error messages
   - The script uses headless Chrome for auditing

3. **Report Not Opening**
   - Check if the report was generated in the configured reports directory
   - Look in the logs for the exact report path
   - Try opening the report manually

4. **Active Window Detection Not Working**
   - macOS: Make sure your browser is allowed in System Settings > Privacy & Security > Automation
   - Windows: Ensure PowerShell is available
   - Linux: Check if xdotool is installed (`which xdotool`)
   - Check logs for detection method used

5. **Stream Deck Button Not Working**
   - Check the logs in `~/lighthouse_reports/logs/`
   - Verify the script path in Stream Deck configuration
   - Make sure Python is in your system PATH
   - Check if the button shows the fail state

## Notes
- Reports are stored locally and can be accessed later
- Logs provide detailed information for troubleshooting
- The tool uses the official Lighthouse CLI
- For best results, ensure you have a stable internet connection
- The script runs Chrome in headless mode
- Browser window detection works with Chrome, Safari, and Firefox on macOS, and most modern browsers on Windows and Linux
- Stream Deck integration provides visual feedback for success/failure 