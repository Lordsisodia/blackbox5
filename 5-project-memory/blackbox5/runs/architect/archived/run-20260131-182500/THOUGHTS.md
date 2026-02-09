# THOUGHTS: TASK-001 - Fix RALF Loop Continuity

## Problem Analysis

The issue is that the bash loop `while true; do cat ralf.md | claude --dangerously-skip-permissions ; done` stops after one iteration instead of continuing indefinitely.

## Root Cause Investigation

Looking at the code:

1. **ralf-simple-loop.sh** (line 28): Uses `if ! cat "$PROMPT_FILE" | claude --dangerously-skip-permissions 2>&1; then`
   - The `if !` checks if the claude command fails (non-zero exit code)
   - If it succeeds (exit 0), the loop continues
   - If it fails, it waits 10 seconds and continues

2. **ralf.md Exit Conditions** (line 322): Documents that COMPLETE status should output `<promise>COMPLETE</promise>`
   - However, the prompt doesn't explicitly instruct the agent to output this at the end
   - The agent needs a clear signal that it's done so the loop can continue

## The Fix

The ralf.md file needs to explicitly tell the agent to output a completion signal at the very end. This serves two purposes:
1. It signals to the loop that the iteration is complete
2. It provides a consistent pattern for the bash loop to detect success

The fix is to add an explicit instruction at the end of ralf.md telling the agent to output a completion marker.

## Approach

1. Add a final step to ralf.md that explicitly tells the agent to output `<promise>COMPLETE</promise>` when done
2. This ensures the loop receives proper signaling
3. Test the loop behavior
