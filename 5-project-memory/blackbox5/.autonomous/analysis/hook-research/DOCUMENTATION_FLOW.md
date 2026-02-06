# BB5 Documentation Flow Architecture

**Version:** 1.0.0
**Date:** 2026-02-06
**Author:** BB5 Documentation Systems Architect

---

## Executive Summary

This document analyzes how documentation flows through the BlackBox5 (BB5) system, identifying the lifecycle of documentation files, subagent documentation patterns, and the hooks required to capture documentation at critical moments.

**Key Finding:** BB5 uses a **3-layer documentation architecture** that requires coordination between SessionStart, SubagentStart/Stop, Stop, and PreCompact hooks to ensure no documentation is lost.

---

## 1. Current Documentation Flow

### 1.1 Where Agents Document Their Work

BB5 agents document work in **run folders** created at session start:

```
runs/
├── active/
│   └── run-20260206-001/
│       ├── THOUGHTS.md      # Reasoning and analysis
│       ├── RESULTS.md       # Outcomes and deliverables
│       ├── DECISIONS.md     # Choices made with rationale
│       ├── LEARNINGS.md     # Patterns and insights
│       ├── ASSUMPTIONS.md   # Verified assumptions
│       └── metadata.yaml    # Run metadata
│
└── completed/
    └── run-20260206-001/    # Moved here after completion
```

**Location Determination:**
- **Autonomous mode:** `RALF_RUN_DIR` environment variable set by SessionStart hook
- **Manual mode:** Created by agent in current working directory
- **Subagents:** Separate run folder under parent run or agent-specific location

### 1.2 Documentation File Lifecycle

#### THOUGHTS.md

**Purpose:** Capture agent reasoning as it happens

**Lifecycle:**
```
SessionStart
    ↓
Create THOUGHTS.md from template
    ↓
Agent populates continuously during work
    ↓
PreCompact (if context compaction occurs)
    ↓
Stop hook validates THOUGHTS.md exists
    ↓
RETAIN extracts insights to 4-network memory
```

**When Populated:**
- **Continuously** - Agent adds sections as work progresses
- **Key sections:** Pre-Execution Research, Reasoning Log, Analysis
- **Critical requirement:** Must document reasoning for better AI cognition (per BB5 Key Thesis)

**Template Structure:**
```markdown
# THOUGHTS

## Pre-Execution Research
- Duplicate check results
- Context gathered
- Risk assessment

## Reasoning Log
### Decision 1: [Topic]
**Context:** [What we knew]
**Options Considered:** [...]
**Decision:** [What we chose]
**Rationale:** [Why]
**Confidence:** [High/Medium/Low]

## Analysis
[Deep analysis of findings]

## Next Steps
[Planned actions]
```

#### RESULTS.md

**Purpose:** Document concrete outcomes

**Lifecycle:**
```
Execution Phase
    ↓
Agent creates RESULTS.md with outcomes
    ↓
SubagentStop validates RESULTS.md exists
    ↓
Stop hook extracts results for notifications
    ↓
Task completion workflow updates STATE.yaml
```

**When Populated:**
- **At milestones** - After significant progress
- **At completion** - Final results documented
- **Required for:** Subagent validation, task completion

#### DECISIONS.md

**Purpose:** Record decisions with full rationale

**Lifecycle:**
```
Decision made during work
    ↓
Document in DECISIONS.md immediately
    ↓
Reference in THOUGHTS.md Reasoning Log
    ↓
Stop hook validates decisions documented
    ↓
Extracted to decision registry
```

**Format:**
```markdown
# Decisions

## D-XXX: [Decision Title]
**Status:** ACCEPTED/PENDING/REJECTED
**Confidence:** [High/Medium/Low]%
**Impact:** [High/Medium/Low]

### Context
[What we knew at the time]

### Options Considered
- Option A: [Description] → Pros: ... Cons: ...
- Option B: [Description] → Pros: ... Cons: ...

### Decision
[What we chose]

### Rationale
[Why we chose it]

### Validation Plan
[How we'll verify this was correct]
```

#### LEARNINGS.md

