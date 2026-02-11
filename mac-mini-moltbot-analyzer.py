#!/usr/bin/env python3
"""
MoltBot Transcript Analyzer

Analyzes YouTube transcripts with multi-pass Claude analysis,
rates them 0-100, and sends key learnings to Telegram via MoltBot.

Usage:
    python mac-mini-moltbot-analyzer.py --continuous
    python mac-mini-moltbot-analyzer.py --once
    python mac-mini-moltbot-analyzer.py --video VIDEO_ID
"""

import os
import sys
import json
import sqlite3
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import anthropic

# Configuration
DB_PATH = Path("/Users/shaansisodia/Projects/youtube-ai-research/database/queue.db")
TRANSCRIPTS_DIR = Path("/Users/shaansisodia/Projects/youtube-ai-research/content/transcripts")
ANALYSIS_DIR = Path("/Users/shaansisodia/Projects/youtube-ai-research/analysis/moltbot")
LOG_FILE = Path("/Users/shaansisodia/Projects/youtube-ai-research/.logs/moltbot-analyzer.log")
TELEGRAM_CHAT_ID = "7643203581"
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# Initialize Claude client
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Ensure directories exist
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log(message: str):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")


def read_transcript(video_id: str, channel: str) -> Optional[str]:
    """Read transcript file for a video."""
    # Try multiple path patterns
    paths = [
        TRANSCRIPTS_DIR / channel / f"{video_id}.md",
        TRANSCRIPTS_DIR / channel / f"{video_id}.txt",
        TRANSCRIPTS_DIR / channel / f"{video_id}.json",
    ]

    for path in paths:
        if path.exists():
            content = path.read_text()
            # If markdown with YAML frontmatter, extract just the transcript
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content

    return None


def analyze_with_claude(transcript: str, title: str, channel: str) -> Dict:
    """
    Multi-pass analysis with Claude API.
    Returns structured analysis with rating.
    """

    # Truncate if too long
    max_chars = 10000
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "\n\n[Transcript truncated for length]"

    # Multi-pass prompt
    prompt = f"""You are an expert AI research analyst. Analyze this YouTube video transcript.

VIDEO: {title}
CHANNEL: {channel}

Perform 3 passes of analysis:

---
PASS 1: SUMMARY & CONTEXT
- What's the main topic?
- Who is the target audience?
- What's the format (tutorial, news, deep-dive)?

PASS 2: KEY LEARNINGS
Extract 3-5 specific, actionable insights:
- New tools/frameworks mentioned
- Techniques or workflows
- Important announcements or updates
- Gotchas or common mistakes

PASS 3: RATING & RECOMMENDATION
Rate the video 0-100 based on:
- Novelty (30%): How new/unique is this information?
- Actionability (30%): Can viewers implement this immediately?
- Accuracy (20%): Is the information reliable and correct?
- Production (20%): Is it well-explained and structured?

Also provide:
- Who should watch this?
- Priority level (P0=Critical, P1=High, P2=Medium, P3=Low)
- Should we add to knowledge base? (Yes/No)

---

Respond in this exact JSON format:
{{
  "summary": "2-3 sentence summary",
  "target_audience": "Who should watch",
  "key_learnings": [
    "Learning 1 with specific detail",
    "Learning 2 with specific detail",
    "Learning 3 with specific detail"
  ],
  "novelty_score": 8,
  "actionability_score": 7,
  "accuracy_score": 9,
  "production_score": 8,
  "overall_rating": 80,
  "priority": "P1",
  "add_to_kb": true,
  "tags": ["tag1", "tag2", "tag3"]
}}

Transcript:
{transcript}"""

    try:
        # Use Anthropic API
        response = claude_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            temperature=0.3,
            system="You are an expert AI research analyst. Always respond with valid JSON.",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON from response
        content = response.content[0].text

        # Extract JSON if wrapped in markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        analysis = json.loads(content.strip())
        return analysis

    except Exception as e:
        log(f"Analysis failed: {e}")
        return {
            "summary": "Analysis failed",
            "target_audience": "Unknown",
            "key_learnings": ["Error during analysis"],
            "overall_rating": 0,
            "priority": "P3",
            "add_to_kb": False,
            "tags": ["error"]
        }


