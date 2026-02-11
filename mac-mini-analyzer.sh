#!/bin/bash
# MoltBot Transcript Analysis System
# Analyzes YouTube transcripts and sends insights to Telegram

set -e

DB_PATH="$HOME/Projects/youtube-ai-research/database/queue.db"
TRANSCRIPTS_DIR="$HOME/Projects/youtube-ai-research/content/transcripts"
ANALYSIS_DIR="$HOME/Projects/youtube-ai-research/analysis/by_date"
LOG_FILE="$HOME/Projects/youtube-ai-research/.logs/analyzer.log"

# Ensure directories exist
mkdir -p "$ANALYSIS_DIR" "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to analyze transcript with Claude
analyze_transcript() {
    local video_id="$1"
    local channel="$2"
    local transcript_file="$3"

    log "Analyzing $video_id from $channel"

    # Read transcript
    local transcript=$(cat "$transcript_file")

    # Truncate if too long (Claude has context limits)
    local max_chars=8000
    if [ ${#transcript} -gt $max_chars ]; then
        transcript="${transcript:0:$max_chars}..."
    fi

    # Multi-pass analysis with Claude
    local analysis=$(cat <<EOF | claude --stdin 2>/dev/null || echo "ERROR"
Analyze this YouTube transcript about AI/technology. Perform 3 passes:

PASS 1 - SUMMARY:
- What is the main topic?
- Who is the target audience?
- What's the video format (tutorial, news, opinion)?

PASS 2 - KEY LEARNINGS:
- Extract 3-5 specific actionable insights
- Identify any new tools, techniques, or frameworks mentioned
- Note any important announcements or updates

PASS 3 - RATING & RECOMMENDATION:
- Rate the video 0-100 based on:
  * Novelty (30%): How new is this information?
  * Actionability (30%): Can viewers implement this?
  * Accuracy (20%): Is the information reliable?
  * Production (20%): Is it well-explained?
- Who should watch this?
- Should we add this to our knowledge base?

Format your response as:

📊 RATING: [X]/100

🎯 SUMMARY:
[Brief 2-3 sentence summary]

💡 KEY LEARNINGS:
1. [Learning 1]
2. [Learning 2]
3. [Learning 3]

🎬 RECOMMENDATION:
[Who should watch and why]

Transcript:
$transcript
EOF
)

    echo "$analysis"
}

# Function to send to Telegram via OpenClaw
send_to_telegram() {
    local video_id="$1"
    local channel="$2"
    local title="$3"
    local analysis="$4"
    local rating="$5"

    # Format message
    local message=$(cat <<EOF
📺 *New Analysis: $title*

Channel: $channel
Video ID: $video_id

$analysis

🔗 https://youtube.com/watch?v=$video_id
EOF
)

    # Send via OpenClaw Telegram
    log "Sending to Telegram..."

    # Use OpenClaw CLI to send message
    export PATH="$HOME/.local/bin:$PATH"
    export OPENCLAW_CONFIG="$HOME/.openclaw"

    # Try to send via openclaw message command
    openclaw message send \
        --channel telegram \
        --target "7643203581" \
        --message "$message" 2>/dev/null || {

        # Fallback: write to a file that MoltBot can pick up
        local msg_file="$HOME/.openclaw/telegram/outbox/analysis_$(date +%s).json"
        mkdir -p "$(dirname "$msg_file")"

        cat > "$msg_file" <<EOF
{
  "chat_id": "7643203581",
  "text": "$message",
  "parse_mode": "Markdown"
}
EOF
        log "Queued message for Telegram: $msg_file"
    }
}

# Main loop
main() {
    log "Starting MoltBot Transcript Analyzer"

    while true; do
        log "Checking for new transcripts..."

        # Find unanalyzed completed videos
        local unanalyzed=$(sqlite3 "$DB_PATH" <<EOF
SELECT video_id, channel_slug, channel_name, title
FROM video_queue
WHERE status = 'completed'
AND transcript_path IS NOT NULL
AND video_id NOT IN (
    SELECT DISTINCT video_id FROM analysis_log
    WHERE analyzed_at > datetime('now', '-7 days')
)
ORDER BY score DESC
LIMIT 1;
EOF
)

        if [ -z "$unanalyzed" ]; then
            log "No new transcripts to analyze. Sleeping..."
            sleep 300  # 5 minutes
            continue
        fi

        # Parse results
        IFS='|' read -r video_id channel_slug channel_name title <<< "$unanalyzed"

        log "Found: $title ($video_id)"

        # Find transcript file
        local transcript_file=$(find "$TRANSCRIPTS_DIR" -name "${video_id}*" -type f | head -1)

        if [ -z "$transcript_file" ]; then
            log "Transcript file not found for $video_id"
            sleep 60
            continue
        fi

        # Analyze
        local analysis=$(analyze_transcript "$video_id" "$channel_name" "$transcript_file")

        # Extract rating
        local rating=$(echo "$analysis" | grep -oE 'RATING: [0-9]+' | grep -oE '[0-9]+' || echo "N/A")

        # Save analysis
        local analysis_file="$ANALYSIS_DIR/${video_id}_$(date +%Y%m%d_%H%M).md"
        cat > "$analysis_file" <<EOF
---
video_id: $video_id
channel: $channel_name
title: $title
analyzed_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
rating: $rating
---

$analysis
EOF

        log "Analysis saved: $analysis_file"

        # Send to Telegram if rating is good (>= 60)
        if [ "$rating" != "N/A" ] && [ "$rating" -ge 60 ]; then
            send_to_telegram "$video_id" "$channel_name" "$title" "$analysis" "$rating"
        else
            log "Rating $rating < 60, skipping Telegram notification"
        fi

        # Mark as analyzed
        sqlite3 "$DB_PATH" <<EOF
CREATE TABLE IF NOT EXISTS analysis_log (
    video_id TEXT PRIMARY KEY,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER,
    analysis_file TEXT
);
INSERT OR REPLACE INTO analysis_log (video_id, rating, analysis_file)
VALUES ('$video_id', '$rating', '$analysis_file');
EOF

        log "Analysis complete. Waiting before next..."
        sleep 60  # 1 minute between analyses
    done
}

# Run main loop
main "$@"
