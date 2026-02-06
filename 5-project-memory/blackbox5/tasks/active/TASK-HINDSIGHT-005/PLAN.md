# PLAN.md: Implement REFLECT Operation

**Task:** TASK-HINDSIGHT-005 - REFLECT Operation
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 days
**Linked Goal:** IG-008 (Hindsight Memory System)
**Linked Plan:** PLAN-HINDSIGHT-001
**Importance:** 90 (High)

---

## 1. First Principles Analysis

### Why Does Hindsight Need REFLECT?

1. **Continuity of Self**: Agents need persistent beliefs that evolve over time, not just stateless responses
2. **Preference-Conditioned Reasoning**: Different contexts require different reasoning approaches (skeptical vs empathetic)
3. **Evidence-Based Updates**: Beliefs should change based on accumulated evidence, not just recent context
4. **Consistent Personality**: Users expect agents to behave consistently across sessions

### What Happens Without REFLECT?

- **Stateless Responses**: Each interaction starts from scratch, losing accumulated knowledge
- **Inconsistent Behavior**: Agent personality shifts based on prompt phrasing
- **No Belief Evolution**: Cannot update opinions based on new evidence
- **Missed Patterns**: Cannot recognize contradictions or trends across tasks

### How Should REFLECT Work?

1. **Disposition Profiles**: Configurable personality dimensions (skepticism, literalism, empathy, bias)
2. **Belief Storage**: Persistent storage of agent beliefs with confidence scores
3. **Evidence Tracking**: Record evidence that supports or contradicts beliefs
4. **Update Logic**: Bayesian-style belief updating based on evidence quality
5. **Contradiction Detection**: Identify and resolve conflicting beliefs

---

## 2. Current State Assessment

### Hindsight System Status

| Component | Status | Description |
|-----------|--------|-------------|
| RETAIN | Implemented | Stores task outcomes to memory |
| RECALL | Implemented | Retrieves relevant past context |
| **REFLECT** | **Not Implemented** | **Preference-conditioned reasoning** |
| Integration | Pending | Full pipeline integration |

### Existing Memory Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| Memory Store | `.autonomous/memory/store/` | Persistent storage |
| Task Outcomes | `outcomes/` | RETAIN output |
| Context Index | `index/` | RECALL retrieval |
| OPINIONS.md | Project root | Human-readable beliefs |

### Missing Components for REFLECT

1. **Disposition system** - No personality profiles
2. **Belief tracker** - No structured belief storage
3. **Evidence accumulation** - No evidence tracking
4. **Confidence scoring** - No belief confidence metrics
5. **Update mechanisms** - No belief evolution logic

---

## 3. Proposed Solution

### REFLECT Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        REFLECT Operation                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Disposition  │───▶│   Belief     │───▶│   Update     │  │
│  │  Profiles    │    │   Engine     │    │   Logic      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Skepticism   │    │  Evidence    │    │ Contradiction│  │
│  │ Literalism   │    │  Tracking    │    │  Resolution  │  │
│  │ Empathy      │    │  Confidence  │    │  Belief      │  │
│  │ Bias         │    │  Scoring     │    │  Evolution   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   OPINIONS.md    │
                    │  (Human-Readable) │
                    └──────────────────┘
```

### Disposition Profiles

**Dimensions:**

| Dimension | Range | Description |
|-----------|-------|-------------|
| **Skepticism** | 0-100 | Evidence threshold for accepting claims |
| **Literalism** | 0-100 | Interpretation strictness vs flexibility |
| **Empathy** | 0-100 | Weight given to user preferences |
| **Bias** | -100 to 100 | Confirmation (-) vs exploration (+) bias |

**Default Profile:**
```yaml
# .autonomous/memory/profiles/default.yaml
disposition:
  skepticism: 50      # Moderate evidence requirement
  literalism: 50      # Balanced interpretation
  empathy: 70         # High user preference weight
  bias: 0             # Neutral (no confirmation/exploration bias)

