# AI Improvement Research - Architecture

**Date**: 2026-02-01
**Status**: Implemented
**Version**: 1.0

---

## First Principles

### What Problem Are We Solving?

1. **Information Overload**: Too much AI content, not enough time
2. **Context Loss**: Watching videos without capturing insights
3. **Action Gap**: Knowing about tools but not implementing them
4. **Temporal Blindness**: Not seeing trends emerge over time

### Core Design Decisions

| Decision | Rationale |
|----------|-----------|
| Separate collection from extraction | Server can be lightweight, extraction needs Claude |
| GitHub as data bus | Universal access, version control, no database needed |
| YAML frontmatter + Markdown | Machines parse YAML, humans read Markdown |
| Multi-dimensional organization | Time, area, topic - access data however you think about it |
| Timeline layers | Micro to meta - events to strategic insights |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                             │
├─────────────────────────────────────────────────────────────────┤
│  23 YouTube Channels (RSS)                                      │
│  - Tier 1 (8): Must watch                                       │
│  - Tier 2 (9): High quality                                     │
│  - Tier 3 (6): Filtered                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COLLECTION SERVER                           │
│                    (Railway - lightweight)                       │
├─────────────────────────────────────────────────────────────────┤
│  Cron: Every hour                                                │
│  1. Check RSS feeds                                              │
│  2. Download transcripts (yt-dlp)                                │
│  3. Store raw data                                               │
│  4. Push to GitHub                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GITHUB REPO                              │
│                    (blackbox5-data/youtube)                      │
├─────────────────────────────────────────────────────────────────┤
│  data/sources/        - Raw transcripts + metadata               │
│  timeline/events/     - Event log                                │
│  queue/pending/       - Awaiting extraction                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LOCAL PROCESSING                            │
│                     (Claude Code)                                │
├─────────────────────────────────────────────────────────────────┤
│  1. Pull from GitHub                                             │
│  2. Process pending queue                                        │
│  3. Extract insights (Claude)                                    │
│  4. Generate timeline layers                                     │
│  5. Push back to GitHub                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT / CONSUMPTION                        │
├─────────────────────────────────────────────────────────────────┤
│  extracted/           - Structured insights                      │
│  timeline/            - Daily, weekly, monthly                   │
│  reports/             - Actionable summaries                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Collection Server

**Purpose**: Lightweight data collector
**Location**: Railway (or similar)
**Runtime**: Python + cron

**Responsibilities**:
- Poll RSS feeds every hour
- Download transcripts with yt-dlp
- Store raw YAML files
- Push to GitHub
- Log events

**NOT responsible for**:
- LLM extraction (too expensive, needs Claude)
- Analysis (needs context)
- User interface

**Environment Variables**:
```bash
GITHUB_TOKEN=ghp_xxx
GITHUB_REPO=username/blackbox5-data
DATA_PATH=/app/data
```

### 2. GitHub Repository

**Purpose**: Universal data bus
**Structure**:
```
blackbox5-data/
└── youtube/
    └── AI-Improvement-Research/
        ├── data/sources/       # Raw data
        ├── timeline/events/    # Event log
        ├── queue/pending/      # Processing queue
        └── extracted/          # Processed data
```

**Why GitHub?**
- Free storage
- Version history
- Universal access
- No database to manage
- Claude can read directly

### 3. Local Processing

**Purpose**: Intelligence extraction
**Location**: Your machine + Claude Code
**Trigger**: Manual or scheduled

**Workflow**:
```bash
# Pull latest data
git pull

# Process queue
python scripts/extract.py --pending

# Generate reports
python scripts/report.py --daily

# Push results
git add .
git commit -m "extraction: $(date)"
git push
```

---

## Data Flow

### Stage 1: Collection

```yaml
# Server-side
Event: RSS poll detects new video
Action: Download transcript
Output: data/sources/{creator}/videos/{id}.yaml
Event Log: timeline/events/2025-02-01.yaml
Queue: queue/pending/{id}.yaml
Git Push: Automatic
```

### Stage 2: Extraction

```yaml
# Local-side
Input: queue/pending/{id}.yaml
Action: Claude extracts insights
Output: extracted/by_date/{date}/{id}.md
Updates:
  - timeline/daily/{date}.md
  - timeline/events/ (extraction_completed)
  - reports/actionable/todo-queue.yaml
Git Push: Manual or scheduled
```

### Stage 3: Synthesis

```yaml
# Local-side
Input: extracted/by_date/{date}/*.md
Action: Aggregate, detect themes
Output:
  - timeline/weekly/{week}.md
  - timeline/monthly/{month}.md
  - synthesized/{year}/{month}/
Git Push: Scheduled (weekly, monthly)
```

---

## Storage Architecture

### Multi-Dimensional Organization

**Time Dimension** (when did we learn this?)
```
timeline/
├── events/          # Micro - individual events
├── daily/           # Meso - daily digest
├── weekly/          # Macro - weekly synthesis
└── monthly/         # Meta - strategic view
```

**Area Dimension** (what domain?)
```
extracted/by_area/
├── ai-engineering/  # Building AI systems
├── claude-mcp/      # Claude-specific
├── coding-tools/    # Dev tools
├── ai-agents/       # Autonomous agents
├── ai-news/         # Industry news
└── business-strategy/ # AI business
```

