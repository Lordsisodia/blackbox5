# First Principles Analysis: AGENTS.md

## 1. Question the Question

**What problem are we ACTUALLY trying to solve?**

We want AI agents to work effectively in our codebase. But what does "effectively" mean?

Looking at the hooks and system, the REAL problems are:
- Agents make irreversible mistakes
- Agents lose context between sessions
- Agents don't follow our standards
- Agents work on the wrong branch
- Agents mark things "done" that aren't actually done
- Agents don't learn from past work
- Agents repeat the same mistakes

**The fundamental question**: How do we make an agent that:
1. Doesn't break things
2. Follows our standards
3. Learns and improves
4. Works transparently

## 2. Identify Assumptions

**What are we assuming to be true?**

Assumption 1: "Agents will read a long document at session start"
- Is this true? Claude has limited context
- Long documents get summarized or ignored
- What's the optimal length?

Assumption 2: "Prescriptive rules work better than descriptive reference"
- Do agents actually follow "MUST" and "ALWAYS" rules?
- Or do they need patterns and examples?

Assumption 3: "More content = better guidance"
- Could less be more?
- What if agents only need the essentials?

Assumption 4: "One AGENTS.md works for all scenarios"
- Different sessions have different needs
- Should it be contextual?

Assumption 5: "Static content is sufficient"
- What if AGENTS.md should be generated?
- What if it should adapt based on project state?

## 3. Break Down to Fundamentals

**What are the TRUE constraints?**

Constraint 1: **Context Window**
- Claude has limited context (200K tokens for Opus)
- Every token counts
- Long documents reduce available context for actual work

Constraint 2: **Agent Behavior is Hard to Control**
- Agents don't always follow instructions
- "MUST" and "ALWAYS" are often ignored
- Agents prioritize the user's request over instructions

Constraint 3: **Session State Matters**
- Is this a new session or continuing?
- What's the current git state?
- What's been done already?

Constraint 4: **Cognitive Load**
- Too many rules = agent gets confused
- Contradictory rules = agent ignores all
- Complex rules = agent misses edge cases

Constraint 5: **File Location Matters**
- Root AGENTS.md = global context
- But what about project-specific context?
- What about session-specific context?

## 4. Build Up from First Principles

**Given the fundamentals, what MUST be true?**

Truth 1: **The document must be SHORT**
- If it's too long, agents won't read it
- If it's too long, it wastes precious context
- Optimal: under 2000 tokens (~1500 words)

Truth 2: **The document must be ACTIONABLE**
- Not "here's what you CAN do"
- But "here's what you MUST do"
- Clear triggers, clear actions

Truth 3: **The document must be CONTEXTUAL**
- Different information for different scenarios
- New session vs continuing session
- Simple task vs complex project

Truth 4: **The document must be TESTABLE**
- Can we verify agents are following it?
- Are the rules measurable?
- Do hooks enforce what's in AGENTS.md?

Truth 5: **The document must ALIGN with hooks**
- If AGENTS.md says "ALWAYS log work"
- Then auto-log-activity.sh must exist and work
- No orphaned rules

## 5. What Solutions Emerge?

### Solution A: Ultra-Short AGENTS.md (Radical Minimalism)

```
# AGENTS.md

## Before You Start
1. Check git branch (must not be main/master)
2. Read WORK-LOG.md to understand context
3. Choose: Direct (1-2 files), Ralphy (3-10 files), or Planning Agent (10+ files)

## While You Work
1. Every Edit is logged automatically
2. Read the impact analysis before editing
3. Use first principles for complex problems

## Before Saying "Done"
Check: Tests pass? Docs updated? Code reviewed? No breaking changes?

## Never
- Work on main/master
- Exceed 80% context window
- Mark done without validation
```

**Pros**: Short, memorable, fits in context
**Cons**: Missing nuance, missing examples

### Solution B: Layered AGENTS.md

**Base layer** (always shown): Ultra-short version (Solution A)
**Context layers** (injected based on situation):
- "New feature" → Planning Agent workflow
- "Bug fix" → Ralphy workflow
- "Complex task" → First principles framework
- "Done detected" → Completion checklist

**Pros**: Always short, always relevant
**Cons**: Complex to implement, requires smart hooks

### Solution C: Generated AGENTS.md

**Generate AGENTS.md from project state**:
- Read git status (branch, recent commits)
- Read WORK-LOG.md (recent activity)
- Read decisions/INDEX.md (recent decisions)
- Generate contextual guidance

**Pros**: Always relevant, always up-to-date
**Cons**: Adds latency to session start, complex to build

### Solution D: Hybrid (Recommended)

**Short base AGENTS.md** + **Smart hook injection**:

AGENTS.md (ultra-short, ~200 words):
```
# HOW TO WORK IN THIS CODEBASE

## 1. Check Environment
git status  # Are you on main? Don't work on main.
git log -5 # What just happened?

## 2. Choose Your Approach
Simple (1-2 files)?  → Do it directly
Medium (3-10 files)? → Use Ralphy
Large (10+ files)?  → Use Planning Agent

## 3. Work Transparently
All edits are logged. Read the impact analysis before changing files.
Decisions go in decisions/ folder with ADR format.

## 4. Never Say "Done" Without
☐ Tests pass
☐ Docs updated
☐ Code reviewed
☐ No breaking changes

## 5. Get Help
- Stuck? Use first principles (triggered automatically)
- Context full? /compact or start new session
- Need details? Read AGENT-REFERENCE.md
```

**Hooks inject the rest**:
- First principles framework (when needed)
- Workflows (when complex task detected)
- Checklists (before "done")
- Project-specific context (from project state)

**Pros**: Best of both worlds
- Short base document (always loaded)
- Contextual guidance (injected when needed)
- Aligns with existing hook system
- Preserves context window

## 6. What This Means

### Current AGENTS.md (v2.0.0)
- ~580 words
- Comprehensive but long
- Has everything upfront

### Problems
1. Wastes context (580 words ~780 tokens)
2. Agent may not read all of it
3. Not contextual (same for every session)
4. Duplicates what hooks already inject

### Optimal AGENTS.md (Proposed v3.0.0)
- ~200 words (ultra-short)
- Only what MUST be in every session
- Let hooks inject the rest
- Base contract, not comprehensive guide

### The Trade-off

We're trading:
- Completeness → Relevance
- Length → Alignment with hooks
- Static → Dynamic

This is the RIGHT trade-off because:
- Hooks already inject guidance
- Context window is precious
- Relevance beats completeness

## 7. First Principles Verdict

**What AGENTS.md should be**:

A **minimal behavioral contract** that:
1. Fits in ~200 words
2. Covers ONLY what's not covered by hooks
3. Applies to EVERY session
4. Is TESTABLE (we can verify it's followed)

**What AGENTS.md should NOT be**:

- A comprehensive guide (that's what AGENT-REFERENCE.md is for)
- A tutorial (that's what docs/ are for)
- A workflow catalog (that's what hooks inject dynamically)
- A feature list (that's what CATALOG.md is for)

**The essential question**: What MUST the agent know BEFORE the hooks even run?

Answer:
1. What environment to check (git state)
2. What approach to choose (Direct/Ralphy/Planning)
3. What the non-negotiables are (no main branch, no "done" without validation)
4. Where to find detailed help (AGENT-REFERENCE.md)

Everything else is:
- Covered by hooks (first principles, assumptions, impact analysis)
- Covered by other docs (workflows, agents, skills)
- Can be injected contextually

This is the first-principles answer.
