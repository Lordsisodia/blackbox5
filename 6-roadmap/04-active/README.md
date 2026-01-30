# Active Plans

**Status**: Currently In Progress  
**Location**: `6-roadmap/04-active/`

---

## Overview

This directory contains plans that are currently being executed.

Active plans have moved from `03-planned/` and are in the execution phase.

---

## Current Active Plans

### PLAN-008: Fix Critical API Mismatches
**Folder**: `PLAN-008-fix-critical-api-mismatches/`  
**Started**: 2026-01-20  
**Status**: Active

**Contents**:
- `CHANGELOG.md` - Progress changelog
- `COMPLETION-REPORT.md` - Completion report
- `SUMMARY.md` - Executive summary

---

## Structure

Each active plan folder contains:

```
PLAN-XXX-name/
├── metadata.yaml      # Plan metadata (status: active)
├── README.md          # Summary (optional)
├── CHANGELOG.md       # Progress updates
├── COMPLETION-REPORT.md  # Final report
├── SUMMARY.md         # Executive summary
└── outputs/           # Generated artifacts (optional)
```

---

## Workflow

### Moving to Active
1. Move from `03-planned/`: `mv 03-planned/PLAN-XXX 04-active/PLAN-XXX`
2. Update `metadata.yaml`: set `status: active`
3. Update `STATE.yaml`: move from `planned` to `active`
4. Create `CHANGELOG.md` to track progress

### Completing
1. Create `COMPLETION-REPORT.md`
2. Move to `05-completed/YYYY/`: `mv 04-active/PLAN-XXX 05-completed/2026/PLAN-XXX`
3. Update `metadata.yaml`: set `status: completed`
4. Update `STATE.yaml`: move from `active` to `completed`

---

*See ../STRUCTURE.md for full roadmap documentation.*
