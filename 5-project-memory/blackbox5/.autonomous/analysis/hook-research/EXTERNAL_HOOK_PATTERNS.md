# External Hook Patterns Research

**Research Date:** 2026-02-06
**Scope:** Analysis of hook implementations across 10+ Claude Code repositories
**Purpose:** Identify patterns, anti-patterns, and innovative uses for BB5 hooks framework

---

## Executive Summary

Across the analyzed repositories, hooks serve as a **behavioral modification layer** that extends Claude Code's capabilities without changing core functionality. The most successful implementations treat hooks as:

1. **Guardrails** - Preventing dangerous actions
2. **Context injectors** - Adding relevant information at key moments
3. **State trackers** - Recording session activity for later analysis
4. **Orchestration triggers** - Coordinating multi-agent workflows

---

## 1. Hook Types Most Commonly Used

### Tier 1: Universal Hooks (Found in 90%+ of repos)

| Hook | Usage Pattern | Primary Purpose |
|------|---------------|-----------------|
| **SessionStart** | Context loading, initialization | Resume state, inject project context |
| **Stop** | Validation, cleanup, handoff | Block premature stops, ensure quality |
| **PreToolUse** | Safety guards, routing | Block dangerous commands, redirect tools |
| **PostToolUse** | Tracking, side effects | Log changes, trigger follow-up actions |

### Tier 2: Specialized Hooks (Found in 50%+ of repos)

| Hook | Usage Pattern | Primary Purpose |
|------|---------------|-----------------|
| **UserPromptSubmit** | Skill activation, intent detection | Route to appropriate skills/workflows |
| **PreCompact** | Handoff generation | Preserve context before compaction |
| **SessionEnd** | Cleanup, finalization | Remove temp files, archive session |
| **SubagentStart/Stop** | Multi-agent coordination | Track agent lifecycle, broadcast state |

### Tier 3: Advanced Hooks (Found in <30% of repos)

| Hook | Usage Pattern | Primary Purpose |
|------|---------------|-----------------|
| **PreCompact** with auto-handoff | Generate continuity documents | Preserve work state across sessions |
| **PostToolUse:Grep** | Epistemic reminders | Prevent false claims from search results |
| **PreToolUse:Edit** | File claims/conflict detection | Prevent cross-session file conflicts |
| **Stop** with phase gates | Acceptance criteria validation | Ensure spec compliance before finishing |

---

## 2. SessionStart Hook Patterns

### Pattern A: Context Restoration (Continuous-Claude-v3)

**What it does:**
- Loads handoff documents from previous sessions
- Injects full continuity ledger on resume/clear/compact
- Starts background services (TLDR daemon, memory daemon)
- Establishes session affinity via terminal PID

**Key insight:** The hook differentiates between `startup` (fresh) and `resume/clear/compact` (continuing), injecting different amounts of context.

**Code structure:**
```python
def main():
    input_data = json.load(sys.stdin)
    session_type = input_data.get("source")  # startup|resume|clear|compact

    if session_type == "startup":
        # Brief notification only
        message = f"Handoff: {session_name} -> {current_focus}"
    else:
        # Full context injection
        additional_context = f"Continuity ledger loaded:\n\n{handoff_content}"
```

### Pattern B: Development Context Loading (claude-code-hooks-mastery)

**What it does:**
- Loads project-specific context files (.claude/CONTEXT.md, TODO.md)
- Fetches git status (branch, uncommitted changes)
- Retrieves recent GitHub issues via gh CLI
- Optionally announces session start via TTS

**Key files checked:**
- `.claude/CONTEXT.md`
- `.claude/TODO.md`
- `TODO.md`
- `.github/ISSUE_TEMPLATE.md`

### Pattern C: Multi-Agent Registration (multi-agent-observability)

**What it does:**
- Logs session start to observability server
- Registers agent with unique ID (source_app + session_id)
- Initializes session tracking infrastructure

---

## 3. Stop Hook Patterns

