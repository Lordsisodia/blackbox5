# PLAN.md: Add File Locking to Shell Scripts

**Task:** TASK-SSOT-026 - Shell scripts lack file locking mechanisms
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Shell scripts throughout the codebase perform file operations without any locking:
- `ralf-loop.sh` reads/writes state files
- `bb5-*.sh` scripts modify task files
- Hook scripts update event files
- No protection against concurrent access

This creates:
1. **Race Conditions**: Multiple scripts can modify same file
2. **Data Corruption**: Partial writes possible
3. **Lost Updates**: One script overwrites another's changes
4. **Inconsistent State**: Files in partially updated state
5. **No Coordination**: Scripts don't coordinate access

### First Principles Solution
- **File Locking**: Use `flock` for exclusive/shared locks
- **Atomic Operations**: Write to temp file, then move
- **Lock Files**: Separate lock files for coordination
- **Timeout Handling**: Don't wait forever for locks
- **Error Handling**: Graceful handling of lock failures

---

## 2. Current State Analysis

### Current Shell Script Patterns

```bash
# Pattern 1: Direct read
data=$(cat file.yaml)

# Pattern 2: Direct write
echo "$data" > file.yaml

# Pattern 3: Read-modify-write
current=$(cat counter.txt)
new=$((current + 1))
echo $new > counter.txt

# Pattern 4: Append
echo "new entry" >> log.txt
```

### Race Condition Scenario

```bash
# Script A                    # Script B
# --------                    # --------
read: value=5                 read: value=5

compute: new=6                compute: new=7

write: value=6
                              write: value=7
                              # A's update LOST!
```

---

## 3. Proposed Solution

### Locking Utilities for Shell

**File:** `2-engine/.autonomous/lib/locking.sh`

```bash
#!/bin/bash
# File locking utilities for shell scripts

# Acquire exclusive lock
# Usage: acquire_lock /path/to/file.lock [timeout_seconds]
acquire_lock() {
    local lock_file="$1"
    local timeout="${2:-30}"
    local wait_time=0

    while true; do
        # Try to acquire lock
        exec 200>"$lock_file"
        if flock -n 200; then
            # Lock acquired
            echo "200"  # Return file descriptor
            return 0
        fi
        exec 200>&-

        # Check timeout
        if [ $wait_time -ge $timeout ]; then
            echo "ERROR: Could not acquire lock on $lock_file" >&2
            return 1
        fi

        # Wait and retry
        sleep 0.1
        wait_time=$(echo "$wait_time + 0.1" | bc)
    done
}

# Release lock
# Usage: release_lock $fd
release_lock() {
    local fd="$1"
    eval "exec $fd>&-"
}

# Atomic write
# Usage: atomic_write /path/to/file "content"
atomic_write() {
    local target_file="$1"
    local content="$2"
    local lock_file="${target_file}.lock"
    local temp_file="${target_file}.tmp.$$"

    # Acquire lock
    local fd
    fd=$(acquire_lock "$lock_file") || return 1

    # Write to temp file
    echo "$content" > "$temp_file"

    # Atomic move
    mv "$temp_file" "$target_file"

    # Release lock
    release_lock "$fd"

    return 0
}

# Safe read
# Usage: content=$(safe_read /path/to/file)
safe_read() {
    local target_file="$1"
    local lock_file="${target_file}.lock"

    # Acquire shared lock
    local fd
    fd=$(acquire_lock "$lock_file") || return 1

    # Read content
    cat "$target_file"

    # Release lock
    release_lock "$fd"
}

# Read-modify-write
# Usage: modify_file /path/to/file modify_function
modify_file() {
    local target_file="$1"
    local modify_fn="$2"
    local lock_file="${target_file}.lock"
    local temp_file="${target_file}.tmp.$$"

    # Acquire lock
    local fd
    fd=$(acquire_lock "$lock_file") || return 1

    # Read current content
    local content
    content=$(cat "$target_file")

    # Modify content
    local new_content
    new_content=$(echo "$content" | $modify_fn)

    # Write to temp file
    echo "$new_content" > "$temp_file"

    # Atomic move
    mv "$temp_file" "$target_file"

    # Release lock
    release_lock "$fd"

    return 0
}

# Increment counter atomically
# Usage: increment_counter /path/to/counter.txt
increment_counter() {
    local counter_file="$1"
    local lock_file="${counter_file}.lock"
    local temp_file="${counter_file}.tmp.$$"

    # Acquire lock
    local fd
    fd=$(acquire_lock "$lock_file") || return 1

    # Read, increment, write
    local current
    if [ -f "$counter_file" ]; then
        current=$(cat "$counter_file")
    else
        current=0
    fi

    local new=$((current + 1))
    echo "$new" > "$temp_file"
    mv "$temp_file" "$counter_file"

    # Release lock
    release_lock "$fd"

    echo "$new"
}
```

### Implementation Plan

#### Phase 1: Create Locking Library (1 hour)

1. Create `locking.sh` with utility functions
2. Test each function
3. Document usage

#### Phase 2: Update Critical Scripts (2 hours)

**Script 1: ralf-loop.sh**

```bash
#!/bin/bash
# Updated with locking

source ~/.blackbox5/2-engine/.autonomous/lib/locking.sh

# Update state with locking
update_state() {
    local new_state="$1"
    atomic_write "$RUN_DIR/state.yaml" "$new_state"
}

# Read state with locking
read_state() {
    safe_read "$RUN_DIR/state.yaml"
}
```

**Script 2: bb5-task.sh**

```bash
#!/bin/bash
# Updated with locking

source ~/.blackbox5/2-engine/.autonomous/lib/locking.sh

# Update task status
update_task_status() {
    local task_id="$1"
    local new_status="$2"
    local task_file="$PROJECT_DIR/tasks/active/$task_id/task.md"

    modify_file "$task_file" "sed 's/Status: .*/Status: $new_status/'"
}
```

**Script 3: Hook scripts**

Update all hook scripts to use locking for:
- Event file updates
- Queue updates
- State updates

#### Phase 3: Add Lock Cleanup (30 min)

Create cleanup script for stale locks:

```bash
#!/bin/bash
# cleanup-locks.sh - Remove stale lock files

find ~/.blackbox5 -name "*.lock" -type f -mtime +1 -delete
echo "Cleaned up stale lock files"
```

#### Phase 4: Documentation (30 min)

1. Document locking usage in shell scripts
2. Add examples
3. Explain when to use each function

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/locking.sh` - Locking utilities
2. `2-engine/.autonomous/bin/cleanup-locks.sh` - Lock cleanup

### Modified Files
1. `2-engine/.autonomous/shell/ralf-loop.sh`
2. `bin/bb5-task.sh`
3. `bin/bb5-goal.sh`
4. All hook scripts in `.autonomous/hooks/`

---

## 5. Success Criteria

- [ ] Locking library created
- [ ] All critical scripts use locking
- [ ] No race conditions in shell scripts
- [ ] Lock cleanup working
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Remove locking calls
2. **Fix**: Debug locking library
3. **Re-enable**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Locking Library | 1 hour | 1 hour |
| Phase 2: Critical Scripts | 2 hours | 3 hours |
| Phase 3: Lock Cleanup | 30 min | 3.5 hours |
| Phase 4: Documentation | 30 min | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Shell scripts lack locking*
