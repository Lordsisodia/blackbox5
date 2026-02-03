# Data Architecture V2 - Multi-Dimensional Organization

**Date**: 2026-02-02
**Status**: Design Phase

---

## Core Principle

**Data lives in multiple places simultaneously** - each optimized for different access patterns:

1. **Canonical Source** (data/sources/) - Immutable raw data
2. **Query Index** (index/) - Fast lookups, cross-references
3. **Topic Views** (by_topic/) - Organized by subject matter
4. **Timeline Views** (by_date/) - Chronological organization
5. **Importance Views** (by_importance/) - Ranked by value
6. **Synthesized** (synthesized/) - Aggregated intelligence

---

## Directory Structure

```
AI-Improvement-Research/
│
├── data/
│   └── sources/                    # Canonical source (immutable)
│       └── {creator}/
│           └── videos/
│               └── {video_id}.yaml
│
├── index/                          # Query-optimized indexes
│   ├── videos.yaml                 # Master video index by ID
│   ├── tools.yaml                  # All tools mentioned across videos
│   ├── frameworks.yaml             # AI frameworks catalog
│   ├── links.yaml                  # All URLs mentioned
│   └── insights.yaml               # All extracted insights (queryable)
│
├── by_topic/                       # Topic-based organization
│   ├── claude-code/
│   │   ├── _index.yaml             # Topic metadata + all videos
│   │   └── {date}_{video_id}.md    # Individual extractions
│   ├── mcp/
│   ├── ai-agents/
│   └── ...
│
├── by_date/                        # Chronological organization
│   ├── 2026/
│   │   ├── 02-february/
│   │   │   ├── _summary.md         # Daily summary of all sources
│   │   │   ├── _key-sources.md     # All key links/frameworks found today
│   │   │   └── {video_id}.md       # Individual extractions
│   │   └── 03-march/
│   └── 2027/
│
├── by_importance/                  # Importance-ranked organization
│   ├── critical/                   # [CRITICAL] - Game-changing insights
│   ├── high/                       # [HIGH] - Very valuable
│   ├── medium/                     # [MEDIUM] - Useful context
│   └── low/                        # [LOW] - Background info
│
├── synthesized/                    # Aggregated intelligence
│   ├── weekly/                     # Week-by-week synthesis
│   ├── monthly/                    # Month-by-month synthesis
│   └── themes/                     # Cross-cutting themes
│
└── timeline/                       # Temporal event log
    ├── events/                     # Raw events (existing)
    ├── daily/                      # Daily digests
    ├── weekly/                     # Weekly summaries
    └── monthly/                    # Monthly retrospectives
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COLLECTION PIPELINE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

Stage 1: collect_metadata.py
    ↓
data/sources/{creator}/videos/{id}.yaml  (canonical source)
    ↓
Stage 2: rank_v2.py
    ↓
queue/pending/{id}.yaml  (processing state)
    ↓
Stage 3: download_transcripts.py
    ↓
Update data/sources/ with transcript
    ↓
Stage 4: extract.py (NEW VERSION)
    ↓
    ├─→ by_topic/{topic}/{date}_{id}.md
    ├─→ by_date/{year}/{month}/{date}_{id}.md
    ├─→ by_importance/{level}/{date}_{id}.md
    ├─→ index/videos.yaml (update entry)
    ├─→ index/tools.yaml (append new tools)
    ├─→ index/frameworks.yaml (append new frameworks)
    ├─→ index/links.yaml (append new links)
    ├─→ index/insights.yaml (append structured insights)
    └─→ by_date/{year}/{month}/_key-sources.md (daily aggregation)
    ↓
Stage 5: synthesize.py (NEW)
    ↓
    ├─→ by_date/{year}/{month}/_summary.md (daily synthesis)
    ├─→ synthesized/weekly/{week}.md (weekly aggregation)
    ├─→ synthesized/monthly/{month}.md (monthly aggregation)
    └─→ timeline/{daily,weekly,monthly}/ (timeline views)
```

---

## File Formats

### 1. Canonical Source (data/sources/)

Unchanged - stores raw video data + transcript.

### 2. Index Files (index/)

