# Research Documentation

**Last Updated**: 2026-01-30
**Status**: Framework research and analysis

---

## Overview

This directory contains research on AI agent frameworks, methodologies, and patterns. These documents analyze various frameworks and approaches to inform BlackBox5's design decisions.

**Note**: This content was moved from `development/reference/research/` as it belongs in the theory section.

---

## Document Index

### Framework Analyses

| Document | Framework | Purpose |
|----------|-----------|---------|
| `AGENTSCOPE-GITHUB-ANALYSIS.md` | AgentScope | Multi-agent platform analysis |
| `agentscope-ai-agentscope-ANALYSIS.md` | AgentScope | Detailed technical analysis |
| `BMAD-ANALYSIS.md` | BMAD | Multi-agent methodology analysis |
| `bmad-code-org-BMAD-METHOD-ANALYSIS.md` | BMAD Method | Methodology deep dive |
| `DEERFLOW-ANALYSIS.md` | DeerFlow | ByteDance agent framework |
| `bytedance-deer-flow-ANALYSIS.md` | DeerFlow | Alternative analysis |
| `GOOGLE-ADK-ANALYSIS.md` | Google ADK | Google's agent framework |
| `google-adk-python-ANALYSIS.md` | Google ADK Python | Python SDK analysis |
| `METAGPT-GITHUB-ANALYSIS.md` | MetaGPT | Multi-agent framework |
| `FoundationAgents-MetaGPT-ANALYSIS.md` | MetaGPT | Foundation Agents analysis |
| `microsoft-agent-framework-ANALYSIS.md` | Microsoft | MS agent framework |
| `openai-swarm-ANALYSIS.md` | OpenAI Swarm | Swarm intelligence |
| `PRAISONAI-ANALYSIS.md` | PraisonAI | AI framework analysis |
| `MervinPraison-PraisonAI-ANALYSIS.md` | PraisonAI | Alternative analysis |
| `iflytek-astron-agent-ANALYSIS.md` | iFlytek Astron | Chinese agent framework |
| `ruvnet-claude-flow-ANALYSIS.md` | Claude Flow | Claude-based workflows |
| `ralphy-ANALYSIS.md` | Ralph | TUI-based agent system |

### Research Summaries

| Document | Purpose |
|----------|---------|
| `NEW-FRAMEWORKS-DISCOVERY.md` | New framework research findings |
| `FRAMEWORK-PATTERNS-SYNTHESIS.md` | Pattern synthesis across frameworks |
| `AUTONOMOUS-TEST-SUMMARY.md` | Autonomous testing research |

### Code Snippets
**Directory**: `snippets/`

Contains reusable code snippets from framework research.

---

## Key Research Insights

### 1. Memory Architecture Patterns
Research across frameworks identified common patterns:
- **Tiered Memory**: Working → Extended → Archival
- **Episode-Based Storage**: Structured knowledge categorization
- **Knowledge Graphs**: Neo4j/Graphiti for relationships
- **Vector Search**: ChromaDB for semantic retrieval

See: `../02-memory/` for implementation

### 2. Multi-Agent Orchestration
Frameworks analyzed for orchestration patterns:
- **Auto-Claude**: Spec-based coordination
- **MetaGPT**: Role-based multi-agent
- **OpenAI Swarm**: Swarm intelligence
- **BMAD**: 12-agent methodology

See: `../../02-implementation/01-core/orchestration/` for implementation

### 3. Skills and Capabilities
Research on agent capabilities:
- **CLI vs MCP**: CLI tools outperform (77 vs 60 benchmark)
- **Agent Skills Standard**: Cross-platform compatibility
- **Hybrid Approach**: Tier 1 (Python) + Tier 2 (Agent Skills)

See: `../../02-implementation/06-tools/skills/` for implementation

---

## Framework Comparison Matrix

| Framework | Type | Memory | Orchestration | Status |
|-----------|------|--------|---------------|--------|
| AgentScope | Platform | Graph-based | Visual | Research |
| BMAD | Methodology | Artifact-based | 12 agents | Research |
| DeerFlow | Framework | Vector store | Workflow | Research |
| Google ADK | Framework | SQLite | Sequential | Research |
| MetaGPT | Framework | Knowledge graph | Role-based | Research |
| OpenAI Swarm | Framework | State-based | Swarm | Research |
| PraisonAI | Framework | Multi-backend | DAG | Research |
| Ralph | TUI | Progressive | Interactive | Research |

---

## How to Use This Research

### For Architects
1. Review framework analyses for design patterns
2. Check `FRAMEWORK-PATTERNS-SYNTHESIS.md` for commonalities
3. Apply insights to BlackBox5 architecture

### For Developers
1. Check `snippets/` for reusable code patterns
2. Review specific framework analyses for implementation details
3. Use research to inform feature development

### For Decision Makers
1. Review framework comparison matrix
2. Check `NEW-FRAMEWORKS-DISCOVERY.md` for emerging trends
3. Use research to guide technology choices

---

## Related Documentation

- **Memory Architecture**: `../02-memory/`
- **Orchestrator**: `../../02-implementation/01-core/orchestration/`
- **Skills**: `../../02-implementation/06-tools/skills/`

---

## Summary

This directory contains **framework research that informs BlackBox5's design**:

- 17 framework analyses
- Pattern synthesis documents
- Code snippets for reuse
- Comparison matrices

All research is preserved for reference and ongoing learning.

---

**Maintainer**: SISO Internal Team
**Last Review**: 2026-01-30
**Original Location**: `development/reference/research/`
**New Location**: `01-theory/05-research/`