**Topic Dimension** (what specific subject?)
```
extracted/by_topic/
├── vibe-coding/
├── mcp-servers/
├── ai-agents/
├── claude-code/
└── memory-management/
```

**Source Dimension** (who said it?)
```
data/sources/
├── david_ondrej/
├── simon_willison/
├── anthropic/
└── ...
```

### Why Multi-Dimensional?

Different questions need different access patterns:

| Question | Access Pattern |
|----------|----------------|
| "What did I learn today?" | `timeline/daily/2025-02-01.md` |
| "What about MCP servers?" | `extracted/by_topic/mcp-servers/` |
| "What did Simon Willison say?" | `data/sources/simon_willison/videos/` |
| "What should I implement?" | `reports/actionable/todo-queue.yaml` |
| "What's trending this week?" | `timeline/weekly/2025-W05.md` |

---

## Timeline Architecture

### Event Layer (Micro)

**Purpose**: Immutable log of everything that happened
**Format**: Append-only YAML
**Location**: `timeline/events/YYYY-MM-DD.yaml`

```yaml
events:
  - timestamp: 2025-02-01T08:15:00Z
    type: video_discovered
    source: david_ondrej
    video_id: XuSFUvUdvQA
    significance: high
```

### Daily Layer (Meso)

**Purpose**: Aggregated daily summary
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/daily/YYYY-MM-DD.md`

```yaml
---
date: 2025-02-01
summary:
  videos_collected: 12
  themes_emerging: 3
---

# Daily Digest - February 1, 2025

## Emerging Themes
...
```

### Weekly Layer (Macro)

**Purpose**: Pattern detection
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/weekly/YYYY-WNN.md`

### Monthly Layer (Meta)

**Purpose**: Strategic view
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/monthly/YYYY-MM.md`

---

## Processing Pipeline

### Ingest Pipeline

```python
# scripts/ingest.py

def ingest():
    for source in config.sources:
        # 1. Check RSS
        videos = check_rss(source.rss_feed)

        for video in videos:
            # 2. Download transcript
            transcript = download_transcript(video.id)

            # 3. Save raw data
            save_raw_data(source, video, transcript)

            # 4. Log event
            log_event('video_discovered', source, video)

            # 5. Add to queue
            add_to_queue(video.id)

    # 6. Push to GitHub
    git_push()
```

### Extract Pipeline

```python
# scripts/extract.py

def extract():
    for video_id in queue.pending:
        # 1. Load raw data
        raw = load_raw_data(video_id)

        # 2. Claude extraction
        extraction = claude_extract(raw)

        # 3. Save extraction
        save_extraction(video_id, extraction)

        # 4. Update timeline
        update_daily_digest(extraction)
        log_event('extraction_completed', video_id)

        # 5. Queue actions
        for action in extraction.actions:
            add_action(action)

    # 6. Push to GitHub
    git_push()
```

### Synthesize Pipeline

```python
# scripts/synthesize.py

def synthesize():
    # 1. Load week's extractions
    extractions = load_week_extractions()

    # 2. Detect themes
    themes = detect_themes(extractions)

    # 3. Generate weekly report
    generate_weekly_report(themes, extractions)

    # 4. Update knowledge graph
    update_knowledge_graph(themes)
```

---

## Scaling Considerations

### Current Scale
- 23 sources
- ~10-50 videos/day estimated
- ~100KB-1MB per video (transcript)
- ~5-10MB/day total

### Future Scale
- 100+ sources
- 100-500 videos/day
- Git LFS for large storage
- Database consideration at 10K+ videos

### Optimization Points
1. **Transcript storage**: Compress old transcripts
2. **Extraction caching**: Don't re-extract unchanged videos
3. **Incremental sync**: Only push changes
4. **Selective extraction**: Skip low-value content

---

## Security & Privacy

### API Keys
- YouTube Data API: Not needed (yt-dlp uses public endpoints)
- GitHub Token: Stored as Railway secret
- Claude API: Local only, not on server

### Data Sensitivity
- All data is public YouTube content
- No private user data
- Safe to store in GitHub (public or private repo)

---

## Monitoring & Observability

### Metrics to Track
- Videos collected per day
- Extraction success rate
- Queue depth
- Processing time
- Theme detection accuracy

### Alerts
- Queue depth > 100 (backlog)
- Failed extractions > 5 in a row
- Source offline > 7 days

---

## Future Enhancements

### Phase 2
- [ ] Reddit integration (r/LocalLLaMA, etc.)
- [ ] Twitter/X monitoring
- [ ] Podcast transcription
- [ ] Paper summaries (arXiv)

### Phase 3
- [ ] Web UI for browsing
- [ ] Search functionality
- [ ] Telegram bot notifications
- [ ] Automatic action tracking

### Phase 4
- [ ] Knowledge graph visualization
- [ ] Trend prediction
- [ ] Personalized recommendations
- [ ] Multi-user support

---

## Related Documents

- `TIMELINE-ARCHITECTURE.md` - Timeline system design
- `DATA-STRUCTURE.md` - File formats and schemas
- `../README.md` - User-facing documentation
