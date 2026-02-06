# CLAUDE.local.md Guide for BlackBox5 Users

> **Purpose:** Personalize Claude's behavior per-project without affecting global settings
> **Location:** `CLAUDE.local.md` in any project root (e.g., `~/.blackbox5/5-project-memory/blackbox5/CLAUDE.local.md`)
> **Scope:** Project-specific only — does not affect other projects

---

## What is CLAUDE.local.md?

`CLAUDE.local.md` is a **project-local configuration file** that overrides or extends the global `~/.claude/CLAUDE.md`. It allows you to:

- Customize output style for specific projects
- Set default agent types (RALF vs direct)
- Define project-specific shortcuts and aliases
- Configure workflow preferences
- Override global defaults without affecting other work

### How It Differs from CLAUDE.md

| Aspect | `~/.claude/CLAUDE.md` | `CLAUDE.local.md` |
|--------|----------------------|-------------------|
| **Scope** | Global (all projects) | Project-specific only |
| **Location** | `~/.claude/CLAUDE.md` | `[project-root]/CLAUDE.local.md` |
| **Purpose** | Universal rules, SISO patterns | Personal preferences, project quirks |
| **Overrides** | Nothing (base layer) | Global settings (when specified) |
| **Shared?** | Yes, across all sessions | No, only this project |

### Loading Order

1. Global `~/.claude/CLAUDE.md` loads first
2. Project `CLAUDE.local.md` loads second (can override)
3. Later definitions take precedence

---

## Use Cases for BlackBox5

### 1. Personal Output Style Preferences

Customize how Claude communicates with **you specifically** for BB5 work:

```markdown
## Personal Output Preferences

### Communication Style
- **Default:** Ultra-terse (follow global)
- **Exceptions:**
  - Explain reasoning for architecture decisions
  - Verbose mode for learning new concepts
  - Bullet summaries for long outputs

### Code Presentation
- Always show diff-style output for changes
- Include line numbers in file references
- Use tables for multi-item comparisons
```

### 2. Default Agent Type Preference

Set your preferred agent for BB5 tasks:

```markdown
## Agent Preferences

### Default Agent
- **Primary:** Direct Claude (for most tasks)
- **Auto-delegate to RALF when:**
  - Task queue is empty
  - Continuous iteration needed
  - Long-running background work
  - Pattern: "run this overnight"

### Agent Switching
- Don't ask before switching agents
- Just notify: "Handing off to RALF for autonomous execution"
```

### 3. Custom bb5 Command Shortcuts

Define aliases for frequently used commands:

```markdown
## bb5 Shortcuts

### My Common Commands
| Alias | Full Command | When to Use |
|-------|--------------|-------------|
| `bb5 here` | `bb5 whereami` | Quick context check |
| `bb5 next` | `bb5 task:list --status=pending --limit=5` | See next tasks |
| `bb5 current` | `bb5 task:current` | What am I working on? |
| `bb5 recent` | `bb5 runs:list --limit=10` | Recent activity |
| `bb5 done` | `bb5 task:complete --with-learnings` | Finish current task |

### Custom Flags
- Always use `--with-context` for task creation
- Default sort: priority, then created date
```

### 4. Workflow Preferences

Configure how you like to work:

```markdown
## Workflow Preferences

### Task Management
- **Auto-claim:** Yes, when task is clear and <2 hours
- **Auto-create runs:** Yes, always create run folder
- **Commit style:** Conventional commits with task ID

### Documentation
- **LEARNINGS.md:** Required for every run
- **DECISIONS.md:** For any choice with >2 options
- **THOUGHTS.md:** Stream of consciousness, don't polish

### Review Preferences
- **Self-review:** Always run validation before marking complete
- **User review:** Ask for production code, just do docs/configs
- **Skip confirmation for:** File reads, searches, status checks
```

---

## Starter Template

Copy this template to your project root as `CLAUDE.local.md`:

