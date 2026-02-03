#!/usr/bin/env python3
"""
AI Improvement Research - Stage 1: Metadata Collection
Collects video metadata WITHOUT transcripts (fast, no rate limits)

This is the first step in the 3-stage pipeline:
1. collect_metadata.py - Get title, description, views, etc. (fast)
2. rank_v2.py - Score videos based on metadata (free)
3. download_transcripts.py - Only get transcripts for valuable videos (slow)
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml
import feedparser

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
TIMELINE_DIR = BASE_DIR / "timeline"
QUEUE_DIR = BASE_DIR / "queue"

# Ensure directories exist
(DATA_DIR / "sources").mkdir(parents=True, exist_ok=True)
(TIMELINE_DIR / "events").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "pending").mkdir(parents=True, exist_ok=True)


def load_sources():
    """Load source configuration from sources.yaml."""
    sources_file = CONFIG_DIR / "sources.yaml"
    all_sources = []
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "sources" in doc:
                for source in doc.get("sources", []):
                    source["source_type"] = "channel"
                    all_sources.append(source)
            if doc and "playlists" in doc:
                for playlist in doc.get("playlists", []):
                    playlist["source_type"] = "playlist"
                    all_sources.append(playlist)
    return all_sources


def log_event(event_type, data):
    """Log an event to the timeline."""
    today = datetime.now().strftime("%Y-%m-%d")
    events_file = TIMELINE_DIR / "events" / f"{today}.yaml"

    if events_file.exists():
        with open(events_file) as f:
            events_data = yaml.safe_load(f) or {}
    else:
        events_data = {"date": today, "events": []}

    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        **data
    }
    events_data["events"].append(event)

    with open(events_file, "w") as f:
        yaml.dump(events_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_channel_id_from_handle(handle):
    """Extract channel ID from YouTube handle using yt-dlp."""
    url = f"https://www.youtube.com/{handle}"
    cmd = ["yt-dlp", "--print", "channel_id", "--playlist-items", "1", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_video_metadata(video_id):
    """Get video metadata using yt-dlp (fast, no transcript)."""
    url = f"https://youtube.com/watch?v={video_id}"
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None

    data = json.loads(result.stdout)
    return {
        "id": data["id"],
        "title": data["title"],
        "description": data.get("description", ""),
        "channel": data["channel"],
        "channel_id": data["channel_id"],
        "published_at": data.get("upload_date", ""),
        "duration": data["duration"],
        "view_count": data.get("view_count", 0),
        "like_count": data.get("like_count", 0),
        "url": f"https://youtube.com/watch?v={data['id']}",
        "thumbnail": data.get("thumbnail", ""),
    }


def check_rss_feed(channel_id, last_check=None):
    """Check RSS feed for new videos."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    try:
        feed = feedparser.parse(rss_url)
        videos = []

        for entry in feed.entries:
            published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z")

            # Skip if before last check
            if last_check and published <= last_check:
                continue

            # Extract video ID from URL
            if "/shorts/" in entry.link:
                video_id = entry.link.split("/shorts/")[-1].split("?")[0]
            else:
                video_id = entry.link.split("v=")[-1].split("&")[0]

            videos.append({
                "id": video_id,
                "title": entry.title,
                "published_at": entry.published,
                "url": entry.link,
            })

        return videos
    except Exception as e:
        print(f"Error checking RSS: {e}")
        return []


def get_playlist_videos(playlist_url):
    """Extract all video IDs from a YouTube playlist using yt-dlp."""
    print(f"   Extracting playlist videos...")
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s",
        "--print", "%(title)s",
        "--print", "%(duration)s",
        playlist_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ Failed to extract playlist: {result.stderr}")
        return []

    lines = result.stdout.strip().split("\n")
    videos = []

    # Parse output (id, title, duration in groups of 3)
    for i in range(0, len(lines) - 2, 3):
        video_id = lines[i].strip()
        title = lines[i + 1].strip() if i + 1 < len(lines) else ""
        duration = lines[i + 2].strip() if i + 2 < len(lines) else "0"

        if video_id:
            videos.append({
                "id": video_id,
                "title": title,
                "url": f"https://youtube.com/watch?v={video_id}",
                "published_at": "",  # Playlists don't give us this
                "duration": int(duration) if duration.isdigit() else 0
            })

    return videos


def get_creator_slug(creator_name):
    """Convert creator name to filesystem-friendly slug."""
    return creator_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")


