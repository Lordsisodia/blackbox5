# YouTube Scraper Research Document

**Created:** 2025-02-10
**Purpose:** Research on YouTube scraping options and best practices for BlackBox5

---

## Executive Summary

After researching YouTube scraping approaches, we've identified the following optimal solution:

**Recommended Approach:** Hybrid system combining:
- **yt-dlp** for video metadata and download (robust, actively maintained)
- **youtube-transcript-api** for transcript extraction (cleaner than parsing subtitles)
- **BlackBox5 Memory System** for storage and deduplication
- **Rate limiting** via exponential backoff and request pooling

---

## 1. YouTube Scraping Tool Comparison

### Option 1: yt-dlp (RECOMMENDED)

**Pros:**
- Actively maintained (frequent updates to bypass YouTube changes)
- CLI tool with Python API
- Extracts comprehensive metadata (title, channel, views, upload date, etc.)
- Can download videos or extract subtitles/transcripts
- Handles age restrictions, private videos gracefully
- Supports rate limiting and retries
- Large community, battle-tested

**Cons:**
- YouTube actively fights scraping (requires frequent updates)
- API can break without warning
- May be flagged for heavy usage

**Use Case:** Primary tool for video metadata and optional video download

---

### Option 2: youtube-transcript-api (RECOMMENDED)

**Pros:**
- Specifically designed for transcripts
- Clean transcript output (no timestamp parsing needed)
- Handles auto-generated and manual transcripts
- Lightweight, focused API
- Works well with yt-dlp (get video ID, then fetch transcript)

**Cons:**
- Requires cookies for age-restricted videos
- Some videos may not have transcripts
- Limited to transcript data only

**Use Case:** Transcript extraction (already installed)

---

### Option 3: YouTube Data API v3

