# Context Checkpointing System - Proposal

**Status:** Analysis Complete
**Date:** 2026-02-07
**Proposed By:** User + Claude Analysis

---

## Executive Summary

**VERDICT: PROCEED WITH IMPLEMENTATION**

The Context Checkpointing proposal is **highly feasible** and represents a natural evolution of existing BlackBox5 infrastructure. It solves the critical problem of context window degradation in long-running RALF loops by preserving key decisions and compressing history into per-route checkpoint files.

**Key Innovation:** On-demand context access rather than auto-injection, preserving token budget while maintaining long-running context awareness.

---

## The Problem

| Issue | Impact | Current Behavior |
|-------|--------|------------------|
| Context window degradation | 12-18% accuracy drop after 40% utilization | Information lost to sliding window truncation |
| Fresh RALF start each run | No memory of previous work | Must rediscover context each session |
| Token inefficiency | Wasted tokens on irrelevant history | Auto-injected context may not be needed |
| Decision loss | Critical choices forgotten | Decisions buried in THOUGHTS.md get truncated |

---

## The Solution

### Core Concept

Create **per-route context checkpoint files** that:
1. **Persist** key decisions, active work state, compressed history across runs
2. **Checkpoint** (summarize) every ~50k tokens or at task completion
3. **Access** on-demand rather than auto-injected (token efficiency)
4. **Integrate** with existing RALF, timeline-memory, session_tracker

### File Structure

```
.autonomous/context/routes/{route-name}.md
```

**Format:** YAML frontmatter + Markdown sections

```yaml
---
context_checkpoint:
  version: "1.0.0"
  route: "api-refactoring"
  agent_type: "executor"
  created: "2026-02-07T10:00:00Z"
  last_checkpoint: "2026-02-07T14:30:00Z"
  checkpoint_count: 3
  tokens_at_checkpoint: 52000
  total_tokens_consumed: 156000

decisions:
  - id: "DEC-001"
    timestamp: "2026-02-07T10:15:00Z"
    decision: "Use FastAPI over Flask"
    rationale: "Better async support"
    status: "active"

active_work:
  current_task: "TASK-001"
  current_phase: "execute"
  work_status: "in_progress"
  open_files:
    - path: "src/api/routes.py"
      last_modified: "2026-02-07T14:25:00Z"

checkpoint_history:
  - checkpoint_id: "cp-001"
    timestamp: "2026-02-07T10:00:00Z"
    tokens: 50000
    summary_ref: "## Checkpoint 1: Initial Setup"
    key_events: ["Project initialized"]
---

## Compressed History

### Checkpoint 3: Auth Middleware (Current)
**Period:** 2026-02-07T12:00:00Z → 2026-02-07T14:30:00Z
**Tokens:** 52,000

Started implementing JWT authentication middleware...

---

*This file is automatically managed. Do not edit manually.*
```

---

## Architecture

### Checkpointing Flow

```
Token Threshold (~50k) Reached
         │
         ▼
┌─────────────────────┐
│ Spawn Summarization │
│    Sub-Agent        │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Extract & Preserve │
│  ─────────────────  │
│  • Decisions        │
│  • Active work      │
│  • File states      │
│                     │
│  Summarize          │
│  ─────────────────  │
│  • Reasoning        │
│  • Code snippets    │
│  • Exploration      │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Update Context File│
│  (atomic write)     │
└─────────────────────┘
```

### Access Patterns

| Pattern | When | How |
|---------|------|-----|
| **Explicit** | Agent needs historical context | `context_reader.get_context("api-refactoring")` |
| **Session Start** | Route detected | Display: "Context available: use --load-context" |
| **Lazy-Loaded** | Route mentioned in prompt | Auto-load if referenced |

---

## Implementation Plan

### MVP (1 Day)

**Goal:** Validate the approach with minimal implementation

1. **Create core data model** (`context_checkpoint.py`)
   - Checkpoint dataclass
   - File I/O with YAML frontmatter
   - Basic summarization

2. **Create file structure** (`context_manager.py`)
   - Directory: `.autonomous/context/routes/`
   - Route ID from task/routes.yaml

3. **Manual test**
   - Create checkpoint manually
   - Verify file format
   - Read it back

### Phase 1: Core System (1 Week)

| Task | Effort | Files |
|------|--------|-------|
| Checkpoint data model | Small | `context_checkpoint.py` |
| Context file structure | Small | `context_manager.py` |
| Checkpoint trigger integration | Small | Modify `context_budget.py` |
| Summarization engine | Medium | `context_summarizer.py` |
| Context reader | Medium | `context_reader.py` |