def save_video_metadata(source, metadata):
    """Save video metadata WITHOUT transcript."""
    creator_slug = source.get("slug") or get_creator_slug(source["name"])
    video_id = metadata["id"]

    # Create creator directories
    creator_dir = DATA_DIR / "sources" / creator_slug
    videos_dir = creator_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    # Build video record (NO TRANSCRIPT)
    video_data = {
        "source": {
            "type": "youtube",
            "id": video_id,
            "url": metadata["url"],
            "title": metadata["title"],
            "description": metadata["description"],
            "channel": metadata["channel"],
            "channel_id": metadata["channel_id"],
            "published_at": metadata["published_at"],
            "duration": metadata["duration"],
            "view_count": metadata["view_count"],
            "like_count": metadata["like_count"],
            "thumbnail": metadata["thumbnail"],
        },
        "creator": {
            "name": source["name"],
            "slug": creator_slug,
            "handle": source.get("handle", "@unknown"),
            "tier": source["tier"],
            "areas": source.get("areas", []),
            "topics": source.get("topics", []),
        },
        "collection": {
            "discovered_via": "rss" if source.get("source_type") == "channel" else "playlist",
            "discovered_at": datetime.now().isoformat(),
            "collected_at": datetime.now().isoformat(),
            "collected_by": "collect_metadata.py",
        },
        "transcript": {
            "status": "pending",  # pending | downloaded | failed | not_available
            "full_text": None,
            "segments": None,
            "segment_count": None,
            "language": None,
            "is_auto_generated": None,
        },
        "processing": {
            "stage": "metadata_collected",  # metadata_collected | ranked | transcript_downloaded | extracted
            "stages_completed": ["metadata"],
            "next_stage": "rank",
        }
    }

    # Save to YAML
    output_file = videos_dir / f"{video_id}.yaml"
    with open(output_file, "w") as f:
        yaml.dump(video_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return output_file


def add_to_queue(video_id, source, metadata):
    """Add video to processing queue."""
    queue_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"

    queue_entry = {
        "video_id": video_id,
        "title": metadata.get("title", ""),
        "creator": source.get("name", ""),
        "creator_slug": source.get("slug") or get_creator_slug(source.get("name", "")),
        "url": metadata.get("url", ""),
        "status": "pending_ranking",
        "queued_at": datetime.now().isoformat(),
        "source_path": f"data/sources/{source.get('slug') or get_creator_slug(source.get('name', ''))}/videos/{video_id}.yaml"
    }

    with open(queue_file, "w") as f:
        yaml.dump(queue_entry, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return queue_file


def process_source(source, dry_run=False):
    """Process a single source - collect metadata only."""
    source_type = source.get("source_type", "channel")

    print(f"\n{'='*60}")
    print(f"Processing: {source['name']} (Tier {source['tier']}, Type: {source_type})")

    if source_type == "playlist":
        print(f"URL: {source['url']}")
        print(f"{'='*60}")
        new_videos = get_playlist_videos(source['url'])
    else:
        print(f"Handle: {source.get('handle', 'N/A')}")
        print(f"{'='*60}")

        channel_id = source.get("channel_id")
        if not channel_id and source.get('handle'):
            channel_id = get_channel_id_from_handle(source['handle'])

        if not channel_id:
            print(f"❌ Could not get channel ID")
            return []

        print(f"Channel ID: {channel_id}")
        print("Checking RSS feed...")
        new_videos = check_rss_feed(channel_id)

    if not new_videos:
        print("No new videos found.")
        return []

    print(f"Found {len(new_videos)} video(s)")

    processed = []

    for video in new_videos:
        print(f"\n📹 {video['title'][:60]}...")

        if dry_run:
            print("   [DRY RUN - skipping]")
            processed.append(video)
            continue

        # Check if already processed
        creator_slug = source.get("slug") or get_creator_slug(source["name"])
        existing = DATA_DIR / "sources" / creator_slug / "videos" / f"{video['id']}.yaml"
        if existing.exists():
            print("   Already collected, skipping")
            continue

        # Get metadata (fast, no rate limit issues)
        print("   Fetching metadata...")
        metadata = get_video_metadata(video['id'])
        if not metadata:
            print("   ❌ Failed to get metadata")
            continue

        # Save metadata (NO TRANSCRIPT)
        output_file = save_video_metadata(source, metadata)
        print(f"   ✓ Saved metadata: {output_file.relative_to(BASE_DIR)}")

        # Add to queue for ranking
        queue_file = add_to_queue(video['id'], source, metadata)
        print(f"   ✓ Queued for ranking: {queue_file.relative_to(BASE_DIR)}")

        # Log event
        log_event("video_metadata_collected", {
            "source": source["name"],
            "video_id": video["id"],
            "title": video["title"][:100],
        })

        processed.append({
            "video": video,
            "file": output_file,
        })

        # Small delay to be polite (but not rate-limited)
        if len(new_videos) > 1:
            time.sleep(0.5)

    return processed


def main():
    parser = argparse.ArgumentParser(description="Collect video metadata (NO transcripts)")
    parser.add_argument("--source", help="Process specific source by name")
    parser.add_argument("--tier", type=int, help="Process only sources of this tier")
    parser.add_argument("--dry-run", action="store_true", help="Check without saving")
    parser.add_argument("--all", action="store_true", help="Process all configured sources")

    args = parser.parse_args()

    sources = load_sources()

    # Filter sources
    to_process = sources
    if args.source:
        to_process = [s for s in sources if args.source.lower() in s['name'].lower()]
    if args.tier:
        to_process = [s for s in to_process if s['tier'] == args.tier]

    if not args.all and not args.source and not args.tier:
        print("Use --all to process all sources, or --source/--tier to filter")
        print(f"Configured sources: {len(sources)}")
        return

    print(f"\nProcessing {len(to_process)} source(s)")
    if args.dry_run:
        print("[DRY RUN MODE]")

    all_processed = []
    for source in to_process:
        processed = process_source(source, dry_run=args.dry_run)
        all_processed.extend(processed)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Sources checked: {len(to_process)}")
    print(f"Videos found: {len(all_processed)}")
    print(f"\nNext steps:")
    print(f"  1. Run: python scripts/rank_v2.py")
    print(f"  2. Run: python scripts/download_transcripts.py")


if __name__ == "__main__":
    main()
