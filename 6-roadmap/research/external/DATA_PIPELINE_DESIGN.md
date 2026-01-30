# Deep Research Data Pipeline - Complete Flow

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INPUT SOURCES                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  VIP Channels (RSS)    │    Manual URLs      │    Reddit/Twitter (future)   │
│  - Anthropic           │    - You paste      │                               │
│  - Simon Willison      │    - Auto-process   │                               │
│  - Latent Space        │                     │                               │
└──────────┬─────────────────────────┬────────────────────────────────────────┘
           │                         │
           ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STAGE 1: INGESTION & STORAGE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  data/raw/YYYY-MM-DD/                                                        │
│  ├── videos/                                                                 │
│  │   └── {video_id}.json          # Metadata + source info                   │
│  ├── transcripts/                                                            │
│  │   └── {video_id}.txt           # Full transcript text                     │
│  └── index.yaml                   # Daily manifest of all sources            │
│                                                                              │
│  Key Fields:                                                                 │
│  - source_type: "vip_rss" | "manual" | "reddit" | "twitter"                  │
│  - discovered_at: timestamp                                                  │
│  - processed_stage: 0-4                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STAGE 2: SOURCE-LEVEL EXTRACTION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  For EACH video/source, run extraction agent:                                │
│                                                                              │
│  data/extracted/YYYY-MM-DD/                                                  │
│  └── {video_id}.yaml              # Structured extraction                    │
│                                                                              │
│  Structure:                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ source:                                                                 │ │
│  │   id: "video_id"                                                        │ │
│  │   type: "youtube"                                                       │ │
│  │   url: "https://..."                                                    │ │
│  │   channel: "Anthropic"                                                  │ │
│  │   published_at: "2025-01-30T10:00:00Z"                                  │ │
│  │   discovered_via: "vip_rss"                                             │ │
│  │                                                                         │ │
│  │ extraction:                                                             │ │
│  │   summary:                                                              │ │
│  │     overview: "2-3 sentences"                                           │ │
│  │     key_thesis: "Main argument"                                         │ │
│  │     novelty_score: 1-10        # How new is this info?                  │ │
│  │                                                                         │ │
│  │   concepts:                    # Knowledge artifacts                    │ │
│  │     - name: "Claude Code MCP Server"                                    │ │
│  │       description: "What it does"                                       │ │
│  │       timestamp: "04:32"                                                │ │
│  │       type: "tool|technique|pattern|model"                              │ │
│  │       confidence: "high|medium|low"                                     │ │
│  │                                                                         │ │
│  │   actionable_takeaways:        # Things to implement                    │ │
│  │     - action: "Set up MCP server for..."                                │ │
│  │       context: "When you need X..."                                     │ │
│  │       difficulty: "easy|medium|hard"                                    │ │
│  │       impact: "high|medium|low"                                         │ │
│  │       timestamp: "07:15"                                                │ │
│  │       prerequisites: ["Claude Code", "Node.js"]                         │ │
│  │                                                                         │ │
│  │   resources_mentioned:                                                  │ │
│  │     - name: "mcp-server-github"                                         │ │
│  │       type: "github_repo"                                               │ │
│  │       url: "https://github.com/..."      # If extractable               │ │
│  │       timestamp: "12:45"                                                │ │
│  │       description: "What it does"                                       │ │
│  │                                                                         │ │
│  │   code_examples:                                                        │ │
│  │     - description: "MCP server setup"                                   │ │
│  │       timestamp: "08:20"                                                │ │
│  │       language: "typescript"                                            │ │
│  │       code_snippet: |                                                   │ │
│  │         // Approximate code from transcript                             │ │
│  │                                                                         │ │
│  │   mcp_relevance:                                                        │ │
│  │     has_mcp_content: true                                               │ │
│  │     mcp_patterns: ["server-architecture", "tool-definition"]            │ │
│  │     mcp_servers_mentioned: ["github", "filesystem"]                     │ │
│  │                                                                         │ │
│  │   claude_relevance:                                                     │ │
│  │     has_claude_content: true                                            │ │
│  │     claude_features: ["Claude Code", "Projects"]                        │ │
│  │     claude_code_patterns: ["mcp-integration", "system-prompts"]         │ │
│  │                                                                         │ │
│  │   quality_signals:                                                      │ │
│  │     originality: "original|repackaged|curated"                          │ │
│  │     demonstrated: true           # Did they show it working?            │ │
│  │     depth: "surface|moderate|deep"                                      │ │
│  │     source_credibility: 1-10                                            │ │
│  │                                                                         │ │
│  │   tags:                                                                 │ │
│  │     topics: ["MCP", "Claude Code", "AI Agents"]                         │ │
│  │     type: "tutorial|news|analysis|demo|opinion"                         │ │
│  │     technical_level: "beginner|intermediate|advanced"                   │ │
│  │                                                                         │ │
│  │ ranking:                                                                │ │
│  │   urgency: 1-100               # How soon should you act?               │ │
│  │   relevance: 1-100             # Match to your projects                 │ │
│  │   quality: 1-100               # Overall information quality            │ │
│  │   novelty: 1-100               # How new is this to you?                │ │
│  │   composite: 1-100             # Weighted average                       │ │
│  │                                                                         │ │
│  │ processing_metadata:                                                    │ │
│  │   extracted_at: "2025-01-30T14:00:00Z"                                  │ │
│  │   extractor_version: "1.0"                                              │ │
│  │   transcript_quality: "good|partial|poor"                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STAGE 3: AGGREGATION & THEME DETECTION                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Read ALL extractions for the period, detect patterns:                       │
│                                                                              │
│  data/synthesized/YYYY-MM-DD/                                                │
│  ├── themes.yaml                  # Detected themes across sources           │
│  └── ranked_sources.yaml          # Sources sorted by composite score        │
│                                                                              │
│  themes.yaml structure:                                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ synthesis_date: "2025-01-30"                                            │ │
│  │ period: "daily"                    # or "weekly"                        │ │
│  │ total_sources: 12                                                       │ │
│  │                                                                          │ │
│  │ themes:                      # Auto-detected from extractions           │ │
│  │   - name: "MCP Server Best Practices"                                   │ │
│  │     description: "Multiple sources discussing MCP architecture"         │ │
│  │     frequency: 4              # How many sources mention this           │ │
│  │     related_concepts: ["tool-definition", "server-lifecycle"]           │ │
│  │     key_sources: ["video_id_1", "video_id_2"]                           │ │
│  │     urgency: 85               # Highest urgency in theme                │ │
│  │                                                                          │ │
│  │   - name: "Claude Code Workflows"                                       │ │
│  │     description: "New patterns for Claude Code usage"                   │ │
│  │     frequency: 3                                                          │ │
│  │     ...                                                                  │ │
│  │                                                                          │ │
│  │ cross_cutting_insights:      # Insights that span multiple themes       │ │
│  │   - insight: "MCP is becoming the standard for AI tool integration"     │ │
│  │     supporting_evidence:                                                  │ │
│  │       - source: "video_id_1"                                            │ │
│  │         quote: "MCP is the USB-C for AI..."                             │ │
│  │         timestamp: "05:30"                                              │ │
│  │                                                                          │ │
│  │ ranked_sources:              # All sources, sorted by value             │ │
│  │   - id: "video_id_1"                                                    │ │
│  │     title: "..."                                                        │ │
│  │     composite_score: 92                                                 │ │
│  │     tier: "must_watch"          # must_watch|recommended|reference      │ │
│  │     primary_theme: "MCP Server Best Practices"                          │ │
│  │                                                                          │ │
│  │   - id: "video_id_2"                                                    │ │
│  │     composite_score: 78                                                 │ │
│  │     tier: "recommended"                                                 │ │
│  │     ...                                                                  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STAGE 4: FINAL REPORT GENERATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  data/reports/YYYY-MM-DD/                                                    │
│  ├── full_report.md               # Complete detailed report                │
│  ├── executive_summary.md         # 1-page TL;DR                            │
│  └── actionable_queue.yaml        # Your to-implement list                  │
│                                                                              │
│  full_report.md structure:                                                   │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ # AI Research Digest - 2025-01-30                                       │ │
│  │                                                                          │ │
│  │ ## Executive Summary                                                    │ │
│  │ 3-4 sentences on what matters most today                                │ │
│  │                                                                          │ │
│  │ ## Today's Big Themes                                                   │ │
│  │                                                                          │ │
│  │ ### 🔥 MCP Server Best Practices (4 sources)                            │ │
│  │ **Why it matters:** Context for this theme                              │ │
│  │                                                                          │ │
│  │ **Key Insights:**                                                       │ │
│  │ 1. **Insight name** - Description with [reasoning]                      │ │
│  │    - Source: [Video Title](url) at 04:32                                │ │
│  │    - Evidence: "Direct quote or summary of proof"                       │ │
│  │                                                                          │ │
│  │ 2. **Insight name** - Description                                       │ │
│  │    - Source: [Video Title](url) at 07:15                                │ │
│  │    - Supporting: Links to repos, papers mentioned                       │ │
│  │                                                                          │ │
│  │ **Actionable Takeaways:**                                               │ │
│  │ - [HIGH] Action item with difficulty estimate                           │ │
│  │   - Prerequisites: What's needed                                        │ │
│  │   - Expected outcome: What you'll gain                                  │ │
│  │                                                                          │ │
│  │ ### 🚀 Claude Code Workflows (3 sources)                                │ │
│  │ ...                                                                      │ │
│  │                                                                          │ │
│  │ ## Notable Mentions                                                     │ │
│  │ Sources worth noting but not theme leaders                              │ │
│  │                                                                          │ │
│  │ ## Resources Discovered                                                 │ │
│  │ | Resource | Type | Mentioned In | Why It Matters |                      │ │
│  │ |------------|------|--------------|------------------|                  │ │
│  │ | mcp-server-github | Repo | Video 1 | Official GitHub MCP |            │ │
│  │                                                                          │ │
│  │ ## Tomorrow's Exploration                                               │ │
│  │ Questions or threads to follow up on                                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  actionable_queue.yaml:                                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ queue:                                                                  │ │
│  │   - id: "action_001"                                                    │ │
│  │     action: "Set up MCP filesystem server"                              │ │
│  │     source: "video_id_1"                                                │ │
│  │     difficulty: "medium"                                                │ │
│  │     impact: "high"                                                      │ │
│  │     estimated_time: "30 min"                                            │ │
│  │     prerequisites: ["Claude Code installed", "Node.js"]                 │ │
│  │     status: "pending"                                                   │ │
│  │     added_date: "2025-01-30"                                            │ │
│  │                                                                          │ │
│  │   - id: "action_002"                                                    │ │
│  │     action: "Review new Claude Projects feature"                        │ │
│  │     ...                                                                  │ │
│  │                                                                          │ │
│  │ completed: []                                                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STAGE 5: DELIVERY & INTERACTION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Delivery Options:                                                           │
│  1. Telegram message with executive summary + link to full report           │
│  2. Claude Code can read reports/ and answer questions                      │
│  3. Web UI for browsing (future)                                            │ │
│                                                                              │
│  Interaction Patterns:                                                       │
│  - "What did Simon Willison say about MCP this week?"                       │
│  - "Show me all high-impact actions from today"                             │
│  - "Summarize the theme around AI memory"                                   │
│  - "What repos were mentioned yesterday?"                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


