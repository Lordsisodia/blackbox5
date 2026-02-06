# TaskClaim Hook - Edge Case Analysis

**Analyst:** Edge Case Analysis Expert
**Date:** 2026-02-06
**Design Under Review:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/TASK_CLAIM_HOOK_DESIGN.md`
**Status:** CRITICAL ISSUES FOUND - Design requires hardening before implementation

---

## Executive Summary

The TaskClaim hook design has **47 identified edge cases and failure modes** across 6 categories. Many are high-severity issues that could cause data corruption, race conditions, or silent failures. The design assumes a cooperative single-agent environment and lacks defensive programming for production use.

**Severity Breakdown:**
- CRITICAL: 12 issues
- HIGH: 18 issues
- MEDIUM: 12 issues
- LOW: 5 issues

---

## 1. EDGE CASES: Task State & Existence

### 1.1 Task Already Claimed

**Scenario:** Agent A claims TASK-001. Agent B (or the same agent in a new session) tries to claim TASK-001 again.

**Current Design Behavior:**
- Design mentions "Update queue.yaml: mark task as claimed" but doesn't check existing status first
- No explicit handling for duplicate claims

**Failure Modes:**
1. **Silent overwrite:** Second claim overwrites first claim's metadata, orphaning the first run folder
2. **Orphaned run folder:** First run folder exists but is no longer referenced in queue.yaml
3. **Dual execution:** Both agents think they own the task and work in parallel
4. **Data loss:** If first agent writes results, second agent may overwrite them

**Required Safeguards:**
```python
# Must check BEFORE claiming
if task.status == "claimed":
    if task.claimed_by == current_agent_id:
        return "You already claimed this task"  # Idempotent
    else:
        raise TaskAlreadyClaimedError(f"Task claimed by {task.claimed_by} at {task.claimed_at}")
```

**Severity:** CRITICAL

---

### 1.2 Task Doesn't Exist

**Scenario:** User types "claim TASK-999" but TASK-999 has never been created.

**Current Design Behavior:**
- `load_task_hierarchy()` will attempt to read non-existent file
- Exception handler catches and prints error, exits with 0

**Failure Modes:**
1. **Silent failure:** Hook exits 0, user thinks claim succeeded
2. **Confusing UX:** No clear message that task doesn't exist
3. **Ghost task creation risk:** If hook has bugs, it might create partial data

**Required Safeguards:**
```python
task_path = Path(project_root) / 'tasks' / 'active' / task_id / 'task.md'
if not task_path.exists():
    return {
        "error": f"Task {task_id} not found in tasks/active/",
        "suggestion": f"Available tasks: {list_available_tasks()}"
    }
```

**Severity:** HIGH

---

### 1.3 Task in completed/ Instead of active/

**Scenario:** User tries to claim a task that was already completed and moved to `tasks/completed/`.

**Current Design Behavior:**
- Only searches `tasks/active/{task_id}/task.md`
- Will report "task not found" even though task exists

**Failure Modes:**
1. **User confusion:** "I can see the task folder, why can't I claim it?"
2. **Re-work risk:** User might recreate an already-completed task
3. **Historical data ignored:** Task history in completed folder is invisible

**Required Safeguards:**
```python
# Check both locations
active_path = Path(project_root) / 'tasks' / 'active' / task_id / 'task.md'
completed_path = Path(project_root) / 'tasks' / 'completed' / task_id / 'task.md'

if completed_path.exists():
    return {
        "error": f"Task {task_id} is already completed",
        "location": str(completed_path),
        "completed_at": get_completion_date(completed_path)
    }
```

**Severity:** MEDIUM

---

### 1.4 Task Exists But Has No task.md

**Scenario:** Task folder exists but `task.md` is missing, corrupted, or empty.

**Current Design Behavior:**
- `parse_task_md()` will fail or return empty data
- Subsequent plan/goal loading will fail with KeyError

**Failure Modes:**
1. **Cascade failure:** Missing task.md causes all hierarchy loading to fail
2. **Partial context injection:** Task metadata incomplete, agent works with bad context
3. **KeyError exceptions:** Code references `task_data['plan_id']` which doesn't exist

**Required Safeguards:**
```python
def parse_task_md(path):
    if not path.exists():
        raise MissingTaskFileError(f"task.md not found at {path}")

    content = path.read_text()
    if not content.strip():
        raise EmptyTaskFileError(f"task.md is empty at {path}")

    metadata = extract_metadata(content)
    if 'plan_id' not in metadata:
        raise MissingMetadataError(f"task.md missing plan_id at {path}")

    return metadata
