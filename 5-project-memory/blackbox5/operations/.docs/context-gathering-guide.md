# Context Gathering Optimization Guide

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/context-gathering.yaml`

**Purpose:** Reduce "missed file" errors and improve cross-project task execution efficiency

---

## Quick Start

### For RALF-Executor

At the start of each run:

1. **Read this configuration file**
2. **Analyze the task** for cross-project indicators
3. **Apply automatic reads** based on task type
4. **Validate paths** before file operations

```yaml
# Automatic reads for all tasks:
- .autonomous/routes.yaml    # Project routing
- STATE.yaml                 # Project state (if exists)

# Additional reads for cross-project tasks:
- operations/project-map.yaml           # Cross-project dependencies
- 2-engine/.autonomous/routes.yaml      # Engine routing
```

---

## Heuristics for Cross-Project Detection

### 1. Engine Dependency Detection

**Trigger:** Task involves BMAD commands, skills, or workflows

**Indicators:**
- BMAD command mentioned (CP, VP, EP, CA, VA, BP, RS, etc.)
- "skill" or "workflow" mentioned
- "2-engine" path referenced

**Required Reads:**
- `2-engine/.autonomous/routes.yaml`
- `2-engine/.autonomous/skills/`

**Example Task:** "Create a new BMAD skill for code review"

### 2. Pattern Reference Detection

**Trigger:** Task involves project structure or organization

**Indicators:**
- "STATE.yaml" mentioned
- "siso-internal" mentioned
- "project structure" or "organization" referenced

**Required Reads:**
- `5-project-memory/siso-internal/STATE.yaml`
- `operations/project-map.yaml`

**Example Task:** "Replicate siso-internal folder structure"

### 3. Cross-Project Documentation

**Trigger:** Creating documentation that applies to multiple projects

**Indicators:**
- "documentation" creation mentioned
- Multiple project paths referenced
- ".docs/" folder mentioned

**Required Reads:**
- `operations/project-map.yaml`
- `.autonomous/routes.yaml`

**Example Task:** "Create documentation for cross-project workflow"

### 4. Shared Configuration Detection

**Trigger:** Task involves CLAUDE.md or other shared files

**Indicators:**
- "CLAUDE.md" mentioned
- "~/.claude/" path referenced
- "shared configuration" mentioned

**Required Reads:**
- `~/.claude/CLAUDE.md`
- `operations/project-map.yaml` (shared_files section)

**Example Task:** "Update decision framework in CLAUDE.md"

### 5. Multi-Project Task Detection

**Trigger:** Task explicitly spans multiple projects

**Indicators:**
- Multiple project names in task (2-engine, siso-internal, blackbox5)
- "cross-project" or "multi-project" mentioned

**Required Reads:**
- `operations/project-map.yaml`
- `.autonomous/routes.yaml`
- `2-engine/.autonomous/routes.yaml`

**Example Task:** "Implement context gathering optimization across projects"

---

## Automatic Reads by Task Type

| Task Type | Automatic Reads | Condition |
|-----------|----------------|-----------|
| **All Tasks** | `.autonomous/routes.yaml` | Always |
| | `STATE.yaml` | If exists |
| **Cross-Project** | `operations/project-map.yaml` | If multi-project detected |
| | `2-engine/.autonomous/routes.yaml` | If engine involved |
| **Documentation** | `.docs/` folder | If creating docs |
| **Implementation** | `operations/validation-checklist.yaml` | Always |

---

## Path Validation Rules

### Before Any File Operation:

1. **Use absolute paths** - Never relative paths
2. **Verify file exists** - Check before attempting read
3. **Check project-map.yaml** - For cross-project paths
4. **Use routes.yaml** - For path resolution

### Cross-Project Path Patterns:

| Pattern | Validation | Example |
|---------|------------|---------|
| `../../2-engine/` | Check engine routes | `../../2-engine/.autonomous/routes.yaml` |
| `../../5-project-memory/` | Check project map | `../../5-project-memory/siso-internal/` |
| `~/.claude/` | Check exists | `~/.claude/CLAUDE.md` |

---

## Cached Files

These files are accessed frequently and should be cached:

| File | Cache Duration | Priority |
|------|---------------|----------|
| `~/.claude/CLAUDE.md` | 1 hour | High |
| `2-engine/.autonomous/routes.yaml` | 30 minutes | High |
| `.autonomous/routes.yaml` | 30 minutes | High |
| `operations/project-map.yaml` | 1 hour | Medium |
| `STATE.yaml` | 15 minutes | Medium |

---

## Integration with Run Initialization

### Step-by-Step for Executor:

```yaml
Run Initialization:
  1. Read context-gathering.yaml (this config)
  2. Read .autonomous/routes.yaml
  3. Read STATE.yaml (if exists)
  4. Analyze task file for indicators:
     - Scan for BMAD commands
     - Scan for project names
     - Scan for cross-project keywords
  5. Apply heuristics:
     - If engine indicators → Read 2-engine/routes.yaml
     - If multi-project → Read project-map.yaml
     - If shared config → Check shared_files section
  6. Validate all paths before reads
  7. Cache frequently accessed files
  8. Begin task execution
