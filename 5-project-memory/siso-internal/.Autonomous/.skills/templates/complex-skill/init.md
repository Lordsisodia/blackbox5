---
skill: complex-skill-example
command: init
version: 1.0.0
---

# Command: init

## Purpose
Initialize the complex workflow with proper setup.

## When to Invoke
This is the FIRST command in the workflow. Always start here.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workflow_id | string | yes | Unique identifier for this workflow run |
| config | object | no | Configuration options |

## Process

1. **Validate inputs**
   - Check workflow_id is unique
   - Validate config schema

2. **Initialize state**
   - Create workflow directory
   - Set up tracking files

3. **Prepare resources**
   - Load required data
   - Verify MCPs available

## Output

| Result | Type | Description |
|--------|------|-------------|
| status | string | "ready" or "failed" |
| state_path | string | Path to state file |
| config_validated | object | Validated configuration |

## Next Command

→ [process.md](./process.md)

## Example

```yaml
Input:
  workflow_id: "workflow-001"
  config:
    mode: "standard"
    retries: 3

Output:
  status: "ready"
  state_path: ".skills/runs/workflow-001/state.yaml"
  config_validated:
    mode: "standard"
    retries: 3
```
