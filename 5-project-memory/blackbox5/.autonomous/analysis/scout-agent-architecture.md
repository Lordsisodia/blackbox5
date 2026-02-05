# Scout Report: 6-Agent Pipeline Architecture Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Executive Summary

The BlackBox5 system has **two parallel agent implementations** with different purposes and coupling levels:

| Layer | Location | Language | Purpose | Coupling |
|-------|----------|----------|---------|----------|
| **Engine Agents** | `2-engine/.autonomous/bin/` | Python | Generic improvement loop | Tightly coupled to BlackBox5 |
| **Project Agents** | `5-project-memory/blackbox5/.autonomous/agents/` | Bash | GitHub analysis pipeline | Hardcoded to BlackBox5 |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT IMPROVEMENT LOOP                        │
│                     (Engine - Python)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │  Scout   │───▶│ Planner  │───▶│ Executor │───▶│ Verifier │ │
│   │(find    │    │(prioritize│    │(implement│    │(validate │ │
│   │ issues)  │    │  tasks)  │    │  fixes)  │    │  work)   │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │                                               │        │
│        └───────────────────────────────────────────────┘        │
│                      (improvement-loop.py)                       │
│                           Orchestrator                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  GITHUB ANALYSIS PIPELINE                        │
│                   (Project - Bash)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│   │  Scout   │───▶│ Analyzer │───▶│ Planner  │                  │
│   │(extract │    │(summarize│    │(create   │                  │
│   │  repos)  │    │  data)   │    │  plans)  │                  │
│   └──────────┘    └──────────┘    └──────────┘                  │
│        │              │                │                         │
│        ▼              ▼                ▼                         │
│   extractions/    summaries/     integration-plans/              │
│                                                                  │
│              Communication via events.yaml + heartbeat.yaml      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Analysis

### 1. Engine Python Scripts (`2-engine/.autonomous/bin/`)

| Script | Lines | Purpose | Key Dependencies |
|--------|-------|---------|------------------|
| `scout-intelligent.py` | 632 | Spawns Claude subagents to analyze project | Hardcoded `PROJECT_DIR`, `ENGINE_DIR` paths |
| `scout-analyze.py` | 471 | Static analysis of skill metrics, learnings | `skill-metrics.yaml`, `improvement-backlog.yaml` |
| `scout-task-based.py` | 433 | Task tool wrapper for parallel analysis | Same hardcoded paths |
| `planner-prioritize.py` | 441 | Creates tasks from scout reports | `scout-reports/`, `tasks/active/` |
| `executor-implement.py` | 451 | Auto-implements quick wins | Hardcoded task IDs (TASK-SKIL-005, etc.) |
| `verifier-validate.py` | 352 | Validates executor work | `executor-reports/`, specific file paths |
| `improvement-loop.py` | 366 | Orchestrates full loop | All other scripts |

**Coupling Issues:**
- All scripts hardcode `PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"`
- `scout-intelligent.py` embeds 5 different analyzer prompts with BlackBox5-specific file paths
- `executor-implement.py` has hardcoded task handlers for specific task IDs (TASK-SKIL-005, TASK-ARCH-012)
- `verifier-validate.py` validates specific file modifications (skill-selection.yaml thresholds)

### 2. Project Shell Scripts (`5-project-memory/blackbox5/.autonomous/agents/`)

| Script | Lines | Purpose | Key Dependencies |
|--------|-------|---------|------------------|
| `scout/scout-agent.sh` | 165 | GitHub repo extraction | `PROJECT_ROOT="/opt/ralf"`, `repo-list.yaml` |
| `analyzer/analyzer-agent.sh` | 263 | Pattern recognition from extractions | `extractions/`, `events.yaml` |
| `planner/planner-agent.sh` | 429 | Creates integration plans | `summaries/`, `tasks/active/` |
| `github-analysis-pipeline.sh` | 112 | Orchestrates 3-agent pipeline | All agent scripts |

**Coupling Issues:**
- Hardcoded `PROJECT_ROOT="/opt/ralf"` (different from Python scripts!)
- Direct YAML file manipulation for events/heartbeat
- Specific directory structure assumptions (`5-project-memory/blackbox5/...`)
- Creates task files in specific format for BlackBox5

---

## Dependency Analysis

### Hardcoded Paths (Engine Python)

```python
# From scout-intelligent.py, planner-prioritize.py, etc.
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
OUTPUT_DIR = PROJECT_DIR / ".autonomous" / "analysis" / "scout-reports"
```

### Hardcoded Paths (Project Bash)

```bash
# From scout-agent.sh, analyzer-agent.sh, etc.
PROJECT_ROOT="/opt/ralf"
AGENTS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents"
```

### Communication Mechanisms

| Mechanism | Used By | Format | Location |
|-----------|---------|--------|----------|
| YAML files | Bash agents | events.yaml, heartbeat.yaml | `agents/communications/` |
| JSON/YAML reports | Python agents | scout-report-*.yaml | `.autonomous/analysis/` |
| Task files | Both | task.md | `tasks/active/` |
| Subprocess | Python | stdout/stderr | Direct script calls |

