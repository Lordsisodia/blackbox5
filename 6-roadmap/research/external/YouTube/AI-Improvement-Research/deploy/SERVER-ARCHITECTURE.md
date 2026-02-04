# Server Architecture: 77.42.66.40

## Overview

Single Hetzner CX23 (upgraded to 8GB RAM) running:
1. **Moltbot** - Personal AI assistant (OpenClaw)
2. **RALF** - Autonomous agent loops (when fixed)
3. **Transcript Worker** - YouTube transcript fetching
4. **RSS Scraper** - YouTube RSS feed monitoring

## Resource Allocation (8GB RAM)

```
Total: 8GB
├── Moltbot: ~1GB
├── RALF Planner: ~1GB
├── RALF Executor: ~1GB
├── Transcript Worker: ~512MB
├── RSS Scraper: ~256MB (periodic)
├── System/OS: ~1GB
└── Free/Buffers: ~3GB
```

## Directory Structure

```
/opt/
├── moltbot/              # Moltbot personal assistant
│   ├── logs/
│   ├── skills/
│   └── ...
├── ralf/                 # BlackBox5 + RALF engine
│   ├── 2-engine/
│   ├── 5-project-memory/
│   └── bin/
└── youtube-pipeline/     # NEW: YouTube transcript pipeline
    ├── content/          # Transcripts output
    ├── state/            # Worker state
    └── repo/             # Git clone of AI-Improvement-Research
```

## Service Architecture

### 1. Moltbot (Already Running)
- **Service**: `moltbot.service`
- **Status**: Should be running
- **Start**: `systemctl start moltbot`

### 2. RALF (Fix Needed)
- **Services**: `ralf-planner.service`, `ralf-executor.service`
- **Status**: Has bug in executor, needs fix
- **Start**: `ralf-dual start` (after fix)

### 3. Transcript Worker (NEW)
- **Service**: `transcript-worker.service`
- **Function**: Continuously fetch transcripts from queue
- **Rate**: 200 videos/day, 2s delay between requests
- **Output**: `/opt/youtube-pipeline/content/`

### 4. RSS Scraper (NEW - Optional)
- **Service**: `youtube-rss.service` + `youtube-rss.timer`
- **Function**: Check RSS feeds every 4 hours
- **Action**: Add new videos to queue

## GitHub Integration Strategy

### Option A: GitHub Actions (Current - Keep)
- **RSS Scraping**: Stay on GitHub Actions (already working)
- **Leaderboard Generation**: Stay on GitHub Actions
- **Transcript Fetching**: Move to server (too heavy for Actions)

### Option B: Server-Only (Recommended)
- Move everything to server for consistency
- GitHub Actions only for PR validation

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ RSS Scraper  │  │  Leaderboard │  │   Queue Database     │  │
│  │ (Actions)    │  │  Generator   │  │   (queue.db)         │  │
│  └──────┬───────┘  └──────────────┘  └──────────┬───────────┘  │
└─────────┼────────────────────────────────────────┼──────────────┘
          │                                        │
          │ RSS feeds                              │ git pull/push
          ▼                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Server (77.42.66.40)                         │
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────────────────────┐   │
│  │  RSS Scraper    │    │      Transcript Worker            │   │
│  │  (optional)     │    │                                   │   │
│  │                 │    │  • Fetch from queue.db            │   │
│  │  • Check feeds  │    │  • youtube-transcript-api         │   │
│  │  • Add to queue │    │  • Save to content/               │   │
│  └────────┬────────┘    │  • Git commit/push                │   │
│           │             └──────────────────────────────────┘   │
│           │                              │                      │
│           │                              ▼                      │
│           │             ┌──────────────────────────────────┐   │
│           └────────────►│      SQLite Queue (queue.db)     │   │
│                         │                                   │   │
│                         │  • video_queue table              │   │
│                         │  • status: pending/fetching/      │   │
│                         │           completed/failed        │   │
│                         └──────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Git Sync (Cron)                        │   │
│  │                                                           │   │
│  │  Every hour:                                              │   │
│  │  1. git pull (get new queue.db, new videos)               │   │
│  │  2. git add content/transcripts/                          │   │
│  │  3. git commit -m "transcripts: $(date)"                  │   │
│  │  4. git push                                              │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Git Sync Strategy

### Why Git for Transcripts?

1. **Backup**: Transcripts are backed up to GitHub
2. **Version History**: Can see when each transcript was added
3. **Multi-Machine**: Can access transcripts anywhere
4. **Free Storage**: GitHub repos are free

### Sync Approach

**Option 1: Worker commits directly (Simple)**
- Worker commits after every batch
- Pros: Immediate backup
- Cons: Lots of small commits

**Option 2: Cron job hourly (Recommended)**
- Worker just saves files
- Cron job commits hourly
- Pros: Batched commits, cleaner history
- Cons: 1-hour delay for backup

## Implementation Plan

### Phase 1: Setup (Now)
1. Create `/opt/youtube-pipeline/` structure
2. Clone repo
3. Install dependencies
4. Copy queue.db

### Phase 2: Transcript Worker
1. Deploy worker service
2. Start fetching
3. Monitor logs

### Phase 3: Git Sync
1. Setup SSH key for GitHub
2. Create sync script
3. Add cron job

### Phase 4: RSS (Optional)
1. If RSS on Actions is unreliable, move to server
2. Otherwise keep on Actions

## Monitoring

```bash
# Check all services
systemctl status moltbot ralf-planner ralf-executor transcript-worker

# View logs
journalctl -u transcript-worker -f

# Queue status
python3 -c "from scripts.queue.manager import QueueManager; m = QueueManager(); print(m.get_stats())"

# Disk usage
df -h /opt/youtube-pipeline

# Git sync status
tail -f /opt/youtube-pipeline/logs/sync.log
```

## Security

- All services run as separate users where possible
- GitHub SSH key restricted to this repo only
- Firewall: Only SSH (22) and HTTP (80/443) open
- No inbound connections to transcript worker (outbound only)