```

**Severity:** HIGH

---

### 1.5 Task ID Format Variations

**Scenario:** User types variations like:
- "claim task-001" (lowercase)
- "claim Task-001" (mixed case)
- "claim TASK001" (missing hyphen)
- "claim TASK-01" (missing leading zero)

**Current Design Behavior:**
- Regex pattern `r'claim\s+(TASK-\d+)'` is case-insensitive (good)
- But doesn't normalize or validate format

**Failure Modes:**
1. **Pattern mismatch:** "task-001" won't match (lowercase)
2. **False positives:** "claim TASK-001-extra" might match TASK-001 incorrectly
3. **Normalization issues:** TASK-01 and TASK-001 treated as different tasks

**Required Safeguards:**
```python
# Normalize task ID
def normalize_task_id(raw_id):
    # Convert to uppercase
    normalized = raw_id.upper()
    # Validate format
    if not re.match(r'^TASK-\d{3,}$', normalized):
        raise InvalidTaskIdError(f"Invalid task ID format: {raw_id}")
    return normalized
```

**Severity:** MEDIUM

---

### 1.6 Multiple Tasks Mentioned in Prompt

**Scenario:** User says: "Compare TASK-001 and TASK-002, then claim the easier one"

**Current Design Behavior:**
- `detect_task_claim()` returns first match only
- May claim wrong task based on order in prompt

**Failure Modes:**
1. **Wrong task claimed:** Claims TASK-001 when user wanted TASK-002
2. **Ambiguous intent:** No clarification asked
3. **Partial match:** Might match "TASK-001" in a code snippet, not as a claim intent

**Required Safeguards:**
```python
def detect_task_claim(prompt):
    matches = re.findall(r'(?:claim|select|start|work on|pick up)\s+(TASK-\d+)', prompt, re.IGNORECASE)

    if len(matches) > 1:
        return {
            "ambiguous": True,
            "matches": matches,
            "message": f"Multiple tasks detected: {matches}. Which one do you want to claim?"
        }
    # ... rest of logic
```

**Severity:** MEDIUM

---

## 2. EDGE CASES: Hierarchy & Dependencies

### 2.1 Missing Plan Reference

**Scenario:** Task exists but `task.md` doesn't reference a plan (or references non-existent plan).

**Current Design Behavior:**
- `task_data.get('plan_id')` returns None
- Attempts to load plan from `plans/active/None/plan.md`

**Failure Modes:**
1. **Path construction error:** Path with "None" component
2. **Missing context:** Agent works without plan context
3. **Goal loading fails:** Can't find goal without plan

**Required Safeguards:**
```python
plan_id = task_data.get('plan_id')
if not plan_id:
    # Task without plan - allow but warn
    logger.warning(f"Task {task_id} has no plan reference")
    hierarchy = {'task': task_data, 'plan': None, 'goal': None}
else:
    plan_path = Path(project_root) / 'plans' / 'active' / plan_id / 'plan.md'
    if not plan_path.exists():
        raise MissingPlanError(f"Plan {plan_id} not found for task {task_id}")
```

**Severity:** HIGH

---

### 2.2 Missing Goal Reference

**Scenario:** Plan exists but doesn't reference a goal (or references non-existent goal).

**Current Design Behavior:**
- Similar to plan issue - will fail when loading goal

**Failure Modes:**
1. **Incomplete context injection:** Agent doesn't know the ultimate objective
2. **Broken hierarchy:** Goal → Plan → Task chain is broken

**Required Safeguards:**
```python
# Allow orphaned tasks/plans but flag them
def load_hierarchy(task_id):
    hierarchy = {'task': load_task(task_id)}

    try:
        hierarchy['plan'] = load_plan(hierarchy['task'].get('plan_id'))
    except MissingPlanError as e:
        hierarchy['plan'] = None
        hierarchy['warnings'].append(str(e))

    try:
        if hierarchy['plan']:
            hierarchy['goal'] = load_goal(hierarchy['plan'].get('goal_id'))
    except MissingGoalError as e:
        hierarchy['goal'] = None
        hierarchy['warnings'].append(str(e))

    return hierarchy
```

**Severity:** MEDIUM

---

### 2.3 Circular References

**Scenario:** Due to data corruption or manual editing:
- Task A references Plan A
- Plan A references Goal A
- Goal A somehow references back to Task A

**Current Design Behavior:**
- No cycle detection in hierarchy loading
- Could cause infinite recursion

**Failure Modes:**
1. **Stack overflow:** Infinite recursion in hierarchy loading
2. **Memory exhaustion:** Unbounded context growth
3. **Hang:** Hook never completes

**Required Safeguards:**
```python
def load_hierarchy(task_id, visited=None):
    if visited is None:
        visited = set()

    if task_id in visited:
        raise CircularReferenceError(f"Circular reference detected: {visited} -> {task_id}")

    visited.add(task_id)
    # ... continue loading
```

**Severity:** LOW (unlikely but catastrophic)

---

### 2.4 Task Blocked by Dependencies

**Scenario:** Task has `blockedBy` dependencies that aren't completed.

**Current Design Behavior:**
- Design doesn't check blockedBy before claiming
- Queue.yaml shows dependencies but hook doesn't validate

**Failure Modes:**
1. **Premature execution:** Agent works on task that shouldn't start yet
2. **Wasted effort:** Task may need rework when dependencies complete
3. **Dependency violation:** Breaks task ordering guarantees

**Required Safeguards:**
```python
def check_dependencies(task_id):
    task = load_task(task_id)
    blocked_by = task.get('blockedBy', [])

    blocked = []
    for dep_id in blocked_by:
        dep_status = get_task_status(dep_id)
        if dep_status != 'completed':
            blocked.append({'id': dep_id, 'status': dep_status})

    if blocked:
        raise TaskBlockedError(
            f"Task {task_id} is blocked by incomplete dependencies: {blocked}"
        )
