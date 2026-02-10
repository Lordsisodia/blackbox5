# michaelshimeles/ralphy Analysis

**Repository:** https://github.com/michaelshimeles/ralphy
**Version:** 4.7.2 (npm: ralphy-cli)
**License:** MIT
**Analyzed:** 2026-02-10

---

## Overview

Ralphy is a mature, production-ready autonomous AI coding framework that orchestrates AI agents to execute tasks from PRDs (Product Requirements Documents) or single-task prompts. It supports 8 different AI engines (Claude Code, OpenCode, Cursor, Codex, Qwen, Droid, Copilot, Gemini) and provides both sequential and parallel execution modes.

**Key Differentiator:** Ralphy's git worktree-based parallel execution pattern is its standout feature, enabling true isolation between agents while maintaining git history and enabling safe merge strategies.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Ralphy CLI                               │
├─────────────────────────────────────────────────────────────────┤
│  CLI Layer (Commander)                                          │
│  ├── commands/run.ts      - Main execution orchestrator         │
│  ├── commands/task.ts     - Single task execution               │
│  ├── commands/init.ts     - Project configuration               │
│  └── commands/config.ts   - Configuration management            │
├─────────────────────────────────────────────────────────────────┤
│  Task Sources                                                   │
│  ├── Markdown (PRD.md)    - Checkbox task lists                 │
│  ├── Markdown Folder      - Multiple .md files                  │
│  ├── YAML                 - Structured task definitions         │
│  ├── JSON                 - With parallel group support         │
│  └── GitHub Issues        - Issue-based tasks                   │
├─────────────────────────────────────────────────────────────────┤
│  Execution Engine                                               │
│  ├── Sequential Mode      - One task at a time                  │
│  └── Parallel Mode        - Multiple agents via worktrees       │
│       ├── Git Worktrees   - Full git isolation                  │
│       └── Sandbox Mode    - Symlink-based lightweight           │
├─────────────────────────────────────────────────────────────────┤
│  AI Engine Adapters                                             │
│  ├── Claude Code          - Primary/default engine              │
│  ├── OpenCode             - Alternative open source             │
│  ├── Cursor               - IDE-based agent                     │
│  ├── Codex                - OpenAI's coding model               │
│  ├── Qwen                 - Alibaba's coding model              │
│  ├── Droid                - Factory AI agent                    │
│  ├── Copilot              - GitHub Copilot CLI                  │
│  └── Gemini               - Google's coding model               │
├─────────────────────────────────────────────────────────────────┤
│  Git Operations                                                 │
│  ├── Worktree Manager     - Create/cleanup agent worktrees      │
│  ├── Branch Manager       - Per-task branch creation            │
│  ├── Merge Engine         - Conflict detection & resolution     │
│  └── PR Creator           - Automated PR generation             │
├─────────────────────────────────────────────────────────────────┤
│  Supporting Systems                                             │
│  ├── Config Manager       - .ralphy/config.yaml                 │
│  ├── Prompt Builder       - Context-aware prompt construction   │
│  ├── Retry Handler        - Exponential backoff for failures    │
│  ├── Telemetry            - Usage analytics                     │
│  └── Notifications        - Discord/Slack webhooks              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. CLI Interface (`cli/src/cli/`)
- **args.ts**: Argument parsing with Commander
- **commands/run.ts**: Main orchestration logic
- **commands/task.ts**: Single-task mode
- **commands/init.ts**: Project initialization with auto-detection

### 2. Task Sources (`cli/src/tasks/`)
- **types.ts**: Task interface with parallel group support
- **markdown.ts**: Checkbox parsing (`- [ ] task`)
- **markdown-folder.ts**: Multi-file aggregation
- **yaml.ts**: YAML task definitions
- **json.ts**: JSON with parallel_group field
- **github.ts**: GitHub Issues integration
- **cached-task-source.ts**: Performance optimization via caching

### 3. Execution Engine (`cli/src/execution/`)
- **sequential.ts**: Single-threaded task execution
- **parallel.ts**: Multi-agent parallel execution (core innovation)
- **sandbox.ts**: Lightweight symlink-based isolation
- **sandbox-git.ts**: Git operations for sandbox mode
- **prompt.ts**: Prompt construction with context/rules
- **retry.ts**: Retry logic with exponential backoff
- **conflict-resolution.ts**: AI-assisted merge conflict resolution
- **browser.ts**: agent-browser integration for UI automation

### 4. Git Operations (`cli/src/git/`)
- **worktree.ts**: Git worktree creation/management
- **branch.ts**: Branch creation and switching
- **merge.ts**: Merge analysis and execution
- **pr.ts**: GitHub PR creation
- **issue-sync.ts**: Sync progress to GitHub issues

