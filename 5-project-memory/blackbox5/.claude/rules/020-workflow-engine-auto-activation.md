---
name: Workflow Engine Auto-Activation
trigger:
  - "run workflow"
  - "execute flow"
  - "workflow step"
  - "start flow"
alwaysApply: false
priority: 80
---

# Workflow Engine Auto-Activation

## Activation

Activate for multi-step workflow execution.

## Triggers

- "run workflow"
- "execute flow"
- "workflow step"
- "start flow"

## Purpose

Manage workflow execution across Research, Planning, Execution, Verification, and Memory flows.

## Flows

1. **Research** - Gather context
2. **Planning** - Create plans
3. **Execution** - Implement tasks
4. **Verification** - Quality gates
5. **Memory** - Persist context

## Output

workflow_execution.yaml with state tracking
