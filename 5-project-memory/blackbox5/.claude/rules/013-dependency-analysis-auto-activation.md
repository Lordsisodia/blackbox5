---
name: Dependency Analysis Auto-Activation
trigger:
  - "parallel execution"
  - "task order"
  - "dependencies"
  - "conflict detection"
  - "wave planning"
  - "DAG"
  - "cycles"
alwaysApply: false
priority: 80
---

# Dependency Analysis Auto-Activation

## Activation

Activate when planning parallel execution.

## Triggers

- "parallel execution"
- "task order"
- "dependencies"
- "conflict detection"
- "wave planning"
- "detect cycles"

## Purpose

Build DAG, detect cycles, calculate wave groups for parallel execution.

## Input

plan.xml

## Output

wave_groups.yaml
