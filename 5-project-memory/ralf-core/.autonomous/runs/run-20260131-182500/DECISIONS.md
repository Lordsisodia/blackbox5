# DECISIONS: TASK-001 - Fix RALF Loop Continuity

## Decision 1: Add Explicit Completion Signal to ralf.md

**Context:** The bash loop stops after one iteration because there's no explicit completion signal from the agent.

**Options Considered:**
1. Modify the bash loop to not wait for exit codes
2. Add explicit completion output to ralf.md
3. Use a different loop mechanism (e.g., `claude --loop` if available)

**Selected:** Option 2 - Add explicit completion output to ralf.md

**Rationale:**
- The bash loop is correctly structured - it waits for the claude command to complete
- The issue is that ralf.md doesn't tell the agent to signal completion
- Adding an explicit instruction at the end of ralf.md is the cleanest fix
- This maintains the existing pattern documented in the exit conditions table

**Reversibility:** HIGH
- Simple text addition to ralf.md
- Can be removed by deleting the added section
- No dependencies on other systems

**Rollback Steps:**
1. Remove the added completion section from ralf.md
2. Commit the revert

## Decision 2: Use <promise>COMPLETE</promise> as the Signal

**Context:** Need a consistent, detectable signal that the agent has finished.

**Selected:** Use `<promise>COMPLETE</promise>` as documented in the exit conditions

**Rationale:**
- Already documented in ralf.md line 322
- XML-style tags are easy to parse if needed in the future
- Distinctive enough to not be confused with other output
- Consistent with the existing documentation

**Reversibility:** HIGH
- Just a string format choice
- Can be changed to any other format
