# TASK-AUTO-202602110834: Persistent Multi-Bot Infrastructure

**Status:** in_progress
**Priority:** CRITICAL
**Type:** system_architecture
**Category:** infrastructure
**Created:** 2026-02-11T08:34:11Z
**Agent:** main
**Estimated Effort:** 4-8 hours

## Problem Statement

Current autonomous system and OpenClaw sessions are transient - when a session ends, memory is lost. Need persistent multi-bot infrastructure with:

1. **Persistent chat windows** for different topics (dev, research, monitoring, etc.)
2. **Ability to spawn multiple agents simultaneously** across different topics
3. **Each bot has its own persistent memory** separate from session ephemeral memory
4. **Ability to send messages into any session** from any bot to coordinate work
5. **VPS resource capacity** to support multiple concurrent agents
6. **Bot registry and management** for dynamic bot coordination

## Current State

### Existing Infrastructure

**OpenClaw Gateway:**
- Running on VPS (77.42.66.40)
- Dashboard: http://127.0.0.1:18789/
- Multiple sessions available
- Session isolation supported

**BlackBox5:**
- Has agent orchestration system (bb5-orchestrator)
- Has agent memory system (AgentMemory.py)
- Has autonomous improvement system (autonomous.py)
- Current setup: 30-minute task runner using OpenClaw sessions

### Limitations Identified

- [ ] No persistent multi-bot infrastructure
- [ ] Sessions are ephemeral (memory lost on timeout)
- [ ] No coordinated spawning of multiple persistent bots
- [ ] No cross-session messaging between bots
- [ ] Each bot doesn't have its own persistent memory store
- [ ] No bot registry for management
- [ ] No UI console for bot control and monitoring

## Requirements

### Core Requirements

**1. Persistent Session Types**
   - **Main Bot:** SISO's primary interface, always available
   - **Specialist Bots:** Persistent agents for specific domains (dev, research, monitoring, etc.)
   - **Task Bot Agents:** Temporary agents spawned for specific tasks, auto-cleanup after completion

**2. Persistent Memory per Bot**
   - Each bot has its own memory store separate from session ephemeral context
   - Memory persists across session restarts
   - Bot can access its memory and reasoning history
   - Structured storage (key-value pairs, embeddings, summaries)

**3. Bot Capabilities**
   - **Spawn Agents:** Each bot can spawn sub-agents
   - **Cross-Session Messaging:** Any bot can send messages to any session
   - **Read/Write Memory:** Each bot manages its own memory
   - **Tool Access:** Full tool access based on bot role
   - **Topic Isolation:** Each bot operates in its topic context

**4. Infrastructure Support**
   - **Session Management:** Create persistent sessions (not ephemeral)
   - **Memory Backend:** Persistent storage (SQLite, file-based, or extend Agent Memory)
   - **Bot Registry:** Track which bots are active, their topics, capabilities
   - **Coordination Service:** Allow bots to discover and message each other
   - **UI/Management Console:** View all active bots, their sessions, memory usage
   - **Topic Channels:** Group and route messages by topic

## Proposed Architecture

