# FEATURE-010: Knowledge Base & Learning Engine

**Status:** planned
**Priority:** high
**Type:** feature
**Estimated:** 180 minutes (~3 hours)

---

## User Value

**Who benefits:** RALF system (self-improvement autonomous agents)

**What problem does it solve:** Learnings are captured but not leveraged systematically. No active learning or knowledge sharing across runs. Past mistakes are often repeated. No mechanism to suggest relevant learnings for new tasks.

**What value does it creates:**
- Self-improving system that applies past learnings to new tasks
- Reduces repeated mistakes by >50% (target metric)
- Accelerates task completion by >15% through relevant learning application
- Creates institutional knowledge that persists across all RALF instances
- Enables pattern recognition to identify recurring issues and solutions

**Example:**
- Who: RALF Executor (task execution agent)
- Problem: Executors make the same mistakes across different runs (e.g., import errors, path issues)
- Value: System detects pattern, suggests relevant learning from TASK-XXX, prevents mistake recurrence

---

## Feature Scope

**MVP (Minimum Viable Product):**
- [x] Structured learning capture format (enhanced LEARNINGS.md with YAML frontmatter)
- [x] Learning extraction from THOUGHTS.md and DECISIONS.md
- [x] Pattern recognition (finds similar tasks based on keywords, context, errors)
- [x] Knowledge retrieval (searches learnings by type, task_id, effectiveness)
- [x] Learning application (injects relevant learnings into executor context)
- [x] Integration with existing memory/insights/ infrastructure
- [x] CLI interfaces for manual knowledge queries

**Future Enhancements (out of scope for this feature):**
- [ ] Machine learning for semantic similarity (Phase 2)
- [ ] Cross-project learning sharing (Phase 2)
- [ ] Learning expiry/deprecation (auto-archive outdated learnings) (Phase 2)
- [ ] Knowledge visualization dashboard (Phase 2)
- [ ] Effectiveness tracking with long-term metrics (Phase 2)

**Scope Boundaries:**
- **IN SCOPE:** Keyword-based pattern matching, structured learning capture, CLI interfaces, integration with executor prompt
- **OUT OF SCOPE:** ML-based semantic similarity, cross-project sharing, auto-deprecation, visualization UI, effectiveness tracking beyond basic logging

---

## Context & Background

**Why this feature matters:**
- **Institutional Knowledge:** RALF runs contain valuable learnings that are currently lost after execution
- **Continuous Improvement:** Self-improving systems require systematic learning capture and application
- **Error Reduction:** Pattern recognition can prevent recurring mistakes across runs
- **Acceleration:** Relevant learnings suggested upfront reduce trial-and-error

**Related Features:**
- **F-009 (Skill Marketplace):** Provides skill registry, learning engine can recommend skills based on past task patterns
- **F-008 (Real-time Dashboard):** Can visualize learning metrics and effectiveness in future phase
- **F-005 (Automated Documentation):** Learning extraction can populate documentation automatically

**Current State:**
- Learnings captured in THOUGHTS.md, DECISIONS.md (unstructured)
- No systematic learning extraction or indexing
- No pattern recognition or similarity detection
- No mechanism to suggest past learnings for new tasks
- No centralized learning index

**Desired State:**
- Learnings automatically extracted and structured (YAML frontmatter)
- Central learning index (learning-index.yaml) with metadata
- Pattern recognition identifies similar tasks (>70% precision target)
- Knowledge retrieval finds relevant learnings (>75% accuracy target)
- Executor prompt enhanced with relevant learnings
- CLI interfaces for manual queries and management

---

## Success Criteria

### Must-Have (Required for completion)
- [x] Learnings captured in structured format (enhanced LEARNINGS.md with YAML frontmatter)
- [x] Pattern recognition identifies recurring issues (e.g., "similar to TASK-XXX")
- [x] Knowledge retrieval finds relevant past learnings
- [x] Suggestions appear in task context (executor prompt enhancement)
- [x] Integration with existing memory/insights/ infrastructure

### Should-Have (Important but not blocking)
- [x] Automatic learning extraction from THOUGHTS.md and DECISIONS.md
- [x] Learning categorization (by type, severity, frequency)
- [x] Learning effectiveness tracking (basic logging - did applying a learning help?)
- [x] CLI interface for knowledge queries

### Nice-to-Have (If time permits)
- [ ] Machine learning for pattern recognition (deferred to Phase 2)
- [ ] Cross-project learning sharing (deferred to Phase 2)
- [ ] Learning expiry/deprecation (deferred to Phase 2)
- [ ] Knowledge visualization dashboard (deferred to Phase 2)

