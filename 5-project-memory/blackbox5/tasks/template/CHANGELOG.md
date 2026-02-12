# Changelog: {TASK_ID}

**Task:** {TASK_TITLE}
**Completed:** {TIMESTAMP}
**Executor:** {AGENT_NAME}

---

## Summary

{ONE_OR_TWO_SENTENCE_SUMMARY_OF_WHAT_CHANGED}

---

## Added

### New Files

- **{FILE_PATH}** - {DESCRIPTION_OF_WHAT_THIS_FILE_CONTAINS}

### New Features

- **{FEATURE_NAME}** in `{FILE_PATH}`
  - Description: {WHAT_IT_DOES}
  - Impact: {WHY_THIS_MATTERS}
  - Lines added: {NUMBER}

- **{FEATURE_NAME}** in `{FILE_PATH}`
  - Description: {WHAT_IT_DOES}
  - Impact: {WHY_THIS_MATTERS}
  - Lines added: {NUMBER}

### New Functions/Methods

- **{FUNCTION_NAME}** in `{FILE_PATH}`
  - Purpose: {WHAT_IT_DOES}
  - Parameters: {INPUTS}
  - Returns: {OUTPUTS}
  - Lines added: {NUMBER}

---

## Changed

### Modified Files

- **{FILE_PATH}**
  - **Before:** {BRIEF_DESCRIPTION_OF_PREVIOUS_STATE}
  - **After:** {BRIEF_DESCRIPTION_OF_NEW_STATE}
  - **Lines changed:** {ADDED}/{DELETED}/{MODIFIED}
  - **Impact:** {WHY_THIS_CHANGE_MATTERS}

  ```diff
  + {ADDED_LINE}
  - {REMOVED_LINE}
  ~ {MODIFIED_LINE}
  ```

- **{FILE_PATH}**
  - **Before:** {BRIEF_DESCRIPTION_OF_PREVIOUS_STATE}
  - **After:** {BRIEF_DESCRIPTION_OF_NEW_STATE}
  - **Lines changed:** {ADDED}/{DELETED}/{MODIFIED}
  - **Impact:** {WHY_THIS_CHANGE_MATTERS}

  ```diff
  + {ADDED_LINE}
  - {REMOVED_LINE}
  ~ {MODIFIED_LINE}
  ```

### Refactored Functions

- **{FUNCTION_NAME}** in `{FILE_PATH}`
  - **Why:** {REASON_FOR_REFACTORING}
  - **Changes:** {WHAT_WAS_CHANGED}
  - Impact: {PERFORMANCE_OR_MAINTAINABILITY_IMPROVEMENT}

---

## Fixed

### Bug Fixes

- **{BUG_DESCRIPTION}** in `{FILE_PATH}`
  - **Issue:** {WHAT_WAS_WRONG}
  - **Root cause:** {WHY_IT_WAS_HAPPENING}
  - **Fix:** {HOW_IT_WAS_FIXED}
  - **Test case:** {HOW_TO_VERIFY_FIX}

- **{BUG_DESCRIPTION}** in `{FILE_PATH}`
  - **Issue:** {WHAT_WAS_WRONG}
  - **Root cause:** {WHY_IT_WAS_HAPPENING}
  - **Fix:** {HOW_IT_WAS_FIXED}
  - **Test case:** {HOW_TO_VERIFY_FIX}

### Performance Improvements

- **{IMPROVEMENT_DESCRIPTION}** in `{FILE_PATH}`
  - **Before:** {OLD_PERFORMANCE_METRIC}
  - **After:** {NEW_PERFORMANCE_METRIC}
  - **Improvement:** {PERCENTAGE_OR_AMOUNT_BETTER}
  - **Technique:** {OPTIMIZATION_APPLIED}

---

## Removed

### Deleted Files

- **{FILE_PATH}** - {WHY_IT_WAS_DELETED}

### Deleted Functions/Methods

- **{FUNCTION_NAME}** in `{FILE_PATH}`
  - **Why deleted:** {REASON}
  - **Replacement:** {WHAT_TO_USE_INSTEAD}

### Deprecated Code

- **{FUNCTION/FEATURE}** in `{FILE_PATH}`
  - **Status:** Deprecated
  - **Removal date:** {WHEN_IT_WILL_BE_FULLY_REMOVED}
  - **Migration guide:** {HOW_TO_UPDATE_CODE}

---

## Documentation Updates

- **Updated:** `{FILE_PATH}` - {WHAT_CHANGED}
- **Created:** `{FILE_PATH}` - {WHAT_IT_CONTAINS}
- **Deprecated:** `{FILE_PATH}` - {WHY_NO_LONGER_NEEDED}

### README Changes

- Added section: {SECTION_TITLE}
- Updated: {WHAT_WAS_CHANGED}

### API Documentation

- Added endpoint: {ENDPOINT}
- Updated parameter: {PARAMETER}
- Removed deprecated: {WHAT_WAS_REMOVED}