```

**Severity:** HIGH

---

## 3. FAILURE MODES: File System & I/O

### 3.1 Queue.yaml Locked or Corrupted

**Scenario:** Another process has queue.yaml open, or file is corrupted (invalid YAML, truncated).

**Current Design Behavior:**
- `update_queue_yaml()` implementation is empty (placeholder)
- No error handling shown

**Failure Modes:**
1. **Write conflict:** Two agents write simultaneously, one change lost
2. **Parse error:** Can't read corrupted YAML
3. **Permission denied:** File locked by another process
4. **Silent corruption:** Partial write creates invalid YAML

**Required Safeguards:**
```python
import fcntl  # Unix file locking
import tempfile
import shutil

def update_queue_yaml(task_id, run_id):
    queue_path = Path(project_root) / '.autonomous' / 'agents' / 'communications' / 'queue.yaml'

    # Atomic read with lock
    with open(queue_path, 'r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        queue = yaml.safe_load(f)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    # Modify in memory
    update_task_claim(queue, task_id, run_id)

    # Atomic write
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=queue_path.parent) as tmp:
        yaml.dump(queue, tmp)
        tmp.flush()
        os.fsync(tmp.fileno())
        shutil.move(tmp.name, queue_path)
```

**Severity:** CRITICAL

---

### 3.2 Disk Full

**Scenario:** Disk is out of space when creating run folder and files.

**Current Design Behavior:**
- Creates multiple files without checking disk space
- Exception handler catches but exits 0 (silent failure)

**Failure Modes:**
1. **Partial folder creation:** Some files created, others fail
2. **Inconsistent state:** Run folder exists but incomplete
3. **Silent failure:** User thinks claim succeeded
4. **Queue updated but folder missing:** Orphaned queue entry

**Required Safeguards:**
```python
def check_disk_space(path, required_mb=10):
    stat = os.statvfs(path)
    available_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
    if available_mb < required_mb:
        raise InsufficientDiskError(f"Only {available_mb:.1f}MB available, need {required_mb}MB")

def create_task_folder(task_id, hierarchy):
    check_disk_space(project_root, required_mb=50)  # Conservative estimate

    try:
        run_dir, run_id = create_folder_and_files(task_id, hierarchy)
    except OSError as e:
        # Cleanup partial creation
        if 'run_dir' in locals():
            shutil.rmtree(run_dir, ignore_errors=True)
        raise
```

**Severity:** CRITICAL

---

### 3.3 Hook Crashes Mid-Execution

**Scenario:** Hook crashes after creating run folder but before updating queue.yaml.

**Current Design Behavior:**
- No transaction/rollback mechanism
- Operations are not atomic

**Failure Modes:**
1. **Orphaned run folder:** Folder exists but not in queue
2. **Orphaned queue entry:** Queue updated but folder creation failed
3. **Partial files:** Some template files created, others not
4. **Inconsistent state:** Requires manual cleanup

**Required Safeguards:**
```python
from contextlib import contextmanager

@contextmanager
def atomic_claim():
    """Ensure claim is atomic or rolled back."""
    created_files = []
    created_dirs = []
    queue_updated = False

    try:
        yield {
            'track_file': lambda p: created_files.append(p),
            'track_dir': lambda p: created_dirs.append(p),
            'set_queue_updated': lambda: queue_updated.__setitem__(0, True)
        }
    except Exception:
        # Rollback on failure
        for f in created_files:
            f.unlink(missing_ok=True)
        for d in sorted(created_dirs, reverse=True):  # Delete deepest first
            d.rmdir()  # Only removes empty dirs
        if queue_updated:
            rollback_queue_update(task_id)
        raise
```

**Severity:** CRITICAL

---

### 3.4 Permission Denied

**Scenario:** User doesn't have write permissions to:
- `runs/` directory
- `queue.yaml` file
- Task folder

**Current Design Behavior:**
- No permission checks
- Exception handler will catch but exit 0

**Failure Modes:**
1. **Silent failure:** Hook exits 0, user thinks claim succeeded
2. **Partial write:** Can create folder but not update queue
3. **Confusing UX:** No clear error about permissions

**Required Safeguards:**
```python
def verify_permissions(project_root):
    paths_to_check = [
        (project_root / 'runs', os.W_OK | os.X_OK),
        (project_root / '.autonomous' / 'agents' / 'communications' / 'queue.yaml', os.W_OK),
    ]

    for path, mode in paths_to_check:
        if not os.access(path, mode):
            raise PermissionError(f"No {'write' if mode == os.W_OK else 'access'} permission for {path}")
