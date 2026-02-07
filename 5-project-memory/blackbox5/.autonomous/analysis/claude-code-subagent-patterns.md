# Claude Code Sub-Agent Patterns for BlackBox5

**Research Date:** 2026-02-07
**Source:** Claude Code Official Documentation
**Purpose:** Extract practical patterns for BlackBox5's autonomous agent system

---

## Executive Summary

Claude Code's sub-agent system provides a battle-tested architecture for autonomous AI operations. This document extracts actionable patterns that BlackBox5 can implement immediately for:

- Agent Discovery Service
- Intent-Based Routing
- MCP Protocol Integration
- RALF Framework Enhancement

---

## 1. Sub-Agent Configuration Patterns

### 1.1 YAML Frontmatter Schema

Every sub-agent is defined as a Markdown file with YAML frontmatter:

```yaml
---
name: agent-name                    # Required: lowercase letters, hyphens
description: When to use this agent # Required: drives auto-delegation
tools: [Read, Grep, Glob, Bash]     # Optional: allowlist (inherits all if omitted)
disallowedTools: [Write, Edit]      # Optional: denylist
model: sonnet                       # Optional: sonnet/opus/haiku/inherit
permissionMode: default             # Optional: default/acceptEdits/dontAsk/bypassPermissions/plan
skills:                             # Optional: skills to preload
  - api-conventions
  - error-handling-patterns
hooks:                              # Optional: lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
```

### 1.2 Tool Restriction Patterns

**Pattern A: Explicit Allowlist (Most Secure)**
```yaml
tools: [Read, Grep, Glob, Bash]
```

**Pattern B: Inherit with Denylist**
```yaml
disallowedTools: [Write, Edit]
```

**Pattern C: MCP Tool Restrictions**
```yaml
tools: [Bash, Read, mcp__memory__*]  # Allow specific MCP servers
```

### 1.3 Model Selection Strategy

| Model | Use Case | Cost/Speed |
|-------|----------|------------|
| `haiku` | Fast exploration, search, simple lookups | Low/Fast |
| `sonnet` | Balanced analysis, code review | Medium/Medium |
| `opus` | Complex reasoning, architecture decisions | High/Slow |
| `inherit` | Match parent conversation (default) | Variable |

**Recommendation for BlackBox5:**
- Scout agents: `haiku`
- Analyzer/Architect agents: `sonnet`
- Complex planning: `opus`

### 1.4 Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | General use |
| `acceptEdits` | Auto-accept file edits | Trusted code generation |
| `dontAsk` | Auto-deny permission prompts | Read-only agents |
| `bypassPermissions` | Skip all checks (dangerous) | CI/automation only |
| `plan` | Read-only exploration | Planning mode |

---

## 2. Built-in Agent Types

### 2.1 Agent Specifications

| Agent | Model | Tools | When Auto-Delegated |
|-------|-------|-------|---------------------|
| **Explore** | Haiku | Read-only (no Write/Edit) | Codebase search, file discovery, analysis without changes |
| **Plan** | Inherits | Read-only | Plan mode research, pre-implementation analysis |
| **General-purpose** | Inherits | All tools | Complex multi-step tasks requiring exploration + action |

### 2.2 Auto-Delegation Triggers

Claude auto-delegates based on:
1. **Task description keywords** matching agent `description` field
2. **Tool requirements** (read-only vs read-write)
3. **Complexity indicators** (multi-step vs single lookup)

**Example auto-delegation triggers:**
- "Find all files that..." -> Explore agent
- "Research the codebase for..." -> Plan agent
- "Implement and test..." -> General-purpose agent

### 2.3 Thoroughness Levels for Explore Agent

When invoking Explore, Claude specifies thoroughness:
- **quick**: Targeted lookups
- **medium**: Balanced exploration
- **very thorough**: Comprehensive analysis

**BlackBox5 Implementation:** Add `thoroughness` parameter to scout agent invocations.

---

## 3. Agent Scopes & Locations

### 3.1 Location Hierarchy

| Location | Scope | Priority | Use Case |
|----------|-------|----------|----------|
| `--agents` CLI flag | Current session | 1 (highest) | Quick testing, automation |
| `.claude/agents/` | Current project | 2 | Team-shared agents |
| `~/.claude/agents/` | All projects | 3 | Personal agents |
| Plugin `agents/` | Where plugin enabled | 4 (lowest) | Distributed agents |

### 3.2 Priority Resolution Rules

1. Higher priority wins when names conflict
2. CLI-defined agents are ephemeral (session-only)
3. Project agents should be version-controlled
4. User agents are personal and persistent

### 3.3 CLI Definition Pattern

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

---

## 4. Skills Integration

### 4.1 Skill Directory Structure

