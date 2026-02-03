#!/usr/bin/env python3
"""
Collect ALL video metadata from a channel (no rate limits)
Stores in database for training data purposes
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

def ensure_directories():
    """Create database directory."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    (DATABASE_DIR / "channels").mkdir(exist_ok=True)

def get_channel_videos(channel_url: str, max_videos: int = 1000) -> List[Dict]:
    """Get all video metadata from channel using yt-dlp."""
    print(f"Fetching videos from: {channel_url}")
    print(f"This may take a while for channels with many videos...")

    # First, get video IDs and titles (fast)
    cmd_basic = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s",
        "--print", "%(title)s",
        f"--playlist-items", f"1:{max_videos}",
        channel_url
    ]

    try:
        result = subprocess.run(cmd_basic, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error getting basic info: {result.stderr}")
            return []

        lines = result.stdout.strip().split("\n")
        videos = []

        # Parse output (alternating: id, title, id, title...)
        for i in range(0, len(lines) - 1, 2):
            if i + 1 < len(lines):
                video_id = lines[i].strip()
                title = lines[i + 1].strip()

                # Skip empty or invalid entries
                if not video_id or not title or len(video_id) != 11:
                    continue

                video = {
                    "id": video_id,
                    "title": title,
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "collected_at": datetime.now().isoformat()
                }
                videos.append(video)

        print(f"Found {len(videos)} videos, getting detailed metadata...")

        # Now get detailed metadata for each video
        for i, video in enumerate(videos):
            try:
                cmd_detail = [
                    "yt-dlp",
                    "--print", "%(upload_date)s",
                    "--print", "%(duration)s",
                    "--print", "%(view_count)s",
                    f"https://youtube.com/watch?v={video['id']}"
                ]
                result = subprocess.run(cmd_detail, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    detail_lines = result.stdout.strip().split("\n")
                    if len(detail_lines) >= 3:
                        video["upload_date"] = detail_lines[0].strip()
                        video["duration"] = detail_lines[1].strip()
                        video["view_count"] = detail_lines[2].strip()

                if (i + 1) % 50 == 0:
                    print(f"  Processed {i + 1}/{len(videos)} videos...")
            except Exception as e:
                print(f"  Warning: Could not get details for {video['id']}: {e}")
                continue

        return videos
    except subprocess.TimeoutExpired:
        print("Timeout - channel has too many videos")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def save_channel_database(creator_slug: str, creator_name: str, videos: List[Dict]):
    """Save videos to channel database file."""
    db_file = DATABASE_DIR / "channels" / f"{creator_slug}.yaml"

    # Load existing if present
    if db_file.exists():
        with open(db_file) as f:
            existing = yaml.safe_load(f) or {"videos": []}
    else:
        existing = {"videos": []}

    # Create ID lookup for deduplication
    existing_ids = {v["id"] for v in existing["videos"]}

    # Add new videos (skip duplicates)
    new_count = 0
    for video in videos:
        if video["id"] not in existing_ids:
            existing["videos"].append(video)
            new_count += 1

    # Sort by upload date (newest first)
    existing["videos"].sort(key=lambda x: x.get("upload_date", ""), reverse=True)

    # Update metadata
    existing["creator"] = creator_name
    existing["creator_slug"] = creator_slug
    existing["total_videos"] = len(existing["videos"])
    existing["last_updated"] = datetime.now().isoformat()
    existing["database_version"] = "1.0"

    # Save
    with open(db_file, "w") as f:
        yaml.dump(existing, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nDatabase saved: {db_file}")
    print(f"Total videos: {existing['total_videos']}")
    print(f"New videos added: {new_count}")

    return db_file

def main():
    parser = argparse.ArgumentParser(description="Collect all video metadata from a channel")
    parser.add_argument("--channel", required=True, help="Channel URL (e.g., https://www.youtube.com/@DavidOndrej)")
    parser.add_argument("--name", required=True, help="Creator name")
    parser.add_argument("--slug", required=True, help="Creator slug (e.g., david_ondrej)")
    parser.add_argument("--max", type=int, default=1000, help="Maximum videos to fetch")

    args = parser.parse_args()

    ensure_directories()

    print("="*60)
    print(f"COLLECTING ALL VIDEOS FROM: {args.name}")
    print("="*60)

    # Get videos
    videos = get_channel_videos(args.channel, args.max)

    if not videos:
        print("No videos found")
        return

    print(f"\nFound {len(videos)} videos")

    # Save to database
    db_file = save_channel_database(args.slug, args.name, videos)

    # Show sample
    print("\n" + "="*60)
    print("MOST RECENT VIDEOS:")
    print("="*60)
    for video in videos[:5]:
        print(f"\n{video['upload_date']}: {video['title'][:60]}...")
        print(f"  Views: {video['view_count']}, Duration: {video['duration']}s")
        print(f"  URL: {video['url']}")

if __name__ == "__main__":
    main()
