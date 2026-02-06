# Minimal Documentation Hooks Design

**Date:** 2026-02-06
**Status:** Design Document
**Purpose:** Define the minimum set of hooks needed to ensure BB5 documentation is captured without per-tool overhead

---

## Executive Summary

This document designs a minimal hook architecture for BlackBox5 documentation capture. The design prioritizes:

1. **Zero per-tool overhead** - No PreToolUse/PostToolUse hooks
2. **Complete coverage** - All agents (normal + subagents) document properly
3. **Context preservation** - Documentation survives context compaction
4. **Validation at boundaries** - Check docs exist when it matters

---

## The 5-Hook Minimal Set

| Hook | Trigger | Documentation Purpose |
|------|---------|----------------------|
| **SessionStart** | New session begins | Create documentation templates |
| **SubagentStart** | Subagent spawns | Inject parent context + create templates |
| **PreCompact** | Context compaction imminent | Preserve documentation to disk |
| **SubagentStop** | Subagent ends | Capture results back to parent |
| **Stop** | Session ends | Validate documentation completeness |

---

## Hook 1: SessionStart - Template Creation

### When It Runs
- Every new Claude Code session start
- Both normal agents and subagents (subagent has its own SessionStart)

### What It Does

```bash
# 1. Detect run directory
RUN_DIR=$(detect_run_directory)  # From RALF_RUN_DIR, cwd, or .agent-context

# 2. Create documentation templates if they don't exist
for file in THOUGHTS.md DECISIONS.md ASSUMPTIONS.md LEARNINGS.md RESULTS.md; do
    if [ ! -f "$RUN_DIR/$file" ]; then
        create_template "$RUN_DIR/$file"
    fi
done

# 3. Load parent context if this is a subagent
if is_subagent; then
    inject_parent_context
fi
```

### Template Content (THOUGHTS.md Example)

```markdown
# THOUGHTS: [Run Name]

**Started:** [TIMESTAMP]
**Agent Type:** [planner|executor|architect|unknown]
**Parent Task:** [TASK-ID or "N/A"]

## Session Objectives

<!-- Document what you aim to accomplish in this session -->
- [ ] Objective 1
- [ ] Objective 2

## Key Decisions

<!-- Record significant decisions and their rationale -->

## Assumptions Made

<!-- Note any assumptions that could affect outcomes -->

## Progress Log

<!-- Chronological record of work done -->

---

*Session started: [TIMESTAMP]*
```

### Key Design Decisions

