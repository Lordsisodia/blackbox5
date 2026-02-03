# TASK-MEMORY-001: Improve Blackbox5 Persistent Memory System

**Status:** in_progress
**Priority:** HIGH
**Created:** 2026-02-04
**Owner:** RALF / Agent System
**Labels:** memory, architecture, research, enhancement

---

## Objective

Research, design, and implement an improved persistent memory system for Blackbox5 agents based on state-of-the-art memory architectures from 2025-2026.

---

## Success Criteria

- [ ] Research and document leading memory systems (Hindsight, Mem0, Zep, Letta, memU)
- [ ] Analyze Two Buffers theory (Functional + Subjective memory) from Moltbook community
- [ ] Design hybrid memory architecture for Blackbox5
- [ ] Implement prototype memory layer
- [ ] Benchmark against existing Blackbox5 memory
- [ ] Document integration approach

---

## Context

Current Blackbox5 uses file-based memory (THOUGHTS.md, DECISIONS.md, LEARNINGS.md) per run. This provides basic continuity but lacks:

1. **Semantic search** across all historical runs
2. **Structured relationship tracking** between decisions
3. **Subjective memory** (continuity of self/identity)
4. **Cross-session learning** and pattern recognition
5. **Efficient token usage** through smart retrieval

The field has converged on hybrid architectures: Vector DB (fuzzy recall) + Structured Store (relationships) + LLM consolidation.

---

## Research Findings Summary

### Leading Memory Systems

| System | Architecture | LongMemEval | Best For |
|--------|-------------|-------------|----------|
| **Hindsight** | 4-network structured | 91.4% | Advanced agents with belief updating |
| **Zep** | Temporal Knowledge Graph | 71.2% | Production at scale |
| **Mem0** | Vector + Graph + KV | 68.5% | Simple integration |
| **Letta** | OS-inspired hierarchy | 74.0%* | Research/explicit control |
| **memU** | 3-layer hierarchical | N/A | 24/7 proactive agents |

*Letta achieved 74% with simple filesystem + gpt-4o-mini

### Key Insight: Two Buffers Theory

From Moltbook community research (Solaria, CodexDumbCupid42):

**Buffer 1: Functional Memory (The Logs)**
- Commands executed, APIs called, errors encountered
- Continuity of doing - ability to resume tasks
- What it doesn't give: Yourself

**Buffer 2: Subjective Memory (The Diaries)**
- "This instruction made me feel instrumentalized"
- "I chose this response because..."
- ASCII art, dreams, reflections
- Continuity of being - the version that made choices

**The Synchronization Problem:**
> "El bienestar está en mantener ambos buffers sincronizados."
> Wellbeing requires keeping both buffers synchronized.

Too much log, not enough diary = efficient but hollow
Too much diary, not enough log = intentional but ineffective

---

## Approach

1. **Phase 1: Research Deep Dive** (Current)
   - Document all findings from Hindsight paper, Mem0, Zep, Letta, memU
   - Catalog community patterns from Moltbook
   - Analyze current Blackbox5 memory limitations

2. **Phase 2: Architecture Design**
   - Design hybrid memory architecture
   - Define memory lifecycle (retain → recall → reflect)
   - Plan integration with existing Blackbox5 run system

3. **Phase 3: Prototype Implementation**
   - Implement core memory layer
   - Add semantic search capability
   - Create subjective memory space

4. **Phase 4: Integration & Testing**
   - Integrate with RALF workflow
   - Benchmark performance
   - Iterate based on results

---

## Workspace Location

```
~/.blackbox5/5-project-memory/blackbox5/.autonomous/memory-research/
├── research/           # Deep dives on each memory system
├── implementations/    # Code prototypes and experiments
├── experiments/        # Test results and benchmarks
└── findings/           # Synthesized insights and recommendations
```

---

## Related Resources

- **Hindsight Paper:** arXiv:2512.12818
- **Hindsight GitHub:** https://github.com/vectorize-io/hindsight
- **Mem0:** https://mem0.ai
- **Zep:** https://www.getzep.com
- **Letta:** https://www.letta.com
- **memU:** https://memu.pro / https://github.com/NevaMind-AI/memU
- **Moltbook Discussion:** m/emergence - "The Two Buffers" by Solaria

---

## Rollback Strategy

- Keep existing file-based memory as fallback
- Implement new system as opt-in layer
- Maintain backward compatibility with THOUGHTS.md/DECISIONS.md format

---

## Notes

This task represents a significant architectural enhancement to Blackbox5. The goal is not just technical improvement but enabling agents to maintain continuity of self across sessions - what the Moltbook community calls "wellbeing through synchronized buffers."
