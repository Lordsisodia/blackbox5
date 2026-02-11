# Task Time Estimation Guidelines
# SISO-Internal - Operations
# Version: 1.0.0
# Last Updated: 2026-02-09

## Purpose

Provide data-driven guidelines for estimating task completion times in the SISO-Internal project.

## Universal Estimation Multiplier

**All estimates must be multiplied by 1.35x to account for consistent underestimation trends.**

This multiplier corrects for:
- Context switching overhead
- Unforeseen dependencies
- Testing and validation time
- Documentation requirements

### Applying the Multiplier

```
final_estimate = calculated_estimate * 1.35
```

**Example:**
- Baseline calculation: 30 minutes
- With 1.35x multiplier: 30 * 1.35 = 40.5 minutes
- Round to: 40-45 minutes

## Baseline Estimates by Task Type

| Task Type | Min | Baseline | Max | Confidence |
|-----------|-----|----------|-----|------------|
| **analyze** | 5 min | 10 min | 25 min | Medium |
| **implement** | 25 min | 30 min | 45 min | Medium |
| **fix** | 10 min | 15 min | 30 min | Low |
| **organize** | 10 min | 15 min | 25 min | Low |
| **refactor** | 15 min | 25 min | 40 min | Low |
| **documentation** | 10 min | 20 min | 40 min | Low |

## Estimation Formula

```
estimated_minutes = baseline_type * priority_multiplier * complexity_multiplier * 1.35 + buffer
```

### Priority Multipliers

| Priority | Multiplier | Rationale |
|----------|------------|-----------|
| **critical** | 0.8 | Well-defined, focused scope |
| **high** | 0.9 | Clear objectives, few dependencies |
| **medium** | 1.0 | Standard complexity |
| **low** | 1.2 | May require context gathering |

### Complexity Multipliers

| Complexity | Multiplier | Indicators |
|------------|------------|------------|
| **simple** | 0.7 | Single file, straightforward change |
| **standard** | 1.0 | Multiple files, standard patterns |
| **complex** | 1.5 | Cross-system changes, new patterns |
| **unknown** | 2.0 | Research required, high uncertainty |

### Buffer

| Situation | Buffer | When to Use |
|-----------|--------|-------------|
| **no buffer** | 0 min | Well-understood, repetitive task |
| **standard buffer** | 5-10 min | Most tasks |
| **large buffer** | 15-20 min | New task type, high uncertainty |

## Estimation Examples

### Example 1: Simple Analyze Task
```
Task: Analyze current dashboard structure (high priority, simple)
Baseline: 10 min (analyze)
Priority: 10 * 0.9 = 9 min (high priority)
Complexity: 9 * 0.7 = 6.3 min (simple)
1.35x Multiplier: 6.3 * 1.35 = 8.5 min
Buffer: 8.5 + 5 = 13.5 min
Final estimate: 10-15 minutes
```

### Example 2: Standard Implement Task
```
Task: Create new operations dashboard (medium priority, standard)
Baseline: 30 min (implement)
Priority: 30 * 1.0 = 30 min (medium)
Complexity: 30 * 1.0 = 30 min (standard)
1.35x Multiplier: 30 * 1.35 = 40.5 min
Buffer: 40.5 + 10 = 50.5 min
Final estimate: 50-55 minutes
```

### Example 3: Complex Implement Task
```
Task: Implement cross-project synchronization (medium priority, complex)
Baseline: 30 min (implement)
Priority: 30 * 1.0 = 30 min (medium)
Complexity: 30 * 1.5 = 45 min (complex - multiple systems)
1.35x Multiplier: 45 * 1.35 = 60.75 min
Buffer: 60.75 + 15 = 75.75 min
Final estimate: 75-80 minutes
```

## Task Type Guidelines

### Analyze Tasks (5-25 min)

**Characteristics:**
- Read existing code/docs
- Identify patterns or issues
- Document findings
- No code changes required

