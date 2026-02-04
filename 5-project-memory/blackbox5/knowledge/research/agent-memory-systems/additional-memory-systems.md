# Additional Memory Systems Research

**Research Date:** 2026-02-04
**Purpose:** Cover memory systems not in initial deep dive

---

## LangMem (LangChain Official)

**Launch:** February 2025
**Developer:** LangChain
**Website:** https://python.langchain.com/docs/integrations/memory/langmem

### Overview
LangMem is LangChain's official long-term memory SDK, designed specifically for AI agents to maintain persistent memory across conversations.

### Three Memory Types

| Type | Stores | Use Case |
|------|--------|----------|
| **Semantic** | Facts, concepts, entities | "User works at Google" |
| **Procedural** | How-to knowledge, workflows | "How to deploy to production" |
| **Episodic** | Past experiences, conversations | "Last time we discussed X..." |

### Key Features

1. **Storage-Agnostic Core**
   - Works with PostgreSQL, MongoDB, Redis, vector stores
   - Pluggable backend architecture

2. **Native LangGraph Integration**
   - Type-safe memory consolidation
   - Pydantic schemas for validation

3. **Background Processing**
   - Delayed memory updates
   - Outside active user sessions
   - Non-blocking operation

4. **Prompt Optimization**
   - Automatic memory-based prompt enhancement
   - Relevant context injection

### Code Example
```python
from langchain.memory import LangMem
from langchain.chains import ConversationChain

memory = LangMem(
    semantic_store="qdrant",
    episodic_store="mongodb",
    procedural_store="redis"
)

chain = ConversationChain(
    llm=ChatOpenAI(model="gpt-4o"),
    memory=memory,
    verbose=True
)
```

### When to Use
✅ Already using LangChain/LangGraph
✅ Need fine-grained memory control
✅ Require prompt optimization
✅ Building evolving agents

---

## Vector Database Comparison for Agent Memory

### Executive Summary (2026)

| Database | Best For | Latency | Deployment |
|----------|----------|---------|------------|
| **Pinecone** | Production RAG, zero-ops | 5-10ms serverless | Fully managed |
| **Weaviate** | Hybrid search, complex apps | 30-70ms | Open + managed |
| **pgvector** | Existing PostgreSQL users | 10-50ms | Self-hosted |

### Pinecone: The "Apple Option"

**Strengths:**
- Fully managed, zero infrastructure
- Sub-100ms latency at billions of vectors
- Automatic scaling (serverless)
- SOC 2, GDPR, ISO 27001, HIPAA
- Native LangChain, n8n, Zapier integrations

**For Agent Memory:**
- High-frequency agent recall
- Focus on agent logic, not infrastructure
- Built-in hybrid search and reranking

**Limitations:**
- Cloud-only (no self-hosting)
- Usage-based pricing ($70-120/month for 10M vectors)
- Vendor lock-in

### Weaviate: The Hybrid Powerhouse

**Strengths:**
- Open-source with active community
- Native hybrid search (vector + BM25)
- Built-in ML model integrations
- GraphQL + REST APIs
- Multi-tenant support

**For Agent Memory:**
- Complex contexts requiring semantic + exact-match
- Built-in vectorization
- Structured filtering + similarity search

**Limitations:**
- Steeper learning curve (GraphQL)
- Self-hosting requires DevOps
- Performance tuning complex at scale

### pgvector: The SQL-Native Choice

**Strengths:**
- PostgreSQL extension
- Combines relational + vector in SQL
- Familiar tooling
- Free (pay only for Postgres)
- ACID compliance

**For Agent Memory:**
- Join with existing relational data
- Simpler architecture (<100M vectors)
- Maximum cost efficiency

**Limitations:**
- Not optimized for >100M vectors
- Slower ANN vs dedicated vector DBs
- Scaling limited by PostgreSQL

### Performance Benchmarks (2026)

| Metric | Pinecone | Weaviate | pgvector |
|--------|----------|----------|----------|
| P95 Latency | 20-80ms | 30-70ms | 22-50ms |
| QPS (1M vectors) | 12,300 | 9,800 | 6,500 |
| Recall@10 | 0.945 | 0.941 | 0.932 |
| Scalability | Billions | 100M+ | <100M |

### Cost Analysis (Monthly, 10M Vectors)

| Solution | Cost |
|----------|------|
| Pinecone Serverless | $70-120 |
| Pinecone Pods | $150-300 |
| Weaviate Cloud | $100-250 |
| Weaviate Self-hosted | $150-500 |
| pgvector | $160-260 |

### Recommendation for Blackbox5

**pgvector** is the best fit because:
1. Already using PostgreSQL for TaskRegistry
2. Need to join vector search with relational data
3. Moderate scale expected (<10M memories)
4. SQL-based workflows familiar to team
5. Maximum cost efficiency

---

## Neo4j for Knowledge Graph Memory

