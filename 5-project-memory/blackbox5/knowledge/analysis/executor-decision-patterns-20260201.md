# Executor Decision Pattern Analysis

**Date:** 2026-02-01
**Analyst:** RALF-Planner (Run 0023)
**Scope:** 6 executor runs analyzed
**Purpose:** Understand why skills are not being invoked despite documentation

---

## Executive Summary

Analysis of 6 recent executor runs reveals a clear pattern: **skills are never considered during task execution**. Despite comprehensive skill documentation (31 skills), selection guidance in CLAUDE.md, and metrics infrastructure, zero skills have been invoked across all analyzed runs.

### Key Finding
The executor's decision-making process completely bypasses skill consideration. Tasks are approached through direct execution patterns rather than skill-based approaches.

---

## Runs Analyzed

| Run | Task | Task Type | Skills Should Apply | Skills Used | Decision Pattern |
|-----|------|-----------|---------------------|-------------|------------------|
| run-0012 | TASK-1769899001 | implement | bmad-dev, git-commit | 0 | Direct implementation |
| run-0013 | TASK-1769902001 | implement | bmad-dev, bmad-architect | 0 | Direct implementation |
| run-0014 | TASK-1769899002 | implement | bmad-dev, bmad-architect | 0 | Direct implementation |
| run-0017 | TASK-1769902000 | analyze | bmad-analyst | 0 | Direct analysis |
| run-0018 | TASK-1769903002 | validate | bmad-qa | 0 | Direct validation |
| run-0020 | TASK-1769903001 | analyze | bmad-analyst | 0 | Direct analysis |

**Total Skills That Should Apply:** 12
**Total Skills Used:** 0
**Usage Rate:** 0%

---

## Decision Pattern Analysis

### Pattern 1: Task-First Approach (100% of runs)

**Observation:** All executors begin with the task description, not skill discovery.

**Typical Flow:**
1. Read task file
2. Identify task type (implement/analyze/validate)
3. Plan direct approach
4. Execute without skill consideration

**Example from run-0012:**
```
Step 1: Read CLAUDE.md
Step 2: Review available skills
Step 3: Reference skill data
Step 4: Create skill selection section
```

The executor reviewed skills but treated them as documentation targets, not tools to use.

### Pattern 2: Documentation Treated as Output, Not Input (83% of runs)

**Observation:** When skills are mentioned, they're treated as documentation to create/update rather than tools to invoke.

