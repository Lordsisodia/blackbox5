# Task Claim Hook - UX/Usability Review

**Review Date:** 2026-02-06
**Reviewer:** UX/Usability Expert
**Design Under Review:** /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/hook-research/TASK_CLAIM_HOOK_DESIGN.md
**Severity Scale:** CRITICAL | HIGH | MEDIUM | LOW

---

## Executive Summary

The TaskClaim hook design has **fundamental UX flaws** that will create significant friction for both users and agents. While the automation intent is good, the interface design assumes perfect knowledge, ignores discovery needs, and creates substantial documentation burden. The design needs major revision before implementation.

**Key Finding:** The design optimizes for the "happy path" (user knows exact task ID) but fails for the common case (user needs to browse, discover, or be guided to the right task).

---

## 1. USER EXPERIENCE ISSUES

### 1.1 Task ID Requirement - CRITICAL

**Problem:** The interface requires users to know the exact task ID (e.g., "TASK-001", "TASK-ARCH-016").

**Why This Fails:**
- Task IDs are not memorable (TASK-ARCH-016 vs TASK-ARCH-061)
- Users must navigate away to find the ID, then return to claim
- With 90+ tasks in queue, finding the right ID is cognitively expensive
- Violates the "don't make me think" principle

**Real-World Scenario:**
```
User: "I want to work on the hook system"
System: [crickets - no matching pattern]

User: "claim hook task"
System: [no match - requires exact ID]

User: [must run bb5 task:list, scan 90 tasks, find ID, then claim]
```

**Recommendation:** Support fuzzy matching, keyword search, or natural language task selection.

---

### 1.2 No Discovery Mechanism - CRITICAL

**Problem:** No way to browse or discover tasks before claiming.

**Current Flow:**
```
User → Knows task ID → Types "claim TASK-001" → Hook fires
```

**Missing Flow:**
```
User → Wants to see available tasks → ??? → Selects one → Hook fires
```

**Why This Matters:**
- 60 pending tasks in queue (per queue.yaml)
- User needs context to make informed claim decision
- No integration with priority scores, dependencies, or "quick wins"
- Queue has rich metadata (priority_score, blockedBy, effort) that's invisible

**Recommendation:** Add a "claim" command that shows interactive task browser with filters.

---

### 1.3 No Task Preview Before Commit - HIGH

**Problem:** Claiming is immediate and irreversible (no confirmation or preview).

**Current Behavior:**
1. User says "claim TASK-001"
2. Hook immediately creates run folder
3. Updates queue.yaml
4. Injects context

**What If:**
- User made a typo? (TASK-001 vs TASK-002)
- Task is already claimed by another agent?
- Task has unmet dependencies?
- User didn't realize it was a 120-minute task?

**Recommendation:** Show task summary and ask for confirmation before claiming.

---

### 1.4 No Visual Feedback on Claim - HIGH

**Problem:** Users receive only text context injection - no visual confirmation.

**Current Output:**
```
"Task Claimed: TASK-001 | Goal: IG-008 | Plan: PLAN-003 | Run: run-20260206-143200-TASK-001"
```

**What's Missing:**
- Visual indicator of claimed status
- Progress bar or status widget
- Easy way to see "what am I working on now?"
- No distinction between claimed vs just browsing

**Recommendation:** Add visual claim indicator and "current task" status command.

---

### 1.5 No Escape Hatch - MEDIUM

**Problem:** Once claimed, there's no clear way to "unclaim" or release a task.

**Scenarios:**
- User claimed wrong task
- User needs to switch to higher priority task
- Task is blocked by external dependency
- User realizes they don't have context to complete it

**Current Design:** No mention of task release mechanism.

**Recommendation:** Add explicit "release" or "unclaim" command with reason capture.

---

## 2. AGENT EXPERIENCE ISSUES

### 2.1 Context Injection Overload - CRITICAL

**Problem:** THOUGHTS.md template is too large and complex.

**Template Creates:**
- THOUGHTS.md (200+ lines with full hierarchy)
- DECISIONS.md
- ASSUMPTIONS.md
- LEARNINGS.md
- RESULTS.md
- timeline.yaml
- metadata.yaml

**Agent Cognitive Load:**
```
Agent receives:
- Full goal context (could be massive)
- Full plan context (could be massive)
- Full task context
- 7 empty files to manage
- Multiple templates to fill
```