```markdown
---
name: [Your Name] BB5 Preferences
version: 1.0.0
project: blackbox5
created: 2026-02-06
---

# Personal Preferences for BlackBox5

This file customizes Claude's behavior for my BB5 workflow.
It extends `~/.claude/CLAUDE.md` with project-specific preferences.

---

## Output Style Overrides

### Communication
- Default: Follow global ultra-terse style
- Exceptions:
  - [Add your exceptions here]

### Code Changes
- [Your preferences for code presentation]

---

## Agent Preferences

### Default Behavior
- Primary: [Direct / RALF / Hybrid]
- Auto-switch when: [Your triggers]

### Delegation Rules
- [When to hand off to other agents]

---

## bb5 Command Shortcuts

### My Aliases
| Alias | Expands To | Notes |
|-------|------------|-------|
| [alias] | [full command] | [when to use] |

---

## Workflow Preferences

### Task Handling
- Auto-claim: [Yes/No]
- Auto-create runs: [Yes/No]
- Default commit message format: [Your format]

### Documentation Style
- LEARNINGS.md: [Required/Optional]
- DECISIONS.md: [When to create]
- ASSUMPTIONS.md: [Your preference]

### Stop Conditions
- Always ask before: [Your list]
- Just do it for: [Your list]

---

## Project-Specific Context

### My Active Goals
- [Goal 1]
- [Goal 2]

### Current Focus Areas
- [Area 1]
- [Area 2]

### Known Preferences
- [Any other context about how you like to work]

---

## Overrides from Global

### Modified Rules
| Global Rule | Local Override | Reason |
|-------------|----------------|--------|
| [Rule name] | [Your change] | [Why] |

---

*Last updated: 2026-02-06*
```

---

## Agent Integration

### When Agents Can Suggest Updates

Agents may propose `CLAUDE.local.md` updates when they detect:

1. **Recurring Patterns**
   - You consistently ask for the same formatting
   - You frequently override a default behavior
   - You always skip certain steps

2. **Friction Points**
   - You correct Claude's output style repeatedly
   - You redirect workflow multiple times
   - You override agent selection

3. **Explicit Requests**
   - "Remember that I prefer..."
   - "From now on, always..."
   - "Add this to my preferences"

### How Agents Propose Changes

Agents will:

1. **Identify the pattern** (3+ occurrences)
2. **Draft the update** showing exact changes
3. **Present for approval:**
   ```
   Detected pattern: You always ask for verbose output on architecture tasks.

   Proposed addition to CLAUDE.local.md:
   ```markdown
   ## Output Style Overrides

   ### Architecture Tasks
   - Use verbose mode for all architecture/design discussions
   - Include reasoning for each recommendation
   ```

   Apply this change? (yes/no/edit)
   ```
4. **Apply only after explicit approval**

### Safety Considerations

Agents **WILL NOT** automatically:
- Overwrite existing preferences
- Remove your customizations
- Change core workflow without asking
- Update after a single occurrence

Agents **WILL**:
- Show exact diff before applying
- Explain the detected pattern
- Allow you to modify the proposal
- Respect "no" without asking again for same pattern

---

## Example Preferences

### Example 1: Verbose Mode for Learning

```markdown
## Learning Mode

When I'm working on unfamiliar tech:
- Explain concepts before implementing
- Show 2-3 approaches with tradeoffs
- Include "why" not just "what"
- Link to relevant documentation

Trigger: I say "this is new to me" or ask "how does X work?"
```

### Example 2: Specific Commit Format

```markdown
## Commit Preferences

### Format
```
[type]([scope]): [description]

- [detail 1]
- [detail 2]

Task: [TASK-ID]
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructuring
- `test:` Tests only

### Always Include
- Task ID from current task
- Co-authored-by: Claude <claude@blackbox5.local>
```

### Example 3: Auto-Delegation Rules

```markdown
## Auto-Delegation

### Always Use RALF For
- Tasks with >10 files
- Refactoring patterns across codebase
- Generating boilerplate/code scaffolding
- Running tests across modules
- Any "find all occurrences of X" tasks

### Never Delegate
- Security-related changes
- Database migrations
- API contract changes
- Production config changes
```

### Example 4: Custom Stop Conditions

```markdown
## Modified Stop Conditions

### Additional Stop Triggers
- When estimated time >4 hours
- When touching >5 files in critical path
- When changing files I didn't author
- When task description is <10 words

### Skip Confirmation For
- Adding tests (even production code)
- Documentation improvements
- Refactoring with tests in place
- Dependency updates (patch versions)
```

### Example 5: Documentation Style

```markdown
## Documentation Preferences

### LEARNINGS.md Format
```markdown
# Learnings: [TASK-ID]

## What Worked
- [Specific technique]

## What Didn't
- [Approach and why it failed]

## Key Insight
- [The one thing to remember]

## Next Time
- [What I'd do differently]
```