### Bot System

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Bot Registry / Management                   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ Main Bot (SISO's primary interface, persistent)          ││
│  │ Specialist Bots (dev, research, monitoring, etc.)        ││
│  │ Task Agents (ephemeral, task-specific)                  ││
│  └────────────────────────────────────────────────────────────┘│
│                           ↓ ↓ ↓                                 │
│                           ↘ ↘ ↘                                   │
│              ┌────────────────────────────────────────────┐        │
│              │         Bot Memory Backend          │        │
│              │    (SQLite + Index)             │        │
│              │    Per-bot memory stores           │        │
│              └────────────────────────────────────────────┘        │
│                           ↓                                          │
└────────────────────────────────────────────────────────────────────────┘
└──────────────┬───────────────────────────────────────────────────────────────┘
              │
              ↓
        ┌───────────────────────────────────────────────────────┐
        │   OpenClaw Sessions / Coordination            │
        │  (Cross-session messaging, bot registry)        │
        │   Session Manager (create persistent sessions)    │
        │   Bot-to-bot communication protocol        │
        │   Agent Spawning (task-specific agents)        │
        └──────────────────────────────────────────────────────┘
              │
              ↓
        ┌───────────────────────────────────────────────────────────────┐
        │   Topic Channels & Routing                   │
        │   (Group bots by topic)                        │
        │   (Cross-topic bot communication)                 │
        └──────────────────────────────────────────────────────┘
              │
              ↓
        ┌───────────────────────────────────────────────────────────────┐
        │   UI / Management Console                      │
        │   (Bot list, bot console, session viewer,           │
        │   (Memory inspector, topic routing)                 │
        └───────────────────────────────────────────────────────────────┘
              │
              ↓
        ┌───────────────────────────────────────────────────────────────┐
        │   VPS: Development Environment                │
        │   (Dev bot, research bots, task agents)        │
        │   (Persistent storage, git, tools)                 │
        └──────────────────────────────────────────────────────┘
              │
              ↓
        ┌───────────────────────────────────────────────────────────────┐
        │   SISO (Human Operator)                       │
        │   (Accesses all systems, manages everything)       │
        └──────────────────────────────────────────────────────┘
```

### Implementation Plan

### Phase 1: Research & Design (Week 1)

**Goal:** Understand OpenClaw session system capabilities and design bot memory architecture

**Tasks:**
1. Review OpenClaw documentation for session persistence options
2. Research bot memory patterns and best practices
3. Design schema for bot registry
4. Design cross-session messaging protocol
5. Create detailed technical specification document

**Deliverables:**
- Technical specification document
- Architecture diagrams
- Data model for bot registry
- Protocol documentation for bot-to-bot communication
- Feasibility analysis for OpenClaw session persistence

**Success Criteria:**
- [ ] OpenClaw capabilities documented
- [ ] Bot memory architecture designed
- [ ] Feasibility confirmed or workarounds identified
- [ ] Technical spec complete and reviewed

**Estimated Effort:** 4 hours

### Phase 2: Core Infrastructure - Bot Registry & Memory (Week 2)

**Goal:** Implement bot registry and persistent memory system

**Tasks:**
1. Implement bot registry API (CRUD operations)
2. Design and implement bot memory database schema
3. Create bot session manager (persistent sessions)
4. Implement memory read/write API per bot
5. Build bot memory management console UI
6. Add indexing for fast memory queries

**Deliverables:**
- Bot registry service (REST API)
- Bot memory database (SQLite with full-text search)
- Bot memory management interface
- Persistent session manager
- Memory inspector UI

**Success Criteria:**
- [ ] Bot registry can track 10+ bots
- [ ] Each bot has persistent memory store
- [ ] Memory persists across session restarts
- [ ] Full-text search on bot memories
- [ ] Bot console for memory inspection

**Estimated Effort:** 8-12 hours

### Phase 3: Agent Spawning & Cross-Session Messaging (Week 3)

**Goal:** Enable specialized persistent bots and agent coordination

**Tasks:**
1. Implement bot spawning API with auto-cleanup
2. Create bot-to-bot communication protocol
3. Build session manager for spawning persistent bot sessions
4. Implement cross-session message router
5. Add agent lifecycle management (spawn, monitor, cleanup)
6. Build agent coordination console for main bot

**Deliverables:**
- Agent spawning service (API)
- Bot-to-bot communication system
- Session manager for persistent bots
- Cross-session message router
- Agent lifecycle manager
- Agent coordination console

**Success Criteria:**
- [ ] Persistent bots can be spawned dynamically
- [ ] Bots can send messages to each other
- [ ] Tasks can be assigned to specific bots
- [ ] Auto-cleanup of task agents after completion
- [ ] Agent lifecycle properly managed
- [ ] Cross-session messaging working

**Estimated Effort:** 12-16 hours

### Phase 4: Topic Channels & UI/Management Console (Week 4)

**Goal:** Build unified bot management interface

**Tasks:**
1. Implement topic-based bot routing
2. Build bot console for sending commands
3. Create session viewer for all bot sessions
4. Implement memory inspector for any bot
5. Build topic management interface
6. Create unified dashboard with all components

**Deliverables:**
- Topic router with channel management
- Bot console with command execution
- Session viewer showing all active sessions
- Memory inspector with search capabilities
- Topic management UI
- Unified dashboard linking all components

**Success Criteria:**
- [ ] Bots can be grouped by topic
- [ ] Messages routed by topic automatically
- [ ] Commands can be sent to specific bots
- [ ] All bot sessions visible in one place
- [ ] Memory of any bot can be inspected
- [ ] Topic channels can be managed via UI

**Estimated Effort:** 8-12 hours

### Phase 5: Integration & Deployment (Week 5)

**Goal:** Integrate all components and deploy to production

**Tasks:**
1. Integrate bot registry with session manager
2. Connect memory backend with all bots
3. Link cross-session messaging with all bots
4. Integrate topic channels with bot console
5. Deploy to OpenClaw environment
6. Performance testing and optimization
7. Documentation and training materials

**Deliverables:**
- Fully integrated multi-bot system
- Production-ready deployment
- API documentation
- Bot operator guide
- System architecture documentation
- Performance benchmarks

**Success Criteria:**
- [ ] All components integrated and working together
- [ ] System deployed to VPS
- [ ] Performance meets requirements (10+ concurrent bots)
- [ ] Documentation complete
- [ ] SISO can access and control system
- [ ] System scalable to 50+ bots

**Estimated Effort:** 8-12 hours

## Success Criteria

- [ ] Multiple persistent bots can run simultaneously
- [ ] Each bot has its own persistent memory
- [ ] Bots can spawn sub-agents for tasks
- [ ] Cross-session messaging working
- [ ] Bot registry allows dynamic management
- [ ] UI console provides full visibility and control
- [ ] Memory persists across session restarts
- [ ] System can handle 10+ concurrent agents
- [ ] Architecture is scalable and maintainable
- [ ] Documentation complete

## Risks & Mitigations

**Risk:** OpenClaw may not support persistent sessions as required
**Mitigation:** Research thoroughly, implement workarounds if needed

**Risk:** Managing multiple persistent bots is complex
**Mitigation:** Start with 2 bots, scale gradually

**Risk:** Memory storage requirements (10+ bots)
**Mitigation:** Use SQLite with proper indexing, implement cleanup

**Risk:** Bot-to-bot messaging could be abused
**Mitigation:** Implement authentication, rate limits, message logging

**Risk:** Building this is a large project (5 phases, 40+ hours)
**Mitigation:** Break down into phases, deliver incrementally

## Next Steps

### Immediate
- [ ] Review OpenClaw session system capabilities
- [ ] Determine if persistent sessions are possible
- [ ] If not, find workarounds or alternative approaches
- [ ] Begin Phase 1 research

### Week 1
- [ ] Start research and design phase
- [ ] Review OpenClaw documentation
- [ ] Create technical specifications
- [ ] Get approval on architecture from SISO

### Week 2-5
- [ ] Implement phases sequentially
- [ ] Test each phase thoroughly
- [ ] Deploy incrementally
- [ ] Gather feedback and iterate

### Long Term
- [ ] Scale to 10+ concurrent bots
- [ ] Add more specialized bots (testing, security, documentation)
- [ ] Implement advanced features (bot learning, collaborative problem solving)
- [ ] Build self-healing and auto-recovery capabilities

## Timeline

**Phase 1 (Research & Design):** 1 week
**Phase 2 (Core Infrastructure):** 2 weeks
**Phase 3 (Agent Spawning):** 3-4 weeks
**Phase 4 (Topic Channels):** 2 weeks
**Phase 5 (Integration):** 2-4 weeks

**Total:** 10-14 weeks

**Critical Path:** Phases 1-2 must be completed before agent spawning

## Budget & Resources

**VPS Capacity:**
- Storage: ~20GB available (should be sufficient)
- Memory: 2GB RAM (should handle 10+ bots)
- CPU: 2 cores (may need optimization for 10+ bots)
- Network: 100GB/month (monitor usage)

**OpenClaw API Costs:**
- Estimated: 10M tokens/month for base system
- Additional: 5M tokens/month for coordination features
- Total: 15M tokens/month

**Development Effort:**
- 320-560 hours (40-70 person-weeks)
- 2-5 developers if working full-time
- Or 6-12 months if part-time

---

**Task created successfully in tasks/active/TASK-AUTO-202602110834/task.md**
