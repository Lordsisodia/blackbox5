#!/usr/bin/env python3
"""
OPTIMIZED channel video collector
- Caches all results (never re-fetches)
- Batch processing (25 videos per call)
- Parallel workers (5 concurrent batches)
- Resume capability
- Smart error handling
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import time

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database"
CACHE_DIR = DATABASE_DIR / ".cache"

def ensure_directories():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    (DATABASE_DIR / "channels").mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

def get_cache_file(slug: str) -> Path:
    """Get cache file path for a channel."""
    return CACHE_DIR / f"{slug}_metadata_cache.json"

def load_cache(slug: str) -> Dict[str, Dict]:
    """Load cached metadata."""
    cache_file = get_cache_file(slug)
    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)
    return {}

def save_cache(slug: str, cache: Dict[str, Dict]):
    """Save metadata cache."""
    cache_file = get_cache_file(slug)
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def get_all_video_ids(channel_url: str, max_videos: int = 5000) -> List[str]:
    """Get all video IDs from channel."""
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

def get_video_metadata_batch(video_ids: List[str]) -> List[Dict]:
    """Get metadata for multiple videos in ONE yt-dlp call."""
    if not video_ids:
        return []

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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        lines = result.stdout.strip().split("\n")

        videos = []
        for i in range(0, len(lines) - 4, 5):
            if i + 4 < len(lines):
                video_id = lines[i].strip()
                if len(video_id) == 11:
                    videos.append({
                        "id": video_id,
                        "title": lines[i + 1].strip(),
                        "upload_date": lines[i + 2].strip(),
                        "duration": lines[i + 3].strip(),
                        "view_count": lines[i + 4].strip() if lines[i + 4].strip() else "0"
                    })
        return videos
    except subprocess.TimeoutExpired:
        print(f"    ⚠ Batch timeout (size: {len(video_ids)})")
        return []
    except Exception as e:
        print(f"    ⚠ Batch error: {e}")
        return []

def process_batch_with_retry(video_ids: List[str], cache: Dict, max_retries: int = 2) -> List[Dict]:
    """Process a batch with retry logic for failed videos."""
    results = []
    failed_ids = []

    # Try batch fetch
    videos = get_video_metadata_batch(video_ids)
    found_ids = {v["id"] for v in videos}

    for vid in video_ids:
        if vid in found_ids:
            video_data = next(v for v in videos if v["id"] == vid)
            results.append(video_data)
            cache[vid] = video_data  # Update cache
        else:
            failed_ids.append(vid)

    # Retry failed individually (some might be private/deleted)
    if failed_ids and max_retries > 0:
        for vid in failed_ids:
            time.sleep(0.5)  # Brief pause between retries
            single = get_video_metadata_batch([vid])
            if single:
                results.append(single[0])
                cache[vid] = single[0]

    return results

def fetch_metadata_parallel(
    video_ids: List[str],
    cache: Dict[str, Dict],
    slug: str,
    max_workers: int = 5,
    batch_size: int = 25
) -> List[Dict]:
    """Fetch metadata with parallel batches and caching."""

    # Filter out already cached videos
    uncached_ids = [vid for vid in video_ids if vid not in cache]
    cached_count = len(video_ids) - len(uncached_ids)

    if cached_count > 0:
        print(f"  Using cache for {cached_count} videos")

    if not uncached_ids:
        print("  All videos in cache!")
        return [cache[vid] for vid in video_ids if vid in cache]

    # Split into batches
    batches = [uncached_ids[i:i + batch_size] for i in range(0, len(uncached_ids), batch_size)]

    all_videos = []
    completed = 0
    failed_batches = 0

    print(f"Fetching {len(uncached_ids)} videos in {len(batches)} batches (size={batch_size}, workers={max_workers})")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {
            executor.submit(process_batch_with_retry, batch, cache): batch
            for batch in batches
        }

        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                videos = future.result()
                all_videos.extend(videos)
                completed += len(batch)

                # Save cache periodically
                if completed % 100 == 0:
                    save_cache(slug, cache)
                    print(f"  Progress: {completed}/{len(uncached_ids)} - Cache saved")

            except Exception as e:
                failed_batches += 1
                print(f"  ⚠ Batch failed: {e}")

    # Final cache save
    save_cache(slug, cache)

    # Combine cached + new results
    final_results = []
    for vid in video_ids:
        if vid in cache:
            final_results.append(cache[vid])

    print(f"  Fetched {len(all_videos)} new, {len(final_results)} total")
    if failed_batches > 0:
        print(f"  ⚠ {failed_batches} batches had issues")

    return final_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--max", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()

    ensure_directories()

    print("="*70)
    print(f"OPTIMIZED COLLECTION: {args.name}")
    print(f"Batch size: {args.batch_size}, Workers: {args.workers}")
    print("="*70)

    start_time = datetime.now()

    # Load cache
    cache = load_cache(args.slug)
    print(f"Loaded cache: {len(cache)} videos cached")

    # Get all video IDs
    video_ids = get_all_video_ids(args.channel, args.max)
    print(f"Found {len(video_ids)} videos on channel ({(datetime.now() - start_time).seconds}s)")

    if not video_ids:
        print("No videos found")
        return

    # Load existing database
    db_file = DATABASE_DIR / "channels" / f"{args.slug}.json"
    if db_file.exists():
        with open(db_file) as f:
            db = json.load(f)
        existing_ids = {v["id"] for v in db.get("videos", [])}
        print(f"Database has {len(existing_ids)} videos")
    else:
        db = {"videos": []}
        existing_ids = set()

    # Find missing videos
    missing_ids = [vid for vid in video_ids if vid not in existing_ids]
    print(f"Missing from database: {len(missing_ids)}")

    if not missing_ids:
        print("\n✓ Database is complete!")
        return

    # Fetch metadata (with caching)
    fetch_start = datetime.now()
    new_videos = fetch_metadata_parallel(
        missing_ids,
        cache,
        args.slug,
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
    print(f"  List fetch: {total_time - fetch_time}s")
    print(f"  Metadata fetch: {fetch_time}s")
    print(f"  Total time: {total_time}s")
    print(f"  Speed: {len(new_videos)/max(fetch_time, 1):.1f} videos/sec")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
