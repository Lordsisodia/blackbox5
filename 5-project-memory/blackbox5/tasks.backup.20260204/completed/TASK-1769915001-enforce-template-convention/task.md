# TASK-1769915001: Enforce Template File Naming Convention

**Type:** implement
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T02:35:00Z
**Source:** IMP-1769903005

## Objective

Implement and enforce the template file naming convention to prevent confusion and reduce false bug reports about template files that appear to be "real" files but are actually templates.

## Context

Template files (ending in `.template`) cause confusion because:
1. They appear in file searches and grep results
2. Users report "bugs" when they find discrepancies
3. Time is wasted investigating "issues" that are actually template features
4. New team members don't understand the template system

**Evidence from Learnings:**
- 6 mentions in learning files about template confusion
- IMP-1769903005 created but not yet implemented
- Pattern: Template files consistently cause confusion

## Success Criteria

- [ ] Template file naming convention documented
- [ ] Convention added to .docs/ system for visibility
- [ ] Templates renamed to follow convention (if needed)
- [ ] Template system guide created or updated
- [ ] CLAUDE.md updated with template handling rules

## Approach

1. **Define Convention:**
   - Standardize on `.template` suffix (already in use)
   - Define naming pattern: `[filename].template.md`
   - Document when to use templates vs real files

2. **Document Convention:**
   - Create or update `.docs/template-system-guide.md`
   - Add to STATE.yaml under documentation patterns
   - Include examples of proper template usage

3. **Update Agent Instructions:**
   - Add template handling rules to CLAUDE.md
   - Specify: "Always check for .template suffix before reporting bugs"
   - Add to file discovery workflow

4. **Validate Existing Templates:**
   - Audit all .template files in project
   - Ensure they follow convention
   - Rename any that don't comply

5. **Add Warning Headers:**
   - Ensure all templates have clear warning headers
   - Example: "# THIS IS A TEMPLATE - DO NOT EDIT DIRECTLY"

## Files to Modify

- `.docs/template-system-guide.md`: Create or update template system documentation
- `STATE.yaml`: Add template convention to documentation patterns
- `~/.claude/CLAUDE.md`: Add template handling rules
- All `.template` files: Ensure consistent naming and warnings

## Template Files to Audit

- `.templates/root/*.template` (8 files)
- `.templates/decisions/*.template` (3 files)
- `.templates/research/*.template` (5 files)
- `.templates/epic/*.template` (7 files)
- `.templates/tasks/*.template` (3 files)

Total: ~26 template files

## Notes

- **Priority:** MEDIUM - Reduces confusion but not critical
- **Effort:** LOW (35 minutes) - Documentation and naming only
- **Risk:** LOW - No code changes, documentation only
- **Impact:** Reduces false bug reports, improves onboarding

## Expected Outcomes

1. Fewer "bug reports" about template files
2. Faster onboarding for new team members
3. Less time wasted investigating template discrepancies
4. Clear understanding of template vs real file distinction

## Validation

After completion, verify:
1. All template files follow naming convention
2. Documentation is clear and accessible
3. CLAUDE.md includes template handling rules
4. Template system is discoverable (docs/index or similar)

## Related Improvements

- IMP-1769903005: Template file convention (this task)
- Connected to documentation freshness (Run 36 analysis found 100% fresh)