1. **Templates are created empty** - No unfilled markers to track
2. **Idempotent** - Safe to run multiple times (won't overwrite existing)
3. **Self-documenting** - Comments guide the agent on what to write
4. **Minimal** - Only 5 files, focused on high-value capture

---

## Hook 2: SubagentStart - Context Injection

### When It Runs
- Immediately before a subagent session starts
- Called via subagent-tracking.sh with "start" argument

### What It Does

```bash
# 1. Detect parent context
PARENT_RUN_DIR=$(pwd)
PARENT_TASK=$(extract_task_from_context)
PARENT_AGENT_TYPE=$(detect_agent_type)

# 2. Prepare subagent context file
cat > "$BB5_DIR/.agent-context" << EOF
parent_run_dir: "$PARENT_RUN_DIR"
parent_task: "$PARENT_TASK"
parent_agent_type: "$PARENT_AGENT_TYPE"
parent_thoughts: "$PARENT_RUN_DIR/THOUGHTS.md"
timestamp: "$(date -Iseconds)"
EOF

# 3. Subagent's SessionStart will read this and:
#    - Create its own templates
#    - Add "Parent Context" section to THOUGHTS.md
#    - Know it's a subagent (affects validation rules)
```

### Context Flow

```
Parent Agent                    Subagent
------------                    --------
THOUGHTS.md ---(reference)--->  THOUGHTS.md
    |                               |
    |                            "Parent Context" section
    |                            links back to parent
    v                               |
DECISIONS.md <---(results)-----  DECISIONS.md
    ^                               |
    |_______________________________|
         (on SubagentStop)
```

### Key Design Decisions

1. **File-based context passing** - No environment variables needed
2. **Reference, not copy** - Subagent references parent's docs, doesn't duplicate
3. **Bidirectional link** - Parent knows subagent exists, subagent knows parent

---

## Hook 3: PreCompact - Documentation Preservation

### When It Runs
- Before Claude Code compacts context (removes old messages)
- NOT on every tool use - only at compaction boundaries

### What It Does

```bash
# 1. Read input (compaction metadata)
read -r input

# 2. Check if documentation needs preservation
RUN_DIR=$(detect_run_directory)

# 3. Ensure all docs are flushed to disk
for file in THOUGHTS.md DECISIONS.md ASSUMPTIONS.md LEARNINGS.md RESULTS.md; do
    if [ -f "$RUN_DIR/$file" ]; then
        # File exists - ensure it's persisted (sync to disk)
        sync "$RUN_DIR/$file" 2>/dev/null || true
    fi
done

# 4. Optional: Create compact summary if THOUGHTS.md is large
THOUGHTS_SIZE=$(stat -f%z "$RUN_DIR/THOUGHTS.md" 2>/dev/null || echo "0")
if [ "$THOUGHTS_SIZE" -gt 50000 ]; then  # > 50KB
    create_thoughts_summary "$RUN_DIR"
fi

# 5. Allow compaction to proceed
echo '{"continue": true}'
```

### Preservation Strategy

| Risk | Mitigation |
|------|------------|
| Docs only in context | Force flush to disk before compaction |
| Large THOUGHTS.md | Create summary for context window |
| Context loss | Disk is source of truth, not context |

### Key Design Decisions

1. **Disk is source of truth** - Always read from disk, not context
2. **Minimal intervention** - Just ensure persistence, don't block
3. **Summarization optional** - Only for very large files

---

## Hook 4: SubagentStop - Result Capture

### When It Runs
- When subagent session ends
- Called via subagent-tracking.sh with "stop" argument

### What It Does

```bash
# 1. Load persisted context
source "$BB5_DIR/.agent-context"

# 2. Find subagent's run directory
SUBAGENT_RUN_DIR=$(find_subagent_run_dir)

# 3. Capture subagent's key outputs
if [ -f "$SUBAGENT_RUN_DIR/RESULTS.md" ]; then
    SUBAGENT_RESULTS=$(cat "$SUBAGENT_RUN_DIR/RESULTS.md")
fi

if [ -f "$SUBAGENT_RUN_DIR/DECISIONS.md" ]; then
    SUBAGENT_DECISIONS=$(cat "$SUBAGENT_RUN_DIR/DECISIONS.md")
fi

# 4. Append to parent's documentation
cat >> "$parent_run_dir/THOUGHTS.md" << EOF

---

## Subagent Results: $(basename "$SUBAGENT_RUN_DIR")

**Completed:** $(date -Iseconds)

### Summary
$(extract_summary "$SUBAGENT_RUN_DIR/RESULTS.md")

### Key Decisions
$(extract_decisions "$SUBAGENT_RUN_DIR/DECISIONS.md")

### Full Output Location
$SUBAGENT_RUN_DIR/
EOF

# 5. Clean up context file
rm -f "$BB5_DIR/.agent-context"

# 6. Log event
echo "Subagent results captured in parent THOUGHTS.md"
```

### Result Capture Flow

```
Subagent Completes
       |
       v
+------------------+
| Read RESULTS.md  |
| Read DECISIONS.md|
| Read LEARNINGS.md|
+------------------+
       |
       v
+------------------+
| Append summary   |
| to parent's      |
| THOUGHTS.md      |
+------------------+
       |
       v
Parent has full
context of what
subagent did
```

### Key Design Decisions

1. **Append, don't replace** - Parent keeps their own thoughts + subagent summary
2. **Reference full output** - Parent can dive deeper if needed
3. **Clean up context** - Remove .agent-context after use

---

## Hook 5: Stop - Validation & Enforcement

### When It Runs
- When Claude Code session ends (user exits or session timeout)
- Final checkpoint before agent disappears

### What It Does

```bash
# 1. Detect run directory
RUN_DIR=$(detect_run_directory)

# 2. Define required files
REQUIRED_FILES=("THOUGHTS.md" "RESULTS.md")
OPTIONAL_FILES=("DECISIONS.md" "ASSUMPTIONS.md" "LEARNINGS.md")

# 3. Check each required file
ISSUES=0
for file in "${REQUIRED_FILES[@]}"; do
    filepath="$RUN_DIR/$file"

    if [ ! -f "$filepath" ]; then
        echo "MISSING: $file"
        ISSUES=$((ISSUES + 1))
    elif [ ! -s "$filepath" ]; then  # Empty file
        echo "EMPTY: $file"
        ISSUES=$((ISSUES + 1))
    elif is_template_only "$filepath"; then
        echo "TEMPLATE_ONLY: $file (no content added)"
        ISSUES=$((ISSUES + 1))
    fi
done

# 4. Check optional files (warn only)
for file in "${OPTIONAL_FILES[@]}"; do
    filepath="$RUN_DIR/$file"
    if [ ! -f "$filepath" ]; then
        echo "OPTIONAL_MISSING: $file (not required)"
    fi
done

# 5. Handle validation result
case "${BB5_DOC_VALIDATION_MODE:-warn}" in
    "strict")
        if [ $ISSUES -gt 0 ]; then
            echo "Documentation validation FAILED (strict mode)"
            echo "Fix issues or set BB5_DOC_VALIDATION_MODE=warn"
            exit 1  # Block session end
        fi
        ;;
    "block")
        if [ $ISSUES -gt 0 ]; then
            echo "Documentation validation FAILED (block mode)"
            read -p "Press Enter to force exit (not recommended)..."
            exit 1  # Block session end
        fi
        ;;
    "warn"|*)
        if [ $ISSUES -gt 0 ]; then
            echo "WARNING: Documentation incomplete ($ISSUES issues)"
            echo "Run validation: bb5 validate:docs"
        fi
        ;;
esac

exit 0
```

### Validation Levels

| Mode | Behavior | Use Case |
|------|----------|----------|
| `strict` | Block exit if docs incomplete | Production agents |
| `block` | Block with prompt to override | Development |
| `warn` | Warn but allow exit (default) | Exploration |

### Key Design Decisions

1. **Minimum required: THOUGHTS.md + RESULTS.md** - Core capture
2. **Optional files tracked but not enforced** - Flexibility for different tasks
3. **Template detection** - Check if agent actually wrote anything
4. **Configurable strictness** - Different modes for different contexts

---

## Documentation Flow Through System

### Normal Agent Flow

```
SessionStart
    |
    v
Create Templates --------> THOUGHTS.md (empty template)
    |                      DECISIONS.md (empty template)
    |                      ASSUMPTIONS.md (empty template)
    |                      LEARNINGS.md (empty template)
    |                      RESULTS.md (empty template)
    |
    v
[Agent Works]
    |
    v
PreCompact (if triggered)
    |
    v
Flush docs to disk
    |
    v
Stop
    |
    v
Validate docs exist & have content
    |
    v
Session ends (docs preserved)
```

### Subagent Flow

```
Parent Agent                Subagent
------------                --------
    |                           |
    |---- SubagentStart ---->   |
    |     (write .agent-context)|
    |                           |
    |                       SessionStart
    |                           |
    |                       Create Templates
    |                       + Parent Context section
    |                           |
    |                       [Subagent Works]
    |                           |
    |<---- SubagentStop ------|
    |     (read .agent-context)|
    |     (capture results)     |
    |                           |
    v                           v
Parent THOUGHTS.md now
contains subagent summary
```

---

## Validation Points

### 1. Does Documentation Exist?

**When:** SessionStart hook
**Check:** Create if missing
**Action:** Generate templates

### 2. Is Documentation Complete?

**When:** Stop hook
**Check:**
- Required files exist (THOUGHTS.md, RESULTS.md)
- Files are not empty
- Files contain more than just template headers
**Action:** Warn or block based on mode

### 3. Is Documentation Preserved?

**When:** PreCompact hook
**Check:** Files are on disk
**Action:** Ensure sync to disk

### 4. Is Subagent Documentation Captured?

**When:** SubagentStop hook
**Check:** Subagent has RESULTS.md
**Action:** Append summary to parent THOUGHTS.md

---

## Handling Missing Documentation

### Scenario 1: Missing at SessionStart
**Action:** Create templates automatically
**No user intervention needed**

### Scenario 2: Missing at Stop (Warn Mode)
**Action:**
1. Print warning message
2. List missing files
3. Suggest: "Run `bb5 validate:docs` for details"
4. Allow exit

### Scenario 3: Missing at Stop (Strict Mode)
**Action:**
1. Print error message
2. List specific issues
3. Block exit with instructions
4. Require: Fix issues OR override with env var

### Scenario 4: Subagent Missing Documentation
**Action:**
1. Log to events.yaml
2. Still capture what exists
3. Warn parent agent
4. Don't block (subagent may have failed)

---

## Implementation Files

### New Files to Create

```
~/.blackbox5/.claude/hooks/
├── session-start-docs.sh      # Hook 1: Template creation
├── subagent-context.sh        # Hook 2 & 4: Start/stop handling
├── pre-compact-preserve.sh    # Hook 3: Preservation
└── stop-validate-docs.sh      # Hook 5: Validation (exists, needs update)
```

### Supporting Infrastructure

```
~/.blackbox5/5-project-memory/blackbox5/
├── .autonomous/
│   └── hooks/
│       ├── templates/         # Documentation templates
│       │   ├── THOUGHTS.md.template
│       │   ├── DECISIONS.md.template
│       │   ├── ASSUMPTIONS.md.template
│       │   ├── LEARNINGS.md.template
│       │   └── RESULTS.md.template
│       └── lib/
│           └── hook-utils.sh  # Shared functions
└── bin/
    └── bb5-validate-docs      # CLI validation tool
```

---

## Comparison: Minimal vs. Comprehensive

| Approach | Hooks | Coverage | Overhead | Best For |
|----------|-------|----------|----------|----------|
| **Minimal (this design)** | 5 | Complete | Zero per-tool | Production systems |
| Comprehensive | 15+ | Exhaustive | Per-tool hooks | Debugging/auditing |
| None | 0 | None | Zero | Quick tasks |

### Why Not Per-Tool Hooks?

| Approach | Cost | Benefit |
|----------|------|---------|
| PreToolUse/PostToolUse | High (every tool call) | Detailed trace |
| Session boundaries | Low (5 hooks total) | Complete capture |

**Per-tool hooks are 10-100x more expensive** for marginal benefit.

---

## Success Metrics

### Coverage Metrics

- [ ] 100% of sessions have THOUGHTS.md
- [ ] 100% of sessions have RESULTS.md
- [ ] 100% of subagent results captured in parent
- [ ] 0% documentation loss during context compaction

### Quality Metrics

- [ ] THOUGHTS.md average > 500 characters
- [ ] RESULTS.md contains actionable outcomes
- [ ] DECISIONS.md records key choices
- [ ] LEARNINGS.md captures insights

### Efficiency Metrics

- [ ] Hook execution < 100ms each
- [ ] No per-tool overhead
- [ ] Zero blocking in warn mode

---

## Rollout Plan

### Phase 1: Core Hooks (Week 1)
1. Implement SessionStart hook
2. Implement Stop hook (update existing)
3. Test with normal agents

### Phase 2: Subagent Support (Week 2)
1. Implement SubagentStart hook
2. Implement SubagentStop hook
3. Test with subagent workflows

### Phase 3: Preservation (Week 3)
1. Implement PreCompact hook
2. Test with long-running sessions
3. Verify no data loss

### Phase 4: Validation (Week 4)
1. Add bb5-validate-docs CLI
2. Configure validation modes
3. Train agents on new workflow

---

## Appendix: Template Examples

### RESULTS.md Template

```markdown
# RESULTS: [Run Name]

**Completed:** [TIMESTAMP]
**Status:** [complete|partial|blocked]

## Outcomes

<!-- What was actually achieved -->

## Deliverables

<!-- Files created, code written, decisions made -->
- [ ] Deliverable 1
- [ ] Deliverable 2

## Next Steps

<!-- What should happen next -->

## Blockers (if any)

<!-- What prevented completion -->

---

*Session completed: [TIMESTAMP]*
```

### DECISIONS.md Template

```markdown
# DECISIONS: [Run Name]

## Decision Log

### [TIMESTAMP] - Decision Title

**Context:** Why this decision was needed

**Options Considered:**
1. Option A
2. Option B

**Decision:** Which option was chosen

**Rationale:** Why this option

**Consequences:** What this enables/prevents

---
```

---

## Conclusion

This minimal hook design captures complete documentation with only 5 hooks:

1. **SessionStart** - Creates templates
2. **SubagentStart** - Injects context
3. **PreCompact** - Preserves to disk
4. **SubagentStop** - Captures results
5. **Stop** - Validates completeness

**Zero per-tool overhead. Complete coverage. Context preservation.**
