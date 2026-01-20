#!/bin/bash

# BlackBox5 Roadmap → Project Memory Migration Script
# Created: 2026-01-20
# Purpose: Move reference knowledge from roadmap to project memory

set -euo pipefail

# Paths
ROOT="/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL"
BLACKBOX5="$ROOT/blackbox5"
ROADMAP="$BLACKBOX5/6-roadmap"
MEMORY="$BLACKBOX5/5-project-memory/blackbox5"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[DONE]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Phase 1: Move reference research docs
log_info "Phase 1: Moving reference research documents..."
mkdir -p "$MEMORY/knowledge/research"

# Core research reference docs
cp "$ROADMAP/research/BLACKBOX5-RESEARCH-CATEGORIES.md" "$MEMORY/knowledge/research/categories.md"
cp "$ROADMAP/research/FIRST-PRINCIPLES-ANALYSIS.md" "$MEMORY/knowledge/research/first-principles.md"
cp "$ROADMAP/research/VALIDATION-PLAN.md" "$MEMORY/knowledge/research/validation-plan.md"
cp "$ROADMAP/research/README.md" "$MEMORY/knowledge/research/README.md"

# Vision to project identity
cp "$ROADMAP/research/BLACKBOX5-VISION-AND-FLOW.md" "$MEMORY/project/vision.md"

log_success "Phase 1 complete: Reference research docs moved"

# Phase 2: Move first-principles knowledge
log_info "Phase 2: Moving first-principles knowledge..."
mkdir -p "$MEMORY/knowledge/first-principles"
cp -r "$ROADMAP/first-principles/"* "$MEMORY/knowledge/first-principles/"

# Move Ralph PRD to plans
cp "$ROADMAP/first-principles/RALPH-LOOP-PRD.md" "$MEMORY/plans/features/ralph-loop-prd.md"

log_success "Phase 2 complete: First-principles knowledge moved"

# Phase 3: Move framework research
log_info "Phase 3: Moving framework research..."
mkdir -p "$MEMORY/knowledge/frameworks"
cp -r "$ROADMAP/frameworks/"* "$MEMORY/knowledge/frameworks/"

log_success "Phase 3 complete: Framework research moved"

# Phase 4: Move Ralph integration research
log_info "Phase 4: Moving Ralph integration research..."
mkdir -p "$MEMORY/knowledge/ralph-integration"
cp -r "$ROADMAP/framework-research/ralphy-integration/"* "$MEMORY/knowledge/ralph-integration/"

log_success "Phase 4 complete: Ralph integration research moved"

# Phase 5: Move Ralph loop sessions
log_info "Phase 5: Moving Ralph loop sessions..."
mkdir -p "$MEMORY/knowledge/ralph-loop/sessions"
if [ -d "$ROADMAP/first-principles/ralph-loop-sessions" ]; then
  cp -r "$ROADMAP/first-principles/ralph-loop-sessions/"* "$MEMORY/knowledge/ralph-loop/sessions/"
fi

log_success "Phase 5 complete: Ralph loop sessions moved"

# Phase 6: Move validation findings
log_info "Phase 6: Moving validation findings..."
mkdir -p "$MEMORY/knowledge/validation"
mkdir -p "$MEMORY/knowledge/architecture"

# Consolidated report
cp "$ROADMAP/02-validation/CONSOLIDATED-REPORT.md" "$MEMORY/knowledge/validation/consolidated-report.md"

# Individual validation findings
for agent_dir in "$ROADMAP/02-validation"/agent-*; do
  if [ -d "$agent_dir" ]; then
    agent_name=$(basename "$agent_dir")
    # Findings to knowledge/validation
    if [ -f "$agent_dir/VALIDATION-FINDINGS.md" ]; then
      cp "$agent_dir/VALIDATION-FINDINGS.md" "$MEMORY/knowledge/validation/${agent_name}-findings.md"
    fi
    # README to knowledge/validation
    if [ -f "$agent_dir/README.md" ]; then
      cp "$agent_dir/README.md" "$MEMORY/knowledge/validation/${agent_name}-overview.md"
    fi
    # Architecture diagrams
    if [ -f "$agent_dir/ARCHITECTURE-DIAGRAM.md" ]; then
      cp "$agent_dir/ARCHITECTURE-DIAGRAM.md" "$MEMORY/knowledge/architecture/${agent_name}-diagram.md"
    fi
    if [ -f "$agent_dir/SKILLS-SYSTEM-DIAGRAM.md" ]; then
      cp "$agent_dir/SKILLS-SYSTEM-DIAGRAM.md" "$MEMORY/knowledge/architecture/skills-diagram.md"
    fi
    if [ -f "$agent_dir/WORKFLOW-DIAGRAM.md" ]; then
      cp "$agent_dir/WORKFLOW-DIAGRAM.md" "$MEMORY/knowledge/architecture/workflow-diagram.md"
    fi
    # Action checklists to tasks backlog
    if [ -f "$agent_dir/ACTION-CHECKLIST.md" ]; then
      cp "$agent_dir/ACTION-CHECKLIST.md" "$MEMORY/tasks/backlog/validation-${agent_name}-actions.md"
    fi
  fi
done

log_success "Phase 6 complete: Validation findings moved"

# Phase 7: Move archives
log_info "Phase 7: Moving archives..."
mkdir -p "$MEMORY/knowledge/archives"
cp -r "$ROADMAP/archives/"* "$MEMORY/knowledge/archives/"

log_success "Phase 7 complete: Archives moved"

# Phase 8: Extract research findings (keep logs in roadmap)
log_info "Phase 8: Extracting research findings to knowledge..."

for research_dir in "$ROADMAP/01-research"/*; do
  if [ -d "$research_dir" ]; then
    category_name=$(basename "$research_dir")

    # Create destination
    mkdir -p "$MEMORY/knowledge/research/$category_name/findings"

    # Move findings if they exist
    if [ -d "$research_dir/findings" ]; then
      cp -r "$research_dir/findings/"* "$MEMORY/knowledge/research/$category_name/findings/"
      log_info "  Extracted findings for: $category_name"
    fi

    # Keep research-log.md and session-summaries in roadmap
    # These are active research tracking, not reference knowledge
  fi
done

log_success "Phase 8 complete: Research findings extracted"

# Summary
echo ""
log_success "==========================================="
log_success "Migration Complete!"
log_success "==========================================="
echo ""
log_info "Summary of changes:"
log_info "  - Reference research docs → knowledge/research/"
log_info "  - First-principles → knowledge/first-principles/"
log_info "  - Framework research → knowledge/frameworks/"
log_info "  - Ralph integration → knowledge/ralph-integration/"
log_info "  - Validation findings → knowledge/validation/"
log_info "  - Archives → knowledge/archives/"
log_info "  - Research findings → knowledge/research/{category}/"
log_info ""
log_info "Remaining in roadmap (6-roadmap/):"
log_info "  - Active research logs (research-log.md)"
log_info "  - Session summaries"
log_info "  - Proposals (00-proposed)"
log_info "  - Plans (03-planned)"
log_info "  - Active work (04-active)"
log_info ""
log_warn "IMPORTANT: Review moved files and update internal links!"
log_warn "Run: find $MEMORY -name '*.md' -exec grep -l '6-roadmap' {} \;"
echo ""
