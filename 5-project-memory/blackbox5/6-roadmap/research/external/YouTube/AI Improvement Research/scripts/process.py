#!/usr/bin/env python3
"""
Deep Research - Video Processing Pipeline
Process a YouTube URL: download transcript → extract → categorize → save
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

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
EXTRACTS_DIR = DATA_DIR / "extracts"
VIDEOS_DIR = DATA_DIR / "videos"
CONFIG_DIR = BASE_DIR / "config"

# Ensure directories exist
for d in [TRANSCRIPTS_DIR, EXTRACTS_DIR, VIDEOS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_video_metadata(url: str) -> dict:
    """Get video metadata using yt-dlp."""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {result.stderr}")

    data = json.loads(result.stdout)
    return {
        "id": data["id"],
        "title": data["title"],
        "description": data.get("description", ""),
        "channel": data["channel"],
        "channel_id": data["channel_id"],
        "published_at": data["upload_date"],
        "duration": data["duration"],
        "view_count": data.get("view_count", 0),
        "url": f"https://youtube.com/watch?v={data['id']}",
        "thumbnail": data.get("thumbnail", ""),
    }


def download_transcript(url: str, video_id: str) -> tuple[str, list]:
    """Download auto-generated captions using yt-dlp."""
    output_path = TRANSCRIPTS_DIR / f"{video_id}"

    # Try to get auto-generated English subtitles
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-langs", "en",
        "--skip-download",
        "--no-warnings",
        "--output", str(output_path),
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Find the downloaded subtitle file
    vtt_file = TRANSCRIPTS_DIR / f"{video_id}.en.vtt"
    srt_file = TRANSCRIPTS_DIR / f"{video_id}.en.srt"

    subtitle_file = vtt_file if vtt_file.exists() else srt_file if srt_file.exists() else None

    if not subtitle_file:
        # Try manual subtitles if auto-sub failed
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--sub-langs", "en",
            "--skip-download",
            "--no-warnings",
            "--output", str(output_path),
            url
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        subtitle_file = vtt_file if vtt_file.exists() else srt_file if srt_file.exists() else None

    if not subtitle_file:
        raise RuntimeError("No subtitles available for this video")

    # Parse subtitle file
    return parse_subtitle_file(subtitle_file)


def parse_subtitle_file(filepath: Path) -> tuple[str, list]:
    """Parse VTT or SRT file into clean text and segments."""
    content = filepath.read_text(encoding="utf-8")

    # Remove WEBVTT header if present
    if content.startswith("WEBVTT"):
        content = content[6:]

    # Extract text between timestamps
    lines = content.split("\n")
    segments = []
    full_text_parts = []
    current_text = []
    current_start = None

    # Simple regex for timestamps
    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')

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
            current_start = match.group(1)
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

    full_text = " ".join(full_text_parts)
    return full_text, segments


def create_extraction_prompt(metadata: dict, transcript: str) -> str:
    """Create prompt for Claude to extract value from transcript."""
    return f"""Analyze this video about AI/Claude/MCP and extract structured value.

VIDEO METADATA:
Title: {metadata['title']}
Channel: {metadata['channel']}
Published: {metadata['published_at']}
Duration: {metadata['duration']} seconds

TRANSCRIPT:
{transcript[:15000]}  # First 15k chars to manage token usage

EXTRACTION TASK:
Extract the following in YAML format:

