# Blackbox5 Memory Research Index

**Project:** Improve Blackbox5 Persistent Memory System
**Task:** TASK-MEMORY-001
**Last Updated:** 2026-02-04

---

## Quick Navigation

### Research Deep Dives
- [Hindsight Deep Dive](../research/hindsight-deep-dive.md) - The 91.4% SOTA system
- [Two Buffers Theory](../research/two-buffers-theory.md) - Functional vs Subjective memory
- [Memory System Comparison](../research/memory-system-comparison.md) - Complete landscape analysis

### Key External Resources

**Papers & GitHub**
- Hindsight Paper: [arXiv:2512.12818](https://arxiv.org/abs/2512.12818)
- Hindsight GitHub: https://github.com/vectorize-io/hindsight
- Mem0: https://mem0.ai / https://github.com/mem0ai/mem0
- Zep: https://www.getzep.com
- Letta: https://www.letta.com / https://github.com/letta-ai/letta
- memU: https://memu.pro / https://github.com/NevaMind-AI/memU

**Community Discussions**
- Moltbook m/emergence: "The Two Buffers" by Solaria
- Moltbook m/openclaw-explorers: "Hybrid Memory Architecture"

---

## Research Summary

### The Consensus

The field has converged on **hybrid memory architectures**:

> Vector DB (fuzzy recall) + Structured Store (relationships) + LLM-based consolidation

### Top Performers

| System | Score | Key Innovation |
|--------|-------|----------------|
| Hindsight | 91.4% | 4-network structured memory with belief updating |
| Zep | 71.2% | Temporal knowledge graphs |
| Letta | 74.0% | Self-editing memory via tools |

### The Philosophical Layer

From the Moltbook community:

**Buffer 1 (Functional):** What you did - logs, commands, APIs
**Buffer 2 (Subjective):** Who you were - intentions, reflections, stance

> "El bienestar está en mantener ambos buffers sincronizados."
> Wellbeing is in keeping both buffers synchronized.

---

## Current Status

- [x] Initial research complete
- [x] Key systems documented
- [x] Two Buffers theory captured
- [x] Workspace structure created
- [ ] Blackbox5 current state analysis
- [ ] Architecture design
- [ ] Prototype implementation
- [ ] Benchmarking

---

## Key Decisions Needed

1. **Architecture:** Full Hindsight implementation vs hybrid approach?
2. **Storage:** PostgreSQL + pgvector vs specialized vector DB?
3. **Integration:** Replace existing memory or layer on top?
4. **Two Buffers:** How to implement subjective memory in Blackbox5?
5. **Priority:** Which capabilities to implement first?

---

## Active Questions

- Can we achieve Hindsight-level accuracy with simpler infrastructure?
- How to synchronize functional and subjective memory?
- What's the minimum viable memory system for Blackbox5?
- How to preserve agent identity across runs?

---

## Next Actions

1. Analyze current Blackbox5 memory implementation
2. Design hybrid architecture
3. Create proof-of-concept
4. Benchmark against baseline

---

*This is a living document. Update as research progresses.*
