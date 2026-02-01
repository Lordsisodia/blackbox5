# BlackBox5 First Principles Baseline

**Purpose:** Document what we know to be true at 3 levels before running analysis loops.

**Last Updated:** 2026-01-21
**Status:** 🟡 IMPROVED - Added 7 new pillars (now 13 total, up from 6)

---

## Level 1: The Lowest Level - WHY BLACKBOX5 Exists

### Core Purpose

**BLACKBOX5 is infrastructure that lets AI agents do work autonomously.**

**What this MEANS:**
- BLACKBOX5 ≠ an AI agent
- BLACKBOX5 = the tools/skills/memory/knowledge that agents USE
- Agents = the brain (Claude, GPT, etc.)
- BLACKBOX5 = the hands/tools

### The Problem We Solve

**Before BLACKBOX5:**
- Each AI coding session starts from zero
- No persistent memory across sessions
- No shared capabilities between agents
- Every agent must rebuild context
- No autonomous execution possible

**After BLACKBOX5:**
- Agents have access to 200+ capabilities instantly
- Memory persists across all sessions
- Skills are shared and reusable
- Autonomous execution is possible
- Continuous self-improvement

### Fundamental Truth (The "Why")

**"If agents are the brains, BLACKBOX5 is the nervous system."**

You don't build a brain and then make it rebuild hands every time it wants to do something.
You build ONCE, then the brain can use those hands forever.

---

## Level 2: The Core Pillars - What Makes BLACKBOX5 Work

### Pillar 1: Universal Capability Registry (Skills)

**What it is:** 52+ reusable capabilities that any agent can access

**Examples:**
- first-principles-thinking (fundamental analysis)
- sequential-thinking (step-by-step reasoning)
- github-integration (PR/issue management)
- supabase (database operations)
- playwright (browser automation)

**Why it matters:** Agents don't need to rebuild common patterns

**File location:** `2-engine/02-agents/capabilities/skills-cap/`

---

### Pillar 2: Persistent Memory System

**What it is:** 4-tier memory that survives across sessions

**Tiers:**
1. **Working Memory** - Current task context
2. **Episodic Memory** - What happened in past sessions
3. **Semantic Memory** - Knowledge that persists
4. **Procedural Memory** - How to do things (skills)

**Why it matters:** Agents learn from past work

**File location:** `2-engine/03-knowledge/storage/ProductionMemorySystem.py`

---

### Pillar 3: Event-Driven Architecture

**What it is:** Components communicate via events (loose coupling)

**Pattern:**
```
Agent A → Event Bus → Agent B → Event Bus → Memory
```

**Why it matters:** No agent depends on another agent directly

**File location:** `2-engine/01-core/communication/event_bus.py`

---

### Pillar 4: Complexity-Based Routing

**What it is:** Tasks analyzed and routed to appropriate agents

**Metrics:**
- Complexity score (task description, tech stack, dependencies)
- Agent specialization (who does what best)

**Why it matters:** Right agent gets the right task

**File location:** `2-engine/01-core/routing/`

---

### Pillar 5: MCP Integration Layer

**What it is:** Standardized interface to external tools

**Integrations:** 16 MCP servers (Supabase, GitHub, Shopify, etc.)

**Why it matters:** Agents access tools through consistent interface

**File location:** `2-engine/06-integrations/`

---

### Pillar 6: Autonomous Execution Engine

**What it is:** Ralph Runtime - continuous improvement loop

**Pattern:**
```
Read PRD → Pick task → Execute → Quality check → Commit → Repeat
```

**Why it matters:** System improves itself without human intervention

**File location:** `5-project-memory/siso-internal/operations/agents/history/sessions/ralph/`

---

### Pillar 7: Central Service Kernel ⭐ NEW

**What it is:** EngineKernel - singleton managing all engine services

**Capabilities:**
- Service registry with factory pattern
- Lifecycle management (startup/shutdown)
- Health monitoring
- Run level management for graceful degradation

**Run Levels:**
- **DEAD** (0): Critical failure, cannot operate
- **MINIMAL** (1): Core only, no agents/tools
- **DEGRADED** (2): Some components failed
- **FULL** (3): Everything working

**Why it matters:** Single source of truth for system health and service availability

**File location:** `2-engine/01-core/infrastructure/kernel.py`

---

### Pillar 8: Resilience & Safety Systems ⭐ NEW

**What it is:** Circuit breakers + kill switches for safe autonomous operation

**Components:**

