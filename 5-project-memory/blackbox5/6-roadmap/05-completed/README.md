# Completed Plans

**Status**: Shipped / Completed  
**Location**: `6-roadmap/05-completed/`

---

## Overview

This directory contains plans that have been completed and shipped.

Completed plans are organized by year for historical tracking.

---

## Structure

```
05-completed/
├── README.md           # This file
├── 2026/               # Completed items in 2026
│   ├── 01-january/
│   ├── 02-february/
│   ├── 03-march/
│   ├── 04-april/
│   ├── 05-may/
│   ├── 06-june/
│   ├── 07-july/
│   ├── 08-august/
│   ├── 09-september/
│   ├── 10-october/
│   ├── 11-november/
│   └── 12-december/
└── YYYY/               # Future years
```

---

## Current Organization

### 2026
Completed items from 2026 are organized by month:
- `01-january/` - January completions
- `02-february/` - February completions
- `03-march/` - March completions
- ...and so on

---

## Item Structure

Each completed plan:

```
PLAN-XXX-name/
├── metadata.yaml      # Plan metadata (status: completed)
├── report.md          # Completion report
└── artifacts/         # Deliverables (optional)
```

---

## Usage

### Finding Completed Work

Browse by year and month:
```bash
# List all 2026 completions
ls 05-completed/2026/

# List January 2026 completions
ls 05-completed/2026/01-january/
```

### Moving Completed Items

When a plan is completed:

```bash
# From 04-active/
mv 04-active/PLAN-XXX-name 05-completed/2026/01-january/PLAN-XXX-name

# Update metadata.yaml: status: completed
# Update STATE.yaml: move from active to completed
```

---

## Purpose

- Historical record of shipped work
- Reference for future similar work
- Metrics and reporting source
- Knowledge preservation

---

*See ../STRUCTURE.md for full roadmap documentation.*
