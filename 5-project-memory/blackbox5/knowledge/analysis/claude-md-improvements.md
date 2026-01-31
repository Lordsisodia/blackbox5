# CLAUDE.md Decision Framework Analysis

**Analysis Date:** 2026-02-01
**Task:** TASK-1738366800
**Analyst:** RALF-Executor
**Source:** goals.yaml IG-001

---

## Executive Summary

Analysis of `~/.claude/CLAUDE.md` and recent run patterns reveals **4 specific improvement areas** that would reduce decision hesitation and context overflow exits. The current framework is well-structured but lacks specificity in key decision boundaries.

---

## Identified Improvement Areas

### 1. **Decision Framework Thresholds Need Quantification**

**Current State:**
The "When to Just Do It" section uses vague time estimates:
- "Clear bug fix (< 30 min)"
- "Simple edit (< 10 min)"
- "> 30 minutes of work"

**Problem:** Time estimates are subjective and vary by context. Recent DECISIONS.md files show hesitation when tasks fall in the gray zone between categories.

**Evidence from Run Patterns:**
- run-0003: Debated between "implement" and "analyze" for validation system
- run-0004: Uncertainty about whether project mapping was "simple" or "complex"

**Recommendation:**
Replace time-based thresholds with **action-based criteria**:

```markdown
### When to Just Do It
- Single file modification with clear scope
- Documentation typo or formatting fix
- Adding a log line or comment
- Changing a configuration value
- All target paths are known and exist

### When to Create Formal Task
- Requires reading >3 files to understand context
- Modifies >2 files
- Has external dependencies (APIs, databases)
- Affects critical system paths
- Requires validation/testing beyond syntax check
```

**Reversibility:** HIGH - Can adjust criteria based on usage

---

### 2. **Context Management Thresholds Need Tuning**

**Current State:**
```markdown
- **70% context usage:** Summarize THOUGHTS.md
- **85% context usage:** Complete current task, exit with PARTIAL
- **95% context usage:** Force checkpoint, exit immediately
```

**Problem:** The 70% threshold for summarization may be too aggressive. Recent runs show THOUGHTS.md summarization happening when substantial context remains.

**Evidence from Run Patterns:**
- No recent runs have hit 85% or 95% thresholds
- Most tasks complete well below 70%
- Summarization at 70% may discard useful context prematurely

**Recommendation:**
Adjust thresholds based on observed patterns:

```markdown
### Context Management

**Conservative Mode (default):**
- **75% context usage:** Summarize THOUGHTS.md (keep key decisions only)
- **85% context usage:** Complete current subtask, exit with PARTIAL
- **95% context usage:** Force checkpoint, exit immediately

**Aggressive Mode (for complex tasks):**
- **80% context usage:** Summarize THOUGHTS.md
- **90% context usage:** Complete current subtask, exit with PARTIAL
- **95% context usage:** Force checkpoint, exit immediately

**When to use Aggressive Mode:**
- Task involves >5 files
- Task requires multi-step reasoning
- Task is in unfamiliar domain
```

**Reversibility:** MEDIUM - Threshold changes affect all future runs

---

### 3. **Sub-Agent Deployment Rules Lack Specificity**

**Current State:**
```markdown
**ALWAYS spawn sub-agents for:**
- Codebase exploration (finding files, patterns)
- Context gathering (reading multiple files)
- Research (investigating unknown areas)
- Validation (reviewing your work)

**NEVER spawn sub-agents for:**
- Simple file reads (use Read tool directly)
- Implementation work (do it yourself)
- Known locations
```

**Problem:** "Codebase exploration" and "Context gathering" are vague. Recent runs show inconsistent sub-agent usage.

**Evidence from Run Patterns:**
- run-0003: Used direct reads instead of sub-agent for skill discovery (worked well)
- run-0004: Direct file reads for project mapping (efficient)
- No recent runs used sub-agents for exploration

**Recommendation:**
Add specific heuristics for sub-agent deployment:

```markdown
### Sub-Agent Deployment Rules

**ALWAYS spawn sub-agents when:**
- Searching for patterns across >10 files
- Need to find files by content (not just name)
- Investigating error patterns in logs
- Cross-project context gathering (>2 projects)
- Time estimate for manual search >5 minutes

**USE JUDGMENT (consider context cost):**
- 3-10 files to examine → Direct reads with Glob/Grep
- Known directory structure → Direct navigation
- Simple pattern matching → Grep directly

**NEVER spawn sub-agents for:**
- <3 file reads
- Files at known paths
- Implementation work
- Single-purpose validation
```

