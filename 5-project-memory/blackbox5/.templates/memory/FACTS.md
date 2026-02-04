---
memory_type: world
network: W
created: "{{DATE}}"
source: "{{SOURCE}}"
version: "1.0"
---

# FACTS - Objective World Knowledge

**Task:** {{TASK_ID}}
**Source:** {{SOURCE}}
**Created:** {{DATE}}

---

## Facts Recorded

### F-001: [Fact Title]

**Category:** [technical/decision/entity/relationship]
**Confidence:** [0.0-1.0]
**Verification:** [verified/assumed/inferred]

**Statement:**
> Clear, objective statement of fact

**Evidence:**
- Source: [file/line/reference]
- Context: [surrounding context]

**Related:**
- Links to: [other facts]
- Entities: [people, places, concepts]

---

### F-002: [Fact Title]

[Additional facts following same format]

---

## Entities Discovered

| Entity | Type | First Seen | Context |
|--------|------|------------|---------|
| [Name] | [person/place/concept] | {{DATE}} | [Brief context] |

---

## Relationships Established

| Subject | Relationship | Object | Confidence |
|---------|--------------|--------|------------|
| [Entity A] | [relates to] | [Entity B] | [0.0-1.0] |

---

## How to Use This Template

**World Network (W)** stores objective facts about the world:
- Technical facts (APIs, configurations, code patterns)
- Decisions made (what was decided, by whom)
- Entities (people, organizations, technologies)
- Relationships (how things connect)

**When to record:**
- You discover something new about the system
- A decision is made
- You identify an entity or relationship
- You verify or correct existing knowledge

**Writing tips:**
- Be objective - facts, not interpretations
- Include confidence scores
- Link to evidence
- Use clear, searchable language

---

*Part of Hindsight Memory Architecture - World Network*
