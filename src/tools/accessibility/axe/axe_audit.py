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

# Initialize rich console
console = Console()

# Try to import tkinter, but have a fallback
try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

def show_error_dialog(message):
    """Show an error message in a modal dialog or fallback to console."""
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Axe Audit Error", message)
        root.destroy()
    else:
        console.print(Panel(f"[red]Error:[/red] {message}", title="Axe Audit Error", style="red"))

def get_active_url():
    """Get URL from active browser window based on OS."""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
        end tell
        
        if frontApp is "Google Chrome" then
            tell application "Google Chrome"
                get URL of active tab of front window
            end tell
        else if frontApp is "Safari" then
            tell application "Safari"
                get URL of current tab of front window
            end tell
        else if frontApp is "Firefox" then
            tell application "Firefox"
                get URL of active tab of front window
            end tell
        end if
        '''
        try:
            return subprocess.check_output(['osascript', '-e', script]).decode().strip()
        except:
            return None
            
    elif system == "windows":
        try:
            import win32gui
            import win32process
            import psutil
            
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            
            if any(browser in process.name().lower() for browser in ['chrome', 'firefox', 'iexplore', 'edge']):
                title = win32gui.GetWindowText(window)
                if ' - ' in title:
                    return title.split(' - ')[-1]
        except:
            return None
            
    elif system == "linux":
        try:
            wm_class = subprocess.check_output(['xprop', '-id', '$(xprop -root _NET_ACTIVE_WINDOW | cut -d# -f2)', 'WM_CLASS']).decode()
            if any(browser in wm_class.lower() for browser in ['chrome', 'firefox', 'chromium']):
                title = subprocess.check_output(['xprop', '-id', '$(xprop -root _NET_ACTIVE_WINDOW | cut -d# -f2)', '_NET_WM_NAME']).decode()
                if ' - ' in title:
                    return title.split(' - ')[-1]
        except:
            return None
    
    return None

def check_axe_cli():
    """Check if axe-core CLI is installed."""
    try:
        subprocess.run(['axe', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        show_error_dialog(
            "axe-core CLI not found!\n\n"
            "Please install it first:\n"
            "1. Visit https://nodejs.org\n"
            "2. Download and install Node.js\n"
            "3. Restart your computer\n"
            "4. Open Terminal and run: npm install -g @axe-core/cli"
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
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Axe Accessibility Audit Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-item {{
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .passes {{ background: #d4edda; color: #155724; }}
        .incomplete {{ background: #fff3cd; color: #856404; }}
        .violations {{ background: #f8d7da; color: #721c24; }}
        .issue-section {{
            margin: 30px 0;
            padding: 20px;
            border-radius: 6px;
            background: white;
        }}
        .issue {{
            border: 1px solid #ddd;
            margin: 10px 0;
            padding: 15px;
            border-radius: 4px;
        }}
        .impact-critical {{ border-left: 5px solid #dc3545; }}
        .impact-serious {{ border-left: 5px solid #fd7e14; }}
        .impact-moderate {{ border-left: 5px solid #ffc107; }}
        .impact-minor {{ border-left: 5px solid #17a2b8; }}
        .tag {{
            display: inline-block;
            padding: 2px 8px;
            margin: 2px;
            background: #e9ecef;
            border-radius: 12px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Axe Accessibility Audit Report</h1>
        <div class="summary">
            <div class="summary-item passes">
                <h2>✅ Passed</h2>
                <p>{len(passes)} checks</p>
            </div>
            <div class="summary-item incomplete">
                <h2>⚠️ Needs Review</h2>
                <p>{len(incomplete)} checks</p>
            </div>
            <div class="summary-item violations">
                <h2>❌ Violations</h2>
                <p>{len(violations)} checks</p>
            </div>
        </div>
"""
    
    if violations:
        html += """
        <div class="issue-section">
            <h2>Violations</h2>
"""
        for violation in violations:
            impact = violation.get('impact', 'unknown')
            html += f"""
            <div class="issue impact-{impact}">
                <h3>{violation.get('help', violation.get('description', 'No description'))}</h3>
                <p><strong>Impact:</strong> {impact}</p>
                <p>{violation.get('helpUrl', '')}</p>
                <div class="tags">
                    {''.join(f'<span class="tag">{tag}</span>' for tag in violation.get('tags', []))}
                </div>
            </div>
"""
    
    if incomplete:
        html += """
        <div class="issue-section">
            <h2>Needs Review</h2>
"""
        for item in incomplete:
            impact = item.get('impact', 'unknown')
            html += f"""
            <div class="issue impact-{impact}">
                <h3>{item.get('help', item.get('description', 'No description'))}</h3>
                <p><strong>Impact:</strong> {impact}</p>
                <p>{item.get('helpUrl', '')}</p>
                <div class="tags">
                    {''.join(f'<span class="tag">{tag}</span>' for tag in item.get('tags', []))}
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    with open(report_file, 'w') as f:
        f.write(html)

def run_axe_audit(url, reports_dir, logs_dir):
    """Run the axe-core audit on the specified URL."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = url.split('/')[2] if '://' in url else url.split('/')[0]
    output_format = os.getenv('AXE_OUTPUT_FORMAT', 'terminal').lower()
    
    # Always get JSON output for processing
    cmd = ['axe', url, '--stdout', '--no-reporter']
    
    # Set up logging
    log_file = os.path.join(logs_dir, f'axe_audit_{timestamp}.log')
    with open(log_file, 'w') as log:
        log.write(f'Running axe-core audit on: {url}\n')
        log.write(f'Command: {" ".join(cmd)}\n\n')
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            log.write(result.stdout)
            log.write(result.stderr)
            
            if result.returncode != 0:
                show_error_dialog(f"Error running axe-core audit.\nCheck the log file: {log_file}")
                return False
            
            try:
                results = json.loads(result.stdout)
                
                if output_format == 'html':
                    # Generate and open HTML report
                    report_file = os.path.join(reports_dir, f'axe_{domain}_{timestamp}.html')
                    generate_html_report(results, report_file)
                    
                    if platform.system() == 'Darwin':
                        subprocess.run(['open', report_file])
                    elif platform.system() == 'Windows':
                        os.startfile(report_file)
                    else:
                        subprocess.run(['xdg-open', report_file])
                else:
                    # Display results in terminal
                    display_terminal_results(results)
                
                return True
                
            except json.JSONDecodeError:
                console.print(result.stdout)
                return True
            
        except Exception as e:
            log.write(f'Error: {str(e)}\n')
            show_error_dialog(f"Error running axe-core audit.\nCheck the log file: {log_file}")
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
        url = get_active_url()
        if not url:
            url = pyperclip.paste()
    
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