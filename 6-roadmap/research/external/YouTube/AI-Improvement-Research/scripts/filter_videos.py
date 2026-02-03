#!/usr/bin/env python3
"""
Filter videos database - remove shorts, add duration scoring

Rules:
- Remove all videos < 2 minutes (shorts)
- Add +50% score bonus for videos >= 17 minutes
"""

import json
from pathlib import Path
from datetime import datetime


def parse_duration(duration):
    """Parse duration to seconds."""
    if isinstance(duration, int):
        return duration
    try:
        return int(duration)
    except:
        return 0


def filter_channel_videos(channel_data):
    """Filter videos for a single channel."""
    videos = channel_data.get('videos', [])

    filtered = []
    removed_shorts = 0
    long_form_count = 0

    for video in videos:
        duration = parse_duration(video.get('duration', 0))

        # Skip shorts (< 2 minutes = 120 seconds)
        if duration < 120:
            removed_shorts += 1
            continue

        # Mark long-form content (>= 17 minutes = 1020 seconds)
        if duration >= 1020:
            video['is_long_form'] = True
            video['duration_bonus'] = 1.5  # 50% bonus
            long_form_count += 1
        else:
            video['is_long_form'] = False
            video['duration_bonus'] = 1.0

        filtered.append(video)

    return filtered, removed_shorts, long_form_count


def main():
    """Main filtering function."""
    base_dir = Path(__file__).parent.parent
    channels_dir = base_dir / 'database' / 'channels'

    if not channels_dir.exists():
        print(f"Channels directory not found: {channels_dir}")
        return

    total_removed = 0
    total_long_form = 0
    total_before = 0
    total_after = 0

    print("=" * 70)
    print("Filtering Videos - Removing Shorts, Flagging Long-Form")
    print("=" * 70)
    print()

    for json_file in sorted(channels_dir.glob('*.json')):
        try:
            with open(json_file, 'r') as f:
                channel_data = json.load(f)

            channel_name = json_file.stem.replace('_', ' ').title()
            original_count = len(channel_data.get('videos', []))

            # Filter videos
            filtered_videos, removed, long_form = filter_channel_videos(channel_data)

            # Update channel data
            channel_data['videos'] = filtered_videos
            channel_data['filtered_at'] = datetime.now().isoformat()
            channel_data['stats'] = {
                'original_count': original_count,
                'filtered_count': len(filtered_videos),
                'shorts_removed': removed,
                'long_form_count': long_form,
            }

            # Save back
            with open(json_file, 'w') as f:
                json.dump(channel_data, f, indent=2)

            total_before += original_count
            total_after += len(filtered_videos)
            total_removed += removed
            total_long_form += long_form

            status = "✓"
            if long_form > 0:
                status = "⭐"

            print(f"{status} {channel_name:<30} | Before: {original_count:3} | After: {len(filtered_videos):3} | Removed: {removed:3} | Long-form: {long_form:2}")

        except Exception as e:
            print(f"✗ Error processing {json_file}: {e}")

    print()
    print("=" * 70)
    print("FILTERING COMPLETE")
    print("=" * 70)
    print(f"Total videos before: {total_before}")
    print(f"Total videos after:  {total_after}")
    print(f"Shorts removed:      {total_removed}")
    print(f"Long-form videos:    {total_long_form}")
    print(f"Removal rate:        {(total_removed/total_before*100):.1f}%")
    print("=" * 70)


if __name__ == '__main__':
    main()
