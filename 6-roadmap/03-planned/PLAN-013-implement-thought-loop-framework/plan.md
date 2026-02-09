# PLAN-008: Implement Thought Loop Framework

**Priority:** 🔴 CRITICAL
**Estimated Effort:** 1-2 weeks
**Dependencies:** None
**Status:** 📋 Planned
**Created:** 2026-01-20

---

## Problem Statement

**Current State:** Blackbox5 has no iterative reasoning capability. AI agents make decisions in a single pass, which is error-prone and lacks the deep validation that comes from questioning assumptions and researching to validate conclusions.

**Desired State:** AI agents can run thought loops with up to 10 iterations of first-principles reasoning, arriving at highly confident answers through self-questioning, assumption validation, and research.

**Impact:** This is THE critical missing piece. Without thought loops, autonomous self-improvement is impossible. WITH thought loops, Blackbox5 can validate its own reasoning and converge on correct answers.

---

## Vision

### The Core Innovation

**Research Finding:** AI with iterative first-principles thought loops will almost always arrive at the correct answer by the 10th iteration, significantly outperforming:
- Single-pass AI reasoning (prone to hallucinations)
- Human selection from AI options (80% accuracy at best)

### Important: Thought Loops Are Standalone

**Thought loops do NOT require Vibe Kanban, agent spawning, or any external coordination system.**

Thought loops are **pure internal reasoning** - they happen entirely within an agent's own mind:
- The agent thinks about a problem
- Questions its own assumptions
- Researches to validate them
- Updates its understanding
- Repeats until confident

**What thought loops need:**
- ✅ Research capability (to validate assumptions)
- ✅ LLM access (for reasoning)
- ✅ Memory (to track iterations)

**What thought loops DON'T need:**
- ❌ Vibe Kanban (task management - irrelevant for internal reasoning)
- ❌ Agent spawning (this is one agent thinking, not multiple agents)
- ❌ Git operations (no code changes during thought)
- ❌ External coordination (self-contained reasoning process)

**This matters because:**
1. **Simpler implementation** - Fewer dependencies, less complexity
2. **Faster execution** - No external system overhead
3. **More reliable** - Fewer moving parts to break
4. **Universal** - Can be used anywhere in the system

### The Thought Loop Pattern

```
FOR iteration = 1 to 10:
  1. State current understanding
  2. Identify assumptions made
  3. Question each assumption:
     - "Is this assumption true?"
     - "What evidence supports it?"
     - "What would contradict it?"
  4. Research to validate assumptions
  5. Update understanding based on findings
  6. Ask: "Do you even need to do this?"
     - First principles: What problem are we solving?
     - Is this improvement necessary?
  7. Check convergence:
     - Has understanding stabilized?
     - Are we confident (≥90%)?
     - If yes → EXIT
     - If no → CONTINUE
```

### Example Output

**Problem:** "Should we add caching to task router complexity analysis?"

**Iteration 1:** Confidence 60% - "Caching will help"
**Iteration 2:** Confidence 40% - "But it's only 11% of time"
**Iteration 3:** Confidence 70% - "Wrong bottleneck - look at agent loading"
**Iteration 4-7:** Confidence 90% - "Actually, current performance is fine"
**Iteration 8:** Confidence 95% - CONVERGED - "No improvement needed"

---

## Solution Design

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ThoughtLoop Engine                        │
│                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │   Problem  │ -> │ Iteration │ -> │  Research  │       │
│  │    Input   │    │   Logic    │    │   Engine   │       │
│  └────────────┘    └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────┐    ┌────────────┐       │
│                      │Assumption  │    │ Validation │       │
│                      │Identifier  │    │  Module    │       │
│                      └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────┐    ┌────────────┐       │
│                      │ First      │    │ Convergence│       │
│                      │ Principles │    │  Detector  │       │
│                      │   Check    │    │            │       │
│                      └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────────────────────────┐   │
│                      │     Result Generator          │   │
│                      │  (Final understanding +        │   │
│                      │   confidence + answer)         │   │
│                      └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Components

#### 1. ThoughtLoop Core

**File:** `2-engine/03-knowledge/loops/thought_loop.py`

**Responsibilities:**
- Manage iteration loop (up to 10 iterations)
- Track confidence across iterations
- Detect convergence
- Generate final result

**Interface:**
```python
class ThoughtLoop:
    async def run(self, problem: str) -> ThoughtLoopResult:
        """
        Run thought loop until convergence or max iterations.

        Args:
            problem: The problem to analyze

        Returns:
            ThoughtLoopResult with:
            - converged: bool
            - final_iteration: int
            - confidence: float
            - understanding: str
            - answer: str
        """
```

