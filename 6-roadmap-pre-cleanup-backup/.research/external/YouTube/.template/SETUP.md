# Topic Research Setup Guide

Use this template to create a new topic research system.

## Quick Start

1. **Copy this folder** to `../{Topic-Name}/`
2. **Edit `config/sources.yaml`** - Add your sources
3. **Edit `README.md`** - Update topic description
4. **Start collecting data** - Use scripts/ingest.py

## Folder Structure

```
{Topic-Name}/
├── README.md                   # Topic overview
├── SETUP.md                    # This file
├── config/
│   └── sources.yaml            # Source configuration
├── data/
│   └── sources/{source}/       # Raw data (immutable)
├── extracted/                  # Claude-generated insights
│   ├── by_date/               # YYYY-MM-DD/
│   ├── by_area/               # Domain classification
│   └── by_topic/              # Specific topics
├── synthesized/               # Aggregated intelligence
│   └── YYYY/MM/{weekly,monthly}/
├── timeline/                  # 4 temporal layers
│   ├── events/                # Micro
│   ├── daily/                 # Meso
│   ├── weekly/                # Macro
│   └── monthly/               # Meta
├── queue/                     # Processing state
│   ├── pending/
│   ├── processing/
│   ├── completed/
│   └── filtered/
├── reports/                   # User output
│   ├── daily/
│   ├── weekly/
│   └── actionable/
├── scripts/                   # Automation
│   ├── ingest.py
│   ├── extract.py
│   ├── synthesize.py
│   └── report.py
├── index/                     # Navigation
└── .docs/                     # Documentation
```

## File Formats

### Raw Data (data/sources/{source}/{id}.yaml)
```yaml
---
source:
  type: [youtube|github|reddit|twitter]
  id: "unique-id"
  url: "source-url"
  title: "Content title"
  author: "Creator name"
  published_at: YYYY-MM-DDTHH:MM:SSZ
  collected_at: YYYY-MM-DDTHH:MM:SSZ

content:
  raw: "..."

processing:
  status: pending_extraction
  priority: [critical|high|medium|low]
---
```

### Extracted Intelligence (extracted/by_date/{date}/{id}.md)
```yaml
---
extraction:
  source_id: "..."
  extracted_at: YYYY-MM-DDTHH:MM:SSZ

classification:
  areas: [area1, area2]
  topics: [topic1, topic2]

summary:
  overview: "..."
  novelty_score: 1-10

key_points:
  - point: "..."
    timestamp: "MM:SS"

actionable_takeaways:
  - action: "..."
    difficulty: [easy|medium|hard]
    impact: [low|medium|high]

ranking:
  composite: 0-100
---

# Full extraction content here
```

## Source Tiers

- **Tier 1**: Must watch - Auto-process immediately
- **Tier 2**: High quality - Process normally
- **Tier 3**: Filtered - Manual review first

## Processing Pipeline

1. **Ingest** → Collect raw data
2. **Extract** → Claude generates insights
3. **Synthesize** → Aggregate patterns
4. **Report** → Generate summaries

## Timeline Layers

| Layer | Frequency | Purpose |
|-------|-----------|---------|
| Events | Real-time | Individual data points |
| Daily | Daily | Digest |
| Weekly | Weekly | Pattern detection |
| Monthly | Monthly | Strategic view |