```yaml
summary:
  overview: "2-3 sentence summary of what this video delivers"
  key_thesis: "Main argument or insight"
  target_audience: "Who should watch this"

concepts:
  - name: "Concept/tool name"
    description: "Brief explanation"
    timestamp: "MM:SS or approximate"
    novelty: "new|known|emerging"

actionable_takeaways:
  - action: "Specific thing to try"
    context: "When/why to use this"
    difficulty: "easy|medium|hard"
    timestamp: "MM:SS"

code_examples:
  - description: "What the code does"
    timestamp: "MM:SS"
    language: "python|javascript|bash|other"

resources_mentioned:
  - name: "Tool/paper/repo name"
    type: "tool|paper|repo|link|other"
    timestamp: "MM:SS"
    url_hint: "If mentioned in transcript"

mcp_relevance:
  has_mcp_content: true|false
  mcp_servers_mentioned: []
  mcp_patterns: []

claude_relevance:
  has_claude_content: true|false
  claude_features: []
  claude_code_patterns: []

ai_memory_context:
  memory_techniques: []
  context_window_discussion: ""
  rag_mentions: []

quality_signals:
  originality: "original|repackaged|curated"
  demonstrated: true|false  # Did they actually show it working?
  depth: "surface|moderate|deep"
  confidence: "high|medium|low"

tags:
  topics: []  # From: Claude Code, MCP, AI Agents, Prompt Engineering, AI Memory, Vibe Coding, Open Source AI
  type: "tutorial|news|analysis|demo|opinion|interview"
  technical_level: "beginner|intermediate|advanced"
```

