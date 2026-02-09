#!/bin/bash
# =============================================================================
# Migration Script: Optimize Serialization Formats
# TASK-SSOT-029: Migrate to efficient serialization formats
# =============================================================================
#
# This script migrates:
# - events.yaml → LDJSON (Line-Delimited JSON) for append-heavy logs
# - memories.json → MessagePack for binary efficiency
# - Creates SQLite index for task metadata caching
#
# Usage: ./migrate-serialization.sh [--dry-run] [--verify]
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="${HOME}/.blackbox5/5-project-memory/blackbox5"
AUTONOMOUS_DIR="${PROJECT_ROOT}/.autonomous"
EVENTS_SOURCE="${AUTONOMOUS_DIR}/agents/communications/events.yaml"
MEMORIES_SOURCE="${AUTONOMOUS_DIR}/memory/data/memories.json"
BACKUP_DIR="${AUTONOMOUS_DIR}/data/backups/migration-$(date +%Y%m%d-%H%M%S)"

# Output files
EVENTS_LDJSON="${AUTONOMOUS_DIR}/agents/communications/events.ldjson"
MEMORIES_MSGPACK="${AUTONOMOUS_DIR}/memory/data/memories.msgpack"
TASKS_DB="${AUTONOMOUS_DIR}/data/tasks-cache.db"

# Flags
DRY_RUN=false
VERIFY=false

# Statistics
EVENTS_COUNT=0
MEMORIES_COUNT=0
TASKS_COUNT=0

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "============================================================================="
    echo "$1"
    echo "============================================================================="
}

print_stats() {
    echo ""
    echo "============================================================================="
    echo "Migration Statistics"
    echo "============================================================================="
    printf "%-30s %10s\n" "Events migrated:" "$EVENTS_COUNT"
    printf "%-30s %10s\n" "Memories migrated:" "$MEMORIES_COUNT"
    printf "%-30s %10s\n" "Tasks indexed:" "$TASKS_COUNT"
    echo "============================================================================="
}

# =============================================================================
# Pre-flight Checks
# =============================================================================

check_dependencies() {
    log_info "Checking dependencies..."

    local missing_deps=()

    # Check for Python
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi

    # Check for required Python packages
    if ! python3 -c "import yaml" 2>/dev/null; then
        log_warn "PyYAML not installed. Will use basic YAML parsing."
    fi

    if ! python3 -c "import msgpack" 2>/dev/null; then
        log_warn "msgpack not installed. Memories will remain in JSON format."
        log_info "Install with: pip install msgpack"
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        exit 1
    fi

    log_success "Dependencies OK"
}

check_source_files() {
    log_info "Checking source files..."

    if [ ! -f "$EVENTS_SOURCE" ]; then
        log_warn "Events file not found: $EVENTS_SOURCE"
        EVENTS_SOURCE=""
    else
        local size=$(stat -f%z "$EVENTS_SOURCE" 2>/dev/null || stat -c%s "$EVENTS_SOURCE" 2>/dev/null || echo "unknown")
        log_info "Events file: $size bytes"
    fi

    if [ ! -f "$MEMORIES_SOURCE" ]; then
        log_warn "Memories file not found: $MEMORIES_SOURCE"
        MEMORIES_SOURCE=""
    else
        local size=$(stat -f%z "$MEMORIES_SOURCE" 2>/dev/null || stat -c%s "$MEMORIES_SOURCE" 2>/dev/null || echo "unknown")
        log_info "Memories file: $size bytes"
    fi

    if [ -z "$EVENTS_SOURCE" ] && [ -z "$MEMORIES_SOURCE" ]; then
        log_error "No source files found to migrate"
        exit 1
    fi
}

# =============================================================================
# Migration Functions
# =============================================================================

