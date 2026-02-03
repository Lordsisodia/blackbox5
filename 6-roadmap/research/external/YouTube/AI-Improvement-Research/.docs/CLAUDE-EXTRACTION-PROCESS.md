# Claude Extraction Process - 3×3 Parallel System

**Date**: 2026-02-02 (Updated: 2026-02-03)
**Version**: 2.0

---

## IMPORTANT: New 3×3 Methodology

**Research Finding**: Single 3-iteration extractions miss 20-30% of extractable concepts.

**Solution**: Run **3 parallel extractions** (each with 3 iterations), then synthesize results.

**Why**: Different extractions catch different interpretations, framings, and details. Parallel execution with synthesis achieves higher coverage and score consistency.

**Trade-off**: 3× API cost for ~30% more comprehensive coverage.

---

## Overview

Standardized **3×3 parallel extraction process** for video content using Claude.

**Goal**: 98% coverage of important, actionable information through parallel extractions + synthesis.

**Naming Convention**: `"{Video Title} by {Creator}.md"`

### The 3×3 Process

```
┌─────────────────────────────────────────────────────────────┐
│                    PARALLEL EXTRACTIONS                     │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Extraction A   │  Extraction B   │    Extraction C         │
│  (3 iterations) │  (3 iterations) │    (3 iterations)       │
└────────┬────────┴────────┬────────┴──────────┬──────────────┘
         │                 │                   │
         ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│              SYNTHESIS ITERATION (Iteration 4)              │
│  • Merge unique concepts from all 3 extractions             │
│  • Reconcile score differences                              │
│  • Resolve naming inconsistencies                           │
│  • Create unified master document                           │
└─────────────────────────────────────────────────────────────┘
```

**Total**: 4 iterations (3 parallel extractions + 1 synthesis)

---

## The 3 Iterations

### Iteration 1: Initial Extraction (70% coverage)
**Purpose**: Capture core concepts and structure

