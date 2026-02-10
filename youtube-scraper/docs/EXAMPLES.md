# YouTube Scraper - Usage Examples

This document contains real-world examples of using the YouTube scraper.

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Python API Examples](#python-api-examples)
3. [Agent Integration](#agent-integration)
4. [Automation Examples](#automation-examples)
5. [Advanced Patterns](#advanced-patterns)

---

## Basic Usage

### Example 1: Simple Search

```bash
python3 scraper.py --query "machine learning tutorial" --max-results 5
```

**Output:**
```
2025-02-10 20:00:00 - __main__ - INFO - Searching for: machine learning tutorial (max 5 results)
2025-02-10 20:00:05 - __main__ - INFO - Found 5 videos
2025-02-10 20:00:06 - __main__ - INFO - Scraping video: abc123
2025-02-10 20:00:10 - __main__ - INFO - Successfully scraped abc123: Machine Learning Basics
...
```

### Example 2: Scrape Specific Video

```bash
python3 scraper.py --video dQw4w9WgXcQ
```

### Example 3: View Statistics

```bash
python3 scraper.py --stats
```

**Output:**
```
=== YouTube Scraper Statistics ===
Total videos scraped: 150
Videos with transcripts: 142
Unique channels: 45
Total transcript characters: 1,234,567
Transcript coverage: 94.7%
Total errors: 3

Request counts:
  Searches: 25
  Metadata: 150
  Transcripts: 142
```

---

## Python API Examples

### Example 4: Basic Python Usage

```python
from scraper import YouTubeScraper

# Initialize
scraper = YouTubeScraper()

# Search and scrape
results = scraper.search_and_scrape(
    query="AI tutorial",
    max_results=10
)

# Process results
for video in results:
    print(f"✓ {video['title']}")
    print(f"  Channel: {video['channel']}")
    print(f"  Views: {video['views']:,}")
    print()
```

### Example 5: Batch Processing

```python
from scraper import YouTubeScraper

scraper = YouTubeScraper()

# Define topics
topics = [
    "machine learning",
    "deep learning",
    "neural networks",
    "computer vision"
]

# Scrape each topic
for topic in topics:
    print(f"\nScraping: {topic}")
    results = scraper.search_and_scrape(topic, max_results=5)
    print(f"  Scraped {len(results)} videos")
```

### Example 6: Filter by Duration

```python
from scraper import YouTubeScraper

scraper = YouTubeScraper()

# Search for videos
videos = scraper.search_videos("python tutorial", max_results=20)

# Filter: only videos 10-30 minutes long
filtered = [
    v for v in videos
    if v.get('duration') and 600 <= v['duration'] <= 1800
]

print(f"Found {len(filtered)} videos (10-30 min)")

# Scrape filtered videos
for video in filtered:
    scraper.scrape_video(video['video_id'])
```

### Example 7: Error Handling

```python
from scraper import YouTubeScraper
import logging

logging.basicConfig(level=logging.INFO)

scraper = YouTubeScraper()

try:
    results = scraper.search_and_scrape("some topic", max_results=10)
    print(f"Success: {len(results)} videos scraped")
except Exception as e:
    print(f"Error: {e}")
    # Check failed videos
    failed = scraper.state_tracker.get_failed_videos()
    print(f"Failed videos: {len(failed)}")
```

### Example 8: Export Statistics

```python
from scraper import YouTubeScraper
import json

scraper = YouTubeScraper()

# Get stats
stats = scraper.get_stats()

# Export to JSON
with open('scraper_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("Stats exported to scraper_stats.json")
```

---

## Agent Integration

### Example 9: Moltbot Autonomous Research

```python
# In Moltbot's research module
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

def research_topic(topic: str, max_videos: int = 5):
    """
    Autonomous research for a topic.
    Scrapes YouTube videos and processes transcripts.
    """
    scraper = YouTubeScraper()

    # Search and scrape
    videos = scraper.search_and_scrape(topic, max_results=max_videos)

    if not videos:
        print(f"No videos found for: {topic}")
        return []

    # Process transcripts
    results = []
    for video in videos:
        video_id = video['video_id']
        transcript_path = scraper.memory_storage.get_transcript_path(video_id)

        if transcript_path.exists():
            transcript = transcript_path.read_text()

            # Extract insights (placeholder for AI processing)
            insights = extract_insights(transcript)
            results.append({
                'video': video,
                'insights': insights
            })

    return results

def extract_insights(transcript: str) -> list:
    """Extract key insights from transcript."""
    # Implement your AI processing here
    # This could use OpenAI API, local LLM, etc.
    return []
```

### Example 10: OpenClaw Hook

```python
# /opt/blackbox5/2-engine/runtime/hooks/youtube_scrape_hook.py
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

def on_new_goal(goal: dict):
    """
    Trigger YouTube scraping when new goal involves research.
    """
    goal_text = goal.get('title', '') + ' ' + goal.get('description', '')

    research_keywords = ['research', 'learn', 'study', 'investigate']

    if any(keyword in goal_text.lower() for keyword in research_keywords):
        print(f"Research goal detected: {goal['title']}")

        scraper = YouTubeScraper()

        # Extract topic from goal
        topic = goal['title']

        # Scrape relevant videos
        videos = scraper.search_and_scrape(topic, max_results=5)

        print(f"Scraped {len(videos)} videos for research")

        # Log activity
        goal['youtube_videos_scraped'] = len(videos)
        goal['youtube_scrape_time'] = datetime.now().isoformat()
```

### Example 11: ClawDBot Logging

```python
# In ClawDBot's activity tracker
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

def log_youtube_activity():
    """
    Log YouTube scraper statistics to ClawDBot.
    """
    scraper = YouTubeScraper()
    stats = scraper.get_stats()

    activity = {
        'type': 'youtube_scraper',
        'timestamp': datetime.now().isoformat(),
        'data': {
            'total_videos': stats['total_videos'],
            'videos_with_transcripts': stats['videos_with_transcripts'],
            'transcript_coverage': stats['transcript_coverage'],
            'total_errors': stats['total_errors']
        }
    }

    # Send to ClawDBot (implement your logging)
    clawdbot.log_activity(activity)

    return activity
```

---

## Automation Examples

### Example 12: Daily Scraping via Cron

```bash
# Edit crontab
crontab -e

# Add these lines:

# Every 6 hours, scrape scheduled queries
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --scheduled >> logs/cron.log 2>&1

# Daily at 8 AM, generate statistics report
0 8 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --stats >> logs/daily_stats.txt 2>&1

# Weekly on Sunday, backup database
0 2 * * 0 cp /opt/blackbox5/youtube-scraper/data/scraper.db /opt/blackbox5/youtube-scraper/backups/scraper_$(date +\%Y\%m\%d).db
```

### Example 13: Configuration-Based Automation

```yaml
# config/config.yaml
queries:
  # Morning research
  - query: "AI news today"
    max_results: 10
    schedule: "0 6 * * *"
    enabled: true

  # Midday tutorials
  - query: "python tutorial"
    max_results: 5
    schedule: "0 12 * * *"
    enabled: true

  # Evening deep dives
  - query: "machine learning"
    max_results: 10
    schedule: "0 18 * * *"
    enabled: true

  # Weekly topic
  - query: "computer vision"
    max_results: 20
    schedule: "0 10 * * 0"
    enabled: true
```

### Example 14: Python Scheduler

```python
from scraper import YouTubeScraper
import schedule
import time

scraper = YouTubeScraper()

def scrape_ai_news():
    """Scrape AI news every 6 hours."""
    print("Scraping AI news...")
    scraper.search_and_scrape("AI news", max_results=10)
    print("Done!")

def scrape_tutorials():
    """Scrape tutorials every 12 hours."""
    print("Scraping tutorials...")
    scraper.search_and_scrape("python tutorial", max_results=5)
    print("Done!")

# Schedule tasks
schedule.every(6).hours.do(scrape_ai_news)
schedule.every(12).hours.do(scrape_tutorials)
schedule.every().day.at("08:00").do(lambda: print(scraper.get_stats()))

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Advanced Patterns

### Example 15: Custom Transcript Processing

```python
from scraper import YouTubeScraper
from pathlib import Path

scraper = YouTubeScraper()

# Search for videos
videos = scraper.search_and_scrape("topic", max_results=5)

# Process each transcript
for video in videos:
    video_id = video['video_id']
    transcript_path = scraper.memory_storage.get_transcript_path(video_id)

    if transcript_path.exists():
        transcript = transcript_path.read_text()

        # Custom processing
        word_count = len(transcript.split())
        sentences = transcript.split('.')

        print(f"\n{video['title']}")
        print(f"  Words: {word_count:,}")
        print(f"  Sentences: {len(sentences)}")
        print(f"  Avg words/sentence: {word_count // len(sentences):.1f}")
```

### Example 16: Channel-Based Scraping

```python
from scraper import YouTubeScraper

scraper = YouTubeScraper()

# Get all videos from a channel (by scraping search results)
channel_name = "Some Channel"

# Search for channel
videos = scraper.search_videos(f"channel:{channel_name} tutorial", max_results=20)

print(f"Found {len(videos)} videos from {channel_name}")

# Scrape all
for video in videos:
    scraper.scrape_video(video['video_id'])
```

### Example 17: Transcript Search

```python
from scraper import YouTubeScraper
import re

scraper = YouTubeScraper()

# Get all scraped videos
all_videos = scraper.state_tracker.get_recent_videos(limit=100)

# Search transcripts for a keyword
keyword = "neural network"
results = []

for video in all_videos:
    video_id = video['video_id']
    transcript_path = scraper.memory_storage.get_transcript_path(video_id)

    if transcript_path.exists():
        transcript = transcript_path.read_text()

        if keyword.lower() in transcript.lower():
            results.append({
                'video': video,
                'matches': len(re.findall(re.escape(keyword), transcript, re.IGNORECASE))
            })

print(f"\nVideos mentioning '{keyword}':")
for result in sorted(results, key=lambda x: x['matches'], reverse=True)[:10]:
    print(f"  {result['video']['title']} ({result['matches']} matches)")
```

### Example 18: Retry Failed Scrapes

```python
from scraper import YouTubeScraper

scraper = YouTubeScraper()

# Get failed videos with < 3 retries
failed_videos = scraper.state_tracker.get_failed_videos(max_retries=3)

print(f"Found {len(failed_videos)} failed videos to retry")

# Retry each
for failed in failed_videos:
    video_id = failed['video_id']
    print(f"Retrying: {video_id}")

    scraper.scrape_video(
        video_id=video_id,
        force_rescrape=True
    )
```

### Example 19: Export to CSV

```python
from scraper import YouTubeScraper
import csv

scraper = YouTubeScraper()

# Get all videos
all_videos = scraper.state_tracker.get_recent_videos(limit=1000)

# Export to CSV
with open('videos.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Video ID', 'Title', 'Channel', 'Views',
        'Duration', 'Scraped At', 'Has Transcript'
    ])

    for video in all_videos:
        writer.writerow([
            video['video_id'],
            video['title'],
            video['channel'],
            video['views'],
            video['duration'],
            video['scraped_at'],
            video['has_transcript']
        ])

print(f"Exported {len(all_videos)} videos to videos.csv")
```

### Example 20: Multi-Language Scraping

```python
from scraper import YouTubeScraper

# Create scraper with different languages
scraper = YouTubeScraper()
scraper.transcript_extractor.languages = ['en', 'es', 'fr', 'auto']

# Search and scrape
results = scraper.search_and_scrape("topic", max_results=10)

# Check languages
for video in results:
    video_id = video['video_id']
    transcript_path = scraper.memory_storage.get_transcript_path(video_id)

    if transcript_path.exists():
        # Read metadata to check language
        metadata_path = scraper.memory_storage.get_metadata_path(video_id)
        if metadata_path.exists():
            import json
            metadata = json.loads(metadata_path.read_text())
            lang = metadata.get('transcript', {}).get('language', 'unknown')
            print(f"{video['title']}: {lang}")
```

---

## Tips

- **Rate limiting**: Don't scrape too fast, YouTube will block you
- **Deduplication**: The scraper tracks already-scraped videos
- **Error handling**: Failed videos are tracked for retry
- **Monitoring**: Check stats regularly with `--stats`
- **Backups**: Backup the SQLite database periodically

---

**For more examples, see README.md and docs/ARCHITECTURE.md**