Focus on extracting actionable intelligence for someone building AI systems and MCP servers. Be concise but thorough."""


def save_extraction_yaml(video_id: str, metadata: dict, extraction_text: str, transcript: str, segments: list):
    """Save extraction as structured YAML file."""
    # Parse the extraction (assuming Claude returns YAML in code block)
    yaml_content = extraction_text
    if "```yaml" in extraction_text:
        yaml_content = extraction_text.split("```yaml")[1].split("```")[0].strip()
    elif "```" in extraction_text:
        yaml_content = extraction_text.split("```")[1].split("```")[0].strip()

    # Build full document
    document = {
        "video": {
            "id": video_id,
            "url": metadata["url"],
            "title": metadata["title"],
            "channel": metadata["channel"],
            "published_at": metadata["published_at"],
            "duration": metadata["duration"],
            "processed_at": datetime.now().isoformat(),
        },
        "extraction": yaml.safe_load(yaml_content) if yaml_content else {},
        "transcript": {
            "full_text": transcript,
            "segments": segments[:50],  # First 50 segments for reference
            "segment_count": len(segments),
        }
    }

    # Save full YAML
    output_file = EXTRACTS_DIR / f"{video_id}.yaml"
    with open(output_file, "w") as f:
        yaml.dump(document, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Also save minimal JSON for indexing
    index_entry = {
        "id": video_id,
        "title": metadata["title"],
        "channel": metadata["channel"],
        "published_at": metadata["published_at"],
        "processed_at": datetime.now().isoformat(),
        "topics": document.get("extraction", {}).get("tags", {}).get("topics", []),
        "has_mcp": document.get("extraction", {}).get("mcp_relevance", {}).get("has_mcp_content", False),
        "has_claude": document.get("extraction", {}).get("claude_relevance", {}).get("has_claude_content", False),
    }

    json_file = VIDEOS_DIR / f"{video_id}.json"
    with open(json_file, "w") as f:
        json.dump(index_entry, f, indent=2)

    return output_file


def process_video(url: str, skip_extraction: bool = False):
    """Main processing pipeline for a video URL."""
    print(f"🔍 Processing: {url}")

    # Step 1: Extract video ID
    try:
        video_id = extract_video_id(url)
        print(f"   Video ID: {video_id}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # Check if already processed
    existing = EXTRACTS_DIR / f"{video_id}.yaml"
    if existing.exists():
        print(f"⚠️  Already processed: {existing}")
        return existing

    # Step 2: Get metadata
    print("📊 Fetching metadata...")
    try:
        metadata = get_video_metadata(url)
        print(f"   Title: {metadata['title']}")
        print(f"   Channel: {metadata['channel']}")
    except Exception as e:
        print(f"❌ Failed to get metadata: {e}")
        sys.exit(1)

    # Step 3: Download transcript
    print("📝 Downloading transcript...")
    try:
        transcript, segments = download_transcript(url, video_id)
        print(f"   ✓ Downloaded {len(segments)} segments")
    except Exception as e:
        print(f"❌ Failed to download transcript: {e}")
        sys.exit(1)

    if skip_extraction:
        print("⏭️  Skipping extraction (transcript only)")
        return None

    # Step 4: Generate extraction prompt
    print("🤖 Preparing extraction...")
    prompt = create_extraction_prompt(metadata, transcript)

    # Save prompt for Claude to use
    prompt_file = DATA_DIR / f"{video_id}_prompt.txt"
    prompt_file.write_text(prompt)

    print("\n" + "="*60)
    print("EXTRACTION PROMPT READY")
    print("="*60)
    print(f"\nPrompt saved to: {prompt_file}")
    print("\nTo extract value, run Claude with this prompt.")
    print("Then paste the response back to save the extraction.")
    print("\nOr use: claude -p $(cat {})", prompt_file)
    print("="*60)

    return {
        "video_id": video_id,
        "metadata": metadata,
        "transcript": transcript,
        "segments": segments,
        "prompt_file": prompt_file,
    }


def save_claude_extraction(video_id: str, claude_response: str):
    """Save Claude's extraction response."""
    # Load the processing data
    json_file = VIDEOS_DIR / f"{video_id}.json"
    if json_file.exists():
        with open(json_file) as f:
            data = json.load(f)
    else:
        print(f"❌ No processing data found for {video_id}")
        return

    # Load transcript
    transcript_file = TRANSCRIPTS_DIR / f"{video_id}.txt"
    if transcript_file.exists():
        transcript = transcript_file.read_text()
        segments = [{"start": "00:00", "text": line} for line in transcript.split("\n") if line]
    else:
        transcript = ""
        segments = []

    # Build metadata from index
    metadata = {
        "url": f"https://youtube.com/watch?v={video_id}",
        "title": data.get("title", "Unknown"),
        "channel": data.get("channel", "Unknown"),
        "published_at": data.get("published_at", ""),
        "duration": 0,
    }

    # Save extraction
    output_file = save_extraction_yaml(video_id, metadata, claude_response, transcript, segments)
    print(f"✅ Extraction saved: {output_file}")

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Process YouTube video for deep research")
    parser.add_argument("url", help="YouTube URL to process")
    parser.add_argument("--skip-extraction", action="store_true", help="Only download transcript")
    parser.add_argument("--save-extraction", metavar="VIDEO_ID", help="Save Claude extraction for video ID")
    parser.add_argument("--extraction-file", metavar="FILE", help="File containing Claude's extraction")

    args = parser.parse_args()

    if args.save_extraction and args.extraction_file:
        # Mode: Save extraction from file
        claude_response = Path(args.extraction_file).read_text()
        save_claude_extraction(args.save_extraction, claude_response)
    else:
        # Mode: Process new video
        result = process_video(args.url, args.skip_extraction)

        if result and isinstance(result, dict):
            # Save intermediate data for later extraction
            video_id = result["video_id"]
            metadata = result["metadata"]

            # Save transcript to file
            transcript_file = TRANSCRIPTS_DIR / f"{video_id}.txt"
            transcript_file.write_text(result["transcript"])

            # Save minimal index
            index_entry = {
                "id": video_id,
                "title": metadata["title"],
                "channel": metadata["channel"],
                "published_at": metadata["published_at"],
                "duration": metadata["duration"],
                "processed_at": datetime.now().isoformat(),
                "status": "pending_extraction",
            }

            json_file = VIDEOS_DIR / f"{video_id}.json"
            with open(json_file, "w") as f:
                json.dump(index_entry, f, indent=2)

            print(f"\n📁 Files saved:")
            print(f"   Transcript: {transcript_file}")
            print(f"   Index: {json_file}")
            print(f"   Prompt: {result['prompt_file']}")


if __name__ == "__main__":
    main()
