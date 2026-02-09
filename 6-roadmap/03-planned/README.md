# Planned

> Planned features and improvements

## Overview

This directory contains planned features, improvements, and initiatives that are queued for implementation. Items here have been researched and designed, awaiting scheduling.

## Directory Structure

```
03-planned/
├── q1-2026/       # Q1 2026 plans
├── q2-2026/       # Q2 2026 plans
├── backlog/       # Unscheduled items
├── icebox/        # Low priority/future ideas
└── completed/     # Finished items
```

## Plan Format

```yaml
id: PLAN-XXX
title: "Feature or improvement title"
status: planned | in_progress | completed | cancelled
priority: CRITICAL | HIGH | MEDIUM | LOW
target_quarter: Q1-2026

research_doc: "../01-research/active/research-topic.md"
design_doc: "../02-design/features/feature-design.md"
validation_doc: "../02-validation/test-plans/feature-tests.md"

objective: |
  What this plan will achieve.

success_criteria:
  - Measurable outcome 1
  - Measurable outcome 2

tasks:
  - TASK-001
  - TASK-002

estimated_effort: "X days"
dependencies:
  - Other plans that must complete first
```

## Planning Process

1. **Research** - Documented in 01-research/
2. **Design** - Documented in 02-design/
3. **Validation Plan** - Documented in 02-validation/
4. **Schedule** - Added to appropriate quarter
5. **Execute** - Tasks created and assigned

## Related Documentation

- [../01-research/README.md](../01-research/README.md) - Research
- [../02-design/README.md](../02-design/README.md) - Designs
- [../02-validation/README.md](../02-validation/README.md) - Validation

## Usage

Review quarterly to prioritize and schedule upcoming work.
