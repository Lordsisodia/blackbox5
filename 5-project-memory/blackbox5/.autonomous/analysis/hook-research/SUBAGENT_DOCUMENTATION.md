# Subagent Documentation and Handoff Hooks Research

**Research Date:** 2026-02-06
**Scope:** Analysis of subagent lifecycle documentation requirements
**Purpose:** Define hooks needed for subagent documentation capture and parent handoffs

---

## Executive Summary

Subagent execution in BB5 requires a structured documentation flow that ensures:
1. **Context inheritance** - Subagent receives necessary parent context
2. **Documentation production** - Subagent creates required artifacts during execution
3. **Result handoff** - Parent receives and integrates subagent outputs
4. **Validation** - Documentation completeness is verified before completion

This document specifies the hooks, file formats, and validation rules needed for effective subagent documentation management.

---

## 1. Subagent Lifecycle Documentation Flow

### 1.1 Lifecycle Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SUBAGENT DOCUMENTATION LIFECYCLE                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  PARENT AGENT                    SUBAGENT                        PARENT AGENT    │
│  ─────────────                   ────────                        ─────────────   │
│                                                                                  │
│  ┌──────────────┐                                               ┌──────────────┐ │
│  │ Spawn        │─── SubagentStart Hook ───►┌──────────────┐    │              │ │
│  │ Subagent     │    - Inject context       │ Initialize   │    │              │ │
│  │              │    - Set doc requirements │ Run Folder   │    │              │ │
│  └──────────────┘    - Pass parent THOUGHTS│              │    │              │ │
│                                              └──────────────┘    │              │ │
│                                                       │          │              │ │
│                                               Execute Task       │              │ │
│                                                       │          │              │ │
│                                              ┌──────────────┐    │              │ │
│                                              │ Document     │    │              │ │
│                                              │ Progress     │    │              │ │
│                                              │ (THOUGHTS.md)│    │              │ │
│                                              └──────────────┘    │              │ │
│                                                       │          │              │ │
│                                              Complete Task       │              │ │
│                                                       │          │              │ │
│                                              ┌──────────────┐    │              │ │
│                                              │ SubagentStop │    │              │ │
│                                              │ Hook         │───►│ Integrate    │ │
│                                              │ - Validate   │    │ Results      │ │
│                                              │   docs       │    │              │ │
│                                              │ - Write      │    │              │ │
│                                              │   events.yaml│    │              │ │
│                                              └──────────────┘    └──────────────┘ │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Documentation Handoff Matrix

| Phase | Parent Action | Subagent Action | Files Exchanged |
|-------|---------------|-----------------|-----------------|
| **Start** | Spawn subagent with context | Receive context, create run folder | Parent THOUGHTS.md, DECISIONS.md -> Subagent |
| **During** | Monitor progress (optional) | Document in THOUGHTS.md | None (async) |
| **Stop** | Wait for completion signal | Validate docs, write RESULTS.md | Subagent RESULTS.md, LEARNINGS.md -> Parent |

---

## 2. Required Documentation Files

### 2.1 Subagent Run Folder Structure

```
runs/
└── {agent_type}/
    └── active/
        └── {run_id}/
            ├── THOUGHTS.md          # Required - Agent reasoning log
            ├── RESULTS.md           # Required - Outcomes and deliverables
            ├── DECISIONS.md         # Required - Key decisions made
            ├── LEARNINGS.md         # Required - Insights and patterns
            ├── ASSUMPTIONS.md       # Optional - Verified assumptions
            ├── metadata.yaml        # Required - Run metadata
            ├── task_state.json      # Required - Task tracking
            └── .hook_initialized    # Required - Hook marker
```

### 2.2 File Specifications

#### THOUGHTS.md (Required)

**Purpose:** Capture agent reasoning and thought process

**Template:**
```markdown
# THOUGHTS - Run {run_id}

**Project:** {project}
**Agent:** {agent_type}
**Run ID:** {run_id}
**Started:** {timestamp}

---

## State Assessment

### Current System Status
- **Active Tasks:**
- **Queue Depth:**
- **Previous Run Status:**

### Context
- **Git Branch:** {branch}
- **Git Commit:** {commit}

---

## Analysis

[Agent reasoning goes here]

---

## Skill Usage for This Task

- **Applicable skills found:** [skill names or "None"]
- **Skill invoked:** [skill name or "None"]
- **Confidence percentage:** [0-100%]
- **Rationale for decision:** [explanation]

---

## Next Steps

1.
2.
3.

---

*Hook-generated template. Edit as needed.*
```

