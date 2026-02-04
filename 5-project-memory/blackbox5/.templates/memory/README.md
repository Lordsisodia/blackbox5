# Hindsight Memory Templates

**Location:** `.templates/memory/`
**Purpose:** Templates for the 4-network Hindsight memory architecture
**Version:** 1.0

---

## Overview

Hindsight's memory architecture uses 4 distinct networks to capture different types of knowledge:

| Network | File | Stores | Epistemic Type |
|---------|------|--------|----------------|
| **World (W)** | `FACTS.md` | Objective facts | "What is true?" |
| **Experience (B)** | `EXPERIENCES.md` | First-person actions | "What did I do?" |
| **Opinion (O)** | `OPINIONS.md` | Beliefs with confidence | "What do I believe?" |
| **Observation (S)** | `OBSERVATIONS.md` | Synthesized insights | "What does it mean?" |

---

## Quick Reference

### When to Use Each Template

**Use FACTS.md when:**
- You discover technical information
- A decision is made
- You identify entities or relationships
- You want to record objective truth

**Use EXPERIENCES.md when:**
- You complete significant work
- You learn something new
- You overcome a challenge
- You use tools or techniques

**Use OPINIONS.md when:**
- You form a belief
- You make a judgment
- Your confidence changes
- You develop preferences

**Use OBSERVATIONS.md when:**
- You notice patterns
- You synthesize insights
- You connect to past work
- Something surprises you

---

## Template Variables

All templates support these variables (auto-populated by RALF):

| Variable | Description | Example |
|----------|-------------|---------|
| `{{DATE}}` | Current date | 2026-02-04 |
| `{{TIME}}` | Current time | 14:30:00 |
| `{{TASK_ID}}` | Current task ID | TASK-001 |
| `{{SOURCE}}` | Source file path | tasks/active/TASK-001/task.md |
| `{{AGENT_TYPE}}` | Agent type (planner/executor/architect) | planner |

---

## File Structure

```
task-folder/
├── task.md              # Task definition (existing)
├── THOUGHTS.md          # Reasoning (existing)
├── DECISIONS.md         # Decision log (existing)
├── RESULTS.md           # Outcomes (existing)
├── FACTS.md             # World network (NEW)
├── EXPERIENCES.md       # Experience network (NEW)
├── OPINIONS.md          # Opinion network (NEW)
├── OBSERVATIONS.md      # Observation network (NEW)
└── metadata.yaml        # Structured metadata (existing)
```

---

## Integration with Existing Files

| Existing File | Maps To | Relationship |
|---------------|---------|--------------|
| `THOUGHTS.md` | `EXPERIENCES.md` | Thoughts → Actions taken |
| `DECISIONS.md` | `FACTS.md` + `OPINIONS.md` | Decisions → Facts + Rationale |
| `RESULTS.md` | `OBSERVATIONS.md` | Outcomes → Insights |
| `LEARNINGS.md` | `OBSERVATIONS.md` | Learnings → Synthesized insights |

---

## Usage Flow

### Manual Recording (During Task)

1. **Start task** - Templates auto-created by SessionStart hook
2. **During work** - Manually record to appropriate network:
   - Discover something → Add to `FACTS.md`
   - Take action → Add to `EXPERIENCES.md`
   - Form belief → Add to `OPINIONS.md`
   - Have insight → Add to `OBSERVATIONS.md`
3. **Complete task** - RETAIN operation extracts additional memories

### Automatic Extraction (On Task Completion)

```
Task Completion
    ↓
RETAIN Operation
    ↓
├─ Extract from THOUGHTS.md → EXPERIENCES.md
├─ Extract from DECISIONS.md → FACTS.md + OPINIONS.md
├─ Extract from RESULTS.md → OBSERVATIONS.md
└─ Generate embeddings → PostgreSQL
    ↓
Store in databases
├─ PostgreSQL + pgvector (semantic search)
└─ Neo4j (entity relationships)
```

---

## Best Practices

### Recording Memories