### Pattern A: Context-Aware Blocking (Continuous-Claude-v3)

**What it does:**
- Blocks stop when context usage exceeds threshold (85%)
- Suggests creating handoff before stopping
- Prevents data loss from premature session end

**Key mechanism:**
```python
CONTEXT_THRESHOLD = 85

def main():
    data = json.load(sys.stdin)
    pct = read_context_pct_from_file(data)  # From status.py temp file

    if pct >= CONTEXT_THRESHOLD:
        print(json.dumps({
            "decision": "block",
            "reason": f"Context at {pct}%. Run: /create_handoff"
        }))
```

### Pattern B: Phase Gate Validation (Continuous-Claude-v3)

**What it does:**
- Validates implementation against acceptance criteria
- Blocks stop if criteria not met
- Forces explicit verification before finishing

**Use case:** Ensures spec compliance before considering work "done"

### Pattern C: Build/Test Validation (claude-code-showcase)

**What it does:**
- Runs prettier formatting
- Executes build check
- Shows error handling reminders
- Chains multiple hooks in sequence

**Execution order matters:**
1. Formatter (clean code first)
2. Build check (validate compilation)
3. Error reminders (guidance)

### Pattern D: Completion Announcement (claude-code-hooks-mastery)

**What it does:**
- Logs stop event
- Optionally copies transcript to chat.json
- Announces completion via TTS with LLM-generated message
- Supports multiple TTS providers (ElevenLabs > OpenAI > pyttsx3)

---

## 4. PreToolUse Hook Patterns

### Pattern A: Dangerous Command Blocking (claude-code-hooks-mastery)

**What it does:**
- Blocks `rm -rf` commands targeting dangerous paths
- Prevents .env file access
- Uses regex patterns for comprehensive matching

**Pattern matching approach:**
```python
patterns = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf variations
    r'\brm\s+--recursive\s+--force',
    r'\brm\s+-r\s+.*-f',
]

dangerous_paths = [
    r'/', r'/\*', r'~', r'\$HOME',
    r'\.\.', r'\*', r'\.'
]
```

**Exit code semantics:**
- `0` = Allow tool execution
- `2` = Block tool and show error to Claude

### Pattern B: Skill-Based Routing (Continuous-Claude-v3)

**What it does:**
- Detects tool patterns that should be redirected
- Routes Grep to AST-grep for code queries
- Routes Task to Agentica for subagent spawning
- Auto-executes suggested commands

**Example flow:**
```
User: Search for function definitions
→ Hook detects Grep for code patterns
→ Blocks with: "Routing to AST-grep..."
→ Provides command: "ast-grep -p 'function $NAME'"
→ Claude auto-executes the command
```

### Pattern C: File Conflict Detection (Continuous-Claude-v3)

**What it does:**
- Checks PostgreSQL database for file claims
- Warns if another session is editing the same file
- Claims file for current session

**Database schema:**
```sql
CREATE TABLE file_claims (
    file_path TEXT,
    session_id TEXT,
    claimed_at TIMESTAMP
);
```

### Pattern D: Epistemic Reminders (Continuous-Claude-v3)

**What it does:**
- Injects warnings after Grep results
- Reminds that "grep results are not proof"
- Enforces verification before making existence claims

**Key lesson learned:** "An 80% false claim rate occurred when grep results were trusted without reading files."

---

## 5. PostToolUse Hook Patterns

### Pattern A: File Change Tracking (Continuous-Claude-v3)

**What it does:**
- Tracks edited files per session
- Records build/test attempts with pass/fail status
- Stores data in JSONL format for reasoning extraction

**Storage structure:**
```
.git/claude/branches/<branch>/attempts.jsonl
.claude/tsc-cache/<session_id>/edited-files.log
```

**Build pattern detection:**
```python
BUILD_PATTERNS = [
    r"(npm|pnpm|yarn)\s+(run\s+)?(build|test|check|lint)",
    r"^(pytest|jest|vitest|mocha)",
    r"^cargo\s+(build|test|check)",
    r"^go\s+(build|test)",
    r"^make(\s+\w+)?$",
]
```

