#!/usr/bin/env python3
"""
Test script to simulate copying a URL to clipboard
"""

import pyperclip

# Copy a test URL to clipboard
test_url = "https://example.com"
pyperclip.copy(test_url)
print(f"Copied URL to clipboard: {test_url}") 