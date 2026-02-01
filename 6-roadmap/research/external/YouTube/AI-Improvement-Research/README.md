# AI Improvement Research

**Purpose**: Automated collection and analysis of YouTube content about AI, Claude, MCP, and related technologies.

**Status**: In development - local testing phase

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run ingestion (collect new videos)
python scripts/ingest.py --all

# 3. Process queue (extract insights with Claude)
python scripts/extract.py --pending

# 4. Generate daily report
python scripts/report.py --daily
```

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Collect   │────▶│   Extract   │────▶│  Synthesize │
│  (Server)   │     │  (Claude)   │     │   (Claude)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   data/sources/    extracted/          synthesized/
   timeline/         timeline/           timeline/
```

### Data Flow

1. **Collection** (`scripts/ingest.py`)
   - Polls 23 configured YouTube channels via RSS
   - Downloads transcripts and metadata
   - Stores raw data in `data/sources/{creator}/`
   - Logs events to `timeline/events/`

2. **Extraction** (`scripts/extract.py`)
   - Reads pending videos from `queue/pending/`
   - Claude extracts concepts, takeaways, resources
   - Saves to `extracted/by_date/{date}/{video_id}.md`
   - Updates `timeline/daily/` digest

3. **Synthesis** (`scripts/synthesize.py`)
   - Aggregates daily extractions
   - Detects themes and patterns
   - Generates weekly/monthly reports
   - Updates `timeline/weekly/` and `timeline/monthly/`

---

## Folder Structure

```
AI-Improvement-Research/
│
├── README.md                 # This file
├── config/
│   └── sources.yaml          # 23 YouTube sources + config
│
├── data/                     # RAW DATA (immutable)
│   └── sources/              # Organized by creator
│       └── {creator_slug}/
│           └── videos/
│               └── {video_id}.yaml
│
├── extracted/                # CLAUDE-GENERATED
│   ├── by_date/              # Chronological
│   │   └── 2025-02-01/
│   │       └── {video_id}.md
│   ├── by_area/              # Domain classification
│   │   ├── ai-engineering/
│   │   ├── claude-mcp/
│   │   └── ...
│   └── by_topic/             # Specific topics
│       ├── vibe-coding/
│       ├── mcp-servers/
│       └── ...
│
├── synthesized/              # AGGREGATED INTELLIGENCE
│   └── 2025/
│       └── 02/
│           ├── weekly/
│           │   └── 2025-W05.md
│           └── monthly/
│               └── 2025-02.md
│
├── timeline/                 # TEMPORAL LAYERS
│   ├── index.yaml            # Master navigation
│   ├── events/               # Event log (micro)
│   ├── daily/                # Daily digests (meso)
│   ├── weekly/               # Weekly synthesis (macro)
│   └── monthly/              # Monthly retrospective (meta)
│
├── queue/                    # PROCESSING STATE
│   ├── pending/              # Awaiting extraction
│   ├── processing/           # Currently extracting
│   └── completed/            # Done
│
├── reports/                  # USER-FACING OUTPUT
│   ├── daily/                # Daily summaries
│   ├── weekly/               # Weekly reports
│   └── actionable/
│       └── todo-queue.yaml   # Action items
│
├── scripts/                  # AUTOMATION
│   ├── ingest.py             # Collect videos
│   ├── extract.py            # Extract insights
│   ├── synthesize.py         # Aggregate analysis
│   ├── report.py             # Generate reports
│   └── timeline.py           # Timeline management
│
└── .docs/                    # DOCUMENTATION
    ├── ARCHITECTURE.md       # System design
    ├── TIMELINE-ARCHITECTURE.md  # Timeline design
    └── DATA-STRUCTURE.md     # File formats
```

---

## Configuration

### Sources (`config/sources.yaml`)

23 YouTube channels organized by tier:
- **Tier 1 (8)**: Must watch - Anthropic, Simon Willison, Latent Space, etc.
- **Tier 2 (9)**: High quality - Fireship, Theo, Matthew Berman, etc.
- **Tier 3 (6)**: Filtered - AI Labs, AI Code King, etc.

