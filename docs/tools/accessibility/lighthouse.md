# Lighthouse Accessibility Audit Tool

## Overview
A Stream Deck-optimized tool that runs Lighthouse audits on web pages using the official Lighthouse CLI. It can take a URL from the command line or automatically grab it from your clipboard, making it perfect for quick accessibility checks while browsing.

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

## Stream Deck Setup
1. Install the "System: Open" action or a Python script launcher plugin
2. Configure the button:
   - Set the script path to the `lighthouse_audit.py` script
   - (Optional) Add an icon representing accessibility testing
   - (Optional) Add a title like "Audit Page"

## Usage
### Basic Usage
1. Navigate to the webpage you want to audit in your browser
2. Copy the URL (Cmd/Ctrl + L, Cmd/Ctrl + C)
3. Press the Stream Deck button
4. Wait for the audit to complete
5. The report will automatically open in your default browser

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
- Filename format: `lighthouse_domain_YYYYMMDD_HHMMSS.html`
- Reports include scores for:
  - Accessibility
  - Performance
  - Best Practices
  - PWA
  - SEO

## Features
- Automatic URL detection from clipboard
- Headless Chrome operation (no visible browser window)
- Comprehensive HTML reports
- Local report storage for reference
- Progress indication during audit
- Error handling with clear messages
- Customizable reports directory

## Troubleshooting
Common issues and solutions:

1. **No URL Found**
   - Ensure you've copied a valid URL to your clipboard
   - Try passing the URL directly as a command line argument

2. **Chrome Not Found**
   - Ensure Chrome is installed on your system
   - The script uses headless Chrome for auditing

3. **Report Not Opening**
   - Check if the report was generated in the configured reports directory
   - Try opening the report manually from the directory

## Notes
- Reports are stored locally and can be accessed later
- The tool uses the official Lighthouse CLI, providing the same results as Chrome DevTools
- For best results, ensure you have a stable internet connection
- The script runs Chrome in headless mode to avoid visual disruption 