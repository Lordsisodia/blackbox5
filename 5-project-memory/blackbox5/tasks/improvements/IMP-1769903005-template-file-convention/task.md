# IMP-1769903005: Enforce Template File Naming Convention

**Type:** implement
**Priority:** medium
**Category:** guidance
**Source Learning:** L-1769813746-002, L-1769859012-002, L-1769861639-004
**Status:** completed
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

- [x] All template files use `.template` extension
- [x] Existing template files renamed
- [x] Pre-commit hook to catch new violations
- [x] Documentation of template naming convention
- [x] References updated to new names

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

## Implementation Summary (2026-02-12)

**Completed:**

1. **Template File Audit** ✅
   - Identified 23 template files with placeholder syntax
   - Found in: `_template/tasks/working/_template/`, `_template/blackbox/_template/`
   - Template patterns: `{...}`, `<...>` placeholders

2. **Template File Renaming** ✅
   - Renamed 23 files to use `.template` extension
   - Categories:
     - Task templates: `task.md.template`
     - Agent templates: `agent.md.template`, `prompt.md.template`
     - Plan templates: 18 files across `.plans/_template/`
   - All files renamed using `git mv` to preserve history

3. **Script Updates** ✅
   - Updated `new-task.sh`: Reference `task.md.template`
   - Updated `new-agent.sh`: Strip `.template` extension when copying
   - Updated `new-plan.sh`: Strip `.template` extension when copying
   - Scripts now correctly handle `.template` files

4. **Pre-commit Hook Enhancement** ✅
   - Added new template placeholder patterns:
     - Task templates: `{Task Name}`, `{YYYY-MM-DD}`, `{Agent Name}`, etc.
     - Agent templates: `<agent-name>`, `<agent-id>`, etc.
     - Plan templates: `<short title>`, `<YYYY-MM-DD HH:MM>`, etc.
   - Added exclusions for:
     - Documentation files (NAMING.md, README.md, etc.)
     - Executable scripts in template directories
   - Hook now blocks commits of non-conforming template files

5. **Documentation Update** ✅
   - Updated `NAMING.md` with comprehensive template documentation
   - Added "Common Template Placeholders" section
   - Documented all template patterns used across the system
   - Added examples of correct vs incorrect naming

6. **Git Commit** ✅
   - Committed with message: `IMP-1769903005: Enforce Template File Naming Convention`
   - 28 files changed, 68 insertions(+), 4 deletions(-)
   - All changes preserve git history via renames

**Results:**
- ✅ All template files now use `.template` extension
- ✅ Pre-commit hook prevents future violations
- ✅ Documentation is comprehensive and up-to-date
- ✅ Scripts correctly handle `.template` files
- ✅ No false positives from documentation or executable scripts

**Benefits:**
- Prevents false bug reports about syntax errors
- Reduces confusion when working with templates
- Improves linter and static analysis tool behavior
- Provides clear, enforceable naming convention

**Files Modified:**
- 23 template files renamed
- 3 scripts updated (new-task.sh, new-agent.sh, new-plan.sh)
- 1 pre-commit hook enhanced
- 1 documentation file updated (NAMING.md)

## Acceptance Criteria

- [x] All template files renamed with `.template` extension
- [x] Pre-commit hook blocks non-conforming files
- [x] Documentation updated
- [x] All references updated
- [x] No template files with code extensions remain