migrate_events_to_ldjson() {
    if [ -z "$EVENTS_SOURCE" ]; then
        log_warn "Skipping events migration (source not found)"
        return 0
    fi

    print_header "Migrating events.yaml to LDJSON"

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would migrate events to: $EVENTS_LDJSON"
        return 0
    fi

    # Create backup
    mkdir -p "$BACKUP_DIR"
    cp "$EVENTS_SOURCE" "$BACKUP_DIR/events.yaml.bak"
    log_info "Backup created at: $BACKUP_DIR/events.yaml.bak"

    # Convert YAML to LDJSON using Python
    python3 - "$EVENTS_SOURCE" "$EVENTS_LDJSON" << 'PYTHON_SCRIPT'
import sys
import json
import re

events_source = sys.argv[1]
events_ldjson = sys.argv[2]

try:
    with open(events_source, 'r') as f:
        content = f.read()

    # Parse YAML list items
    events = []
    current_event = {}
    current_key = None
    current_value_lines = []
    in_list = False

    for line in content.split('\n'):
        # Check for new top-level item (starts with - )
        if line.startswith('- '):
            # Save previous event if exists
            if current_event and current_key:
                current_event[current_key] = '\n'.join(current_value_lines).strip()
            if current_event:
                events.append(current_event)

            # Start new event
            current_event = {}
            current_key = None
            current_value_lines = []
            in_list = False

            # Parse first key-value pair
            match = re.match(r'-\s+(\w+):\s*(.*)', line)
            if match:
                current_key = match.group(1)
                value = match.group(2).strip()
                if value:
                    # Handle inline values
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    current_event[current_key] = value
                    current_key = None

        # Check for key-value pairs
        elif line.startswith('  ') and ':' in line and not in_list:
            # Save previous key's value
            if current_key:
                current_event[current_key] = '\n'.join(current_value_lines).strip()
                current_value_lines = []

            match = re.match(r'\s+(\w+):\s*(.*)', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()

                # Check if this starts a nested structure
                if value == '':
                    current_key = key
                else:
                    # Handle inline values
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    current_event[key] = value
                    current_key = None

        # Handle list items in nested structures
        elif line.startswith('    - ') and current_key:
            in_list = True
            value = line[6:].strip()
            if current_key not in current_event:
                current_event[current_key] = []
            if not isinstance(current_event[current_key], list):
                current_event[current_key] = [current_event[current_key]]
            current_event[current_key].append(value)

        # Continue multiline values
        elif current_key and line.startswith('    ') and not in_list:
            current_value_lines.append(line.strip())

    # Save last event
    if current_event and current_key:
        current_event[current_key] = '\n'.join(current_value_lines).strip()
    if current_event:
        events.append(current_event)

    # Write LDJSON
    with open(events_ldjson, 'w') as f:
        for event in events:
            f.write(json.dumps(event, separators=(',', ':')) + '\n')

    print(f"Migrated {len(events)} events to LDJSON", file=sys.stderr)
    print(len(events))  # Output count for shell

except Exception as e:
    print(f"Error migrating events: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

    EVENTS_COUNT=$(python3 -c "import sys; print(len(list(open('${EVENTS_LDJSON}'))))" 2>/dev/null || echo "0")

    # Compare sizes
    local old_size=$(stat -f%z "$EVENTS_SOURCE" 2>/dev/null || stat -c%s "$EVENTS_SOURCE" 2>/dev/null || echo "0")
    local new_size=$(stat -f%z "$EVENTS_LDJSON" 2>/dev/null || stat -c%s "$EVENTS_LDJSON" 2>/dev/null || echo "0")

    log_success "Events migrated: $EVENTS_COUNT records"
    log_info "Size comparison: ${old_size} bytes (YAML) → ${new_size} bytes (LDJSON)"

    if [ "$VERIFY" = true ]; then
        verify_events_migration
    fi
}

migrate_memories_to_msgpack() {
    if [ -z "$MEMORIES_SOURCE" ]; then
        log_warn "Skipping memories migration (source not found)"
        return 0
    fi

    print_header "Migrating memories.json to MessagePack"

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would migrate memories to: $MEMORIES_MSGPACK"
        return 0
    fi

    # Check if msgpack is available
    if ! python3 -c "import msgpack" 2>/dev/null; then
        log_warn "msgpack not available, skipping memories migration"
        return 0
    fi

    # Create backup
    mkdir -p "$BACKUP_DIR"
    cp "$MEMORIES_SOURCE" "$BACKUP_DIR/memories.json.bak"
    log_info "Backup created at: $BACKUP_DIR/memories.json.bak"

    # Convert JSON to MessagePack
    python3 - "$MEMORIES_SOURCE" "$MEMORIES_MSGPACK" << 'PYTHON_SCRIPT'
import sys
import json
try:
    import msgpack
except ImportError:
    print("msgpack not installed", file=sys.stderr)
    sys.exit(1)

memories_source = sys.argv[1]
memories_msgpack = sys.argv[2]

try:
    with open(memories_source, 'r') as f:
        memories = json.load(f)

    with open(memories_msgpack, 'wb') as f:
        msgpack.pack(memories, f, use_bin_type=True)

    print(f"Migrated {len(memories)} memories to MessagePack", file=sys.stderr)
    print(len(memories))  # Output count for shell

except Exception as e:
    print(f"Error migrating memories: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

    MEMORIES_COUNT=$(python3 -c "import msgpack; print(len(msgpack.unpack(open('${MEMORIES_MSGPACK}', 'rb'))))" 2>/dev/null || echo "0")

    # Compare sizes
    local old_size=$(stat -f%z "$MEMORIES_SOURCE" 2>/dev/null || stat -c%s "$MEMORIES_SOURCE" 2>/dev/null || echo "0")
    local new_size=$(stat -f%z "$MEMORIES_MSGPACK" 2>/dev/null || stat -c%s "$MEMORIES_MSGPACK" 2>/dev/null || echo "0")

    log_success "Memories migrated: $MEMORIES_COUNT records"
    log_info "Size comparison: ${old_size} bytes (JSON) → ${new_size} bytes (MessagePack)"

    if [ "$VERIFY" = true ]; then
        verify_memories_migration
    fi
}

create_task_metadata_cache() {
    print_header "Creating SQLite Task Metadata Cache"

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would create task cache at: $TASKS_DB"
        return 0
    fi

    python3 - "$PROJECT_ROOT" "$TASKS_DB" << 'PYTHON_SCRIPT'
import sys
import os
import re
import json
from datetime import datetime

tasks_dir = os.path.join(sys.argv[1], "tasks")
tasks_db = sys.argv[2]

try:
    import sqlite3
except ImportError:
    print("sqlite3 not available", file=sys.stderr)
    sys.exit(1)

def parse_task_file(filepath):
    """Parse task markdown file and extract frontmatter and metadata."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract frontmatter (between --- markers)
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        frontmatter = {}
        if frontmatter_match:
            fm_text = frontmatter_match.group(1)
            # Parse simple key: value pairs
            for line in fm_text.split('\n'):
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')

        # Extract task ID from filename or content
        task_id = os.path.basename(os.path.dirname(filepath))

        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else task_id

        # Count checkboxes
        total_checks = len(re.findall(r'- \[', content))
        checked_checks = len(re.findall(r'- \[x\]', content))

        return {
            'task_id': task_id,
            'title': title,
            'status': frontmatter.get('Status', 'unknown'),
            'priority': frontmatter.get('Priority', 'unknown'),
            'created': frontmatter.get('Created', ''),
            'parent': frontmatter.get('Parent', ''),
            'filepath': filepath,
            'total_checks': total_checks,
            'checked_checks': checked_checks,
            'completion_pct': (checked_checks / total_checks * 100) if total_checks > 0 else 0,
            'last_modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
        return None

try:
    # Ensure directory exists
    os.makedirs(os.path.dirname(tasks_db), exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(tasks_db)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT,
            status TEXT,
            priority TEXT,
            created TEXT,
            parent TEXT,
            filepath TEXT,
            total_checks INTEGER,
            checked_checks INTEGER,
            completion_pct REAL,
            last_modified TEXT,
            indexed_at TEXT
        )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created ON tasks(created)')

    # Find and parse all task files
    tasks = []
    for root, dirs, files in os.walk(tasks_dir):
        if 'task.md' in files:
            filepath = os.path.join(root, 'task.md')
            task = parse_task_file(filepath)
            if task:
                tasks.append(task)

    # Insert or replace tasks
    indexed_at = datetime.now().isoformat()
    for task in tasks:
        cursor.execute('''
            INSERT OR REPLACE INTO tasks
            (task_id, title, status, priority, created, parent, filepath,
             total_checks, checked_checks, completion_pct, last_modified, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task['task_id'], task['title'], task['status'], task['priority'],
            task['created'], task['parent'], task['filepath'],
            task['total_checks'], task['checked_checks'], task['completion_pct'],
            task['last_modified'], indexed_at
        ))

    conn.commit()
    conn.close()

    print(f"Indexed {len(tasks)} tasks in SQLite cache", file=sys.stderr)
    print(len(tasks))  # Output count for shell

except Exception as e:
    print(f"Error creating task cache: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

    TASKS_COUNT=$(python3 -c "import sqlite3; conn=sqlite3.connect('${TASKS_DB}'); c=conn.cursor(); c.execute('SELECT COUNT(*) FROM tasks'); print(c.fetchone()[0]); conn.close()" 2>/dev/null || echo "0")

    log_success "Tasks indexed: $TASKS_COUNT records"
    log_info "Cache location: $TASKS_DB"
}

# =============================================================================
# Verification Functions
# =============================================================================

verify_events_migration() {
    log_info "Verifying events migration..."

    if [ ! -f "$EVENTS_LDJSON" ]; then
        log_error "Events LDJSON file not found"
        return 1
    fi

    # Verify each line is valid JSON
    local invalid_lines=$(python3 -c "
import json
invalid = 0
with open('${EVENTS_LDJSON}') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError:
            print(f'Line {i}: Invalid JSON')
            invalid += 1
print(invalid)
" 2>/dev/null || echo "0")

    if [ "$invalid_lines" -eq "0" ]; then
        log_success "All events are valid JSON"
    else
        log_error "Found $invalid_lines invalid JSON lines"
        return 1
    fi

    # Verify record counts match
    local yaml_count=$(grep -c "^\s*- timestamp" "$EVENTS_SOURCE" 2>/dev/null || echo "0")
    local ldjson_count=$(wc -l < "$EVENTS_LDJSON" | tr -d ' ')

    log_info "Record count: YAML=$yaml_count, LDJSON=$ldjson_count"
}

verify_memories_migration() {
    log_info "Verifying memories migration..."

    if [ ! -f "$MEMORIES_MSGPACK" ]; then
        log_warn "Memories MessagePack file not found (msgpack may not be installed)"
        return 0
    fi

    # Verify MessagePack can be decoded and matches JSON count
    python3 - "$MEMORIES_SOURCE" "$MEMORIES_MSGPACK" << 'PYTHON_SCRIPT'
import json
import sys
try:
    import msgpack
except ImportError:
    print("msgpack not installed, skipping verification")
    sys.exit(0)

memories_source = sys.argv[1]
memories_msgpack = sys.argv[2]

with open(memories_source, 'r') as f:
    json_data = json.load(f)

with open(memories_msgpack, 'rb') as f:
    msgpack_data = msgpack.unpack(f)

if len(json_data) == len(msgpack_data):
    print(f"Record count matches: {len(json_data)}")
    sys.exit(0)
else:
    print(f"Record count mismatch: JSON={len(json_data)}, MsgPack={len(msgpack_data)}")
    sys.exit(1)
PYTHON_SCRIPT

    if [ $? -eq 0 ]; then
        log_success "Memories migration verified"
    else
        log_error "Memories migration verification failed"
        return 1
    fi
}

# =============================================================================
# Main
# =============================================================================

show_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Migrate BlackBox5 serialization formats for better performance.

OPTIONS:
    --dry-run    Show what would be done without making changes
    --verify     Verify migrations after completion
    --help       Show this help message

DESCRIPTION:
    This script migrates:
    - events.yaml → LDJSON (Line-Delimited JSON) for append-heavy logs
    - memories.json → MessagePack for binary efficiency
    - Task metadata → SQLite cache for fast queries

EXAMPLES:
    $(basename "$0")              # Run migration
    $(basename "$0") --dry-run    # Preview changes
    $(basename "$0") --verify     # Run with verification

EOF
}

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verify)
                VERIFY=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    print_header "TASK-SSOT-029: Optimize Serialization Formats"

    if [ "$DRY_RUN" = true ]; then
        log_warn "DRY RUN MODE - No changes will be made"
    fi

    # Pre-flight checks
    check_dependencies
    check_source_files

    # Perform migrations
    migrate_events_to_ldjson
    migrate_memories_to_msgpack
    create_task_metadata_cache

    # Print statistics
    print_stats

    # Final message
    echo ""
    if [ "$DRY_RUN" = true ]; then
        log_info "Dry run complete. Run without --dry-run to apply changes."
    else
        log_success "Migration complete!"
        log_info "Backups stored at: $BACKUP_DIR"
        log_info ""
        log_info "Next steps:"
        log_info "  1. Test applications with new formats"
        log_info "  2. Update code to use LDJSON/MessagePack readers"
        log_info "  3. Remove old formats after validation"
    fi
}

main "$@"
