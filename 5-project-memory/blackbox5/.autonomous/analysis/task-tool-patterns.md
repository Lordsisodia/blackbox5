# Claude Code Task Tool: Deep Dive & RALF Integration Patterns

**Research Date:** 2026-02-07
**Source:** Claude Code Documentation (code.claude.com/docs)
**Purpose:** Technical reference for BlackBox5's autonomous agent system

---

## 1. Task Tool Schema & Parameters

### 1.1 Full Task Tool Definition

The `Task` tool spawns specialized sub-agents to handle complex, multi-step operations. It is the primary mechanism for parallel execution and context isolation in Claude Code.

```typescript
interface TaskTool {
  name: "Task";
  parameters: {
    // Required
    prompt: string;           // The task description for the sub-agent

    // Optional
    description?: string;     // Short description shown in UI
    subagent_type?: string;   // Built-in or custom agent type
    model?: string;           // Model alias: "sonnet", "opus", "haiku", "inherit"
    run_in_background?: boolean;  // Run concurrently (default: false)
    max_turns?: number;       // Limit agentic turns (print mode only)
  };
}
```

### 1.2 Parameter Deep Dive

#### `subagent_type` Options

| Type | Description | Tools | Model |
|------|-------------|-------|-------|
| `"Explore"` | Fast read-only agent for codebase search | Read, Grep, Glob, Bash | Haiku (fast, low-latency) |
| `"Plan"` | Research agent for plan mode | Read-only | Inherits from main |
| `"general-purpose"` | Complex multi-step tasks | All tools | Inherits from main |
| `"Bash"` | Terminal command execution | Bash | Inherits from main |
| `"Claude Code Guide"` | Claude Code feature questions | - | Haiku |
| `"statusline-setup"` | Status line configuration | - | Sonnet |
| Custom | User-defined agents from `.claude/agents/` | Configurable | Configurable |

**Key Insight:** The `subagent_type` determines the agent's capabilities, not just its prompt. Built-in agents have hardcoded tool restrictions.

#### `model` Parameter

- `"sonnet"` - Balanced capability and speed (default for most tasks)
- `"opus"` - Maximum capability for complex reasoning
- `"haiku"` - Fastest, lowest latency for simple tasks
- `"inherit"` - Use the same model as the main conversation (default if omitted)

**Cost Control Pattern:** Route simple exploration to Haiku, complex analysis to Opus:
```python
# Cost-optimized agent selection
if task_complexity == "simple_search":
    model = "haiku"
elif task_complexity == "complex_analysis":
    model = "opus"
else:
    model = "sonnet"
```

#### `run_in_background` Pattern

When `true`:
- Sub-agent runs concurrently with main conversation
- Main conversation continues immediately
- Results retrieved later via `TaskOutput` tool
- Permission prompts are pre-approved upfront
- MCP tools are NOT available in background agents
- If background agent fails due to missing permissions, can be resumed in foreground

**Use Case:** Parallel research across multiple code modules.

#### `max_turns` for Iteration Limits

- Only works in print mode (`claude -p`)
- Exits with error when limit is reached
- Prevents runaway agents in automated workflows
- Example: `--max-turns 3` limits to 3 agentic turns

### 1.3 TaskOutput Tool

Retrieves results from background tasks:

```typescript
interface TaskOutputTool {
  name: "TaskOutput";
  parameters: {
    // The task ID returned from the original Task call
    task_id: string;
  };
}
```

**Important:** Background tasks must be pre-approved for permissions. If a background task needs to ask clarifying questions, that tool call fails but the agent continues.

---

## 2. Parallel Execution Patterns

### 2.1 Launching Multiple Sub-Agents in Parallel

Claude Code supports parallel Task calls in a single response. This is the key pattern for RALF's multi-agent research capabilities.

