# Learning: Script Migration (Engine to Project)

**Task:** TASK-ARCH-061
**Date:** 2026-02-06
**Category:** Architecture

---

## What Worked Well

- Clear separation of concerns - project-specific scripts belong in project
- Moving 4 scripts was straightforward file operations
- Import path updates were minimal (only `improvement-loop.py` needed BIN_DIR change)

## What Was Harder Than Expected

- Scripts use `sys.path.insert()` to find `unified_config` - this needed careful handling
- Verifying all 4 scripts (3/4 OK, 1 pre-existing issue) took time
- Ensuring cross-directory references still worked after migration

## What Would You Do Differently

- Create the destination directory structure first
- Verify import strategy before moving files
- Have automated tests ready to validate script functionality

## Technical Insights

- Scripts using `Path(__file__).parent.parent / "lib"` pattern need special attention when moved
- Engine's `unified_config` can still be accessed via path resolver
- Thin wrappers in engine can maintain backward compatibility

## Process Improvements

- Always verify script syntax with `python -m py_compile` before and after migration
- Document which scripts have dependencies on engine libraries
- Create a migration checklist for future similar tasks

## Key Takeaway

When migrating scripts between directories, always verify import paths and cross-directory references work correctly after the move.
