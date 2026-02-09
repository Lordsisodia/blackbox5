#!/bin/bash
#
# consolidate-run.sh - Merge fragmented run files into unified RUN.yaml
#
# Usage: consolidate-run.sh [run_directory]
#        consolidate-run.sh --all
#        consolidate-run.sh --dry-run [run_directory]
#
# Merges: THOUGHTS.md, DECISIONS.md|yaml, ASSUMPTIONS.md, RESULTS.md, LEARNINGS.md
# Into:   RUN.yaml (unified format)

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default run directory base
RUNS_BASE="${HOME}/.blackbox5/5-project-memory/blackbox5/runs"

# Dry run flag
DRY_RUN=false

# Statistics
STATS_TOTAL=0
STATS_SUCCESS=0
STATS_SKIPPED=0
STATS_FAILED=0

# Help function
show_help() {
    cat << 'EOF'
Usage: consolidate-run.sh [OPTIONS] [RUN_DIRECTORY]

Merge fragmented run output files into unified RUN.yaml format.

OPTIONS:
    -h, --help          Show this help message
    -a, --all           Process all run directories
    -d, --dry-run       Show what would be done without making changes
    -k, --keep          Keep original files after consolidation

ARGUMENTS:
    RUN_DIRECTORY       Path to specific run directory (e.g., runs/planner/run-20260131_192605)

EXAMPLES:
    # Consolidate specific run
    consolidate-run.sh runs/planner/run-20260131_192605

    # Dry run to preview changes
    consolidate-run.sh --dry-run runs/planner/run-20260131_192605

    # Consolidate all runs
    consolidate-run.sh --all

    # Consolidate and keep originals
    consolidate-run.sh --keep runs/planner/run-20260131_192605
EOF
}

# Extract content from Markdown file - simple version
extract_section_content() {
    local file="$1"
    local start_pattern="$2"

    if [[ ! -f "$file" ]]; then
        return
    fi

    awk -v start="$start_pattern" '
        $0 ~ start {found=1; next}
        found && /^## [^#]/ {exit}
        found {print}
    ' "$file" 2>/dev/null || true
}

# Parse decisions from DECISIONS.md
parse_decisions_md() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        return
    fi

    # Convert markdown decisions to YAML format
    awk '
        /^### DEC-[0-9]+:/ {
            if (in_dec) print ""
            in_dec=1
            gsub(/^### /, "")
            print "- id: \"" $0 "\""
            next
        }
        in_dec && /^\*\*Context\*\*:/ {
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  context: \"" $0 "\""
        }
        in_dec && /^\*\*Decision\*\*:/ {
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  decision: \"" $0 "\""
        }
        in_dec && /^\*\*Rationale\*\*:/ {
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  rationale: \"" $0 "\""
        }
        in_dec && /^---$/ {
            in_dec=0
        }
    ' "$file" 2>/dev/null || true
}