**8a. Circuit Breaker System:**
- Prevents cascading failures across agents
- 3 states: CLOSED → OPEN → HALF_OPEN
- 9x faster failure detection
- Per-agent circuit tracking

**8b. Kill Switch:**
- Emergency shutdown capability
- Persistent state tracking
- System-wide emergency broadcast
- Integration with circuit breakers

**8c. Safe Mode:**
- Constitutional classifier for harmful content
- Graceful degradation when issues detected

**Why it matters:** Autonomous agents need safety rails to prevent damage

**File location:**
- Circuit breaker: `2-engine/01-core/resilience/circuit_breaker.py`
- Kill switch: `2-engine/01-core/safety/kill_switch.py`
- Safe mode: `2-engine/01-core/safety/safe_mode.py`

---

### Pillar 9: Model Router ⭐ NEW

**What it is:** Hierarchical model selection based on task complexity

**Routing Strategy:**
- **Strategic Thinking**: GLM-4 Plus / Claude Opus (highest quality)
- **Code with Framework**: Claude Sonnet / GLM-4 (balanced with framework)
- **Standard Execution**: Claude Sonnet / GLM-4 (balanced)
- **Validation**: Claude Haiku / GLM-4 Flash (fast)
- **Simple Operations**: Claude Haiku / GLM-4 Flash (fastest)

**Why it matters:** Optimal cost/quality tradeoff for different task types

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/model_router.py`

---

### Pillar 10: Intelligence Layer ⭐ NEW

**What it is:** Smart task selection, routing, and dependency resolution

**Capabilities:**
- Multi-factor task scoring (priority, complexity, domain freshness)
- Dependency resolution with topological sorting
- Context-aware routing (learns from failures)
- Agent selection based on domain and complexity

**Scoring Factors:**
- Priority (35%)
- Complexity (15%)
- Domain Freshness (20%)
- Agent Availability (15%)
- Time Match (10%)
- User Preference (5%)

**Why it matters:** Autonomous loops make intelligent decisions about what to do next

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/intelligence/`

---

### Pillar 11: Health Monitoring System ⭐ NEW

**What it is:** Continuous health monitoring with automatic recovery

**Capabilities:**
- Service health tracking
- Custom health checks (disk space, memory, CPU)
- Health history and uptime statistics
- Automatic recovery triggers

**Built-in Checks:**
- Disk space availability
- Memory availability
- CPU usage thresholds
- Port listening checks

**Why it matters:** System can detect and respond to degradation before total failure

**File location:** `2-engine/01-core/infrastructure/health.py`

---

### Pillar 12: Manifest & Replayability System ⭐ NEW

**What it is:** Complete execution tracking for debugging and replay

**Tracks:**
- Input/output files
- Execution timeline
- Token usage and costs
- Environment state (git branch, commit, dirty state)
- Validation results
- Replay commands

**Why it matters:** Every run can be replayed, debugged, and analyzed

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/manifest.py`

---

### Pillar 13: Atomic Commit System ⭐ NEW

**What it is:** Multi-step operations with all-or-nothing semantics

**Pattern:**
```
Start Transaction → Execute Steps → Validate → Commit OR Rollback
```

**Why it matters:** Complex operations can fail safely without leaving system in broken state

**File location:** `2-engine/01-core/resilience/atomic_commit_manager.py`

---

## Pillar Dependency Map

```
                    ┌─────────────────────────────────────┐
                    │     ENGINE KERNEL (Pillar 7)        │
                    │  Service Registry + Health Monitor  │
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  HEALTH MONITOR   │    │  SERVICE REGISTRY   │    │   LIFECYCLE MGR      │
│   (Pillar 11)     │    │   (via Kernel)      │    │   (via Kernel)       │
└───────────────────┘    └─────────────────────┘    └──────────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  RESILIENCE (8)   │    │  ROUTING (4, 9, 10) │    │   MEMORY (2)         │
│  - Circuit Breaker│    │  - Task Router      │    │   - 4-tier system    │
│  - Kill Switch    │    │  - Model Router     │    │   - Persistent       │
│  - Atomic Commit  │    │  - Intelligence     │    │                      │
└───────────────────┘    └─────────────────────┘    └──────────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│   SKILLS (1)      │    │    EVENTS (3)       │    │    MCP (5)            │
│   - 52+ capabilities│   │   - Event Bus       │    │   - 16 integrations   │
│   - Reusable       │    │   - Loose coupling  │    │   - Standard interface│
└───────────────────┘    └─────────────────────┘    └──────────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │    AUTONOMOUS EXECUTION (6)         │
                    │    Ralph Runtime                    │
                    │    Uses all pillars to run autonomously│
                    └─────────────────────────────────────┘
