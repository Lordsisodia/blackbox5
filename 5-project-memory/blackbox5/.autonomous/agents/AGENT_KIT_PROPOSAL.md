# BlackBox5 Custom Sub-Agent Kit Proposal

## Current State Analysis

### What We Have Now

**10 Registered Agents in BlackBox5 Registry:**
| Agent | Type | Purpose | Status |
|-------|------|---------|--------|
| scout | bash | GitHub repo discovery | Active |
| analyzer | hybrid | Data summarization | Active |
| planner | bash | Integration planning | Active |
| executor | bash | Task execution | Active |
| architect | hybrid | System architecture | Active |
| communications | yaml | Coordination hub | Active |
| execution | yaml | Parallel execution (5 slots) | Active |
| metrics | yaml | Performance tracking | Active |
| reanalysis | yaml | Task relevance maintenance | Active |
| github-analysis-pipeline | bash | 3-Agent RALF pipeline | Active |

**Problem:** These are RALF-specific bash/yaml agents, NOT Claude Code native sub-agents.

### What Claude Code Supports

**Built-in Subagent Types:**
- `Explore` - Read-only codebase search (Haiku)
- `Plan` - Read-only planning mode
- `general-purpose` - Full tool access
- `Bash` - Terminal commands only
- `claude-code-guide` - Feature questions
- `statusline-setup` - Status line config

**Custom Agent Configuration (YAML Frontmatter):**
```markdown
---
name: agent-name
description: "When to use this agent"
tools: [Read, Write, Edit, Bash, Task]
disallowedTools: [Write, Edit]  # Optional
model: sonnet | opus | haiku
color: red | blue | green | yellow | purple | orange | pink | cyan
---

# Agent instructions here...
```

## The Gap

We need **Claude Code native sub-agents** that can:
1. Be invoked via `Task(subagent_type="custom-agent")`
2. Have specific tool permissions
3. Run with different models (GLM-4.7, Sonnet, Opus)
4. Work in parallel with isolated contexts
5. Integrate with our GLM API for cost-effective tasks

---

## Proposed BlackBox5 Agent Kit

### Tier 1: Core Utility Agents (Always Available)

#### 1. `bb5-explorer`
**Purpose:** Deep codebase exploration with structured output
```yaml
---
name: bb5-explorer
description: "Deep codebase exploration for BlackBox5. Use proactively when searching across >15 files or complex pattern matching."
tools: [Read, Grep, Glob, Bash]
model: sonnet
color: blue
---
```
**Capabilities:**
- Cross-project exploration
- Pattern recognition
- Architecture mapping
- Dependency analysis

#### 2. `bb5-researcher`
**Purpose:** Web research and documentation synthesis
```yaml
---
name: bb5-researcher
description: "Research specialist for BlackBox5. Use proactively for technology research, best practices, and competitive analysis."
tools: [WebSearch, WebFetch, Read, Write]
model: sonnet
color: cyan
---
```
**Capabilities:**
- Technology evaluation
- Best practice research
- Documentation synthesis
- Trend analysis

#### 3. `bb5-validator`
**Purpose:** Multi-dimensional validation
```yaml
---
name: bb5-validator
description: "Validation specialist for BlackBox5. Use proactively after implementation to verify correctness, security, and quality."
tools: [Read, Grep, Bash]
model: sonnet
color: green
---
```
**Capabilities:**
- Correctness verification
- Security audit
- Quality gates
- Test validation

### Tier 2: Domain Specialist Agents (Role-Specific)

#### 4. `bb5-architect`
**Purpose:** System design and architecture decisions
```yaml
---
name: bb5-architect
description: "System architect for BlackBox5. Use proactively for architecture questions, design patterns, and scalability planning."
tools: [Read, Write, Task]
model: opus
color: purple
---
```
**Capabilities:**
- Architecture design
- Pattern selection
- Scalability planning
- Integration architecture

#### 5. `bb5-security-auditor`
**Purpose:** Security-focused code review
```yaml
---
name: bb5-security-auditor
description: "Security auditor for BlackBox5. Use proactively for security reviews, vulnerability detection, and compliance checks."
tools: [Read, Grep, Bash]
model: opus
color: red
---
```
**Capabilities:**
- Vulnerability scanning
- OWASP compliance
- Threat modeling
- Security recommendations

#### 6. `bb5-performance-analyst`
**Purpose:** Performance optimization
```yaml
---
name: bb5-performance-analyst
description: "Performance specialist for BlackBox5. Use proactively for performance bottlenecks, optimization strategies, and profiling."
tools: [Read, Bash, Glob]
model: sonnet
color: orange
---
```
**Capabilities:**
- Bottleneck identification
- Optimization strategies
- Profiling analysis
- Resource usage review

### Tier 3: GLM-Integrated Agents (Cost-Optimized)

#### 7. `bb5-glm-reviewer`
**Purpose:** Cost-effective validation using GLM-4.7
```yaml
---
name: bb5-glm-reviewer
description: "Economic validation agent using GLM-4.7. Use proactively for routine reviews, documentation checks, and simple validations."
tools: [Read, Bash]
model: sonnet  # Claude wraps GLM calls
color: yellow
---
```
**Capabilities:**
- Code review (via GLM-4.7)
- Documentation validation
- Simple pattern matching
- Web search integration

**Special:** This agent uses GLM-4.7 MCP tools for cost-effective operations:
- `mcp__web-search-prime__webSearchPrime`
- `mcp__zai-mcp-server__analyze_image`
- `mcp__zread__search_doc`

