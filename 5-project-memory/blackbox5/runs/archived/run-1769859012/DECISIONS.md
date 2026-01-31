# DECISIONS - Loop 36

## Decision 1: Skip Full PLAN-004 Implementation

**Context:** PLAN-004 assumed broken import paths across the codebase based on an outdated directory structure.

**Decision:** Audit first, then fix only actual issues found.

**Reversibility:** HIGH - Can always return to PLAN-004 if needed.

**Rationale:** The actual codebase structure differs from what PLAN-004 assumed. Pre-execution research revealed the plan was based on outdated information.

## Decision 2: Fix Only Actual Syntax Errors

**Context:** Syntax audit revealed only 2 real bugs in 2003 Python files.

**Decision:** Fix the two syntax errors found:
1. test_logging.py:572 - Fixed typo `log_file=log_file=log_file2` → `log_file=log_file2`
2. github-actions/manager.py:476 - Added missing `async` keyword

**Reversibility:** MEDIUM - Changes are minimal and targeted. Can be reverted with git if needed.

**Rationale:** Don't over-engineer a solution for a problem that doesn't exist at the scale assumed.