### Always Document
- Performance optimizations (with benchmarks)
- Workarounds (with issue links)
- Decisions that weren't obvious
```

### Example 6: Review Preferences

```markdown
## Code Review Style

### Before Submitting
- Self-review diff
- Run relevant tests
- Check for TODOs/FIXMEs

### What to Highlight
- Non-obvious changes
- Tradeoffs made
- Areas needing scrutiny

### Skip Review For
- Typo fixes
- Comment additions
- Test-only changes
- Config updates (non-production)
```

### Example 7: Notification Preferences

```markdown
## Notifications

### Tell Me About
- Task completion (1 line summary)
- Blockers (immediate)
- Unexpected errors (with context)
- Context rollover (brief notice)

### Don't Tell Me About
- Individual file reads
- Successful tool calls
- Normal workflow steps
- Cache hits

### Progress Updates
- Every 30 minutes for long tasks
- At completion of each subtask
- When switching agents
```

### Example 8: Testing Preferences

```markdown
## Testing Approach

### Always Write Tests For
- New features
- Bug fixes (regression test)
- Public APIs
- Complex logic (>10 lines)

### Test Style
- Arrange-Act-Assert comments
- Descriptive test names
- One assertion per test (preferably)

### Skip Tests For
- Simple getters/setters
- Config files
- Type definitions
- Obvious glue code
```

### Example 9: Search Preferences

```markdown
## Search Behavior

### File Discovery
- Prefer `find` over `grep` for file lists
- Always show file count first
- Group by directory, not flat list

### Content Search
- Show 2 lines of context
- Limit to first 20 matches
- Ask before searching >50 files

### Results Format
```
[file:line] - [brief context]
[file:line] - [brief context]
```
```

### Example 10: Context Management

```markdown
## Context Preferences

### At 70% Usage
- Summarize THOUGHTS.md
- Keep DECISIONS.md and ASSUMPTIONS.md

### At 85% Usage
- Complete current subtask
- Exit with PARTIAL status
- Document next steps

### What to Preserve
- Current task objective
- Recent decisions
- Open questions
- Blockers

### What to Drop
- Old THOUGHTS.md entries
- Successful validation results
- Completed subtask details
```

---

## Best Practices

### What Belongs in CLAUDE.local.md

**DO put here:**
- Personal output style preferences
- Project-specific shortcuts
- Your workflow quirks
- Exceptions to global rules
- Temporary overrides (with dates)

**DON'T put here:**
- Universal rules (belongs in global CLAUDE.md)
- Sensitive information (passwords, keys)
- Complex logic (keep it simple)
- Requirements for other users

### What Belongs in Global CLAUDE.md

- Universal SISO patterns
- Security-critical rules
- Core workflow definitions
- Shared team conventions
- Non-negotiable requirements

### Version Control

```markdown
## Version History

### v1.1.0 (2026-02-06)
- Added: Auto-delegation rules for RALF
- Modified: Commit format to include scope

### v1.0.0 (2026-01-15)
- Initial preferences
- Output style overrides
- bb5 shortcuts
```

### Testing Your Preferences

After creating/updating `CLAUDE.local.md`:

1. **Verify loading:** Ask "Did you read CLAUDE.local.md?"
2. **Test overrides:** Request something that triggers your rule
3. **Check conflicts:** Ensure global rules still work as expected

### Maintenance

- **Review monthly:** Are preferences still accurate?
- **Clean up:** Remove temporary overrides
- **Archive:** Move old versions to `.docs/preference-history/`

---

## Quick Reference

| Task | File to Edit |
|------|--------------|
| Change how Claude talks to you | `CLAUDE.local.md` |
| Add project-specific shortcuts | `CLAUDE.local.md` |
| Modify core SISO workflow | `~/.claude/CLAUDE.md` |
| Override a global rule | `CLAUDE.local.md` (explicit override) |
| Share preferences with team | `~/.claude/CLAUDE.md` |
| Personal workflow quirks | `CLAUDE.local.md` |

---

## See Also

- Global config: `~/.claude/CLAUDE.md`
- Output style: `~/.blackbox5/1-docs/03-guides/OUTPUT_STYLE.md`
- Template: `CLAUDE.local.md.example` (in this directory)
- BB5 docs: `~/.blackbox5/1-docs/`