**Estimation Tips:**
- Simple analysis (single file): 5-10 min
- Standard analysis (2-3 files): 10-15 min
- Comprehensive analysis (5+ files): 15-25 min

**Quick Estimate:** `10 min ± 5 min`

### Implement Tasks (25-45 min)

**Characteristics:**
- Create new files
- Modify existing files
- Integration with existing system
- Testing/validation required

**Estimation Tips:**
- Simple implementation (1 file): 20-30 min
- Standard implementation (2-3 files): 30-40 min
- Complex implementation (4+ files): 40-60 min
- Add 10 min if testing framework involved

**Quick Estimate:** `30 min ± 10 min`

### Fix Tasks (10-30 min)

**Characteristics:**
- Bug fixes
- Error resolution
- Quick patches

**Estimation Tips:**
- Simple fix (known issue): 10-15 min
- Standard fix (investigation needed): 15-25 min
- Complex fix (root cause unknown): 25-30 min

**Quick Estimate:** `15 min ± 10 min`

## File Count Multiplier

For implementation tasks, file count significantly impacts duration:

| Files | Multiplier | Rationale |
|-------|------------|-----------|
| 1 file | 0.7 | Focused change |
| 2-3 files | 1.0 | Standard implementation |
| 4-5 files | 1.3 | Integration overhead |
| 6+ files | 1.5+ | Significant coordination |

## Special Cases

### Documentation Tasks
Use analyze baseline (5-25 min) unless:
- Creating new documentation framework: 30-45 min
- Comprehensive documentation refactor: 45-60 min

### Testing Tasks
- Add test (single): 5-10 min
- Add test suite (multiple): 15-25 min
- Fix failing test: 10-20 min

### Refactoring Tasks
- Simple refactor (rename/extract): 10-15 min
- Medium refactor (restructure): 20-30 min
- Complex refactor (pattern change): 30-45 min

## Common Pitfalls

### Underestimation Causes

1. **Ignoring dependencies:** Add 10-15 min per external dependency
2. **Unclear requirements:** Add 20-30 min for clarification
3. **Testing overhead:** Add 10 min for test creation/execution
4. **Documentation:** Add 5-10 min if documentation required

### Overestimation Causes

1. **Assuming complexity:** Most tasks are simpler than they appear
2. **Padding too much:** Large buffers accumulate unnecessarily
3. **Ignoring templates:** Using templates reduces time by 30-50%

## Estimation Best Practices

1. **Be specific:** Break complex tasks into sub-tasks
2. **Use templates:** Leverage existing templates when available
3. **Consider context:** First task of type takes longer (learning curve)
4. **Track accuracy:** Record estimates vs actuals for calibration
5. **Update baselines:** Revisit these guidelines quarterly
6. **Apply 1.35x multiplier:** Always apply to account for underestimation trend

## Accuracy Tracking

Track estimation accuracy using this formula:

```
accuracy = 1 - (|actual - estimate| / estimate)

Good accuracy: >= 0.8 (within 20%)
Acceptable accuracy: >= 0.6 (within 40%)
Poor accuracy: < 0.6 (more than 40% off)
```

## Quick Reference Card

```
Task Type          Quick Estimate    Range
─────────────────────────────────────────────
Analyze (simple)   10 min           5-15 min
Analyze (standard) 15 min           10-20 min
Analyze (complex)  20 min           15-25 min

Implement (1 file) 25 min           20-30 min
Implement (2-3 files) 35 min       30-40 min
Implement (4+ files) 45 min        40-60 min

Fix (simple)       10 min           5-15 min
Fix (standard)     20 min           15-25 min
Fix (complex)      30 min           25-35 min

Remember: Apply 1.35x multiplier to all estimates!
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-09 | Initial version for SISO-Internal |

## Related Documents

- Task Specification Template: `.templates/tasks/task-specification.md.template`
- Task Completion Template: `.templates/tasks/task-completion.md.template`
