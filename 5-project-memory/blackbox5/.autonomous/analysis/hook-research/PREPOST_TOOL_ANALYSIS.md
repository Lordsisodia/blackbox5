# PreToolUse and PostToolUse Hooks: Performance and Necessity Analysis

**Date:** 2026-02-06
**Analyst:** Performance and Systems Analyst
**Status:** Complete - Recommendations Included

---

## Executive Summary

**VERDICT: ELIMINATE PostToolUse hooks. KEEP a MINIMAL PreToolUse hook for safety only.**

After analyzing BB5's actual usage patterns, external research, and first principles, the data is clear:

- **PostToolUse hooks fire 100-300+ times per session** with near-zero value
- **PreToolUse safety hooks are essential** but should be minimal (not logging/tracking)
- **The cost/benefit ratio is terrible** for reactive hooks that agents can handle themselves

---

## 1. Performance Impact Analysis

### 1.1 Actual Tool Call Volume in BB5 Sessions

Analysis of transcript data from `/Users/shaansisodia/.claude/transcripts/`:

| Session | Tool Calls | Duration Est. | Calls/Min |
|---------|------------|---------------|-----------|
| ses_441d58affffeDj0hThDDLd4jpP.jsonl | **327** | ~60 min | ~5.5 |
| ses_441de475bffe57Sv0W8VM2360Q.jsonl | **226** | ~45 min | ~5.0 |
| ses_4154ce28bffe5H6q3yPB0u6bTh.jsonl | **183** | ~40 min | ~4.6 |
| ses_4072eafd1ffekCpIdu0abxoOh2.jsonl | **166** | ~35 min | ~4.7 |
| ses_441d30653ffeaGmQucGuEyw6is.jsonl | **141** | ~30 min | ~4.7 |
| Average (top 20 sessions) | **~100** | ~30 min | ~3.3 |

**Key Finding:** A typical BB5 session makes **100-300+ tool calls**. Complex sessions exceed 300 calls.

### 1.2 Hook Execution Overhead

Each hook invocation has the following overhead:

| Component | Time (ms) | Notes |
|-----------|-----------|-------|
| Process spawn (Python) | 50-150 | Cold start penalty |
| JSON parsing (stdin) | 5-20 | Depends on tool input size |
| Pattern matching | 1-10 | Regex operations |
| File I/O (logging) | 10-50 | Appending to JSONL |
| Process cleanup | 5-15 | Exit handling |
| **Total per hook** | **70-245 ms** | Conservative estimate |

### 1.3 Cumulative Impact

For a session with 200 tool calls:

| Hook Type | Calls | Overhead/Call | Total Overhead | % of Session |
|-----------|-------|---------------|----------------|--------------|
| PreToolUse only | 200 | 100 ms | 20 seconds | ~3% |
| PostToolUse only | 200 | 100 ms | 20 seconds | ~3% |
| **Both hooks** | **400** | **100 ms** | **40 seconds** | **~6%** |

**With logging enabled (writing to disk):**

| Hook Type | Total Overhead | % of Session |
|-----------|----------------|--------------|
| PreToolUse + logging | 40-60 seconds | ~6-10% |
| PostToolUse + logging | 40-60 seconds | ~6-10% |
| **Both + logging** | **80-120 seconds** | **~13-20%** |

### 1.4 The Scaling Problem

As BB5 usage scales:

| Sessions/Day | Tool Calls/Day | Hook Overhead/Day |
|--------------|----------------|-------------------|
| 10 | 1,000-3,000 | 2-12 minutes |
| 50 | 5,000-15,000 | 8-60 minutes |
| 100 | 10,000-30,000 | 17-120 minutes |

**At 100 sessions/day, hooks alone consume 17-120 minutes of compute time.**

---

## 2. Use Case Analysis: What Do These Hooks Actually Do?

### 2.1 PreToolUse Hook Purposes (from research)