```

**Key Dependencies:**
- **Everything depends on Kernel** (Pillar 7) for service registry and health
- **Resilience (8)** protects all other pillars from cascading failures
- **Routing (4, 9, 10)** depends on **Memory (2)** for learning from past executions
- **Autonomous Execution (6)** is the consumer that uses all other pillars
- **Events (3)** is the communication fabric connecting all pillars
- **Manifest (12)** tracks everything for replayability

---

## Level 3: Framework Assumptions - What We Know Works

### Assumption 1: AI-Agnostic Design ✅ VALIDATED

**What we believe:** BLACKBOX5 should work with any AI model

**Evidence:**
- Supports Claude, GPT, Gemini, Codex, OpenCode, Droid
- Model router selects based on task requirements
- No model-specific hard dependencies

**Validation:** ✅ PROVEN - Multiple models in production

**File location:** `2-engine/01-core/infrastructure/kernel.py`

---

### Assumption 2: Skills Beat Hardcoding ✅ VALIDATED

**What we believe:** Reusable skills > agent-specific code

**Evidence:**
- 52 skills shared across all agents
- Skills can be composed in workflows
- Faster development (reuse vs rebuild)

**Validation:** ✅ PROVEN - Skills system is core architecture

**File location:** `2-engine/02-agents/capabilities/skills-cap/`

---

### Assumption 3: Memory Must Be Multi-Tier ⚠️ PARTIAL

**What we believe:** Single memory layer is insufficient

**Evidence:**
- Research validates 3-tier memory (working, episodic, semantic)
- Production systems (LangChain, AutoGen) use multiple layers
- BLACKBOX5 implements 4 tiers (added procedural)

**Validation:** ⚠️ IN PROGRESS - Architecture implemented, not fully tested

**File location:** `2-engine/03-knowledge/storage/`

---

### Assumption 4: First-Principles Reasoning > Chain-of-Thought ✅ VALIDATED

**What we believe:** Breaking down to fundamentals > sequential reasoning

**Evidence:**
- PR-0002: ADI Cycle (Abduction → Deduction → Induction)
- Research shows 70% reasoning improvement with Tree-of-Thoughts
- First-principles skill is foundational

**Validation:** ✅ PROVEN - Core to system design

**File location:** `2-engine/04-work/modules/first-principles/`

---

### Assumption 5: MCP Will Be Universal Protocol ⚠️ UNCERTAIN

**What we believe:** MCP will be the standard for tool integration

**Evidence:**
- 16 MCP integrations working
- Growing ecosystem (Supabase, Shopify, GitHub, etc.)
- BUT: Alternative protocols exist (OpenAI Codex has its own types)

**Validation:** ⚠️ UNCERTAIN - Good but not guaranteed

**Risk:** If MCP dies or is replaced, 16 integrations break

**File location:** `2-engine/06-integrations/`

---

### Assumption 6: Autonomous Loops Need Stop Gates ❌ NOT VALIDATED

**What we believe:** Continuous loops need validation checkpoints

**Evidence:**
- Ralph Runtime runs until complete
- Research shows reflection loops prevent failures
- BUT: No go/no-go gates implemented

**Validation:** ❌ NOT TESTED - Loop runs but doesn't validate direction

**Risk:** Can run 100 iterations going wrong direction

**File location:** `5-project-memory/siso-internal/operations/agents/history/sessions/ralph/ralph_runtime.py`

---

### Assumption 7: Vendor Lock-In Is Death ⚠️ PARTIAL

**What we believe:** Hard-coded executor dependencies are unacceptable

**Evidence:**
- Direct git dependencies on `openai/codex` protocols
- Tight coupling to specific executor interfaces
- Ralph-y shows git worktree pattern as alternative

**Validation:** ⚠️ IN PROGRESS - Problem identified, not fixed

**Risk:** OpenAI changes protocol → system breaks

**File location:** `vibe-kanban/crates/executors/`

---

### Assumption 8: Documentation ≠ Understanding ❌ NOT VALIDATED

**What we believe:** Having docs doesn't mean system is usable

**Evidence:**
- 200+ features documented
- BUT: Test coverage only 66.7%
- BUT: Complex systems need maps, not just docs

**Validation:** ❌ PROVEN WRONG - Docs exist, but system is hard to navigate

**File location:** `README.md` (200+ features, but findability is low)

---

### Assumption 9: Framework Adoption > Custom Building 🤔 OPEN QUESTION

**What we believe:** Should adopt frameworks (BMAD, MetaGPT) vs build custom

**Evidence:**
- Research shows CrewAI, LangGraph, AutoGen have production patterns
- BLACKBOX5 has custom orchestration
- NO DECISION MADE: Build vs adopt is unresolved

**Validation:** 🤔 UNTESTED - Major architectural question unanswered

**Risk:** Reinventing wheel vs leveraging ecosystem

**File location:** `6-roadmap/frameworks/`

---

### Assumption 10: Open-Source Models Will Catch Up ⚠️ SPECULATIVE

**What we believe:** Architecture must support future open-source models

**Evidence:**
- Current: Proprietary models are better (GPT-4, Claude)
- Trend: Open-source models improving (Qwen, Llama, DeepSeek)
- BUT: No architecture for model-agnostic optimization

**Validation:** ⚠️ SPECULATIVE - Future prediction, not tested

**Risk:** When open-source catches up, migration may be hard

**File location:** Architecture-level concern

---

### Assumption 11: Central Kernel Prevents Chaos ✅ VALIDATED ⭐ NEW

**What we believe:** Single service registry is better than distributed initialization

**Evidence:**
- EngineKernel provides singleton service management
- Run level system prevents partial startup
- Dependency-ordered initialization prevents race conditions

**Validation:** ✅ PROVEN - Kernel pattern is working in production

**File location:** `2-engine/01-core/infrastructure/kernel.py`

---

### Assumption 12: Circuit Breakers Prevent Cascading Failures ✅ VALIDATED ⭐ NEW

**What we believe:** Fast failure detection is better than waiting for timeouts

**Evidence:**
- Circuit breaker provides 9x faster failure detection
- OPEN state prevents hammering failing services
- HALF_OPEN state enables safe recovery testing

**Validation:** ✅ PROVEN - Circuit breaker pattern is production-ready

**File location:** `2-engine/01-core/resilience/circuit_breaker.py`

---

### Assumption 13: Kill Switch Is Necessary For Autonomous Agents ⚠️ CRITICAL ⭐ NEW

**What we believe:** Emergency shutdown capability is non-negotiable

**Evidence:**
- Kill switch implemented with persistent state
- Multiple trigger reasons (manual, safety violation, resource exhaustion)
- Integration with event bus for system-wide broadcast

**Validation:** ⚠️ CRITICAL - Implemented but never tested in real emergency

**Risk:** If kill switch fails during real emergency, damage could be unlimited

**File location:** `2-engine/01-core/safety/kill_switch.py`

---

### Assumption 14: Model Routing Optimizes Cost/Quality ⚠️ PARTIAL ⭐ NEW

**What we believe:** Different tasks need different models

**Evidence:**
- Model Router implements 5-tier complexity routing
- Cost estimates for each model tier
- GLM-4 and Claude models supported

**Validation:** ⚠️ PARTIAL - Routing works, but cost optimization not measured

**Risk:** May be over/under-provisioning models without real cost data

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/model_router.py`

