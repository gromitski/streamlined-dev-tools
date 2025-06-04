#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform
from datetime import datetime
from pathlib import Path
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import html
from typing import Optional

# Initialize rich console first
console = Console()

# Add the project root to Python path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
sys.path.insert(0, PROJECT_ROOT)

# Try to import tkinter, but have a fallback
try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

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

def show_error_dialog(message):
    """Show an error message in a modal dialog or fallback to console."""
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Axe Audit Error", message)
        root.destroy()
    else:
        console.print(Panel(f"[red]Error:[/red] {message}", title="Axe Audit Error", style="red"))

def get_url_from_clipboard():
    """Get URL from clipboard with error handling."""
    try:
        text = pyperclip.paste()
        # Basic URL validation
        if text and any(text.startswith(prefix) for prefix in ['http://', 'https://']):
            return text
    except:
        pass
    return None

def check_axe_cli():
    """Check if axe-core CLI is installed and working."""
    try:
        # Try to get version info
        result = subprocess.run(['axe', '--version'], capture_output=True, text=True)
        
        if result.returncode != 0:
            error_msg = (
                "axe-core CLI is installed but not working properly.\n"
                "Try reinstalling it with: npm install -g @axe-core/cli"
            )
            if result.stderr:
                error_msg += f"\nError: {result.stderr}"
            show_error_dialog(error_msg)
            return False
            
        return True
        
    except FileNotFoundError:
        show_error_dialog(
            "axe-core CLI not found!\n\n"
            "Please install it first:\n"
            "1. Visit https://nodejs.org\n"
            "2. Download and install Node.js\n"
            "3. Open Terminal and run: npm install -g @axe-core/cli\n"
            "4. Restart your terminal/IDE"
        )
        return False
    except Exception as e:
        show_error_dialog(
            f"Error checking axe-core CLI: {str(e)}\n\n"
            "Please make sure it's installed correctly:\n"
            "npm install -g @axe-core/cli"
        )
        return False

def setup_output_directory():
    """Set up the output directory for reports and logs."""
    reports_dir = os.getenv('AXE_REPORTS_DIR', os.path.expanduser('~/axe_reports'))
    logs_dir = os.path.join(reports_dir, 'logs')
    
    # Create directories if they don't exist
    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    Path(logs_dir).mkdir(parents=True, exist_ok=True)
    
    return reports_dir, logs_dir