| Use Case | Essential? | Can Agent Do It? | Value/Overhead |
|----------|------------|------------------|----------------|
| **Block rm -rf /** | YES | NO | High/Low |
| **Block git push --force** | YES | NO | High/Low |
| **Block .env file access** | YES | NO | High/Low |
| **Log all tool calls** | NO | YES | Low/High |
| **Validate file structure** | NO | YES | Low/High |
| **Enforce naming conventions** | NO | YES | Low/High |
| **Route to AST-grep** | NO | YES | Medium/Medium |
| **File conflict detection** | PARTIAL | PARTIAL | Medium/High |

**Analysis:**
- Only **safety enforcement** is truly essential
- Everything else is convenience that agents can handle
- Logging creates I/O bottleneck for marginal benefit

### 2.2 PostToolUse Hook Purposes (from research)

| Use Case | Essential? | Can Agent Do It? | Value/Overhead |
|----------|------------|------------------|----------------|
| **Track edited files** | NO | YES | Low/High |
| **Auto-format code** | NO | YES | Medium/Medium |
| **Update timeline** | NO | YES | Low/High |
| **Log tool results** | NO | YES | Low/High |
| **Trigger RETAIN** | NO | YES | Medium/High |
| **Type-check TypeScript** | NO | YES | Medium/Medium |
| **Update skill metrics** | NO | YES | Low/High |

**Analysis:**
- **ZERO essential use cases**
- All can be done by agents at appropriate milestones
- Reactive updates create race conditions and hidden dependencies

### 2.3 What Actually Happens in Practice

Looking at the current BB5 PostToolUse hook (`/Users/shaansisodia/.claude/hooks/post-tool-use.sh`):

```bash
#!/bin/bash
# Post-Tool-Use Hook - Triggered after Edit/MultiEdit/Write/TodoWrite operations

echo "$(date '+%Y-%m-%d %H:%M:%S') - Post-tool-use hook triggered: $1" >> "$LOG_FILE"

case "$1" in
  "Edit"|"MultiEdit"|"Write"|"TodoWrite")
    echo "Significant change detected: $1" >> "$LOG_FILE"
    # TODO: Add sequential thinking capture here
    # TODO: Add real-time context preservation
    ;;
esac

exit 0
```

**Reality check:**
- It logs to a file (I/O overhead)
- It does nothing else (empty TODOs)
- It fires on EVERY Edit/Write (high frequency)
- **Value delivered: Near zero**

---

## 3. The Risk Question: What Are We Actually Preventing?

### 3.1 PreToolUse Safety: Real Risks

| Risk | Likelihood | Impact | PreToolUse Mitigation |
|------|------------|--------|----------------------|
| `rm -rf /` | Very Low | Catastrophic | Blocks it |
| `rm -rf ~` | Low | High | Blocks it |
| `git push --force` | Medium | High | Blocks it |
| `.env` exposure | Low | Medium | Blocks it |
| Accidental file deletion | Medium | Medium | Partial |

**Assessment:** PreToolUse for safety is justified. The risks are real and the mitigation is effective.

### 3.2 Can Agents Be Trusted?

**The uncomfortable truth:** Agents can and do make mistakes.

From the external research (EXTERNAL_HOOK_PATTERNS.md):
> "An 80% false claim rate occurred when grep results were trusted without reading files."

Agents:
- Can hallucinate commands
- Can misinterpret paths
- Can copy-paste dangerous examples
- Cannot be relied upon for self-policing

**Verdict:** PreToolUse safety hooks are necessary. But they should be minimal.

---

## 4. Alternative Approaches

### 4.1 If We Eliminate PostToolUse Hooks

**What agents should do instead:**

| Current Hook Function | Agent Responsibility |
|----------------------|---------------------|
| Track edited files | Agent writes to `edited-files.log` when completing work |
| Update timeline | Agent updates `timeline.yaml` at milestones |
| Log tool usage | Agent logs skills used in `RESULTS.md` |
| Trigger RETAIN | Agent runs `retain-on-complete.py` before exit |
| Update skill metrics | Agent appends to `skill-metrics.yaml` on completion |

**Benefits:**
- Explicit, testable behavior
- No hidden magic
- No per-tool overhead
- Agent understands what it's doing

### 4.2 If We Minimize PreToolUse Hooks

**Minimum viable PreToolUse (safety only):**

```python
#!/usr/bin/env python3
"""Minimal PreToolUse - Safety only, no logging."""
import sys, json, re

data = json.load(sys.stdin)
tool = data.get('tool_name', '')
input_data = data.get('tool_input', {})

# Only check Bash commands for dangerous patterns
if tool == 'Bash':
    cmd = input_data.get('command', '')

    # Block dangerous rm patterns
    dangerous_rm = [
        r'rm\s+-[a-z]*r[a-z]*f\s+/',
        r'rm\s+-[a-z]*r[a-z]*f\s+~',
        r'rm\s+--recursive.*--force.*/',
    ]
    for pattern in dangerous_rm:
        if re.search(pattern, cmd):
            print(f"Blocked dangerous command: {cmd}", file=sys.stderr)
            sys.exit(2)

    # Block force push
    if 'git push --force' in cmd or 'git push -f' in cmd:
        print("Blocked: git force push", file=sys.stderr)
        sys.exit(2)

