# Decisions - TASK-1769899000

## Threshold Selection for File Count

**Context:** The analysis showed 4-12 file reads work efficiently with direct access, but didn't specify an upper bound for when sub-agents become more efficient.

**Selected:** 15 files as the threshold

**Rationale:**
- Analysis observed 4-12 files working well with direct reads
- 15 provides a buffer above the observed range
- Round number that's easy to remember
- Aligns with the "complexity" intuition - 15+ files starts to feel like a significant exploration task

**Reversibility:** HIGH - Can adjust threshold based on future observations

## Preserving Two-Section Format

**Context:** Could have restructured to a single flowchart-style decision tree or kept the two-section format.

**Selected:** Kept the two-section format (ALWAYS spawn when / USE DIRECT READS when)

**Rationale:**
- Maintains familiarity for existing users of CLAUDE.md
- Easier to scan quickly
- Matches the mental model of "when to use each approach"

**Reversibility:** MEDIUM - Could refactor to a decision tree later if needed

## Original Text Preserved for Reference

**Original text (lines 167-178):**
```markdown
### Sub-Agent Rules

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

**Rollback:** Can restore with: `git checkout ~/.claude/CLAUDE.md`
