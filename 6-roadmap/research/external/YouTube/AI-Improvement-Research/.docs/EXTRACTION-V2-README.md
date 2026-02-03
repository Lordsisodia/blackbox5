# Extraction System V2 - Multi-Dimensional Organization

**Date**: 2026-02-02
**Status**: Implemented and Tested

---

## What's New in V2

### 1. Importance Rankings

Every insight is ranked with importance brackets:

- **[CRITICAL]** - Game-changing insight, novel technique, major framework
- **[HIGH]** - Very valuable, actionable, specific tools/techniques
- **[MEDIUM]** - Useful context, good to know
- **[LOW]** - Background info, general knowledge

### 2. Multi-Dimensional Output

Each video extraction is saved to multiple locations simultaneously:

| Location | Purpose | Example Path |
|----------|---------|--------------|
| `by_topic/{topic}/` | Find all content about MCP, Claude Code, etc. | `by_topic/mcp/2026-02-02_videoId.md` |
| `by_date/{year}/{month}/` | Chronological browsing | `by_date/2026/02-february/2026-02-02_videoId.md` |
| `by_importance/{level}/` | Only critical/high importance content | `by_importance/high/2026-02-02_videoId.md` |
| `index/` | Queryable database files | `index/videos.yaml`, `index/insights.yaml` |

### 3. Daily Key Sources

Every day, a `_key-sources.md` file is generated aggregating:
- All links found that day (ranked by importance)
- All frameworks discovered (ranked by importance)
- All tools mentioned (ranked by importance)
- All videos processed

### 4. Queryable Index

Structured YAML files for fast lookups:
- `index/videos.yaml` - Master video registry with locations
- `index/insights.yaml` - Every insight with importance, topics, tools
- `index/tools.yaml` - Tool catalog with mention counts
- `index/frameworks.yaml` - Framework/pattern catalog
- `index/links.yaml` - All URLs mentioned across videos

---

## Directory Structure

```
AI-Improvement-Research/
│
├── index/                          # Queryable indexes
│   ├── videos.yaml                 # Master video registry
│   ├── insights.yaml               # All insights (queryable)
│   ├── tools.yaml                  # Tool catalog
│   ├── frameworks.yaml             # Framework catalog
│   └── links.yaml                  # URL database
│
├── by_topic/                       # Topic-based organization
│   ├── mcp/
│   │   ├── _index.yaml             # Topic metadata
│   │   └── 2026-02-02_videoId.md   # Individual extractions
│   ├── claude-code/
│   ├── ai-agents/
│   └── ...
│
├── by_date/                        # Chronological organization
│   └── 2026/
│       └── 02-february/
│           ├── _key-sources.md     # Daily aggregation
│           └── 2026-02-02_videoId.md
│
├── by_importance/                  # Importance-ranked
│   ├── critical/                   # [CRITICAL] content only
│   ├── high/                       # [HIGH] content only
│   ├── medium/
│   └── low/
│
└── data/sources/                   # Canonical source (unchanged)
    └── {creator}/
        └── videos/
            └── {video_id}.yaml
```

---

## Usage

### Extract All Pending Videos

```bash
python scripts/extract_v2.py
```

### Extract Specific Video

```bash
python scripts/extract_v2.py --video VIDEO_ID
```

### Extract Only Videos Matching Topic

```bash
python scripts/extract_v2.py --topic claude_code
```

### Dry Run (See what would be extracted)

```bash
python scripts/extract_v2.py --dry-run --limit 5
```

### Limit Number of Videos

```bash
python scripts/extract_v2.py --limit 10
```

---

## Output Format

### Markdown Files (by_topic, by_date, by_importance)

```markdown
---
video_id: xxx
title: "Video Title"
creator: Creator Name
creator_tier: 1
url: https://youtube.com/watch?v=xxx
published_at: YYYYMMDD
duration: seconds
view_count: N
topics: [topic1, topic2]
overall_importance: HIGH
tools_mentioned:
  - Tool 1
  - Tool 2
frameworks:
  - Framework 1
difficulty: intermediate
extracted_at: ISO timestamp
---

# [HIGH] Video Title

**Creator:** Name
**Video:** [URL](URL)
**Published:** Date
**Overall Importance:** [HIGH]

## Summary

Brief overview...

## Key Insights

**[CRITICAL]** This is a game-changing insight...

**[HIGH]** This is very valuable...

**[MEDIUM]** This is useful context...

## Frameworks & Patterns

### [CRITICAL] Framework Name
**Type:** architecture
Description...

**Components:**
- Component 1
- Component 2

## Tools Covered

### [HIGH] Tool Name
Description...

**Use Case:** How it's used...

## Techniques

### [HIGH] Technique Name
Description...

**Steps:**
1. Step one
2. Step two

## Resources Mentioned

**[HIGH]** [Resource Title](URL) - Description

## Full Transcript
<details>
<summary>Click to expand</summary>
...
</details>
```

---

## Querying the Data

### Find All Critical Insights

```bash
grep -r "\[CRITICAL\]" by_importance/critical/ | head -20
```

### Find All Videos About MCP

```bash
ls by_topic/mcp/
```

### Find All Tools Mentioned

```bash
cat index/tools.yaml | grep "^  [A-Z]"
```

### Find Videos by Creator

```bash
grep -l "creator: Rasmus" by_topic/*/*.md
```

### Search Across All Content

```bash
grep -r "progressive disclosure" by_topic/
```

---

## Data Flow

```
Video with Transcript
        ↓
   extract_v2.py
        ↓
    ├─→ Claude API (extracts with importance rankings)
    ├─→ by_topic/{topic}/{date}_{id}.md
    ├─→ by_date/{year}/{month}/{date}_{id}.md
    ├─→ by_importance/{level}/{date}_{id}.md (if critical/high)
    ├─→ index/videos.yaml (update)
    ├─→ index/insights.yaml (append)
    ├─→ index/tools.yaml (append/update)
    ├─→ index/frameworks.yaml (append/update)
    ├─→ index/links.yaml (append)
    └─→ by_date/{year}/{month}/_key-sources.md (daily aggregation)
```

---

## Benefits

1. **No Data Loss** - Insights live in multiple places
2. **Multiple Access Patterns** - Browse by topic, date, or importance
3. **Queryable** - Index files enable fast searches
4. **Git-Friendly** - All text-based, version controlled
5. **Claude-Optimized** - Structured for agent consumption
6. **Daily Aggregation** - `_key-sources.md` gives daily overview

---

## Migration from V1

V1 extractions in `output/` are preserved. New extractions use V2 structure.

To re-extract a V1 video with V2:
```bash
python scripts/extract_v2.py --video VIDEO_ID
```

---

## Current Status

- **Videos collected**: 63
- **Videos with transcripts**: 32
- **Videos extracted (V2)**: 1 (FsDYk0WqBt0)
- **Pending extraction**: 31

---

## Next Steps

1. Run extraction on all 31 pending videos
2. Build synthesis layer for weekly/monthly aggregation
3. Create query interface for index files