### 5. AI Engine Adapters (`cli/src/engines/`)
- **types.ts**: Common AIEngine interface
- **base.ts**: Shared engine functionality
- **claude.ts**: Claude Code integration (default)
- **opencode.ts**: OpenCode integration
- **cursor.ts**: Cursor agent integration
- **codex.ts**: OpenAI Codex integration
- **qwen.ts**: Qwen-Code integration
- **droid.ts**: Factory Droid integration
- **copilot.ts**: GitHub Copilot CLI integration
- **gemini.ts**: Gemini CLI integration

---

## Git Worktree Parallel Execution

### The Pattern

Ralphy's most innovative feature is using git worktrees for parallel agent execution:

```
Main Repository (.git/)
    │
    ├── Worktree 1 (/tmp/ralphy-xxx/agent-1/)
    │   ├── src/          (isolated working copy)
    │   └── branch: ralphy/agent-1-add-auth
    │
    ├── Worktree 2 (/tmp/ralphy-xxx/agent-2/)
    │   ├── src/          (isolated working copy)
    │   └── branch: ralphy/agent-2-create-dashboard
    │
    └── Worktree 3 (/tmp/ralphy-xxx/agent-3/)
        ├── src/          (isolated working copy)
        └── branch: ralphy/agent-3-build-api
```

### Implementation Details

**Worktree Creation** (`cli/src/git/worktree.ts:22-48`):
```typescript
export async function createAgentWorktree(
    taskName: string,
    agentNum: number,
    baseBranch: string,
    worktreeBase: string,
    originalDir: string,
): Promise<{ worktreeDir: string; branchName: string }> {
    const uniqueId = generateUniqueId();
    const branchName = `ralphy/agent-${agentNum}-${uniqueId}-${slugify(taskName)}`;
    const worktreeDir = join(worktreeBase, `agent-${agentNum}-${uniqueId}`);

    // Use atomic -B flag to create/reset branch in one operation
    await git.raw(["worktree", "add", "-B", branchName, worktreeDir, baseBranch]);

    return { worktreeDir, branchName };
}
```

**Key Features:**
1. **Atomic branch creation**: Uses `git worktree add -B` to avoid race conditions
2. **Unique identifiers**: Timestamp + random suffix prevents collisions
3. **Automatic cleanup**: Worktrees removed after task completion
4. **Dirty worktree preservation**: Failed tasks leave worktrees intact for debugging
5. **Branch preservation**: Successfully merged branches can be kept for PRs

### Parallel Execution Flow

**Batch Processing** (`cli/src/execution/parallel.ts:316-437`):
1. Get next batch of tasks (up to maxParallel)
2. For each task, create worktree + branch
3. Copy PRD file to worktree
4. Execute AI agent in worktree directory
5. Collect results in parallel
6. Cleanup worktrees
7. Merge successful branches back to base

**Merge Phase** (`cli/src/execution/parallel.ts:676-774`):
1. **Pre-merge analysis**: Run `git diff` in parallel for all branches
2. **Conflict likelihood sorting**: Merge clean branches first
3. **Sequential merges**: Git locking requires sequential execution
4. **AI conflict resolution**: Use AI to resolve merge conflicts
5. **Parallel cleanup**: Delete merged branches

### Sandbox Mode Alternative

For large repos with heavy dependencies, Ralphy offers sandbox mode:

**Symlink Strategy** (`cli/src/execution/sandbox.ts:63-111`):
- **Symlink**: node_modules, .git, vendor, .venv, .cache (read-only)
- **Copy**: src/, app/, config files (writable)

**Benefits:**
- Avoids duplicating gigabytes of dependencies
- Much faster creation for large monorepos
- Changes synced back via git commit

---

## Agent Orchestration

### Task Distribution

**Parallel Groups** (JSON/YAML tasks):
```yaml
tasks:
  - title: Create User model
    parallel_group: 1    # Runs with group 1
  - title: Create Post model
    parallel_group: 1    # Runs with group 1
  - title: Add relationships
    parallel_group: 2    # Runs after group 1 completes
```

**Dynamic Batching**:
- Tasks without groups run in FIFO order
- Batch size controlled by `--max-parallel` (default: 3)
- Global agent counter ensures unique numbering across batches

### Agent Lifecycle

1. **Spawn**: Create worktree/sandbox
2. **Prepare**: Copy PRD, ensure .ralphy/ exists
3. **Execute**: Run AI engine with constructed prompt
4. **Retry**: Exponential backoff on retryable errors
5. **Commit**: Auto-commit changes (if enabled)
6. **Cleanup**: Remove worktree/sandbox
7. **Merge**: Integrate branch back to base

### Error Handling

**Retryable Errors** (`cli/src/execution/retry.ts`):
- Rate limits (429)
- Quota exceeded
- Temporary network failures

**Fatal Errors** (abort all tasks):
- Authentication failures
- Configuration errors
- Permission denied

