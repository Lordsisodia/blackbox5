# Claude Code Hooks for Autonomous Agent Workflows in BlackBox5

**Research Date:** 2026-02-07
**Source:** Claude Code Hooks Reference Documentation
**Target:** BlackBox5 RALF Agent System with 19 Research Agents

---

## Executive Summary

Claude Code hooks provide a powerful mechanism for orchestrating autonomous agent workflows in BlackBox5. By mapping Claude's lifecycle events to BlackBox5's event system, we can achieve:

- **Agent Lifecycle Management:** Track when agents start/stop with SessionStart/Stop hooks
- **Intent Classification:** Intercept and classify user prompts before processing
- **Tool Access Control:** Block/allow tools per agent with PreToolUse hooks
- **Action Logging:** Capture all agent actions with PostToolUse hooks
- **Telemetry Integration:** Sync events to BlackBox5's event system
- **Prevent Premature Stopping:** Use Stop hooks to keep agents working

---

## 1. Hook Events for Agent Orchestration

### 1.1 SessionStart - Agent Context Loading

**When it fires:** When a session begins or resumes
**Matcher support:** `startup`, `resume`, `clear`, `compact`
**Use for BlackBox5:**
- Load agent context from BlackBox5 memory at startup
- Initialize agent state from `.autonomous/memory/`
- Set environment variables for agent operation
- Sync with BlackBox5 event system

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-5-20250929",
  "agent_type": "Explore"  // If started with --agent flag
}
```

**BlackBox5 Integration Recipe:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-agent-init.sh"
          }
        ]
      }
    ]
  }
}
```

**Hook Script Example:**
```bash
#!/bin/bash
# .claude/hooks/bb5-agent-init.sh
# Initialize agent context from BlackBox5

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // "default"')

# Load agent context from BlackBox5
BB5_CONTEXT=$(cat ~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/agent-context.yaml 2>/dev/null || echo "")

# Emit BlackBox5 event
python3 ~/.blackbox5/bin/bb5-events.py emit \
  --type agent_start \
  --agent "$AGENT_TYPE" \
  --session "$SESSION_ID" \
  --source hook

# Return context to Claude
echo "{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"$BB5_CONTEXT\"}}"
```

---

### 1.2 UserPromptSubmit - Intent Classification

**When it fires:** When user submits a prompt, before Claude processes it
**Matcher support:** None (fires on every prompt)
**Use for BlackBox5:**
- Classify intent before processing
- Route to appropriate agent
- Block unauthorized operations
- Add context based on prompt content

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

**Decision Control:**
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

**BlackBox5 Intent Classification Recipe:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Classify this user intent for BlackBox5 routing: $ARGUMENTS. Categories: research, implement, analyze, fix, docs, test. Return JSON: {\"ok\": true} to allow, or {\"ok\": false, \"reason\": \"routing to specialized agent\"} to block."
          }
        ]
      }
    ]
  }
}
```

---

### 1.3 PreToolUse - Tool Access Control

**When it fires:** Before a tool call executes
**Matcher support:** Tool name regex (`Bash`, `Edit|Write`, `mcp__.*`, etc.)
**Use for BlackBox5:**
- Block dangerous operations per agent
- Validate MCP tool usage
- Modify tool input before execution
- Enforce agent-specific permissions

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite",
    "timeout": 120000
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**Decision Control (hookSpecificOutput):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason for decision",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Context for Claude"
  }
}
```

**BlackBox5 Tool Control Recipe:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-bash-validator.sh"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-mcp-write-guard.sh"
          }
        ]
      }
    ]
  }
}
```

**Bash Validation Script:**
```bash
#!/bin/bash
# .claude/hooks/bb5-bash-validator.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // "unknown"')

# Block destructive commands for research agents
if [[ "$AGENT_TYPE" == "researcher" ]] && echo "$COMMAND" | grep -qE '(rm -rf|git push --force|docker .* rm)'; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Research agents cannot execute destructive commands"
    }
  }'
  exit 0
fi

