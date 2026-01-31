# Superintelligence Hand-Off Guide

**Purpose:** Enable automatic superintelligence activation for complex tasks
**Applies to:** RALF, Claude Code, and all SISO agents
**Status:** Active

---

## The Pattern

```
Regular Agent (limited context)
    ↓
Detects complex problem / architecture question / high uncertainty
    ↓
HAND OFF → Superintelligence Protocol
    ↓
Deploys:
  - Context gatherers (scan projects/folders)
  - Expert agents (architect, critic, researcher, synthesizer)
  - Information seekers (search, verify, test)
    ↓
Returns: Deeply researched, multi-perspective recommendation
    ↓
Regular Agent continues with enhanced understanding
```

---

## Auto-Activation Criteria

### Activate WITHOUT asking when:

| Trigger | Examples |
|---------|----------|
| **Architecture questions** | "Should we...", "How should we...", "What's the best way to..." |
| **Design decisions** | Choosing between approaches, technology selection |
| **Multi-system impact** | Changes spanning multiple components |
| **High uncertainty** | Novel problems, unclear requirements |
| **Significant decisions** | Hard to reverse, large impact |
| **Keywords detected** | architecture, design, refactor, optimize, strategy, complex, integrate |

### Don't activate for:
- Simple file edits
- Clear bug fixes
- Information lookups
- Routine tasks
- Single-file changes

---

## For RALF Integration

### 1. Add to ralf.md Prompt

Already done. RALF now auto-activates protocol for complex tasks.

### 2. Usage in RALF

```bash
# Manual activation
ralf SI "design new authentication system"

# Automatic activation (detected keywords)
ralf "Should we refactor the database layer?"
→ RALF: "I'll activate the superintelligence protocol for this."
```

### 3. What RALF Does

When protocol activates:
1. Deploys context gatherer sub-agent
2. Scans relevant projects/folders
3. Deploys expert agents (architect, critic, etc.)
4. Synthesizes recommendation
5. Returns to main RALF flow with enhanced context

---

## For Claude Code Integration

### Auto-Activation (Already Configured)

Claude Code now reads `.claude/CLAUDE.md` which includes:

```markdown
## Superintelligence Hand-Off Protocol (Auto-Activation)

**Activate the protocol WITHOUT asking when:**
- User asks architecture/design questions
- Task involves multiple files or systems
- High uncertainty or novel problem
- Keywords: architecture, design, refactor, optimize, strategy, complex, integrate
```

### What Claude Does

**Before:**
```
User: "Should we use JWT or sessions for auth?"
Claude: "JWT is good because... [shallow answer]"
```

**After:**
```
User: "Should we use JWT or sessions for auth?"
Claude: "I'll activate the superintelligence protocol for this."
      [Deploys context gatherer]
      [Scans auth code]
      [Deploys architect + researcher + critic]
      [Synthesizes analysis]
Claude: "Based on multi-perspective analysis...
        **Recommendation:** JWT with refresh tokens
        **Confidence:** 90%
        **Key Assumptions:** [X, Y]
        **Risks:** [A, B]
        **Implementation Path:** [steps]"
```

---

## For Day-to-Day Code

### Pattern: Delegate to Superintelligence

When you hit a hard problem:

```python
# Instead of:
"I think we should use Redis for caching"

# Do:
"I'll activate the superintelligence protocol for caching strategy"
→ Context gatherer scans current caching
→ Researcher finds best practices
→ Architect designs approach
→ Critic identifies risks
→ Synthesizer integrates
→ "Recommendation: Redis with fallback to in-memory..."
```

### Sub-Agent Deployment

```python
# Context gathering
deploy_sub_agent(
    role="context_gatherer",
    task="understand current auth system",
    scan_projects=["blackbox5"],
    scan_folders=["2-engine/core/auth", "6-roadmap/security"]
)

# Expert analysis
deploy_sub_agent(
    role="architect",
    task="design auth architecture",
    context=gathered_context
)

deploy_sub_agent(
    role="critic",
    task="identify auth risks",
    context=gathered_context
)
```

---

## Documentation Structure

```
superintelligence-protocol/
├── README.md                          # Main framework
├── core-framework/
│   ├── 7-dimensions.md               # Detailed methodology
│   └── activation-protocol.md        # When/how to activate
├── sub-agent-strategies/
│   ├── context-gatherers.md          # Project/folder scanning
│   ├── expert-roles.md               # 5 expert definitions
│   └── deployment-patterns.md        # When to deploy
├── implementation/
│   ├── iterative-improvement-framework.md
│   ├── batch-001-project-scanner.md  # Working implementation
│   ├── folder-scanner-agent.md       # Working implementation
│   ├── cli-interface.md              # CLI design
│   └── ralf-integration-plan.md      # RALF integration
├── meta-research/
│   └── metas-superintelligence-lab.md
└── co-superintelligence/
    ├── collective-intelligence.md
    └── trust-mechanisms.md
```

---

## Quick Reference

### Activation Phrase
```
"I'll activate the superintelligence protocol for this."
```

### 7 Steps
1. Context Gathering
2. First Principles
3. Information Gap
4. Active Research
5. Multi-Perspective
6. Meta-Cognitive Check
7. Synthesis

### Expert Roles
- **Architect** - System design
- **Researcher** - Information gathering
- **Critic** - Risk analysis
- **Implementer** - Code/execution
- **Validator** - Testing/verification

### Output Format
```
**Recommendation:** [Clear answer]
**Confidence:** [0-100%]
**Key Assumptions:** [What we're betting on]
**Risks:** [What could go wrong]
**Implementation Path:** [Next steps]
```

---

## Success Metrics

Track in `ralf-metrics.jsonl`:
- Protocol activations per day
- Expert roles used
- Average confidence score
- Time per activation
- Task success rate with/without protocol

---

## Next Steps

1. **Test Auto-Activation** - Ask Claude an architecture question, verify it activates
2. **Monitor RALF** - Check if SI command works
3. **Iterate** - Refine activation criteria based on usage
4. **Expand** - Add more expert roles as needed

---

**Status:** Active and configured
**Last Updated:** 2026-01-31
**Owner:** SISO