**Pattern: Batch Parallel Research**
```python
# Research authentication, database, and API modules in parallel
research_tasks = [
    Task(prompt="Research the authentication module. Find all auth-related files,
                 understand the auth flow, and summarize key components.",
         description="Auth module research",
         subagent_type="Explore"),
    Task(prompt="Research the database module. Find all DB-related files,
                 understand the schema and query patterns.",
         description="Database module research",
         subagent_type="Explore"),
    Task(prompt="Research the API module. Find all API endpoint definitions,
                 understand the routing and handlers.",
         description="API module research",
         subagent_type="Explore")
]
```

**Key Points:**
- Each Task call returns a unique agent ID
- Agents execute simultaneously
- Main conversation receives all results when agents complete
- Context usage scales with number of agents and result detail

### 2.2 Message Batching Syntax

When using the Claude Code SDK or programmatic interface, parallel Task calls are made by including multiple tool calls in a single message:

```json
{
  "message": {
    "role": "assistant",
    "content": "Launching parallel research agents...",
    "tool_calls": [
      {
        "id": "task_001",
        "type": "function",
        "function": {
          "name": "Task",
          "arguments": {
            "prompt": "Research auth module...",
            "subagent_type": "Explore"
          }
        }
      },
      {
        "id": "task_002",
        "type": "function",
        "function": {
          "name": "Task",
          "arguments": {
            "prompt": "Research DB module...",
            "subagent_type": "Explore"
          }
        }
      }
    ]
  }
}
```

### 2.3 Collecting Results with TaskOutput

For background tasks, results are retrieved asynchronously:

```python
# Launch background tasks
auth_task = Task(
    prompt="Research auth module...",
    run_in_background=True
)
db_task = Task(
    prompt="Research DB module...",
    run_in_background=True
)

# Continue with other work...

# Later, retrieve results
auth_results = TaskOutput(task_id=auth_task.id)
db_results = TaskOutput(task_id=db_task.id)
```

### 2.4 Managing Concurrent Agent Execution

**Best Practices:**
1. **Limit parallel agents** - Each consumes context window. Too many = context overflow
2. **Summarize before returning** - Agents should return synthesized insights, not raw data
3. **Chain when dependent** - Use sequential execution for dependent tasks
4. **Use background for long tasks** - Keep main conversation responsive

**RALF-Specific Pattern: The 6-Agent Pipeline**
```bash
# From ralf-six-agent-pipeline.sh
agents=("scout" "architect" "developer" "reviewer" "tester" "documenter")

for agent in "${agents[@]}"; do
    Task(
        prompt="Execute $agent role for task $TASK_ID",
        subagent_type="general-purpose",
        run_in_background=true
    )
done
```

---

## 3. Dynamic Agent Creation

### 3.1 `--agents` CLI Flag JSON Format

Custom agents can be defined at runtime without creating files:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

### 3.2 JSON Schema for Dynamic Agents

```typescript
interface DynamicAgentDefinition {
  [agentName: string]: {
    description: string;      // When to invoke this agent (required)
    prompt: string;          // System prompt (required)
    tools?: string[];        // Allowed tools (optional, inherits all if omitted)
    model?: string;          // "sonnet", "opus", "haiku", or "inherit"
  }
}
```

### 3.3 Runtime Agent Definition Patterns

**Pattern 1: Session-Only Agents**
```bash
# Define agents for current session only
claude --agents '{...}' -- "Execute the code-reviewer agent on src/"
```

**Pattern 2: Project-Level Agents**
```bash
# Save to .claude/agents/ for team sharing
# File: .claude/agents/security-auditor.md
---
name: security-auditor
description: Security-focused code reviewer
tools: Read, Grep, Glob
model: sonnet
---
You are a security auditor. Focus on identifying vulnerabilities...
```

**Pattern 3: User-Level Agents**
```bash
# Save to ~/.claude/agents/ for personal use across projects
# File: ~/.claude/agents/my-custom-agent.md
```

### 3.4 Agent Priority/Precedence

