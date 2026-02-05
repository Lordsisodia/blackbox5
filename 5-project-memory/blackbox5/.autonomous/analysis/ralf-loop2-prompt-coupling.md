# RALF Loop 2 Analysis: Prompt Template Coupling

## Executive Summary

RALF's prompt templates contain **extensive BlackBox5-specific coupling** that Loop 1 missed. The prompts have 40+ hardcoded references to "BlackBox5", assume BB5 directory structure, and embed BB5-specific concepts throughout.

## Critical Findings

### 1. Hardcoded Project Name (40+ occurrences)
**Files affected:** Almost all prompt files

Examples:
- `ralf.md` line 16: "You have FULL ACCESS to ALL of blackbox5."
- `ralf-executor.md` line 27: "You are RALF-Executor operating on BlackBox5."
- `ralf-improvement-loop.md` line 52: "Analyze BlackBox5 for improvement opportunities"
- `intelligent-scout.md` line 11: "You are an Intelligent Scout - an AI agent that deeply analyzes BlackBox5"

### 2. Hardcoded Directory Structure Assumptions

| Assumed Path | Problem | Files Affected |
|--------------|---------|----------------|
| `2-engine/` | BB5 numbering scheme | ralf.md, bb5-infrastructure.md |
| `5-project-memory/` | BB5 numbering scheme | ralf.md, six-agent-pipeline.md |
| `operations/` | BB5-specific directory | ralf-executor.md, ralf-improvement-loop.md, intelligent-scout.md |
| `.autonomous/` | Assumed project structure | intelligent-scout.md, deep-repo-scout.md |
| `runs/` | Assumed run directory | improvement-scout.md |

### 3. Hardcoded File Paths in Prompts

**ralf-executor.md lines 200-205:**
```
cat $RALF_PROJECT_DIR/operations/skill-usage.yaml
cat $RALF_PROJECT_DIR/operations/skill-selection.yaml
```

**intelligent-scout.md lines 44-47:**
```
**Files to analyze:**
- `operations/skill-metrics.yaml`
- `operations/skill-usage.yaml`
- `operations/skill-selection.yaml`
```

**improvement-scout.md lines 121-125:**
```
**Files to analyze:**
- `operations/improvement-backlog.yaml`
- `operations/improvement-metrics.yaml`
- `operations/improvement-pipeline.yaml`
- `STATE.yaml`
```

### 4. BlackBox5-Specific Concepts Embedded

- "Superintelligence Protocol" (BB5-specific feature)
- Skill system integration (assumes BB5 operations/ structure)
- Improvement loop (assumes BB5 metrics files)
- Queue system (assumes BB5 communications/ structure)
- Task ID format (TASK-XXX)

### 5. Most Critical: Context Files

**bb5-infrastructure.md** - Entire file is BB5-specific:
- Lines 11-26: Hardcoded BB5 directory structure
- Lines 32-36: Specific project names (siso-internal, ralf-core)
- Lines 86-93: Legacy BB5 references

**project-specific.md** - Contains hardcoded project details:
- Lines 9-30: E-Commerce Client Project section
- Lines 32-50: SISO Internal App section

## Decoupling Recommendations

### Immediate (High Priority)
1. Replace all "BlackBox5" with `$RALF_PROJECT_NAME` or generic "the project"
2. Make all BB5-specific file references optional (check existence)
3. Remove hardcoded paths from prompts

### Medium Priority
4. Create project discovery protocol instead of assuming structure
5. Abstract skill system (make optional)
6. Create template system for prompts (Jinja2)

### Long Term
7. Define RALF Project Interface
8. Create project adapters (BB5 adapter, generic adapter)
9. Separate engine from project assumptions completely

## Files Requiring Complete Rewrite

1. `prompts/context/bb5-infrastructure.md` - Should be template
2. `prompts/context/project-specific.md` - Should be loaded from project

## Impact

**Without these changes, RALF cannot be used on any project other than BlackBox5.**
The prompts assume BB5-specific structure, features, and naming throughout.
