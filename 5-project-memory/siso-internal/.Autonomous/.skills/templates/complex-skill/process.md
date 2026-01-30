---
skill: complex-skill-example
command: process
version: 1.0.0
---

# Command: process

## Purpose
Execute the main logic of the workflow.

## When to Invoke
After [init.md](./init.md) completes successfully.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_path | string | yes | Path from init command |
| iteration | number | no | Current iteration (for loops) |

## Process

1. **Load state**
   - Read state from state_path
   - Verify prerequisites met

2. **Execute main logic**
   - Process data
   - Apply transformations
   - Handle edge cases

3. **Update state**
   - Save progress
   - Record results

4. **Determine next action**
   - More iterations needed? → Loop to process
   - Complete? → Go to finalize
   - Error? → Handle or abort

## Output

| Result | Type | Description |
|--------|------|-------------|
| status | string | "complete", "continue", or "error" |
| results | object | Processing results |
| next_action | string | "finalize" or "process" |

## Error Handling

- **Retryable error**: Log, increment retry count, continue
- **Fatal error**: Log, set status "error", go to finalize

## Example

```yaml
Input:
  state_path: ".skills/runs/workflow-001/state.yaml"
  iteration: 1

Output:
  status: "continue"
  results:
    items_processed: 50
    items_remaining: 150
  next_action: "process"
```