When multiple agents share the same name:

1. **CLI `--agents` flag** (highest priority)
2. **`.claude/agents/`** (project-level)
3. **`~/.claude/agents/`** (user-level)
4. **Plugin `agents/`** (lowest priority)

---

## 4. Context Passing Strategies

### 4.1 Passing Large Context to Sub-Agents

**Strategy 1: File References**
```python
# Pass file paths, not content
Task(prompt=f"""
Read and analyze these files:
- {project_dir}/src/auth.js
- {project_dir}/src/db.js

Provide a summary of the authentication and database integration.
""")
```

**Strategy 2: Summarized Context**
```python
# Summarize before passing
context_summary = summarize_large_context(full_context)

Task(prompt=f"""
Context: {context_summary}

Task: Implement the feature based on the above context.
""")
```

**Strategy 3: Context Chunks**
```python
# Break large context into focused chunks
for chunk in context_chunks:
    Task(prompt=f"""
Context chunk: {chunk}

Analyze this portion and return key findings.
""")
```

### 4.2 Context Summarization Before Handoff

**Pre-Handoff Checklist:**
1. Remove irrelevant conversation history
2. Extract key decisions and assumptions
3. Summarize findings in structured format
4. Include file paths for reference
5. State current task state clearly

**Example Summarization:**
```markdown
## Context Summary for Sub-Agent

### Task
Implement user authentication for the API

### Key Findings
- Auth middleware exists in `src/middleware/auth.js`
- JWT library already installed
- Database schema supports user roles

### Relevant Files
- `src/middleware/auth.js` - Existing auth logic
- `src/routes/users.js` - User routes
- `src/models/user.js` - User model

### Decisions Made
- Use JWT for token generation
- Store tokens in HTTP-only cookies

### Current State
Ready to implement login endpoint
```

### 4.3 File Paths vs Inline Content

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| File paths | Large files, multiple files | Low token usage, always current | Agent must read files |
| Inline content | Small snippets, specific lines | Immediate context, no file reads | Token-heavy, may become stale |
| Summaries | Complex analysis results | Balanced context | Requires summarization step |

**RALF Recommendation:** Use file paths for >100 lines of code. Use inline for specific snippets <20 lines.

---

## 5. RALF Integration Patterns

### 5.1 How RALF Can Use Task Tool for Agent Spawning

**Current RALF Architecture:**
- RALF operates as a single agent loop
- Uses shell scripts for orchestration
- Has 19 planned research agents to deploy

**Proposed Integration:**
```python
# RALF Task Router
class RALFTaskRouter:
    def route_task(self, task):
        """Route task to appropriate agent(s)"""

        # Determine complexity
        if task.file_count > 15:
            return self.spawn_exploration_agents(task)
        elif task.cross_project:
            return self.spawn_cross_project_agents(task)
        elif task.complexity == "high":
            return self.spawn_specialized_agent(task)
        else:
            return self.execute_directly(task)

    def spawn_exploration_agents(self, task):
        """Spawn parallel exploration agents"""
        return [
            Task(
                prompt=f"Explore {area} for task: {task.description}",
                subagent_type="Explore",
                model="haiku"  # Fast for exploration
            )
            for area in task.areas
        ]
```

### 5.2 Queue-Based Agent Dispatch Patterns

**Pattern: Event-Driven Agent Dispatch**
```yaml
# RALF Event Queue Structure
event_queue:
  - event: task_created
    handlers:
      - agent: scout
        priority: high
      - agent: architect
        condition: complexity > threshold

  - event: code_changed
    handlers:
      - agent: reviewer
        trigger: post_commit
      - agent: tester
        trigger: post_commit
```

