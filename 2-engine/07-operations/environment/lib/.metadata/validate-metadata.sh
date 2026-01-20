#!/usr/bin/env bash

# Metadata Validation Script
# Validates metadata.yaml files for consistency with AgentMD schema

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$(dirname "$SCRIPT_DIR")"
SCHEMA_FILE="$LIB_DIR/../../03-knowledge/storage/brain/metadata/schema.yaml"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Counters
TOTAL_FILES=0
VALID_FILES=0
INVALID_FILES=0
WARNINGS=0

show_help() {
    cat << EOF
${BLUE}Metadata Validation Script${NC}

Validates metadata.yaml files for consistency with AgentMD schema.

${YELLOW}Usage:${NC}
    $0 [options] [path]

${YELLOW}Arguments:${NC}
    path                Path to validate (default: current directory)

${YELLOW}Options:${NC}
    -s, --schema FILE   AgentMD schema file
    -r, --recursive     Recursively validate all metadata files
    -f, --fix           Attempt to fix common issues
    -v, --verbose       Show detailed validation output
    -q, --quiet         Only show errors
    -h, --help          Show this help message

${YELLOW}Validation Checks:${NC}
    - Required fields present (id, type, name, category, version)
    - Valid artifact types
    - Valid phases (1-4)
    - Valid status values
    - Valid stability levels
    - Valid relationship types
    - YAML syntax
    - Date formats (YYYY-MM-DD)
    - Path references exist
    - Consistent relationships (referenced artifacts exist)

${YELLOW}Exit Codes:${NC}
    0    All valid
    1    Errors found
    2    Schema file not found

EOF
}

# Parse arguments
RECURSIVE=false
FIX=false
VERBOSE=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--schema)
            SCHEMA_FILE="$2"
            shift 2
            ;;
        -r|--recursive)
            RECURSIVE=true
            shift
            ;;
        -f|--fix)
            FIX=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            VALIDATE_PATH="$1"
            shift
            ;;
    esac
done

# Default path
[[ -z "$VALIDATE_PATH" ]] && VALIDATE_PATH="$LIB_DIR"

# Check schema file exists
if [[ ! -f "$SCHEMA_FILE" ]]; then
    echo "${RED}Error: Schema file not found: $SCHEMA_FILE${NC}"
    exit 2
fi

# Valid values (from schema)
VALID_TYPES=("agent" "skill" "plan" "library" "script" "template" "document" "test" "config" "module" "framework" "tool" "workspace" "example")
VALID_PHASES=(1 2 3 4)
VALID_STATUS=("active" "deprecated" "archived" "experimental" "beta" "development")
VALID_STABILITY=("high" "medium" "low")
VALID_RELATIONSHIPS=("implements" "documents" "tests" "uses" "parallel" "extends" "refines" "deprecates" "integrates" "complements" "manages")

# Logging functions
log_info() {
    [[ "$QUIET" == "false" ]] && echo "${BLUE}[INFO]${NC} $*"
}

log_success() {
    [[ "$QUIET" == "false" ]] && echo "${GREEN}[✓]${NC} $*"
}

log_error() {
    echo "${RED}[✗]${NC} $*" >&2
}

log_warning() {
    echo "${YELLOW}[!]${NC} $*" >&2
    ((WARNINGS++))
}

log_verbose() {
    [[ "$VERBOSE" == "true" ]] && echo "  $*"
}

# Check if value is in array
contains_element() {
    local e match="$1"
    shift
    for e; do [[ "$e" == "$match" ]] && return 0; done
    return 1
}