#### RESULTS.md (Required)

**Purpose:** Document outcomes, deliverables, and task completion status

**Template:**
```markdown
# RESULTS - Run {run_id}

**Project:** {project}
**Status:** {in_progress|completed|failed|partial|blocked}
**Started:** {timestamp}
**Completed:** {timestamp}

---

## Summary

[What was accomplished in this run]

---

## Tasks Completed

- [ ] Task 1
- [ ] Task 2

---

## Deliverables

| File | Description | Status |
|------|-------------|--------|
| path/to/file | Description | created/modified |

---

## Blockers

- None / [List blockers]

---

## Parent Handoff Notes

[Information parent needs to know]

---

*Hook-generated template. Edit as needed.*
```

#### DECISIONS.md (Required)

**Purpose:** Record key architectural and implementation decisions

**Template:**
```markdown
# DECISIONS - Run {run_id}

**Date:** {timestamp}
**Agent:** {agent_type}

---

## Decisions Made

### Decision 1: [Title]
**Context:** [What led to this decision]
**Options Considered:** [Alternatives]
**Decision:** [What was chosen]
**Rationale:** [Why this choice]
**Consequences:** [Impact of decision]

---

## Open Questions

- [Question 1]
- [Question 2]
```

#### LEARNINGS.md (Required)

**Purpose:** Extract patterns and insights for future reference

**Template:**
```markdown
# LEARNINGS - Run {run_id}

**Date:** {timestamp}
**Agent:** {agent_type}

---

## What Worked Well

-

## What Was Harder Than Expected

-

## What Would I Do Differently

-

## Patterns Detected

-

## Technical Insights

-
```

#### ASSUMPTIONS.md (Optional)

**Purpose:** Document assumptions made and their verification status

**Template:**
```markdown
# ASSUMPTIONS - Run {run_id}

**Date:** {timestamp}

---

## Assumptions Made

| Assumption | Verification Method | Status | Verified By |
|------------|---------------------|--------|-------------|
| [Assumption] | [How verified] | verified/pending/failed | [Agent] |
```

#### metadata.yaml (Required)

**Purpose:** Machine-readable run metadata for tracking and analysis

**Schema:**
```yaml
run:
  id: string
  agent_type: string
  parent_task_id: string|null
  parent_run_id: string|null
  timestamp_start: ISO8601
  timestamp_end: ISO8601|null
  status: pending|in_progress|completed|failed|partial|blocked

task:
  task_id: string
  task_type: string
  priority: CRITICAL|HIGH|MEDIUM|LOW
  goal_id: string|null
  plan_id: string|null

context:
  git_branch: string
  git_commit: string
  working_directory: string

metrics:
  files_modified: []
  files_created: []
  duration_seconds: integer|null
  loop_count: integer

subagent:
  is_subagent: true
  parent_agent_id: string
  handoff_type: spawn|delegate
```

---

## 3. Hook Specifications

### 3.1 SubagentStart Hook

**Hook Name:** `subagent-start-documentation.sh`

**Event:** `SubagentStart`

**Purpose:** Initialize subagent run folder and inject parent context

**Trigger Conditions:**
- Task tool invoked with `subagent_type` parameter
- Parent agent is spawning a subagent

**Actions:**
1. Create subagent run directory
2. Copy parent context (THOUGHTS.md, DECISIONS.md) to subagent folder
3. Initialize required documentation files with templates
4. Write metadata.yaml with parent references
5. Log subagent spawn event to events.yaml

**Input (from stdin):**
```json
{
  "tool_name": "Task",
  "tool_input": {
    "subagent_type": "code-reviewer",
    "model": "sonnet",
    "prompt": "..."
  },
  "parent_context": {
    "run_id": "parent-run-001",
    "thoughts_path": "/path/to/parent/THOUGHTS.md",
    "decisions_path": "/path/to/parent/DECISIONS.md"
  }
}
```

