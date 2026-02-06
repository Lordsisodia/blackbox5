# PLAN.md: Empty Template Files in Runs Not Being Populated

**Task:** TASK-PROC-003 - Empty Template Files in Runs Not Being Populated  
**Status:** Planning  
**Created:** 2026-02-06  
**Estimated Effort:** 60 minutes  
**Importance:** 95/100 (Critical)

---

## 1. First Principles Analysis

### Why Are Empty Template Files a Critical Problem?

1. **Knowledge Loss**: Run folders capture institutional knowledge. Empty files mean insights are permanently lost.
2. **Continuous Improvement Breakdown**: The Agent Improvement Loop depends on analyzing run history.
3. **Accountability Gap**: No way to verify what was accomplished.
4. **Pattern Detection Failure**: First principles reviews require actual content.

### What Value Is Lost?

| File | Purpose | Value Lost |
|------|---------|------------|
| THOUGHTS.md | Execution reasoning | Decision context |
| LEARNINGS.md | Insights | Improvement opportunities |
| DECISIONS.md | Decision records | Rationale for choices |
| RESULTS.md | Outcomes | Success/failure metrics |

### How Can We Enforce Documentation?

1. **Validation at Exit**: Hook into session-end to verify documentation
2. **Minimum Content Thresholds**: Define "filled" vs "unfilled"
3. **Configurable Enforcement**: Warn vs block modes
4. **Clear Error Messages**: Guide agents on what to complete

---

## 2. Current State Assessment

### Run Folder Creation Process

Templates exist at:
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.templates/runs/`

### Evidence of Problem

From INTELLIGENT-SCOUT-RESULTS.md:
> "Run run-1770133139 has all template files with 'RALF_TEMPLATE: UNFILLED' markers"

### Existing Hook Infrastructure

1. **Session End Hook**: `/Users/shaansisodia/.claude/hooks/session-end.sh`
2. **Validation Pattern**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/validate-skill-usage.py`

---

## 3. Proposed Solution

### Validation Hook Structure

Create `bin/validate-run-documentation.py`:
- Content detection
- Minimum threshold validation
- Exit code strategy
- Integration with session-end hook

### Minimum Content Requirements

**THOUGHTS.md:**
- Minimum 500 characters
- Must contain "## " sections
- No template placeholders

**LEARNINGS.md:**
- Minimum 300 characters
- At least one "Learning" section

**DECISIONS.md:**
- Minimum 200 characters
- At least one decision entry

**RESULTS.md:**
- Minimum 400 characters
- Must contain "## Summary" section

### Enforcement Configuration

```yaml
validation:
  mode: "warn"  # warn | block | strict
  thresholds:
    thoughts_min_chars: 500
    learnings_min_chars: 300
```

---

## 4. Implementation Plan

### Phase 1: Define Minimum Content Requirements (15 min)

1. Create `operations/run-validation.yaml`
2. Define thresholds for each file type
3. Document requirements

### Phase 2: Create Validation Script (20 min)

1. Create `bin/validate-run-documentation.py`
2. Parse configuration
3. Check content length
4. Detect template placeholders
5. Generate colorized output

### Phase 3: Integrate with Session-End Hook (15 min)

1. Modify `session-end.sh`
2. Call validation script
3. Check exit code
4. Block completion if needed

### Phase 4: Add Configuration Options (5 min)

1. Environment variable overrides
2. Mode switching

### Phase 5: Test Enforcement (3 min)

1. Test with sample run
2. Verify all modes work
3. Test edge cases

### Phase 6: Document the Process (2 min)

1. Update CLAUDE.md
2. Add to run-lifecycle.md

---

## 5. Success Criteria

- [ ] Validation hook created
- [ ] Configuration file created
- [ ] Empty runs trigger warnings/errors
- [ ] Session-end hook integrated
- [ ] Documentation updated

---

## 6. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Define Requirements | 15 min |
| Create Script | 20 min |
| Integrate Hook | 15 min |
| Configuration | 5 min |
| Test | 3 min |
| Document | 2 min |
| **Total** | **60 min** |

---

*Plan created based on process analysis*