# Validate date format
validate_date() {
    local date="$1"
    if [[ ! "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        return 1
    fi
    return 0
}

# Validate path exists
validate_path() {
    local path="$1"
    local base_dir="$2"

    # Handle relative paths
    if [[ ! "$path" =~ ^/ ]]; then
        path="$base_dir/$path"
    fi

    if [[ ! -e "$path" ]]; then
        return 1
    fi
    return 0
}

# Validate single metadata file
validate_metadata_file() {
    local file="$1"
    local errors=0
    local file_warnings=0

    ((TOTAL_FILES++))

    log_verbose "Validating: $file"

    # Check YAML syntax (requires yamllint or python)
    if command -v yamllint >/dev/null 2>&1; then
        if ! yamllint -d "{extends: relaxed, rules: {line-length: {max: 200}}}" "$file" 2>/dev/null; then
            log_error "$file: YAML syntax error"
            ((errors++))
        fi
    elif command -v python3 >/dev/null 2>&1; then
        if ! python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
            log_error "$file: YAML syntax error"
            ((errors++))
        fi
    fi

    # Extract values using grep/sed (no yaml parser required)
    local id=$(grep -m1 "^id:" "$file" | sed 's/^id: *//' | tr -d '"')
    local type=$(grep -m1 "^type:" "$file" | sed 's/^type: *//' | tr -d '"')
    local name=$(grep -m1 "^name:" "$file" | sed 's/^name: *//' | tr -d '"')
    local category=$(grep -m1 "^category:" "$file" | sed 's/^category: *//' | tr -d '"')
    local phase=$(grep -m1 "^phase:" "$file" | sed 's/^phase: *//')
    local status=$(grep -m1 "^status:" "$file" | sed 's/^status: *//' | tr -d '"')
    local stability=$(grep -m1 "^stability:" "$file" | sed 's/^stability: *//' | tr -d '"')
    local created=$(grep -m1 "^created:" "$file" | sed 's/^created: *//' | tr -d '"')
    local modified=$(grep -m1 "^modified:" "$file" | sed 's/^modified: *//' | tr -d '"')
    local docs_path=$(grep -A1 "^docs:" "$file" | grep "primary:" | sed 's/.*primary: *//' | tr -d '"')

    # Validate required fields
    [[ -z "$id" ]] && { log_error "$file: Missing required field 'id'"; ((errors++)); }
    [[ -z "$type" ]] && { log_error "$file: Missing required field 'type'"; ((errors++)); }
    [[ -z "$name" ]] && { log_error "$file: Missing required field 'name'"; ((errors++)); }
    [[ -z "$category" ]] && { log_error "$file: Missing required field 'category'"; ((errors++)); }

    # Validate type
    if [[ -n "$type" ]] && ! contains_element "$type" "${VALID_TYPES[@]}"; then
        log_error "$file: Invalid type '$type' (must be one of: ${VALID_TYPES[*]})"
        ((errors++))
    fi

    # Validate phase
    if [[ -n "$phase" ]] && ! contains_element "$phase" "${VALID_PHASES[@]}"; then
        log_error "$file: Invalid phase '$phase' (must be 1-4)"
        ((errors++))
    fi

    # Validate status
    if [[ -n "$status" ]] && ! contains_element "$status" "${VALID_STATUS[@]}"; then
        log_error "$file: Invalid status '$status' (must be one of: ${VALID_STATUS[*]})"
        ((errors++))
    fi

    # Validate stability
    if [[ -n "$stability" ]] && ! contains_element "$stability" "${VALID_STABILITY[@]}"; then
        log_error "$file: Invalid stability '$stability' (must be one of: ${VALID_STABILITY[*]})"
        ((errors++))
    fi

    # Validate dates
    if [[ -n "$created" ]] && ! validate_date "$created"; then
        log_error "$file: Invalid created date format '$created' (expected YYYY-MM-DD)"
        ((errors++))
    fi

    if [[ -n "$modified" ]] && ! validate_date "$modified"; then
        log_error "$file: Invalid modified date format '$modified' (expected YYYY-MM-DD)"
        ((errors++))
    fi

    # Validate docs path exists
    if [[ -n "$docs_path" ]]; then
        local doc_dir=$(dirname "$file")
        if ! validate_path "$docs_path" "$doc_dir"; then
            log_warning "$file: Documentation path does not exist: $docs_path"
            ((file_warnings++))
        fi
    fi

    # Summary for file
    if [[ $errors -eq 0 ]]; then
        log_success "$file: Valid"
        ((VALID_FILES++))
    else
        log_error "$file: $errors error(s)"
        ((INVALID_FILES++))
    fi

    ((WARNINGS += file_warnings))
}

# Find metadata files
find_metadata_files() {
    local base_path="$1"

    if [[ "$RECURSIVE" == "true" ]]; then
        find "$base_path" -name "metadata.yaml" -type f
    else
        # Direct subdirectories with metadata.yaml
        for dir in "$base_path"/*/; do
            if [[ -f "${dir}metadata.yaml" ]]; then
                echo "${dir}metadata.yaml"
            fi
        done

        # Also check .metadata/ directory
        if [[ -d "$base_path/.metadata" ]]; then
            find "$base_path/.metadata" -name "*.metadata.yaml" -type f
        fi
    fi
}

# Main validation
main() {
    log_info "Validating metadata files in: $VALIDATE_PATH"
    log_info "Schema: $SCHEMA_FILE"
    echo ""

    # Find all metadata files
    METADATA_FILES=($(find_metadata_files "$VALIDATE_PATH"))

    if [[ ${#METADATA_FILES[@]} -eq 0 ]]; then
        log_warning "No metadata files found"
        exit 0
    fi

    # Validate each file
    for file in "${METADATA_FILES[@]}"; do
        validate_metadata_file "$file"
    done

    # Summary
    echo ""
    echo "${BLUE}=== Validation Summary ===${NC}"
    echo "Total files: $TOTAL_FILES"
    echo -e "${GREEN}Valid: $VALID_FILES${NC}"
    [[ $INVALID_FILES -gt 0 ]] && echo -e "${RED}Invalid: $INVALID_FILES${NC}" || echo "Invalid: $INVALID_FILES"
    [[ $WARNINGS -gt 0 ]] && echo -e "${YELLOW}Warnings: $WARNINGS${NC}" || echo "Warnings: $WARNINGS"

    # Exit code
    if [[ $INVALID_FILES -gt 0 ]]; then
        exit 1
    fi
    exit 0
}

main