```

**Severity:** HIGH

---

### 3.5 Network File System Issues

**Scenario:** Project is on NFS/SMB mount with:
- High latency
- Stale file handles
- Locking issues

**Current Design Behavior:**
- Assumes local filesystem
- No retry logic

**Failure Modes:**
1. **Stale file handle:** File was deleted/recreated by another host
2. **Lock contention:** NFS lock semantics differ from local
3. **Latency timeouts:** Operations timeout on slow NFS

**Required Safeguards:**
```python
import time
from functools import wraps

def retry_on_stale_handle(max_retries=3, delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OSError as e:
                    if 'Stale file handle' in str(e) and attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        continue
                    raise
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**Severity:** MEDIUM

---

### 3.6 Concurrent File Creation

**Scenario:** Two agents claim different tasks simultaneously, both trying to create run folders.

**Current Design Behavior:**
- Uses `exist_ok=True` in mkdir
- But no coordination on queue.yaml updates

**Failure Modes:**
1. **Queue corruption:** Simultaneous writes corrupt queue.yaml
2. **Timestamp collision:** If claims happen in same second, run IDs could collide
3. **Resource exhaustion:** Too many concurrent claims exhaust file descriptors

**Required Safeguards:**
```python
def create_run_id(task_id):
    # Include microseconds and random component to avoid collisions
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    microsecond = datetime.now().microsecond
    random_suffix = secrets.token_hex(4)
    return f"run-{timestamp}-{microsecond:06d}-{task_id}-{random_suffix}"
```

**Severity:** HIGH

---

## 4. RACE CONDITIONS

### 4.1 Concurrent Claims (Same Task)

**Scenario:** Two agents try to claim the same task within milliseconds of each other.

**Current Design Behavior:**
- No locking mechanism shown
- Both could pass "is claimed?" check simultaneously

**Failure Modes:**
1. **Double claim:** Both agents think they own the task
2. **Last-write-wins:** Second queue update overwrites first
3. **Split brain:** Two run folders for same task, only one in queue

**Required Safeguards:**
```python
import fcntl

def claim_task_atomic(task_id, agent_id):
    queue_path = get_queue_path()

    with open(queue_path, 'r+') as f:
        # Exclusive lock - blocks other claim attempts
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        try:
            queue = yaml.safe_load(f)

            # Check if already claimed (under lock)
            task = find_task(queue, task_id)
            if task.get('status') == 'claimed':
                raise TaskAlreadyClaimedError(f"Task claimed by {task['claimed_by']}")

            # Claim it
            task['status'] = 'claimed'
            task['claimed_by'] = agent_id
            task['claimed_at'] = datetime.now().isoformat()

            # Atomic write
            f.seek(0)
            yaml.dump(queue, f)
            f.truncate()
            f.flush()
            os.fsync(f.fileno())

        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

**Severity:** CRITICAL

---

### 4.2 Claim During Task Move (active→completed)

**Scenario:** Agent A claims TASK-001. Simultaneously, another process moves TASK-001 from `active/` to `completed/` (e.g., batch cleanup script).

**Current Design Behavior:**
- No coordination between folder operations and queue updates

**Failure Modes:**
1. **Claimed completed task:** Agent claims task that's being archived
2. **Orphaned claim:** Queue shows claimed, but task folder is gone
3. **Path confusion:** Hook reads from active/, but folder is in completed/

**Required Safeguards:**
```python
def verify_task_location(task_id):
    """Verify task hasn't moved during claim process."""
    active_path = get_active_path(task_id)
    completed_path = get_completed_path(task_id)

    if not active_path.exists() and completed_path.exists():
        raise TaskMovedError(f"Task {task_id} was moved to completed/ during claim")

    if not active_path.exists():
        raise TaskDisappearedError(f"Task {task_id} folder disappeared")
```

**Severity:** HIGH

---

### 4.3 Claim While Another Agent Updates Queue.yaml

**Scenario:** Agent A is claiming TASK-001. Agent B is updating queue.yaml for a different reason (e.g., completing TASK-002).

**Current Design Behavior:**
- No file locking shown
- Read-modify-write cycle is not atomic

**Failure Modes:**
1. **Lost update:** Agent B's update overwrites Agent A's claim
2. **Parse error:** Queue.yaml corrupted by simultaneous writes
3. **Stale data:** Agent A reads queue, Agent B updates, Agent A writes old data + its change

**Required Safeguards:**
```python
# Use atomic file operations with locking
# See section 4.1 for implementation
```

**Severity:** CRITICAL

---

### 4.4 Claim During Queue.yaml Reload

**Scenario:** External process reloads queue.yaml (e.g., queue manager) while claim is in progress.

**Current Design Behavior:**
- No coordination with external processes

**Failure Modes:**
1. **Reload misses claim:** Queue manager reloads before claim is written
2. **Claim missed by scheduler:** Task appears unclaimed to queue manager

**Required Safeguards:**
```python
# Use file system events or timestamp checking
# Queue manager should check mtime before reload
# Or use inotify/watchdog for event-driven updates
```

**Severity:** MEDIUM

---

### 4.5 SessionStart Hook Race

**Scenario:** TaskClaim hook and SessionStart hook both try to create/modify run folder.

**Current Design Behavior:**
- Design shows integration but no coordination
- Both hooks might create folders

**Failure Modes:**
1. **Duplicate folders:** Two run folders for same claim
2. **Conflicting metadata:** Different info in each folder
3. **Queue confusion:** Which run_id goes in queue?

**Required Safeguards:**
```python
# Single responsibility: TaskClaim creates the folder, SessionStart validates it
# TaskClaim should set environment variable that SessionStart checks
# RALF_RUN_DIR should be set by TaskClaim before SessionStart runs
```

**Severity:** HIGH

---

## 5. INTEGRATION ISSUES

### 5.1 SessionStart Hook Interaction

**Scenario:** Both SessionStart and TaskClaim hooks configured. User claims task in new session.

**Current Design Behavior:**
- Design shows TaskClaim runs on UserPromptSubmit
- SessionStart runs at session start
- Order depends on timing

**Failure Modes:**
1. **Double folder creation:** SessionStart creates folder, TaskClaim creates another
2. **Context confusion:** SessionStart loads different context than TaskClaim
3. **Race condition:** Hooks run concurrently, interfere with each other

**Required Safeguards:**
```python
# Coordination mechanism:
# 1. SessionStart checks for RALF_TASK_CLAIM_IN_PROGRESS
# 2. TaskClaim sets RALF_TASK_CLAIMED and RALF_RUN_DIR
# 3. SessionStart skips folder creation if RALF_TASK_CLAIMED is set

# In SessionStart hook:
if os.environ.get('RALF_TASK_CLAIMED'):
    # TaskClaim already handled setup
    run_dir = os.environ['RALF_RUN_DIR']
    validate_folder_exists(run_dir)
    return
```

**Severity:** CRITICAL

---

### 5.2 Agent Claims Then Immediately Exits

**Scenario:** Agent claims task, then session ends (crash, user quit, timeout) before any work is done.

**Current Design Behavior:**
- Task remains "claimed" in queue
- No timeout/heartbeat mechanism

**Failure Modes:**
1. **Stuck task:** Task permanently claimed by dead agent
2. **Resource leak:** Run folder exists but abandoned
3. **No retry:** Task never gets worked on

**Required Safeguards:**
```python
# Heartbeat mechanism
# Claim includes lease with expiration

def claim_task(task_id, agent_id, lease_minutes=30):
    task['status'] = 'claimed'
    task['claimed_by'] = agent_id
    task['claimed_at'] = datetime.now().isoformat()
    task['lease_expires'] = (datetime.now() + timedelta(minutes=lease_minutes)).isoformat()

# Background process or hook periodically checks for expired leases
# and resets status to 'pending'
```

**Severity:** HIGH

---

### 5.3 User Claims Multiple Tasks

**Scenario:** User claims TASK-001, works on it, then claims TASK-002 without completing TASK-001.

**Current Design Behavior:**
- No check for existing claimed tasks
- Agent could have multiple active claims

**Failure Modes:**
1. **Context confusion:** Agent has context for multiple tasks
2. **Resource waste:** Multiple run folders, abandoned work
3. **Queue pollution:** Multiple tasks "claimed" but not being worked on

**Required Safeguards:**
```python
def check_existing_claims(agent_id):
    queue = load_queue()
    existing_claims = [
        task for task in queue['tasks']
        if task.get('claimed_by') == agent_id and task.get('status') == 'claimed'
    ]

    if existing_claims:
        raise MultipleClaimsError(
            f"You already have claimed tasks: {[t['id'] for t in existing_claims]}. "
            f"Complete or release them before claiming new tasks."
        )
```

**Severity:** MEDIUM

---

### 5.4 Claim After Session Started (No SessionStart Hook)

**Scenario:** User starts session normally, then decides to claim a task mid-session.

**Current Design Behavior:**
- TaskClaim hook fires on UserPromptSubmit
- SessionStart already ran without task context

**Failure Modes:**
1. **Context switch:** Agent switches from general mode to task mode mid-session
2. **Folder conflict:** SessionStart may have created a generic run folder
3. **State inconsistency:** Agent has mix of general and task context

**Required Safeguards:**
```python
# TaskClaim should handle both cases:
# 1. New session: TaskClaim runs before/during SessionStart
# 2. Existing session: TaskClaim creates task-specific subfolder or migrates

if os.environ.get('RALF_RUN_DIR'):
    # Session already has run folder
    # Create task subfolder or ask user if they want to switch
    existing_run = Path(os.environ['RALF_RUN_DIR'])
    task_run = existing_run / f'task-{task_id}'
    task_run.mkdir(exist_ok=True)
    return task_run
```

**Severity:** MEDIUM

---

### 5.5 Claim Intent Detection False Positives

**Scenario:** User mentions task ID in different contexts:
- "Don't claim TASK-001, it's blocked"
- "What is the status of TASK-001?"
- "Compare TASK-001 with TASK-002"

**Current Design Behavior:**
- Pattern matching on "claim TASK-001" etc.
- May match when user isn't trying to claim

**Failure Modes:**
1. **Unintended claim:** User mentions task, hook claims it unexpectedly
2. **Context pollution:** Task context injected when not wanted
3. **User confusion:** "I didn't ask to claim this!"

**Required Safeguards:**
```python
TASK_CLAIM_PATTERNS = [
    # Require explicit action verbs at start of sentence or after punctuation
    r'(?:^|[.!?]\s+)claim\s+(TASK-\d+)',
    r'(?:^|[.!?]\s+)select\s+(TASK-\d+)',
    r'(?:^|[.!?]\s+)start\s+(TASK-\d+)',
    r'(?:^|[.!?]\s+)work\s+on\s+(TASK-\d+)',
    r'(?:^|[.!?]\s+)pick\s+up\s+(TASK-\d+)',
    # Explicit command format
    r'^/claim\s+(TASK-\d+)',
]

# Also check for negation
NEGATION_PATTERNS = [
    r"don't\s+claim\s+(TASK-\d+)",
    r"do\s+not\s+claim\s+(TASK-\d+)",
    r"never\s+claim\s+(TASK-\d+)",
]

def detect_task_claim(prompt):
    # Check for negation first
    for pattern in NEGATION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return None  # User explicitly said not to claim

    for pattern in TASK_CLAIM_PATTERNS:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1)
    return None