**Output (stdout):**
```json
{
  "continue": true,
  "systemMessage": "Subagent run initialized at: runs/{type}/active/{run_id}/"
}
```

**File Operations:**
```bash
# Create run directory
mkdir -p "runs/${AGENT_TYPE}/active/${RUN_ID}"

# Initialize documentation files
touch "runs/${AGENT_TYPE}/active/${RUN_ID}/THOUGHTS.md"
touch "runs/${AGENT_TYPE}/active/${RUN_ID}/RESULTS.md"
touch "runs/${AGENT_TYPE}/active/${RUN_ID}/DECISIONS.md"
touch "runs/${AGENT_TYPE}/active/${RUN_ID}/LEARNINGS.md"
touch "runs/${AGENT_TYPE}/active/${RUN_ID}/ASSUMPTIONS.md"

# Copy parent context
cp "${PARENT_THOUGHTS}" "runs/${AGENT_TYPE}/active/${RUN_ID}/.parent_thoughts.md"
cp "${PARENT_DECISIONS}" "runs/${AGENT_TYPE}/active/${RUN_ID}/.parent_decisions.md"

# Write metadata
cat > "runs/${AGENT_TYPE}/active/${RUN_ID}/metadata.yaml" << EOF
run:
  id: ${RUN_ID}
  agent_type: ${AGENT_TYPE}
  parent_task_id: ${PARENT_TASK_ID}
  parent_run_id: ${PARENT_RUN_ID}
  timestamp_start: $(date -u +%Y-%m-%dT%H:%M:%SZ)
  status: in_progress
subagent:
  is_subagent: true
  parent_agent_id: ${PARENT_AGENT_ID}
  handoff_type: spawn
EOF

# Log event
echo "- timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
  type: agent_start
  agent_type: ${AGENT_TYPE}
  agent_id: ${RUN_ID}
  parent_task: ${PARENT_TASK_ID}
  source: hook" >> "agents/communications/events.yaml"
```

### 3.2 SubagentStop Hook

**Hook Name:** `subagent-stop-validation.sh`

**Event:** `SubagentStop`

**Purpose:** Validate subagent documentation and trigger parent handoff

**Trigger Conditions:**
- Subagent execution completes
- Task status changes to completed/failed/partial/blocked

**Actions:**
1. Validate required documentation files exist
2. Validate files have non-empty content
3. Update metadata.yaml with completion timestamp
4. Move run folder from active/ to completed/
5. Write completion event to events.yaml
6. Trigger parent notification

**Validation Rules:**

| File | Validation | Failure Action |
|------|------------|----------------|
| THOUGHTS.md | Must exist, >100 bytes | Block completion, request documentation |
| RESULTS.md | Must exist, status field filled | Block completion, request results |
| DECISIONS.md | Must exist | Warn, allow completion |
| LEARNINGS.md | Must exist | Warn, allow completion |
| metadata.yaml | Must exist, valid YAML | Block completion |

**Input (from stdin):**
```json
{
  "tool_name": "Task",
  "tool_output": {
    "status": "completed",
    "result": "..."
  },
  "subagent_run_id": "scout-001",
  "subagent_type": "scout"
}
```

**Output (stdout):**
```json
{
  "continue": true,
  "systemMessage": "Subagent documentation validated. Results available at: runs/{type}/completed/{run_id}/"
}
```

