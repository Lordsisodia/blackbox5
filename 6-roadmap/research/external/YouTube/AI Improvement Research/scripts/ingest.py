#!/usr/bin/env python3
"""
Deep Research - Stage 1: Intelligent Ingestion
Downloads video metadata and transcripts, organized by creator
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

# Try to import youtube-transcript-api, fallback to yt-dlp
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    YT_TRANSCRIPT_API_AVAILABLE = False
    print("Warning: youtube-transcript-api not available, falling back to yt-dlp")

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_creators():
    """Load creator configuration."""
    creators_file = CONFIG_DIR / "creators.yaml"
    with open(creators_file) as f:
        config = yaml.safe_load(f)
    return config.get("creators", [])


def get_channel_id_from_handle(handle):
    """Extract channel ID from YouTube handle using yt-dlp."""
    url = f"https://www.youtube.com/{handle}"
    cmd = ["yt-dlp", "--print", "channel_id", "--playlist-items", "1", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_video_metadata(video_id):
    """Get video metadata using yt-dlp."""
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


def download_transcript(video_id):
    """Download transcript using youtube-transcript-api (preferred) or yt-dlp fallback."""

    # Try youtube-transcript-api first (more reliable, no rate limits)
    if YT_TRANSCRIPT_API_AVAILABLE:
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_obj = ytt_api.fetch(video_id)

            segments = []
            full_text_parts = []

            for snippet in transcript_obj:
                # Convert seconds to HH:MM:SS format
                start_secs = int(snippet.start)
                hours = start_secs // 3600
                minutes = (start_secs % 3600) // 60
                seconds = start_secs % 60
                timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                text = snippet.text.strip()
                if text:
                    segments.append({
                        "start": timestamp,
                        "text": text
                    })
                    full_text_parts.append(text)

            full_text = " ".join(full_text_parts)
            return full_text, segments

        except Exception as e:
            print(f"   youtube-transcript-api failed: {e}")
            print("   Falling back to yt-dlp...")

    # Fallback to yt-dlp
    return download_transcript_ytdlp(video_id)


def download_transcript_ytdlp(video_id):
    """Fallback transcript download using yt-dlp."""
    url = f"https://youtube.com/watch?v={video_id}"
    output_base = f"/tmp/{video_id}"

    # Download auto-generated subtitles
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-langs", "en",
        "--skip-download",
        "--no-warnings",
        "--output", output_base,
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Find the subtitle file
    vtt_file = Path(f"{output_base}.en.vtt")
    srt_file = Path(f"{output_base}.en.srt")

    subtitle_file = vtt_file if vtt_file.exists() else srt_file if srt_file.exists() else None

    if not subtitle_file:
        # Try manual subtitles
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--sub-langs", "en",
            "--skip-download",
            "--no-warnings",
            "--output", output_base,
            url
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        subtitle_file = vtt_file if vtt_file.exists() else srt_file if srt_file.exists() else None

    if not subtitle_file:
        return None, None

    # Parse subtitle file
    return parse_subtitle_file(subtitle_file)


def parse_subtitle_file(filepath):
    """Parse VTT or SRT file into clean text and segments."""
    content = filepath.read_text(encoding="utf-8")

    # Remove WEBVTT header
    if content.startswith("WEBVTT"):
        content = content[6:]

    lines = content.split("\n")
    segments = []
    full_text_parts = []
    current_text = []
    current_start = None

    # Timestamp pattern
    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}[\.\,]?\d{0,3})\s*-->\s*(\d{2}:\d{2}:\d{2}[\.\,]?\d{0,3})')

    for line in lines:
        line = line.strip()

        if time_pattern.match(line):
            # Save previous segment
            if current_text and current_start:
                text = " ".join(current_text).strip()
                if text:
                    segments.append({
                        "start": current_start,
                        "text": text
                    })
                    full_text_parts.append(text)

            # Start new segment
            match = time_pattern.match(line)
            current_start = match.group(1).replace(",", ".")
            current_text = []

        elif line and not line.isdigit() and not line.startswith("NOTE"):
            # Remove HTML-like tags
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                current_text.append(line)

    # Save last segment
    if current_text and current_start:
        text = " ".join(current_text).strip()
        if text:
            segments.append({
                "start": current_start,
                "text": text
            })
            full_text_parts.append(text)

    # Cleanup temp file
    filepath.unlink(missing_ok=True)

    full_text = " ".join(full_text_parts)
    return full_text, segments


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


def get_creator_slug(creator_name):
    """Convert creator name to filesystem-friendly slug."""
    return creator_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")


def save_video_data(creator, metadata, transcript, segments):
    """Save video data organized by creator."""
    creator_slug = get_creator_slug(creator["name"])
    video_id = metadata["id"]

    # Create creator directories
    creator_dir = DATA_DIR / "by_creator" / creator_slug
    videos_dir = creator_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    # Build complete video record
    video_data = {
        "video": {
            "id": video_id,
            "url": metadata["url"],
            "title": metadata["title"],
            "description": metadata["description"],
            "published_at": metadata["published_at"],
            "duration": metadata["duration"],
            "view_count": metadata["view_count"],
            "like_count": metadata["like_count"],
            "thumbnail": metadata["thumbnail"],
        },
        "creator": {
            "name": creator["name"],
            "handle": creator["handle"],
            "tier": creator["tier"],
            "focus_areas": creator.get("focus_areas", []),
        },
        "source": {
            "discovered_via": "vip_rss",
            "discovered_at": datetime.now().isoformat(),
            "processed_at": datetime.now().isoformat(),
        },
        "transcript": {
            "full_text": transcript,
            "segments": segments[:100],  # First 100 segments for reference
            "segment_count": len(segments),
            "language": "en",
            "is_auto_generated": True,
        },
        "processing": {
            "stage": "ingested",  # ingested | classified | extracted | reported
            "stages_completed": ["ingest"],
            "next_stage": "classify",
        }
    }

    # Save to YAML
    output_file = videos_dir / f"{video_id}.yaml"
    with open(output_file, "w") as f:
        yaml.dump(video_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return output_file


def process_creator(creator, dry_run=False):
    """Process a single creator - check RSS and download new videos."""
    print(f"\n{'='*60}")
    print(f"Processing: {creator['name']} (Tier {creator['tier']})")
    print(f"Handle: {creator['handle']}")
    print(f"Focus: {', '.join(creator.get('focus_areas', []))}")
    print(f"{'='*60}")

    # Get channel ID
    channel_id = get_channel_id_from_handle(creator['handle'])
    if not channel_id:
        print(f"❌ Could not get channel ID for {creator['name']}")
        return []

    print(f"Channel ID: {channel_id}")

    # Check RSS for new videos
    print("Checking RSS feed...")
    new_videos = check_rss_feed(channel_id)

    if not new_videos:
        print("No new videos found.")
        return []

    print(f"Found {len(new_videos)} new video(s)")

    processed = []

    for video in new_videos:
        print(f"\n📹 {video['title'][:60]}...")
        print(f"   Published: {video['published_at']}")

        if dry_run:
            print("   [DRY RUN - skipping download]")
            processed.append(video)
            continue

        # Check if already processed
        creator_slug = get_creator_slug(creator["name"])
        existing = DATA_DIR / "by_creator" / creator_slug / "videos" / f"{video['id']}.yaml"
        if existing.exists():
            print("   Already processed, skipping")
            continue

        # Get metadata
        print("   Fetching metadata...")
        metadata = get_video_metadata(video['id'])
        if not metadata:
            print("   ❌ Failed to get metadata")
            continue

        # Download transcript
        print("   Downloading transcript...")
        transcript, segments = download_transcript(video['id'])

        if not transcript:
            print("   ⚠️  No transcript available")
            transcript = ""
            segments = []

        print(f"   ✓ Transcript: {len(segments)} segments, {len(transcript)} chars")

        # Save data
        output_file = save_video_data(creator, metadata, transcript, segments)
        print(f"   ✓ Saved: {output_file.relative_to(BASE_DIR)}")

        processed.append({
            "video": video,
            "file": output_file,
            "has_transcript": len(transcript) > 0,
        })

        # Polite delay between videos
        if len(new_videos) > 1:
            delay = random.uniform(2, 5)
            print(f"   Waiting {delay:.1f}s...")
            time.sleep(delay)

    return processed


def main():
    parser = argparse.ArgumentParser(description="Ingest YouTube videos from VIP creators")
    parser.add_argument("--creator", help="Process specific creator by name")
    parser.add_argument("--tier", type=int, help="Process only creators of this tier")
    parser.add_argument("--dry-run", action="store_true", help="Check RSS without downloading")
    parser.add_argument("--url", help="Process single YouTube URL (manual mode)")

    args = parser.parse_args()

    # Load creators
    creators = load_creators()

    if args.url:
        # Manual URL mode
        print(f"Manual mode: {args.url}")
        # TODO: Implement manual URL processing
        return

    # Filter creators
    to_process = creators

    if args.creator:
        to_process = [c for c in creators if args.creator.lower() in c['name'].lower()]
        if not to_process:
            print(f"Creator '{args.creator}' not found")
            return

    if args.tier:
        to_process = [c for c in to_process if c['tier'] == args.tier]

    print(f"\nProcessing {len(to_process)} creator(s)")
    if args.dry_run:
        print("[DRY RUN MODE - no downloads]")

    # Process each creator
    all_processed = []
    for creator in to_process:
        processed = process_creator(creator, dry_run=args.dry_run)
        all_processed.extend(processed)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Creators checked: {len(to_process)}")
    print(f"Videos found: {len(all_processed)}")
    if not args.dry_run:
        print(f"Videos downloaded: {sum(1 for v in all_processed if v.get('has_transcript', False))}")


if __name__ == "__main__":
    main()
