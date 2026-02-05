# TASK-SSOT-013: Split CLAUDE.md into Focused Documents

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #18 - SSOT Documentation Violations

## Objective
Split 2,000+ line CLAUDE.md into focused, single-purpose documents.

## Success Criteria
- [ ] Create docs/ directory structure
- [ ] Extract skill documentation to docs/REFERENCE/skills.md
- [ ] Extract commands to docs/REFERENCE/commands.md
- [ ] Extract RALF docs to docs/ARCHITECTURE.md
- [ ] Keep CLAUDE.md as operational guide only
- [ ] Update all cross-references
- [ ] Remove duplicate content

## Context
CLAUDE.md is 2,000+ lines and contains:
- Operational guide (should stay)
- Skill documentation (duplicate)
- Command reference (should be auto-generated)
- RALF documentation (duplicate)
- Template docs (duplicate)

## Approach
1. Create docs/ directory structure
2. Extract sections to new files
3. Update CLAUDE.md to reference new files
4. Remove duplicate content
5. Update cross-references

## Related Files
- CLAUDE.md
- operations/skill-selection.yaml
- .docs/template-system-guide.md

## Rollback Strategy
Keep full CLAUDE.md backup until split verified.
