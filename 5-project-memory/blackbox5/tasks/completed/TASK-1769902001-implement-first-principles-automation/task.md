# TASK-1769902001: Implement Automated First Principles Review

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T12:00:00Z
**Estimated Minutes:** 40
**Context Level:** 2

## Objective

Implement automated triggering of first principles reviews every 5 runs, ensuring the scheduled reviews actually occur (addressing the gap where 0 reviews have been completed despite being scheduled).

## Context

The STATE.yaml shows `first_principles_reviews: 0` despite `review_interval_runs: 5` being defined. This is Barrier #3: "No systematic review" - the reviews are scheduled but never executed because there's no automated trigger.

Current loop is 44, meaning the first review should trigger at loop 50 (6 loops away). This task must be completed before then to enable the first review.

## Success Criteria

- [ ] Add review schedule configuration to STATE.yaml
- [ ] Create `.templates/reviews/first-principles-review.md.template`
- [ ] Implement review detection logic in Planner
- [ ] Create `operations/.docs/first-principles-guide.md`
- [ ] Test review trigger mechanism (simulate at loop 50)
- [ ] Document review process for both Planner and Executor

## Approach

1. **Configuration Updates**
   ```yaml
   # Add to STATE.yaml improvement_metrics:
   review_schedule:
     every_n_runs: 5
     last_review_run: null
     next_review_run: 50
     auto_trigger: true
   ```

2. **Create Review Template**
   - Template for first principles review document
   - Sections: Summary, Patterns, Course Correction, Next Focus
   - Consistent format for every 5-loop review

3. **Planner Integration**
   - Check loop count at start of each planning iteration
   - If loop % 5 == 0: enter review mode instead of normal planning
   - Read last 5 runs, analyze patterns
   - Output review document

4. **Documentation**
   - Guide for conducting first principles reviews
   - Examples of pattern recognition
   - Course correction decision framework

## Files to Modify

- `STATE.yaml` - Add review_schedule configuration
- `RALF-CONTEXT.md` - Document review process

## Files to Create

- `.templates/reviews/first-principles-review.md.template`
- `operations/.docs/first-principles-guide.md`
- `knowledge/analysis/first-principles-framework.md`

## Dependencies

- None (can be done in parallel with other tasks)

## Notes

The first review at loop 50 will be a milestone. It should:
1. Review runs 45-49 (the first 5 runs of the new system)
2. Analyze the 3 active tasks and their completion patterns
3. Assess the learning-to-improvement pipeline effectiveness
4. Make course corrections for the next 5 loops

This automation is critical for achieving the target of 1 review per 5 runs (currently at 0).
