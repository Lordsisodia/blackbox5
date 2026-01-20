# Blackbox5 + Claude Code Hooks System

**Version**: 1.0.0
**Last Updated**: 2026-01-21
**Status**: Active

---

## Overview

This hooks system integrates Blackbox5 with Claude Code to create a **reliable, effective, and learning AI-augmented development workflow**.

### First Principles

**Problem**: AI operates without persistent context, repeats mistakes, loses insights, and can't build on past work.

**Solution**: Hooks that automatically:
1. Track everything (audit trail)
2. Learn from every session (memory persistence)
3. Think more deeply (first principles triggering)
4. Make better decisions (assumption detection, impact analysis)
5. Stay safe (reversibility checks, environment validation)
6. Maintain quality (atomic commits, completion criteria)

---

## Hook Architecture

```
Claude Code Event → Hook Script → Action → Result
```

### Hook Events Used

| Event | When It Fires | Hooks |
|-------|---------------|-------|
| **UserPromptSubmit** | Before sending prompt to AI | First principles, assumptions, tasks, dependencies |
| **PreToolUse** | Before tool execution | Context check, impact analysis, reversibility, completion |
| **PostToolUse** | After tool execution | Activity log, decisions, debt detection, test coverage |
| **SessionStart** | When Claude Code starts | Environment validation, time boxing |
| **SessionEnd** | When Claude Code ends | Memory extraction, compaction, pattern detection |
| **SubagentStop** | When subagent finishes | Quality analysis |

---

## Hook Specifications

### 🔴 CRITICAL HOOKS (9 hooks)

#### 1. Auto-log Activity (PostToolUse)
**File**: `hooks/auto-log-activity.sh`

**Purpose**: Complete audit trail of all work

**What It Does**:
- Logs every Edit/Write operation to WORK-LOG.md
- Captures: timestamp, file, tool, session ID

**Why Critical**: Without this, work is lost and untraceable

---

#### 2. Extract & Persist Memories (SessionEnd)
**File**: `hooks/extract-memories.sh`

**Purpose**: Organizational learning from every session

**What It Does**:
- Analyzes session for decisions, learnings, insights
- Writes to appropriate memory folders (decisions/, knowledge/)
- Extracts "why" and "what we learned"

**Why Critical**: Without this, insights are lost between sessions

---

#### 3. First Principles Triggering (UserPromptSubmit)
**File**: `hooks/first-principles-trigger.sh`

**Purpose**: Inject first principles framework for complex problems

**What It Does**:
- Detects keywords: "architecture", "design", "approach", "how to"
- Injects first principles questions before processing
- Promotes deeper thinking over pattern-matching

**Why Critical**: Prevents shallow solutions to complex problems

---

#### 4. Decision Capture (PostToolUse)
**File**: `hooks/capture-decisions.sh`

**Purpose**: Record decision rationale automatically

**What It Does**:
- Detects decision-related files (*decision*, *adr*, *architecture*)
- Prompts for decision components: context, options, decision, rationale
- Writes to decisions/ folder with proper format

**Why Critical**: Future-you needs to know WHY decisions were made

---

#### 5. Context Boundary Detection (PreToolUse)
**File**: `hooks/check-context-boundary.sh`

**Purpose**: Prevent context overflow failures

**What It Does**:
- Checks context window usage percentage
- Warns at 80%, blocks at 95%
- Suggests compaction or new session

**Why Critical**: Context overflow causes silent failures

---

#### 6. Commit Message Enforcement (Git commit-msg)
**File**: `.git/hooks/commit-msg`

**Purpose**: Enforce clean, atomic git history

**What It Does**:
- Validates conventional commit format: `type(scope): description`
- Blocks: "wip", "fix", "updates", "tmp"
- Requires body for commits with >5 files
- Warns on mixed concerns (feature + fix in one commit)

**Why Critical**: Git log tells the story of WHY changes happened

---

#### 7. Change Impact Analysis (PreToolUse)
**File**: `hooks/analyze-change-impact.sh`