**The Problem:**
- Agents will skip filling most files (documentation fatigue)
- Empty templates create guilt/noise
- Context window consumed by boilerplate
- No guidance on which files matter most

**Evidence from Queue:**
Looking at queue.yaml, there are already documentation drift issues:
- TASK-DOCU-025: "Fix Skill Metrics Documentation Drift"
- TASK-DOCU-034: "Fix Inconsistent Directory Structure Docs"

This suggests documentation burden is already a problem.

**Recommendation:**
- Start with ONLY THOUGHTS.md
- Add other files lazily (when first needed)
- Provide tiered template (minimal vs comprehensive)

---

### 2.2 No Mid-Session Task Switching - HIGH

**Problem:** Design assumes one task per session. No clean task switching.

**Scenario:**
```
Session Start:
  User: "claim TASK-001"
  [Hook creates run-20260206-143200-TASK-001/]

Mid-Session:
  User: "Actually, let me work on TASK-002 instead"
  [What happens?]
  - New run folder created?
  - Old run abandoned?
  - Queue shows both claimed?
```

**Current Design Gaps:**
- No "switch task" workflow
- No cleanup of abandoned runs
- No guidance on when to start new session vs switch

**Recommendation:** Add explicit task switch protocol with cleanup options.

---

### 2.3 Ambiguous Agent Role - MEDIUM

**Problem:** Design doesn't distinguish between agent types (planner vs executor).

**From queue.yaml, tasks have types:**
- architecture
- process
- skill
- infrastructure
- documentation
- development
- cleanup
- autonomous

**Questions:**
- Should a planner agent claim architecture tasks?
- Should an executor claim documentation tasks?
- Does the hook validate role-task fit?

**Current Design:** No role validation or guidance.

**Recommendation:** Add agent type detection and task suitability warnings.

---

### 2.4 No Progress Persistence Guidance - MEDIUM

**Problem:** Agent must manually track progress across files.

**Current Expectation:**
- Update THOUGHTS.md with progress
- Update DECISIONS.md with decisions
- Update LEARNINGS.md with insights
- Update queue.yaml with status
- Update task.md with completion

**Reality:** Agents will forget or be inconsistent.

**Recommendation:** Provide single "update progress" command that propagates to all relevant files.

---

## 3. WORKFLOW INTEGRATION ISSUES

### 3.1 Planner → Executor Handoff Gap - CRITICAL

**Problem:** No clear handoff mechanism from planner to executor.

**Current Design Flow:**
```
Planner: Creates task TASK-001
Executor: Claims task TASK-001
[Gap: How does planner signal "ready for execution"?]
```

**Missing:**
- Task state transitions (draft → ready → claimed → in_progress → done)
- Handoff documentation (what did planner intend?)
- Dependency resolution (are prerequisites met?)

**From Queue Analysis:**
Tasks have `blockedBy` field but no mechanism to check/unblock.

**Recommendation:** Add explicit handoff state and validation.

---

### 3.2 Assignment vs Claim Confusion - HIGH

**Problem:** Design conflates "claim" (self-assigned) with "assign" (delegated).

**Current Design:** Only supports claim (user-initiated)

**Missing Scenarios:**
- Planner assigns task to specific executor
- Auto-assignment based on agent capabilities
- Round-robin task distribution
- Urgent task escalation

**From Queue Data:**
```yaml
- id: "TASK-ARCH-016"
  status: "pending"
  blockedBy: ["TASK-ARCH-011"]
  blocks: ["TASK-ARCH-039", "TASK-PROC-008"]
```

When TASK-ARCH-011 completes, who claims TASK-ARCH-016?

**Recommendation:** Support both claim (pull) and assign (push) modes.

---

### 3.3 Subtask Handling - HIGH

**Problem:** No mention of subtasks in design.

**Evidence of Subtasks:**
Looking at task files, there are patterns suggesting subtasks:
- TASK-ARCH-001B (follows TASK-ARCH-001)
- TASK-ARCH-003B, 003C, 003D (phases of TASK-ARCH-003)

**Questions:**
- Can you claim a parent task?
- Do subtasks auto-create on parent claim?
- How do subtask completions roll up?

**Recommendation:** Define subtask claim rules and hierarchy behavior.

---