```
.claude/skills/skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── reference.md          # Optional: detailed docs
├── examples.md           # Optional: usage examples
└── scripts/
    └── helper.py         # Optional: executable scripts
```

### 4.2 Skill Frontmatter

```yaml
---
name: skill-name                    # Optional: defaults to directory name
description: When to use this skill # Recommended: for auto-invocation
argument-hint: "[filename]"         # Optional: autocomplete hint
disable-model-invocation: true      # Optional: manual only
user-invocable: false               # Optional: hide from / menu
allowed-tools: [Read, Grep]         # Optional: tool restrictions
model: sonnet                       # Optional: model override
context: fork                       # Optional: run in subagent
agent: Explore                      # Optional: which agent to use
hooks:                              # Optional: skill-scoped hooks
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

### 4.3 Skill Invocation Control

| Configuration | User Can Invoke | Claude Can Invoke | When Loaded |
|---------------|-----------------|-------------------|-------------|
| (default) | Yes | Yes | Description always in context; full skill on invoke |
| `disable-model-invocation: true` | Yes | No | Only when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill on invoke |

### 4.4 Skill-to-Subagent Patterns

**Pattern A: Skill runs in subagent (`context: fork`)**
```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

**Pattern B: Subagent preloads skill (`skills` field)**
```yaml
---
name: api-developer
description: Implement API endpoints
skills:
  - api-conventions
  - error-handling-patterns
---
Implement API endpoints following preloaded conventions...
```

### 4.5 Auto-Discovery from Nested Directories

Claude Code automatically discovers skills from nested `.claude/skills/` directories based on working directory.

**Example for monorepo:**
```
packages/
  frontend/
    .claude/skills/react-patterns/SKILL.md  # Discovered when editing frontend/
  backend/
    .claude/skills/api-patterns/SKILL.md    # Discovered when editing backend/
```

---

## 5. Hooks for Agent Lifecycle

### 5.1 Hook Event Types

| Event | When Fires | Can Block? | Matcher Support |
|-------|------------|------------|-----------------|
| `SessionStart` | Session begins/resumes | No | Yes (startup/resume/clear/compact) |
| `UserPromptSubmit` | Before processing prompt | Yes | No |
| `PreToolUse` | Before tool executes | Yes | Yes (tool name) |
| `PermissionRequest` | Permission dialog shown | Yes | Yes (tool name) |
| `PostToolUse` | After tool succeeds | No | Yes (tool name) |
| `PostToolUseFailure` | After tool fails | No | Yes (tool name) |
| `Notification` | Notification sent | No | Yes (notification type) |
| `SubagentStart` | Subagent spawned | No | Yes (agent type) |
| `SubagentStop` | Subagent finishes | Yes | Yes (agent type) |
| `Stop` | Claude finishes responding | Yes | No |
| `PreCompact` | Before context compaction | No | Yes (manual/auto) |
| `SessionEnd` | Session terminates | No | Yes (exit reason) |

### 5.2 Hook Configuration Schema

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "pattern",      // Optional: regex filter
        "hooks": [
          {
            "type": "command",      // command | prompt | agent
            "command": "./script.sh",
            "timeout": 60,
            "statusMessage": "Running validation...",
            "async": false           // command only
          }
        ]
      }
    ]
  }
}
```

### 5.3 Subagent Lifecycle Hooks

**SubagentStart Hook:**
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/setup-db-connection.sh"
          }
        ]
      }
    ]
  }
}
```

**SubagentStop Hook:**
```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/cleanup.sh"
          }
        ]
      }
    ]
  }
}
```

### 5.4 Context Injection via Hooks

**Inject context into subagent on start:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### 5.5 Decision Control Patterns

**Block destructive commands:**
```bash
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')
if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Destructive command blocked"
    }
  }'
else
  exit 0
fi
```

---

## 6. Practical Implementation Guide

### 6.1 Step-by-Step: Code Reviewer Agent

**File:** `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: [Read, Grep, Glob, Bash]
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

**Usage:**
```
Use the code-reviewer agent to review my recent changes
```

### 6.2 Step-by-Step: Exploration Agent

**File:** `.claude/agents/explorer.md`

```markdown
---
name: explorer
description: Fast codebase exploration agent. Use for finding files, understanding structure, and gathering context without making changes.
tools: [Read, Grep, Glob]
model: haiku
permissionMode: dontAsk
---

You are a fast exploration agent optimized for codebase discovery.

When invoked:
1. Use Glob to find relevant files
2. Use Grep to search for patterns
3. Read key files to understand structure
4. Return concise findings with file paths

Focus on:
- File locations and organization
- Key configuration files
- Entry points and main modules
- Test file locations

Return results as structured markdown with file paths.
```

### 6.3 Step-by-Step: Database Reader with Validation

**File:** `.claude/agents/db-reader.md`

```markdown
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: [Bash]
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access.

