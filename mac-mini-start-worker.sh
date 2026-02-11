#!/bin/bash
# Start YouTube Transcript Worker on Mac Mini

cd ~/Projects/youtube-ai-research
source venv/bin/activate

# Create necessary directories
mkdir -p content/transcripts .state .logs analysis/by_date analysis/digests

# Run worker with reasonable limits
# Using --limit to avoid IP blocks - run frequently with small batches
exec python scripts/worker/worker.py \
    --output-dir content/transcripts \
    --state-dir .state \
    --daily-limit 100 \
    --request-delay 3.0 \
    --batch-size 5 \
    --continuous