**Pros:**
- Official API (won't break)
- Reliable, documented
- Supports search, metadata, transcripts
- Rate-limited but predictable

**Cons:**
- Requires API key (quota limits)
- Cost for high-volume usage
- More complex setup
- Quota: 10,000 units/day (search = 100 units, video details = 1 unit)

**Pricing:**
- Free tier: 10,000 units/day
- Additional: $5 per million units

**Use Case:** Production-grade, high-volume scraping where API costs are acceptable

---

### Option 4: Invidious API

**Pros:**
- Open-source YouTube frontend
- No API key required
- Privacy-focused instances

**Cons:**
- Third-party service (uptime not guaranteed)
- May have rate limits
- Less reliable than direct methods
- Instance availability varies

**Use Case:** Backup option when yt-dlp fails

---

## 2. Integration with BlackBox5

### Memory System Integration

BlackBox5 provides a file-based memory system at `/opt/blackbox5/2-engine/.autonomous/lib/memory.py`:

```python
from memory import MemorySystem

memory = MemorySystem(project_name="youtube-scraper")
memory.record_insight("Found a useful pattern...", category="youtube_pattern")
```

**Storage Structure:**
```
/opt/blackbox5/5-project-memory/youtube-scraper/
├── decisions/          # Scraping decisions (e.g., "chose yt-dlp")
├── knowledge/          # Learned patterns from videos
│   ├── transcripts/     # Raw transcripts
│   ├── summaries/      # AI-generated summaries
│   └── metadata/        # Video metadata cache
├── operations/         # Scraping logs, schedules
└── tasks/              # Scraping tasks
```

---

### Agent Invocation Methods

#### Method 1: Direct CLI Call (Simplest)

```bash
# From any agent
/opt/blackbox5/youtube-scraper/scraper.py \
  --query "machine learning tutorial" \
  --max-results 10
```

#### Method 2: Python Import

```python
from youtube_scraper.scraper import YouTubeScraper

scraper = YouTubeScraper(config="/opt/blackbox5/youtube-scraper/config/config.yaml")
results = scraper.search_and_scrape("AI agents tutorial", max_results=5)
```

#### Method 3: OpenClaw Gateway Hook

Create a skill that exposes the scraper to all agents:

```yaml
# /opt/blackbox5/.skills/youtube-scraper.json
{
  "name": "youtube-scraper",
  "description": "Search and scrape YouTube videos",
  "commands": [
    {
      "name": "scrape",
      "description": "Scrape YouTube videos by query",
      "exec": "/opt/blackbox5/youtube-scraper/scraper.py",
      "args": ["--query", "{{query}}", "--max-results", "{{max_results}}"]
    }
  ]
}
```

---

## 3. Rate Limiting and Anti-Blocking Strategies

### YouTube's Anti-Scraping Measures

YouTube employs several protections:
- **IP-based rate limiting** (throttles after ~50-100 requests/minute)
- **Request pattern detection** (bot-like behavior)
- **Cookie/session tracking**
- **CAPTCHA challenges**
- **User-Agent checking**

---

### Best Practices

#### 1. Exponential Backoff

```python
import time
import random

def rate_limited_request(func, *args, **kwargs):
    """Wrapper with exponential backoff"""
    max_retries = 5
    base_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt) + random.uniform(0, 2)
            time.sleep(delay)
```

#### 2. Request Delays

- **Delay between searches:** 3-5 seconds minimum
- **Delay between video details:** 1-2 seconds
- **Delay between transcript fetches:** 2-3 seconds
- **Random jitter:** ±30% to avoid patterns

#### 3. Session Management

- Use cookies (yt-dlp auto-manages)
- Rotate User-Agent strings
- Limit concurrent requests (max 3-5)
- Respect 429 (Too Many Requests) responses

#### 4. Request Pooling

- **Batch operations:** Get metadata first, filter, then fetch transcripts
- **Deduplicate:** Don't re-scrape already processed videos
- **Priority queues:** Process important videos first

---

### Recommended Limits

| Operation | Rate | Concurrent |
|-----------|------|------------|
| Search queries | 1 per 5 sec | 1 |
| Video metadata | 3 per sec | 2 |
| Transcripts | 1 per 2 sec | 1 |
| Video download | 1 per 10 sec | 1 |

---

## 4. Resumability and Deduplication

### State Tracking

```python
# Track scraped videos
{
  "video_id": "abc123",
  "scraped_at": "2025-02-10T20:00:00Z",
  "has_transcript": true,
  "downloaded": false,
  "checksum": "md5hash"
}
```

### Deduplication Strategy

1. **Primary key:** YouTube video ID
2. **Store:** SQLite database for fast lookups
3. **Checksum:** Optional video file checksum
4. **Resume:** Check database before scraping

### Database Schema

```sql
CREATE TABLE videos (
  video_id TEXT PRIMARY KEY,
  title TEXT,
  channel TEXT,
  scraped_at TIMESTAMP,
  has_transcript BOOLEAN,
  transcript_length INTEGER,
  downloaded BOOLEAN,
  file_path TEXT,
  checksum TEXT
);

CREATE INDEX idx_scraped_at ON videos(scraped_at);
CREATE INDEX idx_channel ON videos(channel);
```

---

## 5. Automation Options

### Option 1: Cron Jobs (Recommended for periodic scraping)

```bash
# Every 6 hours, scrape predefined queries
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --config config/config.yaml

# Daily at 2 AM, scrape specific channels
0 2 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --channels "channel1,channel2"
```

### Option 2: BlackBox5 Autonomous Hooks

Create a hook in `/opt/blackbox5/2-engine/runtime/hooks/`:

```python
# youtube_scrape_hook.py
from youtube_scraper.scraper import YouTubeScraper

def on_new_goal(goal):
    """Trigger scraping when new goal involves research"""
    if "research" in goal.lower():
        scraper = YouTubeScraper()
        scraper.scrape_relevant_topics(goal)
```

### Option 3: Dashboard Manual Trigger

Add a button in the dashboard to trigger scraping:

```javascript
// Dashboard integration
fetch('/api/youtube-scrape', {
  method: 'POST',
  body: JSON.stringify({ query: "topic", max_results: 10 })
})
```

---

## 6. Logging and Monitoring

### Log Levels

- **INFO:** Scraping progress, videos found
- **WARN:** Rate limits hit, retries needed
- **ERROR:** Failed scrapes, API errors
- **DEBUG:** Request details, delays

### Log Location

```
/opt/blackbox5/youtube-scraper/logs/
├── scraper_2025-02-10.log        # Daily logs
├── errors.log                    # Error-only log
└── metrics.json                  # Scraping stats
```

### Metrics to Track

- Videos scraped (total, today, this week)
- Transcripts extracted
- Failed scrapes (with reasons)
- Average scrape time
- Rate limit hits
- API quota usage (if using YouTube API)

---

## 7. Storage Strategy for BlackBox5 Knowledge System

### Transcript Storage

Store transcripts as individual markdown files:

```
/opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/
├── abc123.md              # Video ID as filename
├── def456.md
└── ghi789.md
```

### Transcript Format

```markdown
# Video Title

**Video ID:** abc123
**Channel:** Channel Name
**Published:** 2025-02-10
**Duration:** 15:32
**Views:** 45,000
**URL:** https://youtube.com/watch?v=abc123

## Metadata

- Category: Technology
- Tags: ["machine learning", "AI", "tutorial"]
- Language: English
- Transcript Type: Auto-generated

## Summary

*(Optional: AI-generated summary)*

## Full Transcript

[00:00] Speaker: Welcome to the tutorial...

[00:15] Speaker: Today we're going to learn about...
```

### AI Integration

Transcripts can be:
- **Indexed** by BlackBox5 knowledge system
- **Summarized** by AI agents
- **Queried** for relevant information
- **Used** for training/fine-tuning

---

## 8. Integration with Existing Agents

### Moltbot Integration

Moltbot can invoke the scraper for autonomous research:

```python
# In Moltbot's research module
from youtube_scraper.scraper import YouTubeScraper

def research_topic(topic):
    scraper = YouTubeScraper()
    videos = scraper.search_and_scrape(topic, max_results=5)
    return summarize_transcripts(videos)
```

### ClawDBot Integration

ClawDBot can log scraping activities:

```python
# Log to ClawDBot's activity stream
clawdbot.log_activity("youtube_scraper", {
    "videos_scraped": len(results),
    "query": query,
    "timestamp": datetime.now().isoformat()
})
```

### OpenClaw Integration

OpenClaw orchestrator can schedule scraping:

```python
# OpenClaw autonomous scheduler
scheduler.add_task(
    name="youtube_scrape_daily",
    func=scrape_youtube_videos,
    schedule="0 2 * * *",  # Daily at 2 AM
    args=["query1", "query2"]
)
```

---

## 9. Cost Analysis

### yt-dlp + youtube-transcript-api

- **Cost:** Free (open-source)
- **Bandwidth:** Low (transcripts ~10-50KB per video)
- **Storage:** Minimal (text files)
- **Compute:** Low (text processing)

### YouTube Data API v3

- **Cost:** Free tier (10,000 units/day)
- **Video search:** 100 units/query
- **Video details:** 1 unit/video
- **Transcript:** Not directly supported (need other method)

**Estimated daily capacity with API:**
- 100 searches + 1000 videos = 20,000 units (needs paid tier)

---

## 10. Security and Privacy

### IP Protection

- Use residential proxies if heavy scraping (recommended for production)
- Respect YouTube's ToS
- Don't scrape private/restricted content

### Data Privacy

- Store only public data
- Don't store PII from transcripts
- Anonymize user mentions if necessary

### API Key Security

- Store API keys in `/opt/blackbox5/.secrets/`
- Never commit to git
- Use environment variables

---

## 11. Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BlackBox5 Ecosystem                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Moltbot    │  │  ClawDBot    │  │  OpenClaw    │       │
│  │  (Research)  │  │   (Logging)  │  │(Orchestration)│       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
│         └─────────────────┴─────────────────┘               │
│                           │                                   │
│                           ▼                                   │
│              ┌──────────────────────┐                        │
│              │  YouTube Scraper     │                        │
│              │  (Python Module)     │                        │
│              └──────────┬───────────┘                        │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         ▼               ▼               ▼                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   yt-dlp     │ │transcript-api│ │  SQLite DB   │        │
│  │  (Metadata)  │ │(Transcripts) │ │ (State)      │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌──────────────────────┐
              │  BlackBox5 Memory    │
              │  (Transcripts,       │
              │   Summaries,         │
              │   Knowledge Base)    │
              └──────────────────────┘
```

---

## 12. Next Steps

1. ✅ Research complete
2. ⏳ Build Python scraper with yt-dlp
3. ⏳ Implement rate limiting and retry logic
4. ⏳ Create SQLite deduplication system
5. ⏳ Integrate with BlackBox5 memory
6. ⏳ Add logging and metrics
7. ⏳ Create configuration system
8. ⏳ Build OpenClaw skill for agent access
9. ⏳ Set up cron jobs for automation
10. ⏳ Test with real YouTube searches
11. ⏳ Document usage for agents
12. ⏳ Deploy to VPS

---

## 13. References

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [BlackBox5 Documentation](/opt/blackbox5/1-docs/)
- [Rate Limiting Best Practices](https://developer.mozilla.org/en-US/docs/Web/HTTP/Rate_limiting)

---

**Document Status:** ✅ Complete
**Next Phase:** Implementation
