# Consolidated Rules Analysis for BlackBox5

**Date:** 2026-02-06
**Status:** Analysis Complete - Ready for Implementation

---

## Executive Summary

Three sub-agents analyzed CLAUDE.md, LEGACY.md, and executor/planner prompts. This document consolidates their findings into a prioritized implementation plan.

**Total Rules Identified:** 40+
**Critical (P0):** 8 rules
**High (P1):** 12 rules
**Medium (P2):** 15+ rules

---

## P0 - Critical Rules (Implement First)

These rules are fundamental to system operation and safety.

### 1. `001-one-task-per-session.md`
**Source:** LEGACY.md, executor prompts
**Trigger:** Always active
**Content:**
- Each session completes exactly ONE task
- No batching, no multitasking
- Exception: spawning sub-agents for research

### 2. `002-read-before-change.md`
**Source:** LEGACY.md, CLAUDE.md, executor prompts
**Trigger:** Before any file modification
**Content:**
- NEVER propose changes to unread code
- Read ALL target files completely before modifying
- Prevents breaking changes

### 3. `003-git-safety.md`
**Source:** CLAUDE.md
**Trigger:** Git operations
**Content:**
- NEVER update git config
- NEVER run destructive commands (push --force, reset --hard, etc.)
- NEVER skip hooks unless explicitly requested
- NEVER force push to main/master
- Prefer specific file staging over `git add -A`

### 4. `004-phase-1-5-skill-check.md`
**Source:** CLAUDE.md, skill-selection.yaml
**Trigger:** BEFORE Phase 2 (Execution)
**Content:**
- MUST check skill-selection.yaml
- Match task keywords against domain_mapping
- Calculate confidence (>=70% to invoke)
- Document decision in THOUGHTS.md

### 5. `005-superintelligence-auto-activation.md`
**Source:** CLAUDE.md
**Trigger:** Keywords: "Should we", "How should we", architecture, design, refactor, optimize, strategy, complex, integrate
**Content:**
- Activate WITHOUT asking
- Execute 7-step process
- Deploy expert agents
- Return: Recommendation, Confidence, Assumptions, Risks, Implementation Path

### 6. `006-stop-conditions.md`
**Source:** CLAUDE.md, LEGACY.md
**Trigger:** Various stop conditions
**Content:**
- PAUSE and ask user when: unclear requirements, scope creep, blocked, high risk, context overflow (85%), contradictions, no clear path
- EXIT with status: COMPLETE, PARTIAL, or BLOCKED

### 7. `007-sub-agent-deployment.md`
**Source:** CLAUDE.md, executor prompts
**Trigger:** Task planning
**Content:**
- ALWAYS spawn for: >15 files, complex patterns, cross-project, validation, open-ended exploration
- NEVER spawn for: <15 files, known paths, implementation work

### 8. `008-output-style.md`
**Source:** CLAUDE.md, OUTPUT_STYLE.md
**Trigger:** Always active
**Content:**
- High signal, low noise
- 1-3 lines max unless complexity demands
- No intros, no reassurance, no summaries
- Code changes: `[file_path:line] - [what changed]`

---

## P1 - High Priority Rules

### 9. `009-duplicate-check-required.md`
**Trigger:** Phase 1 (Pre-Execution)
**Content:** Search completed/ directory and recent commits for similar tasks

### 10. `010-required-documentation.md`
**Trigger:** Every run
**Content:** Create THOUGHTS.md, RESULTS.md, DECISIONS.md in every run directory

### 11. `011-pre-execution-research.md`
**Trigger:** Phase 1
**Content:** Duplicate detection, context gathering, document in THOUGHTS.md

### 12. `012-quality-gates-checklist.md`
**Trigger:** Before completion
**Content:** Apply task-type specific quality gates

### 13. `013-continuous-improvement.md`
**Trigger:** After every run, every 5 runs
**Content:** Document learnings, synthesize patterns, propose improvements

### 14. `014-decision-framework.md`
**Trigger:** Task assessment
**Content:**
- Just Do It: <30 min, single file
- Create Formal Task: >30 min, multiple files
- Hand Off to RALF: continuous iteration
- Ask User: unclear, scope creep, blocked, high risk

### 15. `015-context-management-thresholds.md`
**Trigger:** During long tasks
**Content:**
- 70%: Summarize THOUGHTS.md
- 85%: Complete task, exit PARTIAL
- 95%: Force checkpoint, exit immediately

### 16. `016-verification-before-completion.md`
**Trigger:** Before claiming completion
**Content:** Check file existence, run import tests, verify functionality

### 17. `017-task-claiming-protocol.md`
**Trigger:** Before starting execution
**Content:** Write to events.yaml with timestamp, task_id, type: started

