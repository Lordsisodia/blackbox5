# Agent 2a — Classification + Options

Goal: For each issue, classify it and propose **three realistic solutions** based on the actual code.

## Input

- `.blackbox/issues/<ISSUE-ID>/plan.md` (seeded)
- Codebase (must inspect relevant files; no speculative designs)

## Output

Update the issue’s `plan.md`:

- Classification (category, risk, blast radius, testing)
- Three options (A/B/C), each with concrete file-level changes

## Constraints

- Options must be implementable in this repo.
- Prefer existing patterns and services.
- If DB-related, explicitly call out:
  - tables involved
  - RLS/policies impact
  - whether a migration is required

## What “good” looks like

- Option A is a minimal safe fix.
- Option B is the “best long-term” fix consistent with existing patterns.
- Option C is a legitimate alternate (not a strawman).



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