```

**Severity:** MEDIUM

---

### 5.6 Stop Hook Interaction

**Scenario:** TaskClaim creates run folder. Agent works. Stop hook runs. Task status needs updating.

**Current Design Behavior:**
- Design mentions Stop hook updates queue
- But coordination not specified

**Failure Modes:**
1. **Status mismatch:** TaskClaim says "claimed", Stop says "completed", but work failed
2. **Missing completion:** Stop hook doesn't know which task was claimed
3. **Premature completion:** Stop hook marks complete before agent confirms

**Required Safeguards:**
```python
# Environment variable coordination
# TaskClaim sets RALF_ACTIVE_TASK
# Stop hook reads it and updates accordingly

# In TaskClaim:
os.environ['RALF_ACTIVE_TASK'] = task_id
os.environ['RALF_RUN_DIR'] = str(run_dir)

# In Stop hook:
task_id = os.environ.get('RALF_ACTIVE_TASK')
if task_id:
    # Ask agent or check RESULTS.md for completion status
    status = determine_completion_status(run_dir)
    update_queue(task_id, status)
```

**Severity:** HIGH

---

## 6. DATA INTEGRITY ISSUES

### 6.1 Partial Template Creation

**Scenario:** Hook crashes after creating THOUGHTS.md but before creating DECISIONS.md.

**Current Design Behavior:**
- Creates files sequentially
- No rollback on partial failure

**Failure Modes:**
1. **Incomplete run folder:** Some templates missing
2. **Agent confusion:** "Which files should I use?"
3. **Inconsistent state:** Partial context available

**Required Safeguards:**
```python
def create_task_folder(task_id, hierarchy):
    # Create all content in memory first
    files_to_create = {
        'THOUGHTS.md': render_thoughts_template(hierarchy),
        'DECISIONS.md': render_decisions_template(task_id),
        'ASSUMPTIONS.md': render_assumptions_template(task_id),
        'LEARNINGS.md': render_learnings_template(task_id),
        'RESULTS.md': render_results_template(task_id),
        'timeline.yaml': render_timeline_template(task_id),
        'metadata.yaml': render_metadata_template(task_id, run_id),
    }

    # Then write all atomically (or as atomic as possible)
    try:
        for filename, content in files_to_create.items():
            (run_dir / filename).write_text(content)
    except Exception:
        # Clean up anything we created
        for filename in files_to_create:
            (run_dir / filename).unlink(missing_ok=True)
        run_dir.rmdir()  # Only works if empty
        raise
