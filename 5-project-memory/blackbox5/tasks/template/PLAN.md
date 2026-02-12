# Implementation Plan: {TASK_ID}

**Created:** {TIMESTAMP}
**Last Updated:** {LAST_UPDATE}
**Status:** {DRAFT/APPROVED/IN_PROGRESS/COMPLETED}

---

## Overview

**Task:** {TASK_TITLE}
**Objective:** {CLEAR_STATEMENT_OF_OBJECTIVE}
**Estimated Duration:** {ESTIMATED_TIME}

---

## Phase 1: Preparation

### 1.1 Understand the Task

- [ ] Read task description and context
- [ ] Review related documentation
- [ ] Understand success criteria
- [ ] Identify constraints and requirements

**Estimated Time:** {TIME}

**Deliverables:**
- Understanding confirmed in THOUGHTS.md
- Questions raised (if any)

### 1.2 Environment Setup

- [ ] Verify required tools and dependencies
- [ ] Set up working directory
- [ ] Create run folder with templates (handled by SessionStart hook)
- [ ] Configure any required services

**Estimated Time:** {TIME}

**Deliverables:**
- Environment ready for implementation
- All dependencies installed/verified

---

## Phase 2: Analysis

### 2.1 Codebase Exploration

- [ ] Locate relevant files and routes
- [ ] Understand existing architecture
- [ ] Identify integration points
- [ ] Review similar implementations

**Estimated Time:** {TIME}

**Deliverables:**
- Map of relevant files and their purposes
- Notes on architecture patterns

### 2.2 Impact Assessment

- [ ] Identify what will change
- [ ] Identify potential side effects
- [ ] Plan testing strategy
- [ ] Define rollback plan

**Estimated Time:** {TIME}

**Deliverables:**
- List of files to modify
- Risk assessment
- Test plan

---

## Phase 3: Implementation

### 3.1 Core Implementation

- [ ] Implement {FEATURE_1}
- [ ] Implement {FEATURE_2}
- [ ] Implement {FEATURE_3}

**Estimated Time:** {TIME}

**Files to Modify:**
- `{FILE_PATH}`: {WHAT_TO_CHANGE}
- `{FILE_PATH}`: {WHAT_TO_CHANGE}

**Notes:**
{ANY_IMPORTANT_IMPLEMENTATION_NOTES}

### 3.2 Integration

- [ ] Connect {COMPONENT_1}
- [ ] Connect {COMPONENT_2}
- [ ] Verify data flow

**Estimated Time:** {TIME}

**Integration Points:**
- **{COMPONENT}:** {HOW_TO_INTEGRATE}

### 3.3 Error Handling

- [ ] Add error handling for {SCENARIO_1}
- [ ] Add error handling for {SCENARIO_2}
- [ ] Validate edge cases

**Estimated Time:** {TIME}

---

## Phase 4: Testing

### 4.1 Unit Tests

- [ ] Write test for {FUNCTION_1}
- [ ] Write test for {FUNCTION_2}
- [ ] Run all unit tests

**Estimated Time:** {TIME}

**Test Files:**
- `{TEST_FILE}`: {WHAT_TO_TEST}

### 4.2 Integration Tests

- [ ] Test {INTEGRATION_SCENARIO_1}
- [ ] Test {INTEGRATION_SCENARIO_2}

**Estimated Time:** {TIME}

### 4.3 Manual Verification

- [ ] Verify {MANUAL_CHECK_1}
- [ ] Verify {MANUAL_CHECK_2}
- [ ] Test edge cases

**Estimated Time:** {TIME}

**Verification Checklist:**
- [ ] {CHECK_1}
- [ ] {CHECK_2}
- [ ] {CHECK_3}

---

## Phase 5: Documentation

### 5.1 Code Documentation

- [ ] Add docstrings to functions
- [ ] Add inline comments for complex logic
- [ ] Update README if needed

**Estimated Time:** {TIME}

### 5.2 External Documentation

- [ ] Update {DOC_FILE}
- [ ] Add examples if applicable
- [ ] Document any breaking changes

**Estimated Time:** {TIME}

---

## Phase 6: Validation and Cleanup

### 6.1 Final Verification

- [ ] Run full test suite
- [ ] Verify all success criteria met
- [ ] Check for regressions

**Estimated Time:** {TIME}

### 6.2 Code Cleanup

- [ ] Remove debug code
- [ ] Remove temporary files
- [ ] Format code consistently

**Estimated Time:** {TIME}

### 6.3 Git Commit

- [ ] Stage changes
- [ ] Write clear commit message
- [ ] Commit changes (handled by Stop hook)

**Estimated Time:** {TIME}

**Commit Message Draft:**
```
{TASK_ID}: {COMMIT_MESSAGE_TITLE}

{COMMIT_MESSAGE_BODY}

- Related to: {TASK_ID}
```

---

## Timeline Summary

| Phase | Estimated Time | Actual Time |
|-------|----------------|-------------|
| Phase 1: Preparation | {TIME} | {ACTUAL} |
| Phase 2: Analysis | {TIME} | {ACTUAL} |
| Phase 3: Implementation | {TIME} | {ACTUAL} |
| Phase 4: Testing | {TIME} | {ACTUAL} |
| Phase 5: Documentation | {TIME} | {ACTUAL} |
| Phase 6: Validation | {TIME} | {ACTUAL} |
| **Total** | **{TOTAL_TIME}** | **{ACTUAL_TOTAL}** |

---

## Notes

{ANY_ADDITIONAL_IMPLEMENTATION_NOTES}

{POTENTIAL_RISKS_AND_MITIGATIONS}

{REFERENCES_TO_SIMILAR_IMPLEMENTATIONS}
