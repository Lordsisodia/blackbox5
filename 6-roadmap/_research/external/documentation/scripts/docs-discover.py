#!/usr/bin/env python3
"""
Documentation Discovery Script
Discovers all routes from a documentation site's llms.txt or sitemap
"""

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def discover_from_llms_txt(base_url: str) -> dict:
    """Discover routes from llms.txt index file"""
    # Ensure base_url ends with / for proper urljoin
    if not base_url.endswith('/'):
        base_url += '/'
    llms_url = urljoin(base_url, "llms.txt")

    try:
        response = requests.get(llms_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {llms_url}: {e}")
        return None

    content = response.text
    routes = []

    # Parse markdown list format: - [Title](url): description
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- ['):
            # Extract markdown link: [Title](URL)
            match = re.search(r'- \[([^\]]+)\]\(([^)]+)\)(?::\s*(.+))?', line)
            if match:
                title = match.group(1)
                url = match.group(2)
                description = match.group(3) if match.group(3) else ""

                if url.startswith('http'):
                    parsed = urlparse(url)
                    path = parsed.path.replace('.md', '')
                    routes.append({
                        "path": path,
                        "title": title,
                        "description": description,
                        "url": url,
                        "type": "guide" if "guide" in description.lower() or "how" in title.lower() else "reference"
                    })

    return {
        "source": {
            "name": "",
            "base_url": base_url,
            "discovered_at": "",
            "discovered_via": "llms.txt"
        },
        "routes": routes,
        "metadata": {
            "total_routes": len(routes),
            "llms_txt": llms_url
        }
    }


def discover_from_sitemap(base_url: str) -> dict:
    """Discover routes from sitemap.xml"""
    sitemap_url = urljoin(base_url, "sitemap.xml")

    try:
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {sitemap_url}: {e}")
        return None

    # Simple regex extraction of URLs
    urls = re.findall(r'<loc>([^<]+)</loc>', response.text)

    routes = []
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path
        if path.endswith('.md'):
            path = path[:-3]
        routes.append({
            "path": path,
            "title": "",
            "url": url,
            "type": "unknown"
        })

    return {
        "source": {
            "name": "",
            "base_url": base_url,
            "discovered_at": "",
            "discovered_via": "sitemap.xml"
        },
        "routes": routes,
        "metadata": {
            "total_routes": len(routes),
            "sitemap_xml": sitemap_url
        }
    }


def organize_tiers(routes: list) -> dict:
    """Organize routes into priority tiers"""
    tier_1_keywords = ['overview', 'quickstart', 'getting-started', 'cli-reference',
                       'settings', 'configuration', 'permissions', 'mcp', 'common-workflows']
    tier_2_keywords = ['guide', 'tutorial', 'how-to', 'workflow', 'best-practices',
                       'sub-agents', 'skills', 'hooks', 'plugins', 'extensions',
                       'vscode', 'jetbrains', 'desktop', 'chrome', 'slack',
                       'github-actions', 'authentication', 'security', 'memory']

    tier_1 = []
    tier_2 = []
    tier_3 = []

    for route in routes:
        path_lower = route['path'].lower()

        if any(kw in path_lower for kw in tier_1_keywords):
            route['tier'] = 1
            tier_1.append(route)
        elif any(kw in path_lower for kw in tier_2_keywords):
            route['tier'] = 2
            tier_2.append(route)
        else:
            route['tier'] = 3
            tier_3.append(route)

    return {
        "tier_1": tier_1,
        "tier_2": tier_2,
        "tier_3": tier_3
    }


def main():
    parser = argparse.ArgumentParser(description='Discover documentation routes')
    parser.add_argument('--url', required=True, help='Base URL of documentation')
    parser.add_argument('--output', '-o', required=True, help='Output index.json path')
    parser.add_argument('--name', help='Source name (e.g., claude-code)')
    parser.add_argument('--method', choices=['llms.txt', 'sitemap', 'auto'],
                        default='auto', help='Discovery method')

    args = parser.parse_args()

    # Auto-detect method
    if args.method == 'auto':
        # Try llms.txt first
        result = discover_from_llms_txt(args.url)
        if result is None or result['metadata']['total_routes'] == 0:
            print("llms.txt not found or empty, trying sitemap.xml...")
            result = discover_from_sitemap(args.url)
    elif args.method == 'llms.txt':
        result = discover_from_llms_txt(args.url)
    else:
        result = discover_from_sitemap(args.url)

    if result is None:
        print("Error: Discovery failed")
        sys.exit(1)

    if result['metadata']['total_routes'] == 0:
        print("Warning: No routes discovered")
        sys.exit(1)

    # Add metadata
    from datetime import datetime
    result['source']['name'] = args.name or 'unknown'
    result['source']['discovered_at'] = datetime.now().isoformat()

    # Organize into tiers
    tiers = organize_tiers(result['routes'])
    result['routes'] = tiers

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Discovered {result['metadata']['total_routes']} routes:")
    print(f"  Tier 1 (critical): {len(tiers['tier_1'])}")
    print(f"  Tier 2 (important): {len(tiers['tier_2'])}")
    print(f"  Tier 3 (reference): {len(tiers['tier_3'])}")
    print(f"\nWritten to: {output_path}")


if __name__ == '__main__':
    main()