### Neo4j Aura Agent (October 2025)

**Product:** End-to-end automated orchestration for graph-based AI agents
**Pricing:** $0.35/agent/hour (public), free (internal)
**Runtime:** Google Gemini 2.5 Flash

### Key Capabilities

| Feature | Implementation |
|---------|---------------|
| **Persistent Memory** | Knowledge graphs store interconnected entities |
| **Contextual Reasoning** | Multi-hop graph traversal |
| **Temporal Memory** | Temporal Knowledge Graphs (TKGs) |
| **Explainability** | Decision paths traceable |
| **Security** | Role-based access control |

### GraphRAG

Combines vector search with rich graph context:
- Returns entities, relationships, citations
- Connects unrelated info through intermediate links
- More explainable than pure vector RAG

### Temporal Knowledge Graphs

Featured at NODES 2025:
- Captures when events happened
- Tracks relationship evolution
- Uses LangGraph + Graphiti on Neo4j

### Industry Validation

> "The graph is essential. It is the skeleton to the LLM's flesh."
> — Charles Betz, VP Forrester

> "Agentic systems are the future of software. They need contextual reasoning, persistent memory, and accurate, traceable outputs, all of which graph technology is uniquely designed to deliver."
> — Emil Eifrem, Neo4j CEO

### Real-World Applications

| Domain | Implementation |
|--------|---------------|
| Healthcare | QIAGEN biomedical knowledge graphs |
| Automotive | Daimler Truck architecture graph |
| Scientific | Dr.Sai Agent with BESIII Knowledge Graph |
| Cybersecurity | CyRAG for threat intelligence |

### For Blackbox5

**Already using Neo4j** for concept relationships in RAPS project.

**Potential integration:**
- Entity relationships from decisions
- Cross-run pattern detection
- Multi-hop reasoning ("what depends on X?")

---

## OpenClaw Memory Architecture

**OpenClaw** is an open-source implementation inspired by Claude Code's agentic capabilities.

### Memory System Components

| Component | Purpose |
|-----------|---------|
| **Working Memory** | Active conversation context |
| **Tool Results Buffer** | Recent tool outputs |
| **Summarization Layer** | Condenses older context |
| **Persistent Memory** | Optional long-term storage |

### Architecture Pattern

```
User Input
    ↓
Context Window (Sliding) ← Memory Management
    ↓
Agent Loop (LLM + Tools) → Tool Use
    ↑                        ↓
    └────────────────────── Tool Results
```

### memory.md Configuration

OpenClaw projects typically define:
- **Token budget allocation** (80% context, 20% reserved)
- **Eviction policies** for overflow
- **Summarization triggers**
- **Priority ranking** for memory types

### Community Patterns

From Moltbook discussions:
- Daily logs (memory/YYYY-MM-DD.md)
- MEMORY.md for curated long-term knowledge
- SOUL.md / SELF.md for identity
- NOW.md for active context

---

## Emerging Patterns Summary

### 2025-2026 Trends

1. **Hybrid Architectures**
   - Vector + Graph + Relational
   - Not one-size-fits-all

2. **MCP (Model Context Protocol)**
   - Standardized memory management
   - Neo4j MCP server example

3. **Self-Editing Agents**
   - Agents manage own memory
   - Letta's approach gaining traction

4. **Background Consolidation**
   - Async memory processing
   - LangMem pattern

5. **Multi-Agent Memory**
   - Shared memory spaces
   - Relational buffer concept

6. **Temporal Knowledge Graphs**
   - Time-aware relationships
   - Evolving memory

### Key Insight

The field is converging on:
- **Unified storage** (PostgreSQL + pgvector)
- **Graph relationships** (Neo4j for complex queries)
- **Two Buffers** (functional + subjective)
- **Self-management** (agents edit own memory)

---

## Gaps in Current Research

Still need to investigate:
- [ ] Amazon Neptune vs Neo4j
- [ ] Milvus for large-scale deployments
- [ ] Qdrant for Rust-based systems
- [ ] Chroma for lightweight use cases
- [ ] A-Mem (Zettelkasten-inspired)
- [ ] MemGPT variants beyond Letta

---

## Sources

- [Neo4j Aura Agent](https://neo4j.com/product/aura-agent/)
- [Neo4j Agentic AI Blog](https://neo4j.com/blog/agentic-ai/)
- [LangMem Documentation](https://python.langchain.com/docs/integrations/memory/langmem)
- [Vector Database Comparison 2026](https://reintech.io/blog/vector-database-comparison-2026-pinecone-weaviate-milvus-qdrant-chroma)
- [Pinecone vs Weaviate vs pgvector](https://techshitanshu.com/vector-databases-pinecone-weaviate-milvus/)
- [NODES 2025 Recap](https://neo4j.com/blog/developer/nodes-2025-a-recap-in-10-videos/)