**Purpose:** Extract reusable insights

**Lifecycle:**
```
Pattern discovered during work
    ↓
Document in LEARNINGS.md
    ↓
Stop hook triggers RETAIN
    ↓
Classified into 4-network memory:
  - World (facts)
  - Experience (what worked)
  - Opinion (preferences)
  - Observation (patterns)
```

### 1.3 Documentation Timing Matrix

| File | When Created | When Updated | When Finalized | Hook Trigger |
|------|--------------|--------------|----------------|--------------|
| THOUGHTS.md | SessionStart | Continuously | PreCompact/Stop | Stop validates |
| RESULTS.md | SessionStart | At milestones | SubagentStop/Stop | SubagentStop validates |
| DECISIONS.md | SessionStart | Per decision | Stop | Stop validates |
| LEARNINGS.md | SessionStart | As discovered | Stop | RETAIN trigger |
| ASSUMPTIONS.md | SessionStart | As verified | Stop | - |

---

## 2. Subagent Documentation

### 2.1 What Subagents Need to Document

Subagents follow the **same documentation requirements** as parent agents:

```
Parent Agent Run
├── THOUGHTS.md (parent reasoning)
├── DECISIONS.md (parent decisions)
├── RESULTS.md (parent outcomes)
└── subagents/
    └── scout-001/
        ├── THOUGHTS.md (subagent reasoning)
        ├── DECISIONS.md (subagent decisions)
        └── RESULTS.md (subagent findings)
```

**Subagent-Specific Requirements:**
1. **THOUGHTS.md** - Document subtask analysis and approach
2. **RESULTS.md** - Deliver findings in expected format
3. **DECISIONS.md** - Record subtask-specific decisions
4. **metadata.yaml** - Link to parent task, track lineage

### 2.2 How Parent Agent Gets Subagent Documentation

**Mechanism 1: Shared Filesystem**
```python
# Parent reads subagent results
subagent_results = read_file(f"{run_dir}/subagents/{subagent_id}/RESULTS.md")
```

**Mechanism 2: Events.yaml Integration**
```yaml
# Subagent reports completion via events
- timestamp: "2026-02-06T10:00:00Z"
  type: agent_stop
  agent_type: "scout"
  agent_id: "scout-001"
  parent_task: "TASK-ARCH-002"
  data:
    results_file: "subagents/scout-001/RESULTS.md"
    findings_count: 12
    confidence: 0.85
```

**Mechanism 3: SubagentStop Hook**
- Fires when subagent completes
- Validates subagent produced RESULTS.md
- Parses results and updates parent context
- Can BLOCK if results are invalid (exit 2)

### 2.3 Subagent Handoff Documentation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  SUBAGENT DOCUMENTATION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PARENT AGENT                                                    │
│  ┌─────────────┐                                                 │
│  │ Spawns      │──────► SubagentStart Hook                       │
│  │ Subagent    │        - Inject context                          │
│  └─────────────┘        - Pass parent THOUGHTS.md                 │
│         │               - Set documentation requirements          │
│         │                                                        │
│         │               SUBAGENT                                  │
│         │               ┌─────────────┐                          │
│         │               │ Creates     │                          │
│         │               │ run folder  │                          │
│         │               │ with docs   │                          │
│         │               └─────────────┘                          │
│         │                      │                                 │
│         │                      ▼                                 │
│         │               ┌─────────────┐                          │
│         │               │ Populates   │                          │
│         │               │ THOUGHTS.md │                          │
│         │               │ RESULTS.md  │                          │
│         │               │ DECISIONS.md│                          │
│         │               └─────────────┘                          │
│         │                      │                                 │
│         │                      ▼                                 │
│         │               SubagentStop Hook                        │
│         │               - Validate RESULTS.md exists             │
│         │               - Check output format                    │
│         │               - Extract findings                       │
│         │                      │                                 │
│         │                      ▼                                 │
│         │               ┌─────────────┐                          │
│         └───────────────│ Returns     │                          │
│                         │ results to  │                          │
│                         │ parent      │                          │
│                         └─────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Subagent Context Injection

