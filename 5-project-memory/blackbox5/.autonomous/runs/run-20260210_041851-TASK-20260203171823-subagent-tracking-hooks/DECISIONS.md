# DECISIONS - TASK-20260203171823

## Decision 1: Use Heuristic Summarization Instead of LLM

**Context:** Task summarization could use LLM or simple heuristic.

**Decision:** Use simple heuristic approach.

**Rationale:**
- No LLM service configured in BB5 (no Ollama/Anthropic)
- Reduces dependencies and infrastructure requirements
- Sufficient for MVP - shows what's possible

**Trade-offs:**
- Pro: Simple, fast, no dependencies
- Con: Less intelligent summaries than LLM

**Future Extension:**
- Can add `summarize_with_llm()` function that calls Ollama
- Keep heuristic as fallback

---

## Decision 2: Support JSONL Transcript Parsing

**Context:** Need to extract task context from subagent transcripts.

**Decision:** Implement JSONL parser that reads first user message.

**Rationale:**
- Subagents work with transcripts that track their execution
- First user message contains the original task description
- Provides meaningful context for summarization

**Implementation Details:**
- Check for `agent_transcript_path` first, then `transcript_path`
- Parse JSONL file line by line
- Look for `type="user"` entries
- Extract from `message.content` or direct `content`

**Edge Cases Handled:**
- Missing transcript path
- Non-existent transcript file
- Corrupted JSONL lines (skip them)
- Empty content fields

---

## Decision 3: JSON Log File Format

**Context:** How to structure the log files.

**Decision:** JSON array with appended entries.

**Format:**
```json
[
  {
    "agent_id": "Executor-abc123",
    "agent_type": "executor",
    "logged_at": "2026-02-10T04:20:00.000000"
  }
]
```

**Rationale:**
- Append-only pattern - easy to add new entries
- JSON is human-readable
- Easy to parse and analyze with tools like jq

**File Paths:**
- `logs/subagent_start.json`
- `logs/subagent_stop.json`

---

## Decision 4: Agent Type Tracking

**Context:** Need to distinguish between Executor, Planner, Architect.

**Decision:** Use `agent_type` field from input data.

**Values:**
- "executor" - for Executor agent
- "planner" - for Planner agent
- "architect" - for Architect agent (if created)
- "unknown" - default fallback

**Rationale:**
- Field exists in research repo templates
- Simple string field - no schema needed
- Easy to filter/aggregate by type later

---

## Decision 5: Timestamp Field

**Context:** Need to know when events occurred.

**Decision:** Add `logged_at` timestamp to all log entries.

**Format:** ISO 8601 string

**Rationale:**
- Standard format for machine and human reading
- Enables time-series analysis
- Easy to sort/filter

---

## Decision 6: Error Handling Strategy

**Context:** What to do if hooks fail.

**Decision:** Fail gracefully - log error, exit with 0.

**Implementation:**
- `json.JSONDecodeError` -> exit 0 (malformed input, ignore)
- Other exceptions -> exit 0 (fail silently)
- Log directory creation failures ignored
- File write failures ignored

**Rationale:**
- Hooks should not crash the main Claude session
- Fail silently to prevent error propagation
- Graceful degradation is acceptable for tracking hooks

---

## Decision 7: Task Summarizer Reusability

**Context:** Should summarization logic be reusable.

**Decision:** Create standalone utility in `utils/task_summarizer.py`.

**Functions:**
- `extract_task_context()` - reads transcript
- `summarize_heuristic()` - heuristic summarization
- `summarize_subagent_task()` - main entry point

**Rationale:**
- Reusable across hooks and other code
- Extensible for future LLM integration
- Clear API for other developers

**Trade-offs:**
- Pro: Reusable, testable
- Con: Extra file and import overhead