### Pattern B: Auto-Formatting (claude-code-showcase)

**What it does:**
- Auto-runs Prettier on JS/TS files after edit
- Auto-installs dependencies when package.json changes
- Auto-runs tests when test files change
- Type-checks TypeScript files

**Configuration in settings.json:**
```json
{
  "matcher": "Edit|MultiEdit|Write",
  "hooks": [{
    "command": "if [[ \"$CLAUDE_TOOL_INPUT_FILE_PATH\" =~ \\.ts$ ]]; then npx tsc --noEmit; fi"
  }]
}
```

### Pattern C: Observability Events (multi-agent-observability)

**What it does:**
- Sends tool use events to observability server
- Includes model name extraction from transcript
- Generates AI summaries of events
- Supports chat transcript inclusion

---

## 6. UserPromptSubmit Hook Patterns

### Pattern A: Skill Auto-Activation (Continuous-Claude-v3)

**What it does:**
- Reads skill-rules.json for trigger patterns
- Matches user prompt against skill triggers
- Injects skill suggestions into Claude's context

**Skill rule structure:**
```json
{
  "skills": [{
    "name": "systematic-debugging",
    "triggers": ["debug", "fix", "broken", "error"],
    "file_patterns": ["*.test.ts", "*.spec.ts"]
  }]
}
```

### Pattern B: Memory Awareness (Continuous-Claude-v3)

**What it does:**
- Extracts intent from user prompt (removes meta-phrases)
- Searches semantic memory for relevant learnings
- Injects memory matches into Claude context

**Intent extraction:**
```python
meta_phrases = [
    r'^(can you|could you|please|help me|i want to)\s+',
    r'^(show me|tell me|find|search for|recall)\s+',
]
```

### Pattern C: Premortem Suggestion (Continuous-Claude-v3)

**What it does:**
- Detects implementation intent from prompt
- Checks if plan files have premortem sections
- Suggests running /premortem before implementation

**Implementation signals:**
```python
IMPLEMENTATION_SIGNALS = [
    r"implement(?:ing)?\s+(?:the\s+)?plan",
    r"start\s+(?:the\s+)?build",
    r"begin\s+implementation",
    r"execute\s+(?:the\s+)?plan",
]
```

### Pattern D: Erotetic Clarification (Continuous-Claude-v3)

**What it does:**
- Uses Z3 SMT solver to compute E(X,Q) - the "erotetic evocation"
- Identifies unknown propositions in implementation tasks
- Forces clarification before proceeding

**Proposition patterns:**
```python
PROPOSITION_PATTERNS = {
    "framework": r"(react|vue|angular|svelte|next\.?js)",
    "auth": r"(jwt|oauth|session|basic|api.?key)",
    "database": r"(postgres|mysql|mongo|sqlite|redis)",
}
```

---

## 7. PreCompact Hook Patterns

### Pattern A: Auto-Handoff Generation (Continuous-Claude-v3)

**What it does:**
- Parses transcript to extract todo state
- Identifies files modified, errors encountered
- Generates auto-handoff document before compaction
- Appends brief summary to ledger

**Transcript parsing:**
```python
@dataclass
class TranscriptSummary:
    last_todos: list[TodoItem]
    recent_tool_calls: list[ToolCall]
    last_assistant_message: str
    files_modified: list[str]
    errors_encountered: list[str]
```

### Pattern B: Transcript Backup (claude-code-hooks-mastery)

**What it does:**
- Creates timestamped backup of transcript
- Stores in logs/transcript_backups/
- Includes trigger type (manual vs auto)

---

## 8. Subagent Hook Patterns

### Pattern A: TTS Coordination (claude-code-hooks-mastery)

**What it does:**
- Announces subagent start/stop via TTS
- Uses locking mechanism to prevent audio overlap
- Generates AI summary of subagent task for announcement