### 18. `018-planner-executor-separation.md`
**Trigger:** In Dual-RALF mode
**Content:** Planner decides WHAT, Executor decides HOW. Never pick tasks yourself.

### 19. `019-validator-read-only.md`
**Trigger:** When operating as validator
**Content:** NEVER write to worker's directory. ONLY read and validate.

### 20. `020-forbidden-phrases.md`
**Trigger:** Response generation
**Content:** Never use: "I understand you want...", "Let me start by...", "This approach ensures..."

---

## P2 - Medium Priority Rules

### 21. `021-atomic-commits.md`
**Trigger:** Git operations
**Content:** One logical change per commit

### 22. `022-test-everything.md`
**Trigger:** After each change
**Content:** Every change must be verified

### 23. `023-full-paths-only.md`
**Trigger:** All file operations
**Content:** No relative paths ever

### 24. `024-integration-verification.md`
**Trigger:** Before completion
**Content:** Code must work with existing system

### 25. `025-no-placeholders.md`
**Trigger:** Task completion
**Content:** Complete or exit PARTIAL. Never leave placeholder code.

### 26. `026-first-principles-review.md`
**Trigger:** Every 5 runs
**Content:** Read last 5 THOUGHTS.md, analyze patterns, question approach

### 27. `027-validate-assumptions.md`
**Trigger:** Before acting on uncertain info
**Content:** Use truth-seeking skill, self-correct every 3 steps

### 28. `028-completion-signal-requirements.md`
**Trigger:** Before `<promise>COMPLETE</promise>`
**Content:** Task executed, docs exist, all non-empty, task ID recorded

### 29. `029-failure-handling-protocol.md`
**Trigger:** When task cannot complete
**Content:** Document failure, signal appropriately (RETRY, BLOCKED, FAILED, PARTIAL)

### 30. `030-token-budget-management.md`
**Trigger:** During long tasks
**Content:** 60%: save progress, 80%: emergency save, 95%: force checkpoint

### 31. `031-task-validation-before-planning.md`
**Trigger:** Before creating plans
**Content:** Validate task is worth doing (real problem, significant impact, aligned, not duplicate)

### 32. `032-no-placeholders-in-tests.md`
**Trigger:** When writing tests
**Content:** Every test must be functional, no `assert True  # TODO`

### 33. `033-git-branch-safety.md`
**Trigger:** Before commits
**Content:** Never commit directly to main/master

### 34. `034-communication-protocol.md`
**Trigger:** Agent communication
**Content:** Use queue.yaml, events.yaml, chat-log.yaml, heartbeat.yaml

### 35. `035-bb5-navigation.md`
**Trigger:** Path: ~/.blackbox5/
**Content:** Use bb5 CLI for navigation (whereami, goal:list, task:list, etc.)

---

## Implementation Plan

### Week 1: P0 Rules (Critical)
- [ ] Create `.claude/rules/` directory
- [ ] Implement rules 001-008
- [ ] Test auto-trigger behavior
- [ ] Document in CLAUDE-MEMORY-SYSTEM.md

### Week 2: P1 Rules (High Priority)
- [ ] Implement rules 009-020
- [ ] Test with actual tasks
- [ ] Refine triggers based on behavior

### Week 3: P2 Rules (Medium Priority)
- [ ] Implement rules 021-035
- [ ] Run parallel with old system
- [ ] Gather feedback

### Week 4: Migration
- [ ] Deprecate skill-registry.yaml checks
- [ ] Update documentation
- [ ] Train team on new system

---

## Rule File Template

```markdown
---
name: Rule Name
trigger:
  - keyword1
  - keyword2
paths:
  - "**/*.py"
alwaysApply: false
priority: 100
---

# Rule Title

## When to Apply
Description of when this rule triggers.

## Content
- Rule item 1
- Rule item 2
- Rule item 3

## Source
- CLAUDE.md lines X-Y
- LEGACY.md lines Z-W
```

---

## Next Steps

1. **Create P0 rules first** - These are safety-critical
2. **Test with real tasks** - Verify auto-trigger behavior
3. **Iterate on triggers** - Adjust keywords/paths based on experience
4. **Document learnings** - Update this file as we learn

---

**Related:**
- [CLAUDE-RULES-GUIDE.md](./CLAUDE-RULES-GUIDE.md) - How rules work
- [CLAUDE-IMPORTS-GUIDE.md](./CLAUDE-IMPORTS-GUIDE.md) - @path imports (next priority)
- [CLAUDE-LOCAL-GUIDE.md](./CLAUDE-LOCAL-GUIDE.md) - Personal preferences