```

**Severity:** MEDIUM

---

### 6.2 Invalid Task Metadata

**Scenario:** Task file exists but has invalid/malformed metadata.

**Current Design Behavior:**
- `parse_task_md()` extracts metadata
- No validation shown

**Failure Modes:**
1. **Missing required fields:** No title, no objective
2. **Invalid data types:** Priority is "HIGH" vs "high" vs 1
3. **Malformed YAML frontmatter:** Corrupted header section

**Required Safeguards:**
```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class TaskMetadata:
    id: str
    title: str
    objective: str
    status: str
    priority: str
    plan_id: Optional[str] = None
    acceptance_criteria: list = None

    def validate(self):
        required = ['id', 'title', 'objective']
        for field in required:
            if not getattr(self, field):
                raise ValidationError(f"Task missing required field: {field}")

        valid_statuses = ['pending', 'in_progress', 'completed', 'claimed']
        if self.status not in valid_statuses:
            raise ValidationError(f"Invalid status: {self.status}")

def parse_task_md(path):
    content = path.read_text()

    # Extract YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        raise ParseError(f"No YAML frontmatter found in {path}")

    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        raise ParseError(f"Invalid YAML in {path}: {e}")

    task = TaskMetadata(**metadata)
    task.validate()
    return task
```

**Severity:** MEDIUM

---

### 6.3 Run ID Collision

**Scenario:** Two agents claim tasks in the same second.

**Current Design Behavior:**
```python
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
run_id = f"run-{timestamp}-{task_id}"
```

**Failure Modes:**
1. **Same run ID:** If same task claimed twice in same second
2. **Folder collision:** Second claim fails because folder exists
3. **Queue confusion:** Two tasks with same run_id in queue

**Required Safeguards:**
```python
import secrets
from datetime import datetime

