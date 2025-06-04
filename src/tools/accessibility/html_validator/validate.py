#!/usr/bin/env python3
"""HTML Validator tool that uses W3C's validation service to check HTML pages."""

import subprocess
import sys
import urllib.parse
import webbrowser
from typing import Optional

import pyperclip


def get_active_url_macos() -> Optional[str]:
    """Get URL from active browser window on macOS."""
    script = """
    tell application "Google Chrome"
        if frontmost then
            get URL of active tab of front window
        end if
    end tell
    """
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except subprocess.SubprocessError:
        pass
    return None


def get_url_from_clipboard() -> Optional[str]:
    """Get URL from clipboard with error handling."""
    try:
        text = pyperclip.paste()
        if text and any(text.startswith(prefix) for prefix in ["http://", "https://"]):
            return text
    except Exception:  # Handle any clipboard-related errors
        pass
    return None


def get_url() -> Optional[str]:
    """Get URL from command line, active browser window, or clipboard."""
    # First, check command line arguments
    if len(sys.argv) > 1:
        return sys.argv[1]

    # Then try to get URL from active browser window
    if sys.platform == "darwin":
        url = get_active_url_macos()
        if url:
            print(f"Found URL in active browser: {url}")
            return url

    # Finally, try clipboard
    url = get_url_from_clipboard()
    if url:
        print(f"Found URL in clipboard: {url}")
        return url

    return None


def main() -> None:
    """Open W3C HTML Validator with the URL from clipboard or browser."""
    url = get_url()
    if not url:
        print("No URL found! Please either:")
        print("1. Provide a URL as an argument")
        print("2. Have an active Chrome window with a URL")
        print("3. Copy a URL to your clipboard")
        sys.exit(1)

    try:
        # Escape the URL properly
        escaped_url = urllib.parse.quote_plus(url)

        # Build validator URL
        validator_url = f"https://validator.w3.org/nu/?doc={escaped_url}"

        # Open in browser
        print(f"Opening W3C HTML Validator for: {url}")
        webbrowser.open(validator_url)

    except Exception as e:
        print(f"Error validating HTML: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
