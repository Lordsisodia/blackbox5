# LEARNINGS: TASK-001 - Fix RALF Loop Continuity

## Key Insights

1. **Documentation vs Implementation Gap**: The exit conditions table (line 322) documented that COMPLETE status should output `<promise>COMPLETE</promise>`, but the prompt never actually instructed the agent to do so. This is a common pattern - documentation exists but isn't connected to implementation.

2. **Loop Mechanics**: The bash loop uses `if ! cat "$PROMPT_FILE" | claude ...` which means:
   - If claude exits with code 0 (success), the `if !` condition is false, so it skips the error block
   - The loop continues naturally to the next iteration
   - The issue wasn't the loop structure but the agent not knowing when to signal completion

3. **Explicit Instructions Matter**: Agents need explicit instructions for critical behaviors. Assuming the agent will "just know" to signal completion is insufficient - it must be explicitly stated in the prompt.

## What Worked

- Reading the full ralf.md to understand the exit conditions
- Identifying the gap between documented behavior and actual instructions
- Adding a clear "FINAL STEP" section that explicitly tells the agent what to do

## What to Remember for Future

- When documenting exit conditions or status signals, also add explicit instructions telling the agent to use them
- The bash loop is robust - the issue was in the prompt, not the shell script
- Simple text additions to the prompt can fix complex behavioral issues
