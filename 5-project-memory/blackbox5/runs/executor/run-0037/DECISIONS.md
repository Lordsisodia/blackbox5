# Decisions - TASK-1769911100

**Task ID:** TASK-1769911100
**Run Number:** 0037
**Date:** 2026-02-01

---

## Decision 1: Algorithm Selection - Jaccard Similarity

**Context:** Needed to choose similarity algorithm for duplicate task detection. Options included Jaccard, Cosine similarity, Levenshtein distance, semantic embeddings.

**Selected:** Jaccard similarity with keyword extraction

**Rationale:**
- **Simplicity:** Easy to understand, implement, and debug
- **Performance:** O(n × m) complexity, fast for typical task databases (< 1 second for 100+ tasks)
- **No dependencies:** Uses Python standard library only (sets, string operations)
- **Effectiveness:** Keyword matching works well for task titles/descriptions
- **Transparency:** Similarity score easy to explain and tune

**Alternatives Considered:**
1. **Cosine similarity with TF-IDF:** More complex, requires numpy/scipy, marginal benefit for short texts
2. **Levenshtein distance:** Good for typos, but doesn't handle word order changes well
3. **Semantic embeddings (BERT, etc.):** Most accurate, but heavy dependencies, slower, overkill for this use case

**Reversibility:** HIGH - Algorithm is encapsulated in `calculate_jaccard_similarity()` function, can be swapped without affecting interface.

---

## Decision 2: Similarity Threshold - 80%

**Context:** Threshold determines when tasks are flagged as duplicates. Too high misses duplicates; too low creates false positives.

**Selected:** 80% (0.8) default threshold

**Rationale:**
- **Balanced:** Based on testing with various task descriptions, 80% catches duplicates without excessive false positives
- **Industry standard:** Jaccard similarity commonly uses 0.7-0.9 range; 0.8 is middle ground
- **Configurable:** Documented how to adjust; users can tune based on their data
- **Empirical testing:** Tested thresholds from 60%-90%; 80% provided best balance

**Alternatives Considered:**
1. **70%:** Would catch more duplicates, but false positives increased significantly
2. **90%:** Fewer false positives, but would miss some actual duplicates (e.g., different wording, same meaning)
3. **Dynamic threshold:** Vary based on task type - too complex for v1.0

**Reversibility:** HIGH - Threshold is a parameter (`similarity_threshold=0.8`), can be adjusted in one line.

---

## Decision 3: Stopwords Filtering

**Context:** Task titles/descriptions contain many common words ("the", "create", "implement") that don't distinguish tasks.

**Selected:** Comprehensive stopwords list with minimum 4-character word length

**Rationale:**
- **Accuracy improved:** Without stopwords, similarity scores were inflated (e.g., "Create X" and "Create Y" appeared 80% similar)
- **List based on frequency:** Analyzed existing tasks, identified most common non-discriminative words
- **Action-oriented stopwords:** Included "create", "implement", "fix" because these don't distinguish what the task does

**Stopwords Included:**
```
the, a, an, and, or, but, in, on, at, to, for, of, with, by, from,
as, is, was, are, were, been, be, have, has, had, do, does, did,
will, would, could, should, may, might, must, shall, can, need,
create, implement, fix, add, update, modify, change, analyze,
review, check, verify, test, document, write
```

**Alternatives Considered:**
1. **No stopwords:** Simpler, but similarity scores less accurate
2. **NLTK stopwords:** More comprehensive, but adds dependency
3. **TF-IDF weighting:** More sophisticated, but complex to implement

**Reversibility:** HIGH - Stopwords set is easily modified in `STOPWORDS` constant.

---

## Decision 4: Integration Points - Pre-Planning & Pre-Execution

**Context:** Needed to decide where to integrate duplicate detection into Planner and Executor workflows.

**Selected:** Add to "Pre-Planning Research" (Planner) and "Pre-Execution Verification" (Executor)

**Rationale:**
- **Natural fit:** Both workflows already have verification steps
- **Early detection:** Catches duplicates before work begins (most efficient)
- **Non-blocking:** Can be skipped if detector fails (graceful degradation)
- **Clear ownership:** Planner checks before creating; Executor checks before claiming

**Alternatives Considered:**
1. **Post-commit check:** Check after task creation/execution - too late, waste has occurred
2. **Separate service:** Run as background daemon - overcomplicated, adds maintenance burden
3. **Manual process:** Rely on humans to check - proven ineffective (TASK-1769914000 duplicate)

