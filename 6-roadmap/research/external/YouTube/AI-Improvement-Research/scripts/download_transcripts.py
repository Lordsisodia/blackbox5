#!/usr/bin/env python3
"""
AI Improvement Research - Stage 3: Transcript Download
Downloads transcripts ONLY for videos that passed ranking

This is the slow/rate-limited step - we only do it for valuable videos
to stay under YouTube's rate limits.
"""

import argparse
import re
import subprocess
import time
import random
from datetime import datetime
from pathlib import Path

import yaml

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    YT_TRANSCRIPT_API_AVAILABLE = False

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
QUEUE_DIR = BASE_DIR / "queue"
TIMELINE_DIR = BASE_DIR / "timeline"

# Rate limiting settings
MIN_DELAY = 5  # Minimum seconds between transcript downloads
MAX_DELAY = 15  # Maximum seconds between transcript downloads
MAX_RETRIES = 3  # Max retries on failure


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


def get_approved_videos():
    """Get videos that need transcripts (Tier 1 always, others if ranked high)."""
    approved = []

    for queue_file in (QUEUE_DIR / "pending").glob("*.yaml"):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        # Get video data to check tier
        video_id = data.get("video_id")
        source_path = Path(DATA_DIR) / data.get("source_path", "")

        if not source_path.exists():
            continue

        with open(source_path) as f:
            video_data = yaml.safe_load(f)

        # Check if transcript already downloaded
        transcript_status = video_data.get("transcript", {}).get("status")
        if transcript_status == "downloaded":
            continue

        # Get creator tier
        tier = video_data.get("creator", {}).get("tier", 3)

        # Tier 1: Always transcribe (override ranking)
        if tier == 1:
            approved.append({
                "video_id": video_id,
                "title": data.get("title", ""),
                "source_path": source_path,
                "queue_file": queue_file,
                "score": 100,  # Force high score
                "tier": tier,
                "force": True  # Flag to indicate forced inclusion
            })
            continue

        # Tier 2 & 3: Only if ranked high
        ranking = data.get("ranking_v2", {})
        if not ranking:
            continue

        decision = data.get("decision", {})
        if not decision.get("should_process", False):
            continue

        approved.append({
            "video_id": video_id,
            "title": data.get("title", ""),
            "source_path": source_path,
            "queue_file": queue_file,
            "score": ranking.get("final_score", 0),
            "tier": tier,
            "force": False
        })

    # Sort by: Tier 1 first, then by score
    approved.sort(key=lambda x: (0 if x["tier"] == 1 else 1, -x["score"]))
    return approved


def download_transcript_yt_api(video_id):
    """Download transcript using youtube-transcript-api."""
    if not YT_TRANSCRIPT_API_AVAILABLE:
        return None, None

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
        return None, str(e)


def download_transcript_ytdlp(video_id):
    """Download transcript using yt-dlp fallback."""
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

    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}[\.\,]?\d{0,3})\s*-->\s*(\d{2}:\d{2}:\d{2}[\.\,]?\d{0,3})')

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


def update_video_with_transcript(video_path, transcript, segments, source="yt-api"):
    """Update video YAML with transcript data."""
    with open(video_path) as f:
        data = yaml.safe_load(f)

    data["transcript"] = {
        "status": "downloaded",
        "full_text": transcript,
        "segments": segments[:100],  # First 100 segments
        "segment_count": len(segments),
        "language": "en",
        "is_auto_generated": True,
        "downloaded_at": datetime.now().isoformat(),
        "download_source": source,
    }

    data["processing"]["stage"] = "transcript_downloaded"
    data["processing"]["stages_completed"].append("transcript")
    data["processing"]["next_stage"] = "extract"

    with open(video_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def download_transcripts(dry_run=False, limit=None):
    """Download transcripts for all approved videos."""
    approved = get_approved_videos()

    if limit:
        approved = approved[:limit]

    if not approved:
        print("No approved videos waiting for transcripts")
        return

    print(f"\n{'='*60}")
    print(f"DOWNLOADING TRANSCRIPTS FOR {len(approved)} VIDEOS")
    print(f"{'='*60}")
    print(f"This will take approximately {len(approved) * 10 // 60} minutes")
    print(f"(with {MIN_DELAY}-{MAX_DELAY}s delays between downloads)")
    print()

    stats = {"success": 0, "failed": 0, "skipped": 0}

    for i, video in enumerate(approved, 1):
        video_id = video["video_id"]
        title = video["title"][:60]
        score = video["score"]

        print(f"\n[{i}/{len(approved)}] 📹 {title}...")
        print(f"    Score: {score}/100")

        if dry_run:
            print("    [DRY RUN - skipping download]")
            stats["skipped"] += 1
            continue

        # Try youtube-transcript-api first
        print("    Trying youtube-transcript-api...")
        transcript, segments = download_transcript_yt_api(video_id)

        if transcript:
            source = "yt-api"
        else:
            # Fallback to yt-dlp
            print("    Falling back to yt-dlp...")
            transcript, segments = download_transcript_ytdlp(video_id)
            source = "yt-dlp"

        if transcript and len(transcript) > 100:
            update_video_with_transcript(video["source_path"], transcript, segments, source)
            print(f"    ✓ Downloaded: {len(transcript):,} chars, {len(segments)} segments")
            stats["success"] += 1

            log_event("transcript_downloaded", {
                "video_id": video_id,
                "chars": len(transcript),
                "segments": len(segments),
                "source": source
            })
        else:
            print(f"    ❌ Failed to download transcript")
            stats["failed"] += 1

            log_event("transcript_failed", {
                "video_id": video_id,
                "error": str(segments) if segments else "Unknown"
            })

        # Rate limiting delay (except for last video)
        if i < len(approved):
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"    Waiting {delay:.1f}s...")
            time.sleep(delay)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    if dry_run:
        print(f"Skipped (dry run): {stats['skipped']}")


def main():
    parser = argparse.ArgumentParser(description="Download transcripts for approved videos")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded")
    parser.add_argument("--limit", type=int, help="Limit number of transcripts to download")
    parser.add_argument("--video", help="Download specific video by ID")

    args = parser.parse_args()

    if args.video:
        # Download specific video
        for source_dir in (DATA_DIR / "sources").iterdir():
            video_file = source_dir / "videos" / f"{args.video}.yaml"
            if video_file.exists():
                with open(video_file) as f:
                    data = yaml.safe_load(f)

                print(f"Downloading transcript for: {data['source']['title']}")
                transcript, segments = download_transcript_yt_api(args.video)

                if not transcript:
                    transcript, segments = download_transcript_ytdlp(args.video)

                if transcript:
                    update_video_with_transcript(video_file, transcript, segments)
                    print(f"✓ Downloaded: {len(transcript):,} chars")
                else:
                    print("❌ Failed")
                return

        print(f"Video {args.video} not found")
    else:
        download_transcripts(dry_run=args.dry_run, limit=args.limit)


if __name__ == "__main__":
    main()
