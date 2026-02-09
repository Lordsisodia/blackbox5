# Topic Research Architecture

This document describes the architecture of the topic research system.

## Overview

The research system follows a pipeline architecture:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Collect │───▶│  Extract │───▶│ Synthesize│───▶│  Report  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Components

### 1. Collection (scripts/ingest.py)

- Polls configured sources
- Downloads raw content
- Stores in `data/sources/`
- Logs events to `timeline/events/`

### 2. Extraction (scripts/extract.py)

- Reads from `queue/pending/`
- Claude extracts insights
- Saves to `extracted/by_date/`
- Updates `timeline/daily/`

### 3. Synthesis (scripts/synthesize.py)

- Aggregates extractions
- Detects patterns
- Updates `timeline/weekly/` and `timeline/monthly/`

### 4. Reporting (scripts/report.py)

- Generates user-facing summaries
- Updates `reports/`

## Data Organization

### Multi-Dimensional

- **Time**: `timeline/` (events, daily, weekly, monthly)
- **Area**: `extracted/by_area/` (domain classification)
- **Topic**: `extracted/by_topic/` (specific subjects)
- **Source**: `data/sources/` (origin)

### Processing State

- `queue/pending/` - Awaiting processing
- `queue/processing/` - Currently processing
- `queue/completed/` - Done
- `queue/filtered/` - Excluded

## File Formats

See SETUP.md for detailed file format specifications.
