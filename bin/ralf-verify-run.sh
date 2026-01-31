#!/bin/bash
# RALF Run Verification Script
# Validates that a run directory has all required files and systems

RUN_DIR="$1"

if [ -z "$RUN_DIR" ]; then
    echo "Usage: ralf-verify-run.sh <run_directory>"
    exit 1
fi

if [ ! -d "$RUN_DIR" ]; then
    echo "❌ Run directory does not exist: $RUN_DIR"
    exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
echo "  RALF Run Verification"
echo "  Run: $(basename "$RUN_DIR")"
echo "═══════════════════════════════════════════════════════════════"
echo ""

ISSUES=0
WARNINGS=0

# Check required documentation files
echo "📄 Documentation Files:"
REQUIRED_FILES=("THOUGHTS.md" "DECISIONS.md" "ASSUMPTIONS.md" "LEARNINGS.md" "RESULTS.md")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$RUN_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING"
        ISSUES=$((ISSUES + 1))
    fi
done
echo ""

# Check system files
echo "⚙️  System Files:"
SYSTEM_FILES=("context_budget.json" "phase_gate_state.yaml" "decision_registry.yaml" "validations.json" "task_state.json" "metrics.json")
for file in "${SYSTEM_FILES[@]}"; do
    if [ -f "$RUN_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING"
        ISSUES=$((ISSUES + 1))
    fi
done
echo ""

# Validate context_budget.json
echo "📊 Context Budget Validation:"
if [ -f "$RUN_DIR/context_budget.json" ]; then
    if jq -e '.current' "$RUN_DIR/context_budget.json" > /dev/null 2>&1; then
        PERCENTAGE=$(jq -r '.current.percentage // 0' "$RUN_DIR/context_budget.json")
        TOKENS=$(jq -r '.current.current_tokens // 0' "$RUN_DIR/context_budget.json")
        echo "  ✅ Valid JSON"
        echo "  📈 Tokens: $TOKENS ($PERCENTAGE%)"

        THRESHOLD=$(jq -r '.current.threshold_triggered // "null"' "$RUN_DIR/context_budget.json")
        if [ "$THRESHOLD" != "null" ]; then
            echo "  ⚠️  Threshold triggered: $THRESHOLD%"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo "  ❌ Invalid JSON structure"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "  ❌ File not found"
fi
echo ""

# Validate phase_gate_state.yaml
echo "🚦 Phase Gate State:"
if [ -f "$RUN_DIR/phase_gate_state.yaml" ]; then
    # Check if yaml is valid by looking for key fields
    if grep -q "gates:" "$RUN_DIR/phase_gate_state.yaml"; then
        echo "  ✅ Valid YAML structure"

        # Count passed gates
        PASSED=$(grep -c "status: \"passed\"" "$RUN_DIR/phase_gate_state.yaml" 2>/dev/null || echo 0)
        echo "  📊 Gates passed: $PASSED"
    else
        echo "  ❌ Missing gates section"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "  ❌ File not found"
fi
echo ""

# Validate metrics.json
echo "📈 Metrics:"
if [ -f "$RUN_DIR/metrics.json" ]; then
    if jq -e '.loop' "$RUN_DIR/metrics.json" > /dev/null 2>&1; then
        LOOP=$(jq -r '.loop' "$RUN_DIR/metrics.json")
        DURATION=$(jq -r '.duration_seconds // 0' "$RUN_DIR/metrics.json")
        TASK_ID=$(jq -r '.task_id // "unknown"' "$RUN_DIR/metrics.json")
        TASK_STATUS=$(jq -r '.task_status // "unknown"' "$RUN_DIR/metrics.json")

        echo "  ✅ Valid JSON"
        echo "  🔄 Loop: $LOOP"
        echo "  ⏱️  Duration: ${DURATION}s"
        echo "  📝 Task: $TASK_ID ($TASK_STATUS)"

        if [ "$TASK_STATUS" = "completed" ]; then
            echo "  ✅ Task marked as completed"
        else
            echo "  ⚠️  Task not marked as completed"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo "  ❌ Invalid JSON structure"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "  ❌ File not found"
fi
echo ""

# Validate validations.json
echo "✓ Validations:"
if [ -f "$RUN_DIR/validations.json" ]; then
    TOTAL=$(jq -r '.metadata.total_validations // 0' "$RUN_DIR/validations.json")
    VERIFIED=$(jq -r '.metadata.claims_verified // 0' "$RUN_DIR/validations.json")

    echo "  ✅ Valid JSON"
    echo "  📊 Total validations: $TOTAL"
    echo "  ✅ Claims verified: $VERIFIED"

    if [ "$TOTAL" -eq 0 ]; then
        echo "  ⚠️  No validations recorded"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ❌ File not found"
fi
echo ""

# Check task state
echo "📝 Task State:"
if [ -f "$RUN_DIR/task_state.json" ]; then
    TASK_STATUS=$(jq -r '.task.status // "unknown"' "$RUN_DIR/task_state.json")
    echo "  ✅ Valid JSON"
    echo "  📊 Status: $TASK_STATUS"
else
    echo "  ❌ File not found"
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════"
echo "  Verification Summary"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ $ISSUES -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "  ✅ ALL CHECKS PASSED"
    echo ""
    echo "  The run is fully compliant with RALF v2.4 standards."
    exit 0
elif [ $ISSUES -eq 0 ]; then
    echo "  ⚠️  PASSED WITH WARNINGS"
    echo ""
    echo "  Warnings: $WARNINGS"
    echo "  The run is functional but has room for improvement."
    exit 0
else
    echo "  ❌ VERIFICATION FAILED"
    echo ""
    echo "  Issues: $ISSUES"
    echo "  Warnings: $WARNINGS"
    echo ""
    echo "  The run is missing critical components."
    exit 1
fi
