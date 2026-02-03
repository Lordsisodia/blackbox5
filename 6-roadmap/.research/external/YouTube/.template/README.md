# {Topic Name} Research

Research system for tracking and analyzing {topic} content.

## Overview

This system automatically collects, processes, and analyzes {topic} content from multiple sources.

## Quick Links

- [Setup Guide](./SETUP.md)
- [Data Sources](./config/sources.yaml)
- [Queue Status](./queue/)
- [Latest Reports](./reports/)

## Structure

```
├── data/           # Raw collected data
├── extracted/      # Claude-generated insights
├── synthesized/    # Aggregated intelligence
├── timeline/       # Temporal organization
├── queue/          # Processing pipeline
├── reports/        # User-facing output
└── scripts/        # Automation
```

## Usage

1. **Check queue**: See what's pending in `queue/pending/`
2. **Process items**: Run extraction on pending items
3. **Review reports**: Check `reports/` for summaries
4. **Track timeline**: See `timeline/` for temporal view

## Last Updated

YYYY-MM-DD