**Validation Script:**
```bash
#!/bin/bash
# SubagentStop validation logic

RUN_DIR="runs/${AGENT_TYPE}/active/${RUN_ID}"
ERRORS=()

# Validate THOUGHTS.md
if [[ ! -f "${RUN_DIR}/THOUGHTS.md" ]]; then
  ERRORS+=("THOUGHTS.md missing")
elif [[ $(stat -f%z "${RUN_DIR}/THOUGHTS.md" 2>/dev/null || stat -c%s "${RUN_DIR}/THOUGHTS.md" 2>/dev/null) -lt 100 ]]; then
  ERRORS+=("THOUGHTS.md too short (< 100 bytes)")
fi

# Validate RESULTS.md
if [[ ! -f "${RUN_DIR}/RESULTS.md" ]]; then
  ERRORS+=("RESULTS.md missing")
fi

# Validate DECISIONS.md
if [[ ! -f "${RUN_DIR}/DECISIONS.md" ]]; then
  ERRORS+=("DECISIONS.md missing (warning)")
fi

# Validate LEARNINGS.md
if [[ ! -f "${RUN_DIR}/LEARNINGS.md" ]]; then
  ERRORS+=("LEARNINGS.md missing (warning)")
fi

# Block if critical files missing
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  echo "{\"continue\": false, \"error\": \"Documentation incomplete: ${ERRORS[*]}\"}"
  exit 1
fi

# Move to completed
mkdir -p "runs/${AGENT_TYPE}/completed"
mv "${RUN_DIR}" "runs/${AGENT_TYPE}/completed/${RUN_ID}"

# Update metadata
cat > "runs/${AGENT_TYPE}/completed/${RUN_ID}/metadata.yaml" << EOF
run:
  status: completed
  timestamp_end: $(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF

# Log completion
echo "- timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
  type: agent_stop
  agent_type: ${AGENT_TYPE}
  agent_id: ${RUN_ID}
  parent_task: ${PARENT_TASK_ID}
  source: hook
  data:
    status: completed
    results_path: runs/${AGENT_TYPE}/completed/${RUN_ID}/RESULTS.md" >> "agents/communications/events.yaml"
```

### 3.3 Parent Context Integration Hook

**Hook Name:** `parent-context-integrator.sh`

**Event:** `PostToolUse` (after Task completion)

**Purpose:** Integrate subagent results into parent agent's THOUGHTS.md

**Trigger Conditions:**
- Task tool completes (subagent finishes)
- Parent agent needs to incorporate subagent findings

**Actions:**
1. Read subagent RESULTS.md
2. Read subagent LEARNINGS.md
3. Append summary to parent THOUGHTS.md
4. Update parent task status

**Integration Format:**
```markdown
## Subagent Results: {subagent_type} ({run_id})

**Status:** {completed|failed|partial}
**Completed:** {timestamp}

### Summary
{Summary from subagent RESULTS.md}

### Key Findings
{Extracted from subagent LEARNINGS.md}

### Deliverables
- File: {path} - {description}

---
```

---

## 4. Parent-Subagent Documentation Flow

### 4.1 Context Inheritance

**What Parent Passes to Subagent:**

| Data | Method | Purpose |
|------|--------|---------|
| Parent THOUGHTS.md | File copy | Context on parent's reasoning |
| Parent DECISIONS.md | File copy | Decisions that constrain subagent |
| Task specification | Prompt parameter | What subagent should do |
| Success criteria | Prompt parameter | How to know task is complete |
| Parent run ID | metadata.yaml | For linking results back |

**What Subagent Produces Independently:**

| File | Content | Purpose |
|------|---------|---------|
| THOUGHTS.md | Subagent's own reasoning | Track subagent's thought process |
| RESULTS.md | Task outcomes | Deliver results to parent |
| DECISIONS.md | Subagent decisions | Record local choices |
| LEARNINGS.md | Patterns found | Extract insights |

### 4.2 Merging vs. Separation

**Files That Stay Separate:**
- THOUGHTS.md (each agent has their own)
- DECISIONS.md (decisions are agent-scoped)
- metadata.yaml (run-specific)

**Files That Get Merged/Referenced:**
- LEARNINGS.md -> Extracted to parent's learning-index.yaml
- RESULTS.md -> Referenced/summarized in parent THOUGHTS.md
- Discoveries -> Added to parent's context

**Handoff Protocol:**
```yaml
Subagent Completion:
  1. Write final RESULTS.md
  2. Write LEARNINGS.md
  3. Update metadata.yaml status
  4. Trigger SubagentStop hook
  5. Hook validates documentation
  6. Hook moves run to completed/
  7. Hook writes events.yaml entry
  8. Parent reads events.yaml or polls
  9. Parent integrates results
  10. Parent continues execution
```

---

## 5. Validation Rules

### 5.1 Documentation Completeness Check

**Critical Files (Block Completion):**
```python
CRITICAL_FILES = {
    'THOUGHTS.md': {
        'min_size': 100,  # bytes
        'required_sections': ['## State Assessment', '## Analysis'],
        'check_content': True
    },
    'RESULTS.md': {
        'min_size': 50,
        'required_sections': ['## Summary', '## Status'],
        'check_status_field': True
    },
    'metadata.yaml': {
        'valid_yaml': True,
        'required_fields': ['run.id', 'run.agent_type', 'run.status']
    }
}
```

