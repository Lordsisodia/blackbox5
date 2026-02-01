# Timeline Architecture for AI Improvement Research

**Date**: 2026-02-01
**Status**: Proposed
**Purpose**: Define how temporal data is captured, organized, and accessed

---

## First Principles

### Why a Timeline?

Information has value in context:
- **When** did we learn this? (chronological)
- **What** were we working on then? (project context)
- **How** did our understanding evolve? (knowledge graph)
- **What's** emerging now? (trend detection)

### What Makes a Timeline Useful?

1. **Retrievability** - Find what we knew at any point
2. **Traceability** - Follow ideas back to sources
3. **Pattern Detection** - See trends over time
4. **Actionability** - Know what's urgent now

---

## Timeline Layers

### Layer 1: Event Timeline (Micro)

**What**: Individual data points as they arrive
**Format**: Append-only log
**Location**: `timeline/events/`

```yaml
# timeline/events/2025-02-01.yaml
events:
  - timestamp: 2025-02-01T08:15:00Z
    type: video_discovered
    source: david_ondrej
    video_id: XuSFUvUdvQA
    title: "Anthropic's 7 Hour Claude Code Course..."
    significance: high  # Based on creator tier

  - timestamp: 2025-02-01T08:16:30Z
    type: transcript_downloaded
    video_id: XuSFUvUdvQA
    duration: 1620
    segment_count: 145

  - timestamp: 2025-02-01T14:30:00Z
    type: extraction_completed
    video_id: XuSFUvUdvQA
    extractor: claude-3-5-sonnet
    key_themes:
      - mcp-servers
      - vibe-coding
    actionability_score: 85

  - timestamp: 2025-02-01T14:35:00Z
    type: action_queued
    action: "Set up filesystem MCP server"
    priority: high
```

### Layer 2: Daily Digest (Meso)

**What**: Aggregated daily summary
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/daily/`

```yaml
---
date: 2025-02-01
type: daily_digest

summary:
  videos_collected: 12
  videos_extracted: 8
  new_themes_detected: 3
  actions_queued: 5

themes_emerging:
  - name: "MCP Server Standardization"
    frequency: 4
    sources:
      - XuSFUvUdvQA
      - abc123
    insight: "Multiple creators converging on MCP as the integration standard"

  - name: "Vibe Coding Workflows"
    frequency: 3
    sources:
      - def456
      - ghi789

key_actions:
  - action: "Set up filesystem MCP server"
    priority: high
    source_count: 3

  - action: "Review Claude Projects feature"
    priority: medium
    source_count: 2

sources:
  - video_id: XuSFUvUdvQA
    creator: david_ondrej
    title: "..."
    composite_score: 85
    link: ../../extracted/by_date/2025-02-01/XuSFUvUdvQA.md
---

# Daily Digest - February 1, 2025

## Overview
Today we collected 12 videos from 8 creators...

## Emerging Themes

### MCP Server Standardization
Four different creators discussed MCP servers today...

## Priority Actions
1. [HIGH] Set up filesystem MCP server
2. [MEDIUM] Review Claude Projects feature

## Notable Sources
- David Ondrej's comprehensive Claude Code walkthrough
- ...
```

### Layer 3: Weekly Synthesis (Macro)

**What**: Pattern detection across days
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/weekly/`

```yaml
---
week: 2025-W05
date_range: 2025-01-27 to 2025-02-02
type: weekly_synthesis

summary:
  total_videos: 47
  total_creators: 12
  themes_tracked: 5
  actions_completed: 3
  actions_pending: 8

theme_evolution:
  - theme: "MCP Server Ecosystem"
    first_seen: 2025-01-28
    frequency: 12
    trend: accelerating  # accelerating | stable | declining
    key_insight: "MCP is becoming the USB-C for AI tools"

  - theme: "Vibe Coding"
    first_seen: 2025-01-15
    frequency: 8
    trend: stable
    key_insight: "Iterative AI-assisted development is now standard practice"

knowledge_graph:
  new_concepts:
    - "MCP Tool Definition"
    - "Claude Code Workflows"
    - "Agent Memory Patterns"

  concept_relationships:
    - from: "MCP Servers"
      to: "Claude Code"
      relationship: "enables"
      evidence: [XuSFUvUdvQA, abc123]

actions_review:
  completed:
    - action: "Installed filesystem MCP"
      completed_at: 2025-01-30
      outcome: "Successfully integrated with Claude Code"

  pending:
    - action: "Set up GitHub MCP server"
      priority: high
      blocking: null

  abandoned:
    - action: "Test deprecated feature"
      reason: "Feature removed in latest update"
---

# Weekly Synthesis - Week 5, 2025

## Executive Summary
This week marked a significant shift toward MCP server adoption...

## Theme Deep Dives

### MCP Server Ecosystem
[Detailed analysis with evidence]

## Knowledge Graph Evolution
[Concept map showing relationships discovered]

## Action Review
[What we did, what we're doing, what's blocked]
```

