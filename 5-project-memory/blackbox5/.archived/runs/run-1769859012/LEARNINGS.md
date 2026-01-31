# LEARNINGS - Loop 36

## Key Learning: Audit Before Implementing

PLAN-004 was based on outdated codebase information. The 1-2 day estimate was for a problem that didn't exist at that scale. Actual fix time: 15 minutes.

**Lesson:** Always verify assumptions about codebase state before implementing plans.

## Key Learning: Distinguish Real Bugs from Expected Patterns

- Template files with `{PLACEHOLDER}` syntax are not bugs
- Python 2 test data files are not bugs
- Real bugs are simple syntax errors that prevent compilation

**Lesson:** Filter out expected patterns when auditing for errors.

## Key Learning: Plans Can Become Stale

PLAN-004 was created when the codebase had different structure. The system has evolved since then.

**Lesson:** Plans need periodic re-validation against current codebase state.
