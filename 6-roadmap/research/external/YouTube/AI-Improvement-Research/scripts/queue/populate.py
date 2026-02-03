#!/usr/bin/env python3
"""
Populate transcript queue from existing video database.

Reads all videos from database/channels/*.json and adds them to queue.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from queue.manager import QueueManager, get_channel_tier
from queue.database import QueueDatabase


def load_all_videos(channels_dir: Path):
    """Load all videos from channel JSON files."""
    videos = []

    for json_file in channels_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                channel_data = json.load(f)

            channel_slug = json_file.stem
            channel_name = channel_slug.replace('_', ' ').title()

            for video in channel_data.get('videos', []):
                if not video.get('id'):
                    continue

                duration = video.get('duration', 0)
                try:
                    duration = int(duration)
                except:
                    duration = 0

                # Skip shorts (< 2 minutes)
                if duration < 120:
                    continue

                videos.append({
                    'video_id': video['id'],
                    'channel_slug': channel_slug,
                    'channel_name': channel_name,
                    'title': video.get('title', 'Unknown'),
                    'upload_date': video.get('upload_date'),
                    'duration': duration,
                })

        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    return videos


def calculate_score(channel_slug: str, upload_date: str, duration: int) -> float:
    """Calculate AI training value score."""
    tier, tier_mult = get_channel_tier(channel_slug)

    # Recency multiplier
    try:
        upload = datetime.strptime(upload_date, '%Y%m%d')
        days_ago = (datetime.now() - upload).days
    except:
        days_ago = 999

    if days_ago <= 7:
        recency_mult = 1.5
    elif days_ago <= 14:
        recency_mult = 1.2
    else:
        recency_mult = 1.0

    # Duration multiplier (18+ min = 1.2x)
    duration_mult = 1.2 if duration >= 1080 else 1.0

    # Base score 50
    return 50 * recency_mult * duration_mult * tier_mult


def main():
    """Main population function."""
    print("=" * 70)
    print("Populating Transcript Queue")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent.parent.parent
    channels_dir = base_dir / 'database' / 'channels'

    # Initialize queue
    manager = QueueManager()
    db = QueueDatabase()

    # Check existing
    existing_stats = manager.get_stats()
    print(f"Existing queue: {existing_stats['total']} videos")
    print(f"  - Completed: {existing_stats['completed']}")
    print(f"  - Pending: {existing_stats['pending']}")
    print(f"  - Failed: {existing_stats['failed']}")
    print()

    # Load all videos
    print("Loading videos from channels...")
    videos = load_all_videos(channels_dir)
    print(f"Found {len(videos)} videos (filtered shorts)")
    print()

    # Add to queue
    print("Adding videos to queue...")
    added = 0
    skipped = 0
    errors = 0

    for i, video in enumerate(videos, 1):
        # Check if already exists
        if db.video_exists(video['video_id']):
            skipped += 1
            continue

        # Calculate score
        score = calculate_score(
            video['channel_slug'],
            video.get('upload_date', ''),
            video.get('duration', 0)
        )
        video['score'] = score

        # Add to queue
        if manager.add_video(video):
            added += 1
            if i % 100 == 0:
                print(f"  Progress: {i}/{len(videos)} processed, {added} added")
        else:
            errors += 1

    print()
    print("=" * 70)
    print("Population Complete")
    print("=" * 70)
    print(f"Total videos: {len(videos)}")
    print(f"Added: {added}")
    print(f"Skipped (already exists): {skipped}")
    print(f"Errors: {errors}")
    print()

    # Show final stats
    final_stats = manager.get_stats()
    print("Queue Status:")
    print(f"  Total: {final_stats['total']}")
    print(f"  Pending: {final_stats['pending']}")
    print(f"  Completed: {final_stats['completed']}")
    print(f"  Failed: {final_stats['failed']}")
    print()

    # Show priority distribution
    priority_dist = manager.get_priority_distribution()
    print("Priority Distribution:")
    for p in ['P0', 'P1', 'P2', 'P3']:
        count = priority_dist.get(p, 0)
        bar = '█' * (count // max(final_stats['total'] // 50, 1))
        print(f"  {p}: {count:4} {bar}")
    print("=" * 70)


if __name__ == '__main__':
    main()
