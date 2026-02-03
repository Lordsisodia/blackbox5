# YouTube AI Improvement Research - System Usage Guide

**Last Updated**: 2026-02-02

---

## Quick Start

### 1. Collect New Videos

```bash
# Collect metadata for all sources (no rate limits)
python scripts/collect_metadata.py --all
```

### 2. Rank Videos

```bash
# Score videos by actionability, specificity, depth
python scripts/rank_v2.py
```

### 3. Download Transcripts

```bash
# Download transcripts for approved videos only
python scripts/download_transcripts.py

# Or with limit
python scripts/download_transcripts.py --limit 10
```

### 4. Extract Insights (V2)

```bash
# Extract all pending videos with multi-dimensional organization
python scripts/extract_v2.py

# Extract specific video
python scripts/extract_v2.py --video VIDEO_ID

# Extract only matching topic
python scripts/extract_v2.py --topic claude_code

# Dry run (preview without API calls)
python scripts/extract_v2.py --dry-run --limit 5
```

---

## Directory Structure

```
AI-Improvement-Research/
│
├── data/sources/          # Canonical video data + transcripts
├── queue/                 # Processing state
│   ├── pending/           # Videos awaiting extraction
│   ├── filtered/          # Low-ranked videos
│   └── completed/         # Successfully extracted
│
├── index/                 # Queryable databases
│   ├── videos.yaml        # Master video registry
│   ├── insights.yaml      # All extracted insights
│   ├── tools.yaml         # Tool catalog
│   ├── frameworks.yaml    # Framework catalog
│   └── links.yaml         # URL database
│
├── by_topic/              # Topic-organized extractions
│   ├── mcp/
│   ├── claude-code/
│   ├── ai-agents/
│   └── ...
│
├── by_date/               # Chronological organization
│   └── 2026/
│       └── 02-february/
│           ├── _key-sources.md    # Daily aggregation
│           └── 2026-02-02_*.md    # Individual videos
│
├── by_importance/         # Importance-ranked
│   ├── critical/          # [CRITICAL] content
│   ├── high/              # [HIGH] content
│   ├── medium/
│   └── low/
│
└── timeline/              # Temporal event log
    └── events/
```

---

## Importance Rankings

| Level | Bracket | When to Use |
|-------|---------|-------------|
| CRITICAL | **[CRITICAL]** | Game-changing insight, novel technique, major framework |
| HIGH | **[HIGH]** | Very valuable, actionable, specific tools/techniques |
| MEDIUM | **[MEDIUM]** | Useful context, good to know |
| LOW | **[LOW]** | Background info, general knowledge |

---

## Querying Data

### Find All Critical Insights
```bash
grep -r "\[CRITICAL\]" by_importance/critical/
```

### Find Videos by Topic
```bash
ls by_topic/mcp/
```

### Search Across All Content
```bash
grep -r "progressive disclosure" by_topic/
```

### Find Videos by Creator
```bash
grep -l "creator: Rasmus" by_topic/*/*.md
```

### Query Index Files
```bash
# List all tools mentioned
cat index/tools.yaml | grep "^  [A-Z]"

# Find all insights about MCP
python3 -c "import yaml; d=yaml.safe_load(open('index/insights.yaml')); [print(i['content']) for i in d['insights'] if 'mcp' in i.get('topics', [])]"
```

---

## Daily Workflow

### Morning: Collect
```bash
python scripts/collect_metadata.py --all
python scripts/rank_v2.py
```

### Afternoon: Download (respect rate limits)
```bash
python scripts/download_transcripts.py --limit 5
```

### Evening: Extract
```bash
python scripts/extract_v2.py --limit 3
```

---

## Current Status

- **Total videos collected**: 63
- **Videos with transcripts**: 32
- **Videos extracted (V2)**: 1
- **Pending extraction**: 31
- **Blocked (need proxy)**: 30 (in_the_world_of_ai: 15, vrsen: 15)

---

## Scripts Reference

| Script | Purpose | Speed | Cost |
|--------|---------|-------|------|
| `collect_metadata.py` | Get video metadata | Fast | Free |
| `rank_v2.py` | Score videos 0-100 | Fast | Free |
| `download_transcripts.py` | Get transcripts | Slow | Free |
| `extract_v2.py` | Extract insights with Claude | Medium | Claude API |

---

## Architecture

### 4-Stage Pipeline

```
Stage 1: collect_metadata.py
    → data/sources/{creator}/videos/{id}.yaml

Stage 2: rank_v2.py
    → queue/pending/{id}.yaml (with scores)

Stage 3: download_transcripts.py
    → Updates data/sources/ with transcript

Stage 4: extract_v2.py
    → by_topic/{topic}/{date}_{id}.md
    → by_date/{year}/{month}/{date}_{id}.md
    → index/*.yaml (all indexes)
    → by_date/{year}/{month}/_key-sources.md
```

### Data Flow

Each video flows through the system once:
1. Metadata collected (fast, free)
2. Ranked by value (fast, free)
3. Transcript downloaded (slow, rate-limited)
4. Insights extracted (API cost, one-time)

After extraction, insights live forever in:
- Topic folders (for browsing)
- Date folders (for timeline)
- Importance folders (for prioritization)
- Index files (for querying)

---

## Cost Considerations

### Free Operations
- Metadata collection
- Video ranking
- Transcript download (with rate limits)

### Paid Operations (Claude API)
- Insight extraction: ~$0.01-0.03 per video
- 31 videos pending: ~$0.31-0.93 total

### Rate Limits
- YouTube transcript API: ~30-50 videos/day per IP
- Solution: Residential proxy (Webshare free tier: 10 proxies, 1GB/month)

---

## Troubleshooting

### No videos ready for extraction
```bash
# Check transcript status
python3 -c "import yaml; from pathlib import Path;
for f in Path('data/sources').rglob('*.yaml'):
    d=yaml.safe_load(open(f));
    t=d.get('transcript',{}).get('full_text','');
    if len(t)>100: print(f'{f.parent.name}/{f.stem}: {len(t)} chars')"
```

### Transcript download blocked
- Wait 24 hours (ban resets)
- Use VPN to rotate IP
- Sign up for Webshare residential proxy

### Extraction failed
- Check Claude API key is set
- Check video has transcript
- Try with `--dry-run` first

---

## Files Generated

### Per Video
- `by_topic/{topic}/{date}_{video_id}.md` (multiple if multiple topics)
- `by_date/{year}/{month}/{date}_{video_id}.md`
- `by_importance/{level}/{date}_{video_id}.md` (if critical/high)

### Daily
- `by_date/{year}/{month}/_key-sources.md`

### Index (Updated Incrementally)
- `index/videos.yaml`
- `index/insights.yaml`
- `index/tools.yaml`
- `index/frameworks.yaml`
- `index/links.yaml`
