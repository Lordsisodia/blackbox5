#!/usr/bin/env python3
"""
HIGH-PERFORMANCE channel video collector
Uses batch processing and parallelization for 10x speed
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database"

def ensure_directories():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    (DATABASE_DIR / "channels").mkdir(exist_ok=True)

def get_all_video_ids(channel_url: str, max_videos: int = 5000) -> List[str]:
    """Get all video IDs from channel - FAST."""
    print(f"Getting video list from: {channel_url}")

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s",
        f"--playlist-items", f"1:{max_videos}",
        "--ignore-errors",
        "--no-check-certificate",
        channel_url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        ids = [line.strip() for line in result.stdout.strip().split("\n")
               if line.strip() and len(line.strip()) == 11]
        return ids
    except Exception as e:
        print(f"Error getting video list: {e}")
        return []

def get_video_metadata_batch(video_ids: List[str]) -> List[Optional[Dict]]:
    """Get metadata for multiple videos in ONE yt-dlp call."""
    if not video_ids:
        return []

    # Build URLs
    urls = [f"https://youtube.com/watch?v={vid}" for vid in video_ids]

    cmd = [
        "yt-dlp",
        "--print", "%(id)s",
        "--print", "%(title)s",
        "--print", "%(upload_date)s",
        "--print", "%(duration)s",
        "--print", "%(view_count)s",
        "--skip-download",
        "--no-warnings",
        "--ignore-errors",
        "--no-check-certificate",
        "--quiet"
    ] + urls

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        lines = result.stdout.strip().split("\n")

        videos = []
        # Parse output: id, title, date, duration, views (repeating)
        for i in range(0, len(lines) - 4, 5):
            if i + 4 < len(lines):
                video_id = lines[i].strip()
                if len(video_id) == 11:  # Valid video ID
                    videos.append({
                        "id": video_id,
                        "title": lines[i + 1].strip(),
                        "upload_date": lines[i + 2].strip(),
                        "duration": lines[i + 3].strip(),
                        "view_count": lines[i + 4].strip() if lines[i + 4].strip() else "0"
                    })
        return videos
    except Exception as e:
        print(f"Error in batch fetch: {e}")
        return []

def get_metadata_parallel(video_ids: List[str], max_workers: int = 5, batch_size: int = 50) -> List[Dict]:
    """Fetch metadata in parallel batches."""
    # Split into batches
    batches = [video_ids[i:i + batch_size] for i in range(0, len(video_ids), batch_size)]

    all_videos = []
    completed = 0

    print(f"Fetching metadata for {len(video_ids)} videos in {len(batches)} batches (batch_size={batch_size}, workers={max_workers})")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all batches
        future_to_batch = {executor.submit(get_video_metadata_batch, batch): batch for batch in batches}

        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                videos = future.result()
                all_videos.extend(videos)
                completed += len(batch)
                print(f"  Progress: {completed}/{len(video_ids)} videos processed ({len(all_videos)} successful)")
            except Exception as e:
                print(f"  Batch failed: {e}")

    return all_videos

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--max", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=50, help="Videos per batch")
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers")
    args = parser.parse_args()

    ensure_directories()

    print("="*70)
    print(f"FAST COLLECTION: {args.name}")
    print(f"Batch size: {args.batch_size}, Workers: {args.workers}")
    print("="*70)

    start_time = datetime.now()

    # Get all video IDs
    video_ids = get_all_video_ids(args.channel, args.max)
    print(f"Found {len(video_ids)} videos in {(datetime.now() - start_time).seconds}s")

    if not video_ids:
        print("No videos found")
        return

    # Load existing database
    db_file = DATABASE_DIR / "channels" / f"{args.slug}.json"
    if db_file.exists():
        with open(db_file) as f:
            db = json.load(f)
        existing_ids = {v["id"] for v in db.get("videos", [])}
        print(f"Loaded existing database: {len(existing_ids)} videos")
    else:
        db = {"videos": []}
        existing_ids = set()
        print("No existing database found, starting fresh")

    # Find missing videos
    missing_ids = [vid for vid in video_ids if vid not in existing_ids]
    print(f"Missing videos to collect: {len(missing_ids)}")

    if not missing_ids:
        print("\n✓ No missing videos - database is complete!")
        return

    # Fetch metadata in parallel batches
    fetch_start = datetime.now()
    new_videos = get_metadata_parallel(
        missing_ids,
        max_workers=args.workers,
        batch_size=args.batch_size
    )
    fetch_time = (datetime.now() - fetch_start).seconds

    # Add metadata
    for video in new_videos:
        video["url"] = f"https://youtube.com/watch?v={video['id']}"
        video["collected_at"] = datetime.now().isoformat()

    # Merge and sort
    db["videos"].extend(new_videos)
    db["videos"].sort(key=lambda x: x.get("upload_date", ""), reverse=True)

    # Update metadata
    db["creator"] = args.name
    db["creator_slug"] = args.slug
    db["total_videos"] = len(db["videos"])
    db["last_updated"] = datetime.now().isoformat()

    # Save
    with open(db_file, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    total_time = (datetime.now() - start_time).seconds

    print(f"\n{'='*70}")
    print(f"DATABASE UPDATED: {db_file}")
    print(f"Previous count: {len(existing_ids)}")
    print(f"New videos added: {len(new_videos)}")
    print(f"Total videos: {db['total_videos']}")
    print(f"\nTiming:")
    print(f"  List fetch: {(datetime.now() - start_time).seconds - fetch_time}s")
    print(f"  Metadata fetch: {fetch_time}s")
    print(f"  Total time: {total_time}s")
    print(f"  Speed: {len(new_videos)/max(fetch_time, 1):.1f} videos/sec")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
