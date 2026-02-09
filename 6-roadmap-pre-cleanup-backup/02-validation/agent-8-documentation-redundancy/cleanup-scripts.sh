#!/bin/bash

# BlackBox5 Documentation Cleanup Scripts
# Use with caution - test before running on production!

cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5

echo "=== BlackBox5 Documentation Cleanup Scripts ==="
echo ""
echo "WARNING: Test these commands before running!"
echo ""

# Script 1: Update .blackbox5 references
echo "### Script 1: Fix .blackbox5 references ###"
echo "find . -type f -name '*.md' -exec sed -i '' 's/\.blackbox5\//blackbox5\//g' {} \;"
echo ""
echo "# OR for dry-run (preview changes):"
echo "find . -type f -name '*.md' -exec sed -i '' 's/\.blackbox5\//blackbox5\//g' {} +"
echo ""

# Script 2: Delete duplicate code_index files
echo "### Script 2: Remove duplicate code_index.md files ###"
echo "# Backup first!"
echo "mkdir -p /tmp/blackbox5-backup"
echo "cp 5-project-memory/_template/knowledge/codebase/code_index.md /tmp/blackbox5-backup/"
echo "cp 5-project-memory/code_index.md /tmp/blackbox5-backup/"
echo ""
echo "rm 5-project-memory/_template/knowledge/codebase/code_index.md"
echo "rm 5-project-memory/code_index.md"
echo ""

# Script 3: Archive orphaned files
echo "### Script 3: Archive orphaned implementation summaries ###"
echo "mkdir -p 6-roadmap/03-completed/implementation-archive"
echo ""
echo orphaned_files=(
    "1-docs/02-implementation/06-tools/tools/TOOLS-IMPLEMENTATION-SUMMARY.md"
    "1-docs/02-implementation/06-tools/skills/SKILLS-IMPORT-COMPLETE.md"
    "1-docs/02-implementation/06-tools/skills/SKILLS-CONVERSION-FINAL-SUMMARY.md"
    "1-docs/02-implementation/06-tools/skills/SKILLS-CONVERSION-BATCH-COMPLETE.md"
    "1-docs/02-implementation/01-agents/parallel/PARALLEL-AGENT-WORK-COMPLETE.md"
    "1-docs/02-implementation/01-agents/task/TASK-AGENT-IMPLEMENTATION-COMPLETE.md"
    "1-docs/02-implementation/05-memory-implementation/context/CONTEXT-EXTRACTION-SUMMARY.md"
    "1-docs/02-implementation/05-memory-implementation/todo/TODO-IMPLEMENTATION-SUMMARY.md"
    "1-docs/02-implementation/05-memory-implementation/project-memory/PROJECT-MEMORY-IMPLEMENTATION-SUMMARY.md"
    "1-docs/02-implementation/02-core-systems/checkpoint/CHECKPOINT-PROTOCOL-FINAL-SUMMARY.md"
    "1-docs/02-implementation/02-core-systems/atomic-commits/ATOMIC-COMMITS-SUMMARY.md"
    "1-docs/02-implementation/01-core/middleware/GUIDE-MIDDLEWARE-SUMMARY.md"
    "1-docs/02-implementation/01-core/general/MANIFEST-IMPLEMENTATION-SUMMARY.md"
    "1-docs/02-implementation/01-core/state/STATE_MANAGER_IMPLEMENTATION_SUMMARY.md"
    "1-docs/02-implementation/01-core/resilience/CIRCUIT_BREAKER_SUMMARY.md"
    "1-docs/02-implementation/01-core/communication/EVENT_BUS_SUMMARY.md"
    "1-docs/02-implementation/03-pipeline/feature/PIPELINE-INTEGRATION-SUMMARY.md"
    "1-docs/01-theory/03-workflows/adaptive/ENHANCED-WORKFLOW-EXECUTION-SUMMARY.md"
)

echo "for file in \"\${orphaned_files[@]}\"; do"
echo "  if [ -f \"\$file\" ]; then"
echo "    mv \"\$file\" 6-roadmap/03-completed/implementation-archive/"
echo "    echo \"Archived: \$file\""
echo "  fi"
echo "done"
echo ""

# Script 4: Remove empty README files
echo "### Script 4: Remove empty/minimal README files ###"
echo "find . -type f -name 'README.md' -size -100c -not -path '*/node_modules/*'"
echo ""

# Script 5: Standardize naming (BlackBox -> BlackBox5)
echo "### Script 5: Standardize 'BlackBox' to 'BlackBox5' ###"
echo "# Be careful - this might affect legitimate 'BlackBox' references"
echo "find . -type f -name '*.md' -exec sed -i '' 's/BlackBox[^5]/BlackBox5/g' {} \;"
echo ""

# Script 6: Create documentation index
echo "### Script 6: Generate documentation index ###"
cat << 'INDEX_SCRIPT'
#!/bin/bash
echo "# BlackBox5 Documentation Index"
echo ""
echo "## Core Theory"
find 1-docs/01-theory -type f -name "*.md" | sort
echo ""
echo "## Implementation Guides"
find 1-docs/02-implementation -type f -name "*.md" | sort
echo ""
echo "## User Guides"
find 1-docs/03-guides -type f -name "*.md" | sort
INDEX_SCRIPT

echo ""
echo "=== End of Cleanup Scripts ==="
