#!/bin/bash
################################################################################
# Pre-Execution Hook: Skill Enforcement
#
# Enforces skill invocation based on confidence scores from detect-skill.py
#
# Exit Codes:
#   0: Allow execution (proceed with task)
#   1: Block execution (skill must be invoked first)
#
# Usage:
#   This hook is called automatically before task execution.
#   To bypass: BB5_SKIP_SKILL_ENFORCEMENT=1
################################################################################

set -euo pipefail

# Configuration
BB5_ROOT="${BB5_ROOT:-/opt/blackbox5}"
SKILL_REGISTRY="${BB5_ROOT}/5-project-memory/blackbox5/operations/skill-registry.yaml"
SKILL_METRICS="${BB5_ROOT}/5-project-memory/blackbox5/operations/skill-metrics.yaml"
DETECT_SKILL="${BB5_ROOT}/5-project-memory/blackbox5/bin/detect-skill.py"
ENFORCEMENT_LOG="${BB5_ROOT}/5-project-memory/blackbox5/logs/skill-enforcement.log"
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_FILE="${TASK_FILE:-${HOOK_DIR}/../../TASK.md}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Functions
################################################################################

log_enforcement() {
    local action="$1"
    local details="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[${timestamp}] ${action}: ${details}" >> "${ENFORCEMENT_LOG}"
}

get_task_text() {
    if [[ -f "${TASK_FILE}" ]]; then
        # Extract objective or first paragraph from task.md
        local objective=$(grep -E "^#{1,2} (Objective|Task)" -A 5 "${TASK_FILE}" 2>/dev/null | head -10)
        if [[ -n "${objective}" ]]; then
            echo "${objective}"
        else
            # Fallback: first 20 lines of the task
            cat "${TASK_FILE}" | head -20
        fi
    else
        echo "No task file found at ${TASK_FILE}"
    fi
}

print_block_message() {
    local skill_name="$1"
    local confidence="$2"
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║${NC}         ${RED}SKILL ENFORCEMENT: CLEAR TRIGGER DETECTED${NC}            ${RED}║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Task:${NC} $(get_task_text | head -1)"
    echo ""
    echo -e "${RED}Required skill:${NC} ${YELLOW}${skill_name}${NC} (confidence: ${confidence}%)"
    echo -e "${RED}Action:${NC} ${GREEN}MUST invoke before proceeding${NC}"
    echo ""
    echo -e "${BLUE}To proceed:${NC}"
    echo "  1. Invoke skill: ${YELLOW}skill: \"${skill_name}\"${NC}"
    echo "  2. Or set ${YELLOW}BB5_SKIP_SKILL_ENFORCEMENT=1${NC} (not recommended)"
    echo ""
    echo -e "${RED}Execution blocked until skill is invoked.${NC}"
    echo ""
}

print_discretionary_warning() {
    local skill_name="$1"
    local confidence="$2"
    echo ""
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║${NC}     ${YELLOW}SKILL ENFORCEMENT: DISCRETIONARY TRIGGER DETECTED${NC}      ${YELLOW}║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Task:${NC} $(get_task_text | head -1)"
    echo ""
    echo -e "${YELLOW}Recommended skill:${NC} ${GREEN}${skill_name}${NC} (confidence: ${confidence}%)"
    echo -e "${YELLOW}Action:${NC} ${GREEN}SHOULD invoke${NC} (override allowed with justification)"
    echo ""
    echo -e "${BLUE}Override? Add to THOUGHTS.md:${NC}"
    echo '  ## Skill Override Justification'
    echo '  Reason for not invoking: [explain]'
    echo ""
}

print_no_match() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}            ${GREEN}SKILL ENFORCEMENT: NO MATCH DETECTED${NC}             ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Task:${NC} $(get_task_text | head -1)"
    echo ""
    echo -e "${GREEN}Action:${NC} Continue normally (confidence: <70%)"
    echo ""
}

