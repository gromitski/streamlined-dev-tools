#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

# Initialize rich console
console = Console()

def show_error_dialog(message):
    """Show an error message in a modal dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Axe Audit Error", message)
    root.destroy()

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
                return URL of active tab of front window
            end tell
        else if frontApp is "Safari" then
            tell application "Safari"
                return URL of current tab of front window
            end tell
        else if frontApp is "Firefox" then
            tell application "Firefox"
                return URL of active tab of front window
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

def run_axe_audit(url, reports_dir, logs_dir):
    """Run the axe-core audit on the specified URL."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = url.split('/')[2] if '://' in url else url.split('/')[0]
    output_format = os.getenv('AXE_OUTPUT_FORMAT', 'terminal').lower()
    
    if output_format == 'html':
        # Generate HTML report
        report_file = os.path.join(reports_dir, f'axe_{domain}_{timestamp}.html')
        cmd = ['axe', url, '--save', report_file, '--html-report']
    else:
        # Output to terminal in JSON format
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
                
            if output_format == 'html':
                # Open the HTML report
                if platform.system() == 'Darwin':
                    subprocess.run(['open', report_file])
                elif platform.system() == 'Windows':
                    os.startfile(report_file)
                else:
                    subprocess.run(['xdg-open', report_file])
            else:
                # Display results in terminal
                try:
                    results = json.loads(result.stdout)
                    display_terminal_results(results)
                except json.JSONDecodeError:
                    console.print(result.stdout)
            
            return True
            
        except Exception as e:
            log.write(f'Error: {str(e)}\n')
            show_error_dialog(f"Error running axe-core audit.\nCheck the log file: {log_file}")
            return False

def display_terminal_results(results):
    """Display axe-core results in a formatted terminal output."""
    violations = results.get('violations', [])
    
    if not violations:
        console.print(Panel("✅ No accessibility violations found!", style="green"))
        return
        
    table = Table(title=f"Found {len(violations)} accessibility violations")
    table.add_column("Impact", style="red")
    table.add_column("Description")
    table.add_column("WCAG Criteria")
    
    for violation in violations:
        table.add_row(
            violation.get('impact', 'unknown'),
            violation.get('description', 'No description'),
            ", ".join(violation.get('tags', []))
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