---

## Coupling Assessment

### Tight Coupling Areas (Score: High)

1. **Directory Structure** (10/10)
   - Both implementations assume exact BlackBox5 directory hierarchy
   - 47+ hardcoded path references across all scripts

2. **File Formats** (9/10)
   - YAML schemas for events, heartbeat, reports are hardcoded
   - Task markdown format is assumed

3. **Task ID Conventions** (8/10)
   - `executor-implement.py` routes by specific task IDs
   - Pattern: `TASK-{CATEGORY}-{NUMBER}`

4. **Configuration Files** (8/10)
   - Direct references to `skill-metrics.yaml`, `skill-selection.yaml`
   - Assumes specific YAML structure

5. **Communication Protocol** (7/10)
   - Bash agents use file-based events/heartbeat
   - Python agents use report files

### Medium Coupling Areas (Score: Medium)

1. **Analyzer Prompts** (6/10)
   - Embedded in `scout-intelligent.py` with project-specific file paths
   - Would need parameterization for reuse

2. **Scoring Algorithms** (5/10)
   - Priority thresholds, effort mapping are configurable but embedded

---

## Recommendations for Decoupling

### 1. Configuration-Driven Architecture

Create a unified configuration file:

```yaml
# agent-config.yaml
project:
  name: "blackbox5"
  root_dir: "~/.blackbox5/5-project-memory/blackbox5"
  engine_dir: "~/.blackbox5/2-engine"

agents:
  scout:
    output_dir: ".autonomous/analysis/scout-reports"
    analyzers:
      - skill
      - process
      - documentation
  planner:
    output_dir: "tasks/active"
    priority_thresholds:
      CRITICAL: 15.0
      HIGH: 12.0
  executor:
    auto_execute: true
    max_tasks: 5
  verifier:
    validation_checks: 3

communication:
  protocol: "file"  # or "mcp", "http"
  events_file: ".autonomous/agents/communications/events.yaml"
  heartbeat_file: ".autonomous/agents/communications/heartbeat.yaml"
```

### 2. Agent Interface Contract

Standardize agent interface:

```python
# Base agent class
class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config

    def run(self, input_data: Dict) -> AgentResult:
        raise NotImplementedError

    def validate(self) -> bool:
        """Check if required inputs exist"""
        pass

# Standard result format
@dataclass
class AgentResult:
    success: bool
    outputs: Dict[str, Path]
    metrics: Dict[str, Any]
    next_agent: Optional[str]
```

### 3. Project-Agnostic Implementation

**Option A: Environment Variables**
```bash
export AGENT_PROJECT_ROOT="/path/to/project"
export AGENT_CONFIG_PATH="/path/to/config.yaml"
./scout-intelligent.py
```

**Option B: CLI Arguments**
```bash
./scout-intelligent.py \
  --project-dir /path/to/project \
  --config /path/to/config.yaml \
  --output-dir /path/to/output
```

**Option C: MCP Protocol**
```json
{
  "mcpServers": {
    "ralf-agents": {
      "command": "python",
      "args": ["-m", "ralf.agents.server"],
      "env": {
        "RALF_PROJECT_ROOT": "/path/to/project"
      }
    }
  }
}
```

### 4. Unified Agent Location

**Recommendation:** Move all agents to engine, make project-specific via config:

```
2-engine/
└── .autonomous/
    └── agents/
        ├── core/              # Generic agent implementations
        │   ├── scout.py
        │   ├── planner.py
        │   ├── executor.py
        │   └── verifier.py
        ├── interfaces/        # Protocol implementations
        │   ├── file_based.py
        │   ├── mcp_based.py
        │   └── http_based.py
        └── configs/           # Project-specific configs
            ├── blackbox5.yaml
            └── template.yaml
```

---

## Proposed Agent Interface

```yaml
# Agent Interface Specification v1.0

agent:
  name: string           # Unique agent identifier
  version: string        # Semver
  type: scout|planner|executor|verifier|analyzer|architect

  inputs:
    - name: string
      type: file|json|yaml|directory
      required: boolean
      description: string

  outputs:
    - name: string
      type: file|json|yaml
      path: string         # Relative to output_dir

  config:
    parameters:
      - name: string
        type: string|number|boolean
        default: any
        description: string

  communication:
    protocol: file|mcp|http|stdio
    events: boolean        # Emit events
    heartbeat: boolean     # Update heartbeat
```

---

## Summary

| Aspect | Current State | Recommended State |
|--------|---------------|-------------------|
| **Location** | Split (engine + project) | Unified in engine |
| **Configuration** | Hardcoded paths | Config-driven |
| **Coupling** | Tight (BlackBox5-specific) | Loose (project-agnostic) |
| **Communication** | File-based YAML | Pluggable protocol |
| **Scalability** | Single project | Multi-project |
| **Testing** | Difficult (path deps) | Easy (configurable) |

**Priority Actions:**
1. Extract hardcoded paths to configuration
2. Create base agent classes with standard interfaces
3. Implement MCP protocol option for cross-project communication
4. Move all agents to engine, use config for project specifics
5. Create project initialization tool that generates config from template