## Key Design Decisions

### 1. Why YAML for structured data?
- Human-readable (you can open and inspect)
- Claude can parse and query easily
- Supports comments for reasoning
- Version-control friendly

### 2. How does ranking work?
```
composite_score = (
    urgency * 0.30 +      # Time-sensitive?
    relevance * 0.25 +    # Matches your projects?
    quality * 0.25 +      # Information density?
    novelty * 0.20        # New to you?
)
```

### 3. How are themes detected?
- Extract concepts from all sources
- Cluster by semantic similarity
- Count frequency of related concepts
- Human-verified naming

### 4. How do we ensure reasoning is captured?
- Every claim links to source + timestamp
- "Evidence" field for direct quotes
- "Supporting" field for related resources
- Cross-references between related insights

### 5. What about the "so what?"
- Every theme has "Why it matters" section
- Actionable takeaways with impact estimates
- Prerequisites so you know if you can act now
- Queue system to track what you implement


## File Organization Summary

```
deep research/
└── YouTube/
    └── AI Improvement Research/
        ├── config/
        │   ├── vip_channels.yaml
        │   ├── context.yaml
        │   └── ranking_weights.yaml
        ├── data/
        │   ├── raw/                    # Stage 1
        │   │   └── YYYY-MM-DD/
        │   │       ├── videos/
        │   │       ├── transcripts/
        │   │       └── index.yaml
        │   ├── extracted/              # Stage 2
        │   │   └── YYYY-MM-DD/
        │   │       └── {video_id}.yaml
        │   ├── synthesized/            # Stage 3
        │   │   └── YYYY-MM-DD/
        │   │       ├── themes.yaml
        │   │       └── ranked_sources.yaml
        │   └── reports/                # Stage 4
        │       └── YYYY-MM-DD/
        │           ├── full_report.md
        │           ├── executive_summary.md
        │           └── actionable_queue.yaml
        └── scripts/
            ├── ingest.py               # Stage 1
            ├── extract.py              # Stage 2
            ├── synthesize.py           # Stage 3
            ├── report.py               # Stage 4
            └── query.py                # Interactive questioning
```


## Example Query Interface

```bash
# Ask questions about your research
./research.py query "What MCP servers were mentioned this week?"
./research.py query "Show me high-urgency actions from Simon Willison videos"
./research.py query "Summarize the theme around AI memory management"
./research.py query "What code examples were provided for Claude Code?"

# Get reports
./research.py report --date today --format executive
./research.py report --date 2025-01-20 --format full

# Manage action queue
./research.py actions list --status pending
./research.py actions complete action_001
```
