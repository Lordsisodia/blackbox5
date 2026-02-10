#!/usr/bin/env python3
"""
YouTube Channel Collector for GitHub Actions

Collects videos from all configured channels and saves them in the
database/channels/ directory as JSON files.

Designed to run in GitHub Actions environment with:
- No persistent disk (ephemeral runner)
- Time limits (30 minutes)
- Automatic commit of new data
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import yt_dlp
except ImportError:
    print("ERROR: yt-dlp not installed")
    print("Run: pip install yt-dlp")
    sys.exit(1)


# Configuration
CHANNELS_CONFIG = Path(__file__).parent.parent / "config" / "channels.yaml"
DATABASE_DIR = Path(__file__).parent.parent / "database" / "channels"
MAX_VIDEOS_PER_CHANNEL = 50


def load_channels_config() -> Dict[str, Any]:
    """Load channel configuration from YAML file."""
    if not CHANNELS_CONFIG.exists():
        # Return default config if file doesn't exist
        return {
            "channels": [
                # Example channels - add more as needed
                {"name": "Fireship", "url": "https://www.youtube.com/@Fireship"},
                {"name": "AI Grid", "url": "https://www.youtube.com/@AI-Grid"},
                {"name": "Latent Space", "url": "https://www.youtube.com/@LatentSpace"},
            ]
        }

    import yaml
    with open(CHANNELS_CONFIG, 'r') as f:
        return yaml.safe_load(f)


def collect_channel_videos(channel_url: str, channel_name: str, max_videos: int = MAX_VIDEOS_PER_CHANNEL) -> List[Dict[str, Any]]:
    """
    Collect videos from a YouTube channel.

    Args:
        channel_url: Channel URL
        channel_name: Human-readable channel name
        max_videos: Maximum number of videos to collect

    Returns:
        List of video dictionaries
    """
    print(f"\n{'='*60}")
    print(f"Collecting from: {channel_name}")
    print(f"URL: {channel_url}")
    print(f"{'='*60}\n")

    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': 'in_playlist',  # Faster, doesn't download
        'playlistend': max_videos,
        'skip_download': True,
        'writeinfojson': False,
        'writedescription': False,
    }

    videos = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' not in info:
                print(f"Warning: No videos found for {channel_name}")
                return videos

            for entry in info['entries'][:max_videos]:
                if entry is None:
                    continue

                video = {
                    'id': entry.get('id', ''),
                    'title': entry.get('title', ''),
                    'upload_date': entry.get('upload_date', ''),
                    'duration': str(entry.get('duration', 0)),
                    'view_count': str(entry.get('view_count', 0)),
                    'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                    'collected_at': datetime.now().isoformat(),
                    'channel': channel_name,
                    'is_long_form': int(entry.get('duration', 0)) >= 600,  # 10+ minutes
                    'duration_bonus': 2.0 if int(entry.get('duration', 0)) >= 600 else 1.0
                }

                videos.append(video)
                print(f"  ✓ {video['title'][:60]}...")

            print(f"\nCollected {len(videos)} videos from {channel_name}")

    except Exception as e:
        print(f"ERROR: Failed to collect from {channel_name}: {e}")

    return videos


def save_channel_data(channel_name: str, videos: List[Dict[str, Any]]) -> None:
    """
    Save channel data to JSON file.

    Args:
        channel_name: Name of channel (used for filename)
        videos: List of video dictionaries
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_name = channel_name.lower().replace(' ', '_').replace('/', '_')
    filename = f"{safe_name}.json"
    filepath = DATABASE_DIR / filename

    # Load existing data if file exists
    existing_data = []
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                existing_data = json.load(f)

            # Merge existing and new videos
            existing_ids = {v['id'] for v in existing_data}
            new_videos = [v for v in videos if v['id'] not in existing_ids]

            if new_videos:
                print(f"  Found {len(new_videos)} new videos (total: {len(existing_data) + len(new_videos)})")
                videos = existing_data + videos
            else:
                print(f"  No new videos (total: {len(existing_data)})")
                return  # No changes, don't overwrite

        except Exception as e:
            print(f"  Warning: Failed to load existing data: {e}")
            videos = existing_data + videos

    # Sort by upload date (newest first)
    videos.sort(key=lambda x: x.get('upload_date', ''), reverse=True)

    # Save to file
    with open(filepath, 'w') as f:
        json.dump({'videos': videos}, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Saved {len(videos)} videos to {filename}")


def main():
    """Main collection function."""
    print("YouTube Channel Collector for GitHub Actions")
    print("="*60)
    print(f"Started at: {datetime.now().isoformat()}")
    print(f"Database dir: {DATABASE_DIR}")
    print("="*60)

    # Load channel configuration
    config = load_channels_config()
    channels = config.get('channels', [])

    if not channels:
        print("\nERROR: No channels configured")
        print(f"Create config file at: {CHANNELS_CONFIG}")
        print("Example:")
        print("""
channels:
  - name: "Fireship"
    url: "https://www.youtube.com/@Fireship"
  - name: "AI Grid"
    url: "https://www.youtube.com/@AI-Grid"
""")
        sys.exit(1)

    # Collect from all channels
    total_videos_collected = 0
    total_new_videos = 0

    for channel in channels:
        channel_name = channel.get('name', 'Unknown')
        channel_url = channel.get('url', '')

        if not channel_url:
            print(f"Warning: Skipping {channel_name} (no URL)")
            continue

        max_videos = channel.get('max_videos', MAX_VIDEOS_PER_CHANNEL)

        # Collect videos
        videos = collect_channel_videos(channel_url, channel_name, max_videos)
        total_videos_collected += len(videos)

        # Save to database
        save_channel_data(channel_name, videos)

    # Summary
    print("\n" + "="*60)
    print("COLLECTION COMPLETE")
    print("="*60)
    print(f"Channels processed: {len(channels)}")
    print(f"Total videos in database: {total_videos_collected}")
    print(f"Finished at: {datetime.now().isoformat()}")
    print("="*60)


if __name__ == '__main__':
    main()