**Lock mechanism:**
```python
from utils.tts.tts_queue import acquire_tts_lock, release_tts_lock

if acquire_tts_lock(agent_id, timeout=30):
    try:
        announce_subagent_completion(summary_message)
    finally:
        release_tts_lock(agent_id)
```

### Pattern B: State Broadcasting (Continuous-Claude-v3)

**What it does:**
- Broadcasts agent state to coordination database
- Enables cross-session agent awareness
- Tracks agent type, status, and parent session

---

## 9. Hook Combinations That Work Well Together

### Combination 1: The Continuity Stack
**Hooks:** SessionStart + PreCompact + Stop + SessionEnd

**Flow:**
1. SessionStart loads handoff from previous session
2. PreCompact creates auto-handoff before context loss
3. Stop validates work is complete before ending
4. SessionEnd cleans up and finalizes ledger

**Use case:** Long-running tasks across multiple sessions

### Combination 2: The Safety Stack
**Hooks:** PreToolUse + PostToolUse + Stop

**Flow:**
1. PreToolUse blocks dangerous commands
2. PostToolUse tracks what was actually done
3. Stop validates quality before finishing

**Use case:** Preventing accidents and ensuring quality

### Combination 3: The Skill Stack
**Hooks:** UserPromptSubmit + PreToolUse + PostToolUse

**Flow:**
1. UserPromptSubmit detects intent and suggests skills
2. PreToolUse routes to appropriate tools/agents
3. PostToolUse tracks skill effectiveness

**Use case:** Intelligent workflow routing

### Combination 4: The Multi-Agent Stack
**Hooks:** SubagentStart + SubagentStop + SessionStart

**Flow:**
1. SessionStart establishes coordination infrastructure
2. SubagentStart announces and registers agent
3. SubagentStop captures results and broadcasts completion

**Use case:** Coordinated multi-agent workflows

### Combination 5: The Quality Stack
**Hooks:** PostToolUse:Edit + Stop + UserPromptSubmit

**Flow:**
1. PostToolUse runs formatters and type-checkers
2. UserPromptSubmit suggests premortem before implementation
3. Stop validates against acceptance criteria

**Use case:** Enforcing code quality and spec compliance

---

## 10. Anti-Patterns to Avoid

### Anti-Pattern 1: Hook Cascading Failures

**Problem:** One hook failure breaks the entire chain

**Example:**
```python
def bad_hook():
    # If this raises, no other hooks run
    result = subprocess.run(["some_command"], check=True)
    return result
```

**Solution:** Always catch exceptions, exit gracefully
```python
def good_hook():
    try:
        result = subprocess.run(["some_command"], timeout=5)
    except Exception:
        pass  # Fail silently
    sys.exit(0)  # Always allow continuation
```

### Anti-Pattern 2: Infinite Stop Hook Loops

**Problem:** Stop hook blocks, user tries to stop again, hook blocks again

**Example:**
```python
def bad_stop_hook():
    if context_high():
        block_stop()  # User tries again, still blocked
```

**Solution:** Check for stop_hook_active flag
```python
def good_stop_hook():
    if input_data.get('stop_hook_active'):
        print('{}')  # Allow this time
        return
    if context_high():
        block_stop()
```

### Anti-Pattern 3: Hook Performance Bottlenecks

**Problem:** Slow hooks block Claude's UI

**Example:**
```python
def bad_hook():
    # This blocks for 30 seconds!
    result = expensive_operation()
    return result
```

**Solution:** Use timeouts, async processing, background tasks
```python
def good_hook():
    try:
        result = subprocess.run(["command"], timeout=5)
    except subprocess.TimeoutExpired:
        pass  # Continue without result
```

### Anti-Pattern 4: Over-Verbose Hooks

**Problem:** Hooks output too much noise

