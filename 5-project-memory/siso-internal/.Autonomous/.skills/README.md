# Legacy Skills Registry

**Location:** `.Autonomous/.skills/`
**Purpose:** Reusable capabilities for Legacy autonomous execution

---

## Skill Types

| Type | Description | Example |
|------|-------------|---------|
| **Simple** | Single-file skill, one command | `validate-assumption.yaml` |
| **Complex** | Multi-file skill, workflow | `truth-seeking/` folder |
| **Agent** | Pre-configured with persona | `researcher-agent.yaml` |

---

## Available Skills

### Core Skills (Always Loaded)

| Skill | Type | Purpose | Status |
|-------|------|---------|--------|
| [truth-seeking](./truth-seeking.yaml) | Simple | Validate assumptions before acting | ✅ Implemented |
| [task-selection](./task-selection.yaml) | Simple | Select next task from STATE.yaml | ✅ Implemented |
| [run-initialization](./run-initialization.yaml) | Simple | Set up new run folder | ✅ Implemented |
| [git-commit](./git-commit.yaml) | Simple | Safe commit to dev branch | ✅ Implemented |

### Specialized Skills (Invoke as Needed)

| Skill | Type | Purpose | Source | Status |
|-------|------|---------|--------|--------|
| [deep-research](./deep-research.yaml) | Agent | Research with 4D analysis | BB5 | ✅ Implemented |
| [code-implementation](./code-implementation.yaml) | Agent | TDD implementation | BMAD Amelia | ✅ Implemented |
| [architecture-design](./architecture-design.yaml) | Agent | System architecture | BMAD Winston | ✅ Implemented |
| [testing-validation](./testing-validation.yaml) | Simple | Test and verify | BB5 | ✅ Implemented |
| [codebase-navigation](./codebase-navigation.yaml) | Simple | Navigate codebases | BB5 | ✅ Implemented |
| [supabase-operations](./supabase-operations.yaml) | Simple | Database operations | BB5 | ✅ Implemented |
| [product-planning](./product-planning.yaml) | Agent | PRDs and requirements | BMAD Alex | ✅ Implemented |
| [documentation](./documentation.yaml) | Simple | Create documentation | BMAD John | ✅ Implemented |

---

## Skill Index

```yaml
skills:
  # Core - Always Available
  - id: truth-seeking
    file: truth-seeking.yaml
    type: simple
    category: core
    status: implemented

  - id: task-selection
    file: task-selection.yaml
    type: simple
    category: core
    status: implemented

  - id: run-initialization
    file: run-initialization.yaml
    type: simple
    category: core
    status: implemented

  - id: git-commit
    file: git-commit.yaml
    type: simple
    category: core
    status: implemented

  # Specialized - Invoke as Needed
  - id: deep-research
    file: deep-research.yaml
    type: agent
    category: research
    source: bb5-adaptation
    status: implemented

  - id: code-implementation
    file: code-implementation.yaml
    type: agent
    category: development
    source: bmad-amelia-adaptation
    status: implemented

  - id: architecture-design
    file: architecture-design.yaml
    type: agent
    category: design
    source: bmad-winston-adaptation
    status: implemented

  - id: testing-validation
    file: testing-validation.yaml
    type: simple
    category: quality
    source: bb5-adaptation
    status: implemented

  - id: codebase-navigation
    file: codebase-navigation.yaml
    type: simple
    category: utility
    source: bb5-adaptation
    status: implemented

  - id: supabase-operations
    file: supabase-operations.yaml
    type: simple
    category: database
    source: bb5-adaptation
    status: implemented

  - id: product-planning
    file: product-planning.yaml
    type: agent
    category: product
    source: bmad-alex-adaptation
    status: implemented

  - id: documentation
    file: documentation.yaml
    type: simple
    category: documentation
    source: bmad-john-adaptation
    status: implemented
```

---

## Templates

See [templates/](./templates/) for skill templates:
- [Simple Skill](./templates/simple-skill.yaml)
- [Complex Skill](./templates/complex-skill/)
- [Agent Skill](./templates/agent-skill.yaml)

---

## BB5 → Legacy Skill Mapping

### BB5 Skills Adapted

| BB5 Skill | Legacy Equivalent | Priority | Status |
|-----------|-------------------|----------|--------|
| `deep-research.md` | `deep-research.yaml` | High | ✅ Done |
| `repo-codebase-navigation.md` | `codebase-navigation.yaml` | High | ✅ Done |
| `supabase-ddl-rls.md` | `supabase-operations.yaml` | High | ✅ Done |
| `testing-playbook.md` | `testing-validation.yaml` | High | ✅ Done |
| `siso-tasks/` | `task-selection.yaml` | High | ✅ Done |
| `auto-claude/` | `code-implementation.yaml` | High | ✅ Done |
| `feedback-triage.md` | *Not adapted* | Medium | ⏸️ Deferred |

### BMAD Agents Converted to Skills

| BMAD Agent | Legacy Skill | Key Capability | Status |
|------------|--------------|----------------|--------|
| **Amelia** (Dev) | `code-implementation.yaml` | TDD, red-green-refactor | ✅ Done |
| **Winston** (Architect) | `architecture-design.yaml` | System design, patterns | ✅ Done |
| **Alex** (PM) | `product-planning.yaml` | PRDs, requirements | ✅ Done |
| **John** (Tech Writer) | `documentation.yaml` | Docs, examples | ✅ Done |
| **Mary** (Analyst) | *Part of deep-research* | Research, insights | ✅ Done |
| **Analyst** | *Part of deep-research* | 4D analysis | ✅ Done |
| **UX Designer** | *Not converted* | User flows, wireframes | ⏸️ Deferred |
| **SM** (Scrum Master) | *Not converted* | Sprint management | ⏸️ Deferred |
| **TEA** (Team Assistant) | *Not converted* | Communication | ⏸️ Deferred |

---

## Skill vs Agent Differentiation

| Aspect | Skill | Agent |
|--------|-------|-------|
| **Identity** | None | Has persona (name, role) |
| **State** | Stateless | Maintains state |
| **Autonomy** | Follows steps | Makes decisions |
| **Invocation** | Direct call | Can be delegated |
| **Scope** | Single action | Multi-step workflow |
| **Example** | `validate-assumption` | `Amelia-code-implementation` |

**Rule:** An agent IS a skill with:
- Persona definition
- State management
- Delegation capability
- Multi-step autonomy

---

## Usage

### Invoke a Simple Skill

```markdown
Using skill:truth-seeking
Validate assumption: "The database uses UUIDs"
```

### Invoke an Agent Skill

```markdown
Delegate to agent:code-implementation
Task: "Implement user authentication"
Context: [story file]
```

### Skill Self-Invocation

Skills can invoke other skills:
```yaml
process:
  - step: Validate assumption
    skill: truth-seeking
    input: "{{assumption}}"
  - step: Research if needed
    skill: deep-research
    condition: "confidence < 0.7"
```

---

## Creating New Skills

1. Copy template from [templates/](./templates/)
2. Fill in YAML front matter
3. Write process/documentation
4. Add to this README index
5. Test before relying on

---

## Summary

**Total Skills Implemented:** 12
- Core: 4
- Specialized: 8

**BB5 Skills Adapted:** 6 of 7 (86%)
**BMAD Agents Converted:** 5 of 9 (56%)

All critical skills for Legacy's autonomous operation are now implemented.
