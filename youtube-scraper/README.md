# YouTube Scraper for BlackBox5

A robust YouTube video scraper that extracts metadata and transcripts, stores them in BlackBox5's memory system, and supports autonomous operation by AI agents.

## Features

- **Search & Scrape**: Search YouTube by query and extract video metadata + transcripts
- **Deduplication**: Tracks scraped videos in SQLite database to avoid duplicates
- **Rate Limiting**: Exponential backoff and request delays to avoid blocking
- **BlackBox5 Integration**: Stores transcripts in BlackBox5's knowledge system
- **Scheduled Scraping**: Run periodic scrapes via cron or config file
- **Agent-Friendly**: Easy integration with Moltbot, ClawDBot, and OpenClaw agents

## Installation

```bash
cd /opt/blackbox5/youtube-scraper
pip install -r requirements.txt
```

## Quick Start

### Search and Scrape Videos

```bash
# Search for machine learning tutorials
python3 scraper.py --query "machine learning tutorial python" --max-results 10

# Scrape a specific video
python3 scraper.py --video abc123

# Use verbose output
python3 scraper.py --query "AI agents" -v
```

### Run Scheduled Queries

Edit `config/config.yaml` to add your queries, then:

```bash
python3 scraper.py --config config/config.yaml --scheduled
```

### View Statistics

```bash
python3 scraper.py --stats
```

## Configuration

Create or edit `config/config.yaml`:

```yaml
scraper:
  max_videos_per_search: 20
  enable_video_download: false
  transcript_languages:
    - en
    - auto

rate_limits:
  search_delay: 5
  metadata_delay: 1
  transcript_delay: 2
  max_retries: 5

storage:
  sqlite_db: data/scraper.db
  transcripts_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts
  metadata_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/metadata

queries:
  - query: "machine learning tutorial"
    max_results: 10
    schedule: "0 */6 * * *"
    enabled: true

  - query: "autonomous AI agents"
    max_results: 5
    schedule: "0 2 * * *"
    enabled: true
```

## Usage

### Command Line

```bash
# Basic search
python3 scraper.py --query "topic" --max-results 10

# Force re-scrape existing videos
python3 scraper.py --query "topic" --force

# Run all scheduled queries from config
python3 scraper.py --config config/config.yaml --scheduled

# Show statistics
python3 scraper.py --stats
```

### Python API

```python
from scraper import YouTubeScraper

# Initialize
scraper = YouTubeScraper(
    config_path="config/config.yaml",
    sqlite_db="data/scraper.db"
)

# Search and scrape
results = scraper.search_and_scrape(
    query="machine learning tutorial",
    max_results=10
)

# Scrape specific video
video = scraper.scrape_video(video_id="abc123")

# Get statistics
stats = scraper.get_stats()
print(f"Total videos: {stats['total_videos']}")
```

### Agent Integration

#### From Moltbot

```python
# In Moltbot's research module
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

def research_topic(topic):
    scraper = YouTubeScraper()
    videos = scraper.search_and_scrape(topic, max_results=5)
    # Process transcripts...
    return videos
```

#### From OpenClaw Skill

Add to `/opt/blackbox5/.skills/youtube-scraper.json`:

```json
{
  "name": "youtube-scraper",
  "description": "Search and scrape YouTube videos for BlackBox5 knowledge base",
  "commands": [
    {
      "name": "scrape",
      "description": "Scrape YouTube videos by query",
      "exec": "/opt/blackbox5/youtube-scraper/scraper.py",
      "args": ["--query", "{{query}}", "--max-results", "{{max_results|10}}"]
    },
    {
      "name": "stats",
      "description": "Show scraper statistics",
      "exec": "/opt/blackbox5/youtube-scraper/scraper.py",
      "args": ["--stats"]
    }
  ]
}
```

## Storage

Scraped data is stored in:

```
/opt/blackbox5/5-project-memory/youtube-scraper/
├── knowledge/
│   ├── transcripts/       # Video transcripts (.md files)
│   ├── metadata/          # Video metadata (.json files)
│   └── summaries/         # Quick summaries for AI agents
├── data/
│   └── scraper.db        # SQLite database (deduplication)
└── logs/                  # Scraper logs
```

### Transcript Format

Each transcript is stored as a markdown file:

```markdown
# Video Title

## Video Information
- **Video ID:** `abc123`
- **Channel:** Channel Name
- **URL:** https://youtube.com/watch?v=abc123
- **Duration:** 15:32
- **Views:** 45,000
- **Published:** 2025-02-10

## Transcript Metadata
- **Type:** Auto-generated
- **Language:** en
- **Length:** 12,450 characters

## Transcript
[00:00] Speaker: Welcome to the tutorial...

[00:15] Speaker: Today we're going to learn about...
```

## Automation

### Cron Jobs

```bash
# Edit crontab
crontab -e

# Add scraper job (every 6 hours)
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --config config/config.yaml --scheduled >> logs/cron.log 2>&1

# Daily stats report
0 8 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --stats >> logs/daily_stats.txt
```

### BlackBox5 Hooks

Create a hook in `/opt/blackbox5/2-engine/runtime/hooks/`:

```python
def on_new_goal(goal):
    """Trigger scraping when new goal involves research"""
    if "research" in goal.lower():
        from youtube_scraper.scraper import YouTubeScraper
        scraper = YouTubeScraper()
        scraper.search_and_scrape(goal, max_results=5)
```

## Rate Limiting

The scraper implements several protections:

- **Request delays**: 5s between searches, 1s between metadata, 2s between transcripts
- **Exponential backoff**: Retry with increasing delays on failure
- **Request tracking**: Monitors request counts and timestamps
- **Random jitter**: ±30% jitter to avoid request patterns

These can be adjusted in `config.yaml`.

## Troubleshooting

### No Transcripts Available

Some videos don't have transcripts. The scraper will log this and continue.

### Rate Limit Errors

If you see "Too Many Requests" errors:
- Increase `search_delay` and `metadata_delay` in config
- Reduce concurrent workers
- Wait before retrying

### YouTube Updates Breaking Scraper

If the scraper stops working:
1. Update yt-dlp: `pip install --upgrade yt-dlp`
2. Check logs for specific errors
3. Report issues to yt-dlp GitHub

### Database Locked

If SQLite is locked:
```bash
# Wait a moment and retry
# Or check for other processes
lsof data/scraper.db
```

## Architecture

See `docs/ARCHITECTURE.md` for detailed system architecture and data flow.

## Research

See `docs/RESEARCH.md` for research on YouTube scraping options and best practices.

## Contributing

This is part of BlackBox5. Contributions welcome!

## License

Part of BlackBox5 project.

---

**Built for BlackBox5 Autonomous Agents** 🤖
