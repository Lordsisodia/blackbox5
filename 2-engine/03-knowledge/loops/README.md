# Thought Loop Framework

A framework for iterative first-principles reasoning with assumption validation and convergence detection. Enables AI agents to think deeply about problems and converge on high-confidence answers through research and self-questioning.

## Overview

The Thought Loop Framework implements a cognitive process where an AI agent:

1. **States current understanding** of a problem
2. **Identifies assumptions** made in that understanding
3. **Questions each assumption** - "Is this true?", "What evidence supports it?"
4. **Researches to validate assumptions** using git history, codebase search, etc.
5. **Updates understanding** based on findings
6. **Applies first-principles check** - "Do you even need to do this?"
7. **Checks for convergence** - Has confidence stabilized ≥90%?
8. **Repeats** until converged or max iterations (10)
9. **Auto-saves to project memory** - Sessions, insights, patterns, and metrics

## Installation

The framework is part of Blackbox5. No additional installation required.

## Quick Start

```python
import asyncio
from thought_loop import ThoughtLoop

async def main():
    # Create a thought loop (auto-saves to project memory by default)
    loop = ThoughtLoop()

    # Run it on a problem
    result = await loop.run("Should we add caching to this system?")

    # Check results
    if result.converged:
        print(f"Answer: {result.answer}")
        print(f"Confidence: {result.confidence:.1%}")
    else:
        print(f"Best effort after {result.final_iteration} iterations")
        print(f"Answer: {result.answer}")

    # See the reasoning trace
    for trace in result.reasoning_trace:
        print(trace)

asyncio.run(main())
```

## Project Memory Integration

The Thought Loop Framework automatically integrates with Blackbox5's project memory system:

### Automatic Saving

By default, every thought loop session is automatically saved to:
```
blackbox5/5-project-memory/{project_id}/operations/agents/history/sessions/thought-loop/
```

### Saved Data

- **sessions.json** - All session records with iterations, confidence, and answers
- **insights.json** - Extracted insights from assumptions and fallacies detected
- **patterns.json** - Learned patterns across sessions (convergence, decisions)
- **metrics.json** - Performance and quality metrics

### Archived Sessions

Sessions are automatically archived to:
```
blackbox5/5-project-memory/{project_id}/knowledge/research/thought-loop-framework/sessions/{year}/{month}/
```

### Configuration

```python
# Custom project ID
loop = ThoughtLoop(project_id="my-project")

# Disable auto-save
loop = ThoughtLoop(auto_save=False)

# Custom project memory path
loop = ThoughtLoop(
    project_memory_path=Path("/custom/path/to/project-memory")
)
```

### Retrieving Session Data

```python
from thought_loop import ProjectMemoryIntegration

memory = ProjectMemoryIntegration(project_id="siso-internal")

# Get recent sessions
sessions = await memory.get_recent_sessions(limit=10)

# Get learned patterns
patterns = await memory.get_patterns()

# Get insights
insights = await memory.get_insights()

# Get metrics
metrics = await memory.get_metrics()
```

## Components

### 1. ThoughtLoop (Main Orchestration)

```python
from thought_loop import ThoughtLoop

loop = ThoughtLoop(
    max_iterations=10,           # Maximum iterations to run
    confidence_threshold=0.90,   # Target confidence for convergence
    project_root=Path.cwd(),     # For internal research
)

result = await loop.run(
    "Problem to analyze",
    context="Additional context",
    progress_callback=lambda it: print(f"Iteration {it.iteration_number}: {it.confidence:.1%}")
)
```

### 2. AssumptionIdentifier

Extracts and classifies assumptions from reasoning text:

```python
from assumption_identifier import AssumptionIdentifier

identifier = AssumptionIdentifier()

assumptions = await identifier.identify(
    "I assume caching will improve performance",
    context="Discussion about optimization"
)

# Prioritize by importance
prioritized = identifier.prioritize(assumptions)
```

### 3. ValidationModule

Validates assumptions through research:

```python
from validation import ValidationModule
from models import Assumption, AssumptionType

validator = ValidationModule(project_root=Path.cwd())

assumption = Assumption(
    "Caching improves performance",
    AssumptionType.IMPORTANT
)

validation = await validator.validate(assumption)

print(f"Validity: {validation.validity}")
print(f"Supporting evidence: {len(validation.supporting_evidence)}")
print(f"Contradicting evidence: {len(validation.contradicting_evidence)}")
```

### 4. FirstPrinciplesChecker

Asks "Do you even need to do this?":

