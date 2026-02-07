---
name: Orchestrator Auto-Activation
trigger:
  - all_requests
alwaysApply: true
priority: 100
---

# Orchestrator Auto-Activation

## Activation

This skill is ALWAYS active on every request.

## Purpose

The orchestrator is the central coordinator for all BlackBox5 workflows. It routes requests to appropriate flows based on the decision matrix.

## Decision Matrix

| Request Type | Keywords | Flows Activated |
|--------------|----------|-----------------|
| Research | research, analyze, understand | Research Flow |
| Architecture | design, architect, structure | Research + Planning |
| Implementation | implement, build, create | All 4 Flows |
| Bug Fix | fix, debug, error | Execution + Verification |
| Optimization | improve, optimize | Research + Execution |
| Documentation | document, record | Memory Flow |

## Output

Routes to appropriate skill(s):
- `research-suite` for research tasks
- `planner` for planning tasks
- `validator` for verification tasks
- `debug-workflow` for debugging tasks
