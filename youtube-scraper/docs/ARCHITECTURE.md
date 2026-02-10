# YouTube Scraper - Architecture Diagram

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BLACKBOX5 ECOSYSTEM                         │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Moltbot   │  │  ClawDBot   │  │  OpenClaw   │  │   Dashboard │ │
│  │ Autonomous  │  │   Logging   │  │Orchestrator │  │   UI/Web    │ │
│  │    Agent    │  │    Agent    │  │   Agent     │  │  Interface  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │                │       │
│         └────────────────┴────────────────┴────────────────┘       │
│                            │                                         │
│                   ┌────────▼────────┐                               │
│                   │  OpenClaw Skill │                               │
│                   │  (youtube-scraper)                              │
│                   └────────┬────────┘                               │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    YOUTUBE SCRAPER SYSTEM                            │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                      CLI / Python API                      │     │
│  │  - scraper.py (main entry point)                            │     │
│  │  - Command-line interface                                   │     │
│  │  - Programmatic API                                         │     │
│  └────────────────────────┬────────────────────────────────────┘     │
│                           │                                          │
│  ┌────────────────────────▼────────────────────────────────────┐     │
│  │                    Scraper Engine                            │     │
│  │  - Search manager (query processing)                          │     │
│  │  - Video processor (metadata extraction)                      │     │
│  │  - Transcript extractor                                      │     │
│  │  - Deduplication checker                                     │     │
│  └───────────┬──────────────────────┬───────────────────┬──────┘     │
│              │                      │                   │             │
│  ┌───────────▼──────┐    ┌─────────▼────────┐   ┌──────▼───────────┐ │
│  │   Rate Limiter   │    │   Retry Manager  │   │  State Tracker   │ │
│  │  - Exponential   │    │  - Backoff logic │   │  - SQLite DB     │ │
│  │    backoff       │    │  - Error handler │   │  - Progress log  │ │
│  │  - Request delays│    │  - Max retries   │   │  - Dedup check   │ │
│  └──────────────────┘    └──────────────────┘   └──────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
┌──────────────────┐ ┌────────────────┐ ┌──────────────────┐
│     yt-dlp       │ │transcript-api │ │   YouTube API    │
│  (Primary)       │ │  (Transcripts) │ │   (Optional)     │
│  - Video metadata│ │ - Auto/manual  │ │  - Official API  │
│  - Download      │ │   transcripts  │ │  - Reliable      │
│  - Subtitle files│ │ - Clean text   │ │  - Rate limited  │
└──────────────────┘ └────────────────┘ └──────────────────┘
            │                │                │
            └────────────────┴────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE LAYER                              │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    SQLite Database                           │     │
│  │  - scraped_videos table (deduplication)                      │     │
│  │  - scraping_stats table (metrics)                            │     │
│  │  - Indexes for fast lookups                                   │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                BlackBox5 Memory System                       │     │
│  │                                                               │     │
│  │  /opt/blackbox5/5-project-memory/youtube-scraper/            │     │
│  │  ├── knowledge/                                              │     │
│  │  │   ├── transcripts/          # Raw transcripts (.md)       │     │
│  │  │   ├── summaries/            # AI summaries                │     │
│  │  │   └── metadata/             # Video metadata cache        │     │
│  │  ├── decisions/                # Scraping decisions           │     │
│  │  ├── operations/               # Logs, schedules              │     │
│  │  └── tasks/                    # Scraping tasks              │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AUTOMATION LAYER                                │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  Cron Jobs   │  │   Hooks      │  │   Manual     │               │
│  │              │  │              │  │   Trigger    │               │
│  │ 0 */6 * * *  │  │ Autonomous   │  │  Dashboard   │               │
│  │   scrape     │  │  triggers    │  │   button     │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Search Flow

```
Agent/CLI
   │
   ├──> Search Query
   │     │
   │     ▼
   │  ┌──────────────┐
   │  │ Search Query │
   │  │   Processor  │
   │  └──────┬───────┘
   │         │
   │         ▼
   │  ┌──────────────┐
   │  │  Rate Limit  │<────── Check request rate
   │  │   Checker    │
   │  └──────┬───────┘
   │         │
   │         ▼
   │  ┌──────────────┐
   │  │  yt-dlp      │
   │  │  Search      │
   │  └──────┬───────┘
   │         │
   │         ▼
   │    [Results: Video IDs]
   │         │
   └─────────┼─────────┐
           │           │
           ▼           │
     ┌──────────┐       │
     │Dedup Check│─────┘
     │(SQLite DB)│
     └────┬─────┘
          │
          ▼
    [New Videos]
```

### 2. Scraping Flow

