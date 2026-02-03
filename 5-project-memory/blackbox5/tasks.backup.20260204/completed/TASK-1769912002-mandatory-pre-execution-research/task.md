# TASK-1769912002: Make Pre-Execution Research Mandatory

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T02:14:00Z
**Improvement:** IMP-1769903002

## Objective

Make pre-execution research mandatory in the Executor workflow to prevent duplicate work, validate assumptions, and improve task quality. Currently optional but consistently proves valuable based on 5+ learning references.

## Context

**Problem:** Pre-execution research is optional but consistently prevents issues:
- L-1769813746-003: "Research before execution caught potential duplicate"
- L-1769800330-003: "Pre-execution validation saved 20 minutes"
- L-1769808838-001: "Assumptions validated during research phase"
- L-1769807450-002: "Duplicate prevention through research"
- L-run-integration-test-L3: "Research discovered existing implementation"

**Impact:**
- **Without research:** Risk of duplicate work, wasted effort, invalid assumptions
- **With research:** Validates assumptions, checks for existing work, improves quality
- **Current state:** Optional → inconsistent application
- **Desired state:** Mandatory → always applied

**Success Criteria:**
- Pre-execution research added to Executor workflow as REQUIRED step
- Research checklist created (5-7 items)
- Executor cannot skip research step
- Research findings logged to THOUGHTS.md
- Tested with 3+ tasks to verify compliance
- IMP-1769903002 marked complete

## Approach

### Phase 1: Design Research Checklist (10 min)
Create mandatory pre-execution research checklist:

1. **Duplicate Check:**
   - Search completed/ for similar tasks
   - Search active/ for in-progress similar tasks
   - Use duplicate_detector.py if available

2. **File Validation:**
   - Verify target files exist
   - Check file permissions
   - Validate file paths

3. **Assumption Validation:**
   - List all assumptions
   - Validate each with evidence
   - Document confidence level

4. **Dependency Check:**
   - Check if dependencies are met
   - Verify dependent tasks completed
   - Check for blocking issues

5. **Context Gathering:**
   - Read relevant documentation
   - Check for existing patterns
   - Review similar completed tasks

### Phase 2: Integrate into Executor Workflow (10 min)
Modify executor prompt (v2-legacy-based.md):

1. Add "Pre-Execution Research (REQUIRED)" section
2. Place AFTER "Claim Task" and BEFORE "Execute Task"
3. Add enforcement: "Research is MANDATORY, cannot be skipped"
4. Add research logging requirement to THOUGHTS.md

### Phase 3: Create Research Template (10 min)
Create template for structured research output:

```markdown
## Pre-Execution Research

### Duplicate Check
- Searched completed/: [results]
- Searched active/: [results]
- Duplicate detector score: [if applicable]
- Conclusion: [no duplicate / potential duplicate found]

### File Validation
- Target files exist: [yes/no]
- File permissions: [ok/error]
- Invalid paths: [list if any]

### Assumption Validation
1. [Assumption 1]
   - Evidence: [what validates this]
   - Confidence: [high/medium/low]

2. [Assumption 2]
   - Evidence: [what validates this]
   - Confidence: [high/medium/low]

### Dependencies
- Dependencies met: [yes/no]
- Blocked by: [list if any]
- Ready to proceed: [yes/no]

### Context Gathered
- Documentation reviewed: [list]
- Patterns found: [list]
- Similar tasks: [list]

### Research Conclusion
- Ready to execute: [yes/no]
- Risks identified: [list]
- Recommendations: [list]
```

### Phase 4: Test and Validate (5 min)
1. Apply to next 3 executor tasks
2. Verify research step is not skipped
3. Check quality of research output
4. Measure impact on task quality

## Files to Modify

- `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
  - Section: Add "Pre-Execution Research (REQUIRED)"
  - Location: After "Claim Task", before "Execute Task"
  - Content: Research checklist, template, enforcement

- `2-engine/.autonomous/templates/research-template.md` (create)
  - Research checklist template
  - Structured output format
  - Examples for each section

- `operations/.docs/pre-execution-research-guide.md` (create)
  - Why research is mandatory
  - How to conduct research
  - Research quality criteria
  - Common pitfalls

## Notes

**Enforcement Strategy:**
- Make research a GATE in executor workflow
- Add explicit check: "If research not complete, DO NOT proceed"
- Log research completion in metadata.yaml
- Include research in success criteria

**Quality Standards:**
- Research must be documented (not just "done")
- Each checklist item must be addressed
- Assumptions must have evidence
- Conclusion must be explicit (yes/no on proceed)

**Expected Impact:**
- Reduce duplicate task execution (already addressed by IMP-1769903003)
- Improve task quality (better understanding before execution)
- Reduce rework (validate assumptions upfront)
- Increase success rate (catch issues early)

**Dependencies:**
- Related to IMP-1769903003 (duplicate detection) - use that library
- Connected to IMP-1769903001 (roadmap sync) - both improve state management
- Supports all future tasks (quality improvement)

**Estimated Time:** 35 minutes
**Context Level:** 2 (moderate complexity, process change)
**Risk:** Low (process improvement, no core functionality changes)

**Warnings:**
- Monitor for executor resistance (skipping research step)
- If research takes too long (> 10 min), adjust checklist
- If quality is poor, add more specific guidance
- Track impact on task duration (should not increase significantly)

**Success Metrics:**
- Research completion rate: 100% (mandatory)
- Duplicate tasks: 0 (should eliminate remaining duplicates)
- Rework due to invalid assumptions: < 5% (from ~15%)
- Task success rate: > 95% (from 91.7%)
