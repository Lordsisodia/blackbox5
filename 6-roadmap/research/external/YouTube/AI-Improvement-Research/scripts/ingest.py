#!/usr/bin/env python3
"""
AI Improvement Research - Stage 1: Intelligent Ingestion
Downloads video metadata and transcripts, organized by creator

New structure:
- data/sources/{creator_slug}/videos/{video_id}.yaml  (raw data)
- timeline/events/YYYY-MM-DD.yaml                      (event log)
- queue/pending/{video_id}.yaml                        (processing queue)
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
TIMELINE_DIR = BASE_DIR / "timeline"
QUEUE_DIR = BASE_DIR / "queue"

# Ensure directories exist
(DATA_DIR / "sources").mkdir(parents=True, exist_ok=True)
(TIMELINE_DIR / "events").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "pending").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "processing").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "completed").mkdir(parents=True, exist_ok=True)


def load_sources():
    """Load source configuration from sources.yaml."""
    sources_file = CONFIG_DIR / "sources.yaml"
    all_sources = []
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "sources" in doc:
                # Mark channel sources
                for source in doc.get("sources", []):
                    source["source_type"] = "channel"
                    all_sources.append(source)
            if doc and "playlists" in doc:
                # Mark playlist sources
                for playlist in doc.get("playlists", []):
                    playlist["source_type"] = "playlist"
                    all_sources.append(playlist)
    return all_sources


def log_event(event_type, data):
    """Log an event to the timeline."""
    today = datetime.now().strftime("%Y-%m-%d")
    events_file = TIMELINE_DIR / "events" / f"{today}.yaml"

    # Load existing events or create new
    if events_file.exists():
        with open(events_file) as f:
            events_data = yaml.safe_load(f) or {}
    else:
        events_data = {"date": today, "events": []}

    # Add new event
    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        **data
    }
    events_data["events"].append(event)

    # Save events
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

            # Extract video ID from URL (handles both regular and shorts URLs)
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


def get_creator_slug(creator_name):
    """Convert creator name to filesystem-friendly slug."""
    return creator_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")


def get_priority_for_tier(tier):
    """Get queue priority based on creator tier."""
    tier_priorities = {
        1: "critical",   # Tier 1 = must watch
        2: "high",       # Tier 2 = high quality
        3: "normal"      # Tier 3 = filtered
    }
    return tier_priorities.get(tier, "normal")


def save_video_data(source, metadata, transcript, segments):
    """Save video data organized by creator in new structure."""
    creator_slug = source.get("slug") or get_creator_slug(source["name"])
    video_id = metadata["id"]

    # Create creator directories
    creator_dir = DATA_DIR / "sources" / creator_slug
    videos_dir = creator_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    # Build complete video record with new schema
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
            "handle": source["handle"],
            "tier": source["tier"],
            "areas": source.get("areas", []),
            "topics": source.get("topics", []),
        },
        "collection": {
            "discovered_via": "rss",
            "discovered_at": datetime.now().isoformat(),
            "collected_at": datetime.now().isoformat(),
            "collected_by": "ingest.py",
        },
        "transcript": {
            "full_text": transcript,
            "segments": segments[:100],  # First 100 segments for reference
            "segment_count": len(segments),
            "language": "en",
            "is_auto_generated": True,
        },
        "processing": {
            "stage": "ingested",  # ingested | queued | extracting | extracted | synthesized
            "stages_completed": ["ingest"],
            "next_stage": "extract",
        }
    }

    # Save to YAML
    output_file = videos_dir / f"{video_id}.yaml"
    with open(output_file, "w") as f:
        yaml.dump(video_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return output_file


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


def process_source(source, dry_run=False):
    """Process a single source - check RSS or playlist and download new videos."""
    source_type = source.get("source_type", "channel")

    print(f"\n{'='*60}")
    print(f"Processing: {source['name']} (Tier {source['tier']}, Type: {source_type})")

    if source_type == "playlist":
        print(f"URL: {source['url']}")
        print(f"Areas: {', '.join(source.get('areas', []))}")
        print(f"{'='*60}")

        # Get videos from playlist
        new_videos = get_playlist_videos(source['url'])

        if not new_videos:
            print("No videos found in playlist.")
            return []

        print(f"Found {len(new_videos)} video(s) in playlist")

    else:
        # Channel source - use RSS
        print(f"Handle: {source.get('handle', 'N/A')}")
        print(f"Areas: {', '.join(source.get('areas', []))}")
        print(f"{'='*60}")

        # Get channel ID
        channel_id = source.get("channel_id")
        if not channel_id and source.get('handle'):
            channel_id = get_channel_id_from_handle(source['handle'])

        if not channel_id:
            print(f"❌ Could not get channel ID for {source['name']}")
            log_event("source_error", {
                "source": source["name"],
                "error": "Could not get channel ID"
            })
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
    priority = get_priority_for_tier(source["tier"])

    for video in new_videos:
        print(f"\n📹 {video['title'][:60]}...")
        print(f"   Published: {video['published_at']}")

        if dry_run:
            print("   [DRY RUN - skipping download]")
            processed.append(video)
            continue

        # Check if already processed
        creator_slug = source.get("slug") or get_creator_slug(source["name"])
        existing = DATA_DIR / "sources" / creator_slug / "videos" / f"{video['id']}.yaml"
        if existing.exists():
            print("   Already processed, skipping")
            continue

        # Get metadata
        print("   Fetching metadata...")
        metadata = get_video_metadata(video['id'])
        if not metadata:
            print("   ❌ Failed to get metadata")
            log_event("video_error", {
                "source": source["name"],
                "video_id": video["id"],
                "error": "Failed to get metadata"
            })
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
        output_file = save_video_data(source, metadata, transcript, segments)
        print(f"   ✓ Saved: {output_file.relative_to(BASE_DIR)}")

        # Add to queue
        queue_file = add_to_queue(video['id'], source, metadata, priority)
        print(f"   ✓ Queued: {queue_file.relative_to(BASE_DIR)} (priority: {priority})")

        # Log event
        log_event("video_discovered", {
            "source": source["name"],
            "source_slug": creator_slug,
            "video_id": video["id"],
            "title": video["title"][:100],
            "priority": priority,
            "has_transcript": len(transcript) > 0
        })

        processed.append({
            "video": video,
            "file": output_file,
            "queue_file": queue_file,
            "has_transcript": len(transcript) > 0,
        })

        # Polite delay between videos
        if len(new_videos) > 1:
            delay = random.uniform(2, 5)
            print(f"   Waiting {delay:.1f}s...")
            time.sleep(delay)

    return processed


def main():
    parser = argparse.ArgumentParser(description="Ingest YouTube videos from configured sources")
    parser.add_argument("--source", help="Process specific source by name")
    parser.add_argument("--tier", type=int, help="Process only sources of this tier")
    parser.add_argument("--dry-run", action="store_true", help="Check RSS without downloading")
    parser.add_argument("--url", help="Process single YouTube URL (manual mode)")
    parser.add_argument("--all", action="store_true", help="Process all configured sources")

    args = parser.parse_args()

    # Load sources
    sources = load_sources()

    if args.url:
        # Manual URL mode
        print(f"Manual mode: {args.url}")
        # TODO: Implement manual URL processing
        return

    # Filter sources
    to_process = sources

    if args.source:
        to_process = [s for s in sources if args.source.lower() in s['name'].lower()]
        if not to_process:
            print(f"Source '{args.source}' not found")
            return

    if args.tier:
        to_process = [s for s in to_process if s['tier'] == args.tier]

    if not args.all and not args.source and not args.tier:
        print("Use --all to process all sources, or --source/--tier to filter")
        print(f"Configured sources: {len(sources)}")
        print(f"  Tier 1: {len([s for s in sources if s['tier'] == 1])}")
        print(f"  Tier 2: {len([s for s in sources if s['tier'] == 2])}")
        print(f"  Tier 3: {len([s for s in sources if s['tier'] == 3])}")
        return

    print(f"\nProcessing {len(to_process)} source(s)")
    if args.dry_run:
        print("[DRY RUN MODE - no downloads]")

    # Process each source
    all_processed = []
    for source in to_process:
        processed = process_source(source, dry_run=args.dry_run)
        all_processed.extend(processed)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Sources checked: {len(to_process)}")
    print(f"Videos found: {len(all_processed)}")
    if not args.dry_run:
        print(f"Videos downloaded: {sum(1 for v in all_processed if v.get('has_transcript', False))}")
        print(f"Videos queued: {len(all_processed)}")

    # Log completion event
    if not args.dry_run and all_processed:
        log_event("ingest_completed", {
            "sources_checked": len(to_process),
            "videos_found": len(all_processed),
            "videos_downloaded": sum(1 for v in all_processed if v.get('has_transcript', False))
        })


if __name__ == "__main__":
    main()
