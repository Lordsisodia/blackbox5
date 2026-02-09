# TASK-FIX-SKIL-018-3: Create Pre-Execution Hook for Skill Enforcement

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 60 minutes
**Created:** 2026-02-09
**Parent Task:** TASK-SKIL-018

---

## Objective

Create a pre-execution hook that enforces skill invocation for clear triggers (>=85% confidence), preventing agents from subjectively overriding the threshold.

---

## Success Criteria

- [ ] Create `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh`
- [ ] Hook runs before any task execution
- [ ] Hook calls detect-skill.py to analyze task
- [ ] For clear triggers (>=85%): Block execution until skill is invoked
- [ ] For discretionary (70-84%): Warn but allow override with justification
- [ ] For no match (<70%): Continue normally
- [ ] Hook logs enforcement actions to skill-metrics.yaml
- [ ] Add `BB5_SKIP_SKILL_ENFORCEMENT` env var for emergency bypass
- [ ] Update CLAUDE.md with hook documentation

---

## Context

**Root Cause Identified:**
No enforcement mechanism exists - agents override threshold subjectively even when triggers are clear.

**Current Behavior:**
1. Agent reads task
2. Agent checks skill-selection.yaml
3. Agent calculates 90% confidence
4. Agent thinks "I can handle this" and overrides
5. Skill not invoked, quality suffers

**Desired Behavior:**
1. Agent reads task
2. Hook runs detect-skill.py
3. Hook detects 90% confidence (clear trigger)
4. Hook blocks: "MUST invoke skill: git-commit"
5. Agent invokes skill
6. Execution proceeds

---

## Files to Create/Modify

### New Files

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh`
   - Main enforcement hook (~100 lines)
   - Calls detect-skill.py
   - Implements blocking logic
   - Logs enforcement actions

2. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/README.md`
   - Documentation for the hook
   - Bypass instructions
   - Troubleshooting

### Modified Files

3. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/CLAUDE.md`
   - Add pre-execution hook section
   - Document enforcement behavior
   - Add bypass env var documentation

4. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml`
   - Add enforcement_log section
   - Track blocked executions, overrides, justifications

---

## Approach

1. Design hook interface and blocking logic
2. Implement detect-skill.py integration
3. Implement enforcement logic for each trigger type
4. Add logging to skill-metrics.yaml
5. Create bypass mechanism
6. Write documentation
7. Test with sample tasks

---

## Hook Behavior Specification

**Trigger: Clear (>=85% confidence)**
```
[SKILL ENFORCEMENT] Clear trigger detected for task: "Implement git commit"
[SKILL ENFORCEMENT] Required skill: git-commit (confidence: 95%)
[SKILL ENFORCEMENT] Action: MUST invoke before proceeding

To proceed:
1. Invoke skill: skill: "git-commit"
2. Or set BB5_SKIP_SKILL_ENFORCEMENT=1 (not recommended)

Execution blocked until skill is invoked.
```

**Trigger: Discretionary (70-84% confidence)**
```
[SKILL ENFORCEMENT] Discretionary trigger detected
[SKILL ENFORCEMENT] Recommended skill: bmad-dev (confidence: 75%)
[SKILL ENFORCEMENT] Action: SHOULD invoke (override allowed with justification)

Override? Add to THOUGHTS.md:
"## Skill Override Justification\nReason for not invoking: [explain]"
```

**Trigger: None (<70% confidence)**
```
[SKILL ENFORCEMENT] No skill match detected (confidence: 45%)
[SKILL ENFORCEMENT] Action: Continue normally
```

---

## Rollback Strategy

If hook causes issues:
1. Set `BB5_SKIP_SKILL_ENFORCEMENT=1` to bypass
2. Disable hook in `.claude/hooks/pre-execution/`
3. Document issues
4. Fix and re-enable

---

## Notes

**Enforcement Log Format (skill-metrics.yaml):**
```yaml
enforcement_log:
  - timestamp: "2026-02-09T12:00:00Z"
    task_id: "TASK-xxx"
    trigger_type: "clear"
    skill_recommended: "git-commit"
    confidence: 95
    action_taken: "blocked_pending_invocation"
    overridden: false

  - timestamp: "2026-02-09T12:05:00Z"
    task_id: "TASK-yyy"
    trigger_type: "discretionary"
    skill_recommended: "bmad-dev"
    confidence: 75
    action_taken: "override_with_justification"
    overridden: true
    justification: "Simple one-line fix, skill not needed"
```

**Emergency Bypass:**
```bash
# Skip enforcement for this session
export BB5_SKIP_SKILL_ENFORCEMENT=1

# Or for single command
BB5_SKIP_SKILL_ENFORCEMENT=1 bb5 task:run TASK-xxx
```

**Integration with RALF:**
- Hook runs during Phase 1.5 (Skill Checking)
- Blocks progression to Phase 2 (Execution) until resolved
- Logs in run folder THOUGHTS.md
