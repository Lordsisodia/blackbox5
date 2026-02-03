#!/usr/bin/env python3
"""
Simple channel video collector - stores in database
Just gets video IDs and titles (fast), then metadata separately
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database"

def ensure_directories():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    (DATABASE_DIR / "channels").mkdir(exist_ok=True)

def get_all_video_ids(channel_url, max_videos=1000):
    """Get all video IDs from channel."""
    print(f"Getting video list from: {channel_url}")

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s",
        f"--playlist-items", f"1:{max_videos}",
        channel_url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return []

        ids = [line.strip() for line in result.stdout.strip().split("\n") if line.strip() and len(line.strip()) == 11]
        return ids
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_video_metadata(video_id):
    """Get metadata for a single video."""
    url = f"https://youtube.com/watch?v={video_id}"

    cmd = [
        "yt-dlp",
        "--print", "%(title)s",
        "--print", "%(upload_date)s",
        "--print", "%(duration)s",
        "--print", "%(view_count)s",
        "--skip-download",
        "--no-warnings",
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 4:
                return {
                    "title": lines[0].strip(),
                    "upload_date": lines[1].strip(),
                    "duration": lines[2].strip(),
                    "view_count": lines[3].strip() if lines[3].strip() else "0"
                }
    except:
        pass

    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--max", type=int, default=500)
    args = parser.parse_args()

    ensure_directories()

    print("="*60)
    print(f"COLLECTING: {args.name}")
    print("="*60)

    # Get all video IDs
    video_ids = get_all_video_ids(args.channel, args.max)
    print(f"Found {len(video_ids)} videos")

    if not video_ids:
        print("No videos found")
        return

    # Load existing database
    db_file = DATABASE_DIR / "channels" / f"{args.slug}.json"
    if db_file.exists():
        with open(db_file) as f:
            db = json.load(f)
    else:
        db = {"videos": []}

    existing_ids = {v["id"] for v in db["videos"]}

    # Get metadata for each video
    new_videos = []
    for i, video_id in enumerate(video_ids):
        if video_id in existing_ids:
            continue

        print(f"\n[{i+1}/{len(video_ids)}] Getting metadata for: {video_id}")
        metadata = get_video_metadata(video_id)

        if metadata:
            video = {
                "id": video_id,
                **metadata,
                "url": f"https://youtube.com/watch?v={video_id}",
                "collected_at": datetime.now().isoformat()
            }
            new_videos.append(video)
            print(f"  Title: {metadata['title'][:60]}...")
            print(f"  Date: {metadata['upload_date']}, Views: {metadata['view_count']}")

    # Merge and sort
    db["videos"].extend(new_videos)
    db["videos"].sort(key=lambda x: x.get("upload_date", ""), reverse=True)

    # Update metadata
    db["creator"] = args.name
    db["creator_slug"] = args.slug
    db["total_videos"] = len(db["videos"])
    db["last_updated"] = datetime.now().isoformat()

    # Save as JSON (more reliable than YAML for large datasets)
    with open(db_file, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"DATABASE SAVED: {db_file}")
    print(f"Total videos: {db['total_videos']}")
    print(f"New videos added: {len(new_videos)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
