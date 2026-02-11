#!/usr/bin/env python3
"""
Fetch Shopify Polaris Web Components documentation
"""

import json
import time
import re
import html
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import sys

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def html_to_markdown(html: str, url: str) -> str:
    """Convert HTML content to markdown"""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<svg[^>]*>.*?</svg>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Extract main content - Shopify docs have specific structure
    # Try multiple selectors
    content = ""

    # Look for main article/content area
    article_match = re.search(r'<article[^>]*class="[^"]*DocsContent[^"]*"[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    if article_match:
        content = article_match.group(1)
    else:
        # Try main content area
        main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
        if main_match:
            content = main_match.group(1)
        else:
            # Try docs container
            docs_match = re.search(r'<div[^>]*class="[^"]*docs[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL | re.IGNORECASE)
            if docs_match:
                content = docs_match.group(1)
            else:
                content = html

    # Convert headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content, flags=re.DOTALL | re.IGNORECASE)

    # Convert code blocks
    content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL | re.IGNORECASE)

    # Convert links
    content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL | re.IGNORECASE)

    # Convert bold/italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL | re.IGNORECASE)

    # Convert lists
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', content, flags=re.DOTALL | re.IGNORECASE)

    # Convert tables
    content = re.sub(r'<th[^>]*>(.*?)</th>', r'| \1 ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<td[^>]*>(.*?)</td>', r'| \1 ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<tr[^>]*>(.*?)</tr>', r'\1|', content, flags=re.DOTALL | re.IGNORECASE)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Decode HTML entities
    import html as html_module
    content = html_module.unescape(content)

    # Clean up whitespace
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    content = '\n\n'.join(lines)

    return content


def extract_title(html: str, url: str) -> str:
    """Extract page title from HTML"""
    # Try title tag
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove site suffix
        title = re.sub(r'\s*[-|]\s*Shopify.*$', '', title, flags=re.IGNORECASE)
        return title

    # Try h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    if h1_match:
        return h1_match.group(1).strip()

    # Fallback to URL path
    parsed = urlparse(url)
    path = parsed.path.strip('/').split('/')[-1]
    return path.replace('-', ' ').title()


def fetch_page(url: str, delay: float = 1.0) -> dict:
    """Fetch a single page and return content + metadata"""
    try:
        time.sleep(delay)  # Rate limiting

        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; DocumentationResearch/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        title = extract_title(response.text, url)
        markdown = html_to_markdown(response.text, url)

        return {
            'success': True,
            'title': title,
            'content': markdown,
            'status_code': response.status_code,
            'size_bytes': len(response.content)
        }

    except requests.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'status_code': getattr(e.response, 'status_code', None)
        }


def create_frontmatter(url: str, title: str, fetch_result: dict) -> str:
    """Create YAML frontmatter for the markdown file"""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')

    frontmatter = {
        'fetch': {
            'url': url,
            'fetched_at': datetime.now().isoformat(),
            'status': fetch_result.get('status_code'),
            'size_bytes': fetch_result.get('size_bytes')
        },
        'metadata': {
            'title': title,
            'source': 'shopify',
            'category': 'polaris-web-components',
            'section': path_parts[-2] if len(path_parts) > 1 else 'general',
            'component': path_parts[-1] if path_parts else 'index'
        }
    }

    yaml_lines = ['---']
    yaml_lines.append(json.dumps(frontmatter, indent=2))
    yaml_lines.append('---')

    return '\n'.join(yaml_lines)


def sanitize_filename(url: str) -> str:
    """Convert URL to safe filename"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    # Replace slashes with dashes
    filename = path.replace('/', '-')
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9\-_]', '', filename)
    return filename + '.md'


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Fetch Shopify Polaris Web Components docs')
    parser.add_argument('--urls-file', '-f', required=True, help='File with URLs to fetch (one per line)')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--limit', type=int, help='Limit number of pages to fetch')

    args = parser.parse_args()

    # Load URLs
    with open(args.urls_file) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if args.limit:
        urls = urls[:args.limit]

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {len(urls)} pages...")
    print(f"Output: {output_dir}")
    print()

    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        filename = sanitize_filename(url)
        output_path = output_dir / filename

        print(f"[{i}/{len(urls)}] {url} -> {filename}", end=' ')

        # Skip if already exists
        if output_path.exists():
            print("(exists, skipping)")
            success_count += 1
            continue

        # Fetch
        result = fetch_page(url, delay=args.delay)

        if result['success']:
            # Create markdown with frontmatter
            frontmatter = create_frontmatter(url, result['title'], result)
            content = frontmatter + '\n\n# ' + result['title'] + '\n\n' + result['content']

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


if __name__ == '__main__':
    main()
