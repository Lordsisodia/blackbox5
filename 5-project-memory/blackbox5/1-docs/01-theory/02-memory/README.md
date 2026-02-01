# Memory Architecture Documentation

**Last Updated**: 2026-01-30
**Status**: Multi-document consolidation complete

---

## Overview

This directory contains comprehensive documentation for BlackBox5's memory architecture. The memory system has evolved through multiple iterations, resulting in several documents that each capture different aspects and design decisions.

## Quick Navigation

### For New Users
Start with the **Simplified Memory Architecture** for the current production implementation.

### For Architects
Review the **Comprehensive Memory Architecture** for the complete 8-component design.

### For Decision Making
See the **Memory Architecture Comparison** for framework analysis and recommendations.

---

## Document Index

### 1. Simplified Memory Architecture (Production)
**File**: `../01-architecture/core/SIMPLIFIED-MEMORY-ARCHITECTURE.md`

**Purpose**: Current production implementation - simple, proven approach

**Key Points**:
- Working memory with sliding window (deque)
- SQLite persistent storage
- Simple API covering 90% of use cases
- Based on what LangChain, AutoGen, and OpenAI actually use in production
- Implementation time: 2-3 days
- ~300 lines of code

**Use This For**: Understanding the current working implementation

---

### 2. Comprehensive Memory Architecture (Design)
**File**: `../01-architecture/core/COMPREHENSIVE-MEMORY-ARCHITECTURE.md`

**Purpose**: Complete 8-component memory system design based on framework analysis

**Key Points**:
- 8 core memory components (Agent, Task, Workflow, Architecture, GitHub, Codebase, Knowledge Graph, Secure)
- Three-tier architecture (Working 10MB → Extended 500MB → Archival 5GB)
- Multiple backends (Filesystem, SQLite, ChromaDB, PostgreSQL, Neo4j)
- Based on BMAD, GSD, Ralph, BlackBox4, and MIRIX patterns
- Implementation time: 4-6 weeks
- Medium-High complexity

**Use This For**: Understanding the full vision and future implementation path

---

### 3. Multi-Project Memory Architecture
**File**: `../01-architecture/core/MEMORY-ARCHITECTURE.md`

**Purpose**: Architecture for one BlackBox5 engine serving multiple projects

**Key Points**:
- Single engine with per-project memory isolation
- Template-based initialization
- Project-centric memory organization
- GitHub repository structure design

**Use This For**: Understanding how memory works across multiple projects

---

### 4. Memory Architecture Comparison
**File**: `design/MEMORY-ARCHITECTURE-COMPARISON.md`

**Purpose**: Framework analysis and recommendation

**Key Points**:
- Comparison of BlackBox4, Auto-Claude, Cognee, and BlackBox5
- Winner: BlackBox4 + Auto-Claude hybrid
- Best practices across all systems
- Recommended optimal hybrid architecture
- 10-week implementation timeline

**Use This For**: Decision making and understanding trade-offs between approaches

---

### 5. Per-Project Memory Architecture
**File**: `design/PER-PROJECT-MEMORY-ARCHITECTURE.md`

**Purpose**: Project-specific memory organization

**Use This For**: Understanding memory structure within a single project

---

## Architecture Evolution

### Phase 1: Simplified (Current)
We implemented a **simplified production memory system** that matches what major frameworks (LangChain, AutoGen, OpenAI) actually use:

```
Working Memory (deque) → Persistent Memory (SQLite)
```

**Rationale**: 
- 90% of value with 10% of complexity
- Battle-tested in production
- Easy to maintain and extend

### Phase 2: Comprehensive (Future)
The **comprehensive architecture** provides a roadmap for when we need:

```
Working (10MB) → Extended (500MB) → Archival (5GB)
     ↓                ↓                  ↓
  Agents         ChromaDB          Snapshots
  Tasks          PostgreSQL        Exports
  Workflows      Neo4j             Backups
```

**Rationale**:
- Supports advanced features when needed
- Framework-backed design decisions
- Clear migration path from simplified

---

## Key Design Decisions

### 1. Simplicity First
> "Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."
> - Antoine de Saint-Exupéry

We started with the simplified approach because:
- Production systems achieve 90% success with simple conversation buffers
- 10x infrastructure complexity for 4% improvement is poor ROI
- No production AI system uses capability-based memory protection

### 2. Measure Then Optimize
- Implement simple version first
- Measure actual performance
- Optimize only if needed

### 3. Production Over Academic
- What works in production > What looks good in papers
- Real-world constraints > Theoretical ideals
- User value > Technical complexity

---

## Implementation Status

| Component | Status | Document |
|-----------|--------|----------|
| Working Memory | ✅ Implemented | Simplified |
| Persistent Storage | ✅ Implemented | Simplified |
| Agent Memory | ⚠️ Planned | Comprehensive |
| Task Memory | ⚠️ Planned | Comprehensive |
| Workflow Memory | ⚠️ Planned | Comprehensive |
| Knowledge Graph | ⚠️ Planned | Comprehensive |
| Vector Search | ⚠️ Planned | Comprehensive |
| Multi-Project | ✅ Designed | Multi-Project |

---

## Usage

### Current Implementation
```python
from pathlib import Path
from blackbox5.engine.memory import create_message, get_memory_system

# Initialize
memory = get_memory_system(Path("."), project_name="my-project")

# Add message
memory.add(create_message("user", "Implement feature X", task_id="task-123"))

# Get context for LLM
context = memory.get_context(limit=10)

# Search
results = memory.search("feature X")
```

### Future Implementation
See Comprehensive Memory Architecture for the full 8-component API.

---

## Related Documentation

- **Orchestrator**: `../../02-implementation/01-core/orchestration/`
- **Skills**: `../../02-implementation/06-tools/skills/`
- **Getting Started**: `../../03-guides/01-getting-started/`

---

## Summary

This directory serves as the **entry point for memory documentation**. Choose your path:

1. **Want to understand current implementation?** → Simplified Memory Architecture
2. **Want to see the full vision?** → Comprehensive Memory Architecture
3. **Want to compare approaches?** → Memory Architecture Comparison
4. **Want multi-project setup?** → Multi-Project Memory Architecture

All documents are preserved for historical context and future reference.

---

**Maintainer**: SISO Internal Team
**Last Review**: 2026-01-30
