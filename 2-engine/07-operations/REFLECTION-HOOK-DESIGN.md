# Reflection Hook: Next Steps Architecture

**Version**: 1.0.0
**Date**: 2026-01-21
**Status**: Design Phase

---

## Problem Statement

**Current Issue**: Agent output is a dead end. After an agent completes work, there's no automatic reflection on:
1. What was just accomplished?
2. Is this a completion or a checkpoint?
3. What should happen next?
4. Are there open loops to close?

**Desired Behavior**: Every agent completion should trigger a **reflection phase** that:
- Analyzes the current state
- Determines if work is complete or in progress
- Proposes concrete next steps
- Maintains momentum

---

## Architecture

### Hook Event: Stop / SubagentStop

```
Agent Completes
    │
    ↓
[PostToolUse: Write/Edit]  ← Already runs (logs activity)
    │
    ↓
[Stop Event]  ← NEW: Reflection hook runs here
    │
    ├─→ Reflect on what was done
    ├─→ Determine completion status
    ├─→ Generate next steps
    └─→ Propose continuation
```

### Runtime Behavior Questions

The reflection hook should help the agent answer:

1. **Are we just asking for output?**
   - Yes: Output delivered → User review needed
   - No: Action taken → Verify results

2. **Is this just a checkpoint?**
   - Yes: Mark progress → Continue with next phase
   - No: Work unit complete → Consider finalization

3. **Should we continue researching?**
   - Yes: Identify gaps → Plan research
   - No: Sufficient data → Proceed to implementation

4. **What are the next steps?**
   - Immediate: Do this next (within session)
   - Short-term: Plan for next session
   - Long-term: Strategic direction

---

## Reflection Template

```markdown
# Reflection: [Task Name]

## What Was Done

[Brief summary of what the agent just accomplished]

## Completion Status

- [ ] **Output Delivered**: Results provided to user
- [ ] **Checkpoint Reached**: Milestone achieved, more work ahead
- [ ] **Research Complete**: Investigation finished, ready for action
- [ ] **Implementation Complete**: Code shipped, tests passing
- [ ] **Documentation Updated**: Knowledge captured

## Open Loops

- [ ] Loop 1: [Description]
- [ ] Loop 2: [Description]
- [ ] Loop 3: [Description]

## Next Steps

### Immediate (Do Now)
1. [ ] [Action item]
2. [ ] [Action item]

### Short-term (Next Session)
1. [ ] [Action item]
2. [ ] [Action item]

### Long-term (Strategic)
1. [ ] [Action item]
2. [ ] [Action item]

## Blockers / Dependencies

- **Blocker**: [Description]
- **Dependency**: [Description]
- **Risk**: [Description]

## Recommendations

- **Continue**: [What to do next]
- **Pause**: [What to review first]
- **Delegate**: [What to hand off]
```

---

## Hook Implementation

### File: `.claude/hooks/reflect-on-completion.sh`

```bash
#!/bin/bash
#
# Reflection Hook: Trigger next-steps planning after agent completion
#

set -euo pipefail

# Read hook input
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# Don't recurse if reflection is already active
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  exit 0
fi

# Load environment
MEMORY_PATH="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}"
REFLECTIONS_DIR="$MEMORY_PATH/operations/reflections"

# Ensure directory exists
mkdir -p "$REFLECTIONS_DIR"

# Get recent conversation context
if [[ -f "$TRANSCRIPT_PATH" ]]; then
  # Extract last few exchanges
  RECENT_CONTEXT=$(tail -n 50 "$TRANSCRIPT_PATH" | jq -r '.[] | select(.type != "setting") | .message.content' 2>/dev/null || echo "")

  # Detect what just happened
  if echo "$RECENT_CONTEXT" | grep -qi "done\|complete\|finished"; then
    STATUS="completion"
  elif echo "$RECENT_CONTEXT" | grep -qi "implement\|create\|write\|add"; then
    STATUS="implementation"
  elif echo "$RECENT_CONTEXT" | grep -qi "research\|investigate\|analyze\|find"; then
    STATUS="research"
  else
    STATUS="output"
  fi
else
  STATUS="output"
fi

# Generate reflection questions based on status
case "$STATUS" in
  completion)
    QUESTIONS="## Completion Review
1. Is all work truly done?
2. Are tests passing?
3. Is documentation updated?
4. Are there any edge cases?

## Next Steps
- If complete: Consider deployment/shipping
- If not complete: What remains?"
    ;;
  implementation)
    QUESTIONS="## Implementation Check
1. Did the implementation work?
2. Are there errors to fix?
3. Is refactoring needed?
4. What's the next feature?

## Next Steps
- Test the implementation
- Fix any issues
- Plan next iteration"
    ;;
  research)
    QUESTIONS="## Research Synthesis
1. What was discovered?
2. Are there remaining questions?
3. Do we have enough information?
4. Should we implement now or research more?

## Next Steps
- Document findings
- Apply research to implementation
- Identify new research gaps"
    ;;
  *)
    QUESTIONS="## Output Review
1. Was the question answered?
2. Is more information needed?
3. Should we take action based on this?

## Next Steps
- Review output
- Determine next action
- Update knowledge base"
    ;;
esac

# Inject reflection into context
cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤔 REFLECTION: What's Next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: $STATUS

$QUESTIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please provide a brief reflection on the current state and recommend next steps.

EOF

# Save reflection to memory
REFLECTION_FILE="$REFLECTIONS_DIR/reflection_$(date +%s).md"
cat > "$REFLECTION_FILE" << EOF
# Reflection: $(date +%Y-%m-%d\ %H:%M:%S)

Session: $SESSION_ID
Status: $STATUS

## Questions
$QUESTIONS

## Agent Response
[To be filled by agent]

## Next Steps
[To be determined]
EOF

exit 0
```

