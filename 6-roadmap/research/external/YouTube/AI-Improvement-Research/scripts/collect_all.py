#!/usr/bin/env python3
"""Scrape all channels from config/sources.yaml"""
import yaml
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "sources.yaml"

def load_channels():
    all_channels = []
    with open(CONFIG_PATH) as f:
        # YAML has multiple documents separated by ---
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict):
                if 'sources' in doc:
                    all_channels.extend([s for s in doc['sources'] if s.get('active', True)])
                if 'playlists' in doc:
                    all_channels.extend([p for p in doc['playlists'] if p.get('active', True)])
    return all_channels

def scrape_channel(source):
    slug = source['slug']
    url = source.get('url') or source.get('channel_id')
    if not url:
        print(f"Skipping {slug}: no URL")
        return
    name = source['name']

    print(f"Scraping: {name} ({slug})")
    result = subprocess.run([
        sys.executable, str(BASE_DIR / "scripts" / "collect_channel_optimized.py"),
        "--channel", url,
        "--name", name,
        "--slug", slug,
        "--batch-size", "25",
        "--workers", "5"
    ], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    channels = load_channels()
    print(f"Found {len(channels)} channels to scrape")
    print("=" * 60)

    for source in channels:
        scrape_channel(source)
        print()

    print("=" * 60)
    print("Done")