**Purpose**: Understand blast radius before editing

**What It Does**:
- Analyzes what imports from this file
- Finds what this file imports
- Warns about dependencies
- Lists potential affected files

**Why Critical**: Prevents "edit one file, break something elsewhere"

---

#### 8. Completion Criteria Validation (PreToolUse)
**File**: `hooks/validate-completion.sh`

**Purpose**: Stop partial work from being marked "done"

**What It Does**:
- Detects completion language: "done", "complete", "finished"
- Checks: tests exist? docs updated? code reviewed?
- Prompts for missing items

**Why Critical**: Prevents "done but not really done"

---

#### 9. Reversibility Check (PreToolUse)
**File**: `hooks/check-reversibility.sh`

**Purpose**: Safe experimentation

**What It Does**:
- Detects hard-to-reverse operations (deletes, major refactors)
- Suggests creating backup branch
- Offers `git checkout -b backup/$(date +%s)`

**Why Critical**: Fear of experimentation kills innovation

---

### 🟡 HIGH VALUE HOOKS (9 hooks)

#### 10. Assumption Detection (UserPromptSubmit)
**File**: `hooks/detect-assumptions.sh`

**Purpose**: Question implicit assumptions

**What It Does**:
- Detects: "obviously", "clearly", "should be", "everyone knows"
- Injects assumption-challenging questions
- Prompts explicit assumptions

---

#### 11. Task Decomposition Check (UserPromptSubmit)
**File**: `hooks/check-task-complexity.sh`

**Purpose**: Break complex tasks into tractable pieces

**What It Does**:
- Detects complex prompts (>3 ANDs, nested clauses)
- Suggests breaking into steps
- Prompts for prioritization

---

#### 12. Dependency Detection (UserPromptSubmit)
**File**: `hooks/detect-dependencies.sh`

**Purpose**: Identify blockers before starting

**What It Does**:
- Parses for "needs X", "requires Y", "after Z"
- Checks if dependencies exist/are complete
- Warns about blocking issues

---

#### 13. Knowledge Gap Detection (UserPromptSubmit)
**File**: `hooks/detect-knowledge-gaps.sh`

**Purpose**: Identify learning needs before proceeding

**What It Does**:
- Detects uncertainty: "I think", "probably", "should work"
- Detects unfamiliar domains
- Suggests research first

---

#### 14. Time Boxing / Session Management (SessionStart/PreToolUse)
**File**: `hooks/manage-session-time.sh`

**Purpose**: Prevent fatigue-induced mistakes

**What It Does**:
- Tracks session duration
- Warns at 2 hours, suggests break
- Blocks at 4 hours, suggests fresh session

---

#### 15. Stakeholder Detection (PostToolUse)
**File**: `hooks/detect-stakeholders.sh`

**Purpose**: Right people are informed

