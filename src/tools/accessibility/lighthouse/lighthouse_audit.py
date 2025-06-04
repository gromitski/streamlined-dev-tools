#!/usr/bin/env python3
"""
Lighthouse Accessibility Audit Tool

This script runs a Lighthouse audit on a URL (either provided or from clipboard)
and opens the report in Chrome. Designed for Stream Deck integration.
"""

import os
import sys
import json
import tempfile
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

import pyperclip
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
LIGHTHOUSE_API_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
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

def run_lighthouse_audit(url: str) -> Dict[str, Any]:
    """Run Lighthouse audit using PageSpeed Insights API."""
    params = {
        'url': url,
        'strategy': 'desktop',
        'category': ['accessibility', 'best-practices', 'performance', 'pwa', 'seo'],
        'key': os.getenv('PAGESPEED_API_KEY')  # Optional: API key for higher quota
    }
    
    response = requests.get(LIGHTHOUSE_API_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()

def generate_html_report(audit_result: Dict[str, Any], url: str) -> Path:
    """Generate HTML report from audit results."""
    # Create reports directory if it doesn't exist
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate report filename based on URL and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]
    report_path = REPORTS_DIR / f"lighthouse_{domain}_{timestamp}.html"
    
    # Extract the report data
    categories = audit_result.get('lighthouseResult', {}).get('categories', {})
    
    # Create HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lighthouse Report - {url}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            .score {{ font-size: 1.2em; margin: 1em 0; }}
            .good {{ color: #0cce6b; }}
            .average {{ color: #ffa400; }}
            .poor {{ color: #ff4e42; }}
        </style>
    </head>
    <body>
        <h1>Lighthouse Report</h1>
        <p>URL: <a href="{url}">{url}</a></p>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <hr>
    """
    
    for category_id, category in categories.items():
        score = int(category.get('score', 0) * 100)
        score_class = 'good' if score >= 90 else 'average' if score >= 50 else 'poor'
        html_content += f"""
        <div class="score">
            <h2>{category.get('title')}</h2>
            <p class="{score_class}">Score: {score}/100</p>
        </div>
        """
    
    html_content += "</body></html>"
    
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    return report_path

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
            audit_result = run_lighthouse_audit(url)
            
            # Generate report
            progress.add_task(description="Generating report...", total=None)
            report_path = generate_html_report(audit_result, url)
            
            # Open report in default browser
            webbrowser.open(f'file://{report_path}')
            
            console.print(f"\n[green]Report generated and opened: {report_path}[/green]")
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error running Lighthouse audit: {str(e)}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 