#### 8. `bb5-glm-vision`
**Purpose:** Visual analysis and UI validation
```yaml
---
name: bb5-glm-vision
description: "Visual analysis specialist using GLM-4.7 vision capabilities. Use proactively for UI reviews, screenshot analysis, and diagram understanding."
tools: [Read, Bash]
model: sonnet
color: pink
---
```
**Capabilities:**
- Screenshot analysis
- UI regression testing
- Diagram parsing
- Visual error diagnosis

### Tier 4: Workflow Orchestration Agents

#### 9. `bb5-orchestrator`
**Purpose:** Multi-agent workflow coordination
```yaml
---
name: bb5-orchestrator
description: "Workflow orchestrator for BlackBox5. Use proactively for complex tasks requiring multiple agents and parallel execution."
tools: [Task, Read, Write, Bash]
model: opus
color: purple
---
```
**Capabilities:**
- Agent delegation
- Parallel execution
- Result synthesis
- Workflow management

#### 10. `bb5-synthesizer`
**Purpose:** Multi-source information synthesis
```yaml
---
name: bb5-synthesizer
description: "Information synthesizer for BlackBox5. Use proactively to combine outputs from multiple agents into coherent recommendations."
tools: [Read, Write]
model: opus
color: blue
---
```
**Capabilities:**
- Multi-perspective integration
- Conflict resolution
- Recommendation synthesis
- Decision support

---

## File Structure

```
~/.blackbox5/5-project-memory/blackbox5/.claude/
├── agents/
│   ├── bb5-explorer.md
│   ├── bb5-researcher.md
│   ├── bb5-validator.md
│   ├── bb5-architect.md
│   ├── bb5-security-auditor.md
│   ├── bb5-performance-analyst.md
│   ├── bb5-glm-reviewer.md
│   ├── bb5-glm-vision.md
│   ├── bb5-orchestrator.md
│   └── bb5-synthesizer.md
└── settings.json  # Register agents here
```

---

## Usage Patterns

### Pattern 1: Parallel Research
```python
# Launch multiple researchers in parallel
Task(
    prompt="Research authentication best practices",
    subagent_type="bb5-researcher",
    model="sonnet",
    run_in_background=True
)
Task(
    prompt="Research authorization patterns",
    subagent_type="bb5-researcher",
    model="sonnet",
    run_in_background=True
)
Task(
    prompt="Research session management",
    subagent_type="bb5-researcher",
    model="sonnet",
    run_in_background=True
)
```

### Pattern 2: Validation Pipeline
```python
# Sequential validation with different agents
security = Task(
    prompt="Audit auth module for vulnerabilities",
    subagent_type="bb5-security-auditor",
    model="opus"
)

performance = Task(
    prompt="Analyze auth flow performance",
    subagent_type="bb5-performance-analyst",
    model="sonnet"
)

# Cost-effective final review
glm_review = Task(
    prompt="Review auth implementation",
    subagent_type="bb5-glm-reviewer",
    model="sonnet"
)
```

### Pattern 3: GLM-Enhanced Analysis
```python
# Use GLM for cost-effective web research
research = Task(
    prompt='''
    Research the latest React 19 features using GLM web search:
    /glm-web-search "React 19 new features 2026"

    Summarize findings for the team.
    ''',
    subagent_type="bb5-researcher",
    model="sonnet",
    run_in_background=True
)
```

---

## Integration with Existing RALF System

### Current RALF Agents (Bash/YAML-based)
- scout, analyzer, planner, executor, architect
- Communications hub, execution slots, metrics

### New Claude Code Agents (Sub-agent-based)
- bb5-explorer, bb5-researcher, bb5-validator
- bb5-architect, bb5-security-auditor, bb5-performance-analyst
- bb5-glm-reviewer, bb5-glm-vision, bb5-orchestrator, bb5-synthesizer

### Hybrid Approach
1. **RALF handles:** Pipeline orchestration, state management, metrics
2. **Claude sub-agents handle:** Actual implementation, research, validation
3. **Integration via:** Task tool calls from RALF scripts

---

## Cost Optimization Strategy

| Task Type | Agent | Model | Cost Level |
|-----------|-------|-------|------------|
| Exploration | bb5-explorer | sonnet | Medium |
| Research | bb5-researcher | sonnet | Medium |
| Routine validation | bb5-glm-reviewer | GLM-4.7 | Low |
| Visual analysis | bb5-glm-vision | GLM-4.7 | Low |
| Security audit | bb5-security-auditor | opus | High |
| Architecture | bb5-architect | opus | High |
| Synthesis | bb5-synthesizer | opus | High |

---

## Next Steps

1. **Create agent files** in `.claude/agents/`
2. **Register agents** in `.claude/settings.json`
3. **Test integration** with existing RALF pipeline
4. **Document usage patterns** in agent registry
5. **Monitor effectiveness** via metrics agent

---

## Sources

- [A practical guide to the Claude Code sub-agent for 2025](https://www.eesel.ai/blog/claude-code-sub-agent)
- [Claude Code Sub-Agents: Complete Guide](https://smartmaya.ai/blog/claude-code-sub-agents-guide)
- [Mastering Claude Agent SDK: Best Practices](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)
- Multi-Agent Ralph Loop v2.83.1 documentation
- Anthropic Claude Code official documentation (Oct 2025)
