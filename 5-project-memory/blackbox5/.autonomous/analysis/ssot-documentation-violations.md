# SSOT Documentation Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Documentation is duplicated across **150+ files** with **11 major duplications** identified. The same concepts are documented multiple times with no clear canonical source.

---

## 1. Skill System Documentation (CRITICAL)

**Skill tracking documented in 5+ places:**

| File | Lines | Content |
|------|-------|---------|
| `CLAUDE.md` | ~100 | Domain-to-skill mapping, auto-trigger rules |
| `operations/skill-selection.yaml` | 150 | Domain mapping, confidence thresholds |
| `operations/skill-metrics.yaml` | 620 | Metrics schema, effectiveness tracking |
| `operations/skill-usage.yaml` | 303 | Usage tracking documentation |
| `.docs/template-system-guide.md` | ~200 | Skill invocation patterns |

**Specific Duplications:**
- Domain-to-skill mapping table exists in BOTH CLAUDE.md AND skill-selection.yaml
- Confidence threshold of 70% documented in 3+ places
- Auto-trigger rules duplicated between files

---

## 2. Template System Documentation

**Template system documented in 4 places:**

| File | Content |
|------|---------|
| `.docs/template-system-guide.md` | Full template guide (~200 lines) |
| `CLAUDE.md` | Template references |
| `bin/bb5-create` | Inline template documentation |
| `bin/bb5-populate-template` | Template usage docs |

**Issue:** Template guide exists but scripts also contain template documentation.

---

## 3. First Principles Documentation

**First principles methodology in 3+ places:**

| File | Content |
|------|---------|
| `CLAUDE.md` | First principles section |
| `6-roadmap/research/superintelligence-protocol/first-principles.md` | Detailed methodology |
| `.autonomous/prompts/ralf-first-principles.md` | Prompt version |
| `knowledge/first-principles/` | Multiple files |

**Issue:** Same methodology documented for humans (CLAUDE.md), for protocol (research), and for prompts.

---

## 4. Improvement Loop Documentation

**RALF/Improvement loop in 4+ places:**

| File | Content |
|------|---------|
| `CLAUDE.md` | RALF overview |
| `6-roadmap/research/superintelligence-protocol/` | Full protocol docs |
| `.autonomous/analysis/IMPROVEMENT-LOOP-RALF-NATIVE.md` | Analysis doc |
| `.autonomous/analysis/AGENT-IMPROVEMENT-LOOP.md` | Another analysis |
| `2-engine/.autonomous/prompts/ralf-improvement-loop.md` | Prompt version |

**Issue:** Same improvement loop concept documented in research, analysis, and prompts.

---

## 5. BlackBox5 Navigation Documentation

**Navigation commands documented in 3 places:**

| File | Content |
|------|---------|
| `CLAUDE.md` | Full bb5 command reference |
| `bin/bb5-whereami` | Inline help |
| `AGENT_CONTEXT.md` | Quick reference |

**Issue:** Commands documented in main guide AND in individual scripts.

---

## 6. Task File Format Documentation

**Task format in 3+ places:**

| File | Content |
|------|---------|
| `CLAUDE.md` | Task file format section |
| `.docs/template-system-guide.md` | Task template |
| `bin/bb5-task` | Inline format docs |
| Actual task files | Living examples |

---

## 7. Decision Framework Documentation

**Decision framework in 3 places:**

| File | Content |
|------|---------|
| `CLAUDE.md` | "When to Just Do It" section |
| `6-roadmap/research/superintelligence-protocol/decision-framework.md` | Detailed framework |
| `.autonomous/prompts/` | Prompt versions |

---

## 8. Architecture Documentation Duplication

**Engine/Project split documented in:**

| File | Content |
|------|---------|
| `CLAUDE.md` | Brief mention |
| `STRUCTURAL_ISSUES_MASTER_LIST.md` | Detailed analysis |
| `plans/active/engine-project-boundary-plan/epic.md` | Plan documentation |
| Multiple scout reports | Analysis findings |

---

## 9. SSOT Documentation (Meta!)

**SSOT concept itself is now being documented in:**

| File | Content |
|------|---------|
| This file | SSOT violations for documentation |
| `ssot-*.md` files (10 files) | Various SSOT analyses |
| Future: Will need consolidation |

**Irony:** We're creating documentation about documentation duplication.

---

## 10. Getting Started / Onboarding

**Onboarding docs in multiple places:**

| File | Content |
|------|---------|
| `README.md` | Basic setup |
| `CLAUDE.md` | Comprehensive guide |
| `AGENT_CONTEXT.md` | Quick start |
| `6-roadmap/research/` | Research context |

---

## 11. API/Integration Documentation

**Integration docs scattered:**

| File | Content |
|------|---------|
| `CLAUDE.md` | MCP integration notes |
| `.mcp.json` | MCP server config |
| `2-engine/.autonomous/` | Engine-specific integrations |
| Various `INTEGRATION.md` files | Per-integration docs |

---

## Documentation Statistics

| Metric | Count |
|--------|-------|
| Total documentation files | 150+ |
| Major duplications | 11 |
| Estimated redundant lines | 3,000+ |
| Files containing skill docs | 5 |
| Files containing template docs | 4 |
| Files containing RALF docs | 5+ |

---

## Recommendations for SSOT

### 1. Create Documentation Hierarchy

```
docs/
├── README.md                 # Entry point, links to others
├── CLAUDE.md                 # Operational guide (for AI)
├── USER.md                   # User guide (for humans)
├── ARCHITECTURE.md           # System architecture
├── REFERENCE/
│   ├── commands.md           # All bb5 commands
│   ├── skills.md             # Skill system (consolidated)
│   ├── templates.md          # Template system
│   └── api.md                # API integrations
└── RESEARCH/                 # Research docs (superintelligence-protocol)
```

### 2. Consolidate Skill Documentation
**Canonical Source:** `docs/REFERENCE/skills.md`
- Merge skill-selection.yaml docs
- Merge skill-metrics.yaml docs
- Remove from CLAUDE.md (reference only)

### 3. Consolidate Template Documentation
**Canonical Source:** `docs/REFERENCE/templates.md`
- Merge template-system-guide.md
- Remove inline docs from scripts (reference only)

### 4. Consolidate RALF Documentation
**Canonical Source:** `docs/ARCHITECTURE.md#ralf`
- Research stays in `6-roadmap/research/`
- Operational docs in ARCHITECTURE.md
- Prompts reference architecture, don't duplicate

### 5. Auto-Generate Command Reference
**From:** `bin/bb5-*` scripts
- Parse help text from scripts
- Generate `docs/REFERENCE/commands.md`
- Single source: scripts themselves

---

## Critical Files Requiring Immediate Attention

1. `CLAUDE.md` - Too long (2,000+ lines), needs splitting
2. `operations/skill-selection.yaml` - Docs should be in docs/
3. `.docs/template-system-guide.md` - Merge into reference docs
4. Multiple `AGENT_CONTEXT.md` files - Consolidate
5. Research docs - Keep separate but cross-reference

---

## Task Creation Checklist

- [ ] TASK-SSOT-012: Split CLAUDE.md into focused documents
- [ ] TASK-SSOT-013: Consolidate skill documentation
- [ ] TASK-SSOT-014: Consolidate template documentation
- [ ] TASK-SSOT-015: Create docs/ directory structure
- [ ] TASK-SSOT-016: Auto-generate command reference
- [ ] TASK-SSOT-017: Cross-reference research docs
- [ ] TASK-SSOT-018: Remove duplicate onboarding docs
