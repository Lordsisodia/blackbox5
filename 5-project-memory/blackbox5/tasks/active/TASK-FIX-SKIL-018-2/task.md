# TASK-FIX-SKIL-018-2: Create bin/detect-skill.py Auto-Detection Script

**Status:** pending
**Priority:** HIGH
**Category:** skills
**Estimated Effort:** 45 minutes
**Created:** 2026-02-09
**Parent Task:** TASK-SKIL-018

---

## Objective

Create an automated skill detection script that analyzes task input and returns recommended skills with confidence scores, removing subjective agent override.

---

## Success Criteria

- [ ] Create `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/detect-skill.py`
- [ ] Script accepts task description as input (stdin or argument)
- [ ] Script reads skill-selection.yaml for domain mappings
- [ ] Script calculates confidence using formula from skill-selection.yaml
- [ ] Script outputs JSON with: recommended_skills, confidence, trigger_type
- [ ] Script returns exit code 0 if clear trigger (>=85%), 1 if discretionary, 2 if none
- [ ] Add unit tests for script
- [ ] Update bb5 CLI to integrate detect-skill.py

---

## Context

**Root Cause Identified:**
No auto-detection script exists - agents manually check skills and subjectively override thresholds.

**Current Process:**
1. Agent reads skill-selection.yaml
2. Agent manually calculates confidence
3. Agent subjectively decides to invoke or not

**Desired Process:**
1. Script analyzes task automatically
2. Script returns objective confidence score
3. Script classification determines action (MUST/SHOULD/MAY)
4. Agent follows script output without override

---

## Files to Create/Modify

### New Files

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/detect-skill.py`
   - Main detection script (~150 lines)
   - Argument parsing
   - YAML reading
   - Confidence calculation
   - JSON output

2. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/test_detect_skill.py`
   - Unit tests (~100 lines)
   - Test cases for each trigger type
   - Mock skill-selection.yaml

### Modified Files

3. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5`
   - Add `bb5 skill:detect [task-description]` command
   - Integrate into task creation flow

---

## Approach

1. Design script interface and output format
2. Implement YAML loading and parsing
3. Implement confidence calculation algorithm
4. Implement keyword matching logic
5. Add JSON output formatting
6. Create unit tests
7. Integrate with bb5 CLI

---

## Script Specification

**Usage:**
```bash
# Direct input
detect-skill.py "Implement git commit workflow"

# From stdin
echo "Create PRD for user authentication" | detect-skill.py --stdin

# With context file
detect-skill.py --task-file /path/to/task.md
```

**Output Format:**
```json
{
  "task_summary": "Implement git commit workflow",
  "recommended_skills": [
    {
      "name": "git-commit",
      "confidence": 95,
      "trigger_type": "clear",
      "matched_keywords": ["implement", "git", "commit"]
    }
  ],
  "action_required": "MUST invoke",
  "all_matches": [
    {"name": "git-commit", "confidence": 95},
    {"name": "bmad-dev", "confidence": 75}
  ]
}
```

**Exit Codes:**
- 0: Clear trigger (>=85% confidence) - MUST invoke
- 1: Discretionary (70-84% confidence) - SHOULD invoke
- 2: No match (<70% confidence) - MAY check
- 3: Error

---

## Rollback Strategy

If script has issues:
1. Disable in bb5 CLI (remove command)
2. Document issues in task notes
3. Fix and re-release

---

## Notes

**Confidence Calculation Formula (from skill-selection.yaml):**
```
confidence = (
  keyword_match_score * 0.4 +
  domain_match_score * 0.3 +
  task_type_match_score * 0.2 +
  context_match_score * 0.1
)
```

**Keyword Matching:**
- Exact match: +30 points
- Partial match: +15 points
- Related synonym: +10 points

**Trigger Type Determination:**
- >= 85: "clear" - MUST invoke
- 70-84: "discretionary" - SHOULD invoke
- < 70: "none" - MAY check
