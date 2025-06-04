#!/usr/bin/env python3
"""
Example usage of the Lighthouse Accessibility Audit Tool
"""

import sys
sys.path.append('../../src')  # Add src directory to path

from tools.accessibility.lighthouse.lighthouse_audit import main

if __name__ == "__main__":
    # The main function will automatically:
    # 1. Check for URL in command line arguments
    # 2. If no URL provided, check clipboard
    # 3. Run the audit
    # 4. Generate and open the report
    main() 