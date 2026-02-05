# YouTube Transcript Analysis Pipeline - Plan Document

**Created:** 2026-02-05
**Status:** In Progress
**Objective:** Analyze 7,814 YouTube transcripts using BlackBox5's multi-agent analysis system

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Mac Mini       │────▶│  Sub-Agents      │────▶│  Analysis       │
│  (Transcripts)  │     │  (3-Loop Method) │     │  (Scored)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                           ┌──────────────────┐
│  GitHub Sync    │                           │  Insight         │
│  (Hourly)       │                           │  Aggregation     │
└─────────────────┘                           └──────────────────┘
```

---

## Components

### 1. Transcript Worker (Mac Mini)
**Location:** `youtube-pipeline@Shaans-Mac-mini`
**Status:** Running with Tor

- Fetches transcripts via `youtube-transcript-api`
- Uses Tor for IP rotation (bypasses YouTube blocks)
- Rate limited: ~300 videos/day
- Auto-commits to GitHub hourly

**Status:**
- Pending: 7,564
- Completed: 57
- Failed: 193
- Progress: 0.7%

**Access:**
```bash
ssh youtube-pipeline@4.tcp.eu.ngrok.io -p 14841
# Or via ngrok tunnel (get fresh URL from user)
```

---

### 2. Analysis Agents

#### Transcript Analyzer Agent
**File:** `.autonomous/agents/transcript-analyzer.md`

**3-Loop Method:**
1. **Surface Scan** - Metadata, claims, channel credibility
2. **Content Archaeology** - Topics, key claims, quality indicators
3. **Insight Extraction** - Scored learnings, recommendations

**Scoring Formula:**
```
Total = (Relevance × 3) + (Quality × 2) + (Actionability × 1)
Max: 35 points
```

**Output:** `.autonomous/output/analyses/{VIDEO_ID}-analysis.md`

#### Insight Aggregator Agent
**File:** `.autonomous/agents/insight-aggregator.md`

- Cross-video synthesis
- Pattern recognition
- Priority scoring
- Action item extraction

---

### 3. Work Queue

**File:** `.autonomous/queues/transcript-queue.yaml`

Tracks transcripts ready for analysis:
```yaml
queue:
  - video_id: aiLZMvMLYMg
    file: content/transcripts/david_ondrej/aiLZMvMLYMg.md
    status: pending|in_progress|completed
    priority: P0|P1|P2|P3
    assigned_worker: agent-id
    analysis_doc: path/to/analysis.md
```

---

### 4. Scripts

**Batch Runner:** `.autonomous/bin/analyze-transcripts.sh`
```bash
./analyze-transcripts.sh --batch-size 10 --priority P0
```

**Status Check:** `/Users/youtube-pipeline/youtube-pipeline/status.sh`
```bash
# Shows worker status, queue stats, transcript count
```

---

## How to Resume

### Step 1: Get ngrok Tunnel
On Mac Mini:
```bash
ngrok tcp 22
```
Share the tunnel URL (e.g., `tcp://4.tcp.eu.ngrok.io:14841`)

### Step 2: Connect and Check Status
```bash
ssh -i /tmp/macmini_key youtube-pipeline@<ngrok-url> -p <port>
/Users/youtube-pipeline/youtube-pipeline/status.sh
```

### Step 3: Spawn Analysis Sub-Agents
```bash
# Example: Analyze 3 transcripts in parallel
claude -f .autonomous/agents/transcript-analyzer.md --video-id aiLZMvMLYMg
claude -f .autonomous/agents/transcript-analyzer.md --video-id JRXAd-4sB8c
claude -f .autonomous/agents/transcript-analyzer.md --video-id Qh6jg3FymXY
```

### Step 4: Aggregate Insights
```bash
claude -f .autonomous/agents/insight-aggregator.md --batch 10
```

---

## Current Results

### Completed Analyses

| Video ID | Channel | Score | Key Insight |
|----------|---------|-------|-------------|
| aiLZMvMLYMg | David Ondrej | 22/30 | Kimi K2.5 agent swarm (100 parallel agents) |
| JRXAd-4sB8c | bijan_bowen | 22/30 | GLM-Image hybrid architecture |

### High-Value Findings
1. **Agent Swarm Pattern** - Built-in parallel orchestration without config
2. **Cost Efficiency** - 88% savings vs Claude Opus 4.5
3. **Hybrid Architecture** - Autoregressive + diffusion for images

### Action Items
- [ ] Test Kimi K2.5 for multi-agent workflows
- [ ] Benchmark cost-performance vs Claude
- [ ] Study GLM-Image architecture
- [ ] Run more sub-agents on remaining 55 transcripts

---

## File Locations

**Local (this machine):**
- Plan: `.autonomous/PLAN.md`
- Agents: `.autonomous/agents/`
- Analyses: `.autonomous/output/analyses/`
- Queue: `.autonomous/queues/transcript-queue.yaml`

**Mac Mini (youtube-pipeline):**
- Repo: `/Users/youtube-pipeline/youtube-pipeline/repo/`
- Transcripts: `content/transcripts/`
- Worker: `scripts/worker/worker.py`
- Status: `status.sh`

**GitHub:**
- Repo: `lordsisodia/youtube-ai-research`
- Transcripts: `content/transcripts/`
- Auto-sync: Hourly via cron

---

## Next Steps

1. **Short Term:**
   - Continue fetching transcripts (worker running)
   - Run analysis sub-agents on new transcripts
   - Sync analyses to GitHub

2. **Medium Term:**
   - Complete analysis of all 57+ transcripts
   - Run insight aggregation
   - Generate research report

3. **Long Term:**
   - Scale to full 7,814 video queue
   - Build automated analysis pipeline
   - Integrate with BlackBox5 knowledge system

---

## SSH Key

**Location:** `/tmp/macmini_key`
**Public key added to:** `youtube-pipeline@Mac-Mini` and `shaansisodia@Mac-Mini`

If key is lost, regenerate:
```bash
ssh-keygen -t ed25519 -f /tmp/macmini_key -N "" -C "claude"
# Then add public key to Mac Mini's ~/.ssh/authorized_keys
```

---

## Troubleshooting

**Worker stopped:**
```bash
# Restart worker
pkill -f worker.py
rm -f state/rate_limit.json
./run_worker.sh
```

**Tor not working:**
```bash
# Check Tor status
ps aux | grep tor

# Restart Tor
/opt/homebrew/opt/tor/bin/tor &
```

**Git sync failing:**
```bash
# Manual sync
./git_sync.sh
```

---

## Resources

- **BlackBox5 Analysis System:** See `2-engine/.autonomous/prompts/agents/`
- **BMAD Analyst Skill:** `2-engine/.autonomous/skills/bmad-analyst/`
- **Sample Analysis:** `.autonomous/output/analyses/aiLZMvMLYMg-analysis.md`
