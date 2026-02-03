# Data Layout Map - XuSFUvUdvQA (Claude Code Course)

**Video**: Anthropic's 7 Hour Claude Code Course in 27 Minutes
**Video ID**: XuSFUvUdvQA
**Creator**: David Ondrej
**Date Extracted**: 2026-02-02

---

## Complete Data Architecture

```
AI-Improvement-Research/
│
├── data/sources/david_ondrej/videos/
│   └── XuSFUvUdvQA.yaml                    (41 KB - Canonical Source)
│       ├── source:                         # Video metadata
│       │   ├── id: XuSFUvUdvQA
│       │   ├── title: "Anthropic's 7 Hour Claude Code Course..."
│       │   ├── url: https://youtube.com/watch?v=XuSFUvUdvQA
│       │   ├── published_at: "20260120"
│       │   ├── duration: 1662              # 27 minutes
│       │   └── view_count: 24756
│       ├── creator:                        # Creator info
│       │   ├── name: "David Ondrej"
│       │   ├── tier: 1
│       │   └── handle: "@david_ondrej"
│       ├── transcript:                     # Full transcript
│       │   ├── full_text: "Enthropic just released..."
│       │   ├── segment_count: 330
│       │   └── language: "en"
│       └── processing:                     # Pipeline state
│           ├── stage: "extracted"
│           └── extracted_at: "2026-02-02T08:14:00"
│
├── by_topic/claude-code/                    # TOPIC ORGANIZATION
│   ├── _index.yaml                          # Topic metadata
│   │   ├── topic: claude_code
│   │   ├── total_videos: 1
│   │   ├── tools_covered: [MCP, Anthropic Skills, ...]
│   │   └── videos: [list of all videos in this topic]
│   │
│   ├── XuSFUvUdvQA_Claud-Code-Course.md     # ITERATION 1 (47 KB)
│   │   └── 70% coverage - Initial extraction
│   │       - 8 core concepts
│   │       - Basic formatting
│   │       - [CRITICAL], [HIGH], [MEDIUM], [LOW] markers
│   │
│   ├── XuSFUvUdvQA_ITERATION_2.md           # ITERATION 2 (83 KB)
│   │   └── 90% coverage - Deep analysis
│   │       - 35 concepts rated 0-100
│   │       - Context-rich paragraphs
│   │       - Detailed explanations
│   │       - What was missed in iteration 1
│   │
│   ├── XuSFUvUdvQA_ITERATION_3.md           # ITERATION 3 (36 KB)
│   │   └── 95% coverage - Forensic analysis
│   │       - 15 newly discovered items
│   │       - Quantitative data points
│   │       - Specific examples and quotes
│   │       - What was still missed
│   │
│   └── XuSFUvUdvQA_MASTER.md                # ITERATION 4 (79 KB)
│       └── 98-99% coverage - Final synthesis
│           - Complete command reference
│           - All tools inventory
│           - All quantitative data
│           - All quiz questions
│           - Tier 1, 2, 3 synthesis
│           - Action checklist
│
├── by_date/2026/02-february/                # DATE ORGANIZATION
│   ├── _key-sources.md                      # Daily aggregation
│   │   ├── Key links found today
│   │   ├── Key frameworks found today
│   │   ├── Key tools found today
│   │   └── Videos processed
│   │
│   └── 2026-02-02_FsDYk0WqBt0.md            # Another video from same day
│
├── by_importance/                           # IMPORTANCE ORGANIZATION
│   ├── critical/                            # [CRITICAL] content only
│   ├── high/                                # [HIGH] content only
│   ├── medium/                              # [MEDIUM] content only
│   └── low/                                 # [LOW] content only
│
└── index/                                   # QUERYABLE INDEXES
    ├── videos.yaml                          # Master video registry
    │   └── XuSFUvUdvQA:
    │       ├── title: "..."
    │       ├── importance: "critical"
    │       ├── topics: [claude_code, ai_agents, ...]
    │       ├── tools_mentioned: [...]
    │       ├── frameworks: [...]
    │       └── locations:                   # Where to find extraction
    │           ├── by_topic: [...]
    │           ├── by_date: [...]
    │           └── by_importance: [...]
    │
    ├── insights.yaml                        # All extracted insights
    │   └── insights:
    │       ├── id: "XuSFUvUdvQA-001"
    │       ├── video_id: XuSFUvUdvQA
    │       ├── importance: "critical"
    │       ├── content: "..."
    │       ├── topics: [...]
    │       └── extracted_at: "..."
    │
    ├── tools.yaml                           # Tool catalog
    │   └── tools:
    │       ├── "Claude Code":
    │       │   ├── mentions: 15
    │       │   ├── videos: [XuSFUvUdvQA, ...]
    │       │   └── description: "..."
    │       └── "MCP":
    │           ├── mentions: 8
    │           └── videos: [...]
    │
    ├── frameworks.yaml                      # Framework catalog
    │   └── frameworks:
    │       └── "Three-Step Loop":
    │           ├── type: "pattern"
    │           ├── videos: [XuSFUvUdvQA]
    │           └── description: "..."
    │
    └── links.yaml                           # URL database
        └── links:
            ├── url: "https://anthropic.skilljar.com/..."
            ├── source_video: XuSFUvUdvQA
            ├── discovered_at: "..."
            └── importance: "critical"
```

