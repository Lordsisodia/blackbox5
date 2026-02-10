#!/usr/bin/env python3
"""
Quick script to scrape a few YouTube videos and save transcripts to research folder
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent))

from scraper import Config, YouTubeScraper

# Interesting AI/tech videos to scrape
VIDEO_IDS = [
    'JfwwaXhJ1vY',  # AI agents video
    'aircAruvnKk',  # Neural networks explained
    'TCH_1BHY58I',  # AI tutorial
]

def save_to_research(video_id, video_data, transcript, research_dir):
    """Save transcript to research folder with analysis"""
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}_{video_id}.md"
    filepath = research_dir / filename

    # Create content
    content = f"# Video Analysis: {video_data.get('title', 'Unknown')}\n\n"
    content += f"**Video ID:** {video_id}\n"
    content += f"**Channel:** {video_data.get('channel', 'Unknown')}\n"
    content += f"**URL:** https://www.youtube.com/watch?v={video_id}\n"
    content += f"**Word Count:** {transcript['word_count']:,}\n"
    content += f"**Scraped:** {datetime.now().isoformat()}\n\n"

    # Extract key points (simple word frequency)
    words = transcript['full_text'].lower().split()
    word_freq = {}

    # Filter out common words
    stop_words = {'the', 'and', 'is', 'to', 'a', 'in', 'that', 'it', 'of', 'for', 'on', 'with', 'as', 'this', 'are', 'be', 'at', 'or', 'was', 'i', 'you', 'we', 'so', 'but', 'not', 'have', 'will'}

    for word in words:
        if len(word) > 3 and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    content += "## Key Topics\n\n"
    for word, count in top_words:
        content += f"- **{word}** ({count} mentions)\n"

    content += "\n## Transcript\n\n"
    for snippet in transcript['snippets'][:50]:  # First 50 snippets
        start = snippet['start']
        minutes = int(start // 60)
        seconds = int(start % 60)
        content += f"[{minutes}:{seconds:02d}] {snippet['text']}\n"

    if len(transcript['snippets']) > 50:
        content += f"\n... ({len(transcript['snippets']) - 50} more segments)\n"

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Saved to {filepath}")
    return filepath

def main():
    print("=" * 70)
    print("YouTube Video Scraper - Research Extraction")
    print("=" * 70)
    print()

    # Setup
    config = Config('config/config.yaml')
    scraper = YouTubeScraper(config)

    # Research directory
    research_dir = Path('/opt/blackbox5/5-project-memory/blackbox5/knowledge/research')
    research_dir.mkdir(parents=True, exist_ok=True)

    # Process each video
    for video_id in VIDEO_IDS:
        print(f"\n{'=' * 70}")
        print(f"Processing: {video_id}")
        print(f"{'=' * 70}")

        try:
            # Get video metadata
            video_data = scraper.get_video_metadata(video_id)
            print(f"Title: {video_data.get('title', 'Unknown')}")
            print(f"Channel: {video_data.get('channel', 'Unknown')}")

            # Get transcript
            transcript = scraper.get_transcript(video_id)

            if transcript:
                print(f"✓ Transcript: {transcript['word_count']:,} words")

                # Save to research
                save_to_research(video_id, video_data, transcript, research_dir)

                # Also save to knowledge base
                video_data['video_id'] = video_id
                transcript['snippets']  # Ensure snippets are serializable

                print(f"✓ Saved to research folder")
            else:
                print(f"✗ No transcript available")

        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

    print()
    print("=" * 70)
    print("Scraping complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