```
[New Video ID]
      │
      ▼
┌──────────────┐
│ Get Metadata │ (yt-dlp)
│              │
│ - title      │
│ - channel    │
│ - duration   │
│ - views      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Get Transcript│ (transcript-api)
│              │
│ - Auto-gen   │
│ - Manual     │
│ - Clean text │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Save to DB    │ (SQLite)
│ - Mark done  │
│ - Timestamp  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Save to      │ (BlackBox5 Memory)
│ Memory System│
│              │
│ - .md file   │
│ - Metadata   │
│ - Indexed    │
└──────┬───────┘
       │
       ▼
   [Complete]
```

### 3. Agent Integration Flow

```
┌──────────────┐
│   Agent      │
│  (Moltbot/   │
│   OpenClaw)  │
└──────┬───────┘
       │
       │ 1. Request scrape
       ▼
┌──────────────┐
│ YouTube      │
│ Scraper API  │
└──────┬───────┘
       │
       │ 2. Return results
       ▼
┌──────────────┐
│   Agent      │
│              │
│ 3. Process   │
│    transcripts│
└──────────────┘
```

---

## Component Details

### 1. Scraper Engine (`scraper.py`)

**Responsibilities:**
- Parse command-line arguments
- Load configuration
- Coordinate search and scraping
- Handle errors and retries
- Log progress

**Key Functions:**
```python
class YouTubeScraper:
    def __init__(config_path)
    def search(query, max_results)
    def scrape_video(video_id)
    def scrape_batch(video_ids)
    def save_to_memory(video_data, transcript)
    def run_scheduled_queries()
```

---

### 2. Rate Limiter (`rate_limiter.py`)

**Responsibilities:**
- Track request rates
- Enforce delays between requests
- Exponential backoff on errors
- Respect HTTP 429 responses

**Configuration:**
```yaml
rate_limits:
  search: 5        # seconds between searches
  metadata: 1      # seconds between metadata fetches
  transcript: 2    # seconds between transcripts
  max_retries: 5   # maximum retry attempts
  base_delay: 2    # base delay for backoff
```

---

### 3. State Tracker (`state_tracker.py`)

**Responsibilities:**
- Maintain SQLite database
- Check for duplicates
- Track scraping progress
- Store statistics

**Database Schema:**
```sql
CREATE TABLE scraped_videos (
  video_id TEXT PRIMARY KEY,
  title TEXT,
  channel TEXT,
  scraped_at TIMESTAMP,
  has_transcript BOOLEAN,
  transcript_length INTEGER,
  query_used TEXT
);

CREATE TABLE scraping_stats (
  date DATE PRIMARY KEY,
  videos_scraped INTEGER,
  transcripts_fetched INTEGER,
  errors INTEGER,
  total_time_seconds REAL
);
```

---

### 4. Memory Storage (`memory_storage.py`)

**Responsibilities:**
- Save transcripts to BlackBox5 memory
- Format as markdown
- Create metadata files
- Integrate with MemorySystem class

**File Structure:**
```
transcripts/
  ├── {video_id}.md           # Main transcript file
  └── metadata/
      └── {video_id}.json     # Video metadata
```

---

## Configuration

### YAML Config (`config/config.yaml`)

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
  base_delay: 2

storage:
  sqlite_db: data/scraper.db
  transcripts_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts
  metadata_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/metadata

logging:
  level: INFO
  log_dir: logs
  rotate_days: 7

queries:
  - query: "machine learning tutorial"
    max_results: 10
    schedule: "0 */6 * * *"
  - query: "AI agents autonomous"
    max_results: 5
    schedule: "0 2 * * *"

channels:
  - "channel_id_1"
  - "channel_id_2"
```

---

## Deployment

### Files to Create

```
/opt/blackbox5/youtube-scraper/
├── scraper.py                 # Main entry point
├── config/
│   └── config.yaml            # Configuration
├── lib/
│   ├── rate_limiter.py        # Rate limiting
│   ├── state_tracker.py       # Database management
│   ├── memory_storage.py      # BlackBox5 integration
│   └── transcript_extractor.py # Transcript handling
├── data/
│   └── scraper.db             # SQLite database
├── logs/                      # Log files
├── docs/
│   ├── RESEARCH.md            # Research document
│   └── ARCHITECTURE.md        # This file
└── README.md                  # Usage guide
```

### Cron Job Setup

```bash
# Edit crontab
crontab -e

# Add scraper job
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --config config/config.yaml >> logs/cron.log 2>&1
```

---

## Security Considerations

1. **API Keys:** Store in `/opt/blackbox5/.secrets/`
2. **Rate Limits:** Respect YouTube's ToS
3. **IP Protection:** Use proxies if heavy scraping
4. **Data Privacy:** Only store public data
5. **Access Control:** Restrict scraper to authorized agents

---

## Monitoring

### Metrics to Track

- Daily videos scraped
- Transcript success rate
- Error rate by type
- Average scraping time
- Rate limit hits
- Database size

### Alerts

- High error rate (>20% failures)
- Rate limit threshold hit
- Database corruption
- Disk space low

---

**Status:** ✅ Architecture defined
**Next:** Implementation