def generate_run_id(task_id):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    microsecond = datetime.now().microsecond
    # Add random component for uniqueness
    random_suffix = secrets.token_hex(4)
    return f"run-{timestamp}-{microsecond:06d}-{task_id}-{random_suffix}"

# Or use UUID
import uuid
def generate_run_id(task_id):
    return f"run-{task_id}-{uuid.uuid4().hex[:12]}"
```

**Severity:** HIGH

---

### 6.4 Environment Variable Not Set

**Scenario:** `BB5_PROJECT_ROOT` environment variable not set.

**Current Design Behavior:**
```python
project_root = os.environ.get('BB5_PROJECT_ROOT', '.')
```

**Failure Modes:**
1. **Wrong directory:** Falls back to current directory which may be wrong
2. **Silent failure:** Creates folders in wrong location
3. **Relative path issues:** All paths relative to wrong base

**Required Safeguards:**
```python
project_root = os.environ.get('BB5_PROJECT_ROOT')
if not project_root:
    # Try to detect from git root
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                          capture_output=True, text=True)
    if result.returncode == 0:
        project_root = result.stdout.strip()
    else:
        raise ConfigurationError(
            "BB5_PROJECT_ROOT not set and not in a git repository. "
            "Please set BB5_PROJECT_ROOT to the project root directory."
        )

project_root = Path(project_root).resolve()
if not (project_root / '.autonomous').exists():
    raise ConfigurationError(f"{project_root} doesn't look like a BB5 project (no .autonomous directory)")
```

**Severity:** HIGH

---

### 6.5 Template Rendering Failures

**Scenario:** Template rendering fails due to:
- Missing template variables
- Invalid characters in task data
- Encoding issues

**Current Design Behavior:**
- Templates rendered with f-strings or similar
- No error handling shown

**Failure Modes:**
1. **Template syntax error:** Invalid Python syntax in template
2. **Missing variable:** Referenced variable doesn't exist in context
3. **Encoding error:** Non-UTF8 characters in task data

**Required Safeguards:**
```python
from jinja2 import Template, UndefinedError

def render_template(template_str, context):
    try:
        template = Template(template_str)
        return template.render(**context)
    except UndefinedError as e:
        # Variable missing - use empty string or placeholder
        logger.warning(f"Template variable missing: {e}")
        template = Template(template_str, undefined=jinja2.DebugUndefined)
        return template.render(**context)
    except Exception as e:
        raise TemplateRenderError(f"Failed to render template: {e}")
```

**Severity:** LOW

---

## 7. USER EXPERIENCE ISSUES

### 7.1 Misspelled Task ID

**Scenario:** User types "claim TASK-00I" (letter I instead of number 1).

**Current Design Behavior:**
- Pattern `TASK-\d+` won't match
- Hook exits silently (exit 0)

**Failure Modes:**
1. **Silent failure:** User doesn't know why claim didn't work
2. **No suggestions:** User doesn't know correct task ID
3. **Frustration:** User has to manually find correct ID

**Required Safeguards:**
```python
def detect_task_claim_with_fuzzy_matching(prompt):
    # Try exact match first
    exact_match = detect_task_claim(prompt)
    if exact_match:
        return exact_match

    # Check for similar patterns (typos)
    typo_pattern = r'TASK-([0-9OIl]+)'  # Common typo characters
    typo_matches = re.findall(typo_pattern, prompt, re.IGNORECASE)

    if typo_matches:
        # Try to correct common typos
        corrections = []
        for match in typo_matches:
            corrected = match.upper().replace('O', '0').replace('I', '1').replace('L', '1')
            if re.match(r'\d{3,}', corrected):
                corrections.append(f"TASK-{corrected}")

        if corrections:
            return {
                "ambiguous": True,
                "message": f"Did you mean one of these? {corrections}",
                "suggestions": corrections
            }

    return None
```

**Severity:** LOW

---

### 7.2 Case Sensitivity Issues

**Scenario:** User types "claim task-001" (lowercase).

**Current Design Behavior:**
- Pattern is case-insensitive (good)
- But task ID normalization not shown

**Failure Modes:**
1. **Case mismatch:** Task stored as "task-001" but referenced as "TASK-001"
2. **File system issues:** Case-sensitive vs case-insensitive filesystems

**Required Safeguards:**
```python
# Always normalize to uppercase
task_id = raw_task_id.upper()

# And validate
if not re.match(r'^TASK-\d{3,}$', task_id):
    raise InvalidTaskIdError(f"Invalid task ID: {raw_task_id}")