```

---

## Examples

### Example 1: BMAD Skill Task

**Task:** "Create a new skill for code review"

**Context Gathering:**
1. Read `.autonomous/routes.yaml` (always)
2. Detect "skill" keyword → Engine dependency
3. Read `2-engine/.autonomous/routes.yaml`
4. Read `2-engine/.autonomous/skills/` directory
5. Check `operations/project-map.yaml` for skill dependencies

### Example 2: Pattern Replication Task

**Task:** "Replicate siso-internal STATE.yaml structure"

**Context Gathering:**
1. Read `.autonomous/routes.yaml` (always)
2. Detect "siso-internal" → Pattern reference
3. Read `operations/project-map.yaml`
4. Read `5-project-memory/siso-internal/STATE.yaml`
5. Read current `STATE.yaml`

### Example 3: CLAUDE.md Update Task

**Task:** "Update decision framework in CLAUDE.md"

**Context Gathering:**
1. Read `.autonomous/routes.yaml` (always)
2. Detect "CLAUDE.md" → Shared configuration
3. Read `~/.claude/CLAUDE.md`
4. Read `operations/project-map.yaml` (shared_files section)
5. Identify all affected projects

---

## Effectiveness Metrics

Track these metrics to measure optimization success:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Missed file errors | < 1 per run | Check RESULTS.md for errors |
| Context gathering time | < 2 minutes | Timestamp in THOUGHTS.md |
| Cross-project detection rate | > 90% | Manual review |

### Monthly Review

1. Review metrics from last month
2. Update heuristics based on new patterns
3. Add new cross-project relationships to project-map.yaml
4. Document learnings in `knowledge/analysis/`

---

## Troubleshooting

### "Missed file" error still occurred

1. Check if file is in `operations/project-map.yaml` shared_files
2. Verify heuristic didn't trigger (check task keywords)
3. Add new heuristic if this is a new pattern
4. Update this guide with the new case

### Cross-project task not detected

1. Review task keywords against detection patterns
2. Check threshold settings (may need adjustment)
3. Add missing keywords to detection config

### Path validation failing

1. Verify path exists: `ls -la [path]`
2. Check routes.yaml for correct path mapping
3. Use absolute paths only

---

## Related Files

- `operations/project-map.yaml` - Cross-project relationship map
- `operations/validation-checklist.yaml` - Pre-execution validation
- `.autonomous/routes.yaml` - Project routing configuration
- `2-engine/.autonomous/routes.yaml` - Engine routing configuration

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial context gathering optimization guide |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│           CONTEXT GATHERING QUICK REFERENCE             │
├─────────────────────────────────────────────────────────┤
│ ALWAYS READ:                                            │
│   - .autonomous/routes.yaml                             │
│   - STATE.yaml (if exists)                              │
├─────────────────────────────────────────────────────────┤
│ IF BMAD/SKILL MENTIONED:                                │
│   - 2-engine/.autonomous/routes.yaml                    │
│   - 2-engine/.autonomous/skills/                        │
├─────────────────────────────────────────────────────────┤
│ IF SISO-INTERNAL MENTIONED:                             │
│   - operations/project-map.yaml                         │
│   - 5-project-memory/siso-internal/STATE.yaml           │
├─────────────────────────────────────────────────────────┤
│ IF CLAUDE.MD MENTIONED:                                 │
│   - ~/.claude/CLAUDE.md                                 │
│   - operations/project-map.yaml (shared_files)          │
├─────────────────────────────────────────────────────────┤
│ VALIDATE:                                               │
│   - Use absolute paths                                  │
│   - Verify before read                                  │
│   - Check project-map for cross-project                 │
└─────────────────────────────────────────────────────────┘
```