```python
from first_principles_checker import FirstPrinciplesChecker

checker = FirstPrinciplesChecker()

check = await checker.check(
    "We should optimize the database",
    problem="Performance is slow"
)

print(f"Necessary: {check.necessary}")
print(f"Reasoning: {check.reasoning}")
print(f"Alternatives: {check.alternatives}")
```

### 5. ConvergenceDetector

Detects when reasoning has stabilized:

```python
from convergence import ConvergenceDetector
from models import Iteration

detector = ConvergenceDetector(confidence_threshold=0.90)

# Check if converged
if detector.has_converged(iterations):
    print("Converged!")
else:
    reason = detector.get_convergence_reason(iterations)
    print(f"Not converged: {reason}")
```

## Data Models

```python
from models import (
    Assumption,           # An extracted assumption
    AssumptionType,       # CRITICAL, IMPORTANT, MINOR
    AssumptionValidation, # Result of validating an assumption
    Validity,             # VALID, INVALID, UNCERTAIN
    Evidence,             # A piece of evidence from research
    FirstPrinciplesCheck, # Result of first-principles validation
    Iteration,            # A single thought loop iteration
    ThoughtLoopResult,    # Final result from running thought loop
)
```

## Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_models.py -v

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=html
```

## Running Demo

```bash
python3 demo.py
```

The demo will show:
- Basic thought loop usage
- Progress callbacks
- First-principles validation
- Assumption identification
- Assumption validation
- State persistence

## Example: Caching Decision

The classic example from the documentation:

```python
from thought_loop import ThoughtLoop

loop = ThoughtLoop()

result = await loop.run(
    "Should we add caching when only 11% of time is spent on data fetching?"
)

# Expected answer: NO - caching optimization on the wrong bottleneck
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ThoughtLoop Engine                        │
│                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │   Problem  │ -> │ Iteration │ -> │  Research  │       │
│  │    Input   │    │   Logic    │    │   Engine   │       │
│  └────────────┘    └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────┐    ┌────────────┐       │
│                      │Assumption  │    │ Validation │       │
│                      │Identifier  │    │  Module    │       │
│                      └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────┐    ┌────────────┐       │
│                      │ First      │    │ Convergence│       │
│                      │ Principles │    │  Detector  │       │
│                      │   Check    │    │            │       │
│                      └────────────┘    └────────────┘       │
│                             │                │              │
│                             v                v              │
│                      ┌────────────────────────────────┐   │
│                      │     Result Generator          │   │
│                      │  (Final understanding +        │   │
│                      │   confidence + answer)         │   │
│                      └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### Convergence Threshold

Higher threshold = more iterations, higher confidence required:

```python
loop = ThoughtLoop(confidence_threshold=0.95)  # Require 95% confidence
```

### Max Iterations

Circuit breaker to prevent infinite loops:

```python
loop = ThoughtLoop(max_iterations=5)  # Stop after 5 iterations
```

### Research Sources

Control what research sources are used:

```python
from validation import ValidationModule

validator = ValidationModule(
    project_root=Path.cwd(),
    enable_web_search=False,      # Disable external web search
    enable_semantic_search=True   # Use semantic codebase search
)
```

## Persistence

Save and load thought loop state:

```python
# Save state
loop.save_state(Path("state.json"))

# Load into new loop
new_loop = ThoughtLoop()
new_loop.load_state(Path("state.json"))
```

## Performance

- **Per iteration**: ~0.1-1 second (depends on research complexity)
- **Max time (10 iterations)**: ~1-10 seconds
- **Typical convergence**: 2-5 iterations
- **Memory**: Minimal (<1MB for full trace)

## Limitations

1. **Heuristic-based**: Without LLM integration, uses pattern matching
2. **Research quality**: Depends on available data sources
3. **Git history**: Requires project to be a git repository
4. **Semantic search**: Requires chromadb and sentence-transformers

## Enhanced Components (for Deeper Analysis)

The framework includes advanced components for deeper logical analysis:

### 6. LogicalValidator

Detects fallacies and validates reasoning structure:

```python
from logical_validator import LogicalValidator

validator = LogicalValidator()

result = validator.validate(
    "You can't trust his policy - he's divorced!"
)

# Check for fallacies
for fallacy in result.fallacies:
    print(f"{fallacy.fallacy_type}: {fallacy.description}")

# Validate inference steps
step_result = validator.validate_inference_step(
    premise="If P then Q",
    conclusion="Q, therefore P",
    reasoning_type="deductive"
)
```

### 7. SocraticQuestioner

Systematic questioning for deeper analysis:

