# Lighthouse Accessibility Audit Tool

## Overview
A Stream Deck-optimized tool that runs Lighthouse audits on web pages using the official Lighthouse CLI. It can take a URL from the active browser window, command line, or clipboard, making it perfect for quick accessibility checks while browsing.

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

### Production Mode (Silent Operation)
1. Install the "System: Open" action or a Python script launcher plugin
2. Configure the button:
   - Set the script path to the `lighthouse_audit.py` script
   - (Optional) Add an icon representing accessibility testing
   - (Optional) Add a title like "Audit Page"

### Debug Mode (With Terminal Output)
For testing and troubleshooting, use one of the debug launcher scripts:

#### Windows
1. Create a new Stream Deck button
2. Choose "System: Open" action
3. Set the path to `debug_launcher.bat`
4. The script will open a command prompt window showing the progress

#### macOS and Linux
1. Create a new Stream Deck button
2. Choose "System: Open" action
3. Set the path to `debug_launcher.sh`
4. The script will open a terminal window showing the progress

## Usage
### Basic Usage
1. Navigate to the webpage you want to audit in your browser
2. Press the Stream Deck button
3. The script will:
   1. Try to get the URL from the active browser window
   2. If that fails, try to get it from your clipboard
   3. If both fail, show an error message
4. Wait for the audit to complete
5. The report will automatically open in your default browser

### Command Line Usage
```bash
# Normal mode (silent operation)
python lighthouse_audit.py [URL]

# Debug mode (with detailed output)
python lighthouse_audit.py -d [URL]
```

### Debug Mode Features
When running in debug mode (-d flag), the script will:
1. Open in a terminal window
2. Show detailed progress information
3. Display the exact commands being run
4. Show any error messages or output
5. Wait for user input before closing
6. Keep the terminal window open for inspection

### Configuration
The tool can be configured through environment variables in a `.env` file:

```env
# Optional: Custom directory for storing reports
# Default: ~/lighthouse_reports
LIGHTHOUSE_REPORTS_DIR=/path/to/custom/reports/directory
```

### Output
- Reports are saved in `~/lighthouse_reports/` by default (can be customized via `LIGHTHOUSE_REPORTS_DIR`)
- Filename format: `lighthouse_domain_YYYYMMDD_HHMMSS.html`
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
- Debug mode with detailed output
- Headless Chrome operation (no visible browser window)
- Comprehensive HTML reports
- Local report storage for reference
- Progress indication during audit
- Error handling with clear messages
- Customizable reports directory

## Troubleshooting
Common issues and solutions:

1. **No URL Found**
   - Make sure your browser window is in focus
   - Try copying the URL to your clipboard
   - Try passing the URL directly as a command line argument
   - Run in debug mode to see what's happening

2. **Chrome Not Found**
   - Ensure Chrome is installed on your system
   - The script uses headless Chrome for auditing
   - Run in debug mode to see the exact error

3. **Report Not Opening**
   - Check if the report was generated in the configured reports directory
   - Try opening the report manually from the directory
   - Run in debug mode to see the full path

4. **Active Window Detection Not Working**
   - macOS: Make sure your browser is allowed in System Settings > Privacy & Security > Automation
   - Windows: Ensure PowerShell is available
   - Linux: Check if xdotool is installed (`which xdotool`)
   - Run in debug mode to see which detection method is being used

5. **Stream Deck Button Not Working**
   - Try using the debug launcher script instead of the main script
   - Check the file paths in your Stream Deck button configuration
   - Make sure Python is in your system PATH
   - Look for error messages in the debug terminal window

## Notes
- Reports are stored locally and can be accessed later
- The tool uses the official Lighthouse CLI, providing the same results as Chrome DevTools
- For best results, ensure you have a stable internet connection
- The script runs Chrome in headless mode to avoid visual disruption
- Browser window detection works with Chrome, Safari, and Firefox on macOS, and most modern browsers on Windows and Linux
- Debug mode is perfect for testing and troubleshooting Stream Deck integration 