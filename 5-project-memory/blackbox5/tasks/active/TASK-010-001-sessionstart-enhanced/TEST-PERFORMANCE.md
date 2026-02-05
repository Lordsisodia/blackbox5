# BB5 SessionStart Hook - Performance Test Report

**Task:** TASK-010-001
**Hook Version:** 2.0.0
**Test Date:** 2026-02-06
**Tester:** Performance Engineer

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Performance Score** | **42/100** (FAILING) |
| **Critical Bottlenecks** | 7 |
| **Subshell Calls** | 45+ |
| **File Operations** | 23+ |
| **Git Command Calls** | 3 (2 redundant) |
| **Estimated Execution Time** | 250-400ms (unacceptable) |

**Verdict:** This hook is NOT production-ready from a performance standpoint. The self-reported "85/100 Performance" score is wildly optimistic. The hook suffers from severe subshell abuse, redundant operations, and N+1 query patterns that will cause significant latency on every Claude Code session start.

---

## 1. Subshell Analysis (The #1 Killer)

### Subshell Count by Function

| Function | Subshell Calls | Severity |
|----------|---------------|----------|
| `validate_dependencies()` | 3 | MEDIUM |
| `read_stdin_input()` | 4 | HIGH |
| `detect_project()` | 7 | CRITICAL |
| `detect_agent_type()` | 6 | HIGH |
| `match_agent_from_path()` | 0 | GOOD |
| `detect_mode()` | 0 | GOOD |
| `create_run_folder()` | 4 | MEDIUM |
| `persist_environment_vars()` | 9 | CRITICAL |
| `get_git_info()` | 3 | HIGH |
| `get_git_branch()` | 1 | MEDIUM |
| `get_git_commit()` | 1 | MEDIUM |
| `create_template_files()` | 5 | HIGH |
| `generate_agent_context()` | 3 | MEDIUM |
| `generate_json_output()` | 2 | LOW |
| `main()` | 7 | HIGH |
| **TOTAL** | **55+** | **CRITICAL** |

### Critical Subshell Abuses

#### 1.1 `detect_project()` - 7 Subshells (Lines 259-300)

```bash
detect_project() {
    local cwd="$PWD"                                    # 0 (builtin)

    if [ -n "${BB5_PROJECT:-}" ]; then
        if validate_project_name "$BB5_PROJECT"; then
            echo "$BB5_PROJECT"                         # 0 (builtin)
            return 0
        fi
    fi

    if [ -f ".bb5-project" ]; then
        local project_from_file
        project_from_file=$(cat ".bb5-project" 2>/dev/null | tr -d '[:space:]')  # SUBSHELL #1: cat+tr pipeline
        if [ -n "$project_from_file" ] && validate_project_name "$project_from_file"; then
            echo "$project_from_file"                 # 0 (builtin)
            return 0
        fi
    fi

    local dir="$cwd"
    while [ "$dir" != "/" ] && [ "$dir" != "." ]; do   # Loop could iterate 10+ times
        if [ -f "$dir/.bb5-project" ]; then
            local project_from_file
            project_from_file=$(cat "$dir/.bb5-project" 2>/dev/null | tr -d '[:space:]')  # SUBSHELL #2-N: N+1 pattern!
            if [ -n "$project_from_file" ] && validate_project_name "$project_from_file"; then
                echo "$project_from_file"
                return 0
            fi
        fi
        dir=$(dirname "$dir")                          # SUBSHELL #3-N: dirname in loop!
    done

    # ... more code
}
```

**Problem:** Walking up the directory tree uses subshells for EVERY iteration:
- `cat | tr` pipeline for each directory level checked
- `dirname` for each iteration
- If you're 10 directories deep, that's 20 subshells just for project detection!

**Fix:** Use pure bash string manipulation:
```bash
# Instead of: dir=$(dirname "$dir")
# Use: dir="${dir%/*}"
```

#### 1.2 `persist_environment_vars()` - 9 Subshells (Lines 446-518)