**Warning Files (Allow Completion with Warning):**
```python
WARNING_FILES = {
    'DECISIONS.md': {
        'min_size': 0,  # Optional but recommended
    },
    'LEARNINGS.md': {
        'min_size': 0,  # Optional but recommended
    },
    'ASSUMPTIONS.md': {
        'min_size': 0,  # Truly optional
    }
}
```

### 5.2 Content Validation

**THOUGHTS.md Validation:**
- Must have "## State Assessment" section
- Must have "## Analysis" section
- Must have "## Skill Usage for This Task" section (per CLAUDE.md Phase 1.5)
- Must not be template-only (checked by minimum size)

**RESULTS.md Validation:**
- Must have status field filled (not "in_progress" if completing)
- Must have summary section with actual content
- Must list deliverables if files were created

**LEARNINGS.md Validation:**
- Should have at least one of the standard sections
- Can be empty for simple tasks (warning only)

### 5.3 Validation Failure Handling

**On Critical Failure:**
```json
{
  "decision": "block",
  "reason": "Documentation incomplete: THOUGHTS.md missing required sections",
  "missing_files": ["THOUGHTS.md"],
  "action_required": "Complete documentation before finishing"
}
```

**On Warning:**
```json
{
  "decision": "allow",
  "warnings": ["LEARNINGS.md is empty", "DECISIONS.md not found"],
  "recommendation": "Consider adding learnings for future reference"
}
```

---

## 6. Events and Communication

### 6.1 Subagent Events Schema

**agent_start Event:**
```yaml
- timestamp: "2026-02-06T12:00:00Z"
  type: agent_start
  agent_type: "scout"
  agent_id: "scout-001"
  parent_task: "TASK-ARCH-002"
  parent_run: "run-20260206-000001"
  source: hook
  data:
    run_path: "runs/scout/active/scout-001"
    documentation_required: true
```

**agent_stop Event:**
```yaml
- timestamp: "2026-02-06T12:30:00Z"
  type: agent_stop
  agent_type: "scout"
  agent_id: "scout-001"
  parent_task: "TASK-ARCH-002"
  source: hook
  data:
    status: "completed"
    run_path: "runs/scout/completed/scout-001"
    results_path: "runs/scout/completed/scout-001/RESULTS.md"
    learnings_path: "runs/scout/completed/scout-001/LEARNINGS.md"
    documentation_validated: true
    duration_seconds: 1800
```

**agent_progress Event (optional):**
```yaml
- timestamp: "2026-02-06T12:15:00Z"
  type: agent_progress
  agent_type: "scout"
  agent_id: "scout-001"
  parent_task: "TASK-ARCH-002"
  source: agent
  data:
    progress_pct: 50
    status: "Analyzing codebase structure"
```

### 6.2 Parent Notification

**Methods for Parent to Detect Subagent Completion:**

1. **Event Polling** (Recommended):
   - Parent polls events.yaml for agent_stop events
   - Filter by parent_task ID
   - Read results from referenced paths

2. **File Watching**:
   - Parent watches subagent run directory
   - Detects when status changes in metadata.yaml

3. **Direct Integration** (for synchronous subagents):
   - Parent uses TaskOutput tool to wait
   - Subagent completion triggers automatic continuation

---

## 7. Implementation Recommendations

### 7.1 Hook Priority

**Phase 1 (Critical):**
- SubagentStart hook - Initialize run folders
- SubagentStop hook - Validate documentation

**Phase 2 (Important):**
- Parent context integration hook
- Documentation template injection

**Phase 3 (Enhancement):**
- Progress tracking hooks
- Automatic learning extraction

### 7.2 Directory Structure

```
.autonomous/
├── agents/
│   └── communications/
│       └── events.yaml          # Agent lifecycle events
├── memory/
│   └── hooks/
│       ├── subagent-start.sh    # SubagentStart hook
│       ├── subagent-stop.sh     # SubagentStop hook
│       └── parent-integrate.sh  # Parent integration hook
└── runs/
    └── {agent_type}/
        ├── active/              # Currently running
        └── completed/           # Finished runs
```

