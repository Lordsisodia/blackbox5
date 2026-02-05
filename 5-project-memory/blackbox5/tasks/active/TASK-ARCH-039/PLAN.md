# PLAN.md: Unified ResourceManager for Phase Gates and Context Budget

**Task:** TASK-ARCH-039 - Phase Gates and Context Budget Use Different Threshold Models
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2 hours
**Importance:** 70 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Two independent resource management systems (phase gates and context budget) operate without coordination, leading to:
- Conflicting decisions about when to proceed vs. checkpoint
- Phase gates unaware of context constraints
- Context budget unaware of phase-specific requirements
- No unified view of resource health

### First Principle
Resource management is a single concern that should have a unified decision-making authority.

### Key Insight
Phase gates and context budget are both measuring "readiness to continue" but using different metrics:
- Phase gates: "Have we completed the required work for this phase?"
- Context budget: "Do we have sufficient resources to continue?"

These questions must be answered together, not independently.

---

## 2. Current State: Independent Operation

### Phase Gates System
- **File:** `2-engine/.autonomous/lib/phase_gates.py`
- **Model:** Phase-based progression (quick_spec → dev_story → code_review OR align → plan → execute → validate → wrap)
- **Checks:** Required files, exit criteria verification, entry gate validation
- **State Files:** `.gate_{phase}_passed`, `.phase_{phase}_criteria`
- **Failure Actions:** cannot_proceed, rollback_and_retry, return_to_dev_story, rollback_to_plan, cannot_complete

### Context Budget System
- **File:** `2-engine/.autonomous/lib/context_budget.py`
- **Model:** Token percentage thresholds (40%, 70%, 85%, 95%)
- **Checks:** Current token usage against max budget
- **State Files:** `context_budget.json`, `.subagent_spawned`
- **Actions:** spawn_subagent, summarize_thoughts, spawn_subagent_critical, force_checkpoint

### Coordination Problems Identified

1. **No Shared State** - Phase gates don't check context budget before allowing phase completion
2. **Conflicting Decisions Possible** - Phase gate says "proceed" while context budget says "checkpoint"
3. **Phase-Aware Context Management Missing** - Different phases have different context needs
4. **Duplicate State Management** - Both systems maintain separate state files
5. **Agent-2.3 AGENT.md References Both Independently** - No coordination mechanism specified

---

## 3. Proposed Solution: Unified ResourceManager

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ResourceManager                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ PhaseGate    │  │ ContextBudget│  │ Coordination     │  │
│  │   Monitor    │  │   Monitor    │  │   Engine         │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                   │            │
│         └─────────────────┴───────────────────┘            │
│                           │                                │
│                    ┌──────┴──────┐                        │
│                    │   Decision    │                        │
│                    │    Engine     │                        │
│                    └──────┬──────┘                        │
│                           │                                │
│         ┌─────────────────┼─────────────────┐              │
│         ▼                 ▼                 ▼              │
│    ┌─────────┐      ┌─────────┐      ┌─────────┐          │
│    │ PROCEED │      │ DEFER   │      │ CHECKPOINT│         │
│    └─────────┘      └─────────┘      └─────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Single Entry Point:** All resource checks go through ResourceManager
2. **Unified State:** Single state file for all resource management
3. **Phase-Aware Thresholds:** Context thresholds vary by phase
4. **Coordinated Decisions:** Both systems must agree before proceeding
5. **Backward Compatibility:** Existing scripts continue to work

### Phase-Aware Context Thresholds

| Phase | Sub-Agent | Warning | Critical | Hard Limit | Rationale |
|-------|-----------|---------|----------|------------|-----------|
| quick_spec | 40% | 70% | 85% | 95% | Standard thresholds |
| dev_story | 35% | 65% | 80% | 90% | Implementation needs more headroom |
| code_review | 45% | 75% | 88% | 95% | Review can use more context |
| align | 40% | 70% | 85% | 95% | Standard thresholds |
| plan | 30% | 60% | 75% | 85% | Planning needs most headroom |
| execute | 35% | 65% | 80% | 90% | Implementation needs headroom |
| validate | 40% | 70% | 85% | 95% | Standard thresholds |
| wrap | 50% | 80% | 90% | 95% | Documentation can use more context |

---

## 4. Implementation Steps

### Phase 1: Create ResourceManager Core (30 min)

**File:** `2-engine/.autonomous/lib/resource_manager.py`

1. Create `ResourceManager` class that wraps both systems
2. Implement unified state management
3. Add phase-aware threshold configuration
4. Implement coordination decision engine

**Key Methods:**
- `check_resources(phase, current_tokens)` - Unified health check
- `can_proceed(phase, current_tokens)` - Coordinated proceed decision
- `get_recommendation(phase, current_tokens)` - Unified recommendation
- `transition_phase(from_phase, to_phase)` - Coordinated phase transition

### Phase 2: Refactor Phase Gates (15 min)

**File:** `2-engine/.autonomous/lib/phase_gates.py`