**index/videos.yaml** - Master video registry:
```yaml
videos:
  TJkxAJS34CQ:
    title: "Ralph Wiggum killed programming"
    creator: Rasmus
    creator_tier: 1
    published_at: "2026-01-16"
    extracted_at: "2026-02-02T07:25:36"
    topics: [claude_code, ai_agents]
    importance: critical  # [CRITICAL], [HIGH], [MEDIUM], [LOW]
    tools_mentioned: [Claude Code, Ralph Plugin, TypeScript]
    frameworks: [Ralph Wiggum Pattern]
    has_code_examples: true
    locations:
      by_topic: [by_topic/claude-code/2026-02-02_TJkxAJS34CQ.md]
      by_date: [by_date/2026/02-february/2026-02-02_TJkxAJS34CQ.md]
      by_importance: [by_importance/critical/2026-02-02_TJkxAJS34CQ.md]
```

**index/insights.yaml** - Queryable insight database:
```yaml
insights:
  - id: TJkxAJS34CQ-001
    video_id: TJkxAJS34CQ
    type: technique  # technique | tool | concept | resource
    importance: critical
    content: "Ralph Wiggum is a technique for running AI coding agents in an autonomous loop"
    topics: [claude_code, ai_agents]
    tools: [Claude Code]
    source_timestamp: "00:00:30"
    extracted_at: "2026-02-02T07:25:36"

  - id: TJkxAJS34CQ-002
    video_id: TJkxAJS34CQ
    type: tool
    importance: high
    content: "Two essential files: prd.md and progress.txt"
    topics: [claude_code]
    tools: []
    source_timestamp: "00:01:15"
    extracted_at: "2026-02-02T07:25:36"
```

**index/tools.yaml** - Tool catalog:
```yaml
tools:
  Claude Code:
    mentions: 15
    videos: [TJkxAJS34CQ, abc123, def456]
    first_seen: "2026-02-02"
    last_seen: "2026-02-02"
    description: "Anthropic's coding agent/IDE"
    categories: [coding-tools, ai-agents]

  Ralph Plugin:
    mentions: 3
    videos: [TJkxAJS34CQ]
    first_seen: "2026-02-02"
    last_seen: "2026-02-02"
    description: "Official Anthropic plugin for Ralph Wiggum workflow"
    categories: [claude-code, ai-agents]
```

**index/frameworks.yaml** - Framework/pattern catalog:
```yaml
frameworks:
  Ralph Wiggum Pattern:
    type: technique
    videos: [TJkxAJS34CQ]
    description: "Autonomous AI coding pattern with PRD-driven development"
    components: [prd.md, progress.txt, loop script]
    related_tools: [Claude Code, Open Code]
    first_seen: "2026-02-02"
```

**index/links.yaml** - URL database:
```yaml
links:
  - url: "https://rasmic.link/voice-agent"
    title: "Voice Agent server"
    source_video: TJkxAJS34CQ
    source_creator: Rasmus
    discovered_at: "2026-02-02"
    category: resource
    topic: voice-ai
```

### 3. Topic Views (by_topic/)

**by_topic/claude-code/_index.yaml**:
```yaml
topic: claude_code
name: "Claude Code"
description: "Content about Claude Code tool and workflows"
total_videos: 5
total_insights: 23
tools_covered: [Claude Code, Ralph Plugin]
last_updated: "2026-02-02T07:25:36"
videos:
  - id: TJkxAJS34CQ
    title: "Ralph Wiggum killed programming"
    importance: critical
    extracted_at: "2026-02-02"
    file: "2026-02-02_TJkxAJS34CQ.md"
```

