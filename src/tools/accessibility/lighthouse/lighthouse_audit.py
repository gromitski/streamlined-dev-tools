#!/usr/bin/env python3
"""
Lighthouse Accessibility Audit Tool

This script runs a Lighthouse audit on a URL (either provided or from clipboard)
and opens the report in Chrome.
"""

import os
import sys
import subprocess
import logging
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

import pyperclip
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Add parent directory to Python path for imports
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir.parent.parent.parent))
from tools.accessibility.lighthouse.get_active_url import get_active_browser_url

# Load environment variables
load_dotenv()

# Constants
REPORTS_DIR = Path(os.getenv('LIGHTHOUSE_REPORTS_DIR', str(Path.home() / "lighthouse_reports")))
LOGS_DIR = REPORTS_DIR / "logs"
console = Console()

# Set up logging
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / f"lighthouse_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(log_file)),
        logging.StreamHandler(sys.stderr)
    ]
)

def show_error(message: str):
    """Show error message in a modal dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Lighthouse Audit Error", message)
    root.destroy()

def find_node_paths() -> Tuple[Optional[Path], Optional[Path]]:
    """Find npm and lighthouse executables."""
    try:
        # Try using which command first
        npm_path = subprocess.check_output(['which', 'npm'], text=True).strip()
        lighthouse_path = subprocess.check_output(['which', 'lighthouse'], text=True).strip()
        return Path(npm_path), Path(lighthouse_path)
    except subprocess.CalledProcessError:
        # If which fails, try common locations
        common_paths = [
            Path('/usr/local/bin'),
            Path('/usr/bin'),
            Path('/opt/homebrew/bin'),
            Path.home() / '.npm-global/bin',
            Path.home() / '.nvm/current/bin'
        ]
        
        for path in common_paths:
            npm = path / 'npm'
            lighthouse = path / 'lighthouse'
            if npm.exists() and lighthouse.exists():
                return npm, lighthouse
        
        return None, None

def check_lighthouse_installation():
    """Check if lighthouse and npm are installed and accessible."""
    npm_path, lighthouse_path = find_node_paths()
    
    if not npm_path or not npm_path.exists():
        error_msg = (
            "npm not found!\n\n"
            "Please install Node.js and npm first:\n"
            "1. Visit https://nodejs.org\n"
            "2. Download and install Node.js\n"
            "3. Restart your computer\n"
            "4. Open Terminal and run: npm install -g lighthouse"
        )
        show_error(error_msg)
        return None, None

    if not lighthouse_path or not lighthouse_path.exists():
        error_msg = (
            "Lighthouse not installed!\n\n"
            "Please install it by:\n"
            "1. Opening Terminal\n"
            "2. Running: npm install -g lighthouse\n"
            "3. Waiting for installation to complete\n"
            "4. Trying this audit again"
        )
        show_error(error_msg)
        return None, None
    
    return npm_path, lighthouse_path

def validate_url(url: str) -> str:
    """Validate and format URL."""
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    return url

def get_url_from_clipboard() -> Optional[str]:
    """Get URL from clipboard if it looks like a valid URL."""
    try:
        clipboard_content = pyperclip.paste().strip()
        if any(clipboard_content.startswith(prefix) for prefix in ['http://', 'https://', 'www.']):
            return clipboard_content
    except Exception as e:
        logging.error(f"Error getting URL from clipboard: {str(e)}")
    return None

def run_lighthouse_audit(url: str) -> Optional[Path]:
    """Run Lighthouse audit using the Lighthouse CLI."""
    try:
        # Create reports directory if it doesn't exist
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate report filename based on URL and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        report_path = REPORTS_DIR / f"lighthouse_{domain}_{timestamp}.html"
        
        # Check lighthouse installation
        npm_path, lighthouse_path = check_lighthouse_installation()
        if not npm_path or not lighthouse_path:
            return None
        
        # Add the binary directory to PATH
        bin_dir = str(lighthouse_path.parent)
        os.environ['PATH'] = os.pathsep.join([bin_dir, os.environ.get('PATH', '')])
        
        # Lighthouse CLI command
        cmd = [
            str(lighthouse_path),
            url,
            '--quiet',  # Reduces output noise
            '--chrome-flags="--headless"',  # Run Chrome in headless mode
            '--output=html',  # Output format
            '--output-path', str(report_path),
            '--only-categories=accessibility,best-practices,performance,pwa,seo',  # Categories to audit
            '--view'  # Automatically open report in browser
        ]

        logging.info(f"Running Lighthouse audit for URL: {url}")
        
        # Run Lighthouse CLI
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            error_msg = (
                "Error running Lighthouse audit!\n\n"
                f"Details: {stderr}\n\n"
                "Please try:\n"
                "1. Checking your internet connection\n"
                "2. Making sure the URL is accessible\n"
                "3. Running 'npm install -g lighthouse' in Terminal to update Lighthouse"
            )
            show_error(error_msg)
            console.print(f"[red]{error_msg}[/red]")
            return None

        success_msg = f"Report generated and opened in browser:\n{report_path}"
        console.print(f"[green]{success_msg}[/green]")
        return report_path
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}\n\nPlease try running the audit again."
        show_error(error_msg)
        console.print(f"[red]{error_msg}[/red]")
        return None

def get_url() -> Optional[str]:
    """Get URL from command line, active browser window, or clipboard."""
    # First, check command line arguments
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    # Then try to get URL from active browser window
    url = get_active_browser_url()
    if url:
        return url
    
    # Finally, try clipboard
    return get_url_from_clipboard()

def main():
    """Main function to run the Lighthouse audit."""
    # Get URL from available sources
    url = get_url()
    if not url:
        error_msg = (
            "No URL found!\n\n"
            "Please either:\n"
            "1. Provide a URL as an argument\n"
            "2. Have an active browser window with a URL\n"
            "3. Copy a URL to your clipboard\n\n"
            "Try copying a URL to your clipboard and running this again."
        )
        show_error(error_msg)
        console.print(f"[red]Error: {error_msg}[/red]")
        sys.exit(1)
    
    # Validate URL
    url = validate_url(url)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Run audit
        progress.add_task(description=f"Running Lighthouse audit for {url}...", total=None)
        report_path = run_lighthouse_audit(url)
        
        if not report_path:
            sys.exit(1)

if __name__ == "__main__":
    main() 