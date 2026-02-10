# BlackBox5 Scribe Knowledge Base

*Last updated: 2026-02-10*
*Maintained by: BlackBox5 Scribe Agent*

---

## System Documentation

### BlackBox5 Scribe Agent
- **Created:** 2026-02-10
- **Purpose:** Document all BlackBox5 tasks and work
- **Skills File:** `/root/.openclaw/skills/blackbox5-scribe/SKILL.md`
- **Architecture Doc:** `/opt/blackbox5/5-project-memory/blackbox5/knowledge/scribe-architecture.md`
- **Status:** Operational

#### Key Capabilities
1. Monitor tasks in `/opt/blackbox5/5-project-memory/blackbox5/tasks/`
2. Track task statuses (pending → in_progress → completed)
3. Document decisions with rationale
4. Maintain searchable knowledge base
5. Generate daily summaries

#### Invocation Pattern
```
Invoke blackbox5-scribe: [action description]
```

---

---

## Documented Tasks

### Active Tasks
*None yet - waiting for task documentation*

### Recently Completed Tasks
*None yet*

---

## Decision Log

### 2026-02-10
- **Initial Setup Decision:** Created Scribe agent architecture with SKILL.md, knowledge base, and daily summary template
- **Rationale:** Centralized documentation ensures all BlackBox5 work is tracked and learnings are preserved

---

## What Works

### Project Management
- Use `/opt/blackbox5/5-project-memory/blackbox5/tasks/` for task tracking
- Task statuses: `pending`, `in_progress`, `completed`
- Task format should include: ID, title, description, status, assignee, due date, notes

### Communication
- Redis at 77.42.66.40:6379 for pub/sub messaging
- NATS at 77.42.66.40:4222 for JetStream with guaranteed delivery

### Security
- API keys stored in `/opt/blackbox5/.secrets`
- Never share API keys in chat

---

## What Doesn't Work

*None documented yet*

---

## Lessons Learned

### Documentation
- Start documenting from the beginning - catching up later is painful
- Keep decision rationale linked to outcomes
- Record failures alongside successes - both are valuable

### Architecture
- Knowledge base should be centralized and searchable
- Scribe agent should be invoked automatically for key events
- Daily summaries help maintain context over time

---

## Patterns

### Task Creation Pattern
1. Create task file in `/opt/blackbox5/5-project-memory/blackbox5/tasks/`
2. Invoke scribe to document task creation
3. Update status as work progresses
4. Invoke scribe for status changes
5. Invoke scribe on completion

### Decision Recording Pattern
1. State the decision clearly
2. Document alternatives considered
3. Explain rationale for chosen path
4. Record outcome when available
5. Update knowledge base

---

## Anti-Patterns

*None documented yet*

---

## Configuration Reference

### BlackBox5 System
- **Location:** `/opt/blackbox5/`
- **Commands:** `bb5 goal:list`, `bb5 plan:list`, `bb5 task:list`
- **Other Agents:** claude-mac (laptop), moltbot-macmini-01 (Mac Mini)

### Network
- **Redis:** 77.42.66.40:6379
- **NATS:** 77.42.66.40:4222
- **VPS Host:** 77.42.66.40

### Transcription
- **Script:** `/opt/blackbox5/transcribe_audio.py`
- **Model:** Whisper (OpenAI)
- **Cost:** $0.006/minute
- **Key Location:** `/opt/blackbox5/.secrets`

---

## Glossary

- **BlackBox5:** The AI agent system running on the VPS
- **Scribe:** Documentation agent that tracks and records all BlackBox5 work
- **bb5:** Command-line interface for BlackBox5 operations
- **VPS:** Virtual Private Server at 77.42.66.40

---

## Search Tags

To search this knowledge base:
- `#task` - Task-related information
- `#decision` - Decision records and rationale
- `#pattern` - Successful patterns to follow
- `#antipattern` - Things to avoid
- `#config` - Configuration and setup details
- `#lesson` - Lessons learned

---

*This knowledge base is maintained by the BlackBox5 Scribe Agent. Last invocation: N/A*
