# Lighthouse Accessibility Audit Tool

## Overview
A Stream Deck-optimized tool that runs Lighthouse audits on web pages. It can take a URL from the command line or automatically grab it from your clipboard, making it perfect for quick accessibility checks while browsing.

## Requirements
- Python 3.8 or higher
- Required Python packages (automatically installed with the package):
  - pyperclip
  - requests
  - rich
  - python-dotenv
- Optional: Google PageSpeed Insights API key for higher quota

## Installation
The tool is automatically installed with the package. However, for optimal performance:

1. (Optional) Get a Google PageSpeed Insights API key:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the PageSpeed Insights API
   - Create credentials
   - Add your API key to `.env` file:
     ```
     PAGESPEED_API_KEY=your_api_key_here
     ```

## Stream Deck Setup
1. Install the "System: Launch Application" action or a Python script launcher plugin
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

### Output
- Reports are saved in `~/lighthouse_reports/`
- Filename format: `lighthouse_domain_YYYYMMDD_HHMMSS.html`
- Reports include scores for:
  - Accessibility
  - Performance
  - Best Practices
  - PWA
  - SEO

## Configuration
The tool can be configured through environment variables in a `.env` file:
```env
PAGESPEED_API_KEY=your_api_key_here  # Optional: for higher API quota
```

## Troubleshooting
Common issues and solutions:

1. **No URL Found**
   - Ensure you've copied a valid URL to your clipboard
   - Try passing the URL directly as a command line argument

2. **API Rate Limit**
   - Get a PageSpeed Insights API key
   - Add it to your `.env` file

3. **Report Not Opening**
   - Check if the report was generated in `~/lighthouse_reports/`
   - Try opening the report manually from the directory

## Notes
- Reports are stored locally and can be accessed later
- The tool uses the PageSpeed Insights API, which provides Lighthouse results without needing Chrome installed
- For best results, ensure you have a stable internet connection 