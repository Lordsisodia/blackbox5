# Recent Learnings

**Last Updated:** 2026-02-02
**Agent:** Claude

This document tracks recent discoveries and insights. Archive old learnings periodically.

---

## 2026-02-02: Run Structure Analysis

**Discovery:** Analyzed 146 runs to find actual file usage
**Impact:** High
**Action:** Simplified from 6 files to 4 files

Details:
- THOUGHTS.md: 100% usage
- RESULTS.md: 99% usage
- DECISIONS.md: 97% usage
- metadata.yaml: 76% usage
- LEARNINGS.md: 13% usage (merged)
- ASSUMPTIONS.md: 12% usage (merged)

---

## 2026-02-02: Hook vs Prompt Enforcement

**Discovery:** LLMs cannot reliably follow prompt instructions for critical automation
**Impact:** Critical
**Action:** Use COMMAND hooks instead

Details:
- 0% queue sync success with prompts
- 100% success with bash hooks
- Hooks are zero tokens, <100ms

---

## 2026-02-02: Dynamic Prompt Building

**Discovery:** Can include YAML in prompts alongside MD
**Impact:** High
**Action:** Created ralf-build-prompt.sh

Details:
- Concatenate multiple files into prompt
- Self-updating context system
- Agents update files → next run has new context

---

## Template for New Learnings

```markdown
## YYYY-MM-DD: [Discovery Title]

**Discovery:** [What was learned]
**Impact:** Low/Medium/High
**Action:** [What to do about it]

Details:
[Additional context]
```

---

*Archive learnings older than 30 days to learnings/archived/*
