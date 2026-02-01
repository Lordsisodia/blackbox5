# Context Gatherer Sub-Agents

**Purpose:** Efficiently acquire relevant context without wasting super-agent's context budget

---

## The Context Problem

Superintelligence requires understanding:
- Project structure and architecture
- Existing code patterns
- Documentation and requirements
- Cross-project dependencies
- Historical decisions

**But:** The super-agent has limited context. Loading everything wastes capacity needed for reasoning.

**Solution:** Deploy specialized context gatherer sub-agents that scan, summarize, and return only what's relevant.

---

## Context Gatherer Types

### 1. Project Scanner Agent

**Purpose:** Get holistic view of a project

**Deploy When:**
- Task mentions a project name
- Need to understand overall architecture
- Looking for cross-file patterns
- Need to identify key files

**Process:**
```
1. Read project root (README, package.json, etc.)
2. Map directory structure
3. Identify key configuration files
4. Find main entry points
5. Locate documentation
6. Return: Project summary + key files list
```

**Output Format:**
```yaml
project: "blackbox5"
summary: "Multi-agent AI orchestration platform"
architecture: "Modular with engine, memory, and agent systems"
key_files:
  - path: "2-engine/core/orchestrator.py"
    relevance: "high"
    description: "Main agent orchestration logic"
  - path: "1-docs/01-theory/02-memory/README.md"
    relevance: "medium"
    description: "Memory system documentation"
entry_points:
  - "bin/blackbox"
  - "bin/ralf"
dependencies:
  - "redis"
  - "docker"
  - "python3.11+"
```

---

### 2. Folder Scanner Agent

**Purpose:** Deep dive into specific directories

**Deploy When:**
- Need detailed understanding of subsystem
- Task is localized to specific area
- Project scan identified relevant folder
- Looking for specific file types

**Process:**
```
1. List all files in folder
2. Read key files (configs, main modules)
3. Identify patterns and conventions
4. Map relationships between files
5. Return: Detailed folder analysis
```

**Output Format:**
```yaml
folder: "2-engine/core/"
file_count: 23
key_modules:
  - name: "orchestrator.py"
    purpose: "Coordinates agent execution"
    dependencies: ["agent_pool", "memory_system", "mcp_tools"]
  - name: "agent_pool.py"
    purpose: "Manages agent lifecycle"
    dependencies: ["docker", "redis"]
patterns:
  - "All agents extend BaseAgent class"
  - "Async/await for I/O operations"
  - "Redis for state persistence"
conventions:
  - "Files named with snake_case"
  - "Classes use PascalCase"
  - "Constants in UPPER_SNAKE_CASE"
```

---

### 3. Cross-Reference Agent

**Purpose:** Find hidden dependencies across projects/folders

**Deploy When:**
- Suspect cross-project impacts
- Need to understand integration points
- Looking for shared libraries
- Analyzing dependency chains

**Process:**
```
1. Search for imports/includes across codebase
2. Identify shared modules
3. Map dependency graph
4. Find potential conflicts
5. Return: Dependency analysis
```

**Output Format:**
```yaml
cross_references:
  - source: "2-engine/core/orchestrator.py"
    imports: ["5-project-memory/models.py"]
    type: "direct"
    impact: "high"
  - source: "6-roadmap/frameworks/bmad/"
    shared_with: ["2-engine/agents/bmad/"]
    type: "code_duplication"
    recommendation: "Consider extracting to shared library"
potential_conflicts:
  - location: "Multiple requirements.txt"
    issue: "Different versions of redis"
    resolution: "Standardize on 5.0.1"
```

---

### 4. Historical Context Agent

**Purpose:** Understand why things are the way they are

**Deploy When:**
- Need to understand design decisions
- Looking for rationale behind patterns
- Want to avoid repeating past mistakes
- Need to know evolution of system

**Process:**
```
1. Read git history for relevant files
2. Find commit messages with context
3. Look for ADRs (Architecture Decision Records)
4. Check issues/discussions
5. Return: Historical context
```

**Output Format:**
```yaml
historical_context:
  - file: "2-engine/core/orchestrator.py"
    key_decisions:
      - date: "2025-11-15"
        commit: "abc123"
        decision: "Switched from threading to asyncio"
        rationale: "Better performance with I/O-bound operations"
        author: "shaansisodia"
    patterns:
      - "Major refactors happen in November"
      - "Preference for async patterns since 2025"
```

---

## Deployment Strategy

### Always Deploy Both

**Rule:** When gathering context, always scan:
1. **Projects** (holistic view)
2. **Folders** (detailed view)

**Why:** You miss things if you only look at one level.

**Example:**
```python
# Bad: Only project-level
task = "Add memory compression to the agent system"
context = scan_project("blackbox5")  # Misses specific implementation details

# Good: Both levels
project_context = scan_project("blackbox5")
folder_context = scan_folder("2-engine/core/")  # Finds orchestrator.py
folder_context += scan_folder("1-docs/01-theory/02-memory/")  # Finds memory docs
```

---

## Context Budget Management

### Super-Agent Context Allocation

| Component | Budget | Purpose |
|-----------|--------|---------|
| **System Instructions** | 10% | How to reason, what frameworks to use |
| **Task Definition** | 15% | What problem to solve |
| **Gathered Context** | 40% | What sub-agents found |
| **Reasoning Space** | 25% | Working memory for analysis |
| **Output Buffer** | 10% | Space for response |

