# Decisions - TASK-1769899002

---

## Decision 1: 6-State Pipeline Structure

**Context:** Need to define clear flow from learning capture to improvement validation

**Selected:** 6 states: captured → reviewed → prioritized → tasked → implemented → validated

**Alternatives Considered:**
- 3-state (capture → process → complete) - Too simple, loses visibility
- 4-state (capture → review → implement → validate) - Missing prioritization step
- 8-state (with additional approval gates) - Too bureaucratic

**Rationale:**
- 6 states provide clear handoffs without being burdensome
- Each state has clear entry/exit criteria
- Clear ownership at each stage (executor vs planner)
- Maps to actual workflow (capture, review, prioritize, task, implement, validate)

**Reversibility:** MEDIUM - Can collapse states later if too heavy

---

## Decision 2: Mandatory action_item Field

**Context:** Learnings often lack concrete next steps

**Selected:** action_item is mandatory in learning format

**Alternatives Considered:**
- Optional action_item - Doesn't solve the problem
- Separate action_items file - Fragmented, hard to track
- Auto-generate from observation - May miss nuance

**Rationale:**
- Forces explicit thinking about "what should we do about this"
- Makes learning→task conversion explicit
- Template provides structure so it's not burdensome
- Can use "none - informational only" for true observations

**Reversibility:** HIGH - Can make optional if too restrictive

---

## Decision 3: Improvement Queue Reserve Slots

**Context:** Improvements compete with feature work for executor attention

**Selected:** Reserve 2 slots in improvement queue, pull when main queue < 3

**Alternatives Considered:**
- Fixed 50/50 split - Too rigid, may starve urgent features
- Priority only - Improvements always lose to new features
- Time-based (1 day/week) - Hard to schedule in autonomous system

**Rationale:**
- Ensures improvements don't starve
- Flexible - features can use slots if queue full
- Simple rule - easy to implement and understand
- Balanced - doesn't block critical feature work

**Reversibility:** HIGH - Can adjust slot count or threshold

---

## Decision 4: First Principles Review Every 5 Runs

**Context:** Need systematic review without overwhelming execution

**Selected:** Automated review every 5 runs (runs divisible by 5)

**Alternatives Considered:**
- Every run - Too frequent, disrupts flow
- Every 10 runs - May miss patterns
- Manual trigger - Never happens (evidence: 0 reviews completed)
- Time-based (weekly) - Doesn't align with run cadence

**Rationale:**
- 5 runs is ~1 week at current velocity
- Enough data to see patterns (15-20 learnings)
- Not so frequent it disrupts execution
- Auto-trigger ensures it actually happens

**Reversibility:** HIGH - Can adjust frequency in STATE.yaml

---

## Decision 5: 4 Validation Metrics

**Context:** Need to measure if improvements actually work

**Selected:** Track task_completion_time, error_rate, context_efficiency, learning_quality

**Alternatives Considered:**
- Single metric (task completion time) - May miss important dimensions
- 6+ metrics - Too complex to track
- Subjective assessment - Hard to compare

**Rationale:**
- 4 metrics cover speed, quality, efficiency, and process
- All trackable with existing data
- Specific thresholds (10-25% improvement)
- Balanced view of improvement effectiveness

**Reversibility:** MEDIUM - Can add/remove metrics as learn

---

## Decision 6: YAML + Markdown Hybrid Format

**Context:** Need structured data but readable format

**Selected:** YAML frontmatter in markdown with free-form details section

**Alternatives Considered:**
- Pure YAML - Hard to read narrative
- Pure Markdown - Hard to parse programmatically
- JSON - Too verbose, harder to write
- Database - Overkill for this scale

**Rationale:**
- YAML provides structure for automation
- Markdown provides readability for humans
- Template makes YAML easy to write
- Existing pattern in project (STATE.yaml, etc.)

**Reversibility:** HIGH - Can migrate to different format if needed

---

## Decision 7: Separate improvements/ Directory

**Context:** Where to store improvement tasks

**Selected:** `.autonomous/tasks/improvements/` subdirectory

**Alternatives Considered:**
- Mix with regular tasks in active/ - Hard to distinguish
- Separate queue.yaml entry - More complex
- Tag regular tasks - Easy to lose track

**Rationale:**
- Clear separation from feature tasks
- Easy to count and manage
- Can apply different rules
- Matches mental model (improvements are different)

**Reversibility:** MEDIUM - Can move files later if needed

---

## Summary Table

| Decision | Reversibility | Risk Level | Confidence |
|----------|---------------|------------|------------|
| 6-state pipeline | Medium | Low | 90% |
| Mandatory action_item | High | Low | 95% |
| Queue reserve slots | High | Low | 85% |
| Review every 5 runs | High | Low | 90% |
| 4 validation metrics | Medium | Medium | 80% |
| YAML+Markdown format | High | Low | 95% |
| improvements/ directory | Medium | Low | 90% |
