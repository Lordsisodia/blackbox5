#!/bin/bash
#
# Blackbox5 Hook: Validate Completion
# Event: PreToolUse
# Purpose: Stop partial work from being marked "done"
#

set -euo pipefail

data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# Completion indicators
COMPLETION_PATTERNS=(
  "done"
  "complete"
  "finished"
  "ready"
  "task.*done"
  "that.*s it"
  "we.*done"
)

is_completion=false
for pattern in "${COMPLETION_PATTERNS[@]}"; do
  if echo "$prompt" | grep -qi "$pattern"; then
    is_completion=true
    break
  fi
done

if [[ "$is_completion" == "true" ]]; then
  cat << 'EOF'

# ✅ Completion Criteria Check

Before marking this as done, verify:

Code Quality:
- [ ] Code follows project standards
- [ ] No obvious bugs or issues
- [ ] Error handling in place

Testing:
- [ ] Tests written and passing
- [ ] Edge cases considered
- [ ] Manual testing completed

Documentation:
- [ ] Code is self-documenting (clear names, comments)
- [ ] API/docs updated if needed
- [ ] README/example updated if it's a user-facing feature

Review:
- [ ] Self-review completed
- [ ] At least one other person reviewed (if team project)
- [ ] Feedback addressed

Integration:
- [ ] Works with existing code
- [ ] No breaking changes (or documented)
- [ ] Dependencies satisfied

If any of these are missing, consider them before marking done.

---
EOF
fi

echo "$prompt"
exit 0