log_enforcement_to_yaml() {
    local task_id="$1"
    local trigger_type="$2"
    local skill_recommended="$3"
    local confidence="$4"
    local action_taken="$5"
    local overridden="${6:-false}"
    local justification="${7:-}"

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Append to enforcement log in skill-metrics.yaml
    if [[ -f "${SKILL_METRICS}" ]]; then
        # Use Python for reliable YAML manipulation
        python3 <<EOF
import yaml
from pathlib import Path

yaml_file = Path("${SKILL_METRICS}")

try:
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
except:
    data = {}

# Ensure enforcement_log exists and is a list
if not isinstance(data.get('enforcement_log'), list):
    data['enforcement_log'] = []

# Add new entry
data['enforcement_log'].append({
    'timestamp': '${timestamp}',
    'task_id': '${task_id}',
    'trigger_type': '${trigger_type}',
    'skill_recommended': '${skill_recommended}',
    'confidence': ${confidence},
    'action_taken': '${action_taken}',
    'overridden': ${overridden},
    'justification': '${justification}'
})

# Write back
with open(yaml_file, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
EOF
    fi
}

################################################################################
# Main Logic
################################################################################

main() {
    # Check for bypass
    if [[ "${BB5_SKIP_SKILL_ENFORCEMENT:-0}" == "1" ]]; then
        echo "[SKILL ENFORCEMENT] Bypassed via BB5_SKIP_SKILL_ENFORCEMENT=1"
        log_enforcement "bypassed" "BB5_SKIP_SKILL_ENFORCEMENT=1"
        exit 0
    fi

    # Check if detect-skill.py exists
    if [[ ! -x "${DETECT_SKILL}" ]]; then
        echo "[SKILL ENFORCEMENT] Warning: detect-skill.py not found or not executable"
        echo "[SKILL ENFORCEMENT] Skipping skill enforcement"
        log_enforcement "skipped" "detect-skill.py not found"
        exit 0
    fi

    # Get task text
    local task_text=$(get_task_text)

    if [[ -z "${task_text}" ]] || [[ "${task_text}" == "No task file found"* ]]; then
        echo "[SKILL ENFORCEMENT] No task text found, skipping enforcement"
        log_enforcement "skipped" "No task text"
        exit 0
    fi

    # Run detect-skill.py (capture exit code without triggering set -e)
    local skill_output
    skill_output=$(${DETECT_SKILL} --registry "${SKILL_REGISTRY}" "${task_text}" 2>/dev/null) || true
    local detect_exit_code=${PIPESTATUS[0]}

    # Exit code 3 is error, others are valid results
    if [[ ${detect_exit_code} -eq 3 ]]; then
        echo "[SKILL ENFORCEMENT] Error running detect-skill.py (exit: ${detect_exit_code})"
        log_enforcement "error" "detect-skill.py failed with exit ${detect_exit_code}"
        exit 0  # Don't block on error
    fi

    # Parse JSON output
    local action_required=$(echo "${skill_output}" | jq -r '.action_required // "MAY check"')
    local top_skill=$(echo "${skill_output}" | jq -r '.recommended_skills[0] // empty')
    local skill_name=$(echo "${top_skill}" | jq -r '.name // empty')
    local skill_id=$(echo "${top_skill}" | jq -r '.id // empty')
    local confidence=$(echo "${top_skill}" | jq -r '.confidence // 0')

    # Get task ID from environment or file
    local task_id="${TASK_ID:-$(basename $(dirname "${TASK_FILE}"))}"

    # Determine trigger type
    local trigger_type
    if [[ "${action_required}" == "MUST invoke" ]]; then
        trigger_type="clear"
    elif [[ "${action_required}" == "SHOULD invoke" ]]; then
        trigger_type="discretionary"
    else
        trigger_type="none"
    fi

    # Handle different trigger types
    case "${trigger_type}" in
        clear)
            # Clear trigger: Block execution
            print_block_message "${skill_name}" "${confidence}"
            log_enforcement "blocked" "Task: ${task_id}, Skill: ${skill_name}, Confidence: ${confidence}"
            log_enforcement_to_yaml "${task_id}" "clear" "${skill_name}" "${confidence}" "blocked_pending_invocation" "false"
            exit 1
            ;;

        discretionary)
            # Discretionary trigger: Warn but allow
            print_discretionary_warning "${skill_name}" "${confidence}"
            log_enforcement "warned" "Task: ${task_id}, Skill: ${skill_name}, Confidence: ${confidence}"
            log_enforcement_to_yaml "${task_id}" "discretionary" "${skill_name}" "${confidence}" "override_with_justification" "false"
            exit 0
            ;;

        *)
            # No match: Continue normally
            print_no_match
            log_enforcement "allowed" "Task: ${task_id}, No match"
            exit 0
            ;;
    esac
}

# Run main function
main "$@"