---

## Settings Configuration

### File: `.claude/settings.json`

Add to existing hooks configuration:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/reflect-on-completion.sh",
          "timeout": 10
        }
      ]
    }],
    "SubagentStop": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/reflect-on-completion.sh",
          "timeout": 10
        },
        {
          "type": "command",
          "command": ".claude/hooks/analyze-subagent-quality.sh",
          "timeout": 10
        }
      ]
    }]
  }
}
```

---

## Runtime Behavior Examples

### Example 1: Output Delivered

```
Agent: [Explains how to implement JWT auth]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤔 REFLECTION: What's Next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: output

## Output Review
1. Was the question answered? Yes
2. Is more information needed? No
3. Should we take action based on this? Possibly

## Next Steps
- Review output
- Determine next action
- Update knowledge base

Please provide a brief reflection...

Agent Reflection: I provided a clear explanation of JWT implementation.
The user now has the information they need. No immediate action required
unless they want me to implement this for them.

Next Steps:
- Await user direction
- Implement if requested
```

### Example 2: Implementation Complete

```
Agent: [Implements user authentication feature]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤔 REFLECTION: What's Next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: implementation

## Implementation Check
1. Did the implementation work? Yes
2. Are there errors to fix? None
3. Is refactoring needed? Maybe later
4. What's the next feature? Authorization

## Next Steps
- Test the implementation
- Fix any issues
- Plan next iteration

Please provide a brief reflection...

Agent Reflection: I successfully implemented JWT authentication with:
- Login endpoint
- Token validation
- User middleware

Open loops:
- [ ] Add tests
- [ ] Update API docs
- [ ] Implement refresh tokens

Next Steps:
1. Write unit tests for auth endpoints
2. Update API documentation
3. Consider adding refresh token rotation
```

### Example 3: Research Complete

```
Agent: [Analyzes different database options]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤔 REFLECTION: What's Next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: research

## Research Synthesis
1. What was discovered? Compared PostgreSQL, MongoDB, Redis
2. Are there remaining questions? Performance at scale
3. Do we have enough information? Yes for MVP
4. Should we implement now or research more? Implement now

## Next Steps
- Document findings
- Apply research to implementation
- Identify new research gaps

Please provide a brief reflection...

Agent Reflection: Research complete. Recommendation: PostgreSQL for primary data,
Redis for caching, MongoDB for unstructured data.

Open loops:
- [ ] Document architecture decision
- [ ] Create database schema
- [ ] Set up connection pooling

Next Steps:
1. Create ADR documenting database selection
2. Implement initial schema
3. Set up ORM/connection layer
```

---

## Memory Integration

### Reflection Storage

```
5-project-memory/siso-internal/
├── operations/
│   └── reflections/
│       ├── reflection_1705845200.md  # Timestamped reflections
│       ├── reflection_1705845300.md
│       └── ...
├── decisions/
│   └── [Reflections can create ADRs]
└── sessions/
    └── [Reflections linked to sessions]
```

### Reflection → Decision Flow

```
Reflection identifies need for decision
    │
    ↓
[Decision Capture Hook]
    │
    ↓
Create ADR in decisions/
    │
    ↓
Reference in future sessions
```

---

## Advanced Features

### 1. Continuous Reflection Loop

```bash
# Option: Automatically continue without waiting
if [[ "${AUTO_CONTINUE:-false}" == "true" ]]; then
  # Don't block, just log and continue
  echo "Continuing based on reflection..." >&2
  exit 0
fi
```

### 2. Confidence Scoring

```bash
# Detect agent confidence
CONFIDANCE=$(echo "$RECENT_CONTEXT" | grep -c "certain\|definitely\|confirmed" || true)

if [[ $CONFIDANCE -gt 0 ]]; then
  STATUS="high-confidence"
else
  STATUS="needs-validation"
fi
```

### 3. Pattern Recognition

```bash
# Detect repeated sessions on same topic
PREVIOUS_REFLECTIONS=$(ls -t "$REFLECTIONS_DIR"/*.md 2>/dev/null | head -5)

if [[ -n "$PREVIOUS_REFLECTIONS" ]]; then
  echo "Note: You've been working on this topic across multiple sessions."
  echo "Previous reflections may provide context."
fi
```

---

## Implementation Checklist

- [ ] Create `reflect-on-completion.sh` hook script
- [ ] Add to `.claude/settings.json` under `Stop` and `SubagentStop`
- [ ] Create `operations/reflections/` directory structure
- [ ] Test with different completion types
- [ ] Integrate with existing decision capture
- [ ] Add reflection review to SessionEnd hooks
- [ ] Document reflection patterns

---

## Future Enhancements

1. **Smart Reflections**: Use LLM to generate contextual reflections
2. **Reflection Analytics**: Track patterns in reflections
3. **Auto-Continuation**: Suggest starting next session based on reflection
4. **Reflection Summaries**: Weekly summary of all reflections
5. **Integration with Planning**: Feed reflections into planning workflows

---

## Conclusion

The reflection hook transforms agent completions from dead ends into **strategic checkpoints** that:
- Maintain momentum between sessions
- Surface open loops explicitly
- Guide next-step planning
- Build organizational memory

**Key Insight**: Every completion should answer "what's next?" — not just "what did I do?"
