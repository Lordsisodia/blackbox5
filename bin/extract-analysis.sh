#!/bin/bash
# extract-analysis.sh
# Extracts analysis sections from scout and executor reports into separate files
# Usage: extract-analysis.sh [report-file] or extract-analysis.sh --all

set -e

ANALYSIS_DIR="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/analyses"
SCOUT_DIR="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/scout-reports"
EXECUTOR_DIR="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/executor-reports"
INDEX_FILE="$ANALYSIS_DIR/index.yaml"

# Ensure analysis directory exists
mkdir -p "$ANALYSIS_DIR"

# Function to extract analysis from scout report
extract_scout_analysis() {
    local report_file="$1"
    local report_id=$(yq -r '.scout_report.id // .id' "$report_file" 2>/dev/null || echo "unknown")
    local timestamp=$(yq -r '.scout_report.timestamp // .timestamp' "$report_file" 2>/dev/null || echo "unknown")
    local output_file="$ANALYSIS_DIR/${report_id}.analysis.yaml"

    cat > "$output_file" << EOF
analysis:
  analysis_id: "ANALYSIS-${report_id}"
  report_id: "$report_id"
  report_type: "scout"
  source_file: "$report_file"
  extracted_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  timestamp: "$timestamp"

  summary:
    total_opportunities: $(yq -r '.scout_report.summary.total_opportunities // .summary.total_opportunities // 0' "$report_file" 2>/dev/null || echo 0)
    high_impact: $(yq -r '.scout_report.summary.high_impact // .summary.high_impact // 0' "$report_file" 2>/dev/null || echo 0)
    quick_wins: $(yq -r '.scout_report.summary.quick_wins // .summary.quick_wins // 0' "$report_file" 2>/dev/null || echo 0)
    patterns_found: $(yq -r '.scout_report.summary.patterns_found // .summary.patterns_found // 0' "$report_file" 2>/dev/null || echo 0)

  key_findings:
EOF

    # Extract top opportunities
    local count=$(yq -r '.scout_report.top_opportunities // .top_opportunities | length' "$report_file" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then
        for i in $(seq 0 $((count - 1))); do
            local opp_id=$(yq -r ".scout_report.top_opportunities[$i].id // .top_opportunities[$i].id" "$report_file" 2>/dev/null || echo "")
            local title=$(yq -r ".scout_report.top_opportunities[$i].title // .top_opportunities[$i].title" "$report_file" 2>/dev/null || echo "")
            local category=$(yq -r ".scout_report.top_opportunities[$i].category // .top_opportunities[$i].category" "$report_file" 2>/dev/null || echo "")
            local score=$(yq -r ".scout_report.top_opportunities[$i].total_score // .top_opportunities[$i].total_score" "$report_file" 2>/dev/null || echo 0)
            local action=$(yq -r ".scout_report.top_opportunities[$i].suggested_action // .top_opportunities[$i].suggested_action" "$report_file" 2>/dev/null || echo "")

            if [ -n "$opp_id" ] && [ "$opp_id" != "null" ]; then
                cat >> "$output_file" << EOF
    - finding_id: "$opp_id"
      title: "$title"
      category: "$category"
      score: $score
      recommendation: "$action"
EOF
            fi
        done
    fi

    # Extract patterns
    cat >> "$output_file" << EOF

  patterns:
EOF
    local pattern_count=$(yq -r '.scout_report.patterns // .patterns | length' "$report_file" 2>/dev/null || echo 0)
    if [ "$pattern_count" -gt 0 ]; then
        for i in $(seq 0 $((pattern_count - 1))); do
            local pattern_name=$(yq -r ".scout_report.patterns[$i].name // .patterns[$i].name" "$report_file" 2>/dev/null || echo "")
            local severity=$(yq -r ".scout_report.patterns[$i].severity // .patterns[$i].severity" "$report_file" 2>/dev/null || echo "")

            if [ -n "$pattern_name" ] && [ "$pattern_name" != "null" ]; then
                cat >> "$output_file" << EOF
    - pattern: "$pattern_name"
      severity: "$severity"
EOF
            fi
        done
    else
        echo "    []" >> "$output_file"
    fi

    # Extract recommendations
    cat >> "$output_file" << EOF

  recommendations:
EOF
    local rec_count=$(yq -r '.scout_report.recommendations // .recommendations | length' "$report_file" 2>/dev/null || echo 0)
    if [ "$rec_count" -gt 0 ]; then
        for i in $(seq 0 $((rec_count - 1))); do
            local rec_id=$(yq -r ".scout_report.recommendations[$i].opportunity_id // .recommendations[$i].opportunity_id" "$report_file" 2>/dev/null || echo "")
            local rec_title=$(yq -r ".scout_report.recommendations[$i].title // .recommendations[$i].title" "$report_file" 2>/dev/null || echo "")
            local rec_rationale=$(yq -r ".scout_report.recommendations[$i].rationale // .recommendations[$i].rationale" "$report_file" 2>/dev/null || echo "")

            if [ -n "$rec_id" ] && [ "$rec_id" != "null" ]; then
                cat >> "$output_file" << EOF
    - priority: $((i + 1))
      finding_id: "$rec_id"
      title: "$rec_title"
      rationale: "$rec_rationale"
EOF
            fi
        done
    else
        echo "    []" >> "$output_file"
    fi

    echo "  status: "extracted"" >> "$output_file"
    echo "Extracted: $output_file"
}

# Function to extract analysis from executor report
extract_executor_analysis() {
    local report_file="$1"
    local report_id=$(yq -r '.executor_report.id' "$report_file" 2>/dev/null || echo "unknown")
    local timestamp=$(yq -r '.executor_report.timestamp' "$report_file" 2>/dev/null || echo "unknown")
    local output_file="$ANALYSIS_DIR/${report_id}.analysis.yaml"

    cat > "$output_file" << EOF
analysis:
  analysis_id: "ANALYSIS-${report_id}"
  report_id: "$report_id"
  report_type: "executor"
  source_file: "$report_file"
  extracted_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  timestamp: "$timestamp"

  summary:
    total_tasks: $(yq -r '.executor_report.summary.total_tasks // 0' "$report_file" 2>/dev/null || echo 0)
    successful: $(yq -r '.executor_report.summary.successful // 0' "$report_file" 2>/dev/null || echo 0)
    failed: $(yq -r '.executor_report.summary.failed // 0' "$report_file" 2>/dev/null || echo 0)
    success_rate: $(yq -r '.executor_report.summary.success_rate // 0' "$report_file" 2>/dev/null || echo 0)

  key_findings:
EOF

    # Extract task results as findings
    local count=$(yq -r '.executor_report.results | length' "$report_file" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then
        for i in $(seq 0 $((count - 1))); do
            local task_id=$(yq -r ".executor_report.results[$i].task_id" "$report_file" 2>/dev/null || echo "")
            local success=$(yq -r ".executor_report.results[$i].success" "$report_file" 2>/dev/null || echo "false")
            local action=$(yq -r ".executor_report.results[$i].action_taken" "$report_file" 2>/dev/null || echo "")
            local error=$(yq -r ".executor_report.results[$i].error_message" "$report_file" 2>/dev/null || echo "")

            if [ -n "$task_id" ] && [ "$task_id" != "null" ]; then
                local status="completed"
                if [ "$success" = "false" ]; then
                    status="failed"
                fi

                cat >> "$output_file" << EOF
    - finding_id: "$task_id"
      title: "$action"
      category: "execution"
      status: "$status"
      error: "$error"
EOF
            fi
        done
    fi

    echo "" >> "$output_file"
    echo "  status: "extracted"" >> "$output_file"
    echo "Extracted: $output_file"
}

# Function to update the analysis index
update_index() {
    local index_file="$INDEX_FILE"

    cat > "$index_file" << EOF
analysis_index:
  version: "1.0.0"
  generated_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  total_analyses: 0
  analyses:
EOF

    local count=0
    for analysis_file in "$ANALYSIS_DIR"/*.analysis.yaml; do
        if [ -f "$analysis_file" ]; then
            local analysis_id=$(yq -r '.analysis.analysis_id' "$analysis_file" 2>/dev/null || echo "unknown")
            local report_id=$(yq -r '.analysis.report_id' "$analysis_file" 2>/dev/null || echo "unknown")
            local report_type=$(yq -r '.analysis.report_type' "$analysis_file" 2>/dev/null || echo "unknown")
            local timestamp=$(yq -r '.analysis.timestamp' "$analysis_file" 2>/dev/null || echo "unknown")
            local source_file=$(yq -r '.analysis.source_file' "$analysis_file" 2>/dev/null || echo "")

            cat >> "$index_file" << EOF
    - analysis_id: "$analysis_id"
      report_id: "$report_id"
      report_type: "$report_type"
      timestamp: "$timestamp"
      source_file: "$source_file"
      analysis_file: "$analysis_file"
EOF
            count=$((count + 1))
        fi
    done

    # Update total count
    sed -i.bak "s/total_analyses: 0/total_analyses: $count/" "$index_file"
    rm -f "$index_file.bak"

    echo "Index updated: $count analyses indexed"
}

# Main execution
if [ "$1" = "--all" ]; then
    echo "Processing all reports..."

    # Process scout reports
    if [ -d "$SCOUT_DIR" ]; then
        for report in "$SCOUT_DIR"/*.yaml; do
            if [ -f "$report" ]; then
                extract_scout_analysis "$report"
            fi
        done
    fi

    # Process executor reports
    if [ -d "$EXECUTOR_DIR" ]; then
        for report in "$EXECUTOR_DIR"/*.yaml; do
            if [ -f "$report" ]; then
                extract_executor_analysis "$report"
            fi
        done
    fi

    # Update index
    update_index

    echo "Extraction complete."

elif [ -n "$1" ]; then
    # Process single file
    if [ -f "$1" ]; then
        if echo "$1" | grep -q "scout"; then
            extract_scout_analysis "$1"
        elif echo "$1" | grep -q "EXEC"; then
            extract_executor_analysis "$1"
        else
            echo "Unknown report type: $1"
            exit 1
        fi
        update_index
    else
        echo "File not found: $1"
        exit 1
    fi
else
    echo "Usage: $0 [--all | <report-file>]"
    echo ""
    echo "Options:"
    echo "  --all          Process all reports in scout-reports/ and executor-reports/"
    echo "  <report-file>  Process a single report file"
    echo ""
    echo "Examples:"
    echo "  $0 --all"
    echo "  $0 $SCOUT_DIR/scout-report-20260204.yaml"
    exit 1
fi
