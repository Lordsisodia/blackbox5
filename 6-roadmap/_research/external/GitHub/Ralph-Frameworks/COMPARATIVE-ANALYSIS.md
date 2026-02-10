# Ralph Frameworks - Comparative Analysis for BB5 Integration

**Date:** 2026-02-10
**Purpose:** Compare 4 Ralph-related frameworks and recommend integration strategies for BB5
**Analyst:** BB5 Research Team

---

## Executive Summary

| Framework | Language | Maturity | Key Differentiator | BB5 Priority |
|-----------|----------|----------|-------------------|--------------|
| **frankbria/ralph-claude-code** | Bash | v0.11.4, 484 tests | Circuit breaker, rate limiting, session mgmt | HIGH |
| **snarktank/ralph** | Bash | Stable | Simplicity, AGENTS.md pattern, fresh context | MEDIUM |
| **michaelshimeles/ralphy** | TypeScript/Bun | v4.7.2, npm published | Git worktree parallel execution | **HIGHEST** |
| **mikeyobrien/ralph-orchestrator** | Rust | Production-ready | Hat-based pub/sub, multi-backend, web dashboard | HIGH |

**Recommendation:** BB5 should adopt patterns from all four frameworks, with immediate focus on Ralphy's git worktree parallel execution and frankbria's safety mechanisms.

---

## Detailed Comparison Matrix

### 1. Architecture Patterns

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Core Pattern** | Single-agent loop | Single-agent loop | Multi-agent parallel | Hat-based pub/sub |
| **Execution** | Sequential | Sequential | Parallel (worktrees) | Sequential (per hat) |
| **State Management** | JSON files | JSON + text | YAML/JSON config | JSONL + markdown |
| **Communication** | File-based | File-based | Git-based | Event pub/sub |
| **Language** | Bash | Bash | TypeScript/Bun | Rust |

### 2. Autonomous Loop Mechanisms

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Loop Control** | Circuit breaker (3-state FSM) | Simple for loop | Retry with backoff | Event-driven |
| **Exit Detection** | Dual-condition gate | <promise>COMPLETE | Task completion | LOOP_COMPLETE promise |
| **Rate Limiting** | 100 calls/hour | None | Configurable | Cost limits |
| **Session Mgmt** | 24h expiry, resume | None | Per-task isolation | Per-loop tracking |
| **Max Iterations** | Configurable | Default 10 | Configurable | 50-100 default |

### 3. Agent Orchestration

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Multi-Agent** | ❌ | ❌ | ✅ (parallel) | ✅ (hats) |
| **Agent Types** | Single Claude | Single AI | Multi-engine | Hat personas |
| **Specialization** | ❌ | ❌ | ❌ | ✅ (builder, reviewer, etc.) |
| **Communication** | ❌ | ❌ | ❌ | Pub/sub events |
| **Parallel Exec** | ❌ | ❌ | ✅ Git worktrees | ✅ Git worktrees |

### 4. Task Management

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Task Format** | Markdown checklist | JSON (prd.json) | Markdown/YAML/JSON | JSONL |
| **Prioritization** | Manual (fix_plan.md) | Priority field | Priority + parallel groups | Priority 1-5 |
| **Dependencies** | ❌ | Manual ordering | Parallel groups | blocked_by field |
| **Dynamic Tasks** | ❌ | ❌ | ❌ | ✅ |
| **Task Sources** | beads, GitHub, PRD | prd.json | PRD, GitHub Issues, YAML | tasks.jsonl |

### 5. Integration with Claude Code

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Primary Backend** | Claude Code | Amp/Claude | Claude (default) | Claude (primary) |
| **Multi-Backend** | ❌ | ✅ (Amp/Claude) | ✅ (8 engines) | ✅ (7+ engines) |
| **Session Resume** | ✅ --resume | ❌ | ❌ | ❌ |
| **Output Format** | JSON/text | Text | Stream JSON | JSONL events |
| **Skills Integration** | ❌ | ✅ | ❌ | ✅ |

### 6. Safety & Reliability

| Feature | frankbria | snarktank | michaelshimeles | mikeyobrien |
|---------|-----------|-----------|-----------------|-------------|
| **Circuit Breaker** | ✅ 3-state | ❌ | ❌ | ❌ |
| **Rate Limiting** | ✅ Hourly quota | ❌ | ❌ | ✅ Cost limits |
| **Retry Logic** | Basic | None | Exponential backoff | Configurable |
| **Error Recovery** | Auto-reset | Manual | Deferred tasks | Consecutive failure limit |
| **Stuck Detection** | ✅ Test-only loops | ❌ | ❌ | ✅ Loop thrashing |

### 7. Observability

| Feature | frankbria | snarktank | snarktank | mikeyobrien |
|---------|-----------|-----------|-----------|-------------|
| **Logging** | JSON status files | progress.txt | Console + files | JSONL events |
| **Monitoring** | tmux dashboard | ❌ | ❌ | Web dashboard |
| **Metrics** | Call counting | ❌ | Telemetry | Comprehensive |
| **Debugging** | Response analysis | ❌ | Worktree preservation | Diagnostics collection |

