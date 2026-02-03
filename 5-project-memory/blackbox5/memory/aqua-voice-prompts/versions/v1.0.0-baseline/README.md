# Version 1.0.0 - Baseline

**Created:** 2026-02-04
**Status:** Current
**Based on:** Superintelligence protocol research synthesis

## Prompt

```markdown
# AQUA VOICE: AI-OPTIMIZED TRANSCRIPTION

## CORE RULES
1. Remove filler words: um, uh, like, you know, so, actually, basically, I mean
2. Keep self-corrections: preserve "actually", "wait", "no" as they indicate changes of mind
3. Format in Markdown with:
   - ## Headers for topic changes
   - - Bullet points for lists
   - - [ ] Checkboxes for tasks
   - **bold** for emphasis
4. Tag technical references: [FILE:path], [COMPONENT:name]

## CONTEXT HANDLING
- Code: Preserve exact syntax, casing, punctuation
- Tasks: Convert "need to X" → "- [ ] X"
- Questions: Keep question marks and uncertainty markers

## OUTPUT FORMAT
Start with one-sentence summary in bold, then structured content.
```

## Design Rationale

This baseline prompt balances:
- **Disfluency removal** (cleaner output)
- **Semantic preservation** (keeps uncertainty markers)
- **Structure** (Markdown hierarchy)
- **Context awareness** (file/component tagging)

## Intended Use Cases

- General development work
- Claude Code CLI input
- Mixed conversation + code contexts

## Known Limitations

- May not handle rapid context switches well
- Homophones (write/right, cache/cash) remain problematic
- Technical jargon may be misheard
- "Simple" constraints may be lost ("maybe add a simple cache" → "add cache")

## Testing Notes

### Test Scenarios to Try

1. **Code command:** "Fix the bug in auth.ts where login fails"
2. **Planning:** "We need to deploy the fix, update docs, and notify the team"
3. **Architecture:** "I'm thinking maybe we should use Redis for caching, but actually PostgreSQL might be better"
4. **Debug session:** "So the error happens when... wait, no, it's actually when the user clicks submit"

### What to Watch For

- Does it preserve important qualifiers? ("maybe", "simple", "just")
- Does it catch file references correctly?
- Does the structure help or hinder?
- Are self-corrections preserved?

## Next Version Ideas

- v1.1.0-code-focused: Heavier optimization for code commands
- v1.1.0-minimal: Lighter touch for creative/planning contexts
- v1.1.0-tagged: More aggressive context tagging