1. **Be specific** - Concrete details, not vague generalizations
2. **Include confidence** - How certain are you? (0.0-1.0)
3. **Link to evidence** - Cite sources, files, lines
4. **Use searchable language** - Think about how you'll find this later
5. **Record failures too** - What didn't work is as valuable as what did

### Cross-Referencing

Link between networks for richer context:

```markdown
# In OBSERVATIONS.md
**Evidence Base:**
- Facts: [F-003, F-007]
- Experiences: [E-002]
- Opinions: [O-001]
```

### Confidence Calibration

| Score | Meaning | When to Use |
|-------|---------|-------------|
| 0.9-1.0 | Very confident | Well-verified, multiple sources |
| 0.7-0.8 | Confident | Good evidence, some uncertainty |
| 0.5-0.6 | Tentative | Some evidence, needs verification |
| 0.3-0.4 | Uncertain | Weak evidence, speculative |
| 0.0-0.2 | Skeptical | Contradicted or disproven |

---

## Example: Complete Memory Record

### Scenario: Implementing Authentication

**FACTS.md:**
```markdown
### F-001: JWT Token Structure

**Category:** technical
**Confidence:** 0.95

**Statement:**
> JWT tokens consist of three parts: header.payload.signature

**Evidence:**
- Source: RFC 7519
- Implementation: auth/jwt.py:45
```

**EXPERIENCES.md:**
```markdown
### E-001: Implementing JWT Middleware

**Type:** implementation

**What I Did:**
> Created middleware to validate JWT tokens on each request

**Process:**
1. Parsed Authorization header
2. Verified signature with secret key
3. Checked expiration
4. Attached user to request context

**Outcome:**
- Result: Success
- Tests passing: 12/12
```

**OPINIONS.md:**
```markdown
### O-001: JWT vs Session Cookies

**Confidence:** 0.75
**Category:** technical

**Belief:**
> JWT is preferable for API authentication due to statelessness

**Rationale:**
- No server-side storage needed
- Easier horizontal scaling
- Better fit for microservices

**Counter-evidence:**
- Token revocation is harder
- Larger payload size
```

**OBSERVATIONS.md:**
```markdown
### S-001: Authentication Pattern

**Type:** pattern
**Confidence:** 0.85

**Insight:**
> Stateless authentication (JWT) works best for APIs,
> while session-based auth is better for server-rendered apps

**Synthesis:**
- From: F-001, E-001, O-001
- Pattern: Architecture drives auth choice
- Implication: Choose based on client type
```

---

## Integration with RECALL

When you need to recall memories:

```bash
# Search across all networks
bb5 memory:recall "authentication patterns"

# Search specific network
bb5 memory:facts "JWT"
bb5 memory:experiences "middleware"
bb5 memory:opinions "scaling"
bb5 memory:observations "pattern"

# Search with filters
bb5 memory:recall "database" --confidence ">0.8"
bb5 memory:recall "API" --since "2026-01-01"
```

---

## Backward Compatibility

Existing files remain unchanged:
- `THOUGHTS.md` - Continue using for reasoning
- `DECISIONS.md` - Continue using for decisions
- `RESULTS.md` - Continue using for outcomes

New memory files are **additive** - they extract and structure information from existing files, but don't replace them.

---

## Migration Path

### For Existing Tasks

1. RETAIN operation will extract memories from existing THOUGHTS.md/DECISIONS.md
2. Create FACTS.md/EXPERIENCES.md/OPINIONS.md/OBSERVATIONS.md automatically
3. Store in databases for search

### For New Tasks

1. Templates auto-populated on task creation
2. Fill in as you work
3. RETAIN extracts additional memories on completion

---

## References

- **Goal:** `goals/active/IG-008/`
- **Plan:** `plans/active/hindsight-memory-implementation/`
- **Research:** `knowledge/research/agent-memory-systems/`
- **Integration:** `plans/active/hindsight-memory-implementation/INTEGRATION.md`

---

*Part of Hindsight Memory Architecture for Blackbox5*