---

## File Sizes

| File | Size | Lines | Coverage | Purpose |
|------|------|-------|----------|---------|
| `data/sources/david_ondrej/videos/XuSFUvUdvQA.yaml` | 41 KB | ~330 | 100% | Canonical source + transcript |
| `by_topic/claude-code/XuSFUvUdvQA_Claud-Code-Course.md` | 47 KB | 475 | 70% | Iteration 1 - Initial |
| `by_topic/claude-code/XuSFUvUdvQA_ITERATION_2.md` | 83 KB | 813 | 90% | Iteration 2 - Deep |
| `by_topic/claude-code/XuSFUvUdvQA_ITERATION_3.md` | 36 KB | 571 | 95% | Iteration 3 - Forensic |
| `by_topic/claude-code/XuSFUvUdvQA_MASTER.md` | 79 KB | 822 | 98-99% | Iteration 4 - Master |
| `index/videos.yaml` | 763 B | ~30 | N/A | Video registry |
| `index/insights.yaml` | 2.2 KB | ~70 | N/A | Insights database |
| `index/tools.yaml` | 1.3 KB | ~40 | N/A | Tool catalog |
| `index/frameworks.yaml` | 451 B | ~15 | N/A | Framework catalog |
| `index/links.yaml` | 788 B | ~25 | N/A | URL database |

**Total for this video**: ~245 KB across all files

---

## Access Patterns

### To Get the Raw Transcript
```bash
cat data/sources/david_ondrej/videos/XuSFUvUdvQA.yaml | grep "full_text"
```

### To Get the Best Extraction
```bash
cat by_topic/claude-code/XuSFUvUdvQA_MASTER.md
```

### To Get All Top-Rated Concepts (90-100)
```bash
grep "^### \[9[0-9]/100\]" by_topic/claude-code/XuSFUvUdvQA_MASTER.md
```

### To Find All Videos About Claude Code
```bash
ls by_topic/claude-code/*.md
```

### To Query All Insights
```bash
cat index/insights.yaml | grep -A5 "video_id: XuSFUvUdvQA"
```

---

## Iteration Strategy Recommendation

Based on the 4 iterations completed:

| Goal | Iterations | Coverage | Use Case |
|------|------------|----------|----------|
| **Quick reference** | 1 | 70% | Know what's in the video |
| **Good understanding** | 2 | 90% | **RECOMMENDED** - All actionable info |
| **Comprehensive** | 3 | 95% | Deep research |
| **Obsessive** | 4 | 98-99% | Creating definitive reference |

**For most videos: 2 iterations (90% coverage)**
- Captures all important, actionable information
- Gets specific details and ratings
- Good balance of effort vs value

**For critical videos: 3 iterations (95% coverage)**
- When the video is fundamental to your work
- When you need quantitative data
- When subtle details matter

**For master reference videos: 4 iterations (98-99% coverage)**
- When creating canonical documentation
- When others will rely on your extraction
- When you need to be exhaustive

---

## Summary

For the Claude Code course video (XuSFUvUdvQA):
- **Raw data**: `data/sources/david_ondrej/videos/XuSFUvUdvQA.yaml`
- **Best extraction**: `by_topic/claude-code/XuSFUvUdvQA_MASTER.md`
- **All iterations**: `by_topic/claude-code/XuSFUvUdvQA_*.md`
- **Queryable data**: `index/*.yaml`
- **Total size**: ~245 KB
- **Coverage**: 98-99% of important information
