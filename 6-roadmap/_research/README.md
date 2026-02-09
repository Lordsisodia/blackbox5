# Blackbox5 Research

Central research hub for external intelligence and internal R&D.

## Structure

```
_research/
├── external/           # External data sources
│   ├── YouTube/
│   │   ├── AI-Improvement-Research/  # Active YouTube tracking
│   │   └── .template/                 # Template for new topics
│   ├── GitHub/
│   │   ├── Agents/                    # AI agent repos
│   │   └── .template/                 # Template for new topics
│   ├── Reddit/                        # (future)
│   └── Twitter/                       # (future)
│
└── internal/           # Internal research & development
    ├── agent-types/
    ├── data-architecture/
    ├── superintelligence-protocol/
    └── ... (20+ research topics)
```

## External Research

External research tracks intelligence from outside sources using a unified pipeline:

1. **Collect** - Gather raw data (YouTube transcripts, GitHub releases, etc.)
2. **Extract** - Claude generates structured insights
3. **Synthesize** - Aggregate patterns across time
4. **Report** - Generate actionable summaries

### Creating a New Topic

```bash
# Copy template
cp -r external/YouTube/.template external/YouTube/My-New-Topic

# Edit configuration
vim external/YouTube/My-New-Topic/config/sources.yaml

# Start collecting
python external/YouTube/My-New-Topic/scripts/ingest.py
```

## Internal Research

Internal research documents Blackbox5 system design, experiments, and findings.

See [internal/README.md](internal/README.md) for details.

## Data Flow

```
External Sources → Ingest → GitHub Storage → Extract → Synthesize → Reports
                      ↑___________________________________________↓
                                    (Local Processing)
```

## Key Principles

1. **GitHub as Data Bus** - Version control for all research data
2. **Immutable Raw Data** - Never modify collected data
3. **Multi-Dimensional Organization** - Time × Area × Topic × Source
4. **Tiered Processing** - Different priorities for different sources
5. **Temporal Layers** - Events → Daily → Weekly → Monthly