### 3.4 Dependency Awareness - MEDIUM

**Problem:** Hook doesn't check or surface dependencies.

**From Queue:**
```yaml
blocked_count: 52
ready_to_execute: 17
```

58% of tasks are blocked. Claiming a blocked task should at minimum warn the user.

**Current Design:** No dependency checking in Phase 2 (Context Loading).

**Recommendation:** Add dependency validation with override option.

---

### 3.5 Parallel Group Conflicts - MEDIUM

**Problem:** Queue has parallel groups but hook doesn't respect them.

**Queue Data:**
```yaml
parallel_groups:
  - wave_1: 28 tasks
  - wave_2: 24 tasks
  - sequential: 9 tasks
```

**Issue:** Nothing prevents claiming a wave_4 task when wave_1 tasks are pending.

**Recommendation:** Add parallel group validation or guidance.

---

## 4. DOCUMENTATION BURDEN ISSUES

### 4.1 File Proliferation - CRITICAL

**Problem:** Creates 7 files per task claim.

**Math:**
```
90 tasks × 7 files = 630 files
Plus run folders = exponential growth
```

**Current Files Created:**
1. THOUGHTS.md
2. DECISIONS.md
3. ASSUMPTIONS.md
4. LEARNINGS.md
5. RESULTS.md
6. timeline.yaml
7. metadata.yaml

**Evidence This Is Already a Problem:**
- TASK-PROC-024: "Remove Unused Task Template Files"
- TASK-DOCU-042: "Create Missing WORK-LOG.md and ACTIVE.md"

The system already has documentation management issues.

