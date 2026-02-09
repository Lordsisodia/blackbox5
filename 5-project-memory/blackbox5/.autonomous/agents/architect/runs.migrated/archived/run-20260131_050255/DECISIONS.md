# DECISIONS.md - Ralph Master Prompt Creation

**Task:** TASK-1769809124 - Create Ralph Master System Prompt
**Run:** run-20260131_050255
**Agent:** Agent-2.3
**Date:** 2026-01-31T05:05:00Z

---

## Decision 1: Prompt Structure

**Context:** PLAN-011 specified 8 required sections

**Options:**
- A) Minimal prompt with just loop logic
- B) Comprehensive prompt with all 8 sections
- C) Modular prompt with includes

**Selected:** Option B - Comprehensive prompt

**Rationale:**
- Complete documentation ensures consistent behavior
- Self-contained prompt is easier to maintain
- All sections from PLAN-011 covered

**Reversibility:** HIGH - Can edit prompt structure at any time

---

## Decision 2: Ralph Technique Implementation

**Context:** Balance original Ralph Technique with Blackbox5 integration

**Options:**
- A) Pure Ralph Technique (minimal integration)
- B) Full Blackbox5 integration (modified Ralph)
- C) Hybrid (Ralph core + Blackbox5 features)

**Selected:** Option C - Hybrid approach

**Rationale:**
- Preserves Ralph's core simplicity
- Adds Blackbox5's memory and routing systems
- Incorporates Ralphy's proven patterns (git worktree)

**Reversibility:** MEDIUM - Would require prompt rewrite

---

## Decision 3: Exit Condition Format

**Context:** How Ralph signals loop completion

**Options:**
- A) Exit silently (no output)
- B) Return JSON status
- C) Return "PROMISE_COMPLETE" with status

**Selected:** Option C - Text-based completion signal

**Rationale:**
- Matches original Ralph Technique
- Human-readable in logs
- Easy to parse for automation
- Includes status context

**Reversibility:** LOW - Tightly integrated into loop behavior

---

## Decision 4: Sub-Agent Protocol

**Context:** When to spawn sub-agents vs. doing work directly

**Options:**
- A) Always use sub-agents for everything
- B) Never use sub-agents (monolithic)
- C) Selective use (exploration only)

**Selected:** Option C - Selective sub-agent spawning

**Rationale:**
- Sub-agents for exploration preserve main context
- Direct tool use for simple operations is faster
- Balances speed with context preservation

**Reversibility:** MEDIUM - Protocol can be adjusted

---

## Decision 5: Progress Tracking Files

**Context:** What files to maintain for tracking

**Options:**
- A) Single progress.json
- B) fix_plan.md + prd.json
- C) fix_plan.md + prd.json + progress.json

**Selected:** Option C - All three files

**Rationale:**
- fix_plan.md: Human-readable task checklist
- prd.json: Machine-readable task state
- progress.json: Session-level tracking
- Redundancy prevents data loss

**Reversibility:** HIGH - Files can be added/removed

---

## Decision Summary

| Decision | Selection | Reversibility |
|----------|-----------|---------------|
| Prompt Structure | Comprehensive (8 sections) | HIGH |
| Ralph Technique | Hybrid (Ralph + BB5) | MEDIUM |
| Exit Condition | PROMISE_COMPLETE text | LOW |
| Sub-Agent Protocol | Selective spawning | MEDIUM |
| Progress Tracking | 3-file system | HIGH |

---

**No blocking decisions.** All decisions support the core mission of creating a functional Ralph master system prompt.