exit 0  # Allow
```

---

### 1.4 PostToolUse - Agent Action Logging

**When it fires:** After a tool completes successfully
**Matcher support:** Tool name regex
**Use for BlackBox5:**
- Log all agent actions to BlackBox5 event system
- Track file modifications
- Capture tool usage patterns
- Update agent telemetry

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**Decision Control:**
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

**BlackBox5 Action Logging Recipe:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-log-file-change.sh",
            "async": true
          }
        ]
      },
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

---

### 1.5 Stop - Prevent Agent from Stopping

**When it fires:** When Claude finishes responding
**Matcher support:** None
**Use for BlackBox5:**
- Keep agents working until tasks complete
- Prevent premature stopping
- Implement agent persistence
- Continue working on incomplete tasks

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**Decision Control:**
```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

**BlackBox5 Auto-Continue Recipe:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Check if BlackBox5 agent should continue working. Review the conversation and check: 1) Are there incomplete tasks in the context? 2) Did the user request continuous operation? 3) Is there a RALF queue with pending tasks? Return JSON: {\"ok\": false, \"reason\": \"Continue working on pending tasks\"} to continue, or {\"ok\": true} to stop.",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Multi-Criteria Stop Hook:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working for BlackBox5. Context: $ARGUMENTS\n\nAnalyze and determine if:\n1. All user-requested tasks are complete\n2. Task queue is empty\n3. No follow-up work is needed\n4. Agent has reached a natural stopping point\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

### 1.6 SubagentStart/SubagentStop - Agent Lifecycle Tracking

**When they fire:** When subagent spawns/completes
**Matcher support:** Agent type (`Bash`, `Explore`, `Plan`, custom names)
**Use for BlackBox5:**
- Track 19 research agents
- Monitor agent hierarchy
- Collect subagent transcripts
- Implement agent telemetry

**SubagentStart Input:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

**SubagentStop Input:**
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl"
}
```

**BlackBox5 Agent Tracking Recipe:**
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-agent-start.sh"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-agent-stop.sh"
          }
        ]
      }
    ]
  }
}
```

**Agent Start Script:**
```bash
#!/bin/bash
# .claude/hooks/bb5-agent-start.sh

INPUT=$(cat)
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id')
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')

# Emit to BlackBox5 event system
cat >> ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml << EOF
- timestamp: '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
  type: agent_start
  agent_id: $AGENT_ID
  agent_type: $AGENT_TYPE
  session_id: $SESSION_ID
  source: hook
EOF

exit 0
```

---

### 1.7 Notification - Agent Status Notifications

**When it fires:** When Claude sends notifications
**Matcher support:** `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`
**Use for BlackBox5:**
- Alert on permission requests
- Handle idle timeouts
- Track authentication events

**Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

**BlackBox5 Notification Recipe:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-idle-handler.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 2. Decision Control Patterns

### 2.1 Exit Code 2 Behavior

Exit code 2 blocks actions. Behavior varies by event:

| Event | Can Block? | Exit 2 Behavior |
|-------|------------|-----------------|
| `PreToolUse` | Yes | Blocks the tool call |
| `PermissionRequest` | Yes | Denies the permission |
| `UserPromptSubmit` | Yes | Blocks prompt processing |
| `Stop` | Yes | Prevents Claude from stopping |
| `SubagentStop` | Yes | Prevents subagent from stopping |
| `PostToolUse` | No | Shows stderr to Claude |
| `PostToolUseFailure` | No | Shows stderr to Claude |
| `Notification` | No | Shows stderr to user only |
| `SubagentStart` | No | Shows stderr to user only |
| `SessionStart` | No | Shows stderr to user only |
| `SessionEnd` | No | Shows stderr to user only |
| `PreCompact` | No | Shows stderr to user only |

### 2.2 JSON Decision Format

**Universal Fields (all events):**
```json
{
  "continue": true,
  "stopReason": "Message shown when continue is false",
  "suppressOutput": false,
  "systemMessage": "Warning message shown to user"
}
```