### Layer 4: Monthly Retrospective (Meta)

**What**: Strategic view of knowledge accumulation
**Format**: YAML frontmatter + Markdown
**Location**: `timeline/monthly/`

```yaml
---
month: 2025-02
type: monthly_retrospective

summary:
  total_videos_processed: 180
  unique_creators: 23
  themes_identified: 12
  actions_completed: 15
  knowledge_base_growth: "+45%"

strategic_insights:
  - insight: "MCP adoption is happening faster than expected"
    confidence: high
    evidence_count: 34

  - insight: "Vibe coding is replacing traditional prototyping"
    confidence: medium
    evidence_count: 18

knowledge_base_stats:
  concepts_documented: 45
  code_examples_collected: 23
  resources_indexed: 67
  actionable_items: 31

creator_analysis:
  most_valuable:
    - creator: david_ondrej
      videos: 8
      avg_score: 88
      key_contributions: ["MCP deep dive", "Claude Code workflows"]

  emerging:
    - creator: new_ai_channel
      videos: 3
      avg_score: 82
      trend: rising

recommendations:
  - "Increase monitoring of MCP-related content"
  - "Add 3 new creators focused on agent architecture"
  - "Create dedicated vibe-coding resource collection"
---

# Monthly Retrospective - February 2025

## Strategic Overview
February was the month MCP servers went mainstream...

## Knowledge Base Growth
[Visual/graph representation of growth]

## Creator Ecosystem Analysis
[Who's producing the most value]

## Recommendations for March
1. Expand MCP server coverage
2. ...
```

---

## Timeline Index

**Location**: `timeline/index.yaml`

Master index for quick navigation:

```yaml
timeline_index:
  version: "1.0"
  last_updated: 2025-02-01T20:00:00Z

events:
  latest: timeline/events/2025-02-01.yaml
  count: 1567

daily:
  latest: timeline/daily/2025-02-01.md
  count: 32
  by_month:
    2025-01: 31
    2025-02: 1

weekly:
  latest: timeline/weekly/2025-W05.md
  count: 5

monthly:
  latest: timeline/monthly/2025-01.md
  count: 1

themes_active:
  - name: "MCP Server Ecosystem"
    first_seen: 2025-01-15
    last_seen: 2025-02-01
    frequency: 23

  - name: "Vibe Coding"
    first_seen: 2025-01-10
    last_seen: 2025-02-01
    frequency: 18

actions:
  total_queued: 45
  completed: 12
  pending: 28
  abandoned: 5
```

---

## Event Types

| Type | Description | Significance |
|------|-------------|--------------|
| `video_discovered` | New video found via RSS | Always logged |
| `transcript_downloaded` | Raw data collected | Always logged |
| `transcript_failed` | Could not get transcript | Log + alert if pattern |
| `extraction_completed` | Claude finished analysis | Always logged |
| `extraction_queued` | Awaiting processing | Track queue depth |
| `theme_detected` | New theme identified | Log if novel |
| `action_queued` | Actionable item found | Log if high priority |
| `action_completed` | User marked done | Track completion rate |
| `source_added` | New creator added | Log config change |
| `source_removed` | Creator removed | Log config change |

---

## Implementation Notes

### Event Generation

Events are generated by:
1. **ingest.py** - Creates `video_discovered`, `transcript_downloaded` events
2. **extract.py** - Creates `extraction_completed`, `theme_detected`, `action_queued` events
3. **Manual actions** - User marks actions complete

### Aggregation Schedule

| Layer | Trigger | Script |
|-------|---------|--------|
| Events | Real-time | Individual scripts |
| Daily | Daily at 20:00 UTC | `timeline/generate-daily.py` |
| Weekly | Sunday at 20:00 UTC | `timeline/generate-weekly.py` |
| Monthly | Last day of month | `timeline/generate-monthly.py` |

### Agent Interface

Agents query timeline via:

```yaml
# Example agent query context
query:
  type: timeline_lookup
  period: 2025-02-01
  filter:
    themes: ["mcp-servers"]
    min_score: 80
  output: summary
```

---

## Related Documents

- `ARCHITECTURE.md` - Overall system design
- `DATA-STRUCTURE.md` - File organization
- `AGENT-INTERFACE.md` - How agents interact with data