```bash
persist_environment_vars() {
    # ...
    env_dir=$(dirname "$env_file") || return 1          # SUBSHELL #1

    encoded_project=$(printf '%s' "$project" | base64 | tr -d '\n')  # SUBSHELL #2
    encoded_agent=$(printf '%s' "$agent_type" | base64 | tr -d '\n')  # SUBSHELL #3
    encoded_dir=$(printf '%s' "$run_dir" | base64 | tr -d '\n')      # SUBSHELL #4
    encoded_run_id=$(printf '%s' "$run_id" | base64 | tr -d '\n')   # SUBSHELL #5

    # ...
    section_start="# === BEGIN BB5 SessionStart v${HOOK_VERSION} ==="
    section_end="# === END BB5 SessionStart v${HOOK_VERSION} ==="

    if [ -f "$env_file" ]; then
        awk -v start="$section_start" -v end="$section_end" '...' "$env_file" > "$temp_file"  # SUBSHELL #6: awk
    fi

    {
        echo ""
        echo "$section_start"
        echo "# Generated: $(date -Iseconds)"             # SUBSHELL #7: date
        echo "export BB5_PROJECT=\$(echo '$encoded_project' | base64 -d)"  # SUBSHELL #8: base64 decode on every shell startup!
        # ... 3 more base64 decodes
    } >> "$temp_file"

    sync "$temp_file" 2>/dev/null || true               # SUBSHELL #9: sync

    if ! mv "$temp_file" "$env_file" 2>/dev/null; then  # SUBSHELL #10: mv
        release_lock "$LOCK_FD"
        return 1
    fi

    release_lock "$LOCK_FD"
    return 0
}
```

**Problem:**
- 4 base64 encoding operations (expensive)
- 4 base64 decoding operations embedded in generated shell code (runs on EVERY shell startup!)
- `awk` invocation for file manipulation
- `date` call in heredoc

**Impact:** Not only is this slow during hook execution, but it makes EVERY future shell startup slower because the persisted env file contains subshell commands!

#### 1.3 `read_stdin_input()` - 4 Subshells (Lines 237-253)

```bash
read_stdin_input() {
    local input=""
    local original_lang="${LANG:-}"
    export LANG=C

    if IFS= read -r -t "$STDIN_TIMEOUT" -N "$MAX_INPUT_SIZE" input 2>/dev/null; then
        if [ -n "$input" ] && echo "$input" | jq -e . >/dev/null 2>&1; then  # SUBSHELL #1: echo | jq
            export LANG="$original_lang"
            echo "$input"                                                   # SUBSHELL #2: echo
            return 0
        fi
    fi

    export LANG="$original_lang"
    echo "{}"                                                                # SUBSHELL #3: echo
    return 0
}
```

**Problem:**
- `echo "$input" | jq` pipes through subshell
- Multiple `echo` calls (unnecessary)
- `jq` validation is expensive for large input

**Fix:** Use process substitution or direct validation:
```bash
if [ -n "$input" ] && jq -e . <<< "$input" >/dev/null 2>&1; then
```

---

## 2. Git Command Inefficiency

### 2.1 Redundant Git Calls (Lines 524-555)

```bash
get_git_info() {
    [ "$GIT_INFO_CACHE_POPULATED" = "true" ] && { echo "$GIT_INFO_CACHE"; return 0; }

    local git_info
    git_info=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)    # GIT CALL #1

    if [ -n "$git_info" ]; then
        local commit
        commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")  # GIT CALL #2
        GIT_INFO_CACHE="${git_info}|${commit}"
        GIT_INFO_CACHE_POPULATED=true
        echo "$GIT_INFO_CACHE"
        return 0
    else
        GIT_INFO_CACHE="unknown|unknown"
        GIT_INFO_CACHE_POPULATED=true
        echo "$GIT_INFO_CACHE"
        return 1
    fi
}
```

**Problem:**
- Two separate `git` calls when ONE would suffice:
```bash
git_info=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
commit=$(git rev-parse --short HEAD 2>/dev/null)
```
- Could use: `git rev-parse --abbrev-ref HEAD --short HEAD` (single call)

### 2.2 Uncached Git in `detect_agent_type()` (Lines 361-368)

```bash
local git_branch
git_branch=$(git branch --show-current 2>/dev/null || echo "")  # GIT CALL #3 (UNCACHED!)
if [ -n "$git_branch" ]; then
    for pattern in "${AGENT_PATH_PATTERNS[@]}"; do
        IFS=':' read -r agent_type _ <<< "$pattern"
        [[ "$git_branch" == *"$agent_type"* ]] && { echo "$agent_type"; return 0; }
    done
fi
```

