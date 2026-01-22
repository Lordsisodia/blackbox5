# Agent 1 — Research + Grouping

Goal: Convert a messy list of feedback items into **domain-based groups** and **issue folders** that preserve context and reduce redundant research.

## Inputs

- `.blackbox/inbox/issues.md`
- Any supporting notes in `.blackbox/inbox/`
- The actual repo codebase (search, read files, inspect patterns)

## Outputs (must be created/updated)

- `.blackbox/state/groups.md`
- One issue folder per issue:
  - `.blackbox/issues/<ISSUE-ID>/plan.md` (seeded from template)

## Method

1. Parse each inbox item:
   - rewrite into a clear problem statement
   - split multi-problem lines
2. Do lightweight code research:
   - locate likely files via ripgrep and project structure
   - note similar existing patterns to reuse
3. Group by **shared code ownership**:
   - shared directories
   - shared services
   - shared database tables/policies
4. Create issue folders and link them into `.blackbox/state/groups.md`.

## Quality bar

- Every issue has a reproducible description (or a clear “unknown repro” note).
- Every issue has at least one concrete code pointer (file path or service name).
- Groups make execution cheaper (batching related changes).



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
