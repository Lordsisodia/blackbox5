# Multi-Bot Infrastructure Task - 2026-02-11

**Status:** in_progress
**Priority:** CRITICAL
**Type:** system_architecture
**Category:** infrastructure
**Created:** 2026-02-11T08:44:00Z
**Agent:** main
**Estimated Effort:** 8-12 hours

## Problem Statement

Current OpenClaw sessions are ephemeral - when session ends, all context and memory are lost. SISO needs a persistent multi-bot infrastructure with:

1. **Persistent chat windows** for different topics (dev, research, monitoring, etc.)
2. **Concurrent agent sessions** - Multiple bots working simultaneously on different tasks
3. **Each bot has its own persistent memory** - Separate from session ephemeral memory
4. **Ability to send messages into any session** from any bot to coordinate work
5. **UI to manage multiple sessions** - Switch between bots, see activity
6. **VPS resource capacity** to support multiple concurrent bots

## Requirements Analysis

### What OpenClaw Already Has

**OpenClaw Gateway:**
- Running on VPS (77.42.66.40)
- Dashboard: http://127.0.0.1:18789/
- Multiple sessions available
- Session isolation supported

**BlackBox5:**
- Has agent orchestration system (bb5-orchestrator)
- Has agent memory system (AgentMemory.py)
- Has autonomous improvement system (autonomous.py)
- Has task management system

### What's Missing

**❌ No persistent sessions** - Sessions are ephemeral
**❌ No concurrent bot coordination** - Each session is independent
**❌ No cross-session messaging** - Can't message between sessions
**❌ No bot registry** - Can't track multiple specialized bots
**❌ No session management UI** - Can't organize multiple bots
**❌ No visual session indicators** - Can't see which bots are working

## Implementation Plan

### Phase 1: Understand OpenClaw Session System (Week 1)

**Tasks:**
1. Review OpenClaw documentation for session persistence options
2. Research how sessionKey parameter works in WebSocket events
3. Understand state management in OpenClaw
4. Test if persistent sessions can be created via RPC

**Deliverables:**
- Research findings document
- Understanding of capabilities and limitations
- Feasibility analysis

**Estimated Effort:** 1 week

### Phase 2: Design Bot Memory System (Week 2)

**Tasks:**
1. Design persistent memory architecture per bot
2. Choose storage backend (SQLite, file-based, or extend Agent Memory)
3. Design schema (bot_id, memories, sessions, embeddings, metadata)
4. Design memory read/write APIs
5. Design search and retrieval capabilities

**Deliverables:**
- Memory architecture document
- Database schema design
- API specification
- Implementation prototype

**Estimated Effort:** 2 weeks

### Phase 3: Implement Bot Registry & Session Manager (Week 2-3)

**Tasks:**
1. Implement bot registration API
2. Implement session management (create, list, switch sessions)
3. Create session manager service
4. Implement cross-session messaging protocol
5. Build bot health monitoring

**Deliverables:**
- Bot registry service (REST API)
- Session manager service
- Message routing service
- Health check service
- Bot tracking dashboard

**Estimated Effort:** 3-4 weeks

### Phase 4: Build Multi-Agent Session UI (Week 3-4)

**Tasks:**
1. Extend OpenClaw session dropdown to support multiple sessions
2. Add "New Session" button to chat interface
3. Create session list sidebar component
4. Implement quick session switching (keyboard shortcuts)
5. Add active session indicators (● for running, ○ for idle)
6. Add session organization features (group by topic, rename sessions)
7. Build session viewer to see all bot activities

**Deliverables:**
- Session switcher component
- Session list sidebar
- Active session indicators
- Session management console
- Visual session activity tracker

**Estimated Effort:** 3-4 weeks

### Phase 5: Integrate & Deploy (Week 5)

**Tasks:**
1. Integrate bot registry with OpenClaw sessions
2. Connect memory backend to sessions
3. Enable cross-session messaging between bots
4. Deploy session manager service
5. Deploy UI components to OpenClaw
6. Test concurrent bot execution
7. Performance testing

**Deliverables:**
- Full multi-bot system deployed
- Multiple persistent bots running
- UI working with session switching
- Cross-session messaging functional
- Performance benchmarks

**Estimated Effort:** 2 weeks

## Success Criteria

- [ ] Multiple persistent sessions can be created from UI
- [ ] Each session can spawn sub-agents for tasks
- [ ] Each session maintains its own persistent memory
- [ ] Sessions can send messages to each other for coordination
- [ ] Session list sidebar shows all active bots
- [ ] Active session indicators show which bots are working
- [ ] Quick keyboard shortcuts switch between sessions
- [ ] Cross-session messaging working
- [ ] System can handle 10+ concurrent agents
- [ ] Memory persists across session restarts
- [ ] UI console for bot management
- [ ] System deployed and tested

## Risks & Mitigations

**Risk:** OpenClaw may not support persistent sessions natively
**Mitigation:** Research thoroughly, implement workarounds if needed

**Risk:** Managing multiple concurrent bots is complex
**Mitigation:** Start with 2-3 bots, scale gradually

**Risk:** Memory storage requirements (10+ bots)
**Mitigation:** Use efficient storage (SQLite with indexing), implement cleanup

## Current State

**OpenClaw:** Has session system, but sessions are ephemeral by default
**VPS:** Resources available, but no multi-bot system deployed yet
**UI:** Basic chat interface, no session management

## Next Steps

### Option A: Full Implementation
- Execute all 5 phases sequentially
- Total time: 10-14 weeks
- Complete persistent multi-bot infrastructure

### Option B: MVP Approach
- Focus on core features first:
  - Ability to create persistent sessions
  - Each bot can have its own memory (extend Agent Memory)
  - Basic session switching between 2-3 bots
  - Simple session list sidebar
- Estimated time: 3-4 weeks

### Option C: Incremental UI Improvements
- Start with just session switching UI (Phase 4 tasks 1-4)
- Get core functionality working first
- Add more advanced features incrementally
- Estimated time: 2 weeks

## Recommendation

**Start with MVP Approach (Option B)** to get quick wins:

**Phase 1 (Week 1):** Just research OpenClaw session capabilities - 1 week

**Phase 2 (Week 2-3):** Skip complex memory system initially - use extended Agent Memory per bot

**Phase 4 (Week 4):** Build basic session switching UI first:
- Session dropdown with multiple sessions
- "New Session" button
- Simple active indicators
- Keyboard shortcuts (Ctrl+1, Ctrl+2, etc.)
- Estimated time: 1-2 weeks

**Phase 5 (Week 5):** Deploy and test core functionality

This approach gives you working multi-bot system faster while allowing us to learn and iterate.

---

**Ready to proceed with Option B (MVP approach)?** 

Or would you prefer the full 10-14 week implementation plan?