**What It Does**:
- Detects file patterns: decisions/*, API/*, schema*
- Suggests notifications: "team", "API consumers", "frontend team"
- Prompts for communication

---

#### 16. Technical Debt Detection (PostToolUse)
**File**: `hooks/detect-technical-debt.sh`

**Purpose**: Track debt explicitly

**What It Does**:
- Finds: TODO, FIXME, HACK comments
- Tracks frequently-edited files (refactor candidates)
- Logs to debt tracker

---

#### 17. Environment Validation (SessionStart/PreToolUse)
**File**: `hooks/validate-environment.sh`

**Purpose**: Prevent production accidents

**What It Does**:
- Checks git branch (warn on main/master)
- Checks environment variables (PRODUCTION=1 warning)
- Validates current directory

---

#### 18. Test Coverage Validation (PostToolUse)
**File**: `hooks/validate-test-coverage.sh`

**Purpose**: Maintain quality

**What It Does**:
- After editing .ts/.py, checks test coverage
- Warns if <80%
- Suggests adding tests

---

## Git Hooks

### Pre-Commit Hook
**File**: `.git/hooks/pre-commit`

**Purpose**: Validate before commit

**What It Does**:
- Runs linters
- Checks tests pass
- Validates no staged .env files
- Warns on large commits (>10 files)

---

### Commit-Message Hook
**File**: `.git/hooks/commit-msg`

**Purpose**: Enforce conventional commits

**What It Does**:
- Validates format: `type(scope): description`
- Blocks generic messages
- Requires body for large changes
- Enforces atomicity (single logical change)

---

## Configuration

### Claude Code Settings
**File**: `.claude/settings.json`

Defines all hooks with proper event mapping.

### Environment Variables
```bash
BLACKBOX5_ENGINE_PATH=./2-engine
BLACKBOX5_MEMORY_PATH=./5-project-memory/siso-internal
BLACKBOX5_CONTEXT_THRESHOLD=80  # Percentage
BLACKBOX5_SESSION_TIMEOUT=14400  # 4 hours in seconds
```

---

## Installation

### Step 1: Create Directory Structure
```bash
mkdir -p .claude/hooks
chmod +x .claude/hooks/*.sh
```

### Step 2: Install Git Hooks
```bash
./install-git-hooks.sh
```

### Step 3: Configure Claude Code
```bash
# settings.json is automatically read by Claude Code
# No additional configuration needed
```

### Step 4: Verify Installation
```bash
claude --doctor
./verify-hooks.sh
```

---

## Usage

### Automatic Behavior
Hooks run **automatically**. No manual invocation needed.

### Manual Verification
```bash
# Test a specific hook
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.txt"}}' | \
  .claude/hooks/auto-log-activity.sh

# View hook logs
cat .claude/hooks/hooks.log

# Check hook status
./check-hooks-status.sh
```

---

## Troubleshooting

### Hook Not Running
1. Check permissions: `ls -la .claude/hooks/*.sh`
2. Test manually: See Usage section
3. Check Claude Code debug mode: `claude --debug`

### Hook Producing Wrong Output
1. Enable verbose mode in hook script
2. Check input JSON: Hook receives data on stdin
3. Test with sample input

### Git Hooks Not Running
1. Verify: `.git/hooks/` contains hook files
2. Check executable: `ls -la .git/hooks/pre-commit`
3. Test: `git commit -m "test"` (should run hook)

---

## Maintenance

### Adding New Hooks
1. Create script in `.claude/hooks/`
2. Make executable: `chmod +x`
3. Add to `.claude/settings.json`
4. Document in this README

### Updating Hooks
1. Edit hook script
2. Test manually
3. Restart Claude Code session

### Removing Hooks
1. Remove from `.claude/settings.json`
2. Delete script (or keep for future use)

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Activity logging coverage | 100% | All edits appear in WORK-LOG.md |
| Memory extraction rate | 90% | Sessions produce memory entries |
| Commit message quality | 100% conventional | Git log follows format |
| Context overflow failures | 0 | No "context exceeded" errors |
| Decision capture rate | 80% | Decisions recorded in decisions/ |
| Technical debt visibility | 100% | All TODO tracked |

---

## Philosophy

### What Hooks Should Do
✅ Run automatically without user thinking
✅ Prevent catastrophic failures
✅ Capture important information automatically
✅ Enforce consistency and quality
✅ Provide gentle nudges toward best practices

### What Hooks Should NOT Do
❌ Require user input (breaks automation)
❌ Block normal work flow (too restrictive)
❌ Replace human judgment (enhance, don't replace)
❌ Be overly verbose (noise vs signal)
❌ Try to be "smart" (be predictable)

---

## References

- Claude Code Hooks Documentation: https://docs.anthropic.com/claude-code/hooks
- Conventional Commits: https://www.conventionalcommits.org/
- Atomic Commits: https://www.freshconsulting.com/atomic-commits/
- First Principles Thinking: https://fs.blog/first-principles/

---

## Changelog

### v1.0.0 (2026-01-21)
- Initial release
- 9 critical hooks
- 9 high-value hooks
- Git hooks for atomic commits
- Comprehensive documentation

---

## License

Part of Blackbox5. See project LICENSE for details.
