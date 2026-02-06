# PLAN.md: Task Template Files Created But Never Used

**Task ID:** TASK-PROC-024  
**Status:** Planning  
**Priority:** MEDIUM  
**Created:** 2026-02-06  
**Estimated Effort:** 60 minutes  
**Importance Score:** 70/100

---

## 1. First Principles Analysis

### Why Are Template Files Not Being Filled?

1. **No Enforcement**: Templates created via `touch` with no validation
2. **No Guidance**: No instructions on what to document
3. **No Incentives**: No visible benefit to filling templates
4. **Time Pressure**: Quick task completion prioritized over documentation

### What Value Is Lost?

- **Knowledge**: Solutions and insights not captured
- **Patterns**: Cannot identify recurring issues
- **Improvement**: No data for process optimization
- **Onboarding**: New team members lack context

### How Can We Validate Meaningful Content?

**Three-Layer Enforcement:**
1. **Creation**: Templates with prompts, not empty files
2. **Progress**: Mid-task validation checkpoints
3. **Completion**: Final validation before task close

---

## 2. Current State Assessment

### Template Creation Process

Templates created at task start:
- THOUGHTS.md
- LEARNINGS.md
- DECISIONS.md
- RESULTS.md
- ASSUMPTIONS.md

### Evidence of Problem

Analysis found:
- 4 tasks with completely empty files
- Only 1 task with meaningful content
- Files created but never populated

---

## 3. Proposed Solution

### Content Validation Rules

**Minimum Thresholds:**
- THOUGHTS.md: 300+ characters
- LEARNINGS.md: 200+ characters
- DECISIONS.md: 150+ characters
- RESULTS.md: 250+ characters

**Structural Validation:**
- Must have section headers (##)
- Must not contain template placeholders
- Must have actionable content

### Enforcement Mechanism

**Configuration:**
```yaml
validation:
  mode: "warn"  # warn | block
  thresholds:
    thoughts_min: 300
    learnings_min: 200
```

---

## 4. Implementation Plan

### Phase 1: Define Validation Rules (4 hours)

1. Define minimum thresholds
2. Create validation schema
3. Document requirements
4. Get team agreement

### Phase 2: Create Validation Script (8 hours)

1. Create `validate-task-content.py`
2. Implement character counting
3. Detect template placeholders
4. Check structural elements

### Phase 3: Integrate with Task Completion (6 hours)

1. Modify task completion workflow
2. Add validation gate
3. Create warning/block mechanism
4. Test integration

### Phase 4: Add User Guidance (4 hours)

1. Create template prompts
2. Add inline guidance
3. Create examples
4. Document best practices

### Phase 5: Test and Document (6 hours)

1. Test with sample tasks
2. Validate thresholds
3. Update documentation
4. Train team

---

## 5. Success Criteria

- [ ] Validation rules defined
- [ ] Validation script working
- [ ] Integration complete
- [ ] User guidance added
- [ ] Documentation updated

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Rules | 4 hours | 4 hours |
| Phase 2: Script | 8 hours | 12 hours |
| Phase 3: Integration | 6 hours | 18 hours |
| Phase 4: Guidance | 4 hours | 22 hours |
| Phase 5: Test | 6 hours | 28 hours |
| **Total** | **28 hours** | **~4 days** |

---

*Plan created based on template usage analysis*