**What to extract**:
- Summary (2-3 sentences)
- Key concepts (bullet points)
- Commands & basic usage
- Best practices (do/don't)
- Key takeaways (5-10 points)

**Output format**: Structured markdown with importance markers
- [CRITICAL] - Essential, game-changing
- [HIGH] - Very valuable
- [MEDIUM] - Useful context
- [LOW] - Background info

---

### Iteration 2: Deep Analysis (90% coverage)
**Purpose**: Add specifics, ratings, and context

**What to add**:
- Rate every concept 0-100
- Context-rich explanations (paragraphs)
- Specific examples from video
- Exact syntax and commands
- Why it matters (justification)

**Scoring system**:
| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Game-changing, fundamental | Must learn immediately |
| 80-89 | Very important, commonly needed | Learn soon |
| 70-79 | Useful, good to know | Reference when needed |
| 60-69 | Nice to have, situational | Optional |
| 0-59 | Background info | Skip if time-limited |

**Output format**:
```markdown
### [XX/100] Concept Name
**What it is:** [Detailed paragraph]

**Why it matters:** [Explanation]

**Specific example:** [From video]

**Implementation:** [Exact steps/syntax]
```

---

### Iteration 3: Master Synthesis (95% coverage per extraction)
**Purpose**: Create definitive reference document for this extraction branch

**Required sections**:
1. **Executive Summary** - One paragraph overview
2. **All Concepts Rated 0-100** - Complete inventory
3. **Complete Command Reference** - Table format
4. **Key Techniques** - Step-by-step instructions
5. **Synthesis: What Matters Most** - Tiered priorities
6. **Action Checklist** - Specific, ordered actions
7. **Full Transcript** - For verification

**Naming**: `"{Video Title} by {Creator}_A.md"` (or _B, _C for parallel extractions)

---

### Iteration 4: Cross-Extraction Synthesis (98% coverage)
**Purpose**: Merge 3 parallel extractions into unified master document

**Input**: 3 master documents (A, B, C) from parallel extractions

**Tasks**:
1. **Concept Deduplication**
   - Identify same concepts with different names (fuzzy matching)
   - Merge truly unique concepts from each extraction
   - Flag concepts appearing in only 1 of 3 extractions as "uncertain"

2. **Score Reconciliation**
   - For concepts appearing in 2+ extractions: average the scores
   - For concepts appearing in all 3: high confidence, use average
   - For concepts appearing in 1: flag as "low confidence"

3. **Naming Standardization**
   - Choose most descriptive name for each concept
   - Add alternate names as "also known as" where relevant

4. **Coverage Analysis**
   - List concepts unique to each extraction
   - Document overlap percentage
   - Note any major omissions

**Output Sections**:
1. **Executive Summary** - Synthesized from all 3
2. **All Concepts Rated 0-100** - Merged and reconciled
3. **Complete Command Reference** - Unified table
4. **Key Techniques** - Consolidated techniques
5. **Synthesis: What Matters Most** - Tiered priorities
6. **Coverage Analysis** - What each extraction contributed
7. **Action Checklist** - Consolidated actions
8. **Full Transcript** - For verification

**Naming**: `"{Video Title} by {Creator}.md"` (final unified document)

---

## File Organization

### Output Location
```
by_topic/{topic}/
├── _index.yaml                              # Topic metadata
├── "{Title} by {Creator}.md"                # Master document (ITERATION 3)
└── [Other videos...]
```

### Example
```
by_topic/claude-code/
├── _index.yaml
├── "Anthropic's 7 Hour Claude Code Course in 27 Minutes by David Ondrej.md"
├── "Claude Cowork replaces your AI tech stack by David Ondrej.md"
└── ...
```

---

## Usage

### Extract a Video (3×3 Parallel Process)

```bash
# Run 3×3 parallel extraction (recommended)
python scripts/extract_claude_v2.py --video VIDEO_ID --creator CREATOR_SLUG

# This will:
# 1. Spawn 3 parallel sub-agents, each running 3-iteration extraction
# 2. Collect 3 master documents (_A.md, _B.md, _C.md)
# 3. Run synthesis iteration to create unified master document

# Dry run (preview)
python scripts/extract_claude_v2.py --video XuSFUvUdvQA --creator david_ondrej --dry-run
```

### Legacy: Single 3-Iteration Extraction

```bash
# Use v1 for quick extractions where 95% coverage is sufficient
python scripts/extract_claude.py --video VIDEO_ID --creator CREATOR_SLUG
```

### Manual Process (if needed)

If you need to run iterations manually:

```bash
# Iteration 1: Initial extraction
# [Run sub-agent with iteration 1 prompt]

# Iteration 2: Deep analysis
# [Run sub-agent with iteration 2 prompt, feeding iteration 1 output]

# Iteration 3: Master synthesis
# [Run sub-agent with iteration 3 prompt, feeding iteration 2 output]
# [Save as "{Title} by {Creator}.md"]
```

---

## Quality Standards

### Master Document Must Have:

- [ ] Every concept rated 0-100
- [ ] Context-rich explanations (no bullet points except tables/lists)
- [ ] Specific examples from video
- [ ] Exact commands and syntax
- [ ] Practical, actionable focus
- [ ] Complete command reference table
- [ ] Action checklist with exact steps
- [ ] Full transcript included

### Naming Must Be:

- [ ] Video title (full or truncated with ...)
- [ ] " by " separator
- [ ] Creator name
- [ ] .md extension
- [ ] No special characters: < > : " / \ | ? *

---

## Example Output Structure

```markdown
# Anthropic's 7 Hour Claude Code Course in 27 Minutes by David Ondrej

**Video**: https://youtube.com/watch?v=XuSFUvUdvQA
**Published**: 2026-01-20
**Duration**: 27 minutes
**Extraction Date**: 2026-02-02

---

## Executive Summary

[One paragraph overview]

---

## All Concepts Rated 0-100

### [99/100] Three-Step Coding Assistant Loop
**One-sentence summary:** [Core idea]

**Full explanation:** [Detailed paragraphs]

**Specific evidence:** [Quotes from video]

**Implementation:** [How to apply]

**Why this rating:** [Justification]

---

## Complete Command Reference

| Rating | Command | Syntax | What It Does | When to Use |
|--------|---------|--------|--------------|-------------|
| [98/100] | /init | `/init` | Analyzes codebase, creates claude.md | First step in any project |
| ... | ... | ... | ... | ... |

---

## Key Techniques

### Technique Name [85/100]
**Prerequisites:** [What you need]

**Steps:**
1. [Step one]
2. [Step two]
3. [Step three]

**Example from video:** [Specific scenario]

**Common pitfalls:** [What to avoid]

---

## Synthesis: What Matters Most

### Tier 1 (90-100): Must Know
1. [Concept] - [One-line why]
2. ...

### Tier 2 (80-89): Very Important
1. [Concept] - [One-line why]
2. ...

### Tier 3 (70-79): Good to Know
1. [Concept] - [One-line why]
2. ...

---

## Action Checklist

- [ ] [Specific action with exact command]
- [ ] [Specific action with exact command]
- [ ] ...

---

## Full Transcript

<details>
<summary>Click to expand</summary>

[Complete transcript]

</details>
```

---

## Current Extractions

| Video | Creator | File | Coverage |
|-------|---------|------|----------|
| Anthropic's 7 Hour Claude Code Course in 27 Minutes | David Ondrej | `Anthropic's 7 Hour Claude Code Course in 27 Minutes by David Ondrej.md` | 95% |

---

## Process Notes

**Why 3×3 parallel extractions?**

Research on duplicate extractions revealed:
- Single extraction: ~70-75% concept coverage
- Two extractions: 40-53% unique concepts between them
- After adjusting for renames: 20-30% truly unique content per extraction
- Score inconsistency: Same concepts rated 1-17 points differently

**The 3×3 solution:**
- Run 3 parallel extractions (A, B, C), each with 3 iterations
- Synthesize results to catch different interpretations
- Reconcile scores for consistency
- Achieve 98% coverage vs 95% for single extraction

**Cost vs Benefit:**
- Cost: 3× API calls
- Benefit: ~30% more comprehensive coverage
- Recommendation: Use 3×3 for high-priority videos, single 3-iteration for routine

**Why 4 iterations total?**
- Iterations 1-3 (×3 parallel): 95% coverage per branch
- Iteration 4 (synthesis): +3% from merging unique concepts
- Total: 98% coverage with higher confidence

**When to use 3×3?**
- High-priority videos (Tier 1 creators)
- Foundational content you'll reference often
- When creating canonical documentation
- When score consistency matters

**When to use single 3-iteration?**
- Routine extractions
- Lower-tier content
- Quick reference needs
- Cost-sensitive scenarios

---

## Next Steps

1. Extract remaining high-priority videos using this process
2. Maintain consistent naming convention
3. Update topic index files
4. Build synthesis layer for cross-video insights
