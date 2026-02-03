# Transcript Pipeline Action Plan

## Current State Analysis

### What Exists
- **RSS Scraper**: Hourly scraping via GitHub Actions (`.github/workflows/scrape.yml`)
- **Video Database**: 24 channels, 7,979 videos, 3,127 long-form (18+ min)
- **Ranking System**: AI-centric scoring with recency/duration/channel tiers
- **GitHub Actions**: Infrastructure for automation
- **Zero Transcripts**: 3,127 videos need transcripts fetched

### What's Missing
1. Queue management system
2. Rate-limited transcript worker
3. Transcript storage structure
4. Integration with existing workflows

---

## Phase 1: Queue Infrastructure (Agent 1)

**Goal**: Create SQLite queue to track transcript fetching status

**Files to Create**:
```
database/
├── queue.db                    # SQLite database
└── schema/
    └── queue_schema.sql        # Database schema

scripts/
├── queue/
│   ├── __init__.py
│   ├── database.py             # Queue DB operations
│   ├── manager.py              # Queue management
│   └── populate.py             # Initial population from videos
```

**Database Schema**:
```sql
CREATE TABLE video_queue (
    video_id TEXT PRIMARY KEY,
    channel_slug TEXT NOT NULL,
    title TEXT NOT NULL,
    upload_date TEXT,
    duration INTEGER,
    score REAL,                  -- AI ranking score
    priority TEXT,               -- P0, P1, P2, P3
    status TEXT,                 -- pending, fetching, completed, failed
    attempts INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_status_priority ON video_queue(status, priority, score DESC);
CREATE INDEX idx_channel ON video_queue(channel_slug);
```

**Tasks**:
- [ ] Create database schema
- [ ] Build queue manager (add, update, get next)
- [ ] Populate queue from existing videos
- [ ] Priority scoring integration

**Estimated Time**: 2 hours

---

## Phase 2: Transcript Worker (Agent 2)

**Goal**: Rate-limited transcript fetching with yt-dlp

**Files to Create**:
```
scripts/
├── worker/
│   ├── __init__.py
│   ├── transcript_fetcher.py   # yt-dlp wrapper
│   ├── rate_limiter.py         # Rate limiting logic
│   └── worker.py               # Main worker loop

content/
└── transcripts/                # Output directory
    └── {channel_slug}/
        └── {video_id}.md
```

**Rate Limits**:
- Max 50 videos/day (safe)
- 30-second delay between requests
- 3 retry attempts with exponential backoff
- Stop on 403 error (IP ban protection)

**Output Format** (Markdown):
```markdown
---
video_id: xxx
title: xxx
channel: xxx
upload_date: YYYYMMDD
duration: minutes
score: xxx
priority: P0
url: https://youtube.com/watch?v=xxx
fetched_at: ISO timestamp
---

# {title}

[Transcript content here...]
```

**Tasks**:
- [ ] Build yt-dlp wrapper with error handling
- [ ] Implement rate limiter
- [ ] Create MD output formatter
- [ ] Build worker loop (fetch next from queue)

**Estimated Time**: 3 hours

---

## Phase 3: GitHub Actions Integration (Agent 3)

**Goal**: Automate daily transcript fetching

**Files to Create/Modify**:
```
.github/
└── workflows/
    ├── fetch-transcripts.yml     # NEW: Daily transcript job
    └── scrape.yml                # MODIFY: Add queue population
```

**Workflow: fetch-transcripts.yml**:
```yaml
name: Fetch Transcripts

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install yt-dlp
      - name: Fetch transcripts (max 50)
        run: python scripts/worker/worker.py --limit 50
      - name: Commit transcripts
        run: |
          git config user.name "Transcript Bot"
          git config user.email "bot@example.com"
          git add content/transcripts/ database/queue.db
          git commit -m "transcripts: $(date -u '+%Y-%m-%d')" || echo "No changes"
          git push
```

**Modify scrape.yml**:
- Add step to populate queue after scraping
- Run `python scripts/queue/populate.py`

**Tasks**:
- [ ] Create fetch-transcripts workflow
- [ ] Modify scrape workflow
- [ ] Test GitHub Actions
- [ ] Document secrets/tokens needed

**Estimated Time**: 2 hours

---

## Phase 4: Integration & Testing (Agent 4)

**Goal**: Connect everything and validate

**Files to Create**:
```
scripts/
├── integration/
│   ├── __init__.py
│   ├── validate.py             # Validate transcripts
│   └── report.py               # Generate status report

docs/
└── TRANSCRIPT_PIPELINE.md      # Documentation
```

**Validation Checks**:
- [ ] Queue populated correctly
- [ ] Transcripts saved in right format
- [ ] Rate limiting works
- [ ] GitHub Actions run successfully
- [ ] No duplicate fetches

**Status Report**:
```
Transcript Pipeline Status
==========================
Total videos in queue: 3127
Completed: X
Pending: X
Failed: X

Today's fetches: X
Success rate: X%

Top channels by completion:
- david_ondrej: X/Y
- vrsen: X/Y
...
```

**Tasks**:
- [ ] Integration testing
- [ ] Validation scripts
- [ ] Status reporting
- [ ] Documentation

**Estimated Time**: 2 hours

---

## Agent Assignments

| Agent | Phase | Deliverables |
|-------|-------|--------------|
| Agent 1 | Phase 1 | Queue DB, manager, population script |
| Agent 2 | Phase 2 | Worker, fetcher, rate limiter |
| Agent 3 | Phase 3 | GitHub Actions workflows |
| Agent 4 | Phase 4 | Integration, testing, docs |

**Parallel Work**: Agents 1 & 2 can work simultaneously
**Dependencies**: Agent 3 needs 1 & 2, Agent 4 needs all

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1 | 2 hours | 2 hours |
| Phase 2 | 3 hours | 5 hours |
| Phase 3 | 2 hours | 7 hours |
| Phase 4 | 2 hours | 9 hours |

**Total: 9 hours** (can be parallelized to 5 hours with 2 agents)

---

## Success Criteria

- [ ] Queue populated with all 3,127 videos
- [ ] 50 transcripts fetched per day without errors
- [ ] All transcripts saved as MD with metadata
- [ ] GitHub Actions running daily
- [ ] Rate limiting preventing bans
- [ ] Priority system working (P0 fetched first)

---

## Next Steps After Completion

1. **AI Analysis Agent**: Process transcripts for key learnings
2. **Planning Agent**: Create implementation tasks
3. **Implementation Agent**: Execute tasks in Blackbox

The pipeline will feed into your existing agent system.
