# Learning Extraction Module

Extracts structured learnings from task run directories and manages the `learning-index.yaml` knowledge base.

## Overview

This module provides functionality to:
- Extract learnings from THOUGHTS.md, DECISIONS.md, and RESULTS.md files
- Populate and maintain the learning-index.yaml file
- Deduplicate learnings using content hashing
- Provide health checks and monitoring

## Files

| File | Purpose |
|------|---------|
| `learning_extractor.py` | Core extraction library |
| `backfill_learnings.py` | Backfill script for historical runs |
| `check_learning_index.py` | Health check and monitoring |
| `__init__.py` | Module initialization |

## Usage

### Extract from Single Run

```bash
python learning_extractor.py --run-dir /path/to/run-0001
```

### Backfill All Historical Runs

```bash
python backfill_learnings.py
```

### Rebuild Index from Scratch

```bash
python backfill_learnings.py --rebuild
```

### Health Check

```bash
python check_learning_index.py
```

## Integration

The learning extractor is integrated into `retain-on-complete.py` hook, which runs automatically when tasks are completed. This ensures the learning index stays up-to-date without manual intervention.

## Learning Types

The extractor categorizes learnings into the following types:

- **pattern**: Recurring patterns or best practices
- **decision**: Architectural or technical decisions
- **challenge**: Problems encountered and their resolutions
- **optimization**: Performance improvements
- **bugfix**: Bug fixes and error resolutions
- **insight**: General insights and observations

## Categories

Learnings are also categorized by domain:

- **technical**: Code, implementation, technical details
- **process**: Workflow, methodology, procedures
- **architectural**: System design, patterns, structure
- **operational**: Deployment, monitoring, maintenance

## Index Location

The learning index is stored at:
```
/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/memory/insights/learning-index.yaml
```

## Schema

Each learning entry contains:

```yaml
learning_id: TASK-XXX-LEARNING-N
task_id: TASK-XXX
task_title: "Task Title"
timestamp: "2026-02-05T12:00:00Z"
source_file: "THOUGHTS.md"
learning_type: "pattern"
title: "Short title"
description: "Full description"
severity: "medium"  # critical, high, medium, low
effectiveness: 0.0  # 0.0 to 1.0
frequency: "one-time"  # recurring, occasional, one-time
category: "technical"
tags: ["python", "yaml"]
related_tasks: ["TASK-YYY"]
content_hash: "abc123..."  # For deduplication
```