---

## Strengths by Framework

### frankbria/ralph-claude-code
1. **Production-Ready Safety** - Circuit breaker, rate limiting, permission handling
2. **Intelligent Exit Detection** - Dual-condition gate prevents premature exits
3. **Session Management** - Persistent sessions with 24h expiry
4. **Live Monitoring** - tmux dashboard with real-time updates
5. **Comprehensive Testing** - 484 tests, 100% pass rate

### snarktank/ralph
1. **Simplicity** - Single bash script, minimal dependencies
2. **AGENTS.md Pattern** - Excellent for preserving learnings
3. **Fresh Context** - Each iteration starts clean
4. **Tool Agnostic** - Works with Amp or Claude
5. **Skill Ecosystem** - PRD generation and conversion skills

### michaelshimeles/ralphy
1. **Git Worktree Parallel Execution** - True 3-5x speedup on parallelizable tasks
2. **Multi-Engine Support** - 8 AI engines with unified interface
3. **Flexible Task Sources** - Markdown, YAML, JSON, GitHub Issues
4. **Sandbox Mode** - Lightweight isolation for large repos
5. **Merge Conflict Resolution** - AI-assisted conflict resolution

### mikeyobrien/ralph-orchestrator
1. **Sophisticated Event Architecture** - Pub/sub with hatless coordinator
2. **Hat-Based Specialization** - Builder, reviewer, researcher personas
3. **Multi-Backend Flexibility** - Per-hat backend configuration
4. **Memory System** - Persistent learning with token budget
5. **Web Dashboard** - Full-stack monitoring interface
6. **Human-in-the-Loop** - Telegram integration (RObot)

---

## Weaknesses by Framework

### frankbria/ralph-claude-code
- Single-agent only
- No distributed execution
- Flat task checklist (no DAG)
- No database backend
- Bash limitations (cross-platform)

### snarktank/ralph
- No parallel execution
- No agent specialization
- No dynamic planning
- Limited error recovery
- No monitoring dashboard

### michaelshimeles/ralphy
- Node.js/Bun dependency
- No inter-agent communication
- Automatic merge can be risky
- No persistent agent state
- Limited observability

### mikeyobrien/ralph-orchestrator
- Rust complexity (steep learning curve)
- Backend dependency (requires CLI tools)
- Git-centric (less suitable for non-git)
- No native parallelism within loops
- YAML can become verbose

---

## BB5 Integration Recommendations

### Priority 0 (Immediate - Week 1-2)

#### 1. Git Worktree Parallel Execution (from Ralphy)
**Why:** BB5 already has research and prototype; 3-5x speedup potential
**Integration:** Port Ralphy's TypeScript worktree manager to Python
**Effort:** Medium
**Risk:** Low (feature flag, gradual rollout)

```python
# BB5 adaptation
class GitWorktreeManager:
    def create_agent_worktree(self, task, agent_num):
        branch_name = f"bb5/agent-{agent_num}-{task.slug}"
        worktree_dir = f".bb5-worktrees/agent-{agent_num}"
        # Use gitpython or subprocess
```

#### 2. Circuit Breaker Pattern (from frankbria)
**Why:** Prevents runaway loops, essential for autonomous systems
**Integration:** Port bash implementation to Python/TypeScript
**Effort:** Low
**Risk:** Very Low

```python
class CircuitBreaker:
    states = ['CLOSED', 'HALF_OPEN', 'OPEN']
    # Triggers: no progress, same error, permission denials
    # Auto-recovery with cooldown timer
```

### Priority 1 (Short-term - Week 3-4)

#### 3. Response Analysis Framework (from frankbria)
**Why:** Structured exit detection, progress tracking
**Integration:** Adapt for BB5's agent communication format
**Effort:** Medium

#### 4. Memory System (from mikeyobrien)
**Why:** Persistent learning across sessions
**Integration:** Integrate into BB5's learning layer
**Effort:** Low

```yaml
# Memory types
- Pattern: Reusable code patterns
- Decision: Architecture decisions
- Fix: Bug fixes and solutions
- Context: Project-specific context
```

#### 5. AGENTS.md Convention (from snarktank)
**Why:** Excellent for preserving learnings across sessions
**Integration:** Add to BB5 documentation standards
**Effort:** Very Low

### Priority 2 (Medium-term - Week 5-8)

#### 6. Hat-Based Agent Specialization (from mikeyobrien)
**Why:** Specialized agents for different tasks
**Integration:** Extend BB5 agent definitions
**Effort:** Medium

```yaml
# BB5 agent hats
- builder: Code implementation
- reviewer: PR review
- tester: Validation
- documenter: Documentation
- researcher: External research
```

#### 7. Event Pub/Sub System (from mikeyobrien)
**Why:** Decoupled agent communication
**Integration:** Message bus for agent teams
**Effort:** Medium

#### 8. Multi-Engine Support (from Ralphy/mikeyobrien)
**Why:** Flexibility, cost optimization, different perspectives
**Integration:** Abstract AIEngine interface
**Effort:** Medium