confidence:
  initial: 0.5        # Starting confidence for new beliefs
  threshold_high: 0.8 # Consider belief "strong"
  threshold_low: 0.2  # Consider belief "weak"

evidence:
  weight_direct: 1.0   # Direct observation
  weight_indirect: 0.5 # Indirect/inferred
  weight_hearsay: 0.2  # Secondhand information
```

### Belief Structure

```python
@dataclass
class Belief:
    """A belief held by the agent."""
    id: str                          # Unique identifier
    statement: str                   # Natural language belief
    confidence: float               # 0.0 to 1.0
    created_at: datetime
    updated_at: datetime
    evidence: List[Evidence]        # Supporting/contradicting evidence
    disposition_context: Dict       # Profile used when formed

@dataclass
class Evidence:
    """Evidence for or against a belief."""
    id: str
    belief_id: str
    type: EvidenceType              # DIRECT, INDIRECT, HEARSAY
    supports: bool                  # True = supports, False = contradicts
    source: str                     # Where evidence came from
    content: str                    # Evidence content
    timestamp: datetime
    weight: float                   # Calculated based on type
```

### Belief Update Logic

**Bayesian-Inspired Update:**
```python
def update_belief(belief: Belief, new_evidence: Evidence) -> Belief:
    """Update belief confidence based on new evidence."""

    # Get disposition-adjusted weight
    base_weight = evidence_weights[new_evidence.type]
    skepticism_factor = 1 - (disposition.skepticism / 100)
    adjusted_weight = base_weight * skepticism_factor

    # Calculate confidence delta
    if new_evidence.supports:
        delta = adjusted_weight * (1 - belief.confidence)
    else:
        delta = -adjusted_weight * belief.confidence

    # Apply bias adjustment
    if disposition.bias > 0:  # Exploration bias
        delta = delta * 1.1  # More willing to change
    elif disposition.bias < 0:  # Confirmation bias
        delta = delta * 0.9  # Less willing to change

    # Update confidence
    belief.confidence = clamp(belief.confidence + delta, 0.0, 1.0)
    belief.evidence.append(new_evidence)
    belief.updated_at = now()

    return belief
```

### Contradiction Detection

```python
def detect_contradictions(beliefs: List[Belief]) -> List[Contradiction]:
    """Find beliefs that contradict each other."""
    contradictions = []

    for i, belief1 in enumerate(beliefs):
        for belief2 in beliefs[i+1:]:
            if are_contradictory(belief1.statement, belief2.statement):
                contradictions.append(Contradiction(
                    belief1=belief1,
                    belief2=belief2,
                    severity=calculate_severity(belief1, belief2)
                ))

    return contradictions

def resolve_contradiction(contradiction: Contradiction) -> Resolution:
    """Resolve a contradiction between beliefs."""
    b1, b2 = contradiction.belief1, contradiction.belief2

    # Strategy: Keep higher confidence belief
    if b1.confidence > b2.confidence + 0.2:
        return Resolution(
            action="WEAKEN",
            target=b2,
            reason=f"Lower confidence ({b2.confidence}) vs ({b1.confidence})"
        )
    elif b2.confidence > b1.confidence + 0.2:
        return Resolution(
            action="WEAKEN",
            target=b1,
            reason=f"Lower confidence ({b1.confidence}) vs ({b2.confidence})"
        )
    else:
        # Similar confidence - flag for review
        return Resolution(
            action="FLAG",
            target=None,
            reason="Similar confidence levels - manual review needed"
        )
