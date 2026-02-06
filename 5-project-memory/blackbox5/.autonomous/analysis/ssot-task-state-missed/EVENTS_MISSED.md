# SSOT Task State: What Scouts Missed - events.yaml Deep Dive

**Scout:** Architecture Analysis Agent (Follow-up)
**Date:** 2026-02-06
**Focus:** events.yaml data corruption

---

## Critical Finding: Severe Data Corruption in events.yaml

**File Size:** 5,265 lines
**Total Events:** 779 events
**Status:** CRITICALLY CORRUPTED

---

## 1. Malformed task_id Entries (CRITICAL)

Two events contain literal string `'task_id:'` instead of actual task IDs:

```yaml
Line 8:   task_id: 'task_id:'
Line 13:  task_id: 'task_id:'
```

**Impact:** Orphaned data points consuming storage without value.

---

## 2. Orphaned Events - No Corresponding Task Files (CRITICAL)

Events reference task IDs with NO task files:

| Task ID | Events | Directory Exists? |
|---------|--------|-------------------|
| TASK-1738375002 | 2 events | NO |
| TASK-TEST-001 | 1 event | NO |

**Cross-reference:**
- Active tasks: 129 directories
- Task IDs in events: Only 3 unique IDs

---

## 3. Duplicate Event Entries (HIGH)

Multiple events with identical timestamps:

| Lines | Event Type | Timestamp | Issue |
|-------|-----------|-----------|-------|
| 1606-1611 | agent_start | 2026-02-05T23:09:28+07:00 | Duplicate |
| 3208-3214 | agent_start | 2026-02-06T02:08:03+07:00 | Duplicate |
| 3300-3305 | agent_stop | 2026-02-06T02:10:17+07:00 | Duplicate |
| 3705-3711 | agent_start | 2026-02-06T03:52:46+07:00 | Duplicate |
| 4147-4152 | agent_stop | 2026-02-06T04:25:43+07:00 | Duplicate |

**Impact:** Race conditions or lack of idempotency in event logging.

---

## 4. Future Timestamps (CRITICAL)

**Current UTC:** 2026-02-05T23:28:20Z
**Events exist with timestamps up to:** 2026-02-06T06:04:59+07:00

When converted: 2026-02-06T06:04:59+07:00 = 2026-02-05T23:04:59Z

**Issue:** Events dated 2026-02-06 exist when current date is 2026-02-05.

**Possible causes:**
- System clock incorrect
- Events generated with future dates
- Timezone handling broken

---

## 5. Event Type Imbalance (HIGH)

**Event Distribution:**
```
452  agent_stop
316  agent_start
  7  started
  2  in_progress
  1  queue_refilled
  1  docs_modified
```

- **771 agent lifecycle events** (98.8%)
- **9 task-related events** (1.2%)

**Impact:** Event system failing to capture task state transitions.

---

## 6. Empty parent_task Fields (CRITICAL)

**99%+ of agent events have empty `parent_task`:**

```yaml
parent_task: ""
```

**Impact:**
- No correlation between agent activity and tasks
- Cannot track which task an agent was working on
- Agent-task relationship completely broken

---

## 7. Timestamp Format Inconsistency (MEDIUM)

Multiple formats used:

```yaml
Line 1:    timestamp: '2026-02-01T16:01:00Z'           # ISO 8601 UTC
Line 7:    timestamp: '2026-02-03T23:16:31+07:00'      # With offset
Line 55:   timestamp: 2026-02-03T21:40:32+0000         # No quotes
Line 1200: timestamp: "2026-02-05T23:10:35+07:00"      # Double quotes
```

---

## 8. Missing Task Status Transitions (CRITICAL)

**TASK-1738375000 events:**
```
2026-02-01T16:01:00Z - started
2026-02-03T23:17:33+07:00 - started (duplicate?)
2026-02-03T23:20:30+07:00 - started (duplicate?)
2026-02-03T23:21:15+07:00 - started (duplicate?)
2026-02-03T23:22:01+07:00 - in_progress
```

**Issues:**
1. Multiple `started` events (should only transition from pending)
2. No `completed`, `blocked`, or `failed` events
3. Task file shows `pending` but events claim `started` and `in_progress`

**SSOT VIOLATION:** Task file and event log disagree on state.

---

## 9. Event Flooding Pattern (HIGH)

**Example burst (2026-02-06 01:35):**
```
01:35:26 - agent_start
01:35:29 - agent_start
01:35:30 - agent_start
01:35:32 - agent_start
01:35:34 - agent_start
01:35:35 - agent_start AND agent_stop (same second)
01:35:37 - agent_start
01:35:38 - agent_start
01:35:41 - agent_start
01:35:45 - agent_start
01:35:50 - agent_start
01:35:52 - agent_start
01:35:55 - agent_start
```

**13 agent lifecycle events in 29 seconds** suggests:
- Rapid agent creation/destruction (crash loop)
- Hook misfiring
- Event logging capturing noise

---

## What Initial Scouts Missed

| Issue | Severity | Scouts Found? |
|-------|----------|---------------|
| Malformed task_id entries | CRITICAL | NO |
| Orphaned events for non-existent tasks | CRITICAL | NO |
| Future timestamps | CRITICAL | NO |
| Massive duplicate entries | HIGH | NO |
| Empty parent_task fields | CRITICAL | Partial |
| Event type imbalance | HIGH | Partial |
| SSOT violations (task vs events) | CRITICAL | NO |
| Event flooding pattern | HIGH | NO |