```python
from socratic_questioner import SocraticQuestioner

questioner = SocraticQuestioner()

# Generate questions of all types
questions = questioner.question(
    "We should implement caching to improve performance."
)

# Facilitate complete dialogue
session = questioner.facilitate_dialogue(
    "Implementing this feature will improve satisfaction.",
    max_rounds=6
)

for round_data in session.rounds:
    print(f"Round {round_data.round_number}: {round_data.question_type}")
    for q in round_data.questions:
        print(f"  - {q}")
```

### 8. BayesianUpdater

Proper confidence updating using Bayes' theorem:

```python
from bayesian_updater import BayesianUpdater

updater = BayesianUpdater()

# Update belief with evidence
update = updater.update_with_evidence(
    prior=0.5,
    evidence=[
        Evidence(text="Study shows improvement", source="research", supports=True),
        Evidence(text="Counter-example found", source="test", supports=False),
    ],
    hypothesis="Caching helps"
)

print(f"Prior: {update.prior:.2%}")
print(f"Posterior: {update.posterior:.2%}")
print(f"Confidence interval: {update.confidence_interval}")

# Sequential updates
belief_state = updater.sequential_update(
    initial_prior=0.5,
    evidence_list=[
        [Evidence(text=f"Evidence {i}", source="test", supports=True)]
        for i in range(5)
    ]
)
```

### 9. ChainOfThoughtVerifier

Makes reasoning explicit and verifiable:

```python
from chain_of_thought import ChainOfThoughtVerifier

verifier = ChainOfThoughtVerifier()

# Parse reasoning into steps
chain = verifier.parse_reasoning_chain(
    "First, we analyze the data. Then we identify patterns. "
    "Therefore, we conclude X."
)

# Verify the chain
verification = verifier.verify_chain(chain)

print(f"Valid: {verification.is_valid}")
print(f"Confidence: {verification.confidence_score:.2%}")
print(f"Weak links: {verification.weak_links}")

# Improve based on verification
improved = verifier.improve_chain(chain, verification)
```

### 10. FiveWhysAnalyzer

Root cause analysis through systematic questioning:

```python
from five_whys import FiveWhysAnalyzer

analyzer = FiveWhysAnalyzer()

# Analyze with provided answers
result = analyzer.analyze_with_answers(
    problem="Server keeps crashing",
    answers=[
        "Because database connections are exhausted",
        "Because connections aren't being closed",
        "Because the code has a connection leak",
        "Because there's no connection pool validation",
        "Because there's no pre-deployment testing process"
    ]
)

print(f"Root cause: {result.root_cause}")
print(f"Type: {result.root_cause_type}")
print(f"Solutions: {result.suggested_solutions}")

# Check for blame-focused analysis
warnings = analyzer.check_for_blame(result.levels)
if warnings:
    for warning in warnings:
        print(f"Warning: {warning}")
```

## Enhanced Capabilities Summary

The enhanced components address four key requirements:

1. **Not Hallucinating** (LogicalValidator):
   - Detects formal and informal fallacies
   - Validates argument structure
   - Tests for counterexamples
   - Assesses reasoning type appropriateness

2. **Thinking Logically** (SocraticQuestioner):
   - Generates 6 types of systematic questions
   - Uncovers hidden assumptions
   - Examines evidence quality
   - Explores alternative perspectives
   - Considers implications

3. **Breaking Down Logic** (BayesianUpdater, FiveWhysAnalyzer):
   - Explicit Bayesian belief updating
   - Quantifies uncertainty in beliefs
   - Detects overconfidence
   - Root cause analysis via Five Whys
   - Systemic vs. surface issue identification

4. **Knowing Decisions Are Correct** (ChainOfThoughtVerifier):
   - Explicit step-by-step reasoning
   - Identifies assumptions at each step
   - Validates each inference step
   - Detects weak links in reasoning
   - Provides improvement suggestions

## Future Enhancements

- LLM integration for deeper reasoning
- Web search API integration (ArXiv, GitHub, etc.)
- Parallel assumption validation
- Research result caching
- Visualization of thought process
- Integration with agent decision-making

## Related Documents

- [PLAN-008](../../../6-roadmap/03-planned/PLAN-008-implement-thought-loop-framework.md) - Implementation plan
- [AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md](../../../6-roadmap/first-principles/AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md) - Full vision
- [BLACKBOX5-CORE-FLOW.md](../../../6-roadmap/first-principles/BLACKBOX5-CORE-FLOW.md) - Core architecture
- [FIRST_PRINCIPLES_RESEARCH.md](./FIRST_PRINCIPLES_RESEARCH.md) - Research behind enhanced components

