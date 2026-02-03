# Decisions - TASK-1769913001

## Decision 1: Class-Based Validator Design

**Context:** Need reusable validation library for both Planner and Executor

**Selected:** Class-based `PlanValidator` with configurable paths

**Rationale:**
- Reusable across different agents (Planner, Executor)
- Configurable project_root and roadmap_path
- Easy to extend with new validation rules
- Clear separation of concerns (parsing, validation, reporting)
- Follows pattern of existing libraries (duplicate_detector.py)

**Alternatives Considered:**
1. Function-based design - Rejected: Less extensible, harder to maintain state
2. Standalone script - Rejected: Not reusable in Python workflows
3. Shell script - Rejected: Limited error handling, no YAML parsing

**Reversibility:** LOW - Well-structured, easy to modify or extend

---

## Decision 2: Multi-Strategy Path Resolution

**Context:** Plans reference files with inconsistent path formats

**Selected:** Try multiple path resolution strategies in order

**Rationale:**
- Plans use various formats: blackbox5/, /, relative, absolute
- Can't control plan author behavior (historical data)
- Trying all strategies is more robust than enforcing one format
- Performance impact negligible (file system checks are fast)

**Implementation:**
```python
possible_paths = [
    project_root / file_path,  # Direct relative
    project_root / "blackbox5" / file_path,  # Handle prefix
    Path(file_path),  # Absolute as written
]
```

**Alternatives Considered:**
1. Enforce single format - Rejected: Can't change historical plans
2. Regex normalization - Rejected: Complex, error-prone
3. Config-only - Rejected: Doesn't solve existing inconsistency

**Reversibility:** LOW - Easy to add/remove strategies if needed

---

## Decision 3: Error vs Warning Severity Levels

**Context:** Not all validation issues should block execution

**Selected:** Two-tier system (errors block, warnings don't)

**Rationale:**
- **Errors (block execution):**
  - Missing files (can't implement without them)
  - Self-dependencies (logical impossibility)
  - Circular dependencies (deadlock)
- **Warnings (review only):**
  - Stale problem statements (may still be valid)
  - Old plans (> 30 days) (may be intentionally slow-moving)
  - Missing dependencies in STATE.yaml (data issue, not logic issue)

**Alternatives Considered:**
1. Block everything - Rejected: Too restrictive, false positives
2. No blocking - Rejected: Defeats purpose of validation
3. Three-tier (error/warning/info) - Rejected: Unnecessary complexity

**Reversibility:** MEDIUM - Requires updating workflow integration

---

## Decision 4: JSON Output Option

**Context:** Need machine-readable output for CI/CD integration

**Selected:** Add --json flag for structured output

**Rationale:**
- Human-readable output (default): Good for manual use
- JSON output (flag): Good for automation
- Enables CI/CD pipeline integration
- Easy to parse in Python scripts
- Industry standard for tool output

**Implementation:**
```bash
# Human-readable (default)
validator.py plan.md

# Machine-readable (automation)
validator.py --json plan.md | jq '.valid'
```

**Alternatives Considered:**
1. Only JSON - Rejected: Poor user experience for manual use
2. YAML output - Rejected: Less common for tool integration
3. Custom format - Rejected: Reinventing the wheel

**Reversibility:** LOW - Easy to add/remove output formats

---

## Decision 5: Duplicate Task Handling

**Context:** TASK-1769912002 is duplicate of completed TASK-1769908000

**Selected:** Move duplicate to completed/ with status note

**Rationale:**
- Preserves task history (shows it was detected)
- Prevents re-execution of completed work
- Logs duplicate detection for metrics
- Signals Planner that duplicate was detected
- Faster than waiting for Planner to clean up

**Alternatives Considered:**
1. Delete duplicate - Rejected: Loses history
2. Rename to .duplicate - Rejected: Non-standard
3. Skip only, don't move - Rejected: Clutters active/ directory
4. Ask Planner - Rejected: Wastes time (obvious duplicate)

**Reversibility:** LOW - Easy to restore from git if needed

---

## Decision 6: Documentation Scope

**Context:** Balance comprehensive docs with maintenance burden

**Selected:** Single comprehensive guide (350+ lines)

**Rationale:**
- All information in one place
- Covers all use cases (CLI, Python, integration)
- Includes troubleshooting (prevents support burden)
- Examples for all roles (plan authors, planner, executor)
- Self-contained (no external dependencies for understanding)

**Alternatives Considered:**
1. Minimal README - Rejected: Insufficient for complex tool
2. Multiple files - Rejected: Harder to navigate
3. Inline comments only - Rejected: Not accessible to users

**Reversibility:** LOW - Documentation is additive, not breaking

---

## Decision 7: Pre-Execution Research Enforcement

**Context:** Task requires pre-execution research but no enforcement mechanism exists yet

**Selected:** Perform research manually and document in THOUGHTS.md

**Rationale:**
- Follows best practices (IMP-1769903002, though not yet fully enforced)
- Validates assumptions before implementation
- Catches duplicate immediately (saved 35+ minutes)
- Documents research for future reference
- Leads by example (research quality demonstration)

**Note:** This task demonstrates the value of IMP-1769903002 (Mandatory Pre-Execution Research), which was completed in TASK-1769908000.

**Reversibility:** N/A - Process decision, not code

---

## Decision 8: Testing Strategy

**Context:** Need to validate validator works correctly without test framework

**Selected:** Manual testing on real plans with expected outcomes

**Rationale:**
- Real plans have real-world complexity
- Expected outcomes are known (unimplemented plans should fail)
- No test framework dependency needed
- Immediate feedback on correctness
- Tests documentation and examples simultaneously

**Test Cases:**
1. PLAN-003 (unimplemented) → Should fail (missing files) ✅
2. PLAN-002 (completed, files moved) → Should fail (missing files) ✅
3. --all flag → Should validate all ready_to_start ✅

**Alternatives Considered:**
1. Unit tests - Rejected: Overkill for this task, no framework set up
2. Mock plans - Rejected: Doesn't test real-world complexity
3. No testing - Rejected: Risk of bugs in validator

**Reversibility:** LOW - Tests are manual, don't affect codebase

---

## Summary of Key Decisions

| Decision | Impact | Risk | Reversibility |
|----------|--------|------|---------------|
| Class-based validator | High reuse | LOW | LOW |
| Multi-strategy paths | High robustness | LOW | LOW |
| Error/warning tiers | Balanced blocking | MEDIUM | MEDIUM |
| JSON output option | CI/CD ready | LOW | LOW |
| Duplicate handling | Clear history | LOW | LOW |
| Comprehensive docs | High usability | LOW | LOW |
| Manual research | Best practice | NONE | N/A |
| Manual testing | Immediate feedback | LOW | LOW |

**Overall Risk:** LOW - All decisions are reversible and well-considered
**Overall Impact:** HIGH - Significantly improves plan quality and system efficiency
