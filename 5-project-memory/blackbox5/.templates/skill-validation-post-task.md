## Skill Decision Validation

**Task ID:** [TASK-XXX]
**Timestamp:** [YYYY-MM-DD HH:MM]
**Validated By:** [agent-name or human]

---

### Skill Decision Summary

**Skill Recommended:** [skill-name or "None"]
**Confidence Score:** [XX%] (if skill was recommended)
**Decision Made:**
- [ ] Skill was invoked
- [ ] Skill was overridden (not invoked)
- [ ] No skill was recommended

**Override Justification File:** [./skill-override-justification.md] (if overridden)

---

### Validation Criteria

**Was the skill decision correct?**
- [ ] **CORRECT** - Skill was the right choice for this task
- [ ] **INCORRECT** - Skill was the wrong choice (should have invoked different skill or no skill)
- [ ] **PARTIAL** - Skill helped but wasn't optimal (explain below)
- [ ] **UNCLEAR** - Cannot determine (explain why)

**Validation Evidence:**

1. **Task Outcome:** [Describe the outcome - was the task completed successfully?]

2. **Skill Effectiveness:**
   - Did using the skill (or not using it) help or hinder the task?
   - [ ] Helped significantly
   - [ ] Helped somewhat
   - [ ] Made no difference
   - [ ] Hindered the task

3. **Time Impact:**
   - Actual time: [X minutes]
   - Would skill have made it faster/slower? [Explain]

4. **Quality Impact:**
   - Did the skill improve quality of the outcome?
   - [ ] Yes, significantly
   - [ ] Yes, somewhat
   - [ ] No impact
   - [ ] Reduced quality

5. **Alternative Considered:**
   - Could a different skill have been better?
   - [ ] Yes, [which skill?] - [why?]
   - [ ] No, this was the best choice

---

### Detailed Rationale

**If CORRECT:**
[Explain why the skill decision was the right choice.
What was the evidence? What would have happened without this decision?]

**If INCORRECT:**
[Explain why the skill decision was wrong.
What should have been done instead? What negative impact did it have?]

**If PARTIAL:**
[Explain what worked and what didn't.
How could the skill be improved? What was the missing piece?]

**If UNCLEAR:**
[Explain why validation is ambiguous.
What additional information is needed?]

---

### Recommendations for Improvement

**For Skill Triggers:**
- [ ] Adjust confidence threshold for [skill-name] (current: 70% → suggest: XX%)
- [ ] Add/modify trigger keywords: [list keywords]
- [ ] Update domain mapping for [category]
- [ ] Other: [explain]

**For Skill Content:**
- [ ] Add coverage for [specific use case]
- [ ] Improve guidance on [specific topic]
- [ ] Update examples/baselines
- [ ] Other: [explain]

---

### Validation Metadata

**Validation Confidence:** [HIGH/MEDIUM/LOW] (how certain are you of this validation?)
**Validation Basis:**
- [ ] Direct observation of task execution
- [ ] Review of task deliverables
- [ ] Comparison with similar tasks
- [ ] Post-hoc analysis
- [ ] Other: [explain]

**Follow-up Required:**
- [ ] No - validation is complete
- [ ] Yes - [what needs to be done?]

---

**Validation Checklist:**

**Required Fields:**
- [ ] Task outcome documented
- [ ] Skill effectiveness assessed
- [ ] Detailed rationale provided (correct/incorrect/partial/unclear)
- [ ] Evidence cited

**Optional but Recommended:**
- [ ] Time impact noted
- [ ] Quality impact noted
- [ ] Recommendations for improvement provided
- [ ] Validation confidence level set

---

**Validation Status:**
- [ ] **COMPLETE** - All required fields filled, validation ready to submit
- [ ] **INCOMPLETE** - Missing required fields, needs completion before submission

---

**Next Steps:**
1. Run `bb5 skill:validate` to record this validation in skill-registry.yaml
2. Review recommendations and implement improvements
3. Track trigger_accuracy over time

---

**Example Validations:**

### Example 1: CORRECT - Skill Invoked
```
Skill: git-commit
Confidence: 87% (clear trigger)
Decision: Skill invoked
Validation: CORRECT

Rationale:
Task was "implement git commit workflow for feature branch". Skill provided
complete commit message structure, branch naming, and push workflow. Completed
in 5 minutes with no errors. Without skill, would have taken 15 minutes and
required multiple corrections.

Evidence:
- Task completed successfully
- Git history shows proper commits
- No reverts or corrections needed
```

### Example 2: INCORRECT - Override Should Not Have Happened
```
Skill: bmad-architect
Confidence: 72% (discretionary)
Decision: Skill overridden (reason: "I can handle this")
Validation: INCORRECT

Rationale:
Task was "design authentication system for multi-tenant app". Agent override
justification was "I can handle this", but implementation had critical flaws:
- No consideration of token rotation
- Missing rate limiting architecture
- Incorrect session management design

Result:
System required complete redesign (2 days) due to architecture flaws.
If skill had been used, would have caught these issues upfront.

Evidence:
- Implementation had to be scrapped
- Security audit found 3 critical issues
- Re-implementation using skill took 4 hours vs 2 days wasted
```

### Example 3: PARTIAL - Skill Helped But Wasn't Optimal
```
Skill: test-generator
Confidence: 78% (discretionary)
Decision: Skill invoked
Validation: PARTIAL

Rationale:
Skill generated basic unit tests for API endpoints, which was helpful.
However:
- Tests didn't cover edge cases (empty payloads, null values)
- No integration tests for multi-endpoint workflows
- Missing performance tests for rate limiting
- Test coverage only 45% instead of target 70%

Result:
Tests provided basic safety but missed 3 bugs in production.
Would have been better to combine test-generator with manual test design
or use different skill for API testing specifically.

Evidence:
- 3 bugs found in production that should have been caught by tests
- Post-hoc manual test review identified gaps
- Combined approach would have taken 30 min vs 20 min for skill alone
```