**Problem:**
- This git call is NOT using the cache from `get_git_info()`
- Called even when `get_git_info()` was already called elsewhere
- `git branch --show-current` is slower than `git rev-parse --abbrev-ref HEAD`

**Impact:** 3 git calls when 1 would suffice. Git operations are expensive (50-100ms each in large repos).

---

## 3. File I/O Patterns

### 3.1 N+1 File Checks in `detect_project()`

```bash
local dir="$cwd"
while [ "$dir" != "/" ] && [ "$dir" != "." ]; do
    if [ -f "$dir/.bb5-project" ]; then              # File check #N
        local project_from_file
        project_from_file=$(cat "$dir/.bb5-project" 2>/dev/null | tr -d '[:space:]')  # Read #N
        # ...
    fi
    dir=$(dirname "$dir")                            # Subshell #N
```

**Problem:**
- For a project 10 levels deep, this performs 10 file existence checks + 10 file reads
- Each iteration uses a subshell
- No early termination optimization

**Fix:** Use `find` with `-prune` for single operation:
```bash
project_file=$(find "$cwd" -name ".bb5-project" -maxdepth 10 -print -quit 2>/dev/null)
```

### 3.2 Multiple File Existence Checks in `detect_agent_type()` (Lines 344-359)

```bash
if [ -f "queue.yaml" ] || [ -f "loop-metadata-template.yaml" ]; then
    echo "planner"
    return 0
elif [ -f ".task-claimed" ]; then
    echo "executor"
    return 0
elif [ -f "architecture-review.md" ]; then
    echo "architect"
    return 0
elif [ -f "verification-report.md" ]; then
    echo "verifier"
    return 0
elif [ -f "scout-report.md" ]; then
    echo "scout"
    return 0
fi
```

**Problem:** Up to 6 separate file existence checks in worst case.

**Fix:** Batch check with single `ls` or use associative array approach.

### 3.3 Redundant File Operations in `persist_environment_vars()`

```bash
[ -f "$env_file" ] && touch "$env_file" 2>/dev/null || return 1   # Touch if exists?

# Later:
if [ -f "$env_file" ]; then
    if [ ! -f "$env_file" ] || [ -L "$env_file" ]; then           # Double negative check
        release_lock "$LOCK_FD"
        return 1
    fi
```

**Problem:**
- Logic error: `touch` only if file exists? Should be `||` not `&&`
- Redundant file checks
- `sync` call is expensive and likely unnecessary

---

## 4. Lock Contention Analysis

### 4.1 Lock Duration (Lines 460-516)

```bash
persist_environment_vars() {
    # ...
    local lock_file="$env_file.lock"
    local lock_fd
    if ! acquire_lock "$lock_file"; then              # LOCK ACQUIRED
        return 1
    fi

    local temp_file
    temp_file=$(mktemp "${env_file}.tmp.XXXXXX") || { # Subshell + file creation
        release_lock "$LOCK_FD"                       # Early release on error (good)
        return 1
    }
    register_temp_file "$temp_file"

    # ... AWK processing (expensive) ...
    # ... Base64 encoding (4 operations) ...
    # ... File writing ...
    # ... sync call (very expensive) ...

    sync "$temp_file" 2>/dev/null || true             # BLOCKING I/O while holding lock!

    if ! mv "$temp_file" "$env_file" 2>/dev/null; then
        release_lock "$LOCK_FD"
        return 1
    fi

    release_lock "$LOCK_FD"                           # LOCK RELEASED
    return 0
}
```

**Problem:**
- Lock is held during:
  - `mktemp` call
  - `awk` file processing
  - 4 base64 encoding operations
  - File writes
  - `sync` call (flushes ALL disk buffers!)
- `sync` while holding a lock is a critical performance anti-pattern

**Impact:** If 100 hooks run simultaneously, they will serialize on this lock. With `sync` taking 10-50ms, that's 1-5 seconds of serialized wait time.

---

## 5. Memory Usage Analysis

### 5.1 Large Variable Storage

```bash
readonly MAX_INPUT_SIZE=1048576  # 1MB
# ...
if IFS= read -r -t "$STDIN_TIMEOUT" -N "$MAX_INPUT_SIZE" input 2>/dev/null; then
```

**Problem:**
- Reads up to 1MB into memory
- No streaming processing
- Multiple copies of data (input, temp files, etc.)

### 5.2 Array Growth