#### 2. Assumption Identifier

**File:** `2-engine/03-knowledge/loops/assumption_identifier.py`

**Responsibilities:**
- Extract assumptions from understanding
- Classify assumptions (critical, important, minor)
- Prioritize assumptions for validation

**Interface:**
```python
class AssumptionIdentifier:
    async def identify(self, understanding: str) -> List[Assumption]:
        """
        Identify assumptions in current understanding.

        Args:
            understanding: Current thinking

        Returns:
            List of assumptions found
        """
```

#### 3. Validation Module

**File:** `2-engine/03-knowledge/loops/validation.py`

**Responsibilities:**
- Research to validate assumptions
- Find supporting and contradicting evidence
- Calculate validity confidence

**Interface:**
```python
class ValidationModule:
    async def validate(self, assumption: Assumption) -> AssumptionValidation:
        """
        Validate an assumption through research.

        Args:
            assumption: The assumption to validate

        Returns:
            Validation with evidence and confidence
        """
```

#### 4. First-Principles Checker

**File:** `2-engine/03-knowledge/loops/first_principles_checker.py`

**Responsibilities:**
- Ask "Do you even need to do this?"
- Apply first-principles analysis
- Determine necessity

**Interface:**
```python
class FirstPrinciplesChecker:
    async def check(self, understanding: str) -> FirstPrinciplesCheck:
        """
        Apply first-principles validation.

        Args:
            understanding: Current understanding

        Returns:
            Check result with necessity determination
        """
```

#### 5. Convergence Detector

**File:** `2-engine/03-knowledge/loops/convergence.py`

**Responsibilities:**
- Track understanding stability
- Monitor confidence threshold
- Determine when to stop iterating

**Interface:**
```python
class ConvergenceDetector:
    def has_converged(self, iterations: List[Iteration]) -> bool:
        """
        Check if thought loop has converged.

        Args:
            iterations: All iterations so far

        Returns:
            True if converged (confidence ≥ 0.90)
        """
```

---

## Implementation Steps

### Step 1: Core ThoughtLoop Class (Day 1-2)

**Tasks:**
1. Create `thought_loop.py` with basic iteration logic
2. Implement iteration loop with max 10 iterations
3. Add confidence tracking
4. Create ThoughtLoopResult data class
5. Write basic tests

**Success Criteria:**
```python
loop = ThoughtLoop(problem="Should we add caching?")
result = await loop.run()
assert result.final_iteration <= 10
assert 0.0 <= result.confidence <= 1.0
```

### Step 2: Assumption Identifier (Day 2-3)

**Tasks:**
1. Create `assumption_identifier.py`
2. Implement assumption extraction from text
3. Add assumption classification
4. Test with sample problems

**Success Criteria:**
```python
identifier = AssumptionIdentifier()
assumptions = await identifier.identify("Caching will improve performance")
assert len(assumptions) > 0
assert any(a.statement == "Caching improves performance" for a in assumptions)
```

### Step 3: Validation Module (Day 3-4)

**Tasks:**
1. Create `validation.py`
2. Integrate with existing research engine
3. Implement evidence gathering
4. Add validity calculation
5. Test with known assumptions

**Success Criteria:**
```python
validator = ValidationModule()
validation = await validator.validate(assumption)
assert validation.validity in ["VALID", "INVALID", "UNCERTAIN"]
assert len(validation.supporting_evidence) > 0 or len(validation.contradicting_evidence) > 0
```

### Step 4: First-Principles Checker (Day 4-5)

**Tasks:**
1. Create `first_principles_checker.py`
2. Implement necessity questions
3. Add reasoning generation
4. Test with improvement proposals

**Success Criteria:**
```python
checker = FirstPrinciplesChecker()
check = await checker.check("We should add caching")
assert check.necessary in [True, False]
assert len(check.reasoning) > 0
```

### Step 5: Convergence Detector (Day 5-6)

**Tasks:**
1. Create `convergence.py`
2. Implement stability detection
3. Add confidence threshold check
4. Test convergence scenarios

**Success Criteria:**
```python
detector = ConvergenceDetector()
# Should converge when confidence ≥ 0.90
assert detector.has_converged(high_confidence_iterations) == True
assert detector.has_converged(low_confidence_iterations) == False
```

### Step 6: Integration & Testing (Day 6-10)

