# Voice-to-AI Transcription Research Synthesis

**Date:** 2026-02-04
**Researcher:** Claude (Superintelligence Protocol)

## Key Findings

### 1. Markdown is the "Native Language" of LLMs
- AI systems trained on billions of Markdown documents
- Explicit structural constraints outperform implicit ones by 4.7%
- Text tree representations significantly outperform edge lists

### 2. Disfluency Removal Has Trade-offs
**Benefits:**
- Cleaner output, easier parsing
- Reduced token count (cost savings)

**Risks:**
- Loses uncertainty markers ("maybe", "I think")
- Removes scope constraints ("simple", "just", "basic")
- Destroys politeness/tone indicators
- Eliminates self-correction context

### 3. Context Tagging Dramatically Improves AI Tool Use
- `[FILE:path]` enables direct file references
- `[COMPONENT:name]` helps AI identify relevant code
- `[TASK:description]` extracts actionable items

### 4. Hierarchical Structure Parses Better
```markdown
# Main Topic
## Section
- Point 1
- Point 2
  - Detail
```

### 5. Different Contexts Need Different Processing

| Context | Processing Level | Why |
|---------|------------------|-----|
| Code commands | Heavy | Precision matters |
| Debugging | Light | Uncertainty markers help |
| Planning | Medium | Balance structure and nuance |
| Creative | Minimal | Voice/pacing is content |

## Critical Warnings

1. **Homophones remain problematic**: write/right, cache/cash, null/none
2. **Over-processing destroys intent**: "maybe add a simple cache" → "add cache"
3. **Context switches need markers**: Don't remove all restarts/corrections
4. **Technical jargon is fragile**: Function names, variable names easily misheard

## Sources

- HiBench research (Hong Kong Polytechnic University)
- AssemblyAI speech-to-text guide
- Vapi.ai audio preprocessing research
- Promptify token compression analysis
- Claude Code best practices
- Multiple GitHub projects (listen-claude-code, Voice Prompt Enhancement Node)

## Confidence: 85%

Strong research backing for Markdown structure and explicit formatting. Trade-off between processing and preservation is well-documented. Remaining uncertainty is around optimal balance for specific use cases.