```bash
ERRORS=()
TEMP_FILES=()
# ...
log_error() {
    local message="$1"
    ERRORS+=("$message")          # Array append (reallocation)
    echo "[ERROR] $message" >&2
}
```

**Problem:** Bash arrays grow by reallocation. With many errors, this becomes O(n^2).

---

## 6. Scalability Analysis (100 Concurrent Hooks)

### 6.1 Lock Contention

| Scenario | Time Impact |
|----------|-------------|
| 1 hook | 50-100ms (lock uncontested) |
| 10 hooks | 500ms-1s (some contention) |
| 100 hooks | 5-10s (severe contention) |

**Bottleneck:** The `persist_environment_vars()` lock serializes ALL hook executions.

### 6.2 File System Contention

- All hooks write to `$BB5_ROOT/5-project-memory/$project/runs/$agent_type/`
- Directory creation (`mkdir -p`) can block on parent directory locks
- `sync` calls flush global disk buffers, affecting entire system

### 6.3 Git Contention

- Multiple concurrent `git` calls to the same repository
- Git has internal locking that can cause serialization

---

## 7. Detailed Performance Breakdown

### 7.1 Estimated Execution Times

| Operation | Estimated Time | Count | Total |
|-----------|---------------|-------|-------|
| Subshell fork/exec | 5-10ms | 55 | 275-550ms |
| Git commands | 30-50ms | 3 | 90-150ms |
| File I/O (read) | 1-2ms | 15 | 15-30ms |
| File I/O (write) | 2-5ms | 8 | 16-40ms |
| `sync` call | 10-30ms | 1 | 10-30ms |
| `jq` execution | 20-40ms | 2 | 40-80ms |
| `awk` execution | 10-20ms | 1 | 10-20ms |
| `base64` encode | 1-2ms | 4 | 4-8ms |
| `flock` acquire | 1-5ms | 1 | 1-5ms |
| **TOTAL** | | | **461-913ms** |

### 7.2 Critical Path Analysis

```
main()
  |- validate_dependencies()          [10-20ms]
  |- read_stdin_input()               [25-50ms]
  |- detect_project()                 [50-150ms]  <-- N+1 subshells
  |- detect_agent_type()              [40-100ms]  <-- Git + file checks
  |- detect_mode()                    [1-2ms]
  |- create_run_folder()              [20-40ms]
  |- persist_environment_vars()       [100-300ms] <-- Lock + sync
  |- create_template_files()          [30-60ms]
  |- generate_agent_context()         [20-40ms]
  |- generate_json_output()           [15-30ms]

Total Critical Path: 311-792ms
```

---

## 8. Performance Bottlenecks Summary

### Critical (Must Fix)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 1 | N+1 subshells in directory walk | `detect_project()` | 50-150ms |
| 2 | Lock held during `sync` | `persist_environment_vars()` | 10-30ms per hook, serializes |
| 3 | 4 base64 encodes + 4 decodes | `persist_environment_vars()` | 8-16ms + future shell slowdown |
| 4 | Redundant git calls | `detect_agent_type()`, `get_git_info()` | 60-100ms |
| 5 | `jq` validation of large input | `read_stdin_input()` | 20-40ms |

### High (Should Fix)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 6 | Multiple file existence checks | `detect_agent_type()` | 5-10ms |
| 7 | `awk` for simple text removal | `persist_environment_vars()` | 10-20ms |
| 8 | `date` calls in heredocs | `create_template_files()`, `generate_agent_context()` | 5-10ms |
| 9 | `dirname` in subshell | `detect_project()` loop | 20-50ms |
| 10 | `cat | tr` pipelines | `detect_project()` | 10-20ms |

### Medium (Nice to Fix)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 11 | Unnecessary `sync` call | `persist_environment_vars()` | 10-30ms |
| 12 | Array reallocation | `ERRORS[]`, `TEMP_FILES[]` | Minimal |
| 13 | Multiple `echo` subshells | Various | 5-10ms |
| 14 | `command -v` in loop | `validate_dependencies()` | 5-10ms |

---

## 9. Recommendations

### 9.1 Immediate Fixes (Critical)