**Deferred Tasks**:
- Tasks failing with retryable errors are deferred
- Retried up to maxRetries times
- Prevents infinite loops

---

## Task Management

### Task Interface

```typescript
interface Task {
    id: string;                    // Unique identifier
    title: string;                 // Task description
    body?: string;                 // Full details (GitHub issues)
    parallelGroup?: number;        // 0 = sequential, >0 = parallel group
    completed: boolean;            // Completion status
}
```

### Task Source Interface

```typescript
interface TaskSource {
    type: TaskSourceType;
    getAllTasks(): Promise<Task[]>;
    getNextTask(): Promise<Task | null>;
    markComplete(id: string): Promise<void>;
    countRemaining(): Promise<number>;
    getTasksInGroup?(group: number): Promise<Task[]>;
}
```

### Supported Formats

| Format | File | Parallel Groups | Best For |
|--------|------|-----------------|----------|
| Markdown | PRD.md | No | Simple projects |
| Markdown Folder | ./prd/ | No | Large multi-module projects |
| YAML | tasks.yaml | Yes | Complex orchestration |
| JSON | tasks.json | Yes | Programmatic generation |
| GitHub Issues | owner/repo | Yes | Issue-driven development |

---

## Integration with Claude Code

### Claude Engine (`cli/src/engines/claude.ts`)

**Command Construction:**
```typescript
const args = [
    "--dangerously-skip-permissions",
    "--verbose",
    "--output-format", "stream-json"
];
if (options?.modelOverride) {
    args.push("--model", options.modelOverride);
}
```

**Key Features:**
- Uses `--dangerously-skip-permissions` for non-interactive execution
- Stream JSON output for real-time progress tracking
- Model override support (`--sonnet` shortcut)
- Windows compatibility (stdin vs argument passing)

### Prompt Engineering

**Prompt Structure** (`cli/src/execution/prompt.ts`):
1. **Project Context**: From `.ralphy/config.yaml`
2. **Rules**: Code change guidelines + user-defined rules
3. **Boundaries**: Files/directories agents must not touch
4. **Agent Skills**: Auto-detected skill directories
5. **Browser Instructions**: If agent-browser available
6. **Task**: Specific implementation task
7. **Instructions**: Step-by-step workflow

**Parallel Prompt Differences:**
- Explicit "focus ONLY on this task" instruction
- Progress file update requirement
- No task completion marking (handled by orchestrator)

---

## Strengths

### 1. **Mature Parallel Execution**
- Git worktree pattern is production-tested and robust
- True file isolation prevents conflicts
- Safe merge with AI-assisted conflict resolution
- Sandbox mode for large repos

### 2. **Multi-Engine Support**
- 8 AI engines supported
- Unified interface via AIEngine abstraction
- Easy to add new engines
- Engine-specific argument passing

### 3. **Flexible Task Sources**
- Multiple input formats (Markdown, YAML, JSON, GitHub)
- Parallel group support for dependency management
- Caching for performance
- GitHub issue sync

### 4. **Robust Error Handling**
- Retry with exponential backoff
- Fatal vs retryable error distinction
- Deferred task queue
- Dirty worktree preservation for debugging

### 5. **Developer Experience**
- Project configuration via `.ralphy/config.yaml`
- Rules and boundaries system
- Webhook notifications (Discord/Slack)
- Telemetry and cost tracking
- Browser automation support

### 6. **Git Integration**
- Automatic branch creation per task
- PR creation (draft or regular)
- Merge conflict detection and resolution
- Clean worktree cleanup

---

## Weaknesses/Limitations

### 1. **Node.js/Bun Dependency**
- Requires Node.js 18+ or Bun runtime
- Not suitable for environments without Node.js
- Bash version exists but less feature-complete

### 2. **Limited Agent Communication**
- No inter-agent messaging system
- Agents work in complete isolation
- No shared context between parallel agents
- Could lead to duplicated work

### 3. **Merge Complexity**
- Automatic merging can be risky
- AI conflict resolution may not always be correct
- No human-in-the-loop for merge decisions
- Complex merge strategies not supported

### 4. **No Persistent Agent State**
- Agents are ephemeral (created per task)
- No learning from previous tasks
- No agent specialization
- Each task starts fresh

### 5. **Limited Observability**
- Basic progress tracking
- No detailed agent logs
- Limited visibility into agent decision-making
- No replay capability

### 6. **Single Repository Focus**
- Designed for single-repo workflows
- No multi-repo orchestration
- No cross-repository dependencies

### 7. **No Dynamic Task Generation**
- Tasks must be predefined
- No runtime task creation
- No adaptive planning

---

## Integration Potential for BB5

### Existing BB5 Research

BB5 already has research on Ralphy's git worktree pattern:
- **Location:** `6-roadmap/frameworks/ralphy-integration-analysis/`
- **Prototype:** Working Python implementation
- **Status:** Tested and ready for integration

