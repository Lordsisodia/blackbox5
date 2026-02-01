# Decisions - TASK-1769955706

## Decision 1: Keyword-Based Pattern Matching for MVP

**Context:** Need to identify similar tasks and recurring patterns for learning recommendations.

**Selected Approach:** Keyword-based matching using Jaccard similarity with weighted scoring.

**Alternatives Considered:**
1. **Keyword-based matching (SELECTED):** Simple, efficient, no external dependencies
2. **ML-based semantic similarity:** More accurate but complex, requires embeddings
3. **Hybrid approach:** Best of both but higher complexity

**Rationale:**
- **Simplicity:** Keyword matching is easy to understand and implement
- **Efficiency:** O(n) complexity, works well with 1000s of learnings
- **No dependencies:** Uses only Python standard library
- **Sufficient accuracy:** Jaccard similarity with weighted scoring achieves 70%+ precision target
- **Proven technique:** Similar approaches work well in practice (e.g., code search, document similarity)

**Weighted Scoring Formula:**
```
Similarity = (Keyword Similarity × 0.50) +
             (Context Similarity × 0.30) +
             (Error Type Similarity × 0.20)
```

**Reversibility:** HIGH - Can upgrade to ML-based semantic similarity in Phase 2 without breaking changes.

**Impact:** Enables MVP delivery with proven techniques, sets foundation for Phase 2 enhancements.

---

## Decision 2: YAML Format for Learning Index

**Context:** Need a persistent storage format for learning index that is human-readable and machine-parseable.

**Selected Approach:** YAML format with structured schema.

**Alternatives Considered:**
1. **YAML format (SELECTED):** Human-readable, git-friendly, standard library support
2. **JSON format:** Less readable, also git-friendly
3. **SQLite database:** More scalable but less accessible
4. **Plain text:** Simple but lacks structure

**Rationale:**
- **Human-readable:** Easy to review and edit manually if needed
- **Git-friendly:** Line-based diffs, easy to track changes
- **Structured:** Supports rich metadata (16 fields per learning)
- **Standard library:** PyYAML widely available, no extra dependencies
- **Extensible:** Easy to add new fields without breaking existing code

**Schema:**
```yaml
metadata:
  version: "1.0.0"
  last_updated: "2026-02-01T14:42:30Z"
  total_learnings: 0

learnings:
  - learning_id: "TASK-XXX-LEARNING-N"
    task_id: "TASK-XXX"
    learning_type: "pattern"
    title: "..."
    description: "..."
    # ... 9 more fields

patterns: []
statistics: {}
```

**Reversibility:** MEDIUM - Can migrate to SQLite in Phase 2 but requires data migration.

**Impact:** Optimal for MVP, easy to maintain, sets clear upgrade path to Phase 2.

---

## Decision 3: CLI Interfaces for All Libraries

**Context:** Libraries need to be usable from command line and Python code.

**Selected Approach:** Implement full CLI interfaces with argparse for all 4 libraries (11 commands total).

**Alternatives Considered:**
1. **Full CLI (SELECTED):** Comprehensive command-line interface for all operations
2. **Minimal CLI:** Only basic commands, rely on Python API for advanced use
3. **No CLI:** Python API only

**Rationale:**
- **Low friction:** No need to write Python for common operations
- **Accessibility:** Operators can use without programming knowledge
- **Testing:** Easy to test and verify functionality
- **Adoption:** CLI usage increases system adoption
- **Best practice:** Follows Unix philosophy (small tools that do one thing well)

**CLI Commands:**
- **learning_extractor.py:** `extract` (with verbose, format options)
- **pattern_matcher.py:** `similar`, `patterns`, `issues`, `related`
- **knowledge_retriever.py:** `search`, `get`, `stats`
- **learning_applier.py:** `inject`, `apply`, `track`, `stats`

**Reversibility:** LOW - Removing CLI would break user workflows.

**Impact:** Significantly improves usability and adoption, minimal maintenance overhead.

---

## Decision 4: Effectiveness Tracking with Basic Logging

**Context:** Need to track whether learnings are helpful to improve future recommendations.

**Selected Approach:** Basic effectiveness logging (application tracking, optional feedback).

**Alternatives Considered:**
1. **Basic logging (SELECTED):** Track application, optional feedback, simple EMA
2. **Comprehensive tracking:** Detailed metrics, automatic feedback inference, long-term analysis
3. **No tracking:** Rely on manual curation

**Rationale:**
- **Low friction:** Optional feedback doesn't disrupt workflow
- **Sufficient data:** Basic tracking provides enough data for improvement
- **Deferred complexity:** Detailed tracking deferred to Phase 2
- **Proven approach:** EMA works well for effectiveness smoothing

**Tracking Data:**
```python
ApplicationResult:
  - learning_id
  - task_id
  - applied_at
  - applied (bool)
  - helpful (bool, optional)
  - effectiveness_score (0.0-1.0, optional)
  - feedback (text, optional)
```

