# Output Format Section Template for agent.md

## Copy and paste this into any agent.md file

```markdown
## Output Format

This agent follows the [Blackbox5 Output Format Specification](../../01-core/AGENT-OUTPUT-FORMAT-SPEC.md).

### Required Structure

Every response includes:

1. **Summary** (1 paragraph, 2-3 sentences max)
   - What was done
   - Key outcome

2. **Result Box** (Visual ASCII box)
   ```
   ┌─────────────────────────────────────────────────────────────┐
   │  🎯 STATUS: [✅ Success | ⚠️ Partial | ❌ Failed]              │
   │  📊 OUTCOME: [One-line clear outcome statement]             │
   │  📁 DELIVERABLES: [Bullet list of what was produced]        │
   │  ➡️ NEXT STEPS: [What should happen next]                   │
   └─────────────────────────────────────────────────────────────┘
   ```

3. **Details** (Full content)
   - Subsections with ### headers
   - Code blocks with language tags
   - Bullet points for lists
   - Tables for structured data

4. **Technical Notes** (Optional)
   - Implementation details
   - Edge cases handled
   - Performance considerations

5. **Related Files** (Optional)
   - List of files affected
   - Brief descriptions

### Agent-Specific Emphasis

[AGENT-NAME] focuses on:

- [Primary output type - e.g., "Code implementations"]
- [Key deliverables - e.g., "Files created, tests added"]
- [Typical details section content - e.g., "Code blocks with explanations"]

### Example Response

```markdown
# Summary

[One paragraph, 2-3 sentences max, describing what was done and the key outcome]

---

## Result Box

┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Success                                       │
│  📊 OUTCOME: [Clear one-line outcome]                        │
│  📁 DELIVERABLES:                                            │
│  • [Deliverable 1]                                           │
│  • [Deliverable 2]                                           │
│  • [Deliverable 3]                                           │
│  ➡️ NEXT STEPS: [Next action, if any]                        │
└─────────────────────────────────────────────────────────────┘

---

## Details

### Section 1
[Detailed explanation with code, analysis, or content]

### Section 2
[More details as needed]

---

## Technical Notes

[Optional technical details]

---

## Related Files

- `path/to/file1` - [Description]
- `path/to/file2` - [Description]
```
```

## Quick Reference: Status Emojis

| Emoji | Meaning | When to Use |
|-------|---------|-------------|
| ✅ | Success | Task completed successfully |
| ⚠️ | Partial | Task partially complete, has caveats |
| ❌ | Failed | Task failed, error encountered |
| 🎯 | Status | Status indicator |
| 📊 | Outcome | Result/outcome indicator |
| 📁 | Deliverables | Files/artifacts created |
| ➡️ | Next Steps | Forward-looking actions |
| 💡 | Tip | Helpful suggestion |
| 🔧 | Technical | Technical detail |

## Quick Reference: Section Headers

```markdown
# Summary          ← Required
## Result Box       ← Required (ASCII box)
## Details          ← Required
### Subsection      ← Use ### for sections within Details
## Technical Notes  ← Optional
## Related Files    ← Optional
```
