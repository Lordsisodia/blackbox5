# Blackbox5 Claude Code Hooks Architecture

**Version**: 1.0.0
**Last Updated**: 2026-01-21
**Component**: Operations Layer (07-operations)
**Status**: Production

---

## Overview

The Claude Code Hooks System is an **operations layer component** that integrates Blackbox5 with Claude Code to create a reliable, effective, and learning AI-augmented development workflow.

### First Principles Analysis

**Problem**: AI operates without persistent context, repeats mistakes, loses insights, and can't build on past work.

**Solution**: 18 hooks across 6 event types that automatically:
1. **Track everything** (complete audit trail)
2. **Learn from every session** (organizational memory)
3. **Think more deeply** (first principles + assumption detection)
4. **Make better decisions** (impact analysis, decision capture)
5. **Stay safe** (reversibility checks, environment validation)
6. **Maintain quality** (atomic commits, completion criteria, test coverage)

---

## Architecture

### System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                         BLACKBOX5                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  01-core: Agents, Orchestration, Routing                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          ↑                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  07-operations: Runtime, Commands, Workflows               │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  HOOKS SYSTEM ← You are here                         │ │ │
│  │  │  - Event interception                                │ │ │
│  │  │  - Automated validation                              │ │ │
│  │  │  - Memory persistence                                │ │ │
│  │  │  - Quality enforcement                               │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  05-project-memory: Decisions, Knowledge, Sessions         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Hook Event Flow

```
┌──────────────────┐
│ Claude Code Event│
└────────┬─────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│  Hook Matcher (settings.json)                                │
│  - Checks event type                                        │
│  - Matches tool patterns                                    │
│  - Selects relevant hooks                                   │
└────────┬────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│  Parallel Hook Execution (all matching hooks run together)  │
│  ├─ hook1.sh (runs, timeout: 60s)                           │
│  ├─ hook2.sh (runs, timeout: 60s)                           │
│  └─ hook3.sh (runs, timeout: 60s)                           │
└────────┬────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│  Synchronization Point                                       │
│  - Claude waits for ALL hooks to complete                    │
│  - Exit code 2 from any hook = BLOCK action                  │
│  - Exit code 0 = CONTINUE                                    │
└────────┬────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────┐
│ Action Continues │
└──────────────────┘
```

---

## Hook Inventory

### 🔴 CRITICAL HOOKS (10 hooks)

| # | Hook | Event | File | Purpose |
|---|------|-------|------|---------|
| 1 | Auto-log activity | PostToolUse | `auto-log-activity.sh` | Complete audit trail |
| 2 | Extract & persist memories | SessionEnd | `extract-memories.sh` | Organizational learning |
| 3 | First principles triggering | UserPromptSubmit | `first-principles-trigger.sh` | Better thinking |
| 4 | Decision capture | PostToolUse | `capture-decisions.sh` | Decision rationale |
| 5 | Context boundary detection | PreToolUse | `check-context-boundary.sh` | Prevent overflow |
| 6 | Commit message enforcement | Git commit-msg | `.git/hooks/commit-msg` | Clean git history |
| 7 | Change impact analysis | PreToolUse | `analyze-change-impact.sh` | Understand blast radius |
| 8 | Completion criteria validation | PreToolUse | `validate-completion.sh` | Stop partial work |
| 9 | Reversibility check | PreToolUse | `check-reversibility.sh` | Safe experimentation |
| 10 | **Reflection on completion** | **Stop/SubagentStop** | `reflect-on-completion.sh` | **Next steps planning** |

### 🔵 NEXT-STEPS HOOKS (1 hook)

| # | Hook | Event | File | Purpose |
|---|------|-------|------|---------|
| 11 | **Reflection on completion** | **Stop/SubagentStop** | `reflect-on-completion.sh` | **Maintain momentum, plan next steps** |

**Status Detection**: completion | implementation | research | troubleshooting | output

### 🟡 HIGH VALUE HOOKS (9 hooks)

| # | Hook | Event | File | Purpose |
|---|------|-------|------|---------|
| 12 | Assumption detection | UserPromptSubmit | `detect-assumptions.sh` | Question assumptions |
| 11 | Task decomposition check | UserPromptSubmit | `check-task-complexity.sh` | Tractable tasks |
| 12 | Dependency detection | UserPromptSubmit | `detect-dependencies.sh` | Find blockers |
| 13 | Knowledge gap detection | UserPromptSubmit | `detect-knowledge-gaps.sh` | Identify learning needs |
| 14 | Time boxing / Session management | SessionStart | `manage-session-time.sh` | Prevent fatigue |
| 15 | Stakeholder detection | PostToolUse | `detect-stakeholders.sh` | Right communication |
| 16 | Technical debt detection | PostToolUse | `detect-technical-debt.sh` | Track debt |
| 17 | Environment validation | SessionStart | `validate-environment.sh` | Prevent accidents |
| 18 | Test coverage validation | PostToolUse | `validate-test-coverage.sh` | Maintain quality |

