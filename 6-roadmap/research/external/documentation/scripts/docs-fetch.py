#!/usr/bin/env python3
"""
Documentation Fetch Script
Fetches documentation pages and stores them as markdown
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required libraries missing.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


def html_to_markdown(html: str, url: str) -> str:
    """Convert HTML content to markdown"""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer"]):
        script.decompose()

    # Try to find main content area
    main_content = None

    # Common content selectors
    selectors = [
        'main',
        'article',
        '[role="main"]',
        '.content',
        '.documentation',
        '.docs-content',
        '#content',
        '.markdown-body'
    ]

    for selector in selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    if not main_content:
        main_content = soup.find('body') or soup

    # Extract text with basic formatting
    text = main_content.get_text(separator='\n', strip=True)

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n\n'.join(lines)

    return text


def fetch_page(url: str, delay: float = 0.5) -> tuple:
    """Fetch a single page and return content + metadata"""
    try:
        time.sleep(delay)  # Rate limiting
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')

        if 'text/html' in content_type:
            markdown = html_to_markdown(response.text, url)
        else:
            markdown = response.text

        return {
            'success': True,
            'content': markdown,
            'status_code': response.status_code,
            'content_type': content_type,
            'size_bytes': len(response.content)
        }

    except requests.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'status_code': getattr(e.response, 'status_code', None)
        }


def create_frontmatter(route: dict, fetch_result: dict, base_url: str) -> str:
    """Create YAML frontmatter for the markdown file"""
    from urllib.parse import urljoin

    full_url = urljoin(base_url, route['path'])

    frontmatter = {
        'fetch': {
            'url': full_url,
            'fetched_at': datetime.now().isoformat(),
            'status': fetch_result.get('status_code'),
            'content_type': fetch_result.get('content_type'),
            'size_bytes': fetch_result.get('size_bytes')
        },
        'metadata': {
            'title': route.get('title', ''),
            'section': route['path'].strip('/').split('/')[-1] if '/' in route['path'] else 'index',
            'tier': route.get('tier', 3),
            'type': route.get('type', 'unknown')
        }
    }

    # Convert to YAML string
    yaml_lines = ['---']
    yaml_lines.append(json.dumps(frontmatter, indent=2))
    yaml_lines.append('---')

    return '\n'.join(yaml_lines)


def sanitize_filename(path: str) -> str:
    """Convert path to safe filename"""
    # Remove leading/trailing slashes
    path = path.strip('/')
    # Replace slashes with dashes
    path = path.replace('/', '-')
    # Remove .md extension if present
    if path.endswith('.md'):
        path = path[:-3]
    return path + '.md'


def main():
    parser = argparse.ArgumentParser(description='Fetch documentation pages')
    parser.add_argument('--index', '-i', required=True,
                        help='Path to index.json from docs-discover')
    parser.add_argument('--output', '-o', required=True,
                        help='Output directory for fetched pages')
    parser.add_argument('--tier', type=int, choices=[1, 2, 3],
                        help='Only fetch specific tier')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Delay between requests (seconds)')
    parser.add_argument('--limit', type=int,
                        help='Limit number of pages to fetch')

    args = parser.parse_args()

    # Load index
    with open(args.index) as f:
        index = json.load(f)

    base_url = index['source']['base_url']
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect routes to fetch
    routes_to_fetch = []

    for tier_name in ['tier_1', 'tier_2', 'tier_3']:
        if args.tier and tier_name != f'tier_{args.tier}':
            continue

        for route in index['routes'].get(tier_name, []):
            routes_to_fetch.append(route)

    if args.limit:
        routes_to_fetch = routes_to_fetch[:args.limit]

    print(f"Fetching {len(routes_to_fetch)} pages...")
    print(f"Base URL: {base_url}")
    print(f"Output: {output_dir}")
    print()

    # Fetch pages
    success_count = 0
    fail_count = 0

    for i, route in enumerate(routes_to_fetch, 1):
        full_url = urljoin(base_url, route['path'])
        filename = sanitize_filename(route['path'])
        output_path = output_dir / filename

        print(f"[{i}/{len(routes_to_fetch)}] {route['path']} -> {filename}", end=' ')

        # Skip if already exists
        if output_path.exists():
            print("(exists, skipping)")
            success_count += 1
            continue

        # Fetch
        result = fetch_page(full_url, delay=args.delay)

        if result['success']:
            # Create markdown with frontmatter
            frontmatter = create_frontmatter(route, result, base_url)
            content = frontmatter + '\n\n' + result['content']

            # Write file
            with open(output_path, 'w') as f:
                f.write(content)

            print(f"✓ ({result['size_bytes']} bytes)")
            success_count += 1
        else:
            print(f"✗ Error: {result.get('error', 'Unknown')}")
            fail_count += 1

    print()
    print(f"Complete: {success_count} success, {fail_count} failed")

    # Update index with fetch status
    # (In a real implementation, we'd update the index.json)


if __name__ == '__main__':
    main()
