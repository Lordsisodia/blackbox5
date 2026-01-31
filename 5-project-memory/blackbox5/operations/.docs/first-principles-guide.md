# First Principles Review Guide

**Purpose:** Guide for conducting effective first principles reviews every 5 runs
**Version:** 1.0.0
**Last Updated:** 2026-02-01

---

## What is a First Principles Review?

A first principles review is a systematic analysis of the last 5 runs to:
1. **Identify patterns** in execution, success, and failure
2. **Extract learnings** that can drive improvements
3. **Make course corrections** based on evidence
4. **Set focus** for the next 5 runs

Unlike daily standups or weekly retrospectives, this review looks at the **system** not just the tasks.

---

## When to Conduct Reviews

### Automatic Trigger
- Every 5 runs (run numbers divisible by 5: 50, 55, 60, etc.)
- Triggered automatically by the Planner
- Takes precedence over normal task planning

### Manual Trigger
- When velocity drops significantly (>30% decrease)
- When error rates spike
- When major system changes occur
- When requested by human operator

---

## Review Process

### Step 1: Gather Data (10 minutes)

**Read the last 5 runs:**
```bash
# Read THOUGHTS.md, RESULTS.md, DECISIONS.md, LEARNINGS.md from:
# - runs/executor/run-[N-4]/
# - runs/executor/run-[N-3]/
# - runs/executor/run-[N-2]/
# - runs/executor/run-[N-1]/
# - runs/executor/run-[N]/
```

**Extract key data:**
- Task IDs and types
- Completion status
- Duration estimates vs actual
- Learnings captured
- Decisions made
- Assumptions validated/invalidated

### Step 2: Pattern Recognition (15 minutes)

**Look for:**

1. **Success Patterns**
   - What consistently leads to successful outcomes?
   - Which skills are most effective?
   - What pre-execution research correlates with success?

2. **Failure Patterns**
   - What types of tasks fail most often?
   - What assumptions are frequently wrong?
   - Where do we get blocked?

3. **Velocity Patterns**
   - Are tasks taking longer or shorter over time?
   - Is context efficiency improving?
   - Are we using appropriate context levels?

4. **Quality Patterns**
   - Are we validating assumptions before acting?
   - Are we reading code before changing it?
   - Are we following the "one task at a time" rule?

### Step 3: Course Correction (10 minutes)

**For each significant pattern:**

1. **Decide:** Do we need to change something?
2. **Define:** What exactly will change?
3. **Document:** Create improvement task or update guidance
4. **Validate:** Set metrics to verify the change helps

**Decision Framework:**
- If pattern appears in 3+ runs → Make it standard practice
- If friction appears in 2+ runs → Create improvement task
- If assumption wrong in 2+ runs → Update guidance
- If skill unused when expected → Tune trigger or remove skill

### Step 4: Set Next Focus (5 minutes)

**Define 3 priorities for next 5 runs:**
1. **Process improvement** - What will we do differently?
2. **Skill development** - What capability needs enhancement?
3. **Infrastructure** - What tools/templates need updating?

---

## Review Template

Use `.templates/reviews/first-principles-review.md.template`

**Required Sections:**
1. Executive Summary - The "so what"
2. Pattern Analysis - Evidence-based findings
3. Course Correction - Specific decisions
4. Next Focus - Actionable priorities
5. Appendix - Supporting data

---

## Example Patterns

### Pattern: Pre-Execution Research Value
**Finding:** Tasks with pre-execution file reads have 90% success rate vs 60% without.
**Decision:** Make pre-execution research mandatory for all implement tasks.
**Validation:** Track success rate for next 5 runs.

### Pattern: Context Level Appropriateness
**Finding:** Context level 3 tasks frequently exceed token limits.
**Decision:** Split context level 3 tasks or increase to level 4 with sub-agents.
**Validation:** Monitor context overflow exits.

### Pattern: Skill Effectiveness
**Finding:** `bmad-architect` skill used 5 times, only 2 successful outcomes.
**Decision:** Review skill triggers and examples. May need refinement.
**Validation:** Track skill success rate.

---

## Integration with Improvement Pipeline

**Reviews feed the improvement pipeline:**

1. **Review identifies pattern** → Creates improvement task
2. **Improvement task prioritized** → Added to active queue
3. **Improvement implemented** → Validation metrics tracked
4. **Next review validates** → Did the improvement work?

**This closes the loop:**
```
Learning → Review → Improvement → Validation → Learning
```

---

## Planner Responsibilities

**At the start of each planning iteration:**

1. Check `STATE.yaml` → `improvement_metrics.review_schedule.next_review_run`
2. If current loop >= next_review_run:
   - Enter REVIEW MODE instead of normal planning
   - Read last 5 runs from `runs/archived/` or `runs/executor/`
   - Generate first principles review document
   - Save to `knowledge/analysis/first-principles-review-[RUN].md`
   - Update `STATE.yaml` with review completion
   - Update `next_review_run` to current + 5
3. Resume normal planning

**Review Mode Output:**
- Review document created
- Improvement tasks generated (if any)
- STATE.yaml updated
- Events logged to `communications/events.yaml`

---

## Success Metrics

**Review Quality:**
- All 5 runs analyzed
- At least 3 patterns identified
- At least 1 course correction decision
- Review completed within 40 minutes

**System Impact:**
- First principles reviews: 1 per 5 runs (target: 100%)
- Improvements from reviews: At least 1 per review
- Review-to-improvement conversion: >50%

---

## Common Pitfalls

### 1. Superficial Analysis
**Problem:** Just summarizing what happened without identifying patterns.
**Solution:** Force comparison across runs. Look for correlations.

### 2. No Course Correction
**Problem:** Identifying issues but not deciding what to do.
**Solution:** Every significant pattern must result in a decision.

### 3. Vague Improvements
**Problem:** "Improve X" without specifics.
**Solution:** Improvements must have acceptance criteria.

### 4. Ignoring Success
**Problem:** Only focusing on what went wrong.
**Solution:** Document what worked so we can repeat it.

### 5. Review Drift
**Problem:** Reviews get longer and less focused over time.
**Solution:** Timebox each section. 40 minutes max.

---

## Tools and Resources

**Templates:**
- `.templates/reviews/first-principles-review.md.template`

**Reference:**
- `knowledge/analysis/first-principles-framework.md` - Detailed framework
- `STATE.yaml` - Review schedule and metrics
- `goals.yaml` - Improvement goals

**Related Processes:**
- Improvement pipeline (`operations/improvement-pipeline.yaml`)
- Learning extraction (TASK-1769902000)

---

## Quick Reference Card

```
EVERY 5 RUNS:
1. Read last 5 runs (THOUGHTS, RESULTS, DECISIONS, LEARNINGS)
2. Identify 3+ patterns
3. Make 2+ course correction decisions
4. Set 3 priorities for next 5 runs
5. Create review document
6. Update STATE.yaml
7. Generate improvement tasks (if needed)

TIME: 40 minutes max
OUTPUT: knowledge/analysis/first-principles-review-[RUN].md
```

---

**Questions?** Check the framework document or ask in chat-log.yaml.
