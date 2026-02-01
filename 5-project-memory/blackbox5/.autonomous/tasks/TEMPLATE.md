# Task Template

**Task ID:** TASK-[timestamp]
**Type:** implement | fix | refactor | analyze | organize | research
**Priority:** critical | high | medium | low
**Status:** pending
**Created:** YYYY-MM-DDTHH:MM:SSZ
**Estimated Lines:** [NUMBER] (REQUIRED - see Estimation Formula below)

## Lines-Per-Minute Estimation Formula

**Based on executor throughput analysis (runs 56-62):**
- Mean throughput: 271 lines/min
- Standard deviation: 48 lines/min
- Coefficient of variation: 18% (excellent consistency)

**Formula:**
```
Estimated Minutes = Estimated Lines / 270

Where Estimated Lines = spec_lines + code_lines + docs_lines
```

**Accuracy:** 9% error vs 31% error (time-based) - 71% improvement

**How to Estimate Lines:**
1. **Spec Lines:** ~400 lines (feature specification)
2. **Code Lines:** Count of files × avg lines per file (typically 200-400 lines per file)
3. **Docs Lines:** ~500 lines (user guide, API reference, examples)
4. **Total:** Sum of above = Estimated Lines

**Example:**
```
Feature: API Gateway (3 libraries × 300 lines + 1 spec × 400 lines + 1 doc × 500 lines)
Estimated Lines: 900 + 400 + 500 = 1,800 lines
Estimated Minutes: 1,800 / 270 = 6.7 minutes
Actual Duration: 7.2 minutes (7% error) ✅
```

**Reference:** knowledge/analysis/planner-insights.md (Loop 24-25 analysis)

## Objective
[Clear, concise statement of what needs to be done]

## Context
[Why this task matters - 2-3 sentences]
[Link to any analysis docs in knowledge/analysis/]

## Success Criteria
- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]
- [ ] [Specific, measurable criterion 3]

## Approach
[How to implement this task]
[Reference any relevant skills in 2-engine/.autonomous/skills/]

## Files to Modify
- `[path/to/file.ext]`: [what to change]
- `[path/to/file.ext]`: [what to change]

## Dependencies
- [ ] TASK-XXX (if any)

## Notes
[Any warnings, gotchas, or additional context]
