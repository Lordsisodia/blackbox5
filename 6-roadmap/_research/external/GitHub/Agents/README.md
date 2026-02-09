# AI Agents Research

Research system for tracking and analyzing AI agent-related GitHub repositories.

## Overview

This system automatically collects, processes, and analyzes GitHub repositories related to AI agents, autonomous systems, and agent frameworks.

## Quick Links

- [Setup Guide](./SETUP.md)
- [Tracked Repositories](./config/sources.yaml)
- [Queue Status](./queue/)
- [Latest Reports](./reports/)

## Structure

```
├── data/                      # Raw repo data
│   └── repos/{owner}/{repo}/  # README, releases, commits
├── extracted/                 # Claude-generated insights
│   ├── by_date/               # Chronological
│   ├── by_area/               # Domain classification
│   └── by_topic/              # Specific topics
├── synthesized/               # Aggregated intelligence
├── timeline/                  # 4 temporal layers
├── queue/                     # Processing pipeline
├── reports/                   # User-facing output
└── scripts/                   # Automation
```

## Data Collected

- Release notes and changelogs
- README changes
- Commit messages (filtered)
- Issue/PR summaries
- Discussion highlights
- Star/fork trends

## Usage

1. **Check queue**: See repos pending in `queue/pending/`
2. **Process repos**: Run extraction on pending items
3. **Review reports**: Check `reports/` for summaries
4. **Track timeline**: See `timeline/` for temporal view

## Last Updated

YYYY-MM-DD