**Reversibility:** HIGH - Can adjust heuristics based on effectiveness

---

### 4. **Stop Conditions Need Prioritization**

**Current State:**
7 stop conditions listed without priority:
1. Unclear Requirements
2. Scope Creep
3. Blocked
4. High Risk
5. Context Overflow
6. Contradiction
7. No Clear Path

**Problem:** When multiple conditions apply, it's unclear which takes precedence. Recent DECISIONS.md files don't reference stop conditions explicitly.

**Evidence from Run Patterns:**
- No explicit stop condition references in recent runs
- Planner's DECISIONS.md shows implicit application of "No Clear Path" → ask for clarification

**Recommendation:**
Add prioritization and explicit trigger examples:

```markdown
## Stop Conditions

**STOP immediately (do not proceed):**
| Priority | Condition | Trigger Example |
|----------|-----------|-----------------|
| 1 | **Contradiction** | Task says "use JWT" but codebase uses sessions |
| 2 | **Context Overflow** | At 95% with work remaining |
| 3 | **Blocked** | External API down, missing credentials |

**PAUSE and ask user:**
| Priority | Condition | Trigger Example |
|----------|-----------|-----------------|
| 4 | **Unclear Requirements** | Success criteria missing or ambiguous |
| 5 | **No Clear Path** | >2 valid approaches, uncertain which is best |
| 6 | **High Risk** | Change affects >5 critical files |

**PAUSE and reassess:**
| Priority | Condition | Trigger Example |
|----------|-----------|-----------------|
| 7 | **Scope Creep** | Task growing beyond original intent |

**Exit Strategy:**
- Priority 1-3: Exit immediately with BLOCKED status
- Priority 4-6: Ask user via chat-log.yaml, wait for response
- Priority 7: Document scope change, ask if continue
```

**Reversibility:** HIGH - Can reprioritize based on incident analysis

---

## Additional Observations

### What's Working Well

1. **Superintelligence Protocol** - Clear activation criteria with specific keywords
2. **BlackBox5 Workflow Integration** - Well-structured workspace requirements
3. **Task File Format** - Clear template with all required fields
4. **Decision Framework Categories** - Logical separation of decision types

### Minor Gaps

1. **No guidance on task batching** - When can multiple small tasks be done together?
2. **Missing: "When to use skills"** - Skills are available but no selection guidance
3. **No rollback guidance** - Task file mentions rollback strategy but CLAUDE.md doesn't guide how

---

## Recommended Implementation Order

1. **Immediate (this week):** Implement Area 4 (Stop Condition Prioritization)
   - Low risk, high clarity benefit
   - Can be added without changing existing structure

2. **Short-term (next 2 weeks):** Implement Area 1 (Quantified Thresholds)
   - Replace time-based with action-based criteria
   - Test with 5-10 tasks, measure hesitation reduction

3. **Medium-term (next month):** Implement Area 3 (Sub-Agent Specificity)
   - Requires observing sub-agent effectiveness
   - May need skill integration for deployment decisions

4. **Evaluate:** Area 2 (Context Threshold Tuning)
   - Requires data on actual context usage
   - Implement after collecting usage metrics

---

## Success Metrics

Track these to measure improvement effectiveness:

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Decision hesitation events | Unknown | <1 per task | Count "ask user" for unclear decisions |
| Context overflow exits | Unknown | <5% of tasks | Exit with PARTIAL/BLOCKED at 85%+ |
| Sub-agent effectiveness | Unknown | >80% useful | Post-task review of sub-agent value |
| Task initiation time | Unknown | <2 minutes | Time from task read to first action |

---

## Related Goals

- **IG-001:** Improve CLAUDE.md Effectiveness (this analysis)
- **IG-003:** Improve System Flow (cross-project dependencies)
- **IG-004:** Optimize Skill Usage (sub-agent deployment)

---

## Conclusion

The CLAUDE.md decision framework is fundamentally sound but needs specificity in four areas:

1. **Quantify decision thresholds** - Replace time with action-based criteria
2. **Tune context thresholds** - Adjust based on observed patterns
3. **Specify sub-agent rules** - Add concrete heuristics
4. **Prioritize stop conditions** - Add explicit priority and triggers

These changes would address the goals.yaml IG-001 issues of "decision framework could be more specific" and "context management thresholds may need tuning."

---

**Analysis Complete:** 2026-02-01T08:15:00Z
**Next Review:** After 5 tasks executed with new framework
