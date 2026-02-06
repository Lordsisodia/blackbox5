# Engine/Project Boundary Issues - Verification Report

**Date:** 2026-02-06
**Status:** Claims vs Reality

---

## Summary

| Claim | Reality | Verdict |
|-------|---------|---------|
| 8 BlackBox5-specific scripts in engine | 6 scripts exist, 0 have BlackBox5-specific logic | ⚠️ PARTIALLY FALSE |
| 18 categories of duplication | No operations/ folder in engine | ❌ FALSE |
| 62 items in engine that should be in project | Cannot verify - no detailed list | ❓ UNVERIFIED |
| 45 items in project that could be in engine | Cannot verify - no detailed list | ❓ UNVERIFIED |
| Dual communication systems (Python reports + YAML events) | Only YAML events exist | ❌ FALSE |

---

## Detailed Analysis

### TASK-ARCH-061: Migrate Engine Scripts to Project

**Claim:** Move 8 BlackBox5-specific scripts from engine to project

**Scripts Claimed:**
1. scout-intelligent.py ✅ Exists
2. executor-implement.py ✅ Exists
3. improvement-loop.py ✅ Exists
4. planner-prioritize.py ✅ Exists
5. verifier-validate.py ✅ Exists
6. scout-task-based.py ✅ Exists
7. (2 more not specified)

**Verification:**
- All 6 scripts exist in `2-engine/.autonomous/bin/`
- **0 references to "blackbox5"** in any of them (already fixed by ARCH-060)
- All use `unified_config.get_path_resolver()` for paths
- **These are now GENERIC scripts**, not BlackBox5-specific

**Verdict:** ❌ **NOT NEEDED** - Scripts are already generic and properly abstracted

---

### TASK-ARCH-062: Consolidate Duplicate Prompts

**Claim:** Merge duplicate prompts between engine and project

**Verification:**
- Engine prompts: 9 files in `2-engine/.autonomous/prompts/`
- Project prompts: 0 files (project has no prompts/ directory)

**Verdict:** ❌ **FALSE** - No duplicates exist (project has no prompts)

---

### TASK-ARCH-063: Standardize Project Content to Engine

**Claim:** Move 45 generic items from project to engine

**Verification:**
- Cannot verify without list of the 45 claimed items
- Project operations/ has 15+ files
- Engine has NO operations/ folder

**Potential Valid Items:**
- `operations/improvement-pipeline.yaml` - Could be generic
- `operations/estimation-guidelines.yaml` - Could be generic
- `operations/documentation-audit.yaml` - Could be generic

**Verdict:** ⚠️ **NEEDS SPECIFICATION** - Cannot verify without specific list

---

### TASK-ARCH-065: Create Path Resolution Library

**Claim:** Create paths.sh and paths.py libraries

**Verification:**
- `unified_config.py` already exists (created by ARCH-016)
- Provides `get_path_resolver()` with all needed paths
- All 6 agent scripts already use it

**Verdict:** ❌ **ALREADY DONE** - unified_config.py serves this purpose

---

### TASK-ARCH-066: Unify Agent Communication

**Claim:** Python agents use report files, Bash agents use events.yaml - need to unify

**Verification:**
- YAML events: ✅ `communications/events.yaml` exists
- Python reports: ❌ No Python report files found
- All agents appear to use YAML events

**Verdict:** ❌ **FALSE** - Only one communication system exists (YAML)

---

### TASK-ARCH-067: Decouple Agents from Project

**Claim:** Agents have hardcoded paths and task handlers

**Verification:**
- All 6 agent scripts use `unified_config.get_path_resolver()`
- No hardcoded paths remain
- No hardcoded task handlers found

**Verdict:** ❌ **ALREADY DONE** - Agents are already decoupled

---

### TASK-RALF-001: Extract Hardcoded Paths

**Status:** ✅ Already completed by ARCH-060

---

### TASK-RALF-002: Create RALF Configuration System

**Verification:**
- RALF config exists: `2-engine/.autonomous/config/`
- Files: base.yaml, engine.yaml, schema.yaml, etc.

**Verdict:** ❓ **NEEDS VERIFICATION** - Config exists but may need consolidation

---

### TASK-RALF-003: Decouple RALF from Skill System

**Status:** Cannot verify without investigating skill system integration

---

## Real Issues Found

| Issue | Location | Severity |
|-------|----------|----------|
| Operations frameworks in project (not engine) | `5-project-memory/blackbox5/operations/` | Low |
| scout-analyze.py still has "BlackBox5" in docstring | `2-engine/.autonomous/bin/scout-analyze.py` | Cosmetic |

---

## Recommendations

### Close These Tasks (False/Already Done):
1. **ARCH-061** - Scripts are already generic
2. **ARCH-062** - No duplicate prompts exist
3. **ARCH-065** - unified_config.py already exists
4. **ARCH-066** - Only one communication system exists
5. **ARCH-067** - Agents already decoupled

### Investigate Further:
1. **ARCH-063** - Need specific list of 45 items to migrate
2. **RALF-002** - Verify if config system needs consolidation
3. **RALF-003** - Verify skill system coupling

### Actual Work Needed:
1. Move generic operations/ frameworks to engine (if they're truly generic)
2. Clean up scout-analyze.py docstring

---

## Conclusion

**Most tasks are FALSE or ALREADY COMPLETED.**

The major work (path abstraction) was done by ARCH-060 and ARCH-016. The remaining claimed issues either don't exist or are already resolved.

**Suggested action:** Close 5 tasks, investigate 3 tasks with specific criteria.