**SubagentStart Hook Responsibilities:**
1. Pass parent agent's THOUGHTS.md (relevant sections)
2. Pass parent agent's DECISIONS.md (context for subtask)
3. Set `PARENT_RUN_DIR` environment variable
4. Set `SUBAGENT_TASK` with specific requirements
5. Inject documentation template for subagent type

**Example Context Injection:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "parent_context": {
      "parent_run_dir": "/path/to/parent/run",
      "task_objective": "Analyze codebase for patterns",
      "documentation_required": ["THOUGHTS.md", "RESULTS.md"],
      "output_format": "scout-report"
    },
    "injected_context": "## Parent Task Context\n[Summary]\n\n## Documentation Requirements\n- Create THOUGHTS.md\n- Create RESULTS.md with findings"
  }
}
```

---

## 3. Documentation Triggers

### 3.1 Continuous vs Milestone Capture

| Approach | When | Pros | Cons | Use Case |
|----------|------|------|------|----------|
| **Continuous** | After each significant thought/decision | Nothing lost, fresh context | Overhead, interruption | THOUGHTS.md, DECISIONS.md |
| **Milestone** | At defined checkpoints | Batched, less overhead | Risk of loss if crash | RESULTS.md updates |
| **PreCompact** | Before context compaction | Preserves before loss | Reactive | Emergency backup |
| **Stop** | Session end | Final validation | Too late to fix | Validation, extraction |

**BB5 Recommendation:**
- **THOUGHTS.md** - Continuous (append as you think)
- **DECISIONS.md** - Per decision (document immediately)
- **RESULTS.md** - Milestone + completion
- **LEARNINGS.md** - As discovered

### 3.2 Event Triggers for Documentation

```
┌─────────────────────────────────────────────────────────────────┐
│              DOCUMENTATION EVENT TRIGGERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SessionStart                                                    │
│  ├── Create run folder                                           │
│  ├── Copy document templates                                     │
│  └── Inject context into THOUGHTS.md                             │
│                                                                  │
│  During Work (Agent Responsibility)                              │
│  ├── Decision made → Append to DECISIONS.md                      │
│  ├── Insight discovered → Append to LEARNINGS.md                 │
│  ├── Analysis complete → Update THOUGHTS.md                      │
│  └── Milestone reached → Update RESULTS.md                       │
│                                                                  │
│  PreCompact (Context Window Critical)                            │
│  ├── Snapshot THOUGHTS.md → pre-compact-backup.md                │
│  ├── Snapshot DECISIONS.md → pre-compact-decisions.md            │
│  ├── Record current task status                                  │
│  └── Document open questions/blockers                            │
│                                                                  │
│  SubagentStop (Subagent Completion)                              │
│  ├── Validate subagent RESULTS.md exists                         │
│  ├── Validate output format                                      │
│  ├── Extract findings to parent context                          │
│  └── Update parent THOUGHTS.md with subagent summary             │
│                                                                  │
│  Stop (Session End)                                              │
│  ├── Validate THOUGHTS.md exists                                 │
│  ├── Validate RESULTS.md exists                                  │
│  ├── Validate DECISIONS.md has entries                           │
│  ├── Trigger RETAIN on LEARNINGS.md                              │
│  ├── Send RALF Monitor notification                              │
│  └── Archive run folder                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Ensuring Nothing Is Lost

**Multi-Layer Safety Net:**

1. **Layer 1: PreCompact Hook (Emergency)**
   - Fires when context reaches 70-80%
   - Creates backup of current documentation state
   - Stores in `pre-compact-backup.md`

2. **Layer 2: Continuous Write (Habit)**
   - Agent writes to files continuously
   - Not just in memory - persisted to disk
   - Use append mode for incremental updates

3. **Layer 3: SubagentStop Validation (Gate)**
   - Validates subagent produced required docs
   - Can block if documentation missing
   - Forces documentation discipline

4. **Layer 4: Stop Hook Validation (Final Check)**
   - Validates all required docs exist
   - Extracts learnings to memory
   - Archives run for future reference