```

---

## 4. Implementation Plan

### Phase 1: Disposition Profiles (Day 1)

**Files to Create:**
1. `.autonomous/memory/profiles/disposition.py` - Profile dataclasses and loading
2. `.autonomous/memory/profiles/default.yaml` - Default profile configuration
3. `.autonomous/memory/profiles/manager.py` - Profile management

**Features:**
- Load/save disposition profiles
- Validate profile values
- Profile inheritance (base → user → task)
- Profile switching

### Phase 2: Belief System Core (Day 1-2)

**Files to Create:**
1. `.autonomous/memory/belief.py` - Belief and Evidence dataclasses
2. `.autonomous/memory/operations/reflect.py` - REFLECT operation
3. `.autonomous/memory/store/belief_store.py` - Belief persistence

**Features:**
- Belief CRUD operations
- Evidence tracking
- Confidence calculation
- Belief serialization

### Phase 3: Update Logic (Day 2)

**Implementation:**
- Bayesian-inspired update algorithm
- Disposition-adjusted weighting
- Evidence accumulation
- Confidence bounds checking

### Phase 4: Contradiction Handling (Day 2-3)

**Implementation:**
- Contradiction detection algorithm
- Resolution strategies
- Flagging for manual review
- Automatic weakening of beliefs

### Phase 5: Integration (Day 3)

**Files to Modify:**
1. `OPINIONS.md` template - Add confidence format
2. RECALL integration - Context-aware reasoning
3. Task hooks - Trigger REFLECT on completion

### Phase 6: Testing (Day 3-4)

**Tests:**
- Unit tests for belief updates
- Contradiction detection tests
- Profile switching tests
- Integration tests

---

## 5. Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `.autonomous/memory/profiles/disposition.py` | Profile dataclasses |
| `.autonomous/memory/profiles/default.yaml` | Default profile |
| `.autonomous/memory/profiles/manager.py` | Profile management |
| `.autonomous/memory/belief.py` | Belief data structures |
| `.autonomous/memory/operations/reflect.py` | REFLECT operation |
| `.autonomous/memory/store/belief_store.py` | Belief persistence |
| `.autonomous/memory/tests/test_reflect.py` | Unit tests |

### Modified Files

| File | Changes |
|------|---------|
| `OPINIONS.md` | Add confidence scores and evidence links |
| RECALL module | Integrate beliefs into context |

---

## 6. Success Criteria

- [ ] Disposition profiles working (skepticism, literalism, empathy, bias)
- [ ] Belief updating working (update opinions with new evidence)
- [ ] Confidence tracking working (adjust scores based on evidence quality)
- [ ] Integration with RECALL working (context-aware reasoning)
- [ ] Consistent agent personality demonstrated across sessions
- [ ] Contradiction detection and resolution working

---

## 7. Rollback Strategy

If REFLECT causes issues:

1. **Immediate**: Disable REFLECT in configuration
2. **Short-term**: Revert to default profile only
3. **Full**: Remove belief storage, keep RETAIN/RECALL only

**Disable REFLECT:**
```python
# In configuration
hindsight:
  operations:
    retain: true
    recall: true
    reflect: false  # Disable REFLECT
```

---

## 8. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Phase 1: Disposition Profiles | 4 hours |
| Phase 2: Belief System Core | 6 hours |
| Phase 3: Update Logic | 4 hours |
| Phase 4: Contradiction Handling | 4 hours |
| Phase 5: Integration | 4 hours |
| Phase 6: Testing | 4 hours |
| **Total** | **26 hours (3-4 days)** |

---

## 9. Key Design Decisions

### Decision 1: Bayesian vs Rule-Based Updates
**Choice:** Bayesian-inspired with disposition adjustments
**Rationale:** Mathematically sound, naturally handles confidence, extensible

### Decision 2: Profile Inheritance
**Choice:** Base → User → Task hierarchy
**Rationale:** Allows defaults with overrides at appropriate levels

### Decision 3: Contradiction Resolution Strategy
**Choice:** Confidence-based with manual fallback
**Rationale:** Automatic for clear cases, human judgment for edge cases

### Decision 4: Evidence Types
**Choice:** Direct, Indirect, Hearsay with configurable weights
**Rationale:** Reflects real-world evidence quality differences

---

## 10. Dependencies

- [ ] TASK-HINDSIGHT-004 (RECALL must be working for context)

---

*Plan created based on Hindsight architecture and task requirements*
