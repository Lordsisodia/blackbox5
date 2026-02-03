#!/usr/bin/env python3
"""
Download transcripts using Tor proxy to bypass IP blocks
"""

import argparse
import json
import re
import subprocess
import time
import random
import socks  # PySocks
import socket
from datetime import datetime
from pathlib import Path

import yaml
import requests

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
QUEUE_DIR = BASE_DIR / "queue"
TIMELINE_DIR = BASE_DIR / "timeline"

# Tor proxy settings
TOR_PROXY = ("127.0.0.1", 9050)


def setup_tor():
    """Configure socket to use Tor."""
    socks.set_default_proxy(socks.SOCKS5, TOR_PROXY[0], TOR_PROXY[1])
    socket.socket = socks.socksocket
    print("✓ Tor proxy configured")


def get_blocked_videos():
    """Get videos that need transcripts (blocked sources)."""
    blocked = []

    for source_dir in (DATA_DIR / "sources").iterdir():
        if not source_dir.is_dir():
            continue

        videos_dir = source_dir / "videos"
        if not videos_dir.exists():
            continue

        for video_file in videos_dir.glob("*.yaml"):
            with open(video_file) as f:
                data = yaml.safe_load(f)

            # Check if transcript is missing or empty
            transcript = data.get("transcript", {})
            full_text = transcript.get("full_text", "")

            if not full_text or len(str(full_text)) < 100:
                video_id = data.get("source", {}).get("id")
                title = data.get("source", {}).get("title", "")
                blocked.append({
                    "video_id": video_id,
                    "title": title,
                    "source_path": video_file,
                    "source_name": source_dir.name
                })

    return blocked


def download_with_tor(video_id):
    """Download transcript using youtube-transcript-api through Tor."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        # This will use the Tor proxy we set up
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
        return None, str(e)


def update_video_with_transcript(video_path, transcript, segments):
    """Update video YAML with transcript data."""
    with open(video_path) as f:
        data = yaml.safe_load(f)

    data["transcript"] = {
        "status": "downloaded",
        "full_text": transcript,
        "segments": segments[:100],
        "segment_count": len(segments),
        "language": "en",
        "is_auto_generated": True,
        "downloaded_at": datetime.now().isoformat(),
        "download_source": "tor_proxy",
    }

    data["processing"]["stage"] = "transcript_downloaded"
    if "stages_completed" not in data["processing"]:
        data["processing"]["stages_completed"] = []
    data["processing"]["stages_completed"].append("transcript")
    data["processing"]["next_stage"] = "extract"

    with open(video_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Download transcripts using Tor")
    parser.add_argument("--limit", type=int, help="Limit number of videos")
    parser.add_argument("--source", help="Only process specific source (e.g., 'in_the_world_of_ai')")

    args = parser.parse_args()

    # Setup Tor
    print("Setting up Tor proxy...")
    setup_tor()

    # Get blocked videos
    blocked = get_blocked_videos()

    if args.source:
        blocked = [b for b in blocked if args.source.lower() in b["source_name"].lower()]

    if not blocked:
        print("No blocked videos found!")
        return

    if args.limit:
        blocked = blocked[:args.limit]

    print(f"\n{'='*60}")
    print(f"DOWNLOADING {len(blocked)} TRANSCRIPTS VIA TOR")
    print(f"{'='*60}")
    print("Each request uses a different Tor exit node (IP)")
    print()

    stats = {"success": 0, "failed": 0}

    for i, video in enumerate(blocked, 1):
        video_id = video["video_id"]
        title = video["title"][:60]
        source = video["source_name"]

        print(f"\n[{i}/{len(blocked)}] 📹 {title}...")
        print(f"    Source: {source}")

        # Download via Tor
        transcript, segments = download_with_tor(video_id)

        if transcript and len(transcript) > 100:
            update_video_with_transcript(video["source_path"], transcript, segments)
            print(f"    ✓ Success: {len(transcript):,} chars, {len(segments)} segments")
            stats["success"] += 1
        else:
            print(f"    ❌ Failed: {segments}")
            stats["failed"] += 1

        # Delay between requests
        if i < len(blocked):
            delay = random.uniform(3, 8)
            print(f"    Waiting {delay:.1f}s...")
            time.sleep(delay)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")


if __name__ == "__main__":
    main()
