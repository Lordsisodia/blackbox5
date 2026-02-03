# Decisions - TASK-1769895001

## Decision 1: Focus on RALF-Executor, Not LEGACY.md Directly

**Context:** LEGACY.md is located in siso-internal project, but RALF-Executor operates on blackbox5 with different procedures in ralf-executor.md.

**Selected:** Analyze both systems and document the disconnect as a friction point, rather than modifying LEGACY.md directly.

**Rationale:**
- LEGACY.md describes the Legacy autonomous build system
- RALF-Executor uses different procedures in 2-engine/.autonomous/prompts/
- Modifying LEGACY.md would not affect RALF-Executor behavior
- Better to document findings and create RALF-specific optimizations

**Reversibility:** HIGH - Can modify LEGACY.md later if needed

---

## Decision 2: Create Task-Type Specific Quality Gates

**Context:** Current quality gates in LEGACY.md are generic and don't match task-specific needs.

**Selected:** Create operations/quality-gates.yaml with universal gates + task-specific gates for 6 task types.

**Rationale:**
- Analysis tasks don't need "tests written" gate
- Implementation tasks need code review gates
- Fix tasks need regression testing gates
- Task-specific gates improve quality without overhead

**Reversibility:** HIGH - Can adjust gates based on usage

---

## Decision 3: Recommend Lowering Skill Threshold from 80% to 70%

**Context:** Analysis of runs 0022 and 0024 shows skills at 70-75% confidence were not invoked due to 80% threshold.

**Selected:** Recommend lowering threshold to 70% in ralf-executor.md.

**Rationale:**
- Run 0022: bmad-analyst at 70% confidence - would have been invoked
- Run 0024: bmad-analyst at 75% confidence - would have been invoked
- Need invocation data to calibrate system effectiveness
- 70% still ensures high confidence while enabling skill usage

**Reversibility:** HIGH - Can adjust back to 80% if needed

---

## Decision 4: Document Skill Non-Invocation Rationale

**Context:** This analysis task could have used bmad-analyst skill at 75% confidence.

**Selected:** Document rationale for not invoking skill, following Phase 1.5 requirements.

**Rationale:**
- Task requirements are explicit and straightforward
- Deliverables are clear (analysis doc + YAML file)
- Skill would add overhead without significant value
- Demonstrates appropriate use of confidence threshold

**Reversibility:** N/A - Documentation decision

---

## Decision 5: Include LEGACY/RALF Disconnect as Friction Point

**Context:** LEGACY.md and RALF-Executor are different systems with overlapping but different procedures.

**Selected:** Document the disconnect as a high-impact friction point with recommendation to create RALF-specific procedures.

**Rationale:**
- Causes confusion about which procedures to follow
- LEGACY.md references files/paths that don't exist in RALF context
- Clear separation would improve clarity
- Recommendation: Create LEGACY-RALF.md for RALF-specific procedures

**Reversibility:** MEDIUM - Can merge systems later if desired