### 7.3 Configuration

**settings.json additions:**
```json
{
  "hooks": [
    {
      "event": "SubagentStart",
      "command": ".autonomous/memory/hooks/subagent-start.sh",
      "enabled": true
    },
    {
      "event": "SubagentStop",
      "command": ".autonomous/memory/hooks/subagent-stop.sh",
      "enabled": true
    }
  ],
  "subagent_documentation": {
    "required_files": ["THOUGHTS.md", "RESULTS.md", "DECISIONS.md", "LEARNINGS.md"],
    "optional_files": ["ASSUMPTIONS.md"],
    "min_thoughts_size": 100,
    "validate_on_complete": true,
    "auto_move_to_completed": true
  }
}
```

---

## 8. Key Questions Answered

### Q1: Does SubagentStart hook inject documentation requirements?

**Answer:** Yes. The SubagentStart hook:
- Creates all required documentation files
- Populates them with templates
- Copies parent context for reference
- Sets up metadata.yaml with documentation tracking

### Q2: Does SubagentStop hook validate RESULTS.md exists?

**Answer:** Yes. The SubagentStop hook:
- Validates all critical files exist (THOUGHTS.md, RESULTS.md, metadata.yaml)
- Checks file sizes to ensure non-empty content
- Validates required sections are present
- Blocks completion if documentation is incomplete

### Q3: How does parent agent's THOUGHTS.md reference subagent work?

**Answer:** Through the parent integration hook:
- Subagent writes RESULTS.md with structured output
- Parent integration hook reads subagent RESULTS.md
- Appends summary to parent's THOUGHTS.md
- Links to full subagent run folder for details

### Q4: What prevents subagent from completing without documentation?

**Answer:** Multiple safeguards:
1. **SubagentStop hook validation** - Blocks completion if docs missing
2. **Template injection** - Files created at start, harder to forget
3. **Size checks** - Ensures files have actual content
4. **Required sections** - Validates structure, not just existence
5. **Events logging** - Creates audit trail of documentation status

---

## 9. Anti-Patterns to Avoid

### Anti-Pattern 1: Empty Documentation Files

**Problem:** Subagent creates files but leaves them empty or template-only.

**Solution:** Minimum size checks and section validation in SubagentStop hook.

### Anti-Pattern 2: Parent Polling Too Frequently

**Problem:** Parent constantly polls events.yaml, causing performance issues.

**Solution:** Use file watching or notification-based triggers instead of polling.

### Anti-Pattern 3: Documentation After Completion

**Problem:** Subagent marks task complete, then tries to write documentation.

**Solution:** Hook validates docs BEFORE allowing status change to completed.

### Anti-Pattern 4: Orphaned Run Folders

**Problem:** Subagent runs left in active/ directory after completion.

**Solution:** SubagentStop hook automatically moves runs to completed/.

### Anti-Pattern 5: Context Leakage

**Problem:** Subagent documentation contains sensitive parent context.

**Solution:** Copy only necessary context, sanitize before writing.

---

## 10. Summary

**Critical Hooks Needed:**

| Hook | Event | Priority | Purpose |
|------|-------|----------|---------|
| subagent-start.sh | SubagentStart | Critical | Initialize run folder, inject templates |
| subagent-stop.sh | SubagentStop | Critical | Validate docs, move to completed |
| parent-integrate.sh | PostToolUse | High | Integrate results into parent |

**Required Files:**
- THOUGHTS.md - Agent reasoning
- RESULTS.md - Task outcomes
- DECISIONS.md - Key decisions
- LEARNINGS.md - Patterns and insights
- metadata.yaml - Run metadata

**Validation Rules:**
- Critical files must exist and have content
- THOUGHTS.md must have required sections
- RESULTS.md must have status field
- Files must meet minimum size thresholds

**Handoff Flow:**
1. Parent spawns subagent with context
2. Subagent creates documentation during execution
3. SubagentStop validates documentation
4. Results integrated into parent context
5. Parent continues with subagent findings

---

**Document Version:** 1.0
**Last Updated:** 2026-02-06
**Related Documents:**
- COORDINATION_HOOKS.md
- EXTERNAL_HOOK_PATTERNS.md
- /runs/.docs/run-lifecycle.md