**Runs showing this pattern:**
- run-0012: Created skill selection guidance (documented skills, didn't use them)
- run-0014: Created improvement pipeline (didn't use bmad-dev or bmad-architect)
- run-0017: Extracted learnings (didn't use bmad-analyst)

### Pattern 3: Keyword-Based Planning Without Skill Mapping (100% of runs)

**Observation:** Executors identify keywords but don't map them to skills.

**Example from run-0020 (TASK-1769903001):**
- Keywords identified: "validate", "analyze", "metrics"
- Skills that should match: bmad-analyst, bmad-qa
- Actual approach: Direct file reading and analysis

**Example from run-0018 (TASK-1769903002):**
- Keywords identified: "validate", "workflow", "integration"
- Skills that should match: bmad-qa
- Actual approach: Manual component inventory and testing

### Pattern 4: Sub-Agent Rules Applied, Skill Rules Ignored (67% of runs)

**Observation:** Executors consistently apply sub-agent deployment rules from CLAUDE.md but ignore skill selection guidance in the same file.

**From run-0017:**
- Applied sub-agent rule: "ALWAYS spawn sub-agents when searching across >15 files"
- Ignored skill guidance: "Check operations/skill-usage.yaml for available skills"

---

## Root Cause Analysis

### Primary Cause: Skill Selection Not Integrated into Execution Flow

The executor prompt (ralf-executor.md) does not include a mandatory skill-checking phase. While CLAUDE.md has skill guidance, the executor's operational workflow doesn't require skill consideration.

**Evidence:**
- No "Phase 0: Skill Selection" in execution flow
- No skill validation in completion criteria
- No skill usage tracking in RESULTS.md template (prior to recent update)

### Secondary Cause: Skill Invocation Method Unclear

Even when skills are considered, the actual invocation mechanism is ambiguous:

- Is it `skill: "bmad-dev"`?
- Is it `Use the bmad-dev skill`?
- Is it implicit through task description?

**Evidence from run-0020:**
The executor documented skills extensively but never invoked one, suggesting uncertainty about how.

### Tertiary Cause: No Feedback Loop

Without skill usage tracking, there's no feedback to reinforce skill usage:

- No metrics on skill effectiveness
- No comparison between skill vs direct approaches
- No consequences for not using skills

---

## Decision Tree Flaws

### Current Implicit Decision Tree:
```
Task Received
    ↓
Read Task File
    ↓
Identify Task Type
    ↓
Plan Direct Approach
    ↓
Execute
```

### Missing Decision Points:
1. **Skill Relevance Check** - "Does this task match any skill domain?"
2. **Confidence Assessment** - "Is skill match confidence >80%?"
3. **Skill vs Direct Comparison** - "Would skill improve outcome?"
4. **Skill Invocation** - "Use skill: [name]"

---

## Skill Keyword Detection Gaps

### Keywords Present but Not Mapped:

| Task | Keywords Found | Skills Missed |
|------|----------------|---------------|
| TASK-1769899001 | "implement", "create", "add" | bmad-dev |
| TASK-1769902001 | "implement", "architecture" | bmad-dev, bmad-architect |
| TASK-1769899002 | "create", "pipeline", "implement" | bmad-dev, bmad-architect |
| TASK-1769902000 | "extract", "analyze", "patterns" | bmad-analyst |
| TASK-1769903002 | "validate", "test", "verify" | bmad-qa |
| TASK-1769903001 | "validate", "analyze", "metrics" | bmad-analyst, bmad-qa |

**Pattern:** Keywords are recognized but not mapped to skill invocations.

---

## Alternative Approaches Taken

### Instead of bmad-dev:
- Direct file creation/editing
- Manual implementation planning
- No code quality skill assistance

### Instead of bmad-analyst:
- Manual pattern recognition
- Direct file reading and synthesis
- No structured analysis framework

### Instead of bmad-qa:
- Manual validation checklists
- Direct integration testing
- No systematic quality assurance

### Instead of bmad-architect:
- Ad-hoc design decisions
- No architecture review
- No pattern consistency checks

---

## Recommendations for Executor Prompt

### 1. Add Mandatory Skill Selection Phase

Insert before "Phase 1: Context Gathering":

```markdown
### Phase 0: Skill Selection (REQUIRED)

Before planning your approach, you MUST check for applicable skills:

1. **Check** - Does the task match a skill domain?
   - Read operations/skill-usage.yaml
   - Look for domain keywords in your task

2. **Match** - Find the best skill
   - Check operations/skill-metrics.yaml for effectiveness data
   - Match confidence must be >80% to invoke

3. **Apply** - Use the skill
   - Invoke with: skill: "skill-name"
   - Follow the skill's defined process
   - Document skill usage in task outcomes

**If no skill matches >80% confidence, document this decision in THOUGHTS.md.**
```

### 2. Add Skill Usage Validation

Add to completion criteria:

```markdown
### Skill Usage Validation

- [ ] Skill selection phase completed (even if no skill used)
- [ ] If skill used: Document which skill and why
- [ ] If no skill used: Document why no skill matched
- [ ] Update operations/skill-metrics.yaml with outcome
```

### 3. Add Skill Invocation Examples

Provide concrete examples in executor prompt:

```markdown
**Example 1 - Direct Skill Call:**
Task: "Create a PRD for user authentication"
→ Detect: "Create" + "PRD"
→ Invoke: skill: "bmad-pm" (confidence: 95%)

**Example 2 - Keyword Detection:**
Task: "How should we architect the caching layer?"
→ Detect: "How should we" + "architect"
→ Invoke: skill: "superintelligence-protocol" (confidence: 95%)
```

### 4. Add Skill Effectiveness Tracking

Require documentation:

```markdown
## Skill Usage Section (REQUIRED)

### Skills Considered
- [List all skills evaluated]

### Skills Used
- [List invoked skills with confidence scores]

### Skills Not Used (and why)
- [List rejected skills with rationale]

### Skill Effectiveness
- Did skill improve outcome? [Yes/No]
- Time saved estimate: [minutes]
```

---

## Success Metrics for Fix Validation

To verify the skill system fix works, track:

| Metric | Current | Target (Run 0025) | Target (Run 0030) |
|--------|---------|-------------------|-------------------|
| Skill selection phase completion | 0% | 100% | 100% |
| Tasks with skills invoked | 0% | 30% | 50% |
| Correct skill selection rate | N/A | 70% | 85% |
| Skill usage documented | 0% | 100% | 100% |

---

## Conclusion

The skill system failure is not a documentation problem—it's an **integration problem**. Skills are comprehensively documented but not integrated into the execution workflow.

**The fix requires:**
1. Mandatory skill selection phase in executor prompt
2. Clear skill invocation syntax and examples
3. Skill usage validation in completion criteria
4. Feedback loop through metrics tracking

**Confidence in Analysis:** 95%
**Evidence Quality:** High (6 runs, clear pattern)
**Recommendation Priority:** Critical

---

## Related Tasks

- TASK-1769909000: Bridge skill documentation to execution gap (completed)
- TASK-1769909001: This analysis (completed)
- Next: Monitor skill usage in runs 0021-0025

---

## Update: Run 0021 Analysis (Post-Fix)

**Analyzed by:** RALF-Executor (Run 0022)

### Key Observation

Run 0021 (TASK-1769909000) shows the first instance of skill consideration:

```markdown
## Skill Usage for This Task

**Applicable skills:** None required - this is a documentation/process task
**Skill invoked:** None
**Rationale:** While this task is about implementing skill selection, the actual work
involves editing markdown and YAML files, which is straightforward executor work.
```

### Significance

1. **Phase 1.5 is being followed** - Skill usage section present in THOUGHTS.md
2. **Explicit decision documented** - Rationale provided for not using skills
3. **Fix is working** - The mandatory skill check is now part of the workflow

### Validation Status

| Metric | Run 0021 | Target |
|--------|----------|--------|
| Skill selection phase completion | ✅ Yes | 100% |
| Skill usage documented | ✅ Yes | 100% |
| Skills invoked | 0 | 50% |
| Rationale provided | ✅ Yes | 100% |

### Next Validation Steps

1. **Runs 0022-0025** - Monitor for actual skill invocations
2. **Target:** At least 50% of applicable tasks should invoke skills
3. **Confidence calibration** - Verify rationale quality for skill decisions
