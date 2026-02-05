#!/bin/bash
# Analyze YouTube Transcripts using BlackBox5 Analysis Pattern
# Usage: ./analyze-transcripts.sh [--batch-size N] [--priority P0|P1|P2|P3]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
QUEUE_FILE="$PROJECT_DIR/queues/transcript-queue.yaml"
OUTPUT_DIR="$PROJECT_DIR/output/analyses"
REPORTS_DIR="$PROJECT_DIR/reports"

# Parse arguments
BATCH_SIZE=5
PRIORITY="all"

while [[ $# -gt 0 ]]; do
  case $1 in
    --batch-size)
      BATCH_SIZE="$2"
      shift 2
      ;;
    --priority)
      PRIORITY="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Create directories
mkdir -p "$OUTPUT_DIR" "$REPORTS_DIR"

# Generate run ID
RUN_ID="run-$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$REPORTS_DIR/$RUN_ID"
mkdir -p "$RUN_DIR"

echo "=========================================="
echo "YouTube Transcript Analysis"
echo "=========================================="
echo "Run ID: $RUN_ID"
echo "Batch Size: $BATCH_SIZE"
echo "Priority: $PRIORITY"
echo ""

# Function to read queue and get pending items
get_pending_transcripts() {
  local priority_filter="$1"

  # Extract pending items from YAML (simple grep/sed approach)
  # In production, use yq or similar
  if [[ "$priority_filter" == "all" ]]; then
    grep -A 5 "status: pending" "$QUEUE_FILE" | grep "file:" | sed 's/.*file: //'
  else
    # Filter by priority
    awk "/priority: $priority_filter/{found=1} found && /file:/{print \$2; found=0}" "$QUEUE_FILE"
  fi | head -$BATCH_SIZE
}

# Get transcripts to analyze
TRANSCRIPTS=$(get_pending_transcripts "$PRIORITY")

if [[ -z "$TRANSCRIPTS" ]]; then
  echo "No pending transcripts found."
  exit 0
fi

echo "Transcripts to analyze:"
echo "$TRANSCRIPTS" | nl
echo ""

# Initialize run report
cat > "$RUN_DIR/analysis-report.md" << EOF
# Transcript Analysis Report

**Run ID:** $RUN_ID
**Date:** $(date -Iseconds)
**Batch Size:** $BATCH_SIZE
**Priority Filter:** $PRIORITY

## Transcripts Analyzed

EOF

# Analyze each transcript
COUNTER=0
TOTAL_SCORE=0

while IFS= read -r transcript_file; do
  COUNTER=$((COUNTER + 1))
  VIDEO_ID=$(basename "$transcript_file" .md)
  CHANNEL=$(basename "$(dirname "$transcript_file")")

  echo "[$COUNTER] Analyzing: $VIDEO_ID ($CHANNEL)"

  # Create analysis document
  ANALYSIS_FILE="$OUTPUT_DIR/${VIDEO_ID}-analysis.md"

  # Run analysis (in production, this would spawn a Claude subagent)
  cat > "$ANALYSIS_FILE" << EOF
# Analysis: $VIDEO_ID

**Video ID:** $VIDEO_ID
**Channel:** $CHANNEL
**File:** $transcript_file
**Analyzed:** $(date -Iseconds)
**Status:** pending-detailed-analysis

## Quick Summary

This transcript requires detailed analysis using the 3-loop method:
- Loop 1: Surface Scan (metadata, claims)
- Loop 2: Content Archaeology (deep content analysis)
- Loop 3: Insight Extraction (actionable insights)

## Raw Transcript Available

See: $transcript_file

## Next Steps

Run deep analysis with:
\`\`\`
claude -p "analyze-transcript" --file "$transcript_file" --output "$ANALYSIS_FILE"
\`\`\`
EOF

  # Update queue (mark as in_progress)
  sed -i.bak "s/\(video_id: $VIDEO_ID\)/\1\n    status: in_progress/" "$QUEUE_FILE" 2>/dev/null || true

  # Add to report
  echo "$COUNTER. **$VIDEO_ID** ($CHANNEL) → [$ANALYSIS_FILE]($ANALYSIS_FILE)" >> "$RUN_DIR/analysis-report.md"

done <<< "$TRANSCRIPTS"

# Finalize report
cat >> "$RUN_DIR/analysis-report.md" << EOF

## Summary

- **Total Analyzed:** $COUNTER
- **Output Directory:** $OUTPUT_DIR
- **Run Directory:** $RUN_DIR

## Next Steps

1. Review individual analysis files
2. Run insight aggregation: \`./aggregate-insights.sh\`
3. Update queue with completed status

EOF

echo ""
echo "=========================================="
echo "Analysis Complete"
echo "=========================================="
echo "Analyzed: $COUNTER transcripts"
echo "Output: $OUTPUT_DIR"
echo "Report: $RUN_DIR/analysis-report.md"
echo ""
