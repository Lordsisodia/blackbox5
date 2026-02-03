# DECISIONS - TASK-1738334891

**Task:** Archive Duplicate Documentation Files
**Date:** 2026-01-31T05:48:33Z

---

## Decision 1: Focus on Documentation Duplicates

**Context:** PLAN-006 identified multiple redundancy types, but some were already resolved.

**Options Considered:**
- A) Address all PLAN-006 items (event bus, boot files, docs, references)
- B) Focus only on documentation duplicates (remaining work)
- C) Skip PLAN-006 entirely and find new work

**Selected Option:** B

**Rationale:**
- Event bus already consolidated (only 1 exists)
- Boot files already consolidated (none found)
- Documentation duplicates clearly identified and ready for archival
- Other items (templates, project memory) are intentional duplicates

**Reversibility:** LOW - Files can be moved back from archive if needed

---

## Decision 2: Canonical Location Selection

**Context:** Research files existed in 3 locations with identical content.

**Options Considered:**
- A) Keep `1-docs/development/reference/research/` as canonical
- B) Keep `2-engine/.autonomous/prompt-progression/research/` as canonical
- C) Keep `1-docs/01-theory/05-research/` as canonical

**Selected Option:** C

**Rationale:**
- `1-docs/01-theory/` is the proper location for theory and research documentation
- Follows the documentation hierarchy (theory > development reference > engine research)
- Most consistent with blackbox5 documentation structure

**Reversibility:** MEDIUM - Would require moving files back and updating references

---

## Decision 3: Archive vs Delete

**Context:** What to do with duplicate files once identified.

**Options Considered:**
- A) Delete duplicates permanently
- B) Move to archive with preserved structure
- C) Leave in place and add symbolic links

**Selected Option:** B

**Rationale:**
- Archive preserves history for rollback
- Preserved directory structure makes restoration easy
- Git can track the moves as renames
- No risk of permanent data loss

**Reversibility:** LOW - Files in archive can be moved back to original locations

---

## Decision 4: Automation Strategy

**Context:** 172 files need to be moved manually or via script.

**Options Considered:**
- A) Manual file-by-file moves
- B) Bash script with hardcoded paths
- C) Python script with MD5 hash analysis

**Selected Option:** C

**Rationale:**
- MD5 hash analysis ensures exact duplicates only
- Python script is more maintainable and extensible
- Can easily exclude certain directories (templates, active projects)
- Automated approach reduces human error

**Reversibility:** LOW - Script can be re-run or modified if needed

---

## Decision 5: Exclusion Criteria

**Context:** Some files appear duplicated but serve different purposes.

**Options Considered:**
- A) Archive all duplicates regardless of location
- B) Exclude only `5-project-memory/siso-internal/`
- C) Exclude templates and active project memories

**Selected Option:** C

**Rationale:**
- `_template/` files are meant to be copied to new projects
- `siso-internal/` is an active project with its own memory structure
- `pytest_cache/` READMEs are generated files
- Archiving these would break expected functionality

**Reversibility:** LOW - Excluded files remain in place, no action needed

---

## Summary

| Decision | Choice | Risk | Reversibility |
|----------|--------|------|---------------|
| Focus Area | Documentation only | Low | Low |
| Canonical Location | 1-docs/01-theory/ | Medium | Medium |
| Action Method | Archive with structure | Low | Low |
| Automation | Python script | Low | Low |
| Exclusions | Templates & active projects | Low | Low |

**Overall Risk Assessment:** LOW - All decisions preserve data and allow rollback.