1. Add `ResourceManager` integration option
2. Add `check_context_budget` parameter to `validate_phase_gate()`
3. Maintain backward compatibility (default: no integration)
4. Add `get_phase_context_thresholds(phase)` function

### Phase 3: Refactor Context Budget (15 min)

**File:** `2-engine/.autonomous/lib/context_budget.py`

1. Add `ResourceManager` integration option
2. Add `get_phase_aware_thresholds(phase)` method
3. Maintain backward compatibility (default: no integration)
4. Add phase context to state tracking

### Phase 4: Update RALF Loop Integration (15 min)

**File:** `2-engine/.autonomous/shell/ralf-loop.sh`

1. Replace separate `check_phase_gate` and `check_context_budget` calls
2. Add unified `check_resources` call
3. Update initialization to use ResourceManager
4. Maintain fallback to individual systems

### Phase 5: Update Agent-2.3 Documentation (15 min)

**File:** `2-engine/.autonomous/prompt-progression/versions/v2.3/AGENT.md`

1. Update resource management section
2. Replace separate threshold tables with unified model
3. Update initialization instructions
4. Add coordination examples

---

## 5. Files to Modify/Create

### New Files
1. `2-engine/.autonomous/lib/resource_manager.py` - Core coordination system
2. `2-engine/.autonomous/lib/test_resource_manager.py` - Unit tests

### Modified Files
1. `2-engine/.autonomous/lib/phase_gates.py` - Add ResourceManager integration
2. `2-engine/.autonomous/lib/context_budget.py` - Add phase-aware thresholds
3. `2-engine/.autonomous/shell/ralf-loop.sh` - Use unified checks
4. `2-engine/.autonomous/prompt-progression/versions/v2.3/AGENT.md` - Update documentation

### Backward Compatibility
- All existing scripts continue to work unchanged
- ResourceManager is opt-in via new parameter
- Individual systems remain functional standalone

---

## 6. Success Criteria

- [ ] ResourceManager class created with unified state management
- [ ] Phase-aware context thresholds implemented
- [ ] Coordination decision engine working (both systems must agree)
- [ ] Phase gates can check context budget before allowing completion
- [ ] Context budget uses phase-appropriate thresholds
- [ ] ralf-loop.sh uses unified ResourceManager
- [ ] Agent-2.3 documentation updated
- [ ] Unit tests pass for ResourceManager
- [ ] Backward compatibility verified (existing scripts work)
- [ ] Integration test: Phase gate blocks when context critical
- [ ] Integration test: Context budget adjusts for different phases

---

## 7. Rollback Strategy

If changes cause issues:

1. **Immediate:** Revert to individual system calls in ralf-loop.sh
2. **Short-term:** Disable ResourceManager integration in phase_gates.py and context_budget.py
3. **Full:** Remove ResourceManager and restore original files from git

**Rollback Commands:**
```bash
cd ~/.blackbox5
git checkout -- 2-engine/.autonomous/lib/phase_gates.py
git checkout -- 2-engine/.autonomous/lib/context_budget.py
git checkout -- 2-engine/.autonomous/shell/ralf-loop.sh
rm -f 2-engine/.autonomous/lib/resource_manager.py
```

---

## 8. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Create ResourceManager Core | 30 min | 30 min |
| Phase 2: Refactor Phase Gates | 15 min | 45 min |
| Phase 3: Refactor Context Budget | 15 min | 60 min |
| Phase 4: Update RALF Loop | 15 min | 75 min |
| Phase 5: Update Documentation | 15 min | 90 min |
| Testing & Validation | 30 min | 120 min |
| **Total** | | **2 hours** |

---

## 9. Key Design Decisions

### Decision 1: Wrapper vs. Integration
**Choice:** Create ResourceManager as a wrapper/coordination layer rather than merging the systems
**Rationale:** Maintains separation of concerns, easier to test individual components, allows gradual migration

### Decision 2: Phase-Aware Thresholds
**Choice:** Different thresholds per phase rather than uniform thresholds
**Rationale:** PLAN phase needs more headroom for architecture decisions, WRAP phase can use more context for documentation

### Decision 3: Unified State File
**Choice:** Single YAML state file instead of multiple files
**Rationale:** Single source of truth, easier debugging and monitoring, atomic updates prevent inconsistency

### Decision 4: Backward Compatibility
**Choice:** Opt-in integration rather than mandatory
**Rationale:** Existing workflows continue working, allows gradual rollout, easier to test and validate

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing workflows | Low | High | Backward compatibility mode, opt-in integration |
| Performance overhead | Low | Low | Lazy loading, caching of state |
| State file corruption | Low | Medium | Atomic writes, backup files, recovery mode |
| Coordination logic bugs | Medium | High | Comprehensive unit tests, fallback to individual systems |
| Phase threshold tuning | Medium | Medium | Configurable thresholds, metrics collection |

---

*Plan created based on analysis of phase_gates.py and context_budget.py coordination issues*