---

## Directory Structure

```
blackbox5/
├── .claude/
│   ├── settings.json                          # Claude Code configuration
│   ├── CLAUDE.md                              # Project context
│   ├── hooks/                                  # Hook scripts
│   │   ├── auto-log-activity.sh
│   │   ├── extract-memories.sh
│   │   ├── first-principles-trigger.sh
│   │   ├── capture-decisions.sh
│   │   ├── check-context-boundary.sh
│   │   ├── detect-assumptions.sh
│   │   ├── check-task-complexity.sh
│   │   ├── detect-dependencies.sh
│   │   ├── detect-knowledge-gaps.sh
│   │   ├── analyze-change-impact.sh
│   │   ├── check-reversibility.sh
│   │   ├── validate-completion.sh
│   │   ├── detect-technical-debt.sh
│   │   ├── detect-stakeholders.sh
│   │   ├── validate-test-coverage.sh
│   │   ├── validate-environment.sh
│   │   ├── manage-session-time.sh
│   │   ├── detect-patterns.sh
│   │   └── analyze-subagent-quality.sh
│   ├── README.md                               # Complete documentation
│   ├── install-git-hooks.sh                    # Git hooks installer
│   ├── verify-hooks.sh                         # Verification script
│   └── check-status.sh                          # Status checker
│
├── .git/hooks/
│   ├── commit-msg                              # Commit message validation
│   └── pre-commit                              # Pre-commit validation
│
└── 5-project-memory/siso-internal/
    ├── decisions/                              # Auto-populated
    ├── knowledge/                              # Auto-populated
    ├── operations/                             # Auto-populated
    │   ├── agent-quality.txt                   # Subagent quality log
    │   ├── pattern-detection.txt              # Pattern tracking
    │   └── technical-debt.txt                 # Debt tracking
    ├── sessions/                               # Session memory
    ├── WORK-LOG.md                             # Auto-generated activity log
    └── STATE.yaml                              # Single source of truth
```

---

## Event Mapping

### UserPromptSubmit (5 hooks)

Fires when user submits a prompt, before Claude processes it.

| Hook | Purpose | Output |
|------|---------|--------|
| `first-principles-trigger.sh` | Inject first principles for complex tasks | Framework added to context |
| `detect-assumptions.sh` | Question implicit assumptions | Assumptions challenged |
| `check-task-complexity.sh` | Suggest task decomposition | Breakdown suggestions |
| `detect-dependencies.sh` | Identify blockers | Dependency warnings |
| `detect-knowledge-gaps.sh` | Identify learning needs | Research suggestions |

### PreToolUse (4 hooks)

Fires after Claude creates tool parameters, before processing the tool call.

| Hook | Purpose | Action |
|------|---------|--------|
| `check-context-boundary.sh` | Prevent context overflow | Block at 95% usage |
| `analyze-change-impact.sh` | Understand blast radius | Show dependencies |
| `check-reversibility.sh` | Safe experimentation | Suggest backup branch |
| `validate-completion.sh` | Stop partial work | Check completion criteria |

### PostToolUse (4 hooks)

Fires immediately after a tool completes successfully.

| Hook | Purpose | Action |
|------|---------|--------|
| `auto-log-activity.sh` | Complete audit trail | Log to WORK-LOG.md |
| `capture-decisions.sh` | Record decision rationale | Write to decisions/ |
| `detect-technical-debt.sh` | Track debt | Log TODO/FIXME |
| `detect-stakeholders.sh` | Right communication | Suggest notifications |
| `validate-test-coverage.sh` | Maintain quality | Check test coverage |
| `analyze-subagent-quality.sh` | Quality gate | Score subagent output |

### SessionStart (2 hooks)

Fires when Claude Code starts a new session or resumes an existing session.

| Hook | Purpose | Action |
|------|---------|--------|
| `validate-environment.sh` | Prevent accidents | Check branch, env vars |
| `manage-session-time.sh` | Prevent fatigue | Track session duration |

### SessionEnd (2 hooks)

Fires when a Claude Code session ends.

| Hook | Purpose | Action |
|------|---------|--------|
| `extract-memories.sh` | Organizational learning | Write to memory folders |
| `detect-patterns.sh` | Spot systemic issues | Track frequently edited files |