### Phase 2: Integration (1 Week)

| Task | Effort | Files |
|------|--------|-------|
| Session tracker integration | Small | Modify `session_tracker.py` |
| RALF loop hooks | Large | Modify `ralf.md`, `ralf-executor.md` |
| CLI commands | Small | `ralf context list`, `ralf context show` |
| Hook scripts | Small | `context-checkpoint.sh` |

### Phase 3: Migration (3 Days)

- Migration script from `timeline-memory.md`
- Backward compatibility layer
- Deprecation warnings

---

## Integration Points

### 1. context_budget.py (Reuse Threshold System)

```python
# Add checkpoint action at 70% threshold
def _trigger_checkpoint(self):
    """Create context checkpoint before context loss."""
    subprocess.run([
        "python3", "context_checkpoint.py", "create",
        "--route", os.environ.get("BB5_ROUTE", "default"),
        "--tokens", str(self.current_tokens)
    ])
```

### 2. session_tracker.py (Extend Run Tracking)

```python
def record_checkpoint(self, checkpoint_id: str):
    """Record checkpoint ID in run tracking."""
    self.run_data['checkpoint_id'] = checkpoint_id
    self._save_tracking()
```

### 3. RALF Loop (On-Demand Loading)

```markdown
<!-- In ralf.md -->
## Context Checkpointing

If a context checkpoint exists for this route:
- Path: `.autonomous/context/routes/{route-name}.md`
- Access via: `context_reader.get_context("{route-name}")`
- Use when you need historical decisions or work state

Do NOT auto-load context checkpoints. Access on-demand only.
```

---

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Checkpoint bloat | High | Compress at 10:1 ratio; archive old checkpoints |
| Stale context | Medium | Timestamp all entries; verify relevance before use |
| Concurrent overwrites | Medium | Atomic file writes; append-only history |
| Token count inaccuracy | Medium | Use tiktoken; 10% safety margin |
| Over-reliance | Low | Keep as reference-only; decisions from current context |

---

## Comparison: Existing vs Proposed

| Aspect | Current (timeline-memory) | Proposed (context-checkpoint) |
|--------|---------------------------|-------------------------------|
| **Injection** | Auto-injected at start | On-demand access |
| **Granularity** | Per-agent | Per-route |
| **Trigger** | Manual updates | Auto-checkpoint at 50k tokens |
| **Compression** | None | 10:1 summarization |
| **Access** | Always loaded | Explicitly requested |
| **Token cost** | Fixed overhead | Pay-only-for-what-you-use |

---

## Key Decisions Needed

1. **Checkpoint threshold:** 50k tokens vs 70% (140k) vs adaptive
   - **Recommendation:** Start with 50k for granularity

2. **Route ID granularity:** Per-task vs per-goal vs per-project
   - **Recommendation:** Per-task (task_id) for fine-grained context

3. **Retention policy:** Keep all vs last N vs time-based
   - **Recommendation:** Keep all for now; archive after 90 days

4. **Integration with timeline:** Replace vs extend vs parallel
   - **Recommendation:** Extend - timeline for events, checkpoints for context

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Context retrieval accuracy | >90% | Can agent find relevant historical decision? |
| Token efficiency | <5% overhead | Tokens spent on context vs total |
| Checkpoint creation | 100% | Every 50k threshold triggers checkpoint |
| User satisfaction | Qualitative | "I don't lose context between runs" |

---

## Next Steps

### Immediate (This Week)

1. **Approve proposal** - User review and go/no-go
2. **Create MVP branch** - `feature/context-checkpointing`
3. **Implement data model** - `context_checkpoint.py` core
4. **Manual validation** - Test with one route

### Short-term (Next 2 Weeks)

1. Complete Phase 1 implementation
2. Integration testing with RALF
3. Documentation updates

### Long-term (Future)

1. Vector search integration for intelligent retrieval
2. Automatic checkpoint archival
3. Checkpoint diff visualization

---

## References

- Existing timeline-memory: `/5-project-memory/blackbox5/.autonomous/research-pipeline/agents/*/timeline-memory.md`
- Context budget: `/2-engine/helpers/legacy/context_budget.py`
- Session tracker: `/2-engine/helpers/legacy/session_tracker.py`
- RALF instructions: `/2-engine/instructions/ralf.md`
- Decision registry: `/5-project-memory/blackbox5/.autonomous/decisions/decision_registry.yaml`

---

*Generated by Claude Code with sub-agent analysis*
*Analysis completed: 2026-02-07*