### High-Value Integration Points

#### 1. **Git Worktree Parallel Execution** (HIGHEST PRIORITY)
**What to adopt:**
- Worktree creation/cleanup pattern
- Parallel batch processing
- Merge phase with conflict resolution

**BB5 Adaptation:**
```python
# BB5 RALF Runtime integration
class GitWorktreeManager:
    def create_agent_worktree(self, task, agent_num):
        # Adapt Ralphy's TypeScript logic to Python
        branch_name = f"bb5/agent-{agent_num}-{task.slug}"
        worktree_dir = f".bb5-worktrees/agent-{agent_num}"
        # Use gitpython or subprocess
```

**Benefits:**
- 3-5x speedup on parallelizable tasks
- True isolation between BB5 agents
- Safe merge back to main branch

#### 2. **Multi-Engine Support**
**What to adopt:**
- AIEngine interface pattern
- Engine factory/registration
- Engine-specific argument handling

**BB5 Adaptation:**
- Extend BB5's Claude-only approach
- Add OpenCode, Cursor, etc. support
- Allow per-task engine selection

#### 3. **Task Source Abstraction**
**What to adopt:**
- TaskSource interface
- Multiple format support
- Caching layer

**BB5 Adaptation:**
- Unify BB5's various task input methods
- Support YAML/JSON PRDs
- Add task caching for performance

#### 4. **Prompt Engineering Patterns**
**What to adopt:**
- Structured prompt construction
- Rules/boundaries system
- Skill detection

**BB5 Adaptation:**
- Enhance BB5's prompt templates
- Add `.bb5/config.yaml` for project rules
- Auto-detect skills/playbooks

#### 5. **Error Handling & Retry**
**What to adopt:**
- Retryable vs fatal error classification
- Exponential backoff
- Deferred task queue

**BB5 Adaptation:**
- Improve BB5's error recovery
- Add intelligent retry logic
- Handle rate limits gracefully

### Integration Strategy

**Phase 1: Worktree Foundation**
1. Port Ralphy's worktree manager to BB5's Python codebase
2. Add feature flag (default: off)
3. Test with single-agent scenarios

**Phase 2: Parallel Execution**
1. Implement parallel batch processing
2. Add merge phase with conflict detection
3. Test with multi-agent scenarios

**Phase 3: Enhanced Features**
1. Add sandbox mode for large repos
2. Implement AI-assisted conflict resolution
3. Add parallel group support

### Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Breaking existing BB5 workflows | Medium | Feature flags, gradual rollout |
| Merge conflicts | Medium | AI resolution, manual review option |
| Disk space (worktrees) | Low | Automatic cleanup, sandbox mode |
| Complexity increase | Medium | Modular design, clear abstractions |

---

## Recommendation

### Should BB5 Integrate Ralphy Patterns?

**YES - High Priority**

### Priority Levels

| Feature | Priority | Effort | Impact |
|---------|----------|--------|--------|
| Git worktree parallel execution | **P0** | Medium | Very High |
| Sandbox mode | **P1** | Low | High |
| Multi-engine support | **P2** | Medium | Medium |
| Task source abstraction | **P2** | Medium | Medium |
| Prompt engineering patterns | **P3** | Low | Medium |
| Error handling improvements | **P3** | Low | Medium |

### Rationale

1. **Proven Pattern**: Ralphy's worktree approach is production-tested (v4.7.2)
2. **High Impact**: 3-5x speedup on parallelizable tasks
3. **Low Risk**: BB5 already has research and prototype
4. **Competitive**: Other Ralph frameworks lack this sophistication
5. **Isolated**: Can be implemented behind feature flags

### Implementation Path

1. **Week 1-2**: Port worktree manager, add feature flag
2. **Week 3-4**: Implement parallel execution loop
3. **Week 5-6**: Add merge phase and conflict resolution
4. **Week 7-8**: Testing, documentation, gradual rollout

### Conclusion

Ralphy represents the most mature and feature-complete Ralph framework analyzed. Its git worktree parallel execution pattern is a genuine innovation that would significantly enhance BB5's capabilities. The existing BB5 research provides a solid foundation for integration. This should be a top priority for BB5's autonomous improvement roadmap.

---

## References

- **Repository**: https://github.com/michaelshimeles/ralphy
- **NPM Package**: https://www.npmjs.com/package/ralphy-cli
- **BB5 Research**: `6-roadmap/frameworks/ralphy-integration-analysis/`
- **Key Files**:
  - `cli/src/git/worktree.ts` - Worktree management
  - `cli/src/execution/parallel.ts` - Parallel execution
  - `cli/src/execution/sandbox.ts` - Sandbox mode
  - `cli/src/engines/claude.ts` - Claude Code integration