**Top-level Decision (UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop):**
```json
{
  "decision": "block",
  "reason": "Explanation for decision"
}
```

**hookSpecificOutput with hookEventName (PreToolUse, PermissionRequest):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason",
    "updatedInput": { ... },
    "additionalContext": "..."
  }
}
```

**PermissionRequest Decision:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": { ... },
      "updatedPermissions": [ ... ],
      "message": "...",
      "interrupt": false
    }
  }
}
```

### 2.3 permissionDecision Values

| Value | Effect |
|-------|--------|
| `allow` | Bypasses permission system, auto-approves |
| `deny` | Prevents the tool call |
| `ask` | Prompts user to confirm |

---

## 3. Prompt-Based Hooks

### 3.1 Using LLM to Evaluate Hook Conditions

Prompt hooks (`type: "prompt"`) send the hook input to a Claude model for single-turn evaluation.

**Configuration:**
```json
{
  "type": "prompt",
  "prompt": "Evaluate: $ARGUMENTS. Return JSON: {\"ok\": true/false, \"reason\": \"...\"}",
  "model": "claude-haiku",  // Optional, defaults to fast model
  "timeout": 30
}
```

### 3.2 Response Schema

LLM must respond with:
```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

### 3.3 Agent-Based Hooks (Multi-Turn)

Agent hooks (`type: "agent"`) spawn a subagent with tool access.

**Configuration:**
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite and check results. $ARGUMENTS",
  "model": "claude-sonnet",
  "timeout": 60
}
```

**Same response schema:** `{ "ok": true }` or `{ "ok": false, "reason": "..." }`

### 3.4 BlackBox5 Prompt Hook Examples

