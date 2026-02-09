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
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def html_to_markdown(html: str, url: str) -> str:
    """Convert HTML content to markdown (basic implementation)"""
    import re

    # Remove script and style tags and their content
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Try to extract main content
    # Look for common content containers
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    if main_match:
        html = main_match.group(1)
    else:
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
        if article_match:
            html = article_match.group(1)

    # Convert common HTML elements to markdown
    # Headers
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL | re.IGNORECASE)

    # Code blocks
    html = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html, flags=re.DOTALL | re.IGNORECASE)

    # Links
    html = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL | re.IGNORECASE)

    # Bold/italic
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL | re.IGNORECASE)

    # Lists
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL | re.IGNORECASE)

    # Remove remaining HTML tags
    html = re.sub(r'<[^>]+>', '', html)

    # Decode HTML entities
    import html as html_module
    html = html_module.unescape(html)

    # Clean up whitespace
    lines = [line.strip() for line in html.split('\n') if line.strip()]
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