def generate_html_report(results, report_file):
    """Generate an HTML report from axe-core results."""
    if isinstance(results, list):
        results = results[0]
    
    violations = results.get('violations', [])
    incomplete = results.get('incomplete', [])
    passes = results.get('passes', [])
    
    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Audit Report</title>
    <style>
        :root {{
            --color-text: #2c3e50;
            --color-background: #f5f5f5;
            --color-white: #ffffff;
            --color-border: #e9ecef;
            --color-link: #0066cc;
            
            --color-critical: #dc3545;
            --color-serious: #fd7e14;
            --color-moderate: #ffc107;
            --color-minor: #17a2b8;
            
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 1px 3px rgba(0,0,0,0.1);
            
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: var(--space-lg);
            background: var(--color-background);
            color: var(--color-text);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--color-white);
            padding: var(--space-xl);
            border-radius: var(--space-sm);
            box-shadow: var(--shadow-md);
        }}
        
        h1 {{
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            margin: 0 0 var(--space-xl) 0;
            padding-bottom: var(--space-md);
            border-bottom: 2px solid var(--color-border);
            color: var(--color-text);
        }}
        
        h2 {{
            font-size: 20px;
            font-weight: 600;
            margin: var(--space-xl) 0 var(--space-lg) 0;
            padding-bottom: var(--space-sm);
            border-bottom: 1px solid var(--color-border);
            color: var(--color-text);
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-lg);
            margin: var(--space-xl) 0;
        }}
        
        .summary-item {{
            padding: var(--space-lg);
            border-radius: var(--space-sm);
            text-align: center;
        }}
        
        .summary-label {{
            font-size: 16px;
            font-weight: 500;
        }}
        
        .summary-count {{
            font-size: 32px;
            font-weight: 600;
            margin: var(--space-sm) 0;
        }}
        
        .passes {{ 
            background: #e8f5e9;
            color: #1b5e20;
        }}
        
        .incomplete {{ 
            background: #fff3e0;
            color: #e65100;
        }}
        
        .violations {{ 
            background: #ffebee;
            color: #b71c1c;
        }}
        
        .issue {{
            margin: var(--space-lg) 0;
            padding: var(--space-lg);
            border-radius: var(--space-sm);
            background: var(--color-white);
            border: 1px solid var(--color-border);
        }}
        
        .issue-header {{
            display: flex;
            align-items: flex-start;
            gap: var(--space-sm);
            margin-bottom: var(--space-md);
        }}
        
        .impact {{
            display: inline-block;
            padding: var(--space-xs) var(--space-sm);
            border-radius: var(--space-xs);
            font-weight: 500;
            font-size: 14px;
            min-width: 80px;
            text-align: center;
            color: var(--color-white);
        }}
        
        .impact-critical {{ background: var(--color-critical); }}
        .impact-serious {{ background: var(--color-serious); }}
        .impact-moderate {{ background: var(--color-moderate); color: #000; }}
        .impact-minor {{ background: var(--color-minor); }}
        
        .issue-title {{
            font-size: 16px;
            font-weight: 500;
            color: var(--color-text);
            flex: 1;
        }}
        
        .help-link {{
            display: inline-block;
            margin-bottom: var(--space-lg);
            color: var(--color-link);
            text-decoration: none;
            font-size: 14px;
        }}
        
        .help-link:hover {{
            text-decoration: underline;
        }}
        
        .element {{
            margin: var(--space-md) 0;
            padding: var(--space-md);
            background: #f8f9fa;
            border-radius: var(--space-xs);
            border: 1px solid var(--color-border);
        }}
        
        .element-html {{
            font-family: Monaco, monospace;
            font-size: 13px;
            padding: var(--space-sm);
            background: var(--color-white);
            border-radius: var(--space-xs);
            border: 1px solid var(--color-border);
            overflow-x: auto;
            margin: var(--space-sm) 0;
        }}
        
        .element-summary {{
            margin-top: var(--space-sm);
            color: #666;
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: 1fr;
            }}
            
            .container {{
                padding: var(--space-lg);
            }}
            
            .issue {{
                padding: var(--space-md);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Accessibility Audit Report</h1>
        
        <div class="summary">
            <div class="summary-item violations">
                <div class="summary-label">Violations</div>
                <div class="summary-count">{len(violations)}</div>
            </div>
            <div class="summary-item incomplete">
                <div class="summary-label">Needs Review</div>
                <div class="summary-count">{len(incomplete)}</div>
            </div>
            <div class="summary-item passes">
                <div class="summary-label">Passed</div>
                <div class="summary-count">{len(passes)}</div>
            </div>
        </div>
"""
    
    if violations:
        report_html += """
        <h2>Violations</h2>
"""
        for violation in violations:
            impact = violation.get('impact', 'unknown')
            report_html += f"""
            <div class="issue">
                <div class="issue-header">
                    <span class="impact impact-{impact}">{impact.title()}</span>
                    <div class="issue-title">{html.escape(violation.get('help', violation.get('description', 'No description')))}</div>
                </div>
                <a href="{violation.get('helpUrl', '#')}" class="help-link" target="_blank">Learn more about this issue</a>
"""
            for node in violation.get('nodes', []):
                report_html += f"""
                <div class="element">
                    <div class="element-html">{html.escape(node.get('html', 'No HTML available'))}</div>
                    <div class="element-summary">{html.escape(node.get('failureSummary', ''))}</div>
                </div>
"""
            report_html += """
            </div>
"""
    
    if incomplete:
        report_html += """
        <h2>Needs Review</h2>
"""
        for item in incomplete:
            impact = item.get('impact', 'unknown')
            report_html += f"""
            <div class="issue">
                <div class="issue-header">
                    <span class="impact impact-{impact}">{impact.title()}</span>
                    <div class="issue-title">{html.escape(item.get('help', item.get('description', 'No description')))}</div>
                </div>
                <a href="{item.get('helpUrl', '#')}" class="help-link" target="_blank">Learn more about this issue</a>
"""
            for node in item.get('nodes', []):
                report_html += f"""
                <div class="element">
                    <div class="element-html">{html.escape(node.get('html', 'No HTML available'))}</div>
                    <div class="element-summary">{html.escape(node.get('failureSummary', ''))}</div>
                </div>
"""
            report_html += """
            </div>
"""
    
    report_html += """
        </div>
    </div>
</body>
</html>
"""
    
    with open(report_file, 'w') as f:
        f.write(report_html)

def run_axe_audit(url, reports_dir, logs_dir):
    """Run the axe-core audit on the specified URL."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = url.split('/')[2] if '://' in url else url.split('/')[0]
    
    # Simplified command - just get the core results
    cmd = ['axe', url, '--stdout']
    
    # Set up logging
    log_file = os.path.join(logs_dir, f'axe_audit_{timestamp}.log')
    with open(log_file, 'w') as log:
        log.write(f'Running axe-core audit on: {url}\n')
        log.write(f'Command: {" ".join(cmd)}\n\n')
        
        try:
            # Add timeout to prevent hanging
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            # Log both stdout and stderr
            if result.stdout:
                log.write("STDOUT:\n")
                log.write(result.stdout)
                log.write("\n")
            
            if result.stderr:
                log.write("STDERR:\n")
                log.write(result.stderr)
                log.write("\n")
            
            if result.returncode != 0:
                error_msg = f"axe-core CLI failed with return code {result.returncode}.\n"
                if result.stderr:
                    error_msg += f"Error: {result.stderr}\n"
                log.write(f"ERROR: {error_msg}")
                show_error_dialog(f"Error running axe-core audit:\n{error_msg}\nCheck the log file: {log_file}")
                return False
            
            try:
                results = json.loads(result.stdout)
                
                # Always generate HTML report
                report_file = os.path.join(reports_dir, f'axe_{domain}_{timestamp}.html')
                generate_html_report(results, report_file)
                
                # Display results in terminal
                display_terminal_results(results)
                
                # Open HTML report in browser
                console.print(f"\nOpening HTML report: {report_file}")
                if platform.system() == 'Darwin':
                    subprocess.run(['open', report_file])
                elif platform.system() == 'Windows':
                    os.startfile(report_file)
                else:
                    subprocess.run(['xdg-open', report_file])
                
                return True
                
            except json.JSONDecodeError as e:
                log.write(f"JSON Parse Error: {str(e)}\n")
                log.write(f"Raw output:\n{result.stdout}\n")
                show_error_dialog(
                    f"Failed to parse axe-core results.\n"
                    f"JSON Error: {str(e)}\n"
                    f"Check the log file: {log_file}"
                )
                return False
            
        except subprocess.TimeoutExpired:
            error_msg = "axe-core audit timed out after 30 seconds"
            log.write(f"ERROR: {error_msg}\n")
            show_error_dialog(f"{error_msg}\nCheck the log file: {log_file}")
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            log.write(f"ERROR: {error_msg}\n")
            show_error_dialog(f"{error_msg}\nCheck the log file: {log_file}")
            return False

def display_terminal_results(results):
    """Display axe-core results in a formatted terminal output."""
    if isinstance(results, list):
        results = results[0]  # axe-core returns a list with one result object
    
    violations = results.get('violations', [])
    incomplete = results.get('incomplete', [])
    passes = results.get('passes', [])
    
    # Show summary
    console.print("\n=== Axe Core Audit Results ===\n")
    console.print(f"✅ Passed: {len(passes)} checks")
    console.print(f"⚠️  Needs review: {len(incomplete)} checks")
    console.print(f"❌ Violations: {len(violations)} checks\n")
    
    if not violations and not incomplete:
        console.print(Panel("✅ No accessibility violations found!", style="green"))
        return
    
    # Show violations
    if violations:
        table = Table(title=f"Found {len(violations)} accessibility violations")
        table.add_column("Impact", style="red")
        table.add_column("Description")
        table.add_column("WCAG Criteria")
        
        for violation in violations:
            table.add_row(
                violation.get('impact', 'unknown'),
                violation.get('help', violation.get('description', 'No description')),
                ", ".join(violation.get('tags', []))
            )
        
        console.print(table)
        console.print()
    
    # Show items needing review
    if incomplete:
        table = Table(title=f"Found {len(incomplete)} items needing review")
        table.add_column("Impact", style="yellow")
        table.add_column("Description")
        table.add_column("WCAG Criteria")
        
        for item in incomplete:
            table.add_row(
                item.get('impact', 'unknown'),
                item.get('help', item.get('description', 'No description')),
                ", ".join(item.get('tags', []))
            )
        
        console.print(table)

def main():
    """Main function to run the axe-core audit."""
    # Load environment variables
    load_dotenv()
    
    # Check if axe-core CLI is installed
    if not check_axe_cli():
        sys.exit(1)
    
    # Set up output directories
    reports_dir, logs_dir = setup_output_directory()
    
    # Get URL from command line, active window, or clipboard
    url = None
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Try browser first
        try:
            url = get_active_browser_url()
            if url:
                console.print(f"[dim]Found URL in active browser: {url}[/dim]")
        except Exception as e:
            console.print(f"[dim]Error getting browser URL: {e}[/dim]")
        
        # Then try clipboard if browser failed
        if not url:
            url = get_url_from_clipboard()
            if url:
                console.print(f"[dim]Found URL in clipboard: {url}[/dim]")
    
    if not url or not url.startswith(('http://', 'https://')):
        show_error_dialog(
            "No valid URL found!\n\n"
            "Please either:\n"
            "1. Have an active browser window with the URL\n"
            "2. Copy a URL to your clipboard\n"
            "3. Provide a URL as a command line argument"
        )
        sys.exit(1)
    
    # Run the audit
    success = run_axe_audit(url, reports_dir, logs_dir)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 