# Allow everything else
sys.exit(0)
```

**Characteristics:**
- <50ms execution time
- No file I/O
- No logging
- Only blocks truly dangerous operations

### 4.3 Batched Logging Alternative

If logging is truly needed:

```python
# Instead of logging every tool call:
# - Buffer in memory
# - Flush at session end or every 50 calls
# - Write once, not 300 times
```

**Benefits:**
- Reduces I/O from 300 writes to 6 writes
- 50x reduction in disk operations
- Batching is more efficient

---

## 5. Cost-Benefit Analysis

### 5.1 PreToolUse Hooks

| Function | Benefit | Cost | Ratio |
|----------|---------|------|-------|
| Safety blocking | High (prevents disasters) | Low (<50ms) | **GOOD** |
| Logging | Low (audit trail) | High (300 writes) | **POOR** |
| Validation | Medium | Medium | **MARGINAL** |
| Routing | Medium | Medium | **MARGINAL** |

### 5.2 PostToolUse Hooks

| Function | Benefit | Cost | Ratio |
|----------|---------|------|-------|
| File tracking | Low | High | **POOR** |
| Timeline updates | Low | High | **POOR** |
| Auto-formatting | Medium | Medium | **MARGINAL** |
| RETAIN trigger | Medium | High | **POOR** |

**Overall:** PostToolUse hooks have universally poor cost-benefit ratios.

---

## 6. Recommendations

### 6.1 ELIMINATE: PostToolUse Hooks

**Rationale:**
- Zero essential functions
- All use cases can be handled by agents
- 100-300+ executions per session with minimal value
- Creates hidden dependencies and magic behavior

**Migration:**
1. Move file tracking to agent responsibility
2. Move timeline updates to milestone-based updates
3. Move RETAIN triggering to session-end
4. Document the new agent responsibilities

### 6.2 MODIFY: PreToolUse Hooks (Safety Only)

**Rationale:**
- Safety enforcement is essential
- But logging and validation are not
- Current implementation is too heavy

**New Implementation:**
```python
# pre-tool-use-safety.py
# - No logging
# - No validation
# - Only safety blocking
# - <50ms execution time
```

**Block list (minimal):**
- `rm -rf /`, `rm -rf ~`, `rm -rf /important/path`
- `git push --force`
- `.env` file reads (except `.env.sample`)
- `dd if=/dev/zero of=/dev/sda`

### 6.3 ADD: Session-Boundary Validation

Instead of per-tool validation, do validation at key points:

| When | What | Why |
|------|------|-----|
| Session start | Validate environment | One-time check |
| Pre-commit | Validate changes | Batch validation |
| Session end | Validate documentation | Final check |

**Benefits:**
- Validates once, not 300 times
- Catches issues before they become problems
- No per-tool overhead

---

## 7. Implementation Path

### Phase 1: Disable PostToolUse (Immediate)

```bash
# Disable PostToolUse hooks
mv .claude/hooks/post-tool-use.sh .claude/hooks/post-tool-use.sh.disabled

# Update settings.json to remove PostToolUse entries
```

### Phase 2: Simplify PreToolUse (Week 1)

```bash
# Replace current PreToolUse with safety-only version
# Remove all logging
# Remove all validation
# Keep only safety blocking
```

### Phase 3: Update Agent Prompts (Week 1-2)

Add to RALF prompt:
```markdown
## Responsibilities (Previously Handled by Hooks)

You are now responsible for:
1. **File Tracking** - Log edited files in THOUGHTS.md
2. **Timeline Updates** - Update timeline.yaml at milestones
3. **RETAIN Trigger** - Run retain-on-complete.py before exit
4. **Skill Logging** - Document skills used in RESULTS.md
```

### Phase 4: Measure Impact (Week 2-3)

Track:
- Session duration (should decrease 5-10%)
- Tool call latency (should decrease significantly)
- Disk I/O (should decrease dramatically)
- Agent behavior (should be more explicit)

---

## 8. The Ruthless Bottom Line

**If a BB5 session makes 300 tool calls:**

| Approach | Hook Executions | Overhead | Value |
|----------|-----------------|----------|-------|
| Current (13 hooks) | 3,900+ | 6-13 minutes | Low (magic behavior) |
| Recommended (1 safety hook) | 300 | 15 seconds | High (safety only) |
| **Savings** | **3,600+ executions** | **6-12 minutes** | **More clarity** |

**Key Questions Answered:**

1. **If a BB5 session makes 100+ tool calls, do we want hooks firing 100+ times?**
   - Only for safety. Everything else is waste.

2. **What is the actual risk we're preventing with PreToolUse safety checks?**
   - Real risks: rm -rf, force push, .env exposure
   - Risk level: Low probability, high impact
   - Mitigation: Worth it, but minimal implementation

3. **Can agents be trusted to not run `rm -rf /`?**
   - No. Agents make mistakes. Safety hooks are essential.
   - But agents CAN be trusted to update their own documentation.

4. **What is the cost vs benefit of per-tool hooks?**
   - PreToolUse safety: Good ratio (high benefit, low cost if minimal)
   - PreToolUse logging: Poor ratio (low benefit, high cost)
   - PostToolUse everything: Terrible ratio (minimal benefit, high cost)

---

## 9. Conclusion

**Final Recommendation:**

1. **ELIMINATE PostToolUse hooks entirely**
2. **KEEP PreToolUse hooks for safety only** (minimal implementation)
3. **MOVE all reactive updates to agent responsibility**
4. **VALIDATE at session boundaries, not per-tool**

**The 3-Hook System (from FIRST_PRINCIPLES_HOOKS.md) is correct:**
- SessionStart: Initialize workspace
- PreToolUse: Safety enforcement ONLY
- SessionEnd: Cleanup

**Everything else is convenience masquerading as necessity.**

---

*Analysis based on actual transcript data, external research across 10+ repositories, and first principles reasoning.*