**Tasks:**
1. Integrate all components
2. Create end-to-end tests
3. Test with real problems
4. Validate convergence behavior
5. Performance optimization
6. Documentation

**Success Criteria:**
- Thought loop runs successfully on test problems
- Converges to ≥90% confidence for solvable problems
- Maxes out at 10 iterations for unsolvable problems
- All components integrated and working

---

## Testing Strategy

### Unit Tests

Each component tested in isolation:

```python
# Test assumption identification
def test_identify_assumptions():
    identifier = AssumptionIdentifier()
    assumptions = await identifier.identify("Caching improves performance")
    assert len(assumptions) >= 2

# Test validation
def test_validate_assumption():
    validator = ValidationModule()
    result = await validator.validate(assumption)
    assert result.validity in ["VALID", "INVALID", "UNCERTAIN"]

# Test convergence
def test_convergence_detection():
    detector = ConvergenceDetector()
    assert detector.has_converged(confident_iterations) == True
```

### Integration Tests

Full thought loop tested end-to-end:

```python
async def test_thought_loop_convergence():
    loop = ThoughtLoop()
    result = await loop.run("Should we add caching?")
    assert result.converged == True
    assert result.confidence >= 0.90
    assert result.final_iteration <= 10

async def test_thought_loop_max_iterations():
    loop = ThoughtLoop()
    result = await loop.run("Unsolvable problem")
    assert result.converged == False
    assert result.final_iteration == 10
```

### Validation Tests

Test against known problems with correct answers:

```python
async def test_known_problems():
    problems = [
        ("Is caching needed when only 11% of time?", "NO"),
        ("Should we optimize 450ms response?", "NO"),
        ("Should we fix critical security bug?", "YES"),
    ]
    for problem, expected_answer in problems:
        loop = ThoughtLoop()
        result = await loop.run(problem)
        assert result.answer == expected_answer
```

---

## Success Criteria

### Must Have (Required)

- [ ] Thought loop runs up to 10 iterations
- [ ] Confidence tracked and returned
- [ ] Convergence detection works (90% threshold)
- [ ] Assumptions identified from text
- [ ] Assumptions validated through research
- [ ] First-principles check implemented
- [ ] All components integrated
- [ ] Tests passing (80%+ coverage)

### Should Have (Important)

- [ ] Converges on correct answers for test problems
- [ ] Research integration works
- [ ] Evidence gathered and analyzed
- [ ] Reasoning is explainable
- [ ] Performance is acceptable (<30 seconds per thought loop)

### Could Have (Nice to Have)

- [ ] Parallel assumption validation
- [ ] Caching of research results
- [ ] Visualization of thought process
- [ ] Integration with agent decision-making

---

## Risk Mitigation

### Risk 1: Infinite Loops

**Mitigation:** Hard limit of 10 iterations, circuit breaker pattern

### Risk 2: Never Converges

**Mitigation:** Return best answer after max iterations with low confidence flag

### Risk 3: Slow Performance

**Mitigation:** Parallel validation, caching, early convergence detection

### Risk 4: Wrong Convergence

**Mitigation:** Require ≥90% confidence, human oversight for critical decisions

---

## Dependencies

### Internal Dependencies

- `2-engine/03-knowledge/storage/` - For research data
- `2-engine/01-core/resilience/` - Circuit breaker patterns
- Existing research engine (if available)

### External Dependencies

- LLM API (Anthropic Claude) - For reasoning
- Research sources (ArXiv, GitHub, etc.) - For validation

---

## Next Steps

### Immediate (This Week)

1. Create thought loop framework structure
2. Implement core ThoughtLoop class
3. Write basic tests

### Short Term (Next 2 Weeks)

1. Complete all components
2. Integration testing
3. Validation with real problems

### Long Term (Next 1-2 Months)

1. Integration with autonomous self-improvement system
2. Integration with agent decision-making
3. Production deployment

---

## Related Documents

- [AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md](../../../../1-docs/core/AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md) - Full vision
- [BLACKBOX5-CORE-FLOW.md](../../../../1-docs/core/BLACKBOX5-CORE-FLOW.md) - Core architecture
- [EXECUTION-PLAN.md](../EXECUTION-PLAN.md) - Overall execution strategy

---

**Status:** 📋 Planned
**Priority:** 🔴 CRITICAL - This is the foundation of autonomous self-improvement
**Estimated Effort:** 1-2 weeks
**Dependencies:** None
**Created:** 2026-01-20
