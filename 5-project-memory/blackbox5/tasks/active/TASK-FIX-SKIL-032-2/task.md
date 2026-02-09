# TASK-FIX-SKIL-032-2: Create A/B Comparison Framework for Skill vs No-Skill Tasks

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 60 minutes
**Created:** 2026-02-09T12:00:00Z
**Parent:** TASK-SKIL-032

---

## Objective

Create a framework to compare task completion times between tasks using skills versus tasks not using skills, enabling baseline comparison for ROI calculation.

---

## Success Criteria

- [ ] Baseline time estimation mechanism implemented
- [ ] Tasks can be tagged as "with-skill" or "without-skill"
- [ ] Paired comparison data structure defined
- [ ] Comparison report generator created
- [ ] At least 3 paired comparisons (same task type, with/without skill) recorded
- [ ] Time savings calculation formula implemented

---

## Context

**Root Cause:** SKIL-032 identified that ROI calculation requires comparing task time WITH skills vs WITHOUT skills. Currently no baseline comparison data exists.

**Current Gap:**
- No way to mark tasks as "baseline" (no skill) vs "skill-enhanced"
- No mechanism to pair similar tasks for comparison
- No formula to calculate time savings

**Key Insight:** Since true A/B testing is impossible (same task can't be done both ways), we need:
1. **Historical baseline** - Track tasks completed without skills
2. **Estimated baseline** - Executor estimates time without skill
3. **Task type grouping** - Compare similar tasks (e.g., "git-commit" tasks)

**Key Files:**
- `operations/skill-metrics.yaml` - Contains baseline_minutes estimates per skill
- `operations/skill-usage.yaml` - Contains usage patterns
- Task files in `tasks/active/` and `tasks/completed/`

---

## Approach

1. **Add baseline estimation to task workflow**
   - Prompt executor for estimated baseline time ("How long would this take without a skill?")
   - Store estimate in task outcome

2. **Create task tagging system**
   - Tag tasks as `skill-enhanced` or `baseline`
   - Record task type/category for grouping

3. **Implement comparison data structure**
   ```yaml
   comparison_pairs:
     - task_type: "git-commit"
       baseline_tasks:
         - task_id: TASK-001
           duration_minutes: 30
       skill_tasks:
         - task_id: TASK-002
           skill_used: "git-commit"
           duration_minutes: 15
       time_saved_minutes: 15
       time_saved_percent: 50
   ```

4. **Create comparison report generator**
   - Script to analyze task_outcomes
   - Group by task type
   - Calculate average time savings per skill

5. **Test with real tasks**
   - Identify 3 common task types
   - Find/create baseline and skill-enhanced examples
   - Generate comparison report

---

## Files to Modify

| File | Changes |
|------|---------|
| `operations/skill-metrics.yaml` | Add comparison_pairs section |
| `bin/bb5-task` | Add baseline estimation prompt |

## Files to Create

| File | Purpose |
|------|---------|
| `bin/skill-comparison-report.py` | Generate A/B comparison reports |
| `.docs/skill-comparison-framework.md` | Documentation for framework |

---

## Rollback Strategy

If changes cause issues:
1. Remove comparison_pairs from skill-metrics.yaml
2. Disable baseline estimation prompts
3. Revert to simple task tracking

---

## Notes

- Baseline estimation relies on executor judgment - document this limitation
- Focus on common task types first (git-commit, documentation, research)
- Consider automating task type detection from task content
