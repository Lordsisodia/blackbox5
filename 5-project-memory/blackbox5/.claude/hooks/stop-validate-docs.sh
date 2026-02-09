#!/bin/bash
# Stop Hook: Validate Documentation Templates
# Blocks session end if documentation files contain unfilled template markers
#
# Usage: Automatically called by Claude Code on Stop hook
# Override: Set RALF_SKIP_DOC_VALIDATION=1 to skip validation

set -e

# Allow override
if [ "${RALF_SKIP_DOC_VALIDATION}" = "1" ]; then
    echo "[RALF] Documentation validation skipped (RALF_SKIP_DOC_VALIDATION=1)"
    exit 0
fi

# Determine run directory
RUN_DIR="${RALF_RUN_DIR}"

if [ -z "$RUN_DIR" ]; then
    # Try to find current run directory from BlackBox5
    BB5_DIR="${HOME}/.blackbox5"
    CURRENT_RUN_FILE="${BB5_DIR}/5-project-memory/blackbox5/.autonomous/CURRENT_RUN"

    if [ -f "$CURRENT_RUN_FILE" ]; then
        RUN_DIR=$(cat "$CURRENT_RUN_FILE" 2>/dev/null | head -1)
    fi
fi

if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
    # No active run directory - nothing to validate
    exit 0
fi

# Files to validate
REQUIRED_FILES=("THOUGHTS.md" "RESULTS.md" "DECISIONS.md" "ASSUMPTIONS.md" "LEARNINGS.md")
ISSUES=0
UNFILLED=()
MISSING=()

# Check each file
for file in "${REQUIRED_FILES[@]}"; do
    filepath="$RUN_DIR/$file"

    if [ ! -f "$filepath" ]; then
        MISSING+=("$file")
        ISSUES=$((ISSUES + 1))
    elif grep -q "RALF_TEMPLATE: UNFILLED" "$filepath" 2>/dev/null; then
        UNFILLED+=("$file")
        ISSUES=$((ISSUES + 1))
    elif grep -q "FILL_ME" "$filepath" 2>/dev/null; then
        UNFILLED+=("$file")
        ISSUES=$((ISSUES + 1))
    fi
done

# Exit cleanly if no issues
if [ $ISSUES -eq 0 ]; then
    exit 0
fi

# Report issues and block
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  RALF DOCUMENTATION VALIDATION FAILED                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Run directory: $RUN_DIR"
echo ""

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "❌ Missing files:"
    for f in "${MISSING[@]}"; do
        echo "   - $f"
    done
    echo ""
fi

if [ ${#UNFILLED[@]} -gt 0 ]; then
    echo "❌ Files with unfilled template markers:"
    for f in "${UNFILLED[@]}"; do
        echo "   - $f"
    done
    echo ""
fi

echo "─────────────────────────────────────────────────────────────────"
echo "Required actions:"
echo "  1. Edit the files above and replace FILL_ME with actual content"
echo "  2. Remove '<!-- RALF_TEMPLATE: UNFILLED -->' markers when done"
echo ""
echo "To force exit without completing documentation:"
echo "  export RALF_SKIP_DOC_VALIDATION=1"
echo ""
echo "═════════════════════════════════════════════════════════════════"
echo ""

# Return non-zero to block session end
exit 1
