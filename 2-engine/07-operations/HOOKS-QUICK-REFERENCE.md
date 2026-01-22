# Claude Code Hooks Quick Reference

**Location**: `.claude/hooks/`
**Documentation**: [`HOOKS-ARCHITECTURE.md`](./HOOKS-ARCHITECTURE.md)
**Status**: Production Ready

---

## At a Glance

| Event | Hooks | Purpose |
|-------|-------|---------|
| **UserPromptSubmit** | 5 hooks | Enhance thinking before AI processes |
| **PreToolUse** | 4 hooks | Validate before tool execution |
| **PostToolUse** | 6 hooks | Track and learn after actions |
| **SessionStart** | 2 hooks | Set up safe environment |
| **SessionEnd** | 2 hooks | Extract learnings |
| **SubagentStop** | 1 hook | Quality gate |
| **Git Hooks** | 2 hooks | Clean git history |

---

## Critical Hooks (Must Have)

| # | Hook | When | What |
|---|------|------|------|
| 1 | `auto-log-activity.sh` | After edit | Log all work |
| 2 | `extract-memories.sh` | Session end | Save learnings |
| 3 | `first-principles-trigger.sh` | Complex task | Deep thinking |
| 4 | `capture-decisions.sh` | Decision file | Record rationale |
| 5 | `check-context-boundary.sh` | Before tool | Prevent overflow |
| 6 | `analyze-change-impact.sh` | Before edit | Show dependencies |
| 7 | `validate-completion.sh` | "done" mentioned | Check completeness |
| 8 | `check-reversibility.sh` | Risky change | Suggest backup |
| 9 | `commit-msg` (git) | Git commit | Enforce format |

---

## File Locations

```
.claude/
├── settings.json              # Hook configuration
├── hooks/
│   ├── auto-log-activity.sh
│   ├── extract-memories.sh
│   ├── first-principles-trigger.sh
│   ├── capture-decisions.sh
│   ├── check-context-boundary.sh
│   ├── detect-assumptions.sh
│   ├── check-task-complexity.sh
│   ├── detect-dependencies.sh
│   ├── detect-knowledge-gaps.sh
│   ├── analyze-change-impact.sh
│   ├── check-reversibility.sh
│   ├── validate-completion.sh
│   ├── detect-technical-debt.sh
│   ├── detect-stakeholders.sh
│   ├── validate-test-coverage.sh
│   ├── validate-environment.sh
│   ├── manage-session-time.sh
│   ├── detect-patterns.sh
│   └── analyze-subagent-quality.sh
├── verify-hooks.sh
└── check-status.sh

.git/hooks/
├── commit-msg
└── pre-commit
```

---

## Common Tasks

### Add a New Hook

1. Create script: `.claude/hooks/my-hook.sh`
2. Make executable: `chmod +x`
3. Add to `.claude/settings.json`
4. Document in `HOOKS-ARCHITECTURE.md`

### Test a Hook Manually

```bash
# PreToolUse / PostToolUse hooks
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.txt"}}' | \
  .claude/hooks/auto-log-activity.sh

# UserPromptSubmit hooks
echo '{"prompt":"test"}' | \
  .claude/hooks/first-principles-trigger.sh
```

### Disable a Hook Temporarily

Remove from `.claude/settings.json` (keep script for future use)

### Debug Hook Issues

```bash
# Run Claude Code with debug output
claude --debug

# Check hook permissions
ls -la .claude/hooks/*.sh

# View hook execution
# Look for: [DEBUG] Executing hooks for Event:Tool
```

---

## Environment Variables

```bash
BLACKBOX5_ENGINE_PATH=./2-engine
BLACKBOX5_MEMORY_PATH=./5-project-memory/siso-internal
BLACKBOX5_CONTEXT_THRESHOLD=80  # Warn at 80%, block at 95%
BLACKBOX5_SESSION_TIMEOUT=14400  # 4 hours
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Hook not running | `chmod +x .claude/hooks/*.sh` |
| Context overflow | Run `/compact`, start new session |
| Git hook blocks | `git commit --no-verify` (temporary) |

---

## Performance

| Metric | Target |
|--------|--------|
| Hook execution | <100ms (p95) |
| Activity logging | 100% coverage |
| Memory extraction | 90% of sessions |
| Commit quality | 100% conventional |

---

## Full Documentation

See [`HOOKS-ARCHITECTURE.md`](./HOOKS-ARCHITECTURE.md) for:
- Detailed hook specifications
- Event flow diagrams
- Configuration examples
- Usage examples
- Success metrics
- Future enhancements