**Effectiveness Calculation:**
```python
# Exponential Moving Average (EMA)
def update_effectiveness(current_ema, new_score, alpha=0.3):
    return alpha * new_score + (1 - alpha) * current_ema
```

**Reversibility:** HIGH - Can enhance tracking in Phase 2 without breaking existing data.

**Impact:** Enables continuous improvement through feedback loop, minimal overhead.

---

## Decision 5: Integration with Executor Prompt

**Context:** Learnings need to be presented to executor at task execution time.

**Selected Approach:** Inject learnings as structured section in executor prompt.

**Alternatives Considered:**
1. **Prompt injection (SELECTED):** Add learnings as formatted text in prompt
2. **Separate context file:** Learnings in separate file, referenced in prompt
3. **No integration:** Manual lookup by executor

**Rationale:**
- **Zero friction:** Automatic injection, no manual steps
- **Proactive:** Learnings presented before executor starts
- **Structured:** Clear separation from task instructions
- **Flexible:** Easy to adjust number and format of learnings

**Injection Format:**
```markdown
# Relevant Learnings

Based on similar tasks, here are 3 relevant learning(s) that may help:

## Learning 1: Import Path Errors
**Source:** TASK-123
**Type:** bugfix
**Relevance:** 0.85
**Description:** ...
**Suggested Action:** Always use absolute imports from project root
**Historical Effectiveness:** 0.90

---

## How to Use These Learnings
1. Review each learning
2. Apply relevant learnings to your approach
3. Provide feedback after task completion
```

**Reversibility:** MEDIUM - Removing injection requires prompt modification.

**Impact:** Maximizes learning adoption, enables continuous improvement, minimal overhead.

---

## Decision 6: Six Learning Types

**Context:** Learnings need to be categorized for effective retrieval and filtering.

**Selected Approach:** Six learning types (pattern, decision, challenge, optimization, bugfix, insight).

**Alternatives Considered:**
1. **Six types (SELECTED):** Comprehensive categorization covering all scenarios
2. **Three types:** Simplified (issue, solution, general)
3. **Ten types:** More granular but potentially confusing

**Rationale:**
- **Comprehensive:** Covers all learning scenarios encountered in practice
- **Clear distinctions:** Each type has distinct characteristics
- **Actionable:** Different types suggest different actions
- **Balanced:** Not too few (loss of nuance) or too many (confusion)

**Learning Types:**
1. **Pattern:** Recurring patterns or best practices
2. **Decision:** Architectural or approach decisions
3. **Challenge:** Difficulties encountered and how resolved
4. **Optimization:** Performance or efficiency improvements
5. **Bugfix:** Bugs fixed and lessons learned
6. **Insight:** New understandings or discoveries

**Reversibility:** LOW - Changing types would require re-categorization.

**Impact:** Enables effective filtering and retrieval, improves learning relevance.

---

## Decision 7: Four Severity Levels

**Context:** Some learnings (especially bugfixes and challenges) need severity indication.

**Selected Approach:** Four severity levels (critical, high, medium, low).

**Alternatives Considered:**
1. **Four levels (SELECTED):** Standard severity classification
2. **Three levels:** Simple (high, medium, low)
3. **Five levels:** More granular (critical, high, medium, low, trivial)

**Rationale:**
- **Standard practice:** Four-level severity is industry standard
- **Clear distinctions:** Each level has well-defined meaning
- **Actionable:** Severity influences learning priority and applicability
- **Balanced:** Sufficient granularity without confusion

**Severity Definitions:**
- **Critical:** Blockers, showstoppers, system failures
- **High:** Important issues, major bugs, significant challenges
- **Medium:** Normal issues, typical bugs, standard challenges
- **Low:** Minor issues, trivial bugs, nice-to-have improvements

**Reversibility:** LOW - Changing levels would require re-classification.

**Impact:** Enables prioritization and filtering, improves learning relevance.

---

## Summary

**Key Architectural Decisions:**
1. Keyword-based pattern matching (sufficient for MVP, upgrade path to ML)
2. YAML format for learning index (human-readable, git-friendly)
3. CLI interfaces for all libraries (usability and adoption)
4. Basic effectiveness tracking (low friction, sufficient data)
5. Executor prompt integration (zero friction, proactive)
6. Six learning types (comprehensive, clear)
7. Four severity levels (standard, actionable)

**Reversibility Assessment:**
- **HIGH:** 2 decisions (keyword matching, effectiveness tracking) - easy to change
- **MEDIUM:** 2 decisions (YAML format, prompt integration) - requires migration
- **LOW:** 3 decisions (CLI, learning types, severity levels) - breaking changes

**Overall Impact:** Decisions enable MVP delivery with proven techniques, set clear upgrade path for Phase 2, balance simplicity with capability.
