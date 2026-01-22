#!/bin/bash
#
# Reflection Hook: Trigger next-steps planning after agent completion
#
# This hook runs on Stop/SubagentStop events to:
# 1. Analyze what was just completed
# 2. Determine completion status
# 3. Generate next-steps recommendations
# 4. Maintain momentum between sessions
#

set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# Don't recurse if reflection is already active (prevents infinite loops)
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  exit 0
fi

# Load environment variables
MEMORY_PATH="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}"
REFLECTIONS_DIR="$MEMORY_PATH/operations/reflections"

# Ensure reflections directory exists
mkdir -p "$REFLECTIONS_DIR"

# Get recent conversation context to determine what just happened
RECENT_CONTEXT=""
STATUS="output"

if [[ -f "$TRANSCRIPT_PATH" ]]; then
  # Extract recent content (last few exchanges)
  RECENT_CONTEXT=$(tail -n 100 "$TRANSCRIPT_PATH" 2>/dev/null | \
    jq -r '[.[] | select(.type != "setting") | .message.content] | reverse | .[0:10] | reverse | .[]' 2>/dev/null || echo "")

  # Detect completion status based on content patterns
  if echo "$RECENT_CONTEXT" | grep -qiE "done|complete|finished|implemented|shipped"; then
    STATUS="completion"
  elif echo "$RECENT_CONTEXT" | grep -qiE "implement|create|write|add|build|code"; then
    STATUS="implementation"
  elif echo "$RECENT_CONTEXT" | grep -qiE "research|investigate|analyze|find|explore|compare"; then
    STATUS="research"
  elif echo "$RECENT_CONTEXT" | grep -qiE "fix|debug|resolve|error|issue"; then
    STATUS="troubleshooting"
  fi
fi

# Generate reflection questions based on status
case "$STATUS" in
  completion)
    QUESTIONS="## Completion Review
1. Is all work truly complete?
2. Are tests passing?
3. Is documentation updated?
4. Ready to deploy/ship?

## Next Steps
- If complete: Consider deployment, shipping, or handoff
- If not complete: Identify what remains
- Document: Capture lessons learned"
    ;;
  implementation)
    QUESTIONS="## Implementation Check
1. Did the implementation work as expected?
2. Are there errors to fix?
3. Is refactoring needed?
4. What's the next feature or improvement?

## Next Steps
- Test the implementation
- Fix any issues found
- Plan next iteration
- Write/update tests"
    ;;
  research)
    QUESTIONS="## Research Synthesis
1. What was discovered?
2. Are there remaining questions?
3. Do we have enough information to proceed?
4. Should we implement or research more?

## Next Steps
- Document findings (create ADR if applicable)
- Apply research to implementation
- Identify new research gaps"
    ;;
  troubleshooting)
    QUESTIONS="## Resolution Check
1. Was the issue resolved?
2. Root cause identified?
3. Same issue elsewhere?
4. Preventive measures needed?

## Next Steps
- Verify fix works
- Check for similar issues
- Add tests to prevent regression
- Document root cause"
    ;;
  *)
    QUESTIONS="## Output Review
1. Was the question or request fully addressed?
2. Is more information needed?
3. Should we take action based on this output?
4. Any follow-up questions?

## Next Steps
- Review the output
- Determine if action is needed
- Update knowledge base if applicable"
    ;;
esac

# Generate timestamp for this reflection
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)
TIMESTAMP_UNIX=$(date +%s)

# Save reflection to memory for future reference
REFLECTION_FILE="$REFLECTIONS_DIR/reflection_${TIMESTAMP_UNIX}.md"
cat > "$REFLECTION_FILE" << EOF
# Reflection: $TIMESTAMP

**Session**: $SESSION_ID
**Status**: $STATUS
**Transcript**: $TRANSCRIPT_PATH

## Context
$(echo "$RECENT_CONTEXT" | head -n 20)

## Questions
$QUESTIONS

## Agent Response
[To be filled by agent]

## Next Steps Determined
[To be filled based on reflection]

## Open Loops
- [ ] [To be tracked]
EOF

# Build reflection prompt to inject into context
cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤔 REFLECTION: What's Next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Status**: $STATUS
**Session**: $SESSION_ID

$QUESTIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please provide a brief reflection (2-3 sentences) on:
1. What was just accomplished
2. Whether this is complete or a checkpoint
3. Recommended next steps

This reflection will be saved to: $REFLECTION_FILE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

# Log reflection for tracking
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Reflection triggered: $STATUS (session: $SESSION_ID)" >> \
  "$MEMORY_PATH/operations/reflection-log.txt"

exit 0