**Intent Classification:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Classify user intent for BlackBox5 routing. Input: $ARGUMENTS\n\nCategories: research, implement, analyze, fix, docs, test, architect\n\nIf this requires specialized agent handling, return {\"ok\": false, \"reason\": \"routing to [category] agent\"}.\nOtherwise return {\"ok\": true}.",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Task Completion Check:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if BlackBox5 agent tasks are complete. Context: $ARGUMENTS\n\nReview:\n1. Are all success criteria met?\n2. Is there a PROMISE_COMPLETE marker?\n3. Are there pending subtasks?\n\nReturn {\"ok\": false, \"reason\": \"Continue: [specific next steps]\"} if incomplete, or {\"ok\": true} if complete.",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

---

## 4. Async Hooks

### 4.1 Background Task Execution

Async hooks run without blocking Claude. Use for:
- Running tests after file edits
- Logging to external systems
- Telemetry collection
- Long-running analysis

### 4.2 Configure an Async Hook

```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "async": true,
  "timeout": 120
}
```

### 4.3 How Async Hooks Execute

1. Hook starts in background
2. Claude continues immediately
3. When hook completes, `systemMessage` or `additionalContext` delivered on next turn

### 4.4 BlackBox5 Async Recipe: Telemetry Collection

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-async.sh",
            "async": true,
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Telemetry Script:**
```bash
#!/bin/bash
# .claude/hooks/bb5-telemetry-async.sh

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')

# Send to BlackBox5 telemetry
curl -s -X POST http://localhost:8080/telemetry \
  -H "Content-Type: application/json" \
  -d "{\"tool\": \"$TOOL_NAME\", \"session\": \"$SESSION_ID\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  2>/dev/null

exit 0
```

### 4.5 Limitations

- Only `type: "command"` supports async
- Cannot block or return decisions
- Output delivered on next conversation turn
- Each firing creates separate process (no deduplication)

---

## 5. MCP Tool Hooks

### 5.1 Matching MCP Tools

MCP tools follow pattern: `mcp__<server>__<tool>`

**Examples:**
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

### 5.2 Regex Patterns

| Pattern | Matches |
|---------|---------|
| `mcp__memory__.*` | All tools from memory server |
| `mcp__.*__write.*` | Any write tool from any server |
| `mcp__github__.*` | All GitHub operations |

### 5.3 BlackBox5 MCP Integration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__blackbox5__.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-mcp-guard.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "mcp__blackbox5__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-mcp-audit.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### 5.4 MCP Write Validation Script

```bash
#!/bin/bash
# .claude/hooks/bb5-mcp-write-guard.sh

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input')

# Validate BlackBox5 writes
if [[ "$TOOL_NAME" == *"bb5"* ]]; then
  # Check if write is to protected path
  PATH=$(echo "$TOOL_INPUT" | jq -r '.path // .file_path // empty')
  if [[ "$PATH" == *".autonomous/agents"* ]] && [[ "$PATH" != *"/communications/"* ]]; then
    jq -n '{
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Writing to protected agent directory"
      }
    }'
    exit 0
  fi
fi

exit 0
```

---

## 6. Hook Locations & Scope

### 6.1 Configuration Locations

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All projects | No (local to machine) |
| `.claude/settings.json` | Single project | Yes (commit to repo) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| Plugin `hooks/hooks.json` | When plugin enabled | Yes (bundled with plugin) |
| Skill/agent frontmatter | While component active | Yes (defined in component) |

### 6.2 BlackBox5 Recommended Structure

```
~/.blackbox5/
├── .claude/
│   ├── settings.json           # Project-wide hooks
│   ├── settings.local.json     # Local overrides
│   └── hooks/
│       ├── bb5-agent-init.sh
│       ├── bb5-agent-start.sh
│       ├── bb5-agent-stop.sh
│       ├── bb5-bash-validator.sh
│       ├── bb5-telemetry.sh
│       ├── bb5-mcp-guard.sh
│       └── bb5-stop-evaluator.sh
└── 5-project-memory/
    └── blackbox5/
        └── .autonomous/
            └── agents/
                └── communications/
                    └── events.yaml
```

### 6.3 Skill/Agent Frontmatter Hooks

Hooks can be defined in skill/agent frontmatter for scoped execution:

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

**Note:** For subagents, `Stop` hooks are automatically converted to `SubagentStop`.

---

## 7. BlackBox5 Integration

### 7.1 Mapping Claude Hooks to BlackBox5 Events

| Claude Hook | BlackBox5 Event | Purpose |
|-------------|-----------------|---------|
| `SessionStart` | `agent_start` | Agent initialization |
| `SubagentStart` | `agent_start` | Subagent spawn tracking |
| `SubagentStop` | `agent_stop` | Subagent completion |
| `Stop` | `agent_stop` | Main agent completion |
| `PostToolUse` | `tool_executed` | Action logging |
| `UserPromptSubmit` | `intent_classified` | Intent routing |
| `Notification` | `notification` | Status alerts |

### 7.2 Event Sync Architecture

```
Claude Code Session
       |
       v
   [Hook Fires]
       |
       v
[Hook Script] ----> BlackBox5 Event API
       |                    |
       v                    v
  [JSON Output]      [events.yaml]
       |                    |
       v                    v
[Claude Decision]    [RALF Queue]
```

### 7.3 Agent Telemetry with Hooks

**Complete Telemetry Hook Configuration:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-init.sh"
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-agent-start.sh",
            "async": true
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-agent-stop.sh",
            "async": true
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-tool.sh",
            "async": true
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-telemetry-session-end.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### 7.4 Unified Event Emitter Script

```bash
#!/bin/bash
# .claude/hooks/bb5-emit-event.sh
# Unified event emitter for BlackBox5

EVENT_TYPE=$1
shift

# Build YAML event
cat >> ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml << EOF
- timestamp: '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
  type: $EVENT_TYPE
  source: hook
  $@
EOF

# Also send to API if available
curl -s -X POST http://localhost:8080/events \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"$EVENT_TYPE\", \"source\": \"hook\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  2>/dev/null || true

exit 0
```

---

## 8. Complete BlackBox5 Hook Recipes

### 8.1 RALF Agent Orchestration

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/ralf-init.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "RALF Intent Classification: $ARGUMENTS. If this is a task that should be handled by a specialized agent (research, implement, analyze, fix), return {\"ok\": false, \"reason\": \"Route to appropriate agent\"}. Otherwise {\"ok\": true}."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "RALF Stop Evaluation: Check if there are pending tasks in the RALF queue. Review conversation for incomplete work. If tasks remain, return {\"ok\": false, \"reason\": \"RALF queue has pending tasks - continue working\"}. Context: $ARGUMENTS",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### 8.2 19 Research Agent Management

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/research-agent-track.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/research-agent-guard.sh"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/research-agent-complete.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### 8.3 Event System Sync

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"BlackBox5 Event System Active\"}}'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bb5-event-sync.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

---

## 9. Security Considerations

### 9.1 Best Practices

1. **Validate and sanitize inputs** - Never trust hook input blindly
2. **Always quote shell variables** - Use `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..` in file paths
4. **Use absolute paths** - Specify full paths for scripts
5. **Skip sensitive files** - Avoid `.env`, `.git/`, keys

### 9.2 Agent-Specific Guards

```bash
#!/bin/bash
# Agent-specific permission enforcement

INPUT=$(cat)
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // "unknown"')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Research agents: read-only
if [[ "$AGENT_TYPE" == "researcher" ]]; then
  if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
    jq -n '{
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Research agents are read-only"
      }
    }'
    exit 0
  fi
fi

# Executor agents: no destructive commands
if [[ "$AGENT_TYPE" == "executor" ]]; then
  COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
  if echo "$COMMAND" | grep -qE '(rm -rf|git push --force|docker .* rm|drop database)'; then
    jq -n '{
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Destructive command requires approval"
      }
    }'
    exit 0
  fi
fi

exit 0
```

---

## 10. Debugging Hooks

### 10.1 Debug Mode

Run `claude --debug` to see hook execution details:
```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

### 10.2 Verbose Mode

Toggle with `Ctrl+O` to see hook progress in transcript.

### 10.3 Hook Testing Script

```bash
#!/bin/bash
# Test hook with sample input

echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/test"}}' | ./bb5-bash-validator.sh
echo "Exit code: $?"
```

---

## Appendix: Quick Reference

### Event Matcher Quick Reference

| Event | Matcher Field | Example Values |
|-------|---------------|----------------|
| `PreToolUse` | Tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PostToolUse` | Tool name | `Bash`, `Write`, `Read` |
| `PermissionRequest` | Tool name | `Bash`, `Edit` |
| `SessionStart` | Source | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | Reason | `clear`, `logout`, `other` |
| `Notification` | Type | `permission_prompt`, `idle_prompt` |
| `SubagentStart` | Agent type | `Bash`, `Explore`, `Plan` |
| `SubagentStop` | Agent type | `Bash`, `Explore`, `Plan` |
| `PreCompact` | Trigger | `manual`, `auto` |
| `UserPromptSubmit` | None | Always fires |
| `Stop` | None | Always fires |

### Decision Control Quick Reference

| Event | Decision Method | Key Fields |
|-------|-----------------|------------|
| `PreToolUse` | `hookSpecificOutput` | `permissionDecision`, `permissionDecisionReason` |
| `PermissionRequest` | `hookSpecificOutput` | `decision.behavior` |
| `UserPromptSubmit` | Top-level | `decision`, `reason` |
| `Stop` | Top-level | `decision`, `reason` |
| `SubagentStop` | Top-level | `decision`, `reason` |
| `PostToolUse` | Top-level | `decision`, `reason` |

### Timeout Defaults

| Hook Type | Default Timeout |
|-----------|-----------------|
| Command | 600 seconds (10 min) |
| Prompt | 30 seconds |
| Agent | 60 seconds |

---

## References

- **Source Document:** `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-hooks.md`
- **BlackBox5 Events:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`
- **Claude Code Docs:** https://code.claude.com/docs/en/hooks
- **Hooks Guide:** https://code.claude.com/docs/en/hooks-guide

---

*Generated for BlackBox5 autonomous agent system research.*