### Priority 3 (Long-term - Week 9-12)

#### 9. Web Dashboard (from mikeyobrien)
**Why:** Visual monitoring and management
**Integration:** Extend existing BB5 dashboard
**Effort:** High

#### 10. Human-in-the-Loop Protocol (from mikeyobrien)
**Why:** Human guidance without breaking loop
**Integration:** Telegram/Slack integration
**Effort:** Medium

#### 11. Task Dependency DAG (from mikeyobrien)
**Why:** Automatic dependency resolution
**Integration:** Extend existing task system
**Effort:** Medium

---

## Integration Risk Assessment

| Feature | Risk Level | Mitigation |
|---------|------------|------------|
| Git worktrees | Low | Feature flags, gradual rollout |
| Circuit breaker | Very Low | Well-tested pattern |
| Memory system | Low | Incremental adoption |
| Hat system | Medium | Start with 2-3 hats |
| Event pub/sub | Medium | Maintain backward compatibility |
| Multi-engine | Low | Claude remains default |
| Web dashboard | Medium | Separate deployment |

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Port git worktree manager from Ralphy
- [ ] Implement circuit breaker pattern
- [ ] Add feature flags for new components
- [ ] Test with single-agent scenarios

### Phase 2: Safety & Memory (Weeks 3-4)
- [ ] Integrate response analysis framework
- [ ] Add memory system to learning layer
- [ ] Adopt AGENTS.md convention
- [ ] Enhance error recovery

### Phase 3: Multi-Agent (Weeks 5-6)
- [ ] Implement parallel batch processing
- [ ] Add merge phase with conflict detection
- [ ] Test with multi-agent scenarios
- [ ] Performance benchmarking

### Phase 4: Specialization (Weeks 7-8)
- [ ] Define BB5 hat system
- [ ] Implement event pub/sub
- [ ] Add multi-engine support
- [ ] Testing and documentation

### Phase 5: Observability (Weeks 9-10)
- [ ] Enhance dashboard
- [ ] Add metrics collection
- [ ] Implement alerting
- [ ] Create run history browser

### Phase 6: Advanced Features (Weeks 11-12)
- [ ] Human-in-the-loop protocol
- [ ] Task dependency DAG
- [ ] Resource scheduling
- [ ] Plugin system

---

## Key Architectural Decisions

### 1. Fresh Context vs. Persistent Context
**Decision:** Hybrid approach
- Use fresh context per iteration (like snarktank/mikeyobrien)
- Maintain persistent memory system (like mikeyobrien)
- Session resume for continuity (like frankbria)

### 2. Single-Agent vs. Multi-Agent
**Decision:** Multi-agent with coordination
- Ralph pattern: Single-agent sequential
- BB5 enhancement: Multi-agent parallel with worktrees
- Hat system for specialization (mikeyobrien)

### 3. File-Based vs. Database State
**Decision:** Tiered approach
- File-based for simple deployments (current)
- SQLite for 3-5 agents (short-term)
- Redis for 10+ agents (long-term)

### 4. Bash vs. Python/TypeScript
**Decision:** Python/TypeScript for core, bash for simple loops
- frankbria proves bash can work
- BB5 needs more sophistication
- Keep bash for simple fallback mode

---

## Conclusion

### What BB5 Should Adopt Immediately

1. **Ralphy's git worktree parallel execution** - Highest impact feature
2. **frankbria's circuit breaker** - Essential safety mechanism
3. **mikeyobrien's memory system** - Persistent learning
4. **snarktank's AGENTS.md pattern** - Documentation standard

### What Makes BB5 Unique

While adopting patterns from Ralph frameworks, BB5 should maintain its differentiation:

1. **Integration-First Approach** - Code must work with existing systems
2. **Documentation-Heavy** - THOUGHTS, DECISIONS, LEARNINGS, RESULTS
3. **Self-Improving** - Designed to improve itself recursively
4. **Rule-Based Activation** - 20+ auto-activation rules
5. **Multi-Loop Architecture** - Core, docs, maint, research loops

### Final Recommendation

**Study all four frameworks deeply, adopt patterns selectively, maintain BB5's unique philosophy.**

The Ralph ecosystem represents years of iteration on autonomous AI development. BB5 can leapfrog by adopting proven patterns while avoiding pitfalls each framework discovered.

**Timeline:** 12 weeks for full integration
**Priority order:** Safety → Parallelism → Specialization → Observability
**Risk level:** Low to Medium (all patterns are production-tested)

---

## References

- **frankbria/ralph-claude-code:** https://github.com/frankbria/ralph-claude-code
- **snarktank/ralph:** https://github.com/snarktank/ralph
- **michaelshimeles/ralphy:** https://github.com/michaelshimeles/ralphy
- **mikeyobrien/ralph-orchestrator:** https://github.com/mikeyobrien/ralph-orchestrator
- **BB5 Ralphy Research:** `6-roadmap/frameworks/ralphy-integration-analysis/`

---

*Analysis completed by BB5 Research Team*
*For questions or updates, see individual framework analysis documents in this directory*