**by_topic/claude-code/2026-02-02_TJkxAJS34CQ.md**:
```markdown
---
video_id: TJkxAJS34CQ
importance: critical
topics: [claude_code]
extracted_at: "2026-02-02T07:25:36"
---

# [CRITICAL] Ralph Wiggum killed programming

**Creator:** Rasmus
**Video:** [Link](https://youtube.com/watch?v=TJkxAJS34CQ)
**Published:** 2026-01-16

## [CRITICAL] Key Insights

**[CRITICAL]** Ralph Wiggum is a technique for running AI coding agents in an autonomous loop to build applications without constant human intervention.

**[HIGH]** The two essential files are prd.md (defines end state) and progress.txt (tracks completed work).

**[HIGH]** Plan quality dramatically impacts output quality—detailed, precise PRDs produce better software.

**[MEDIUM]** Running with 'fast' flag skips tests and linting for rapid feature building.

## [CRITICAL] Techniques

### Ralph Wiggum Loop
**Importance:** [CRITICAL]
Autonomous AI coding pattern where agent continuously builds features until PRD completion.

**Steps:**
1. Create detailed PRD.md with phased implementation
2. Create empty progress.txt file
3. Run Ralph.sh script to start loop
4. Agent reads PRD and progress.txt each iteration
5. Agent implements next unchecked feature
6. Loop continues until all features complete

## Tools Covered

**[CRITICAL]** Claude Code - Anthropic's coding agent/IDE
**[HIGH]** Ralph Plugin - Official plugin for Ralph workflow
**[MEDIUM]** TypeScript - For type safety

## Code Examples

```bash
# Ralph.sh - Normal mode
# - Generates tests after each feature
# - Runs tests and verifies passing
# - Runs TypeScript linter
```

## Resources

- [Voice Agent server](https://rasmic.link/voice-agent)
```

### 4. Date Views (by_date/)

**by_date/2026/02-february/_key-sources.md**:
```markdown
# Key Sources - February 2, 2026

**Generated:** 2026-02-02T07:25:36
**Videos Processed:** 1

## Key Links Found Today

### [CRITICAL]
- [Voice Agent server](https://rasmic.link/voice-agent) - From Rasmus video

## Key AI Frameworks Found Today

### [CRITICAL]
- **Ralph Wiggum Pattern** - Autonomous AI coding pattern
  - Components: prd.md, progress.txt, loop script
  - Source: TJkxAJS34CQ (Rasmus)

## Key Tools Found Today

### [CRITICAL]
- **Claude Code** - Anthropic's coding agent
- **Ralph Plugin** - Official Ralph workflow plugin

### [HIGH]
- **Open Code** - Alternative AI coding agent
- **TypeScript** - Typed JavaScript

## Videos Processed

1. **[CRITICAL]** Ralph Wiggum killed programming (Rasmus)
   - Topics: claude_code
   - Tools: Claude Code, Ralph Plugin, TypeScript
   - File: `2026-02-02_TJkxAJS34CQ.md`
```

**by_date/2026/02-february/2026-02-02_TJkxAJS34CQ.md**:
(Same content as by_topic version, just organized by date)

### 5. Importance Views (by_importance/)

**by_importance/critical/2026-02-02_TJkxAJS34CQ.md**:
(Same content, but only includes [CRITICAL] and [HIGH] sections)

---

## Importance Ranking System

| Level | Bracket | Criteria | Action |
|-------|---------|----------|--------|
| CRITICAL | **[CRITICAL]** | Game-changing insight, novel technique, major framework | Immediate action recommended |
| HIGH | **[HIGH]** | Very valuable, actionable, specific tools/techniques | Add to learning queue |
| MEDIUM | **[MEDIUM]** | Useful context, good to know | Reference when needed |
| LOW | **[LOW]** | Background info, general knowledge | Archive for search |

---

## Implementation Plan

### Phase 1: Index Layer
1. Create `index/` directory structure
2. Build `index/videos.yaml` from existing data
3. Create extraction template with importance markers

### Phase 2: Multi-Output Extraction
1. Update `extract.py` to write to multiple locations
2. Generate `by_topic/` files
3. Generate `by_date/` files with `_key-sources.md`
4. Update index files incrementally

### Phase 3: Synthesis Layer
1. Build `synthesize.py` for daily/weekly/monthly aggregation
2. Generate timeline views
3. Create cross-cutting theme analysis

### Phase 4: Query Interface
1. Build query tools for index files
2. Create search across all dimensions
3. Generate reports on demand

---

## Benefits

1. **Single Source of Truth**: `data/sources/` remains canonical
2. **Multiple Access Patterns**: Query by topic, date, importance, or tool
3. **No Data Loss**: Insights live in index AND documents
4. **Scalable**: Each dimension can grow independently
5. **Git-Friendly**: All text-based, version controlled
6. **Claude-Optimized**: Structured for agent consumption