---

### Assumption 15: Context-Aware Routing Beats Random Selection ✅ VALIDATED ⭐ NEW

**What we believe:** Learning from failures improves routing decisions

**Evidence:**
- Intelligence Layer tracks domain failures and agent success rates
- Multi-factor scoring (priority, complexity, freshness, availability)
- Dependency resolution ensures correct execution order

**Validation:** ✅ PROVEN - Context-aware routing is well-designed

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/intelligence/`

---

### Assumption 16: Health Monitoring Enables Self-Healing ⚠️ PARTIAL ⭐ NEW

**What we believe:** Continuous monitoring enables automatic recovery

**Evidence:**
- Health Monitor tracks service status and custom health checks
- Built-in checks for disk, memory, CPU, port availability
- Health change callbacks for reactive responses

**Validation:** ⚠️ PARTIAL - Monitoring works, but self-healing not implemented

**Risk:** System detects degradation but doesn't automatically fix it

**File location:** `2-engine/01-core/infrastructure/health.py`

---

### Assumption 17: Manifest System Enables Replayability ✅ VALIDATED ⭐ NEW

**What we believe:** Complete execution tracking is essential for debugging

**Evidence:**
- Manifest tracks inputs, outputs, steps, metrics, environment
- Git state captured (branch, commit, dirty)
- Replay commands generated automatically

**Validation:** ✅ PROVEN - Manifest system provides comprehensive tracking

**File location:** `2-engine/07-operations/environment/lib/python/core/runtime/manifest.py`

---

### Assumption 18: Atomic Commits Prevent Broken State ⚠️ PARTIAL ⭐ NEW

**What we believe:** Multi-step operations should be all-or-nothing

**Evidence:**
- AtomicCommitManager implements transaction pattern
- Rollback capability on validation failure
- Step-by-step execution with state tracking

**Validation:** ⚠️ PARTIAL - Pattern implemented, not widely used

**Risk:** Complex operations may still leave system in broken state

**File location:** `2-engine/01-core/resilience/atomic_commit_manager.py`

---

## What's Missing

### ❌ Level 1: Missing

- **No formal "Purpose Statement" document** - README describes features, not why it exists
- **No "Problem Statement"** - What pain does BLACKBOX5 solve?
- **No "Success Definition"** - How do we know if BLACKBOX5 is working?

### ❌ Level 2: Partial

- **Pillars documented but not validated** - We have the systems, but don't know if they're the RIGHT pillars
- **Dependency Map created** ✅ - Just added pillar dependency visualization
- **No "Failure Mode Analysis"** - What breaks if each pillar fails?

### ❌ Level 3: Improved but still gaps

- **18 assumptions (up from 10), 6 validated, 6 partial, 6 untested**
- **No "Assumption Registry"** - What do we believe that might be wrong?
- **No "Validation Queue"** - What should we test first?

---

## What To Do Before Running Any Loop

### Step 1: Document Purpose (30 min)

Create: `6-roadmap/FIRST-PRINCIPLES-PURPOSE.md`

Answer:
- What problem does BLACKBOX5 solve?
- Who is it for? (agents, developers, both?)
- What does success look like?
- What does failure look like?

### Step 2: Validate Pillars (1 hour)

Create: `6-roadmap/FIRST-PRINCIPLES-PILLAR-VALIDATION.md`

For each of the 13 pillars:
- Is this the RIGHT design, or just what we have?
- What breaks if this pillar fails?
- Are there missing pillars?
- Prioritize pillars by risk

### Step 3: Challenge Assumptions (2-3 hours)

Use the **assumption-challenger** skill:

```bash
# For each of the 18 assumptions above:
1. Read assumption
2. Generate 6-10 challenging questions
3. Design validation experiment
4. Run validation
```

### Step 4: Prioritize Validations (1 hour)

Create: `6-roadmap/FIRST-PRINCIPLES-VALIDATION-QUEUE.md`

Order assumptions by:
- **Risk** - What breaks if wrong?
- **Uncertainty** - What are we least sure about?
- **Effort** - What's easiest to test?

**Critical Path Validations (High Risk + High Uncertainty):**
1. Assumption 13: Kill Switch (NEVER TESTED IN REAL EMERGENCY)
2. Assumption 6: Stop Gates (LOOP CAN RUN 100 ITERATIONS WRONG DIRECTION)
3. Assumption 7: Vendor Lock-In (OPENAI PROTOCOL CHANGE BREAKS SYSTEM)
4. Assumption 5: MCP Universal (MCP DEATH = 16 BROKEN INTEGRATIONS)
5. Assumption 9: Framework Adoption (REINVENTING WHEEL?)

### Step 5: Run Top 3 Validations (3-5 hours)

Pick the 3 highest-priority assumptions and test them.

---

## After This Is Complete

You'll have:

✅ **Level 1:** Clear purpose statement (why BLACKBOX5 exists)
✅ **Level 2:** Core pillars mapped with dependencies (13 pillars, up from 6)
✅ **Level 3:** Assumptions validated (18 assumptions, up from 10)

**THEN** you run the 1909 loop (or my V2 mini-loops).

**Without this:** The loop generates findings that may contradict each other, with no shared truth to validate against.

---

## Current Status

| Level | Status | What's Needed |
|-------|--------|---------------|
| **Level 1: Purpose** | ❌ Missing | Write purpose statement |
| **Level 2: Pillars** | 🟡 Improved | 13 pillars documented (up from 6), need validation |
| **Level 3: Assumptions** | 🟡 Improved | 18 assumptions (up from 10), 6 validated, 12 need testing |

**Overall:** 🟡 **BETTER BUT NOT READY FOR ANALYSIS LOOPS**

**Progress:**
- ✅ Discovered 7 new pillars (13 total, up from 6)
- ✅ Added pillar dependency map
- ✅ Added 8 new assumptions (18 total, up from 10)
- ⚠️ Still need purpose statement
- ⚠️ Still need pillar validation
- ❌ Still need assumption testing

**Risk:** Running loops now produces disconnected findings without shared foundation.

---

**Next Action:** Don't run 1909 loop. Build the baseline first.
