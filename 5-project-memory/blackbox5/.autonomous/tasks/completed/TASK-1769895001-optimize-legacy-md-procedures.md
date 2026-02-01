# TASK-1769895001: Optimize LEGACY.md Operational Procedures

**Type:** analyze
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T08:05:00Z
**Source:** goals.yaml IG-002

---

## Objective

Analyze and optimize the LEGACY.md operational procedures to reduce friction and improve efficiency for the RALF autonomous agent system.

## Context

Per goals.yaml IG-002 (Improve LEGACY.md Operational Efficiency), the current issues are:
- Skill discovery may be too slow
- Quality gates could be more specific
- Run initialization could be optimized

The LEGACY.md file at `~/.blackbox5/5-project-memory/siso-internal/.Autonomous/LEGACY.md` contains the operational procedures that guide RALF execution.

## Success Criteria

- [ ] Read and analyze current LEGACY.md completely
- [ ] Identify at least 3 friction points or inefficiencies
- [ ] Propose specific optimizations for skill discovery
- [ ] Create quality gate checklists per task type
- [ ] Document findings in knowledge/analysis/legacy-md-optimization.md
- [ ] Provide concrete recommendations with examples

## Approach

1. Read LEGACY.md from siso-internal
2. Compare against recent run patterns (check runs/completed/)
3. Identify where agents spend unnecessary time
4. Look for repeated patterns that could be cached or automated
5. Analyze skill selection process for bottlenecks
6. Synthesize optimization recommendations

## Files to Read

- ~/.blackbox5/5-project-memory/siso-internal/.Autonomous/LEGACY.md
- runs/completed/*/THOUGHTS.md (sample 5-10 recent)
- goals.yaml (IG-002 section)
- 2-engine/.autonomous/skills/ (understand skill structure)

## Files to Create

- knowledge/analysis/legacy-md-optimization.md - Analysis and recommendations
- operations/quality-gates.yaml - Task-type specific quality gates (if not exists)

## Focus Areas

### 1. Skill Discovery Optimization
- Current: Skills discovered at runtime
- Target: Faster skill selection, caching frequently used skills

### 2. Quality Gate Specificity
- Current: Generic quality gates
- Target: Task-type specific checklists (analyze, implement, fix, refactor)

### 3. Run Initialization Efficiency
- Current: Multiple file reads at startup
- Target: Streamlined initialization, pre-cached common files

## Notes

Focus on actionable changes that would reduce run setup time and improve task completion efficiency. Reference specific examples from recent runs where procedures were unclear or inefficient.

This task complements TASK-1769895000 (context gathering optimization) - both aim to improve system efficiency.