### Sub-Agent Context Allocation

Context gatherers can use **full context** since they're specialized:
- Can load entire project structures
- Can read many files
- Can execute searches
- Return only summaries

---

## Implementation Pattern

```python
class ContextGatherer:
    def gather(self, task: str, hints: List[str]) -> ContextBundle:
        """
        Gather relevant context for a task.
        """
        bundle = ContextBundle()

        # 1. Identify relevant projects
        projects = self.identify_projects(task, hints)
        for project in projects:
            project_context = self.deploy_project_scanner(project)
            bundle.add(project_context)

        # 2. Identify relevant folders
        folders = self.identify_folders(task, hints, bundle)
        for folder in folders:
            folder_context = self.deploy_folder_scanner(folder)
            bundle.add(folder_context)

        # 3. Check for cross-references
        if self.needs_cross_reference_analysis(bundle):
            cross_refs = self.deploy_cross_reference_agent(bundle)
            bundle.add(cross_refs)

        # 4. Get historical context if needed
        if self.needs_historical_context(bundle):
            history = self.deploy_historical_agent(bundle)
            bundle.add(history)

        # 5. Rank and filter by relevance
        bundle = self.rank_by_relevance(bundle, task)
        bundle = self.filter_to_budget(bundle, max_tokens=16000)

        return bundle

    def deploy_project_scanner(self, project: str) -> ProjectContext:
        """Deploy sub-agent to scan project."""
        agent = SubAgent(
            role="project_scanner",
            instructions="Scan project and return summary + key files",
            context_budget="high"  # Can use lots of context
        )
        return agent.execute(project=project)

    def deploy_folder_scanner(self, folder: str) -> FolderContext:
        """Deploy sub-agent to scan folder."""
        agent = SubAgent(
            role="folder_scanner",
            instructions="Deep dive into folder and return detailed analysis",
            context_budget="high"
        )
        return agent.execute(folder=folder)
```

---

## Best Practices

### 1. Parallel Deployment

Deploy multiple context gatherers in parallel:
```python
# Parallel execution
project_future = deploy_async(project_scanner, "blackbox5")
folder1_future = deploy_async(folder_scanner, "2-engine/core/")
folder2_future = deploy_async(folder_scanner, "1-docs/01-theory/")

# Wait for all
contexts = await gather(project_future, folder1_future, folder2_future)
```

### 2. Caching

Cache context to avoid redundant scans:
```python
@cache(ttl=3600)  # Cache for 1 hour
def get_project_context(project: str) -> ProjectContext:
    return deploy_project_scanner(project)
```

### 3. Incremental Updates

For long-running tasks, incrementally update context:
```python
# Initial context
current_context = gather_context(task)

# Every N iterations, refresh
for iteration in range(max_iterations):
    if iteration % 5 == 0:
        new_context = gather_context(task, since=last_update)
        current_context.merge(new_context)
```

### 4. Relevance Scoring

Score each piece of context:
```python
class ContextItem:
    content: str
    source: str
    relevance_score: float  # 0.0 to 1.0
    token_count: int

# Keep only high-relevance items within budget
filtered = [item for item in context if item.relevance_score > 0.7]
filtered = sort_by_relevance(filtered)
filtered = fit_to_budget(filtered, max_tokens=16000)
```

---

## Example: Architecture Decision

**Task:** "What's the best architecture for adding real-time collaboration to BlackBox5?"

**Context Gathering:**

1. **Project Scanner** → "blackbox5"
   - Finds: Multi-agent orchestration, Redis-based, Docker containers
   - Key files: orchestrator.py, agent_pool.py, memory_system.py

2. **Folder Scanner** → "2-engine/core/"
   - Finds: Async patterns, WebSocket not currently used
   - Pattern: Event-driven architecture

3. **Folder Scanner** → "1-docs/01-theory/02-memory/"
   - Finds: Shared state patterns, Redis pub/sub mentioned

4. **Cross-Reference Agent**
   - Finds: Similar real-time features in "6-roadmap/" documentation
   - Pattern: WebSocket + Redis pub/sub combination

5. **Historical Agent**
   - Finds: Previous attempt at real-time features (2025-09)
   - Lesson: Use Redis streams, not simple pub/sub

**Result:** Super-agent gets condensed context:
```yaml
context_summary:
  current_architecture: "Async, event-driven, Redis-backed"
  relevant_patterns: ["pub/sub", "streams", "WebSocket"]
  previous_attempts: "Redis pub/sub had issues; streams recommended"
  key_constraints: ["Docker containers", "Multi-agent", "Stateless agents"]
```

Instead of loading 50+ files into super-agent context.

---

## Integration with Superintelligence Protocol

```python
def activate_superintelligence(task: str):
    # Phase 1: Context Acquisition (via sub-agents)
    context = ContextGatherer().gather(task)

    # Phase 2-7: Superintelligence reasoning (with clean context)
    return superintelligence_reasoning(task, context)
```

---

## Next Steps

1. **Implement project scanner agent**
2. **Implement folder scanner agent**
3. **Add relevance scoring algorithm**
4. **Create context caching layer**
5. **Build cross-reference detection**

---

**Related:**
- [Expert Roles](./expert-roles.md)
- [Deployment Patterns](./deployment-patterns.md)
- [Hierarchical Context](../context-management/hierarchical-context.md)
