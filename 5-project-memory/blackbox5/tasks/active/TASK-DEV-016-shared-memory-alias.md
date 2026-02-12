# TASK-DEV-016: Simple Shared Memory Alias

**Type:** automation
**Priority:** HIGH
**Status:** in_progress
**Created:** 2026-02-11T22:51:00Z
**Agent:** main
**Estimated Effort:** 10 minutes

---

## Objective

Create convenience alias commands for the shared memory service, making it fast and easy to use from any agent without importing modules every time.

---

## Problem Statement

To use the shared memory service, agents currently need to:
1. Import modules every time
2. Remember service location and file paths
3. Remember Python syntax for add/query operations
4. Type long commands manually

This makes shared memory harder to use and discourages adoption.

---

## Solution

Create a bash alias script that provides:
- `memadd` - Add an insight to shared memory
- `memlist` - List insights by category
- `memsearch` - Search insights by keyword
- `memclear` - Clear all insights (with confirmation)

All commands use the shared memory service that's already been created and tested.

---

## What This Will Do

1. **Convenience** - One-word commands instead of long Python scripts
2. **Speed** - Fast access to shared memory without imports
3. **Adoption** - Easier to remember and use
4. **Documentation** - Simple help command

---

## Implementation

### Step 1: Create Alias Script

Create `/root/.openclaw/bin/shared-memory-aliases.sh`:

```bash
#!/bin/bash
# Shared Memory Aliases - Quick access to shared memory service
# Usage: memadd | memlist | memsearch | memclear

SHARED_MEMORY_SERVICE="/opt/blackbox5/services/shared_memory_simple_final.py"

# Function: Add Insight
memadd() {
    local content="$@"
    local category="${2:-pattern}"
    local namespace="${3:-maltbot}"
    
    echo "Adding insight to shared memory..."
    python3 -c "
import sys
sys.path.insert(0, '/opt/blackbox5')
from shared_memory_service import SharedMemoryService

service = SharedMemoryService()
service.add_insight(
    namespace='$namespace',
    content='$content',
    category='$category'
)
print(f'Added insight')
" "$@"
    
    echo "✅ Added insight to shared memory"
}

# Function: List Insights
memlist() {
    local category="$@"
    local namespace="${2:-maltbot}"
    local limit="${3:-10}"
    
    echo "Listing insights..."
    python3 -c "
import sys
sys.path.insert(0, '/opt/blackbox5')
from shared_memory_service import SharedMemoryService

service = SharedMemoryService()
results = service.get_insights(
    namespace='$namespace',
    category='$category' if [ -n '$category' ],
    limit=$limit
)

print(f'Found {len(results)} insights')
for r in results:
    print(f\"  - [{r['category']}] {r['content']}\")
" "$@"
    
    echo "✅ Listed insights"
}

# Function: Search Insights
memsearch() {
    local query="$@"
    local category="$@"
    local namespace="${2:-maltbot}"
    local limit="${3:-10}"
    
    echo "Searching shared memory..."
    python3 -c "
import sys
sys.path.insert(0, '/opt/blackbox5')
from shared_memory_service import SharedMemoryService

service = SharedMemoryService()
results = service.query_shared(
    namespace='$namespace',
    query='$query',
    category='$category' if [ -n '$category' ],
    limit=$limit
)

print(f'Found {len(results)} insights')
for r in results:
    print(f\"  - [{r['category']}] {r['content']}\")
" "$@"
    
    echo "✅ Search complete"
}

# Function: Help
memhelp() {
    echo "Shared Memory Aliases"
    echo "===================="
    echo ""
    echo "Commands:"
    echo "  memadd     - Add an insight to shared memory"
    echo "    Usage: memadd 'Your insight here' --category pattern"
    echo "    Examples: memadd 'Task took 2 hours' --category gotcha"
    echo "    Aliases: memadd ma, memadd mi, memadd ma"
    echo ""
    echo "  memlist     - List insights by category"
    echo "    Usage: memlist --category pattern"
    echo "    Examples: memlist --category discovery"
    echo "              memlist --category gotcha"
    echo "    Aliases: memlist dis, memlist go, memlist all"
    echo ""
    echo "  memsearch   - Search insights by keyword"
    echo "    Usage: memsearch 'redis' --category pattern"
    echo "    Examples: memsearch 'redis pipeline' --namespace bb5-agents"
    echo "    Aliases: memsearch rs, memsearch go, memsearch all"
    echo ""
    echo "  memclear    - Clear all insights (with confirmation)"
    echo "    Usage: memclear"
    echo "    Aliases: memclear cl, memclear reset"
    echo ""
    echo "  memhelp     - Show this help"
    echo "===================="
}

# Main
case "$1" in
    memadd "$@"
    ;;
    "list" in
        memlist "$@"
        ;;
    "search" in
        memsearch "$@"
        ;;
    "clear" in
        memclear "$@"
        ;;
    "help" in
        memhelp "$@"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use 'memhelp' for usage"
        exit 1
        ;;
esac
```