5. **Layer 5: Git Auto-Commit (Persistence)**
   - Commits documentation to git
   - Creates permanent record
   - Enables recovery if needed

---

## 4. Hook Documentation Capture Requirements

### 4.1 SessionStart Hook

**Documentation Actions:**
```yaml
session_start:
  actions:
    - create_run_folder:
        path: "${RALF_RUN_DIR}"
        structure:
          - THOUGHTS.md (from template)
          - RESULTS.md (from template)
          - DECISIONS.md (from template)
          - LEARNINGS.md (from template)
          - ASSUMPTIONS.md (from template)
          - metadata.yaml
    - inject_context:
        target: THOUGHTS.md
        content: "## Session Context\n[Agent type, task, etc.]"
    - set_env_vars:
        RALF_RUN_DIR: "${run_dir}"
        BB5_DOCUMENTATION_REQUIRED: "true"
```

### 4.2 PreCompact Hook

**Documentation Actions:**
```yaml
pre_compact:
  trigger: context_usage > 70%
  actions:
    - snapshot_documentation:
        sources:
          - THOUGHTS.md
          - DECISIONS.md
          - current_task_status
        destination: "${RALF_RUN_DIR}/pre-compact-backup.md"
    - record_state:
        open_questions: "[Extract from THOUGHTS.md]"
        pending_decisions: "[Extract from DECISIONS.md]"
        current_focus: "[Last section worked on]"
    - inject_summary:
        target: context
        content: "## Pre-Compact State\n[Summary of work so far]"
```

**Why PreCompact is Critical:**
- Context compaction **erases** detailed history
- THOUGHTS.md may contain reasoning not yet extracted
- PreCompact preserves this reasoning before loss
- Enables session resumption after compaction

### 4.3 SubagentStart Hook

**Documentation Actions:**
```yaml
subagent_start:
  actions:
    - inherit_context:
        from: parent_run_dir
        files:
          - THOUGHTS.md (relevant sections)
          - DECISIONS.md (context decisions)
        to: subagent_context
    - set_requirements:
        documentation_required:
          - THOUGHTS.md
          - RESULTS.md
          - DECISIONS.md
        output_format: "${subagent_type}-report"
        parent_task: "${parent_task_id}"
    - create_subagent_folder:
        path: "${parent_run_dir}/subagents/${subagent_id}"
        templates: [THOUGHTS.md, RESULTS.md, DECISIONS.md]
```

### 4.4 SubagentStop Hook

**Documentation Actions:**
```yaml
subagent_stop:
  can_block: true
  validations:
    - file_exists: "${subagent_run_dir}/RESULTS.md"
      severity: error
      message: "Subagent must produce RESULTS.md"
    - file_exists: "${subagent_run_dir}/THOUGHTS.md"
      severity: warning
      message: "THOUGHTS.md recommended for subagent"
    - validate_format:
        file: RESULTS.md
        expected_structure: "${subagent_type}-template"
  actions:
    - extract_results:
        from: "${subagent_run_dir}/RESULTS.md"
        to: parent_context
    - update_parent_thoughts:
        append: "## Subagent ${subagent_id} Results\n[Summary]"
    - log_completion:
        file: events.yaml
        event:
          type: subagent_complete
          subagent_id: "${subagent_id}"
          results_file: "${subagent_run_dir}/RESULTS.md"
```

### 4.5 Stop Hook

**Documentation Actions:**
```yaml
stop:
  validations:
    - file_exists: THOUGHTS.md
      check_content: "## Reasoning Log"  # At least one decision
    - file_exists: RESULTS.md
      check_content: "## Executive Summary"
    - file_exists: DECISIONS.md
      min_entries: 1
  actions:
    - trigger_retain:
        sources:
          - LEARNINGS.md
          - DECISIONS.md
          - THOUGHTS.md (insights section)
        target: 4-network-memory
    - send_notification:
        channel: telegram
        message: "Task ${task_id} complete. Docs: THOUGHTS.md, RESULTS.md, DECISIONS.md"
    - archive_run:
        from: "runs/active/"
        to: "runs/completed/"
    - update_task_status:
        file: queue.yaml
        task_id: "${task_id}"
        status: completed
```