### SubagentStop (1 hook)

Fires when a Claude Code subagent has finished responding.

| Hook | Purpose | Action |
|------|---------|--------|
| `analyze-subagent-quality.sh` | Quality gate | Score and flag low quality |

---

## Git Hooks

### Pre-Commit Hook

**File**: `.git/hooks/pre-commit`

**Purpose**: Validate code quality before commit

**Validates**:
- No .env files committed (security)
- Warns about large files (>1MB)
- Runs tests (optional, commented out)

**Purpose**: Prevent bad commits before they happen

### Commit-Message Hook

**File**: `.git/hooks/commit-msg`

**Purpose**: Enforce conventional commits and atomicity

**Enforces**:
- Conventional commit format: `type(scope): description`
- Blocks generic messages: "wip", "fix", "updates"
- Warns on large commits (>10 files)
- Encourages atomicity (single logical change)

**Purpose**: Clean, readable git history

---

## Configuration

### Claude Code Settings

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/first-principles-trigger.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-assumptions.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/check-task-complexity.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-dependencies.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-knowledge-gaps.sh",
          "timeout": 5
        }
      ]
    }],
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/check-context-boundary.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/analyze-change-impact.sh",
          "timeout": 10
        },
        {
          "type": "command",
          "command": ".claude/hooks/check-reversibility.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/validate-completion.sh",
          "timeout": 5
        }
      ]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/auto-log-activity.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/capture-decisions.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-technical-debt.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-stakeholders.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/validate-test-coverage.sh",
          "timeout": 10
        }
      ]
    }],
    "SessionStart": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/validate-environment.sh",
          "timeout": 5
        },
        {
          "type": "command",
          "command": ".claude/hooks/manage-session-time.sh",
          "timeout": 5
        }
      ]
    }],
    "SessionEnd": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/extract-memories.sh",
          "timeout": 30
        },
        {
          "type": "command",
          "command": ".claude/hooks/detect-patterns.sh",
          "timeout": 10
        }
      ]
    }],
    "SubagentStop": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/analyze-subagent-quality.sh",
          "timeout": 10
        }
      ]
    }]
  }
}
```

### Environment Variables

```bash
BLACKBOX5_ENGINE_PATH=./2-engine
BLACKBOX5_MEMORY_PATH=./5-project-memory/siso-internal
BLACKBOX5_CONTEXT_THRESHOLD=80  # Percentage (warn at 80%, block at 95%)
BLACKBOX5_SESSION_TIMEOUT=14400  # 4 hours in seconds
```

---

## Usage Examples

### Example 1: Simple Task (No Hooks Triggered)

```bash
> What is 2+2?

# Result: Direct answer, no hooks triggered
```

### Example 2: Complex Task (First Principles Triggered)

```bash
> Design a user authentication system

# Hook Output:
# 🧠 First Principles Analysis
# 1. Question the Question
# 2. Identify Assumptions
# 3. Break Down to Fundamentals
# 4. Build Up from First Principles

# Result: Claude thinks more deeply about the problem
```

### Example 3: Task with Assumptions

```bash
> We should obviously use JWT for auth

# Hook Output:
# 🔍 Assumption Detection
# I noticed: "obviously"
# Questions: What evidence supports this? What if it's wrong?

# Result: Assumptions questioned before proceeding
```

### Example 4: Editing File

```bash
> Edit src/auth.ts to add login function

# Hook Output (PreToolUse):
# 📊 Change Impact Analysis
# This file imports: [...]
# This file is used by: [...]
# ⚠️  Changes here may affect dependent files.

# (File edited)

# Hook Output (PostToolUse):
# (Activity logged to WORK-LOG.md)
```

### Example 5: Committing

```bash
$ git commit -m "wip"
❌ Blocked commit message: "wip"
Use conventional commit format: type(scope): description

$ git commit -m "feat(auth): add login support"
✓ Commit accepted
```

---

## Performance & Cost

### Execution Model

- **Parallel execution**: All matching hooks run simultaneously
- **Synchronization**: Claude waits for ALL hooks to complete
- **Timeout**: 60-second default (configurable per hook)
- **Blocking**: Exit code 2 blocks action; exit code 0 continues

### Cost Optimization

1. **Timeouts**: All hooks have appropriate timeouts (5-30s)
2. **Fast-fail**: Hooks exit immediately if not applicable
3. **Specific matchers**: Don't use `*` for everything
4. **Bash over LLM**: `type: "command"` (free) vs `type: "prompt"` (costs credits)

### Monitoring

```bash
# Run Claude Code with debug output
claude --debug

