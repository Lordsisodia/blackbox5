# PLAN.md: Decision Registry and Memory System Unification

**Task:** TASK-ARCH-038 - Decision Registry and Memory System Overlap
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 6-7 hours
**Importance:** 65 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Decision tracking is fragmented across two architectural layers:
- **DecisionRegistry** operates at the run/agent level with structured decision schemas
- **MemorySystem** operates at the message/conversation level with implicit decision capture

### Why This Matters
1. **Duplication**: Decisions recorded in DecisionRegistry are also captured as messages in MemorySystem
2. **Inconsistency**: No synchronization between the two representations
3. **Query Complexity**: Finding all decisions requires checking two systems
4. **Maintenance Overhead**: Two codebases to maintain for similar functionality

### First Principles Solution
- **Single Source of Truth**: DecisionRegistry owns decision tracking
- **Integration, Not Duplication**: MemorySystem references DecisionRegistry for decision queries
- **Clear Boundaries**:
  - DecisionRegistry = Structured decision tracking with reversibility
  - MemorySystem = Message/conversation context with decision references

---

## 2. Current State Analysis

### DecisionRegistry System

**Location:** `2-engine/.autonomous/lib/decision_registry.py`

**Capabilities:**
- Structured decision schema with fields:
  - `id`, `timestamp`, `phase` (ALIGN/PLAN/EXECUTE/VALIDATE/WRAP)
  - `options_considered` with pros/cons
  - `selected_option` and `rationale`
  - `assumptions` with risk levels and verification status
  - `reversibility` assessment (LOW/MEDIUM/HIGH)
  - `rollback_steps` for recovery
  - `verification` tracking
- CLI interface: `init`, `record`, `verify`, `list`, `rollback`, `finalize`
- YAML persistence per run directory
- Decision validation and completeness checking

### MemorySystem

**Location:** `2-engine/runtime/memory/systems/`

**Components:**
1. **ProductionMemorySystem** - Base message storage
2. **EnhancedProductionMemorySystem** - Adds semantic retrieval, importance scoring
3. **EpisodicMemory** - Groups messages into episodes with outcomes and lessons
4. **MemoryConsolidation** - Summarizes old messages

**Decision-Related Capabilities:**
- Messages can contain decision content (unstructured)
- Episodes can capture decision contexts
- Consolidation extracts "key decisions made" from message batches
- No structured decision schema or reversibility tracking

**Overlap Evidence:**
- MemoryConsolidation asks for "Key decisions made"
- EpisodicMemory tracks outcomes and lessons (similar to decision verification)
- Both systems track assumptions

---

## 3. Proposed Unification Architecture

### Design Principle: DecisionRegistry as Primary

