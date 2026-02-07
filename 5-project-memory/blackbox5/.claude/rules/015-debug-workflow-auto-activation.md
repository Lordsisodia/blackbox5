---
name: Debug Workflow Auto-Activation
trigger:
  - "debug"
  - "fix failure"
  - "error analysis"
  - "why failed"
  - "root cause"
  - "test failure"
  - "build failure"
alwaysApply: false
priority: 85
---

# Debug Workflow Auto-Activation

## Activation

Activate when debugging failures.

## Triggers

- "debug this"
- "fix failure"
- "error analysis"
- "why did this fail"
- "root cause"
- "test failure"
- "build failure"

## Purpose

Root cause analysis for failures. Prevents endless retry loops.

## Framework

Erotetic Check: E(X,Q)
- X = failing component
- Q = questions to answer

## Output

debug_report.yaml with root cause and fix strategy
