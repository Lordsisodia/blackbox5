# YAML vs MD for System Prompts - Evaluation

**Date:** 2026-02-04
**Status:** Analysis Complete

---

## Current State

### What's Actually Being Used

| Format | Usage | Location | Purpose |
|--------|-------|----------|---------|
| **Markdown (.md)** | 43+ files | `2-engine/.autonomous/prompts/` | Primary prompt format |
| **YAML front matter** | Embedded in MD | Top of skill files | Metadata only |
| **Pure YAML** | Minimal | Skills deploy configs | Infrastructure only |

### Current Structure

**System Prompts (MD only):**
```
prompts/
├── ralf.md
├── ralf-executor.md
├── system/
│   ├── identity.md
│   ├── executor-identity.md
│   └── planner-identity.md
├── executor/
│   └── versions/v1-20260201/executor.md
├── planner/
│   └── versions/v4-20260202/planner.md
└── architect/
    └── versions/v4-20260202/architect.md
```

**Skills (MD with YAML front matter):**
```
skills/
├── bmad-dev/SKILL.md       (YAML front matter + MD content)
├── bmad-analyst/SKILL.md   (YAML front matter + MD content)
└── git-commit/SKILL.md     (YAML front matter + MD content)
```

---

## Evaluation Criteria

### 1. Readability

| Format | Human | LLM | Winner |
|--------|-------|-----|--------|
| Markdown | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | ✅ MD |
| YAML | ⭐⭐ Good | ⭐⭐⭐ Excellent | - |

**Analysis:**
- MD: Natural flow, clear hierarchy with headers
- YAML: Structured but verbose for long content

### 2. Metadata Support

| Format | Structured Data | Flexibility | Winner |
|--------|----------------|-------------|--------|
| Markdown | ⭐ Limited | ⭐⭐⭐ High | - |
| YAML | ⭐⭐⭐ Excellent | ⭐⭐ Good | ✅ YAML |

**Analysis:**
- MD: Requires front matter or conventions for metadata
- YAML: Native structured data support

### 3. Version Control

| Format | Diff Friendliness | Merge Conflicts | Winner |
|--------|------------------|-----------------|--------|
| Markdown | ⭐⭐⭐ Excellent | ⭐⭐⭐ Low | ✅ MD |
| YAML | ⭐⭐ Good | ⭐⭐ Moderate | - |

**Analysis:**
- MD: Line-by-line changes clear in diffs
- YAML: Indentation issues, nested structure conflicts

### 4. Tooling Support

| Format | Editors | Parsers | Validation | Winner |
|--------|---------|---------|------------|--------|
| Markdown | ⭐⭐⭐ Universal | ⭐⭐⭐ Excellent | ⭐⭐ Limited | - |
| YAML | ⭐⭐⭐ Universal | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | ✅ YAML |

**Analysis:**
- MD: Every editor supports it
- YAML: Schema validation, strict parsing

### 5. LLM Context Efficiency

| Format | Token Efficiency | Structure Clarity | Winner |
|--------|-----------------|-------------------|--------|
| Markdown | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | ✅ MD |
| YAML | ⭐⭐ Good | ⭐⭐⭐ Excellent | - |

**Analysis:**
- MD: Natural language = fewer tokens for same meaning
- YAML: Repetitive syntax ("key: value") adds tokens

### 6. Maintenance Burden

| Format | Editing Ease | Error Prevention | Winner |
|--------|-------------|------------------|--------|
| Markdown | ⭐⭐⭐ Easy | ⭐⭐ Moderate | ✅ MD |
| YAML | ⭐⭐ Moderate | ⭐⭐⭐ Schema validation | - |

**Analysis:**
- MD: Easy to edit, but easy to break formatting
- YAML: Strict syntax prevents some errors

---

## Hybrid Approach (Current Best Practice)

**What we're already doing:**

```markdown
---
name: bmad-dev
description: Implementation and coding tasks
category: agent
trigger: Implementation needed
inputs:
  - name: requirements
    type: document
outputs:
  - name: code
    type: code
---

# BMAD Developer (Amelia)

## Persona
...
```

**Benefits:**
1. ✅ Machine-readable metadata (YAML front matter)
2. ✅ Human-readable content (Markdown)
3. ✅ Version control friendly
4. ✅ LLM token efficient
5. ✅ Universal tooling support

---

## Recommendations

### ✅ Keep Current Hybrid Approach

**For System Prompts:**
- Use **Markdown** as primary format
- Add YAML front matter for metadata (version, purpose, triggers)
- Keep content in natural language

**For Skills:**
- Use **Markdown with YAML front matter**
- YAML: name, description, inputs, outputs, triggers
- MD: Persona, principles, commands, examples

**For Configuration:**
- Use **Pure YAML** (queue.yaml, events.yaml, protocol.yaml)
- Machine-to-machine communication

### 📋 Standard Template

```markdown
---
name: prompt-name
version: 1.0.0
agent: planner|executor|architect
purpose: One-line description
triggers:
  - keyword1
  - keyword2
inputs:
  - name: input1
    type: document|code|string
outputs:
  - name: output1
    type: code|document
category: system|agent|skill
---

# Title

## Identity
...

## Instructions
...
```

### 🚫 What NOT to Do

1. **Don't use pure YAML for long prompts**
   - Bad: `instructions: "Line 1\nLine 2\nLine 3..."`
   - Good: Markdown body after front matter

2. **Don't put logic in YAML**
   - Bad: `if_task_type: {conditions: [...]}`
   - Good: Write logic in Markdown with clear sections

3. **Don't duplicate metadata**
   - Bad: Version in filename AND front matter
   - Good: Front matter is source of truth

---

## Conclusion

**Winner: Markdown with YAML Front Matter (Hybrid)**

The system is already using the optimal approach:
- **43+ MD files** for prompts (human-readable)
- **YAML front matter** for metadata (machine-readable)
- **Pure YAML** for data/config (structured communication)

**No changes needed.** The current approach is best practice.

---

*Evaluation complete. Current hybrid approach is optimal.*
