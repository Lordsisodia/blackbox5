# Epistemic Iteration - Quick Reference

**One-page guide to implementing active reasoning with belief revision**

---

## The Core Loop (7 Steps)

```
Question → Decompose → Identify Gaps → Gather Info → Integrate → Meta-Check → Synthesize
                ↑___________________________________________________________|
```

---

## The Three Meta-Cognitive Questions

| Question | Purpose | Action if "Yes" |
|----------|---------|-----------------|
| **Do I need more information?** | Halting condition | Continue iteration |
| **What information do I need?** | Gap analysis | Generate search queries |
| **Am I thinking correctly?** | Bias detection | Apply corrections |

---

## Key Concepts

| Term | Definition |
|------|------------|
| **Epistemic Iteration** | Successive approximation toward truth through inquiry cycles |
| **Belief State** | Current knowledge with confidence levels |
| **Information Gap** | Difference between known and needed information |
| **Assumption Remaking** | Revising foundational beliefs based on new evidence |
| **Active Retrieval** | Dynamic information seeking vs. one-shot RAG |

---

## Code Pattern: Basic Implementation

```python
class EpistemicAgent:
    def reason(self, question, max_iterations=5):
        belief = BeliefState()

        for i in range(max_iterations):
            # Decompose and identify gaps
            gaps = self.find_gaps(question, belief)

            # Gather information
            for gap in gaps:
                evidence = self.search(gap)
                belief.update(gap, evidence)

            # Check if sufficient
            if self.is_sufficient(belief, question):
                break

        return self.synthesize(belief)
```

---

## When to Use Epistemic Iteration

| Use Epistemic Iteration | Use Simple CoT |
|------------------------|----------------|
| Complex, multi-fact problems | Simple, self-contained questions |
| Evolving/changing information | Static, well-defined domains |
| High-stakes decisions | Low-stakes, quick answers |
| Uncertain or conflicting sources | Single authoritative source |
| Novel problems without known solutions | Standard problems with known solutions |

---

## Halting Conditions

Stop iterating when:
- ✅ Knowledge coverage > 80%
- ✅ Confidence > 85%
- ✅ No critical gaps remain
- ✅ Max iterations reached (safety)
- ✅ Diminishing returns detected

---

## Multi-Agent Setup

```
Research Agent    → Gathers information
Critique Agent    → Evaluates reasoning
Skeptic Agent     → Seeks disconfirming evidence
Synthesizer Agent → Integrates findings
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Infinite loops | Hard iteration limits |
| Compounding errors | Multi-source verification |
| Confirmation bias | Active disconfirmation |
| Over-confidence | Calibration to evidence quality |
| Source bias | Diverse source selection |

---

## Integration with BlackBox5

1. **Belief State** → Connect to Memory System
2. **Information Gathering** → Use MCP tools
3. **Meta-Cognition** → Add to agent prompts
4. **Synthesis** → Output to Vibe Kanban

---

## Further Reading

- Full documentation: [README.md](./README.md)
- Tree-of-Thoughts: [../tree-of-thoughts-implementation-guide.md](../tree-of-thoughts-implementation-guide.md)
- Reflection patterns: [../reflection-self-correction-mechanisms.md](../reflection-self-correction-mechanisms.md)

---

**Last Updated:** 2026-01-31