Each source has:
- `areas`: Domain classification (ai-engineering, claude-mcp, etc.)
- `topics`: Specific topics (vibe-coding, mcp-servers, etc.)
- `tier`: Processing priority
- `rss_feed`: RSS feed URL for monitoring

### Areas

- `ai-engineering`: Building AI systems, tools, infrastructure
- `claude-mcp`: Claude-specific content, MCP protocol
- `coding-tools`: Development tools, IDEs, workflows
- `ai-agents`: Autonomous agents, multi-agent systems
- `ai-news`: Industry news, model releases
- `business-strategy`: AI business, startups
- `ai-research`: Academic research, papers

---

## File Formats

### Raw Data (`data/sources/{creator}/videos/{id}.yaml`)

```yaml
---
source:
  type: youtube
  id: XuSFUvUdvQA
  url: https://youtube.com/watch?v=XuSFUvUdvQA
  title: "..."
  channel: "David Ondrej"
  published_at: 2025-01-28T10:00:00Z
  collected_at: 2025-02-01T08:15:00Z

transcript:
  language: en
  full_text: "..."
  segments:
    - start: "00:00:00"
      text: "..."

processing:
  status: pending_extraction
  priority: high
---
```

### Extracted Intelligence (`extracted/by_date/{date}/{id}.md`)

```yaml
---
extraction:
  video_id: XuSFUvUdvQA
  extracted_at: 2025-02-01T14:30:00Z

classification:
  areas: [ai-engineering, claude-mcp]
  topics: [vibe-coding, claude-code]

summary:
  overview: "..."
  novelty_score: 8

concepts:
  - name: "Claude Code MCP Integration"
    timestamp: "04:32"

actionable_takeaways:
  - action: "Set up filesystem MCP server"
    difficulty: easy
    impact: high

ranking:
  composite: 85

links:
  source: ../../data/sources/david_ondrej/videos/XuSFUvUdvQA.yaml
---

# Video Title

## Core Concepts
...
```

---

## Timeline System

The timeline captures temporal context across four layers:

1. **Events** (`timeline/events/`): Individual data points
   - Video discovered
   - Transcript downloaded
   - Extraction completed
   - Action queued

2. **Daily** (`timeline/daily/`): Daily digests
   - Videos collected
   - Themes emerging
   - Key actions

3. **Weekly** (`timeline/weekly/`): Pattern detection
   - Theme evolution
   - Knowledge graph updates
   - Action review

4. **Monthly** (`timeline/monthly/`): Strategic view
   - Knowledge base growth
   - Creator analysis
   - Recommendations

See `.docs/TIMELINE-ARCHITECTURE.md` for full details.

---

## Current Status

- **Sources configured**: 23 YouTube channels
- **Videos collected**: 9 (all from David Ondrej)
- **Videos extracted**: 0
- **Timeline entries**: 0

### Next Steps

1. [ ] Run full ingestion on all 23 sources
2. [ ] Process collected videos through extraction
3. [ ] Generate first daily digest
4. [ ] Deploy collector to Railway (server)
5. [ ] Set up automated daily sync

---

## Agent Interface

For Claude/agents working with this data:

### Query Patterns

```yaml
# Get today's activity
timeline/daily/2025-02-01.md

# Get this week's synthesis
timeline/weekly/2025-W05.md

# Get videos by area
extracted/by_area/claude-mcp/

# Get pending actions
reports/actionable/todo-queue.yaml

# Get source config
config/sources.yaml
```

### Key Files for Agents

1. `timeline/index.yaml` - Master navigation
2. `config/sources.yaml` - Source definitions
3. `reports/actionable/todo-queue.yaml` - Action items
4. `extracted/by_date/{date}/` - Daily extractions

---

## Development

### Local Testing

```bash
# Test ingestion on single source
python scripts/ingest.py --source david_ondrej --dry-run

# Test extraction on single video
python scripts/extract.py --video XuSFUvUdvQA

# Generate daily report
python scripts/report.py --daily --date 2025-02-01
```

### Server Deployment (Railway)

```bash
# Deploy collector
railway login
railway init
railway up

# Set environment variables
railway variables set GITHUB_TOKEN=xxx
railway variables set GITHUB_REPO=xxx
```

---

## License

Private research project.