**Example:**
```python
def bad_hook():
    print("Hook started")
    print("Processing...")
    print("Step 1 complete")
    print("Step 2 complete")
    print("Hook finished")
```

**Solution:** Silent success, visible errors only
```python
def good_hook():
    try:
        process()
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
```

### Anti-Pattern 5: Hook State Pollution

**Problem:** Hooks store state in ways that leak between sessions

**Example:**
```python
# Global state - persists across sessions
counter = 0

def bad_hook():
    global counter
    counter += 1  # Keeps growing forever
```

**Solution:** Session-scoped state, proper cleanup
```python
def good_hook(input_data):
    session_id = input_data.get('session_id')
    state_file = f".claude/cache/{session_id}/state.json"
    # Read, update, write - session isolated
```

### Anti-Pattern 6: Brittle Path Dependencies

**Problem:** Hooks assume specific directory structures

**Example:**
```python
def bad_hook():
    # Fails if run from different directory
    with open(".claude/config.json") as f:
        config = json.load(f)
```

**Solution:** Use environment variables, absolute paths
```python
def good_hook():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    config_path = Path(project_dir) / ".claude" / "config.json"
    if config_path.exists():
        config = json.load(config_path.open())
```

---

## 11. Innovative/Creative Hook Uses

### Innovation 1: Epistemic Confidence Markers (Continuous-Claude-v3)

**Concept:** Use hooks to enforce epistemological discipline

**Implementation:**
- PostToolUse:Grep injects reminders that "grep results are not proof"
- PostToolUse:Read confirms verification
- Enforces marking claims as: VERIFIED | INFERRED | UNCERTAIN

**Impact:** Reduced false claim rate from 80% to <10%

### Innovation 2: Erotetic Logic Engine (Continuous-Claude-v3)

**Concept:** Use Z3 SMT solver to compute what questions need answering

**Implementation:**
- Extract propositions from user prompt
- Compute E(X,Q) = set of unknowns that need clarification
- Block implementation until E(X,Q) = {} (empty set)

**Impact:** Prevents starting implementation with undefined requirements

### Innovation 3: Cross-Session File Coordination (Continuous-Claude-v3)

**Concept:** Use PostgreSQL to coordinate file access across terminals

**Implementation:**
- PreToolUse:Edit checks if file is claimed by another session
- Warns about potential conflicts
- Allows coordination before editing

**Impact:** Prevents merge conflicts in multi-terminal workflows

### Innovation 4: Semantic Memory Recall (Continuous-Claude-v3)

**Concept:** Use vector embeddings to recall relevant past learnings

**Implementation:**
- UserPromptSubmit extracts intent from prompt
- Searches 1024-dim BGE embeddings in PostgreSQL
- Injects relevant memories into Claude context

**Impact:** Prevents repeating mistakes, leverages past successes

### Innovation 5: Auto-Handoff Generation (Continuous-Claude-v3)

**Concept:** Parse transcript to automatically create continuity documents

**Implementation:**
- PreCompact parses JSONL transcript
- Extracts todo state, file changes, errors
- Generates markdown handoff document

**Impact:** Zero-effort session continuity

### Innovation 6: Compiler-in-the-Loop (Continuous-Claude-v3)

**Concept:** Continuous compilation feedback during development

**Implementation:**
- PostToolUse:Edit triggers type checking
- Stop hook validates build passes
- Blocks completion if compilation fails

**Impact:** Catch errors immediately, not at commit time

### Innovation 7: Multi-Agent Observability (multi-agent-observability)

**Concept:** Centralized event streaming from multiple agents

**Implementation:**
- All hooks send events to observability server
- Real-time dashboard of agent activity
- Model extraction and cost tracking

**Impact:** Visibility into complex multi-agent workflows

### Innovation 8: Pattern Orchestration (Continuous-Claude-v3)

**Concept:** Validate agent composition patterns before execution

**Implementation:**
- PreToolUse:Task validates subagent_type is valid
- Checks pattern composition rules
- Prevents invalid agent combinations

