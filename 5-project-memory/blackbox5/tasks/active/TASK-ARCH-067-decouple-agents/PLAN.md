# PLAN.md: Decouple Agents from Project Structure

**Task:** TASK-ARCH-067
**Status:** pending
**Created:** 2026-02-06

## Objective
Make 6-agent pipeline project-agnostic by removing BlackBox5-specific coupling.

## Current Coupling Issues

### 1. Hardcoded Paths (CRITICAL)
All agents contain:
```python
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
```

### 2. Hardcoded Task IDs (HIGH)
Executor has task-specific handlers:
```python
if task_id == "TASK-SKIL-005":
    return self.execute_threshold_fix(task)
```

### 3. Hardcoded File References (HIGH)
```python
file_path = PROJECT_DIR / "operations" / "skill-selection.yaml"
```

## Decoupling Strategy

### 1. Configuration-Driven Architecture
Create `agent-config.yaml`:
```yaml
project:
  name: "blackbox5"
  root_path: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5"
paths:
  operations: "operations"
  tasks: "tasks/active"
handlers:
  threshold_fix:
    file: "operations/skill-selection.yaml"
    pattern: "threshold: 70"
```

### 2. Base Agent Class
```python
class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.project_dir = config.project_dir
```

### 3. Task Handler System
Pluggable handlers instead of hardcoded task IDs:
```python
class TaskHandler(ABC):
    @abstractmethod
    def can_handle(self, task: Dict) -> bool:
        pass
    @abstractmethod
    def execute(self, task: Dict) -> ExecutionResult:
        pass
```

## Implementation Steps
1. Create AgentConfig class (1.5 hours)
2. Create BaseAgent class (1 hour)
3. Create ProjectDiscovery module (0.5 hours)
4. Update Scout agents (2 hours)
5. Update Planner agent (2 hours)
6. Update Executor agent (3 hours)
7. Update Verifier agent (2 hours)
8. Update Improvement Loop (2 hours)
9. Create agent-init-project.py tool (2 hours)
10. Testing (2 hours)

## Timeline
- Total: 20-24 hours

## Success Criteria
- [ ] All hardcoded paths removed
- [ ] Agent-config.yaml created
- [ ] Base Agent class implemented
- [ ] Task handler system working
- [ ] Agents work with any project directory
- [ ] Project initialization tool created
