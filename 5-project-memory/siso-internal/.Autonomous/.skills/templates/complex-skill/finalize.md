---
skill: complex-skill-example
command: finalize
version: 1.0.0
---

# Command: finalize

## Purpose
Complete the workflow and perform cleanup.

## When to Invoke
ALWAYS invoke this command, even if previous steps failed.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_path | string | yes | Path to state file |
| final_status | string | yes | "success", "partial", or "failed" |

## Process

1. **Generate outputs**
   - Compile results
   - Create summary
   - Write final report

2. **Cleanup resources**
   - Close connections
   - Free memory
   - Archive temp files

3. **Update registry**
   - Mark workflow complete
   - Record final status

## Output

| Result | Type | Description |
|--------|------|-------------|
| final_status | string | "success", "partial", or "failed" |
| summary | object | Workflow summary |
| artifacts | array | Paths to output files |

## Example

```yaml
Input:
  state_path: ".skills/runs/workflow-001/state.yaml"
  final_status: "success"

Output:
  final_status: "success"
  summary:
    workflow_id: "workflow-001"
    duration: "5m 30s"
    items_processed: 200
  artifacts:
    - "workflow-001/report.md"
    - "workflow-001/results.json"
```