```
┌─────────────────────────────────────────────────────────────┐
│                    DecisionRegistry                         │
│              (Primary Decision Authority)                   │
├─────────────────────────────────────────────────────────────┤
│  • Structured decision schema                               │
│  • Reversibility assessment                                 │
│  • Rollback planning                                        │
│  • Assumption verification                                  │
│  • YAML persistence per run                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ integrates with
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MemorySystem                             │
│           (References Decisions, Doesn't Duplicate)         │
├─────────────────────────────────────────────────────────────┤
│  • Message context (references decision IDs)                │
│  • Episodic memory links to decisions                       │
│  • Consolidation queries DecisionRegistry for summaries     │
│  • No inline decision storage                               │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

1. **Message Metadata Enhancement** - Messages can reference `decision_id` in metadata
2. **Episodic Memory Integration** - Episodes explicitly link to decisions via `decision_ids` field
3. **Consolidation Integration** - MemoryConsolidation queries DecisionRegistry for "key decisions"

---

## 4. Implementation Plan

### Phase 1: DecisionRegistry Enhancement (1-2 hours)

**File:** `2-engine/.autonomous/lib/decision_registry.py`

**Changes:**
1. Add query methods for external systems:
   ```python
   def get_decisions_for_task(self, task_id: str) -> List[Dict]
   def get_decisions_by_phase(self, phase: str) -> List[Dict]
   def get_recent_decisions(self, hours: int = 24) -> List[Dict]
   def get_decision_summary(self) -> Dict[str, Any]
   ```

2. Add export methods for MemorySystem integration:
   ```python
   def export_for_consolidation(self) -> str:
       """Export decisions in format suitable for memory consolidation"""
   ```

3. Add global registry discovery:
   ```python
   @staticmethod
   def find_registry_for_task(task_id: str) -> Optional[str]:
       """Find decision registry path for a given task"""
   ```

### Phase 2: MemorySystem Integration (2-3 hours)

**Files to Modify:**
- `2-engine/runtime/memory/systems/ProductionMemorySystem.py`
- `2-engine/runtime/memory/episodic/EpisodicMemory.py`
- `2-engine/runtime/memory/consolidation/MemoryConsolidation.py`

**Changes:**

1. **Message Class Enhancement**
   ```python
   @dataclass
   class Message:
       # ... existing fields ...
       decision_id: Optional[str] = None  # Reference to DecisionRegistry entry
   ```

2. **EpisodicMemory Enhancement**
   ```python
   class Episode:
       # ... existing fields ...
       decision_ids: List[str] = field(default_factory=list)

       def link_decision(self, decision_id: str):
           """Explicitly link episode to a decision"""
   ```

3. **MemoryConsolidation Refactoring**
   - Replace inline decision extraction with DecisionRegistry query
   - Update `_create_summary_prompt()` to use registry data
   - Add `decision_registry_path` parameter to config

### Phase 3: Migration and Deprecation (1 hour)

**Files to Create:**
- `2-engine/runtime/memory/docs/DECISION_INTEGRATION.md`

**Migration Steps:**
1. Document the new integration pattern
2. Mark MemorySystem's implicit decision tracking as deprecated
3. Update all run templates to use DecisionRegistry for decisions

### Phase 4: Validation and Testing (1 hour)

**Files to Create/Modify:**
- `2-engine/runtime/memory/tests/test_decision_integration.py`

**Test Coverage:**
1. DecisionRegistry query methods work correctly
2. Messages can reference decisions
3. Episodes can link to decisions
4. Consolidation pulls from DecisionRegistry
5. No duplication between systems

---

## 5. Files to Modify/Create

### Modify Existing Files

| File | Changes |
|------|---------|
| `2-engine/.autonomous/lib/decision_registry.py` | Add query methods, export functions, registry discovery |
| `2-engine/runtime/memory/systems/ProductionMemorySystem.py` | Add `decision_id` to Message dataclass |
| `2-engine/runtime/memory/episodic/Episode.py` | Add `decision_ids` field |
| `2-engine/runtime/memory/episodic/EpisodicMemory.py` | Add decision linking methods |
| `2-engine/runtime/memory/consolidation/MemoryConsolidation.py` | Query DecisionRegistry instead of extracting from messages |

### Create New Files

| File | Purpose |
|------|---------|
| `2-engine/runtime/memory/integrations/decision_registry_integration.py` | Integration layer between systems |
| `2-engine/runtime/memory/tests/test_decision_integration.py` | Integration tests |
| `2-engine/runtime/memory/docs/DECISION_INTEGRATION.md` | Documentation |

---

## 6. Success Criteria

- [ ] DecisionRegistry provides query methods for external systems
- [ ] MemorySystem Message class can reference decisions via `decision_id`
- [ ] EpisodicMemory can link episodes to decisions
- [ ] MemoryConsolidation queries DecisionRegistry for decision summaries
- [ ] No duplication: decisions only stored in DecisionRegistry
- [ ] All existing tests pass
- [ ] New integration tests pass
- [ ] Documentation updated

---

## 7. Rollback Strategy

If unification causes issues:

1. **Immediate**: Disable integration by setting `decision_registry_path=None` in MemoryConsolidation config
2. **Short-term**: Revert MemorySystem to extract decisions from messages (restore original behavior)
3. **Full**: Revert all changes using git history

---

## 8. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: DecisionRegistry Enhancement | 1-2 hours | 2 hours |
| Phase 2: MemorySystem Integration | 2-3 hours | 5 hours |
| Phase 3: Migration and Deprecation | 1 hour | 6 hours |
| Phase 4: Validation and Testing | 1 hour | 7 hours |
| **Total** | | **6-7 hours** |

---

## 9. Benefits of Unification

1. **Single Source of Truth**: Decisions tracked in one place
2. **Rich Decision Schema**: Reversibility, rollback plans, assumption verification
3. **Better Queryability**: Structured decision data enables better analysis
4. **Reduced Maintenance**: One system to maintain for decision tracking
5. **Clear Boundaries**: Each system has a well-defined responsibility

---

*Plan created based on analysis of DecisionRegistry and MemorySystem overlap*