### Verification Method
- [x] Manual testing: Execute sample task, verify learning extraction and indexing
- [x] Integration testing: Query learnings for similar task, verify pattern matching
- [x] Documentation review: Review learning system guide, verify completeness
- [x] CLI testing: Test all CLI commands (query, extract, match, suggest)

---

## Technical Approach

### Implementation Plan

**Phase 1: Feature Specification & Foundation**
- [x] Create FEATURE-010 specification document
- [x] Design learning structure (YAML frontmatter schema)
- [x] Design learning index format (learning-index.yaml)
- [x] Create directory structure (memory/insights/learnings/)

**Phase 2: Core Libraries (4 libraries)**
- [ ] Create `learning_extractor.py` (extract, categorize, assess impact)
- [ ] Create `pattern_matcher.py` (find similar tasks, identify patterns)
- [ ] Create `knowledge_retriever.py` (search learnings, get patterns)
- [ ] Create `learning_applier.py` (inject learnings to context, track effectiveness)

**Phase 3: Infrastructure Enhancement**
- [ ] Create `memory/insights/learning-index.yaml` (structured index)
- [ ] Enhance `memory/insights/LEARNINGS.md` (structured format)
- [ ] Create `memory/insights/.docs/learning-system-guide.md` (system docs)
- [ ] Create `operations/.docs/knowledge-base-guide.md` (user guide)

**Phase 4: Integration & CLI**
- [ ] Create CLI interfaces (11 commands across 4 libraries)
- [ ] Integrate with executor prompt (learning injection)
- [ ] Test end-to-end workflow (extract → index → retrieve → apply)

**Phase 5: Testing & Verification**
- [ ] Unit tests for all 4 libraries
- [ ] Integration tests for pattern matching
- [ ] CLI testing for all commands
- [ ] End-to-end test with sample task

### Architecture & Design

**Key Components:**

1. **Learning Extractor** (`learning_extractor.py`)
   - Functions: `extract_learnings()`, `categorize_learning()`, `assess_impact()`
   - Input: THOUGHTS.md, DECISIONS.md
   - Output: Structured learning with YAML frontmatter
   - Schema: type, pattern, action_item, related_tasks, effectiveness

2. **Pattern Matcher** (`pattern_matcher.py`)
   - Functions: `find_similar_tasks()`, `identify_patterns()`, `detect_recurring_issues()`
   - Algorithm: Keyword overlap + context matching + error type analysis
   - Metrics: Jaccard similarity for keywords, TF-IDF for context
   - Output: List of similar tasks with confidence scores

3. **Knowledge Retriever** (`knowledge_retriever.py`)
   - Functions: `search_learnings()`, `get_relevant_patterns()`, `suggest_learnings()`
   - Index: task_id, feature_id, learning_type, timestamp, effectiveness
   - Search: Keyword search, type filtering, effectiveness ranking
   - Output: Ranked list of relevant learnings

4. **Learning Applier** (`learning_applier.py`)
   - Functions: `inject_learnings_to_context()`, `apply_learning()`, `track_effectiveness()`
   - Integration: Enhances executor prompt with relevant learnings
   - Format: Structured section in prompt with learning details
   - Tracking: Logs when learnings are suggested and applied

