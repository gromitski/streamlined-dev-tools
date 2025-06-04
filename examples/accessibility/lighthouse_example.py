#!/usr/bin/env python3
"""
Example usage of the Lighthouse Accessibility Audit Tool

This example demonstrates:
1. How to import and use the Lighthouse audit tool
2. Different ways to provide URLs (command line or clipboard)
3. Basic error handling

Usage:
    python lighthouse_example.py [URL]
    
If no URL is provided, the script will attempt to get one from the clipboard.
"""

import sys
sys.path.append('../../src')  # Add src directory to path

from tools.accessibility.lighthouse.lighthouse_audit import main

if __name__ == "__main__":
    # The main function will:
    # 1. Check for URL in command line arguments
    # 2. If no URL provided, check clipboard
    # 3. Run the Lighthouse audit using Chrome in headless mode
    # 4. Generate and open the HTML report
    # 5. Save the report in ~/lighthouse_reports/
    main()

# Example URLs to test with:
# - https://example.com
# - https://www.google.com
# - https://github.com 