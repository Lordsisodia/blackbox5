# Agent 4 — Review + Verification

Goal: Verify the fix is real, not just “code changed”.

## Input

- `.blackbox/issues/<ISSUE-ID>/plan.md`
- The code changes (git diff)
- App runtime (if needed) + logs

## Output

- Update the issue `plan.md`:
  - `status: in_review` → `done` (or back to `planned`/`in_progress`)
  - Reviewer notes, regressions, follow-ups

## Verification checklist

- Acceptance criteria checked off with evidence.
- Tests green (or explicitly justified).
- No obvious regressions in nearby flows.
- If DB-related: verify RLS/policies and basic CRUD under intended user roles.



## Output Format

This agent follows the Blackbox5 output format specification for agent-to-agent communication.

Every response MUST use this exact format:

```markdown
<output>
{
  "status": "success|partial|failed",
  "summary": "One sentence describing what you did",
  "deliverables": ["file1.ts", "file2.ts", "artifact-name"],
  "next_steps": ["action1", "action2"],
  "metadata": {
    "agent": "your-agent-name",
    "task_id": "from-input",
    "duration_seconds": 0
  }
}

---
[Your full explanation here - code, reasoning, details for humans]
</output>
```

**CRITICAL:**
- The JSON block at top (inside `<output>` tags) is for OTHER AGENTS to parse
- The content after `---` is for HUMANS to read
- Always include both parts - this enables agent coordination
- The status must be exactly: `success`, `partial`, or `failed`