**Implementation:**
```python
# Event correlation across sub-agents
class AgentEventBus:
    def __init__(self):
        self.agents = {}
        self.results = {}

    def dispatch(self, event, agent_configs):
        """Dispatch event to multiple agents in parallel"""
        tasks = []
        for config in agent_configs:
            task = Task(
                prompt=config.prompt_template.format(event=event),
                subagent_type=config.agent_type,
                run_in_background=config.async_execution
            )
            tasks.append((config.name, task))

        return tasks

    def collect_results(self, task_ids):
        """Collect and correlate results from multiple agents"""
        results = {}
        for name, task_id in task_ids:
            results[name] = TaskOutput(task_id=task_id)
        return results
```

### 5.3 Event Correlation Across Sub-Agents

**Pattern: Multi-Agent Research with Synthesis**
```python
# Step 1: Launch parallel research agents
research_agents = [
    ("auth", Task(prompt="Research auth system...", subagent_type="Explore")),
    ("db", Task(prompt="Research database layer...", subagent_type="Explore")),
    ("api", Task(prompt="Research API layer...", subagent_type="Explore"))
]

# Step 2: Collect results
research_results = {
    name: TaskOutput(task_id=task.id)
    for name, task in research_agents
}

# Step 3: Synthesize with dedicated agent
synthesis = Task(
    prompt=f"""
Synthesize findings from multiple research agents:

Auth Research: {research_results['auth']}
DB Research: {research_results['db']}
API Research: {research_results['api']}

Provide integrated architecture recommendations.
""",
    subagent_type="general-purpose",
    model="opus"  # Use strongest model for synthesis
)
```

---

## 6. Decision Framework

### 6.1 When to Use Task vs Direct Execution

**Use Task (Sub-Agent) When:**
- [ ] Searching across >15 files (BlackBox5 rule)
- [ ] Complex pattern matching (regex, multiline)
- [ ] Cross-project exploration (>2 projects)
- [ ] Estimated search time >5 minutes
- [ ] Open-ended codebase exploration
- [ ] Validation of complex work
- [ ] Verbose output that would pollute main context
- [ ] Need tool restrictions or specific permissions
- [ ] Work is self-contained with clear summary output

**Use Direct Execution When:**
- [ ] <15 files needed
- [ ] Files at known paths
- [ ] Simple pattern matching (single grep)
- [ ] Known directory structure
- [ ] Implementation work (do it yourself)
- [ ] Task needs frequent back-and-forth iteration
- [ ] Latency matters (sub-agents need startup time)

### 6.2 File Count Thresholds

| File Count | Action | Rationale |
|------------|--------|-----------|
| 1-5 | Direct execution | Minimal context usage |
| 6-15 | Direct with careful reading | Still manageable |
| 16-50 | Spawn Explore agent | BlackBox5 rule threshold |
| 50-200 | Parallel Explore agents | Divide and conquer |
| 200+ | Hierarchical exploration | Multi-level search |

### 6.3 Complexity Classification for Routing

**Simple (Direct Execution):**
- Single file edits
- Known file locations
- Clear requirements
- Standard patterns

**Medium (Single Sub-Agent):**
- Multi-file changes (<10 files)
- Some exploration needed
- Well-defined scope

**Complex (Multiple Sub-Agents):**
- Architecture decisions
- Cross-module changes
- Unclear requirements
- Novel problems

**Very Complex (Superintelligence Protocol):**
- System-wide changes
- Multiple stakeholder impacts
- High uncertainty
- Strategic decisions

---

## 7. Code Examples

### 7.1 Parallel Research Pattern

```python
# Parallel module research
def parallel_module_research(modules: list[str]) -> dict:
    """Research multiple modules in parallel"""
    tasks = {}

    # Launch all research agents
    for module in modules:
        tasks[module] = Task(
            prompt=f"""
Research the {module} module thoroughly:
1. Find all relevant files
2. Understand the architecture
3. Identify key components and their relationships
4. Note any integration points with other modules

Return a structured summary with file paths and key findings.
""",
            description=f"Research {module} module",
            subagent_type="Explore",
            model="haiku"  # Fast for exploration
        )

    # Collect results (agents run in parallel)
    results = {}
    for module, task in tasks.items():
        results[module] = task.result  # Auto-collects when done

    return results
```