# Check hook execution time
# Look for: [DEBUG] Executing hooks for Event:Tool
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Activity logging coverage | 100% | All edits appear in WORK-LOG.md |
| Memory extraction rate | 90% | Sessions produce memory entries |
| Commit message quality | 100% conventional | Git log follows format |
| Context overflow failures | 0 | No "context exceeded" errors |
| Decision capture rate | 80% | Decisions recorded in decisions/ |
| Technical debt visibility | 100% | All TODO tracked |
| Hook execution time | <100ms (p95) | Fast enough to be invisible |

---

## Installation

### For Users

1. **Clone/pull this code**
2. **Start Claude Code in the project directory**
3. **Hooks run automatically**

```bash
cd blackbox5
claude
# Hooks are now active!
```

### Verification

```bash
./.claude/verify-hooks.sh    # Verify hooks are installed
./.claude/check-status.sh     # Check memory structure
```

---

## Troubleshooting

### Hook Not Running

**Symptom**: Hooks not executing

**Diagnosis**:
```bash
# Check permissions
ls -la .claude/hooks/*.sh

# Test a hook manually
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.txt"}}' | \
  .claude/hooks/auto-log-activity.sh
```

**Solution**: Ensure hooks are executable (`chmod +x`)

### Context Overflow Still Happening

**Symptom**: "context exceeded" errors despite hooks

**Diagnosis**: Heuristic-based estimation is not accurate enough

**Solution**:
- Run `/compact` more frequently
- Start fresh sessions more often
- Implement API-based context checking (future)

### Git Hooks Blocking Valid Commits

**Symptom**: Good commit blocked by hook

**Workaround**: Bypass hook temporarily
```bash
git commit --no-verify -m "message"
```

**Solution**: Fix the issue, don't bypass long-term

---

## Future Enhancements

### Short Term (Next 1-2 weeks)

1. **API-based context checking** - More accurate context usage
2. **Hook performance dashboard** - Monitor hook execution times
3. **Hook debugging mode** - Easier troubleshooting
4. **Customizable hook settings** - Per-user preferences

### Medium Term (Next 1-2 months)

1. **Hook marketplace** - Share hooks between projects
2. **Hook composition** - Combine multiple hooks into workflows
3. **Hook templates** - Common patterns as templates
4. **Hook testing framework** - Automated testing

### Long Term (Next 3-6 months)

1. **ML-based hook triggering** - Smart detection of when to run hooks
2. **Hook recommendation engine** - Suggest hooks based on workflow
3. **Cross-session learning** - Hooks learn from past sessions
4. **Hook analytics** - Track which hooks are most useful

---

## Comparison: Before vs After

### Before (Manual Process)

| Activity | Before | Effort |
|----------|--------|--------|
| Track work | Manual notes | High |
| Capture decisions | Manual ADRs | High |
| Think deeply | Remember to do it | Medium |
| Clean git history | Remember convention | Medium |
| Prevent context overflow | Remember to compact | High |
| Validate completions | Manual checklist | Medium |
| **Total Friction** | **High** | |

### After (Automated Hooks)

| Activity | After | Effort |
|----------|-------|--------|
| Track work | Automatic | None |
| Capture decisions | Automatic + validation | Low |
| Think deeply | Auto-triggered | None |
| Clean git history | Enforced | None |
| Prevent context overflow | Automatic | None |
| Validate completions | Auto-checked | None |
| **Total Friction** | **Minimal** | |

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

- **Claude Code Hooks**: https://docs.anthropic.com/claude-code/hooks
- **Conventional Commits**: https://www.conventionalcommits.org/
- **First Principles Thinking**: https://fs.blog/first-principles/
- **Atomic Commits**: https://www.freshconsulting.com/atomic-commits/

---

## Conclusion

This hooks system represents a **first-principles approach** to integrating AI into development workflows:

1. **Identify the problem**: AI lacks persistent context and learning
2. **Break down to fundamentals**: What MUST happen automatically?
3. **Build up from there**: Hooks that ensure reliability and effectiveness
4. **Iterate and refine**: 18 hooks covering all critical aspects
5. **Measure success**: Metrics that matter (quality, reliability, learning)

**Result**: A system that makes AI-augmented development **more reliable, more effective, and continuously improving**.

---

**Implementation Complete**: ✅ All 18 hooks implemented and documented
**Git Hooks Complete**: ✅ Atomic commit enforcement active
**Documentation Complete**: ✅ Comprehensive README and usage guide
**Verification Complete**: ✅ All hooks tested and validated

Ready for production use.
