#!/usr/bin/env python3
"""Add new channel to config. Usage: python add_channel.py --handle @NewCreator --name "Name" --tier 2"""
import argparse
import yaml
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path("config/sources.yaml")

def add_channel(handle, name, tier=2, areas=None, topics=None):
    # Validate handle format
    if not handle.startswith('@'):
        handle = '@' + handle

    # Create slug from handle
    slug = handle.replace('@', '').lower().replace('-', '_')

    # Load existing config
    docs = []
    with open(CONFIG_PATH) as f:
        docs = list(yaml.safe_load_all(f))

    # Check if already exists
    for doc in docs:
        if doc and isinstance(doc, dict):
            for source in doc.get('sources', []):
                if source.get('slug') == slug:
                    print(f"Channel {slug} already exists")
                    return False

    # Find the sources document (usually the 4th doc)
    sources_doc = None
    for doc in docs:
        if doc and isinstance(doc, dict) and 'sources' in doc:
            sources_doc = doc
            break

    if not sources_doc:
        print("Could not find sources section in config")
        return False

    # Add new source
    new_source = {
        'name': name,
        'slug': slug,
        'handle': handle,
        'url': f"https://www.youtube.com/{handle}",
        'tier': tier,
        'areas': areas or ['ai-engineering'],
        'topics': topics or [],
        'active': True
    }

    sources_doc['sources'].append(new_source)

    # Update metadata
    for doc in docs:
        if doc and isinstance(doc, dict) and 'metadata' in doc:
            doc['metadata']['total_sources'] = len(sources_doc['sources'])
            doc['metadata']['last_updated'] = subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()
            break

    # Save
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump_all(docs, f, default_flow_style=False, sort_keys=False)

    print(f"Added {name} ({slug})")

    # Git commit
    subprocess.run(['git', 'add', str(CONFIG_PATH)])
    subprocess.run(['git', 'commit', '-m', f'Add channel: {name} ({slug})'])
    print("Committed to git")

    # Try to push
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Pushed to GitHub. Will be scraped in next hourly run.")
    else:
        print("Could not push (no remote?). Commit is local.")

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add new YouTube channel to scraper')
    parser.add_argument('--handle', required=True, help='@ChannelHandle')
    parser.add_argument('--name', required=True, help='Display name')
    parser.add_argument('--tier', type=int, default=2, choices=[1, 2, 3])
    args = parser.parse_args()

    success = add_channel(args.handle, args.name, args.tier)
    sys.exit(0 if success else 1)