**Reversibility:** MEDIUM - Integration requires prompt changes, but sections clearly marked, easy to remove.

---

## Decision 5: Manual Review vs Auto-Skip

**Context:** When duplicate detected, should system auto-skip or require manual review?

**Selected:** Manual review with logging (recommended skip if > 90% similarity)

**Rationale:**
- **False positive risk:** 80% threshold may catch non-duplicates; human review needed
- **Context matters:** Similar tasks may be valid (e.g., "Fix X in v1" and "Fix X in v2")
- **Learning opportunity:** Review helps tune threshold and improve algorithm
- **Accountability:** Human decision logged to events.yaml for audit

**Guidelines Provided:**
- **> 90% similarity:** Likely duplicate, recommended to skip
- **80-90% similarity:** Possible duplicate, review carefully
- **< 80% similarity:** Not duplicate, proceed

**Alternatives Considered:**
1. **Auto-skip all > 80%:** Risky, could skip valid work
2. **Auto-skip only > 95%:** More conservative, but still risk of false positives
3. **Always proceed with warning:** Defeats purpose of detection

**Reversibility:** HIGH - Workflow is documented recommendation, not enforced. Can change to auto-skip later if accuracy proven.

---

## Decision 6: Library Design - Standalone Python Module

**Context:** Needed to decide how to package duplicate detection functionality.

**Selected:** Standalone Python module with CLI interface

**Rationale:**
- **Reusability:** Can be imported by other tools (e.g., web dashboard, CLI tools)
- **Testability:** CLI interface makes it easy to test and validate
- **No dependencies:** Pure Python standard library, easy to deploy
- **Follows existing patterns:** Similar to other libraries in `2-engine/.autonomous/lib/`

**Key Features:**
- **DuplicateDetector class:** Main API for programmatic use
- **CLI interface:** `python3 duplicate_detector.py <task-file.md>`
- **Exit codes:** 0 = no duplicates, 1 = duplicates found (for shell scripting)
- **Configurable:** Threshold and search paths customizable

**Alternatives Considered:**
1. **Shell script:** Simpler, but string manipulation difficult, less maintainable
2. **Bash function:** Hard to test, limited to bash environment
3. **Integrated into prompts:** Duplicate code, hard to test, no reusability

**Reversibility:** LOW - Library is now integrated into Planner/Executor prompts, but interface is stable and unlikely to change.

---

## Decision 7: Documentation Depth - Comprehensive Guide

**Context:** Needed to decide how much documentation to provide for the duplicate detection system.

**Selected:** Comprehensive 350+ line guide with examples, troubleshooting, and tuning guidance

**Rationale:**
- **New concept:** Duplicate detection is new to users; needs clear explanation
- **Tuning required:** Threshold tuning is non-trivial; needs guidance
- **Troubleshooting:** Users will encounter edge cases; need solutions
- **Adoption:** Good documentation increases usage and effectiveness

**Sections Included:**
- Overview and algorithm explanation
- Usage examples for Planner and Executor
- Threshold tuning guidance
- Troubleshooting common issues
- Integration points
- Performance characteristics
- Testing procedures
- Changelog

**Alternatives Considered:**
1. **Minimal docstrings:** Easier to maintain, but users wouldn't know how to use it
2. **Inline comments only:** Insufficient for complex tuning decisions
3. **Separate documentation repo:** Overkill for single feature

**Reversibility:** HIGH - Documentation is separate from code; can be updated independently.

---

## Summary of Decisions

| Decision | Selection | Reversibility | Impact |
|----------|-----------|---------------|--------|
| Algorithm | Jaccard similarity | HIGH | Core functionality |
| Threshold | 80% | HIGH | Detection accuracy |
| Stopwords | Comprehensive list | HIGH | Detection accuracy |
| Integration | Pre-planning/Pre-execution | MEDIUM | Workflow fit |
| Review process | Manual with logging | HIGH | False positive handling |
| Packaging | Standalone Python module | LOW | Reusability |
| Documentation | Comprehensive guide | HIGH | User adoption |

**Overall Approach:** Conservative, reversible decisions with clear rationale. Prioritized simplicity and transparency over complexity. All decisions can be adjusted based on real-world usage data.
