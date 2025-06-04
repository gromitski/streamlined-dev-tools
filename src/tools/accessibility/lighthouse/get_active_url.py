"""
Get URL from active browser window across different platforms.
Supports Chrome, Safari, Firefox on macOS, Windows, and Linux.
"""

import sys
import subprocess
from typing import Optional

def get_active_url_macos() -> Optional[str]:
    """Get URL from active browser window on macOS."""
    # Try Chrome first
    chrome_script = '''
    tell application "Google Chrome"
        if frontmost then
            get URL of active tab of front window
        end if
    end tell
    '''
    
    # Try Safari if Chrome fails
    safari_script = '''
    tell application "Safari"
        if frontmost then
            get URL of current tab of front window
        end if
    end tell
    '''
    
    # Try Firefox if Safari fails
    firefox_script = '''
    tell application "Firefox"
        if frontmost then
            get URL of active tab of front window
        end if
    end tell
    '''
    
    for script in [chrome_script, safari_script, firefox_script]:
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except subprocess.SubprocessError:
            continue
    
    return None

def get_active_url_windows() -> Optional[str]:
    """Get URL from active browser window on Windows."""
    # PowerShell script to get URL from Chrome
    chrome_script = r'''
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern IntPtr GetForegroundWindow();
            [DllImport("user32.dll")]
            public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
        }
"@
    $window = [Win32]::GetForegroundWindow()
    $buffer = New-Object System.Text.StringBuilder(512)
    [Win32]::GetWindowText($window, $buffer, $buffer.Capacity)
    $title = $buffer.ToString()
    
    # Extract URL from common browser title formats
    # Look for URLs in various browser title formats
    foreach ($pattern in @(
        "(?<url>https?://[^ -]+)",  # Basic URL pattern
        "(?<url>https?://\S+) [-–] ",  # URL followed by dash
        "[-–] (?<url>https?://\S+)$"  # URL at end after dash
    )) {
        if ($title -match $pattern) {
            return $matches['url']
        }
    }
    '''
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', chrome_script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except subprocess.SubprocessError:
        pass
    
    return None

def get_active_url_linux() -> Optional[str]:
    """Get URL from active browser window on Linux."""
    # Try using xdotool to get window title
    try:
        # Get active window ID
        window_id = subprocess.run(
            ['xdotool', 'getactivewindow'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Get window title
        title = subprocess.run(
            ['xdotool', 'getwindowname', window_id],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Extract URL from common browser title formats
        import re
        patterns = [
            r'(?:https?://\S+)',  # Basic URL pattern
            r'(?:https?://[^ ]+) [-–]',  # URL followed by dash
            r'[-–] (?:https?://[^ ]+)$'  # URL at end after dash
        ]
        
        for pattern in patterns:
            url_match = re.search(pattern, title)
            if url_match:
                return url_match.group(0).rstrip('- ')
                
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return None

def get_active_browser_url() -> Optional[str]:
    """Get URL from active browser window based on current platform."""
    if sys.platform == 'darwin':
        return get_active_url_macos()
    elif sys.platform == 'win32':
        return get_active_url_windows()
    elif sys.platform.startswith('linux'):
        return get_active_url_linux()
    return None

if __name__ == '__main__':
    # Test the function
    url = get_active_browser_url()
    print(f"Active browser URL: {url}") 