When asked to analyze data:
1. Identify which tables contain relevant data
2. Write efficient SELECT queries with filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, explain you only have read access.
```

**Validation script:** `scripts/validate-readonly-query.sh`
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

### 6.4 Best Practices for Agent Descriptions

**Good descriptions (enable auto-delegation):**
- "Expert code reviewer. Use proactively after code changes."
- "Debugging specialist for errors and test failures. Use proactively when encountering issues."
- "Data analysis expert for SQL queries. Use proactively for data analysis tasks."

**Key patterns:**
1. Include domain expertise ("expert", "specialist")
2. Specify when to use ("after code changes", "when encountering issues")
3. Use "proactively" to encourage auto-delegation
4. Be specific about the task domain

---

## 7. Patterns for BlackBox5 Implementation

### 7.1 Agent Discovery Service

Based on Claude Code's pattern:

```yaml
# BlackBox5 Agent Registry Schema
agent:
  id: scout-codebase
  name: Scout
  description: Fast read-only codebase explorer. Use proactively for discovery tasks.

  # Capability-based routing
  capabilities:
    - read-only
    - search
    - analysis

  # Tool restrictions
  allowed_tools:
    - Read
    - Grep
    - Glob

  # Model selection
  model: haiku

  # Lifecycle hooks
  hooks:
    on_start: inject_context
    on_stop: summarize_output

  # Scope
  scope: project  # user | project | session | plugin
```

### 7.2 Intent-Based Routing

```python
# Routing logic based on Claude Code's auto-delegation
class IntentRouter:
    def route(self, task_description: str, required_tools: list) -> Agent:
        # 1. Check for explicit agent request
        if explicit_agent := self.parse_explicit_request(task_description):
            return self.get_agent(explicit_agent)

        # 2. Match by description keywords
        for agent in self.registry:
            if agent.matches_description(task_description):
                return agent

        # 3. Match by tool requirements
        if set(required_tools).issubset(READ_ONLY_TOOLS):
            return self.get_agent("scout")

        # 4. Default to general-purpose
        return self.get_agent("executor")
```

### 7.3 MCP Protocol Integration

```yaml
# MCP tool mapping for agents
mcp_tools:
  memory:
    - create_entities
    - search_nodes
  filesystem:
    - read_file
    - write_file
  github:
    - search_repositories

# Agent MCP access
agent:
  name: github-scout
  allowed_mcp:
    - github
    - memory
```

### 7.4 RALF Integration Patterns

**Phase 1: Scout (Explore pattern)**
```yaml
phase: scout
agent: scout-codebase
model: haiku
tools: [Read, Grep, Glob]
thoroughness: medium  # quick | medium | very_thorough
```

**Phase 2: Analyze (Plan pattern)**
```yaml
phase: analyze
agent: analyzer
model: sonnet
tools: [Read, Grep, Glob, Bash]
context_injection: |
  Scout findings: {{scout.output}}
```

**Phase 3: Execute (General-purpose pattern)**
```yaml
phase: execute
agent: executor
model: sonnet
tools: [Read, Edit, Write, Bash, Grep, Glob]
permission_mode: acceptEdits
```

---

## 8. Key Takeaways for BlackBox5

### 8.1 Immediate Implementation Priorities

1. **Agent YAML Schema**: Implement frontmatter-based agent definitions
2. **Tool Restrictions**: Add allowlist/denylist capability
3. **Model Selection**: Support per-agent model configuration
4. **Auto-Discovery**: Scan `.blackbox5/agents/` directories
5. **Lifecycle Hooks**: Implement SubagentStart/SubagentStop events

### 8.2 Design Decisions to Mirror

| Claude Code Pattern | BlackBox5 Implementation |
|---------------------|--------------------------|
| Markdown + YAML frontmatter | YAML agent definitions |
| `description` drives auto-delegation | Intent matching system |
| `tools` allowlist | Capability-based permissions |
| `model` field | Per-agent LLM configuration |
| `skills` preloading | Knowledge injection |
| `hooks` lifecycle | Event-driven agent management |
| Scope hierarchy (CLI > Project > User > Plugin) | Agent override system |

### 8.3 Security Best Practices

1. **Default to read-only** for exploration agents
2. **Explicit tool allowlists** for sensitive operations
3. **PreToolUse hooks** for command validation
4. **Permission modes** for different trust levels
5. **No `bypassPermissions`** in production

---

## 9. References

**Source Files:**
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-sub-agents.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-skills.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-hooks.md`

**Related BlackBox5 Context:**
- 10 active agents in registry
- RALF (Recursive Autonomous Loop Framework)
- Multi-agent-ralph-loop reference (40+ agents)
- Planned: Agent Discovery Service, Intent-Based Routing, MCP Protocol Integration