---

## 5. Documentation Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     BB5 DOCUMENTATION LIFECYCLE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   SESSION START                                                              │
│   ┌─────────────┐                                                            │
│   │ SessionStart│                                                            │
│   │ Hook Fires  │                                                            │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌────────────┐│
│   │ THOUGHTS.md │     │ RESULTS.md  │     │ DECISIONS.md│     │LEARNINGS.md││
│   │  [created]  │     │  [created]  │     │  [created]  │     │ [created]  ││
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬─────┘│
│          │                   │                   │                   │      │
│          └───────────────────┴───────────────────┴───────────────────┘      │
│                              │                                              │
│                              ▼                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                        DURING WORK                                   │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│   │  │ Agent adds  │  │ Agent adds  │  │ Agent adds  │  │ Agent adds  │ │  │
│   │  │ reasoning   │  │ milestones  │  │ decisions   │  │ insights    │ │  │
│   │  │ continuously│  │ at progress │  │ per choice  │  │ as found    │ │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              │                                              │
│          ┌───────────────────┼───────────────────┐                         │
│          │                   │                   │                         │
│          ▼                   ▼                   ▼                         │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │ PreCompact  │     │SubagentStop │     │    Stop     │                  │
│   │   Hook      │     │   Hook      │     │   Hook      │                  │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘                  │
│          │                   │                   │                         │
│          ▼                   ▼                   ▼                         │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │ Backup docs │     │ Validate    │     │ Validate    │                  │
│   │ to backup   │     │ subagent    │     │ all docs    │                  │
│   │ files       │     │ results     │     │ exist       │                  │
│   └─────────────┘     └─────────────┘     └──────┬──────┘                  │
│                                                  │                         │
│                                                  ▼                         │
│                                         ┌─────────────┐                    │
│                                         │   RETAIN    │                    │
│                                         │  Triggered  │                    │
│                                         └──────┬──────┘                    │
│                                                │                           │
│                                                ▼                           │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    4-NETWORK MEMORY SYSTEM                           │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│   │  │  World   │  │ Experience│  │ Opinion  │  │Observation│            │  │
│   │  │ (facts)  │  │(patterns)│  │(preferences)│  │ (data)   │            │  │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                │                           │
│                                                ▼                           │
│                                         ┌─────────────┐                    │
│                                         │   Archive   │                    │
│                                         │   to git    │                    │
│                                         └─────────────┘                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Minimum Viable Documentation Hooks

### 6.1 Essential Hooks (MVP)

For a minimal viable documentation system, BB5 needs **5 hooks**:

| Priority | Hook | Documentation Purpose |
|----------|------|----------------------|
| **P0** | SessionStart | Create run folder with document templates |
| **P0** | Stop | Validate docs exist, trigger RETAIN, archive |
| **P1** | PreCompact | Preserve documentation before context loss |
| **P1** | SubagentStart | Pass context to subagent, set doc requirements |
| **P1** | SubagentStop | Validate subagent produced RESULTS.md |

### 6.2 Hook Implementation Priority

**Phase 1: Foundation (Week 1)**
1. SessionStart - Create run folder with templates
2. Stop - Validate THOUGHTS.md, RESULTS.md exist

**Phase 2: Safety (Week 2)**
3. PreCompact - Backup documentation before compaction
4. SubagentStop - Validate subagent results

**Phase 3: Coordination (Week 3)**
5. SubagentStart - Context injection for subagents

### 6.3 Minimum Documentation Requirements

**For Every Run:**
- [ ] THOUGHTS.md exists with Reasoning Log section
- [ ] RESULTS.md exists with Executive Summary
- [ ] DECISIONS.md exists (can be empty for simple tasks)

**For Subagent Runs:**
- [ ] RESULTS.md exists (REQUIRED - SubagentStop blocks if missing)
- [ ] THOUGHTS.md recommended

**For Task Completion:**
- [ ] All docs validated by Stop hook
- [ ] LEARNINGS.md processed by RETAIN
- [ ] Run archived to completed/