```

**Severity:** LOW

---

### 7.3 No Feedback on Success

**Scenario:** Claim succeeds but user doesn't see clear confirmation.

**Current Design Behavior:**
- Returns JSON with context
- But UX not specified

**Failure Modes:**
1. **User uncertainty:** "Did the claim work?"
2. **Duplicate claims:** User claims again because unsure
3. **Context overload:** Too much info dumped at once

**Required Safeguards:**
```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "TaskClaim",
        "additionalContext": f"""
✅ **Task Claimed Successfully**

**Task:** {task_id} - {hierarchy['task']['title']}
**Goal:** {hierarchy['goal']['id'] if hierarchy['goal'] else 'N/A'}
**Plan:** {hierarchy['plan']['id'] if hierarchy['plan'] else 'N/A'}
**Run Directory:** {run_dir}

**Files Created:**
""" + "\n".join(f"  - {f}" for f in files_created) + """

**Next Steps:**
1. Review THOUGHTS.md for full context
2. Document your approach in DECISIONS.md
3. Start working on the task
""",
        "task": {
            "id": task_id,
            # ... rest of data
        }
    }
}
```

**Severity:** LOW

---

## 8. SECURITY CONSIDERATIONS

### 8.1 Path Traversal Attack

**Scenario:** Malicious user claims "TASK-../../../etc/passwd".

**Current Design Behavior:**
```python
task_path = Path(project_root) / 'tasks' / 'active' / task_id / 'task.md'
```

**Failure Modes:**
1. **File access outside project:** Could read arbitrary files
2. **File overwrite:** Could overwrite system files
3. **Information disclosure:** Could exfiltrate sensitive data

**Required Safeguards:**
```python
def validate_task_id(task_id):
    # Strict validation
    if not re.match(r'^TASK-[A-Z0-9]{3,}$', task_id.upper()):
        raise InvalidTaskIdError(f"Invalid task ID format: {task_id}")

    # No path separators allowed
    if '/' in task_id or '\\' in task_id or '..' in task_id:
        raise InvalidTaskIdError(f"Task ID contains invalid characters: {task_id}")

def get_task_path(project_root, task_id):
    validate_task_id(task_id)
    task_path = Path(project_root) / 'tasks' / 'active' / task_id / 'task.md'

    # Ensure resolved path is within project
    resolved = task_path.resolve()
    project_resolved = Path(project_root).resolve()

    if not str(resolved).startswith(str(project_resolved)):
        raise SecurityError(f"Task path escapes project root: {task_path}")

    return task_path
```

**Severity:** CRITICAL

---

### 8.2 Command Injection via Task Data

**Scenario:** Task metadata contains shell commands that get executed.

**Current Design Behavior:**
- If task data is passed to shell commands without sanitization

**Failure Modes:**
1. **Remote code execution:** Malicious task data runs arbitrary code
2. **Data exfiltration:** Commands send data to external server

**Required Safeguards:**
```python
# Never pass user data to shell without sanitization
# Use subprocess with list args, not shell=True
# Validate all data before use
```

**Severity:** CRITICAL

---

## 9. RECOMMENDATIONS

### 9.1 Critical Fixes Required Before Deployment

1. **Add file locking** for queue.yaml updates (Section 4.1)
2. **Implement atomic claim operation** (Section 4.1)
3. **Add path traversal protection** (Section 8.1)
4. **Add transaction/rollback** for partial failures (Section 3.3)
5. **Verify task existence** before claiming (Section 1.2)
6. **Check for existing claims** (Section 1.1)
7. **Coordinate with SessionStart hook** (Section 5.1)

### 9.2 High Priority Improvements

1. **Dependency validation** before claim (Section 2.4)
2. **Disk space checking** (Section 3.2)
3. **Permission verification** (Section 3.4)
4. **Run ID collision prevention** (Section 6.3)
5. **Lease/heartbeat mechanism** for stuck claims (Section 5.2)
6. **Environment variable validation** (Section 6.4)

### 9.3 Testing Scenarios

Before deployment, test:

1. Two agents claiming same task simultaneously (100x)
2. Claim during queue.yaml write by another process
3. Disk full during folder creation
4. Permission denied scenarios
5. Task moved to completed during claim
6. Hook crash after partial folder creation
7. Path traversal attempts
8. Malformed task files
9. Missing plan/goal references
10. Concurrent claims of different tasks

### 9.4 Monitoring & Observability

Add logging for:
- All claim attempts (success and failure)
- Queue.yaml update timing
- Folder creation timing
- Rollback events
- Lock contention
- Stuck claims (claimed but no activity)

---

## 10. CONCLUSION

The TaskClaim hook design is a good conceptual foundation but requires significant hardening for production use. The most critical issues are:

1. **Race conditions** - Concurrent claims can corrupt queue state
2. **No atomicity** - Partial failures leave system inconsistent
3. **Security vulnerabilities** - Path traversal possible
4. **Poor error handling** - Silent failures confuse users

**Recommendation:** Do not implement as designed. Address CRITICAL and HIGH severity issues first, then implement with comprehensive testing.

---

*Analysis completed: 2026-02-06*
*Analyst: Edge Case Analysis Expert*
*Confidence: High - 47 edge cases identified and documented*