# Parse assumptions from ASSUMPTIONS.md
parse_assumptions_md() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        return
    fi

    awk '
        /^### ASM-[0-9]+:/ {
            if (in_asm) print ""
            in_asm=1
            gsub(/^### /, "")
            print "- id: \"" $0 "\""
            next
        }
        in_asm && /^\*\*Assumption\*\*:/ {
            gsub(/^\*\*Assumption\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  assumption: \"" $0 "\""
        }
        in_asm && /^\*\*Validation Method\*\*:/ {
            gsub(/^\*\*Validation Method\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  validation_method: \"" $0 "\""
        }
        in_asm && /^\*\*Validation Result\*\*:/ {
            gsub(/^\*\*Validation Result\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  validation_result: \"" $0 "\""
        }
        in_asm && /^\*\*Confidence Level\*\*:/ {
            gsub(/^\*\*Confidence Level\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  confidence: \"" $0 "\""
        }
        in_asm && /^---$/ {
            in_asm=0
        }
    ' "$file" 2>/dev/null || true
}

# Parse learnings from LEARNINGS.md
parse_learnings_md() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        return
    fi

    awk '
        /^### LRN-[0-9]+:/ {
            if (in_lrn) print ""
            in_lrn=1
            gsub(/^### /, "")
            print "- id: \"" $0 "\""
            next
        }
        in_lrn && /^\*\*What Worked\*\*:/ {
            gsub(/^\*\*What Worked\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  what_worked: \"" $0 "\""
        }
        in_lrn && /^\*\*Takeaway\*\*:/ {
            gsub(/^\*\*Takeaway\*\*:[[:space:]]*/, "")
            gsub(/^\*\*/, "")
            gsub(/\*\*$/, "")
            print "  takeaway: \"" $0 "\""
        }
        in_lrn && /^---$/ {
            in_lrn=0
        }
    ' "$file" 2>/dev/null || true
}

# Extract metadata from run files
extract_metadata() {
    local run_dir="$1"
    local run_id=""
    local timestamp=""
    local task_id=""
    local agent=""

    # Try to extract from THOUGHTS.md
    if [[ -f "$run_dir/THOUGHTS.md" ]]; then
        run_id=$(grep -E '^\*\*Run ID:\*\*' "$run_dir/THOUGHTS.md" 2>/dev/null | head -1 | sed 's/.*Run ID:[[:space:]]*//' | tr -d '*' | tr -d ' ' || true)
        timestamp=$(grep -E '^\*\*Started:\*\*' "$run_dir/THOUGHTS.md" 2>/dev/null | head -1 | sed 's/.*Started:[[:space:]]*//' | tr -d '*' || true)
    fi

    # Try to extract from RESULTS.md
    if [[ -f "$run_dir/RESULTS.md" ]]; then
        [[ -z "$run_id" ]] && run_id=$(grep -E '^\*\*Run ID:\*\*' "$run_dir/RESULTS.md" 2>/dev/null | head -1 | sed 's/.*Run ID:[[:space:]]*//' | tr -d '*' | tr -d ' ' || true)
        [[ -z "$timestamp" ]] && timestamp=$(grep -E '^\*\*Completed:\*\*' "$run_dir/RESULTS.md" 2>/dev/null | head -1 | sed 's/.*Completed:[[:space:]]*//' | tr -d '*' || true)
        [[ -z "$task_id" ]] && task_id=$(grep -E '^\*\*Task ID:\*\*' "$run_dir/RESULTS.md" 2>/dev/null | head -1 | sed 's/.*Task ID:[[:space:]]*//' | tr -d '*' || true)
    fi

    # Derive run_id from directory name if not found
    if [[ -z "$run_id" ]]; then
        run_id=$(basename "$run_dir")
    fi

    # Default values
    [[ -z "$agent" ]] && agent="claude"
    [[ -z "$timestamp" ]] && timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Clean up extracted values
    run_id=$(echo "$run_id" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    timestamp=$(echo "$timestamp" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    task_id=$(echo "$task_id" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    echo "run_id: \"$run_id\""
    echo "timestamp: \"$timestamp\""
    [[ -n "$task_id" ]] && echo "task_id: \"$task_id\""
    echo "agent: \"$agent\""
}

# Consolidate a single run directory
consolidate_run() {
    local run_dir="$1"
    local keep_originals="$2"

    ((STATS_TOTAL++))

    # Validate directory
    if [[ ! -d "$run_dir" ]]; then
        echo -e "${RED}ERROR: Directory not found: $run_dir${NC}"
        ((STATS_FAILED++))
        return 1
    fi

    # Check if already consolidated
    if [[ -f "$run_dir/RUN.yaml" ]]; then
        echo -e "${YELLOW}SKIP: Already consolidated: $(basename "$run_dir")${NC}"
        ((STATS_SKIPPED++))
        return 0
    fi

    # Check for source files
    local has_source=false
    for file in THOUGHTS.md DECISIONS.md DECISIONS.yaml DECISIONS.yml ASSUMPTIONS.md RESULTS.md LEARNINGS.md; do
        if [[ -f "$run_dir/$file" ]]; then
            has_source=true
            break
        fi
    done

    if [[ "$has_source" == "false" ]]; then
        echo -e "${YELLOW}SKIP: No source files in: $(basename "$run_dir")${NC}"
        ((STATS_SKIPPED++))
        return 0
    fi

    echo -e "${BLUE}Processing: $(basename "$run_dir")${NC}"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "  Would create: RUN.yaml"
        for file in THOUGHTS.md DECISIONS.md DECISIONS.yaml ASSUMPTIONS.md RESULTS.md LEARNINGS.md; do
            if [[ -f "$run_dir/$file" ]]; then
                echo "  Would include: $file"
            fi
        done
        return 0
    fi

    # Create RUN.yaml
    local run_yaml="$run_dir/RUN.yaml"

    {
        echo "# Unified Run Output"
        echo "# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        echo ""
        echo "---"
        echo ""

        # Metadata section
        echo "# Metadata"
        extract_metadata "$run_dir"
        echo ""

        # Thoughts section
        echo "# Thoughts and Reasoning"
        echo "thoughts: |"
        if [[ -f "$run_dir/THOUGHTS.md" ]]; then
            # Extract content after "## Thought Process" or just take everything after header
            awk 'BEGIN{found=0} /^## Thought Process/{found=1; next} found && /^## [^#]/{exit} found{print}' "$run_dir/THOUGHTS.md" 2>/dev/null | sed 's/^/  /' || echo "  (See source file)"
        else
            echo "  No thoughts recorded."
        fi
        echo ""

        # Decisions section
        echo "# Decisions Made"
        echo "decisions:"
        if [[ -f "$run_dir/DECISIONS.yaml" ]]; then
            cat "$run_dir/DECISIONS.yaml" | sed 's/^/  /'
        elif [[ -f "$run_dir/DECISIONS.md" ]]; then
            parse_decisions_md "$run_dir/DECISIONS.md" | sed 's/^/  /'
        else
            echo "  []"
        fi
        echo ""

        # Assumptions section
        echo "# Assumptions"
        echo "assumptions:"
        if [[ -f "$run_dir/ASSUMPTIONS.md" ]]; then
            parse_assumptions_md "$run_dir/ASSUMPTIONS.md" | sed 's/^/  /'
        else
            echo "  []"
        fi
        echo ""

        # Results section
        echo "# Results and Outcomes"
        echo "results:"
        echo "  content: |"
        if [[ -f "$run_dir/RESULTS.md" ]]; then
            # Extract outcome section or full content
            awk 'BEGIN{found=0} /^## Outcome/{found=1; next} found && /^## [^#]/{exit} found{print}' "$run_dir/RESULTS.md" 2>/dev/null | sed 's/^/    /' || cat "$run_dir/RESULTS.md" | sed 's/^/    /'
        else
            echo "    No results recorded."
        fi
        echo ""

        # Learnings section
        echo "# Learnings"
        echo "learnings:"
        if [[ -f "$run_dir/LEARNINGS.md" ]]; then
            parse_learnings_md "$run_dir/LEARNINGS.md" | sed 's/^/  /'
        else
            echo "  []"
        fi
        echo ""

        # Source files reference
        echo "# Source Files (for reference)"
        echo "source_files:"
        for file in THOUGHTS.md DECISIONS.md DECISIONS.yaml ASSUMPTIONS.md RESULTS.md LEARNINGS.md; do
            if [[ -f "$run_dir/$file" ]]; then
                echo "  - $file"
            fi
        done

    } > "$run_yaml"

    echo -e "${GREEN}  Created: RUN.yaml${NC}"

    # Remove original files unless --keep
    if [[ "$keep_originals" != "true" ]]; then
        for file in THOUGHTS.md DECISIONS.md DECISIONS.yaml DECISIONS.yml ASSUMPTIONS.md RESULTS.md LEARNINGS.md; do
            if [[ -f "$run_dir/$file" ]]; then
                rm "$run_dir/$file"
                echo "  Removed: $file"
            fi
        done
    fi

    ((STATS_SUCCESS++))
    return 0
}

# Find and process all run directories
process_all_runs() {
    echo -e "${BLUE}Scanning for run directories...${NC}"
    echo ""

    local keep_originals="$1"

    # Find all run-* directories
    while IFS= read -r -d '' run_dir; do
        consolidate_run "$run_dir" "$keep_originals"
    done < <(find "$RUNS_BASE" -type d -name "run-*" -print0 2>/dev/null || true)
}

# Main function
main() {
    local target=""
    local process_all=false
    local keep_originals=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -a|--all)
                process_all=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -k|--keep)
                keep_originals=true
                shift
                ;;
            -*)
                echo -e "${RED}ERROR: Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
            *)
                target="$1"
                shift
                ;;
        esac
    done

    # Validate arguments
    if [[ "$process_all" == "false" ]] && [[ -z "$target" ]]; then
        echo -e "${RED}ERROR: Must specify run directory or --all${NC}"
        show_help
        exit 1
    fi

    # Header
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Run Output Consolidation Tool                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
        echo ""
    fi

    # Process runs
    if [[ "$process_all" == "true" ]]; then
        process_all_runs "$keep_originals"
    else
        # Resolve relative paths
        if [[ ! "$target" = /* ]]; then
            target="$RUNS_BASE/$target"
        fi
        consolidate_run "$target" "$keep_originals"
    fi

    # Summary
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Consolidation Complete${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo "Total runs processed: $STATS_TOTAL"
    echo -e "  ${GREEN}Success: $STATS_SUCCESS${NC}"
    echo -e "  ${YELLOW}Skipped: $STATS_SKIPPED${NC}"
    echo -e "  ${RED}Failed: $STATS_FAILED${NC}"

    if [[ $STATS_FAILED -gt 0 ]]; then
        exit 1
    fi
}

# Run main
main "$@"
