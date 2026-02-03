# IMP-1769903005: Enforce Template File Naming Convention

**Type:** implement
**Priority:** medium
**Category:** guidance
**Source Learning:** L-1769813746-002, L-1769859012-002, L-1769861639-004
**Status:** pending
**Created:** 2026-02-01T13:30:00Z

---

## Objective

Establish and enforce a template file naming convention using `.template` extension to prevent syntax errors and confusion.

## Problem Statement

Template files cause confusion and false bug reports:
- Template placeholders like `{SERVICE_LOWER}` look like syntax errors
- Python files with template syntax break linters
- Time wasted investigating "bugs" that are features
- No clear convention for template files

## Success Criteria

- [ ] All template files use `.template` extension
- [ ] Existing template files renamed
- [ ] Pre-commit hook to catch new violations
- [ ] Documentation of template naming convention
- [ ] References updated to new names

## Approach

1. Audit all template files in codebase
2. Rename files to use `.template` extension
3. Update all references to template files
4. Create pre-commit hook
5. Document convention in NAMING.md

## Files to Modify

- `2-engine/tools/integrations/_template/` - Rename files
- `.templates/` - Update naming convention
- `2-engine/.autonomous/hooks/pre-commit` (add check)
- `_NAMING.md` - Document convention

## Related Learnings

- run-1769813746: "Template Directory Documentation"
- run-1769859012: "Distinguish Real Bugs from Expected Patterns"
- run-1769861639: "Template Files Have Expected Syntax Errors"

## Estimated Effort

35 minutes

## Acceptance Criteria

- [ ] All template files renamed with `.template` extension
- [ ] Pre-commit hook blocks non-conforming files
- [ ] Documentation updated
- [ ] All references updated
- [ ] No template files with code extensions remain
