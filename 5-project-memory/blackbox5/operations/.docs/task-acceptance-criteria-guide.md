# Task Acceptance Criteria Guide

## Overview

Clear acceptance criteria are essential for task execution success. They define what "done" means and prevent scope creep, misunderstandings, and incomplete work.

## Why Acceptance Criteria Matter

Based on analysis of 80+ learnings, task scope clarity issues consistently cause problems:

- **Ambiguous tasks** lead to confusion and rework
- **Missing criteria** result in incomplete implementations
- **Unclear scope** makes estimation impossible
- **No definition of done** means never-ending tasks

## Using the Acceptance Criteria Template

### Location
`.templates/tasks/task-acceptance-criteria.md.template`

### When to Use

**Required for:**
- All MEDIUM and HIGH priority tasks
- Tasks touching multiple files
- Tasks with complex requirements
- Tasks that will be delegated

**Optional for:**
- LOW priority quick fixes
- Simple documentation updates
- Emergency patches

### How to Apply

1. **Copy the template** into your task file or reference it
2. **Fill in the Definition of Done** section
3. **Select task-type specific criteria** that apply
4. **Define verification steps**
5. **Review criteria before starting work**

## Writing Good Acceptance Criteria

### SMART Criteria

| Principle | Description | Example |
|-----------|-------------|---------|
| **S**pecific | Clear and unambiguous | "Create file X" not "Handle files" |
| **M**easurable | Can be verified | "3 files created" not "some files" |
| **A**chievable | Realistic given constraints | Within time/resources |
| **R**elevant | Aligns with task objective | Directly contributes to goal |
| **T**ime-bound | Has completion deadline | "By end of run" |

### Examples by Task Type

#### Implement Task Example

```markdown
### Must-Have
- [ ] YAML file created at `operations/config.yaml`
- [ ] Schema includes all required fields (name, type, status)
- [ ] File validates against schema
- [ ] Documentation updated in `.docs/config-guide.md`

### Should-Have
- [ ] Example configurations provided
- [ ] Validation script created

### Verification
- [ ] Manual: File exists and is valid YAML
- [ ] Automated: `yamllint operations/config.yaml` passes
```

#### Fix Task Example

```markdown
### Must-Have
- [ ] Error no longer occurs in test case X
- [ ] Root cause documented in THOUGHTS.md
- [ ] No regressions in related functionality

### Should-Have
- [ ] Test case added to prevent regression

### Verification
- [ ] Manual: Run reproduction steps, confirm fix
- [ ] Automated: New test passes
```

#### Refactor Task Example

```markdown
### Must-Have
- [ ] All existing tests pass
- [ ] Code coverage not decreased
- [ ] No functional changes (behavior preserved)
- [ ] Code is more readable/maintainable

### Should-Have
- [ ] Performance improved or maintained
- [ ] Documentation updated

### Verification
- [ ] Automated: Full test suite passes
- [ ] Code review: Peer confirms improvement
```

#### Analyze Task Example

```markdown
### Must-Have
- [ ] Analysis covers all requested areas
- [ ] Findings documented in `knowledge/analysis/`
- [ ] Recommendations are actionable
- [ ] Sources cited for all claims

### Should-Have
- [ ] Visualizations/charts included
- [ ] Alternative approaches considered

### Verification
- [ ] Review: Findings are accurate and thorough
- [ ] Review: Recommendations are practical
```

## Priority Levels Explained

### Must-Have (Blocking)
- Task CANNOT be marked complete without these
- Core functionality requirements
- Quality gates (tests pass, no regressions)
- Process requirements (documentation, commits)

### Should-Have (Important)
- Significantly improve task value
- May be deferred if time-constrained
- Should be completed in most cases

### Nice-to-Have (Bonus)
- Enhancements beyond core requirements
- Only if time permits
- Can be moved to follow-up tasks

## Common Pitfalls to Avoid

### ❌ Vague Criteria
- "Make it better"
- "Improve performance"
- "Fix the bug"

### ✅ Specific Criteria
- "Reduce load time from 5s to under 2s"
- "Fix null pointer exception in function X"
- "Add input validation for email field"

### ❌ Unverifiable Criteria
- "Code is clean"
- "Architecture is good"
- "Users will like it"

### ✅ Verifiable Criteria
- "Code passes linting with zero warnings"
- "Follows established project patterns"
- "Usability test with 3 users shows 90% success rate"

## Integration with Task Workflow

### When Creating Tasks
1. Write acceptance criteria BEFORE starting work
2. Review criteria with stakeholders if unclear
3. Update criteria if requirements change

### When Executing Tasks
1. Review acceptance criteria before starting
2. Check off criteria as you complete them
3. Don't mark task complete until all MUST criteria are met

### When Reviewing Tasks
1. Verify all MUST criteria are met
2. Check SHOULD criteria completion
3. Document any exceptions or deviations

## Template Quick Reference

```markdown
## Acceptance Criteria

### Must-Have
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

### Should-Have
- [ ] [Specific, testable criterion]

### Nice-to-Have
- [ ] [Specific, testable criterion]

### Verification Method
- [ ] [How to verify]
```

## Success Metrics

After implementing acceptance criteria:
- Task rework rate should decrease
- Time to complete should become more predictable
- Task disputes/confusion should decrease
- Quality of deliverables should improve

## Related Resources

- `.templates/tasks/task-specification.md.template` - Full task template
- `.templates/tasks/task-completion.md.template` - Completion documentation
- `operations/improvement-backlog.yaml` - Source: IMP-1769903009