**Integration Points:**
- **memory/insights/**: Enhanced LEARNINGS.md, new learning-index.yaml
- **2-engine/.autonomous/prompts/**: Executor prompt enhanced with learnings
- **Executor workflow**: Learning extraction happens post-completion, retrieval happens pre-execution

**Data Flow:**
```
[Task Completion] → [THOUGHTS.md/DECISIONS.md] → [Learning Extractor]
                                                          ↓
                                                [Structured Learning]
                                                          ↓
                                                [Learning Index (YAML)]
                                                          ↓
[New Task] → [Pattern Matcher] → [Knowledge Retriever] → [Learning Applier]
                                                          ↓
                                                [Enhanced Executor Prompt]
```

---

## Dependencies

### Requires (Prerequisites)
- [x] F-009 (Skill Marketplace) - skill registry can recommend learning-based skills
- [x] Existing memory/insights/ infrastructure
- [x] Python 3.10+ (for libraries)
- [x] YAML parsing libraries (PyYAML)

### Blocks (Dependents)
- [F-011: Self-Optimization Engine]: Learning engine is foundation for self-optimization
- [F-012: Cross-Agent Communication]: Learning sharing enables cross-agent knowledge transfer

### External Dependencies
- [ ] PyYAML: YAML parsing for learning index
- [ ] NLTK/SpaCy: Text processing for pattern matching (optional, can use simple keyword matching for MVP)

---

## Rollout Plan

### Testing Strategy

**Unit Tests:**
- [Learning Extractor]: Test extraction from sample THOUGHTS.md/DECISIONS.md
- [Pattern Matcher]: Test similarity scoring with known similar/dissimilar tasks
- [Knowledge Retriever]: Test search with various queries and filters
- [Learning Applier]: Test prompt injection with various learning types

**Integration Tests:**
- [End-to-End]: Complete workflow (extract → index → retrieve → apply)
- [Similar Task Detection]: Create two similar tasks, verify pattern matching
- [CLI Integration]: Test all 11 CLI commands

**User Acceptance Tests:**
- [Manual Query]: User queries learnings via CLI, receives relevant results
- [Automatic Suggestion]: Executor receives learning suggestions for new task
- [Learning Extraction]: Run completes, learning automatically extracted and indexed

### Deployment Strategy
- **Deployment Method:** Rolling (deploy libraries, integrate with executor gradually)
- **Rollback Plan:** Disable learning injection in executor prompt if issues arise
- **Monitoring:** Track learning retrieval accuracy, pattern matching precision, effectiveness feedback

---

## Files to Modify

### New Files (Create)
- `plans/features/FEATURE-010-knowledge-base.md` (this file)
- `2-engine/.autonomous/lib/learning_extractor.py` (~400 lines)
- `2-engine/.autonomous/lib/pattern_matcher.py` (~350 lines)
- `2-engine/.autonomous/lib/knowledge_retriever.py` (~300 lines)
- `2-engine/.autonomous/lib/learning_applier.py` (~300 lines)
- `memory/insights/learning-index.yaml` (~100 lines initial)
- `memory/insights/.docs/learning-system-guide.md` (~400 lines)
- `operations/.docs/knowledge-base-guide.md` (~450 lines)

### Existing Files (Modify)
- `2-engine/.autonomous/prompts/ralf-executor-v2-legacy-based.md` (enhance with learning injection)
- `memory/insights/LEARNINGS.md` (enhance with structured format)

---

## Risk Assessment

### Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Pattern recognition produces false positives | Medium | Medium | Start with simple keyword matching, tune confidence threshold (70%), add context filtering |
| Learning index becomes large and slow | Medium | Low | Use efficient indexing (YAML for MVP, SQLite for Phase 2), lazy loading |
| Learning extraction misses important insights | High | Medium | Manual review of initial extractions, refine extraction patterns iteratively |
| Executor prompt becomes too long with learnings | Low | Low | Limit to top 3 most relevant learnings, summarize concisely |

### Operational Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Poor quality learnings clutter the index | Medium | Medium | Add effectiveness tracking, filter out low-effectiveness learnings |
| Learning suggestions slow down executor startup | Low | Low | Cache learning index, lazy load on first query |
| Learnings become outdated over time | Medium | Medium | Manual review process, add deprecation workflow in Phase 2 |

---

## Effort Estimation

**Estimated Breakdown:**
- Design: 20 minutes (learning structure, index format, algorithms)
- Implementation: 90 minutes (4 libraries × ~20-25 min each)
- Infrastructure: 20 minutes (learning-index.yaml, directory structure)
- Documentation: 30 minutes (system guide, user guide)
- CLI: 10 minutes (11 commands across libraries)
- Testing: 10 minutes (unit tests, integration tests)
- **Total:** 180 minutes (~3 hours)

**Complexity Factors:**
- [x] Integration complexity (medium) - must integrate with executor workflow and memory/insights/
- [x] Technical uncertainty (low-medium) - pattern matching is well-understood, extraction is straightforward
- [x] Dependencies (low) - minimal external dependencies, mostly Python standard library

---

## Dates

**Created:** 2026-02-01T14:35:00Z
**Started:** 2026-02-01T14:42:30Z
**Completed:** TBD

---

## Notes

**Strategic Value:**
This feature is foundational for RALF's self-improvement capabilities. By systematically capturing, indexing, and applying learnings, RALF becomes a continuously improving system that reduces mistakes and accelerates task completion. This is a key differentiator from traditional automation systems.

**Success Metrics:**
- Learning retrieval accuracy: >75% (relevant learnings found for query)
- Pattern recognition precision: >70% (correct patterns identified)
- Repeated mistakes reduced: >50% (compared to baseline)
- Task completion time improved: >15% (with relevant learnings applied)

**Open Questions:**
- **Q1:** Should we use keyword matching or semantic similarity for MVP?
  - **A1:** Keyword matching for MVP (faster, simpler, no external dependencies). Semantic similarity in Phase 2.
- **Q2:** How many learnings should we inject into executor prompt?
  - **A2:** Top 3 most relevant learnings (balances value vs prompt length).
- **Q3:** How do we measure learning effectiveness?
  - **A3:** Basic logging in Phase 1 (did executor apply the learning?). Long-term metrics in Phase 2.

**Learnings (to be filled after completion):**
- [What went well]
- [What could be improved]
- [Recommendations for future features]
