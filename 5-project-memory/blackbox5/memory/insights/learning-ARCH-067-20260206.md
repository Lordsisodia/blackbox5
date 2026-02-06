# Learning: Agent Decoupling from Hardcoded Paths

**Task:** TASK-ARCH-067
**Date:** 2026-02-06
**Category:** Architecture

---

## What Worked Well

- Simple environment variable approach (`BB5_PROJECT_ROOT`) was effective
- Auto-detection fallback from script location provided graceful degradation
- Pattern of traversing up directory tree (4-5 levels) was reliable
- All 4 bash agents were updated consistently with the same pattern

## What Was Harder Than Expected

- Different agents needed different traversal depths (4 vs 5 levels)
- Maintaining backward compatibility while adding new functionality
- Ensuring all scripts pass `bash -n` syntax validation

## What Would You Do Differently

- Create a shared library/function for path detection instead of duplicating logic
- Standardize directory depth requirements across all agents
- Add validation tests to ensure paths resolve correctly

## Technical Insights

```bash
# Effective pattern for path auto-detection
if [ -n "$BB5_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$BB5_PROJECT_ROOT"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
fi
```

## Process Improvements

- Always provide environment variable override for flexibility
- Document required environment variables in `.env.example`
- Test both modes (env var vs auto-detection) during validation

## Key Takeaway

Environment variables with auto-detection fallback provides both flexibility and ease-of-use for deployment scenarios.