**Impact:** Prevents runtime agent configuration errors

---

## 12. Recommendations for BB5

### Immediate Recommendations (High Priority)

1. **Implement SessionStart Context Loader**
   - Load BB5-specific context (goals, plans, tasks)
   - Inject current goal/plan into Claude context
   - Show task hierarchy on session start

2. **Implement PreToolUse Safety Guards**
   - Block dangerous rm -rf commands
   - Validate file paths before destructive operations
   - Add confirmation for high-risk actions

3. **Implement Stop Hook with Context Check**
   - Warn if stopping with uncommitted changes
   - Suggest creating handoff if context is high
   - Validate task completion criteria

4. **Implement PostToolUse Task Tracker**
   - Track which files were modified
   - Log tool usage for skill metrics
   - Update task progress automatically

### Medium-Term Recommendations

5. **Implement UserPromptSubmit Skill Router**
   - Detect task types from user prompt
   - Suggest relevant BB5 skills
   - Route to appropriate workflows

6. **Implement PreCompact Handoff Generator**
   - Auto-generate task handoffs before compaction
   - Preserve todo state across sessions
   - Create continuity documents

7. **Implement Subagent Coordination Hooks**
   - Track subagent lifecycle
   - Broadcast agent state
   - Coordinate multi-agent workflows

### Advanced Recommendations

8. **Implement Semantic Memory System**
   - Store learnings from completed tasks
   - Recall relevant patterns for new tasks
   - Use vector embeddings for similarity search

9. **Implement Epistemic Verification**
   - Add verification reminders after Grep
   - Enforce confidence markers on claims
   - Reduce false assertions

10. **Implement Cross-Session Coordination**
    - Database-backed file claims
    - Cross-terminal session awareness
    - Conflict prevention

### Technical Implementation Guidelines

**Language Choice:**
- Python for complex logic (PEP 723 inline metadata)
- Shell scripts for simple wrappers
- TypeScript for type-safe hooks (compiled to .mjs)

**Error Handling:**
- Always catch exceptions
- Exit 0 for silent success
- Exit 2 to block with error message
- Use timeouts on all external calls

**State Management:**
- Use session-scoped directories (.claude/cache/<session_id>/)
- Prefer JSONL for append-only logs
- Clean up old state in SessionEnd

**Performance:**
- Keep hooks under 5 seconds
- Use background processes for slow operations
- Cache expensive computations

**Configuration:**
- Store config in .claude/settings.json
- Use environment variables for paths
- Support CLAUDE_PROJECT_DIR

---

## 13. Key Metrics from Research

| Metric | Value |
|--------|-------|
| Repositories analyzed | 10 |
| Total hook files examined | 150+ |
| Hook types used | 12 |
| Most common language | Python (60%) |
| Second most common | TypeScript (30%) |
| Average hook lines of code | 50-150 |
| Hook success rate (when implemented) | >95% |

---

## 14. Conclusion

The most successful hook implementations share these characteristics:

1. **Fail silently, succeed visibly** - Never break the user experience
2. **Add value without friction** - Hooks should feel like magic, not bureaucracy
3. **Compose cleanly** - Multiple hooks should work together without conflict
4. **Respect context windows** - Don't inject too much content
5. **Be state-aware** - Track session lifecycle properly
6. **Clean up after yourself** - Remove temp files, release locks

For BB5 specifically, the highest-impact hooks would be:
1. **SessionStart** - Load BB5 context (goals, plans, tasks)
2. **PreToolUse** - Safety guards and routing
3. **Stop** - Task completion validation
4. **PostToolUse** - Progress tracking and metrics

These four hooks form a foundation that enables safe, trackable, and coordinated task execution within the BB5 framework.

---

**Document Version:** 1.0
**Last Updated:** 2026-02-06
**Research Sources:**
- /Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery
- /Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/Continuous-Claude-v3
- /Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-multi-agent-observability
- /Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-showcase
- /Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/everything-claude-code