---

## Configuration Changes

### Environment Variables

- **{VARIABLE_NAME}**
  - **Default:** {NEW_VALUE}
  - **Previous:** {OLD_VALUE}
  - **Purpose:** {WHY_THIS_CHANGED}
  - **Impact:** {AFFECTED_COMPONENTS}

### Configuration Files

- **{CONFIG_FILE}**
  - **Section:** {SECTION_NAME}
  - **Change:** {WHAT_CHANGED}
  - **Reason:** {WHY_IT_WAS_CHANGED}

---

## Database Changes

### Schema Changes

- **Table:** `{TABLE_NAME}`
  - **Added column:** `{COLUMN_NAME}` - {TYPE} - {PURPOSE}
  - **Modified column:** `{COLUMN_NAME}` - {WHAT_CHANGED}
  - **Dropped column:** `{COLUMN_NAME}` - {REASON}
  - **Index added:** `{INDEX_NAME}` on {COLUMNS}
  - **Index dropped:** `{INDEX_NAME}` - {REASON}

### Data Migrations

- **Migration script:** `{SCRIPT_PATH}`
  - **Description:** {WHAT_IT_DOES}
  - **Impact:** {NUMBER_OF_ROWS_AFFECTED}
  - **Rollback script:** {HOW_TO_UNDO}

---

## Dependency Updates

### Added Dependencies

- **{PACKAGE_NAME}** ({VERSION})
  - **Purpose:** {WHY_NEEDED}
  - **Usage:** {WHERE_IT'S_USED}

### Updated Dependencies

- **{PACKAGE_NAME}** {OLD_VERSION} → {NEW_VERSION}
  - **Breaking changes:** {ANY_BREAKING_CHANGES}
  - **Notable features:** {NEW_FEATURES}

### Removed Dependencies

- **{PACKAGE_NAME}**
  - **Reason:** {WHY_NO_LONGER_NEEDED}
  - **Replaced by:** {ALTERNATIVE}

---

## Testing Changes

### New Tests

- **{TEST_NAME}** in `{TEST_FILE}`
  - **Tests:** {WHAT_IT_TESTS}
  - **Coverage:** {WHAT_CODE_IT_COVERS}

### Modified Tests

- **{TEST_NAME}** in `{TEST_FILE}`
  - **Changed:** {WHAT_WAS_MODIFIED}
  - **Reason:** {WHY_IT_WAS_CHANGED}

### Removed Tests

- **{TEST_NAME}** in `{TEST_FILE}`
  - **Reason:** {WHY_IT_WAS_REMOVED}

---

## Breaking Changes

⚠️ **Breaking Change:** {DESCRIPTION}

- **Impact:** {WHO_IS_AFFECTED}
- **Migration:** {HOW_TO_UPDATE_CODE}
- **Timeline:** {WHEN_IT_WAS_INTRODUCED}

---

## Internal Changes

### Code Quality

- Improved code formatting
- Added type hints
- Improved error handling
- Refactored for maintainability

### Performance

- Optimized database queries
- Reduced memory usage
- Improved caching strategy
- Parallelized operations

### Security

- Added input validation
- Improved error messages (avoid info leakage)
- Updated dependencies for security patches
- Added rate limiting

---

## Migration Guide

If you're upgrading from the previous version, here's what you need to do:

1. **{STEP_1}**
   - **Why:** {REASON}
   - **How:** {INSTRUCTIONS}

2. **{STEP_2}**
   - **Why:** {REASON}
   - **How:** {INSTRUCTIONS}

3. **{STEP_3}**
   - **Why:** {REASON}
   - **How:** {INSTRUCTIONS}

---

## Related Issues and PRs

- **Issue:** {ISSUE_NUMBER} - {ISSUE_TITLE}
- **PR:** {PR_NUMBER} - {PR_TITLE}
- **Related task:** {TASK_ID}

---

## Rollback Information

If you need to rollback this change:

1. **Git revert:** `git revert {COMMIT_HASH}`
2. **Database:** Run rollback script: `{ROLLBACK_SCRIPT}`
3. **Configuration:** Revert config changes in `{CONFIG_FILE}`
4. **Manual steps:** {ANY_MANUAL_STEPS_NEEDED}

---

## Statistics

- **Total files changed:** {NUMBER}
- **Lines added:** {NUMBER}
- **Lines removed:** {NUMBER}
- **Net change:** {+/- NUMBER} lines
- **Tests added:** {NUMBER}
- **Tests modified:** {NUMBER}
- **Tests removed:** {NUMBER}
- **Documentation pages:** {NUMBER}

---

## Notes

{ANY_ADDITIONAL_NOTES_ABOUT_THE_CHANGES}

{KNOWN_ISSUES_OR_LIMITATIONS}

{FOLLOW_UP_TASKS_NEEDED}
