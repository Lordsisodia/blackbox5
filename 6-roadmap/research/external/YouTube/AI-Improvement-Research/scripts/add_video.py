#!/usr/bin/env python3
"""
Add individual YouTube video to the database and pipeline.
Usage: python scripts/add_video.py <youtube_url> [--creator "Creator Name"] [--tier 1]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Try to import youtube-transcript-api
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
TIMELINE_DIR = BASE_DIR / "timeline"
QUEUE_DIR = BASE_DIR / "queue"

# Ensure directories exist
(DATA_DIR / "sources").mkdir(parents=True, exist_ok=True)
(TIMELINE_DIR / "events").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "pending").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "processing").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "completed").mkdir(parents=True, exist_ok=True)


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
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
        print(f"❌ Failed to get metadata: {result.stderr}")
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

    # Try youtube-transcript-api first
    if YT_TRANSCRIPT_API_AVAILABLE:
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_obj = ytt_api.fetch(video_id)

            segments = []
            full_text_parts = []

            for snippet in transcript_obj:
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

    if content.startswith("WEBVTT"):
        content = content[6:]

    lines = content.split("\n")
    segments = []
    full_text_parts = []
    current_text = []
    current_start = None

    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}[\.,]?\d{0,3})\s*-->\s*(\d{2}:\d{2}:\d{2}[\.,]?\d{0,3})')

    for line in lines:
        line = line.strip()

        if time_pattern.match(line):
            if current_text and current_start:
                text = " ".join(current_text).strip()
                if text:
                    segments.append({
                        "start": current_start,
                        "text": text
                    })
                    full_text_parts.append(text)

            match = time_pattern.match(line)
            current_start = match.group(1).replace(",", ".")
            current_text = []

        elif line and not line.isdigit() and not line.startswith("NOTE"):
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                current_text.append(line)

    if current_text and current_start:
        text = " ".join(current_text).strip()
        if text:
            segments.append({
                "start": current_start,
                "text": text
            })
            full_text_parts.append(text)

    filepath.unlink(missing_ok=True)

    full_text = " ".join(full_text_parts)
    return full_text, segments


def get_creator_slug(creator_name):
    """Convert creator name to filesystem-friendly slug."""
    return creator_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")


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

    return event


def add_to_queue(video_id, creator, metadata, priority="normal"):
    """Add a video to the processing queue."""
    queue_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"

    queue_entry = {
        "video_id": video_id,
        "title": metadata.get("title", ""),
        "creator": creator.get("name", ""),
        "creator_slug": get_creator_slug(creator.get("name", "")),
        "url": metadata.get("url", ""),
        "priority": priority,
        "status": "pending",
        "queued_at": datetime.now().isoformat(),
        "source_path": f"data/sources/{get_creator_slug(creator.get('name', ''))}/videos/{video_id}.yaml"
    }

    with open(queue_file, "w") as f:
        yaml.dump(queue_entry, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return queue_file


def save_video_data(source, metadata, transcript, segments):
    """Save video data organized by creator."""
    creator_slug = source.get("slug") or get_creator_slug(source["name"])
    video_id = metadata["id"]

    creator_dir = DATA_DIR / "sources" / creator_slug
    videos_dir = creator_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

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
            "discovered_via": "manual",
            "discovered_at": datetime.now().isoformat(),
            "collected_at": datetime.now().isoformat(),
            "collected_by": "add_video.py",
        },
        "transcript": {
            "full_text": transcript,
            "segments": segments[:100],
            "segment_count": len(segments),
            "language": "en",
            "is_auto_generated": True,
        },
        "processing": {
            "stage": "ingested",
            "stages_completed": ["ingest"],
            "next_stage": "extract",
        }
    }

    output_file = videos_dir / f"{video_id}.yaml"
    with open(output_file, "w") as f:
        yaml.dump(video_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Add individual YouTube video to the database")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--creator", help="Creator/channel name (auto-detected if not provided)")
    parser.add_argument("--tier", type=int, default=1, choices=[1, 2, 3],
                        help="Creator tier (1=critical, 2=high, 3=normal)")
    parser.add_argument("--areas", nargs="+", default=["ai-engineering"],
                        help="Content areas/tags")
    parser.add_argument("--topics", nargs="+", default=["user-added"],
                        help="Content topics/tags")

    args = parser.parse_args()

    # Extract video ID
    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"❌ Could not extract video ID from URL: {args.url}")
        print("Supported formats:")
        print("  - https://www.youtube.com/watch?v=VIDEO_ID")
        print("  - https://youtu.be/VIDEO_ID")
        print("  - https://www.youtube.com/shorts/VIDEO_ID")
        sys.exit(1)

    print(f"📹 Video ID: {video_id}")

    # Get metadata
    print("Fetching video metadata...")
    metadata = get_video_metadata(video_id)
    if not metadata:
        print("❌ Failed to fetch metadata")
        sys.exit(1)

    print(f"✓ Title: {metadata['title']}")
    print(f"✓ Channel: {metadata['channel']}")
    print(f"✓ Duration: {metadata['duration']} seconds")

    # Determine creator info
    creator_name = args.creator or metadata['channel']
    creator_slug = get_creator_slug(creator_name)

    source = {
        "name": creator_name,
        "slug": creator_slug,
        "handle": f"@{creator_slug}",
        "tier": args.tier,
        "areas": args.areas,
        "topics": args.topics,
    }

    # Download transcript
    print("Downloading transcript...")
    transcript, segments = download_transcript(video_id)

    if not transcript:
        print("⚠️  No transcript available")
        transcript = ""
        segments = []
    else:
        print(f"✓ Transcript: {len(segments)} segments, {len(transcript)} characters")

    # Save data
    print("Saving video data...")
    output_file = save_video_data(source, metadata, transcript, segments)
    print(f"✓ Saved: {output_file.relative_to(BASE_DIR)}")

    # Add to queue
    priority_map = {1: "critical", 2: "high", 3: "normal"}
    priority = priority_map[args.tier]
    queue_file = add_to_queue(video_id, source, metadata, priority)
    print(f"✓ Queued: {queue_file.relative_to(BASE_DIR)} (priority: {priority})")

    # Log event
    log_event("video_added_manually", {
        "source": creator_name,
        "source_slug": creator_slug,
        "video_id": video_id,
        "title": metadata["title"][:100],
        "priority": priority,
        "has_transcript": len(transcript) > 0,
        "tier": args.tier
    })

    print("\n" + "="*60)
    print("SUCCESS")
    print("="*60)
    print(f"Video added to database and pipeline")
    print(f"Next stage: extract (run scripts/extract.py to process)")


if __name__ == "__main__":
    main()