def send_to_telegram(video_id: str, channel: str, title: str, analysis: Dict) -> bool:
    """Send analysis to Telegram via OpenClaw/MoltBot."""

    rating = analysis.get("overall_rating", 0)
    priority = analysis.get("priority", "P3")

    # Format message
    learnings = "\n".join([f"  💡 {l}" for l in analysis.get("key_learnings", [])[:3]])

    message = f"""📺 <b>New Analysis: {title[:60]}{'...' if len(title) > 60 else ''}</b>

📊 <b>Rating: {rating}/100</b> | Priority: {priority}
📺 Channel: {channel}

📝 <b>Summary:</b>
{analysis.get('summary', 'N/A')[:200]}...

💡 <b>Key Learnings:</b>
{learnings}

🎯 <b>Target:</b> {analysis.get('target_audience', 'N/A')}
🏷️ <b>Tags:</b> {', '.join(analysis.get('tags', [])[:5])}

🔗 <a href="https://youtube.com/watch?v={video_id}">Watch Video</a>"""

    try:
        # Method 1: Try OpenClaw CLI
        result = subprocess.run(
            ["openclaw", "message", "send",
             "--channel", "telegram",
             "--target", TELEGRAM_CHAT_ID,
             "--message", message],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            log(f"✅ Sent to Telegram via OpenClaw")
            return True

    except Exception as e:
        log(f"OpenClaw send failed: {e}")

    # Method 2: Write to queue for MoltBot to pick up
    try:
        queue_file = Path(f"/Users/shaansisodia/.openclaw/telegram/outbox/analysis_{video_id}.json")
        queue_file.parent.mkdir(parents=True, exist_ok=True)

        with open(queue_file, "w") as f:
            json.dump({
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "video_id": video_id,
                "rating": rating
            }, f, indent=2)

        log(f"📤 Queued for Telegram: {queue_file}")
        return True

    except Exception as e:
        log(f"Queue failed: {e}")
        return False


def save_analysis(video_id: str, channel: str, title: str, analysis: Dict):
    """Save analysis to file."""

    date_str = datetime.now().strftime("%Y-%m-%d")
    date_dir = ANALYSIS_DIR / date_str
    date_dir.mkdir(exist_ok=True)

    analysis_file = date_dir / f"{video_id}.json"

    data = {
        "video_id": video_id,
        "channel": channel,
        "title": title,
        "analyzed_at": datetime.now().isoformat(),
        "analysis": analysis
    }

    with open(analysis_file, "w") as f:
        json.dump(data, f, indent=2)

    log(f"💾 Analysis saved: {analysis_file}")
    return analysis_file


def mark_as_analyzed(video_id: str, rating: int):
    """Mark video as analyzed in database."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moltbot_analysis (
            video_id TEXT PRIMARY KEY,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER,
            sent_to_telegram BOOLEAN DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR REPLACE INTO moltbot_analysis (video_id, rating, sent_to_telegram)
        VALUES (?, ?, 1)
    """, (video_id, rating))

    conn.commit()
    conn.close()


def get_unanalyzed_video() -> Optional[Dict]:
    """Get one unanalyzed completed video with highest score."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create analysis table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moltbot_analysis (
            video_id TEXT PRIMARY KEY,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER,
            sent_to_telegram BOOLEAN DEFAULT 0
        )
    """)

    # Find unanalyzed completed video
    cursor.execute("""
        SELECT v.video_id, v.channel_slug, v.channel_name, v.title, v.score
        FROM video_queue v
        LEFT JOIN moltbot_analysis m ON v.video_id = m.video_id
        WHERE v.status = 'completed'
        AND v.transcript_path IS NOT NULL
        AND m.video_id IS NULL
        ORDER BY v.score DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)

    return None


def analyze_single_video(video_id: str):
    """Analyze a specific video by ID."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, channel_slug, channel_name, title
        FROM video_queue
        WHERE video_id = ? AND status = 'completed'
    """, (video_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        log(f"Video {video_id} not found or not completed")
        return

    video = dict(row)
    process_video(video)


def process_video(video: Dict):
    """Process a single video."""

    video_id = video["video_id"]
    channel = video["channel_slug"]
    channel_name = video["channel_name"]
    title = video["title"]

    log(f"🎬 Processing: {title} ({video_id})")

    # Read transcript
    transcript = read_transcript(video_id, channel)
    if not transcript:
        log(f"❌ Transcript not found for {video_id}")
        return

    log(f"📄 Transcript length: {len(transcript)} chars")

    # Analyze
    log(f"🤖 Analyzing with Claude...")
    analysis = analyze_with_claude(transcript, title, channel_name)

    rating = analysis.get("overall_rating", 0)
    log(f"⭐ Rating: {rating}/100")

    # Save analysis
    save_analysis(video_id, channel_name, title, analysis)

    # Send to Telegram if rating >= 60
    if rating >= 60:
        log(f"📤 Sending to Telegram...")
        send_to_telegram(video_id, channel_name, title, analysis)
    else:
        log(f"⏭️ Rating {rating} < 60, skipping Telegram")

    # Mark as analyzed
    mark_as_analyzed(video_id, rating)

    log(f"✅ Complete: {title}")


def run_continuous():
    """Run continuously, checking for new videos."""

    log("🚀 Starting MoltBot Transcript Analyzer (Continuous Mode)")
    log("=" * 60)

    while True:
        try:
            video = get_unanalyzed_video()

            if video:
                process_video(video)
                log("⏳ Waiting 60 seconds before next...")
                import time
                time.sleep(60)
            else:
                log("😴 No new videos. Sleeping 5 minutes...")
                import time
                time.sleep(300)

        except KeyboardInterrupt:
            log("👋 Stopping...")
            break
        except Exception as e:
            log(f"❌ Error: {e}")
            import time
            time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description="MoltBot Transcript Analyzer")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--once", action="store_true", help="Analyze one video and exit")
    parser.add_argument("--video", help="Analyze specific video ID")

    args = parser.parse_args()

    if args.video:
        analyze_single_video(args.video)
    elif args.once:
        video = get_unanalyzed_video()
        if video:
            process_video(video)
        else:
            log("No unanalyzed videos found")
    else:
        # Default to continuous
        run_continuous()


if __name__ == "__main__":
    main()