**Recommendation:**
- Create files lazily (only when first written)
- Consolidate into single TASK-LOG.md with sections
- Auto-generate metadata files (don't ask agents to fill)

---

### 4.2 THOUGHTS.md Template Too Complex - HIGH

**Current Template:** 70+ lines with 6 sections

**Sections:**
1. Goal Context (with nested structure)
2. Plan Context (with dependencies)
3. Task Context (with acceptance criteria)
4. Assumptions (empty placeholder)
5. Progress Log (empty placeholder)

**Agent Experience:**
```
Agent opens THOUGHTS.md:
- Sees wall of boilerplate
- Has to scroll to find where to write
- Unsure which sections are required
- Context window already 20% consumed
```

**Recommendation:**
- Start with minimal template (3 sections: Context, Plan, Progress)
- Use progressive disclosure (expand sections as needed)
- Provide inline guidance, not just placeholders

---

### 4.3 Empty File Problem - MEDIUM

**Problem:** Creating empty files that may never be filled.

**Files Often Left Empty:**
- DECISIONS.md (if no major decisions)
- ASSUMPTIONS.md (if assumptions documented inline)
- LEARNINGS.md (if agent forgets)

**Result:** Cluttered file system, false sense of documentation coverage.

**Recommendation:** Only create files on first write (lazy initialization).

---

### 4.4 Multiple Source of Truth - MEDIUM

**Problem:** Same information tracked in multiple places.

**Example - Task Status:**
- queue.yaml (claimed/completed)
- task.md (status field)
- metadata.yaml (created by hook)
- THOUGHTS.md (progress log)

**Risk:** Inconsistencies between files.

**Evidence:**
- TASK-ARCH-016 appears twice in queue.yaml with different statuses
- TASK-ARCH-015-status-lifecycle exists (suggesting status confusion)

**Recommendation:** Define single source of truth for each data type.

---

## 5. INTERFACE DESIGN ISSUES

### 5.1 Command Pattern Inconsistency - MEDIUM

**Problem:** Multiple ways to claim, no clear preferred method.

**Options in Design:**
1. Natural language: "claim TASK-001"
2. Natural language: "select task TASK-001"
3. Natural language: "work on TASK-001"
4. Explicit command: "/claim TASK-001"
5. bb5 CLI: "bb5 claim TASK-001"
6. File touch: "touch tasks/active/TASK-001/.claim-request"

**User Confusion:** Which should I use? Do they behave differently?

**Recommendation:** Standardize on ONE primary interface with alternatives documented.

---

### 5.2 No Progress Indication - MEDIUM

**Problem:** Long-running hook operations give no feedback.

**Phase 2 (Context Loading):**
- Load task.md
- Load plan.md
- Load goal.md
- Parse all three

**With large goals/plans, this could take seconds.**

**Current Design:** Silent until complete.

**Recommendation:** Add progress indicators for multi-file operations.

---

### 5.3 Error Handling UX - HIGH

**Problem:** Error cases not designed for user recovery.

**Current Error Handling:**
```python
except Exception as e:
    print(f"TaskClaim hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on error
```

**Silent Failures Possible:**
- Task doesn't exist → hook fails silently
- Task already claimed → no warning
- Permission denied → silent exit
- Hierarchy loading fails → partial context

**Recommendation:** Provide clear error messages with recovery suggestions.

---

## 6. RECOMMENDATIONS SUMMARY

### Must Fix Before Implementation

1. **Add fuzzy task matching** - Users can't be expected to memorize task IDs
2. **Reduce initial file creation** - Start with 1-2 files, not 7
3. **Add confirmation step** - Preview before claim
4. **Check dependencies** - Warn if claiming blocked task
5. **Add release mechanism** - Way to unclaim/switch tasks

### Should Fix Soon After

6. **Support task browsing** - Interactive selection interface
7. **Add role validation** - Match agent type to task type
8. **Lazy file creation** - Only create when first written
9. **Progress indicators** - Show what's happening during claim
10. **Standardize commands** - One clear primary interface

### Nice to Have

11. **Visual status indicator** - Show current task prominently
12. **Auto-save progress** - Don't rely on manual file updates
13. **Task recommendations** - Suggest next task based on priority/dependencies
14. **Handoff protocol** - Planner to executor transition
15. **Batch operations** - Claim multiple related tasks

---

## 7. REVISED USER FLOW (PROPOSED)

```
User: "bb5 claim"

System:
  ┌─────────────────────────────────────────┐
  │  Available Tasks (Ready to Execute)    │
  ├─────────────────────────────────────────┤
  │  1. TASK-ARCH-017 (30 min) - HIGH      │
  │     Fix blackbox.py directory refs     │
  │                                         │
  │  2. TASK-ARCH-003D (45 min) - HIGH     │
  │     SSOT Validate Phase                │
  │                                         │
  │  3. TASK-ARCH-005 (45 min) - HIGH      │
  │     Clean Up Empty Directories         │
  │                                         │
  │  [f]ilter  [s]earch  [b]rowse all      │
  └─────────────────────────────────────────┘

User: "1"

System:
  ┌─────────────────────────────────────────┐
  │  Claim TASK-ARCH-017?                  │
  ├─────────────────────────────────────────┤
  │  Title: Fix blackbox.py Non-Existent   │
  │         Directory References           │
  │                                         │
  │  Estimated: 30 minutes                 │
  │  Priority: HIGH (Score: 8.8)           │
  │  Dependencies: None (Ready)            │
  │                                         │
  │  Goal: IG-007 (System Architecture)    │
  │                                         │
  │  [c]laim  [v]iew details  [b]ack       │
  └─────────────────────────────────────────┘

User: "c"

System:
  "Claimed TASK-ARCH-017"
  "Run folder: runs/run-20260206-074312-TASK-ARCH-017/"
  "Created: THOUGHTS.md (other files created on first use)"
  ""
  "You're working on: Fix blackbox.py Non-Existent Directory References"
  "Part of: IG-007 - System Architecture Improvements"
  ""
  "Type 'bb5 status' anytime to see progress."
  "Type 'bb5 release' to unclaim this task."
```

---

## 8. CONCLUSION

The TaskClaim hook design has good automation intent but significant UX gaps. The core issues are:

1. **Task ID requirement** creates barrier to entry
2. **File proliferation** creates maintenance burden
3. **No discovery/browse** limits usability
4. **Missing error/recovery** paths create dead ends

**Recommendation:** Redesign with "progressive disclosure" principle:
- Start simple (claim by fuzzy match, one file)
- Add complexity only when needed (browse interface, full documentation)
- Always provide escape hatches (release, switch, cancel)

**Estimated UX Impact if Implemented As-Is:**
- User friction: HIGH (requires memorizing IDs)
- Agent friction: HIGH (7 files to manage)
- Documentation drift: HIGH (empty files, inconsistent updates)
- Abandonment rate: LIKELY HIGH

---

*Review completed. Recommend addressing CRITICAL and HIGH issues before implementation.*