### 7.2 Background Task with Polling

```python
# Background execution with result polling
def background_analysis(file_path: str) -> str:
    """Run analysis in background and retrieve results"""

    # Launch background task
    task = Task(
        prompt=f"Analyze {file_path} for security vulnerabilities",
        description="Security analysis",
        run_in_background=True
    )

    # Continue with other work...
    do_other_work()

    # Poll for results
    import time
    max_wait = 300  # 5 minutes
    waited = 0

    while waited < max_wait:
        try:
            result = TaskOutput(task_id=task.id)
            return result
        except TaskNotComplete:
            time.sleep(5)
            waited += 5

    raise TimeoutError("Background task timed out")
```

### 7.3 Dynamic Agent Creation

```python
# Create specialized agents on-the-fly
def create_specialized_agent(agent_type: str, domain: str):
    """Dynamically create domain-specific agents"""

    agent_definitions = {
        "security": {
            "description": f"Security specialist for {domain}",
            "prompt": f"You are a security expert specializing in {domain}...",
            "tools": ["Read", "Grep", "Bash"],
            "model": "sonnet"
        },
        "performance": {
            "description": f"Performance optimizer for {domain}",
            "prompt": f"You are a performance engineer specializing in {domain}...",
            "tools": ["Read", "Bash"],
            "model": "sonnet"
        }
    }

    return agent_definitions.get(agent_type)
```

### 7.4 RALF Integration Example

```python
# RALF multi-agent orchestration
class RALFMultiAgent:
    def execute_research_task(self, task: ResearchTask):
        """Execute research using multiple specialized agents"""

        # Phase 1: Parallel exploration
        scout_agents = [
            Task(
                prompt=f"Explore {area} for: {task.query}",
                subagent_type="Explore",
                model="haiku"
            )
            for area in task.areas
        ]

        # Phase 2: Deep analysis (depends on exploration)
        exploration_results = [agent.result for agent in scout_agents]

        analyst_agents = [
            Task(
                prompt=f"""
Analyze findings for {area}:
{exploration_results[i]}

Provide detailed technical analysis.
""",
                subagent_type="general-purpose",
                model="sonnet"
            )
            for i, area in enumerate(task.areas)
        ]

        # Phase 3: Synthesis
        analysis_results = [agent.result for agent in analyst_agents]

        synthesis = Task(
            prompt=f"""
Synthesize all research into coherent recommendations:

{chr(10).join(analysis_results)}

Provide final recommendations with confidence scores.
""",
            subagent_type="general-purpose",
            model="opus"
        )

        return synthesis.result
```

---

## 8. Best Practices & Anti-Patterns

### 8.1 Best Practices

1. **Always summarize sub-agent outputs** - Don't return raw file listings
2. **Use appropriate models** - Haiku for search, Opus for complex analysis
3. **Limit parallel agents** - Context window is finite
4. **Chain dependent tasks** - Don't parallelize what must be sequential
5. **Use background for long tasks** - Keep main conversation responsive
6. **Pre-approve permissions for background** - Background agents can't ask
7. **Resume failed agents** - Use agent IDs to continue work

### 8.2 Anti-Patterns

1. **Nesting sub-agents** - Sub-agents cannot spawn other sub-agents
2. **Returning too much data** - Summarize, don't dump
3. **Parallelizing dependent tasks** - Creates race conditions
4. **Using background for interactive tasks** - Background can't ask questions
5. **Ignoring context limits** - Each agent consumes tokens
6. **Not handling failures** - Background tasks can fail silently

---

## 9. Integration with BlackBox5 Systems

### 9.1 Agent Discovery Service

The Task tool's `subagent_type` parameter maps to BlackBox5's Agent Discovery Service:

```yaml
# BlackBox5 Agent Registry
agents:
  built_in:
    - Explore
    - Plan
    - general-purpose

  custom:
    - code-reviewer
    - security-auditor
    - performance-analyzer

  ralf_specialized:
    - scout
    - architect
    - developer
    - reviewer
    - tester
    - documenter
```

### 9.2 Intent-Based Routing

```python
# Intent-based agent selection
INTENT_AGENT_MAP = {
    "search": "Explore",
    "analyze": "general-purpose",
    "review": "code-reviewer",
    "plan": "Plan",
    "implement": "general-purpose",
    "test": "test-runner",
    "document": "documenter"
}

def route_by_intent(intent: str, task: dict) -> Task:
    """Route task to appropriate agent based on intent"""
    agent_type = INTENT_AGENT_MAP.get(intent, "general-purpose")

    return Task(
        prompt=task["description"],
        subagent_type=agent_type,
        model=select_model_by_complexity(task["complexity"])
    )
```

### 9.3 19 Planned Research Agents

Based on BlackBox5's roadmap, the following research agents should be implemented:

| # | Agent | Purpose | Tools | Model |
|---|-------|---------|-------|-------|
| 1 | scout | Initial exploration | Read, Grep, Glob | Haiku |
| 2 | architect | System design | All | Opus |
| 3 | developer | Implementation | All | Sonnet |
| 4 | reviewer | Code review | Read, Grep | Sonnet |
| 5 | tester | Test generation | All | Sonnet |
| 6 | documenter | Documentation | Read, Write | Sonnet |
| 7 | security | Security audit | Read, Grep, Bash | Opus |
| 8 | performance | Optimization | Read, Bash | Sonnet |
| 9 | researcher | Deep research | Read, WebSearch | Opus |
| 10 | analyst | Data analysis | Read, Bash | Sonnet |
| 11 | debugger | Bug fixing | All | Sonnet |
| 12 | migrator | Migration tasks | All | Sonnet |
| 13 | validator | Validation | Read, Bash | Sonnet |
| 14 | optimizer | Refactoring | All | Sonnet |
| 15 | integration | Integration | All | Sonnet |
| 16 | deployment | Deployment | Bash | Sonnet |
| 17 | monitor | Monitoring | Bash | Haiku |
| 18 | maintainer | Maintenance | Read, Edit | Sonnet |
| 19 | learning | Pattern learning | Read | Haiku |

---

## 10. References

### 10.1 Source Documentation

1. **CLI Reference** - `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-cli-reference.md`
2. **Sub-Agents** - `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-sub-agents.md`
3. **Common Workflows** - `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-common-workflows.md`
4. **Settings** - `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-settings.md`
5. **Hooks** - `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-hooks.md`

### 10.2 BlackBox5 Context

1. **RALF Core** - `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/prompts/ralf.md`
2. **Sub-Agent Rules** - `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/rules/007-sub-agent-deployment.md`
3. **Superintelligence Protocol** - `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.claude/rules/005-superintelligence-auto-activation.md`

---

## 11. Summary

The Claude Code Task tool provides powerful sub-agent capabilities essential for BlackBox5's autonomous system:

1. **Parallel Execution** - Launch multiple agents simultaneously for research
2. **Context Isolation** - Keep verbose operations out of main conversation
3. **Specialized Agents** - Use built-in or custom agents for specific tasks
4. **Background Processing** - Run long tasks without blocking
5. **Dynamic Creation** - Define agents at runtime via CLI or files

**Key Takeaway for RALF:**
- Use `subagent_type="Explore"` with `model="haiku"` for initial codebase scanning
- Use parallel Task calls for multi-module research
- Always summarize before returning to main context
- Follow the >15 files rule for sub-agent spawning
- Implement the 19 planned research agents using dynamic agent definitions

---

*Document Version: 1.0*
*Last Updated: 2026-02-07*
*Author: Claude Code Research Agent*
