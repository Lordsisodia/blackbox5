---
name: Stop Conditions
trigger:
  - unclear requirements
  - scope creep
  - blocked
  - high risk
  - context overflow
  - contradiction
  - no clear path
alwaysApply: true
priority: 100
---

# Stop Conditions

## PAUSE and Ask User When

1. **Unclear Requirements** - Task objective is ambiguous
2. **Scope Creep** - Task growing beyond original intent
3. **Blocked** - Waiting on external input/dependency
4. **High Risk** - Change could break critical systems
5. **Context Overflow** - At 85% token usage with work remaining
6. **Contradiction** - Finding conflicts with existing code/docs
7. **No Clear Path** - Multiple approaches, uncertain which is best

## EXIT with Status When

- **COMPLETE** - All success criteria met
- **PARTIAL** - Progress made, more work needed
- **BLOCKED** - Cannot proceed without human input

## Documentation
Document reason for stopping in THOUGHTS.md under "## Stop Condition Triggered".

## Source
- CLAUDE.md Stop Conditions
- LEGACY.md operational procedures
