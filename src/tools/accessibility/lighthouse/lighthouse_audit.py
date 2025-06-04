#!/usr/bin/env python3
"""
Lighthouse Accessibility Audit Tool

This script runs a Lighthouse audit on a URL (either provided or from clipboard)
and opens the report in Chrome. Designed for Stream Deck integration.
"""

import os
import sys
import time
import argparse
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

import pyperclip
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from .get_active_url import get_active_browser_url

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
    filename=str(log_file),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

def run_lighthouse_audit(url: str, debug: bool = False) -> Tuple[bool, Path]:
    """Run Lighthouse audit using the Lighthouse CLI."""
    logging.info(f"Starting Lighthouse audit for URL: {url}")
    
    try:
        # Create reports directory if it doesn't exist
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate report filename based on URL and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        report_path = REPORTS_DIR / f"lighthouse_{domain}_{timestamp}.html"
        
        # Lighthouse CLI command
        cmd = [
            'lighthouse',
            url,
            '--quiet',  # Reduces output noise
            '--chrome-flags="--headless"',  # Run Chrome in headless mode
            '--output=html',  # Output format
            '--output-path', str(report_path),
            '--only-categories=accessibility,best-practices,performance,pwa,seo',  # Categories to audit
            '--view'  # Automatically open report in browser
        ]

        if debug:
            console.print(f"[yellow]Running command:[/yellow] {' '.join(cmd)}")
        logging.info(f"Running command: {' '.join(cmd)}")
        
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
            error_msg = f"Lighthouse audit failed: {stderr}"
            logging.error(error_msg)
            return False, report_path

        if stdout:
            logging.info("Command output: " + stdout.replace('\n', ' '))
        
        logging.info(f"Report generated successfully at: {report_path}")
        return True, report_path
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Error running Lighthouse: {str(e)}"
        logging.error(error_msg)
        return False, report_path
    except Exception as e:
        error_msg = f"Unexpected error running Lighthouse: {str(e)}"
        logging.error(error_msg)
        return False, report_path

def get_url() -> Optional[str]:
    """Get URL from command line, active browser window, or clipboard."""
    logging.info("Attempting to get URL...")
    
    # First, check command line arguments
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        url = sys.argv[1]
        logging.info(f"URL found in command line arguments: {url}")
        return url
    
    # Then try to get URL from active browser window
    logging.info("Trying to get URL from active browser window...")
    url = get_active_browser_url()
    if url:
        logging.info(f"URL found in active browser window: {url}")
        return url
    
    # Finally, try clipboard
    logging.info("Trying to get URL from clipboard...")
    url = get_url_from_clipboard()
    if url:
        logging.info(f"URL found in clipboard: {url}")
        return url
    
    logging.error("No URL found from any source")
    return None

def main():
    """Main function to run the Lighthouse audit."""
    try:
        parser = argparse.ArgumentParser(description='Run Lighthouse accessibility audit.')
        parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode with terminal output')
        parser.add_argument('url', nargs='?', help='URL to audit (optional)')
        args = parser.parse_args()

        if args.debug:
            console.print("[yellow]Debug mode enabled[/yellow]")
            console.print("[yellow]Checking for URL...[/yellow]")

        # Get URL from available sources
        url = args.url or get_url()
        if not url:
            error_msg = "No URL provided, no active browser window found, and no valid URL in clipboard"
            console.print(f"[red]Error: {error_msg}[/red]")
            logging.error(error_msg)
            if args.debug:
                console.print("[yellow]Press Enter to exit...[/yellow]")
                input()
            print("fail")  # Stream Deck status
            sys.exit(1)
        
        # Validate URL
        url = validate_url(url)
        if args.debug:
            console.print(f"[green]Found URL:[/green] {url}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Run audit
            progress.add_task(description=f"Running Lighthouse audit for {url}...", total=None)
            success, report_path = run_lighthouse_audit(url, args.debug)
            
            if success:
                console.print(f"\n[green]Report generated and opened in browser: {report_path}[/green]")
                logging.info("Audit completed successfully")
                print("success")  # Stream Deck status
            else:
                error_msg = f"Audit failed. Check the log file for details: {log_file}"
                console.print(f"\n[red]{error_msg}[/red]")
                logging.error("Audit failed")
                print("fail")  # Stream Deck status

        if args.debug:
            console.print("[yellow]Press Enter to exit...[/yellow]")
            input()
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        console.print(f"[red]Error: {error_msg}[/red]")
        logging.error(error_msg)
        if args.debug:
            console.print("[yellow]Press Enter to exit...[/yellow]")
            input()
        print("fail")  # Stream Deck status
        sys.exit(1)

if __name__ == "__main__":
    main() 