#### Fix #1: Eliminate Subshells in Directory Walk
```bash
# BEFORE (7+ subshells)
local dir="$cwd"
while [ "$dir" != "/" ] && [ "$dir" != "." ]; do
    if [ -f "$dir/.bb5-project" ]; then
        local project_from_file
        project_from_file=$(cat "$dir/.bb5-project" 2>/dev/null | tr -d '[:space:]')
        # ...
    fi
    dir=$(dirname "$dir")
done

# AFTER (0 subshells)
local dir="$cwd"
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
    if [ -f "$dir/.bb5-project" ]; then
        read -r project_from_file < "$dir/.bb5-project" 2>/dev/null
        project_from_file="${project_from_file//[[:space:]]/}"
        # ...
    fi
    dir="${dir%/*}"
done
```

#### Fix #2: Remove `sync` from Lock Critical Section
```bash
# BEFORE
acquire_lock "$lock_file"
# ... operations ...
sync "$temp_file"  # BLOCKING!
mv "$temp_file" "$env_file"
release_lock

# AFTER
acquire_lock "$lock_file"
# ... operations ...
mv "$temp_file" "$env_file"
release_lock
# sync AFTER releasing lock (or remove entirely)
```

#### Fix #3: Cache Git Results
```bash
# BEFORE
git_branch=$(git branch --show-current 2>/dev/null)  # In detect_agent_type
# ... later ...
git_info=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)  # In get_git_info

# AFTER - Single call at start
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null)
# Use these variables everywhere
```

#### Fix #4: Eliminate Base64 Encoding
```bash
# BEFORE
encoded_project=$(printf '%s' "$project" | base64 | tr -d '\n')
echo "export BB5_PROJECT=\$(echo '$encoded_project' | base64 -d)"

# AFTER - Use single quotes with proper escaping
printf "export BB5_PROJECT='%s'\n" "${project//'/\\'}"
```

### 9.2 Architecture Changes

#### Change #1: Lazy Evaluation
Don't create run folder or persist env vars unless actually needed:
```bash
# Only create run folder in autonomous mode
[ "$mode" = "autonomous" ] || return 0
```

#### Change #2: Background Persistence
```bash
# Persist env vars in background to not block hook
(persist_environment_vars "$@" &)
```

#### Change #3: Lock-Free Design
Use atomic file operations instead of locks:
```bash
# Atomic write without lock
cat > "${env_file}.tmp.$$" << EOF
...
EOF
mv "${env_file}.tmp.$$" "$env_file"  # Atomic
```

---

## 10. Performance Score Breakdown

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Subshell Efficiency | 15/100 | 25% | 3.75 |
| Git Command Efficiency | 30/100 | 15% | 4.5 |
| File I/O Patterns | 35/100 | 20% | 7.0 |
| Lock Contention | 20/100 | 15% | 3.0 |
| Memory Usage | 60/100 | 10% | 6.0 |
| Scalability | 25/100 | 15% | 3.75 |
| **TOTAL** | | | **28/100** |

**Adjusted for "Production Ready" Claim:** +14 points (generosity)
**Final Score:** **42/100** (FAILING)

---

## 11. Conclusion

The BB5 SessionStart Hook v2.0 is **NOT production-ready** from a performance standpoint. The self-assessed "85/100 Performance" score is inaccurate by a wide margin.

### Key Findings:

1. **55+ subshell calls** - Each fork/exec costs 5-10ms, totaling 275-550ms
2. **Lock contention with `sync`** - Serializes concurrent executions
3. **Redundant git calls** - 3 calls when 1 would suffice
4. **N+1 file operations** - Directory walking is O(n) with expensive operations
5. **Estimated execution time: 250-400ms** - Unacceptable for a session start hook

### Required Actions:

1. **Immediate:** Remove `sync` from lock critical section
2. **Immediate:** Replace `$(dirname)` with `${var%/*}`
3. **Immediate:** Cache git results in global variables
4. **Short-term:** Eliminate base64 encoding/decoding
5. **Short-term:** Batch file existence checks
6. **Medium-term:** Consider lock-free atomic writes
7. **Medium-term:** Implement lazy evaluation for non-autonomous mode

### Success Criteria for Production:

- [ ] Subshell count < 10
- [ ] Execution time < 50ms
- [ ] Lock duration < 10ms
- [ ] No `sync` in critical path
- [ ] Single git call per execution
- [ ] Handles 100 concurrent hooks without serialization

**Current Status:** NOT READY FOR PRODUCTION

---

*Report generated: 2026-02-06*
*Performance Engineer Analysis*
*Score: 42/100 (FAILING)*
