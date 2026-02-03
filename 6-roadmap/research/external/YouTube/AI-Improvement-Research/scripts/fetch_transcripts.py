#!/usr/bin/env python3
"""
Fetch transcripts for long-form videos (17+ minutes)

Only fetches transcripts for videos that are:
1. >= 17 minutes (1020 seconds)
2. Don't already have a transcript
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime


def load_existing_transcripts(transcripts_dir: Path):
    """Load list of video IDs that already have transcripts."""
    if not transcripts_dir.exists():
        return set()

    existing = set()
    for transcript_file in transcripts_dir.glob('*.txt'):
        existing.add(transcript_file.stem)
    return existing


def fetch_transcript(video_id: str, output_path: Path) -> bool:
    """Fetch transcript using yt-dlp."""
    try:
        # Use yt-dlp to get transcript
        result = subprocess.run(
            ['yt-dlp', '--skip-download', '--write-subs', '--write-auto-subs',
             '--sub-langs', 'en', '--sub-format', 'txt',
             '--output', str(output_path.with_suffix('')),
             f'https://youtube.com/watch?v={video_id}'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if transcript was created
        if output_path.exists():
            return True

        # Try to get description as fallback
        result = subprocess.run(
            ['yt-dlp', '--skip-download', '--print', 'description',
             f'https://youtube.com/watch?v={video_id}'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout:
            output_path.write_text(f"[DESCRIPTION ONLY]\n\n{result.stdout}")
            return True

        return False

    except Exception as e:
        print(f"    Error fetching {video_id}: {e}")
        return False


def main():
    """Main function to fetch transcripts."""
    base_dir = Path(__file__).parent.parent
    channels_dir = base_dir / 'database' / 'channels'
    transcripts_dir = base_dir / 'database' / 'transcripts'
    transcripts_dir.mkdir(exist_ok=True)

    existing_transcripts = load_existing_transcripts(transcripts_dir)
    print(f"Found {len(existing_transcripts)} existing transcripts")

    videos_to_fetch = []

    # Find all long-form videos that need transcripts
    for json_file in channels_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                channel_data = json.load(f)

            channel_name = json_file.stem

            for video in channel_data.get('videos', []):
                if video.get('is_long_form') and video.get('id'):
                    video_id = video['id']
                    if video_id not in existing_transcripts:
                        videos_to_fetch.append({
                            'id': video_id,
                            'title': video.get('title', 'Unknown'),
                            'channel': channel_name,
                            'duration': video.get('duration', 0)
                        })
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    print(f"\nFound {len(videos_to_fetch)} long-form videos needing transcripts")
    print("=" * 70)

    if not videos_to_fetch:
        print("No transcripts to fetch!")
        return

    # Fetch transcripts (limit to first 10 for now)
    to_fetch = videos_to_fetch[:10]
    print(f"Fetching first {len(to_fetch)} transcripts...\n")

    successful = 0
    failed = 0

    for i, video in enumerate(to_fetch, 1):
        print(f"[{i}/{len(to_fetch)}] {video['channel']}: {video['title'][:60]}...")

        output_path = transcripts_dir / f"{video['id']}.txt"

        if fetch_transcript(video['id'], output_path):
            print(f"    ✓ Saved to {output_path.name}")
            successful += 1
        else:
            print(f"    ✗ Failed to fetch")
            failed += 1

    print()
    print("=" * 70)
    print(f"Complete: {successful} successful, {failed} failed")
    print(f"Transcripts saved to: {transcripts_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
