#!/usr/bin/env python3
"""
Lighthouse Accessibility Audit Tool

This script runs a Lighthouse audit on a URL (either provided or from clipboard)
and opens the report in Chrome. Designed for Stream Deck integration.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

import pyperclip
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Constants
REPORTS_DIR = Path.home() / "lighthouse_reports"
console = Console()

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
    except Exception:
        return None
    return None

def run_lighthouse_audit(url: str) -> Path:
    """Run Lighthouse audit using the Lighthouse CLI."""
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
    
    try:
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
            raise Exception(f"Lighthouse audit failed: {stderr}")
        
        return report_path
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running Lighthouse: {str(e)}") from e
    except Exception as e:
        raise Exception(f"Unexpected error running Lighthouse: {str(e)}") from e

def main():
    """Main function to run the Lighthouse audit."""
    try:
        # Check for URL argument or get from clipboard
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = get_url_from_clipboard()
            if not url:
                console.print("[red]Error: No URL provided and no valid URL found in clipboard[/red]")
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
            
            console.print(f"\n[green]Report generated and opened in browser: {report_path}[/green]")
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 