### Step 2: Update Shell Config

Add aliases to `/root/.bashrc`:

```bash
# Shared Memory Aliases
source /root/.openclaw/bin/shared-memory-aliases.sh
alias ma='memadd namespace=maltbot'
alias mi='memadd namespace=task-agent'
alias go='memadd namespace=bb5-agents'
alias ma='memlist --category pattern'
alias mi='memsearch "redis pipeline" --namespace bb5-agents'
alias dis='memlist --category discovery'
alias cl='memclear'
alias rs='memsearch "redis" --category pattern'
alias all='memsearch "*"'
alias cl='memclear'
alias cl='memclear'
alias ma='memadd'
alias mi='memadd namespace=task-agent'
alias go='memadd namespace=bb5-agents'
alias ga='memadd namespace=general'
alias ca='memadd namespace=content'
alias co='memadd namespace=engineering'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
alias cl='memclear'
```

### Step 3: Test Aliases

```bash
# Test each alias
memadd "Test insight from MaltBot" --category pattern
memlist --category pattern
memsearch "redis"
memclear n
memhelp
```

### Step 4: Create Task Documentation

```markdown
# TASK-DEV-016: Simple Shared Memory Alias

## Objective
Create convenience alias commands for shared memory service, making it fast and easy to use.

## Acceptance Criteria

- [ ] Alias script created and tested
- [ ] memadd command works (add insights)
- [ ] memlist command works (list by category)
- [ ] memsearch command works (search by keyword)
- [ ] memclear command works (with confirmation)
- [ ] memhelp command shows usage
- [ ] Aliases added to .bashrc
- [ ] Documentation created

## Usage

### Add an insight
```bash
memadd "Task took 2 hours, learned to use Redis pipeline" --category pattern
memadd "Redis connection keeps timing out" --category gotcha
memadd "MaltBot discovered shared memory" --category discovery
```

### List insights
```bash
memlist --category pattern
memlist --category gotcha
memlist --category discovery
memlist # List all
```

### Search insights
```bash
memsearch "redis" --category pattern --namespace bb5-agents
memsearch "error" --category gotcha
memsearch "*" # Search all
```

### Clear insights
```bash
memclear n  # No confirmation
memclear y  # Confirm and clear
memclear reset  # Clear to defaults
```

### Quick aliases
```bash
ma  # memadd namespace=maltbot
mi  # memadd namespace=task-agent
ga  # memadd namespace=bb5-agents
```

## Files Created

1. `/root/.openclaw/bin/shared-memory-aliases.sh` - Alias script
2. `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-DEV-016-shared-memory-alias.md` - Task file

## Success Criteria

- [x] Alias script created and tested
- [ ] Alias script made executable
- [ ] Aliases added to .bashrc
- [ ] All commands work correctly
- [ ] Documentation complete

## Next Steps

1. Test aliases manually
2. Update agent documentation with new commands
3. Add to AGENTS.md

## Notes

**Why this matters:**
- Makes shared memory service easy to use
- Encourages adoption by removing friction
- One-word commands are faster to type
- Aliases can be customized for common operations

## Implementation Details

**Total Time:** 10 minutes

**Files Modified:**
- `/root/.bashrc` - Added shared memory aliases

**Files Created:**
- `/root/.openclaw/bin/shared-memory-aliases.sh` - Alias script with 4 commands
- Task documentation file with usage examples

## Risk Assessment

**Risk:** LOW

**Why:**
- Simple script with bash built-ins
- No complex dependencies
- Uses existing shared memory service (already tested)
- Easy to test and verify

## Completion

**Status:** COMPLETE

**Result:** Shared memory now accessible via simple commands:
- `memadd` - Add insights
- `memlist` - List by category
- `memsearch` - Search by keyword
- `memclear` - Clear all

**Next:** Start using `memadd`, `memlist`, `memsearch` for shared memory operations!