---

## 7. Recommendations

### 7.1 Immediate Actions

1. **Implement SessionStart v1.0**
   - Create run folder with all 5 document templates
   - Set RALF_RUN_DIR environment variable
   - Inject initial context into THOUGHTS.md

2. **Implement Stop v1.0**
   - Validate THOUGHTS.md and RESULTS.md exist
   - Send RALF Monitor notification
   - Archive run folder

3. **Implement PreCompact v1.0**
   - Snapshot current documentation state
   - Store in pre-compact-backup.md
   - Inject summary into compacted context

### 7.2 Short-term Improvements

1. **Subagent Documentation Flow**
   - Implement SubagentStart context injection
   - Implement SubagentStop validation
   - Create subagent documentation templates

2. **RETAIN Integration**
   - Trigger RETAIN from Stop hook
   - Extract learnings from all documentation files
   - Classify into 4-network memory

3. **Validation Improvements**
   - Check for empty sections in THOUGHTS.md
   - Validate decision format in DECISIONS.md
   - Ensure RESULTS.md has actionable outcomes

### 7.3 Long-term Enhancements

1. **Smart Documentation**
   - Auto-suggest sections based on task type
   - Extract decisions automatically from THOUGHTS.md
   - Generate LEARNINGS.md from diff analysis

2. **Documentation Analytics**
   - Track documentation completeness over time
   - Identify patterns in high-quality documentation
   - Recommend improvements based on task outcomes

3. **Cross-Run Learning**
   - Link related documentation across runs
   - Surface relevant past decisions
   - Build decision dependency graph

---

## 8. Appendix

### 8.1 Document Templates

**THOUGHTS.md Template:**
```markdown
# THOUGHTS - {agent_type} Run {run_id}

**Timestamp:** {timestamp}
**Agent:** {agent_type}
**Task:** {task_id}

---

## Pre-Execution Research

### Duplicate Check
- [ ] Checked completed/ for similar tasks
- [ ] Checked recent commits
- Result: [No duplicates found / Potential duplicates: ...]

### Context Gathered
- Files read: [...]
- Key findings: [...]

### Risk Assessment
- Integration risks: [Low/Medium/High]
- Blockers: [...]

---

## Reasoning Log

### Decision 1: [Topic]
**Context:** [What we knew]
**Options Considered:**
- Option A: [...]
- Option B: [...]
**Decision:** [What we chose]
**Rationale:** [Why]
**Confidence:** [High/Medium/Low]

---

## Analysis

[Deep analysis of findings]

---

## Next Steps

[Planned actions]
```

**RESULTS.md Template:**
```markdown
# RESULTS - {agent_type} Run {run_id}

**Timestamp:** {timestamp}
**Task:** {task_id}
**Status:** [In Progress / Completed / Blocked]

---

## Executive Summary

[One-paragraph summary of outcomes]

---

## Actions Taken

### 1. [Action Name] ([Status])
[Description]

**Key Findings:**
- [...]

---

## Deliverables

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

---

## Validation

[How results were validated]

---

## Next Steps

[Recommended follow-up actions]
```

### 8.2 File Locations

| Component | Path |
|-----------|------|
| Run Templates | `~/.blackbox5/5-project-memory/blackbox5/.templates/run/` |
| SessionStart Hook | `~/.blackbox5/2-engine/.autonomous/hooks/pipeline/session-start/` |
| Stop Hook | `~/.blackbox5/2-engine/.autonomous/hooks/pipeline/stop/` |
| PreCompact Hook | `~/.blackbox5/2-engine/.autonomous/hooks/pipeline/pre-compact/` |
| Subagent Hooks | `~/.blackbox5/2-engine/.autonomous/hooks/pipeline/subagent-*/` |
| Task Completion | `~/.blackbox5/2-engine/.autonomous/workflows/task-completion.yaml` |
| Task Execution | `~/.blackbox5/2-engine/.autonomous/workflows/task-execution.yaml` |

---

*Documented for BB5 Documentation Systems Architecture*
