# RALF Integration Plan

**Objective:** Integrate Superintelligence Protocol into RALF (Recursive Autonomous Learning Framework)
**Status:** Planning Phase
**Last Updated:** 2026-01-31

---

## Current RALF Architecture

```
RALF Execution Flow
===================
bin/ralf
    ↓
2-engine/.autonomous/shell/ralf-loop.sh  (Main loop)
    ↓
Phase: Check tasks/active/
    ↓
If tasks exist → Execute ONE task
    ↓
Phase: Execution with BMAD skills
    ↓
Integration checks
    ↓
Git commit + push
    ↓
<promise>COMPLETE</promise>
    ↓
Loop continues
```

**Key Components:**
- `ralf-loop.sh` - Main execution loop (489 lines)
- `ralf.md` - Agent-2.5 prompt with BMAD workflow
- `skill_router.py` - Routes to 9 BMAD roles
- `phase_gates.py` - Validates phase exit criteria
- `decision_registry.py` - Tracks decisions with reversibility

---

## Integration Strategy: 4 Phases

### Phase 1: Protocol as BMAD Skill (Week 1)

**Goal:** Superintelligence Protocol available as a skill RALF can invoke

**Implementation:**

1. **Create Protocol Skill File**
   ```
   2-engine/.autonomous/skills/superintelligence-protocol.md
   ```

2. **Add to Skill Router**
   ```python
   # In skill_router.py
   SkillRole.SUPERINTELLIGENCE = {
       "name": "Superintelligence Protocol",
       "agent": "Protocol",
       "file": "superintelligence-protocol.md",
       "keywords": [
           "protocol", "superintelligence", "deep analysis",
           "architecture decision", "complex problem", "multi-dimensional"
       ],
       "weight": 1.5
   }
   ```

3. **Add Route Command**
   ```yaml
   # In routes.yaml
   - command: "SP"  # Superintelligence Protocol
     skill: "superintelligence-protocol"
     description: "Activate superintelligence protocol for complex tasks"
     usage: "SP <task description>"
   ```

**When RALF Uses It:**
- Task complexity exceeds threshold
- Keywords detected: "architecture", "design", "complex"
- No clear BMAD skill match

---

### Phase 2: Protocol-Enhanced Task Creation (Week 2)

**Goal:** When no tasks exist, use Superintelligence Protocol to identify improvements

**Implementation:**

1. **Modify ralf-loop.sh** (around line 91-114)
   ```bash
   # Current logic:
   if [ "$PENDING_TASKS" -gt 0 ]; then
       # Execute existing task
   else
       # Create first-principles analysis task
   fi

   # Enhanced logic:
   if [ "$PENDING_TASKS" -gt 0 ]; then
       # Execute existing task
   else
       # Run Superintelligence Protocol analysis
       log_phase "protocol-analysis"
       run_superintelligence_analysis

       # Create task from protocol recommendations
       create_task_from_protocol_output
   fi
   ```

2. **Create Protocol Analysis Script**
   ```python
   # 2-engine/.autonomous/lib/protocol_analysis.py
   def run_superintelligence_analysis():
       """
       When no tasks exist, use protocol to identify improvements.
       """
       # Step 1: Context Gathering
       context = gather_context()

       # Step 2: First Principles Analysis
       gaps = analyze_for_gaps(context)

       # Step 3: Multi-Perspective Assessment
       assessments = run_expert_assessments(gaps)

       # Step 4: Synthesize Recommendations
       recommendations = synthesize_recommendations(assessments)

       # Step 5: Create Tasks
       for rec in recommendations:
           create_task(rec)
   ```

**What It Does:**
- Scans recent runs for patterns
- Identifies gaps in system
- Uses expert roles to assess priorities
- Creates tasks from protocol recommendations

---

### Phase 3: Protocol Decision Gates (Week 3)

**Goal:** Add protocol validation as phase in RALF workflow

**Implementation:**

1. **Extend Phase Gates**
   ```python
   # In phase_gates.py
   PROTOCOL_GATE = {
       "name": "protocol_validation",
       "entry_check": "execute",
       "required_files": [
           "protocol_analysis.md",
           "expert_assessments.json"
       ],
       "exit_criteria": [
           "multi_perspective_analysis_complete",
           "assumptions_documented",
           "confidence_score_calculated"
       ]
   }
   ```

2. **Modify ralf.md Prompt**
   ```markdown
   ## Step 4: Execute (Protocol-Enhanced)

   For complex tasks (> 2 hours or high uncertainty):
   1. Activate Superintelligence Protocol
   2. Run Context Gathering (Project Scanner)
   3. Deploy Expert Agents (Architect, Critic, etc.)
   4. Synthesize recommendations
   5. Proceed with BMAD workflow using protocol insights
   ```

**When It Triggers:**
- Task estimated > 2 hours
- Confidence < 70%
- Keywords: "architecture", "redesign", "complex"

---

### Phase 4: Autonomous Protocol Execution (Week 4+)

**Goal:** Protocol runs automatically to improve RALF itself

**Implementation:**

1. **Self-Improvement Loop**
   ```python
   # Every N loops, run protocol on RALF itself
   if loop_count % 10 == 0:
       activate_superintelligence_protocol(
           task="Analyze RALF performance and identify improvements",
           context=["ralf-metrics.jsonl", "recent-runs/"]
       )
   ```

2. **Protocol Metrics Integration**
   ```python
   # Track protocol effectiveness
   protocol_metrics = {
       "activations": count,
       "confidence_scores": [],
       "expert_roles_used": {},
       "improvements_identified": [],
       "task_success_rate": rate
   }
   ```

---

## Specific Integration Points

### 1. Context Gathering Integration

**Current:** RALF loads context manually from files
**Enhanced:** Use Project Scanner Agent

```python
# In ralf-loop.sh or ralf.md
if task_complexity == "high":
    # Deploy context gatherer sub-agent
    context = deploy_sub_agent(
        role="context_gatherer",
        task=current_task,
        scan_projects=["blackbox5"],
        scan_folders=["2-engine/", "6-roadmap/"]
    )
    # Use gathered context instead of manual loading
```

### 2. Expert Role Integration

**Current:** BMAD skills (PM, Architect, Dev, QA)
**Enhanced:** Add Superintelligence expert roles

```python
# When task is ambiguous or complex
experts = ["Architect", "Critic", "Researcher"]
for expert in experts:
    assessment = deploy_expert_agent(
        role=expert,
        task=current_task,
        context=gathered_context
    )
    assessments.append(assessment)

# Synthesize before proceeding
consensus = synthesize_expert_opinions(assessments)
```

### 3. Decision Registry Enhancement

**Current:** Tracks decisions with reversibility
**Enhanced:** Add protocol-aware decision criteria

```python
# In decision_registry.py
def record_decision(decision, protocol_enhanced=False):
    entry = {
        "decision": decision,
        "reversibility": assess_reversibility(decision),
        "protocol_enhanced": protocol_enhanced,
        "confidence": calculate_confidence(decision),
        "expert_assessments": get_expert_input() if protocol_enhanced else None
    }
    registry.add(entry)
```

### 4. Skill Router Enhancement

**Current:** Routes to BMAD skills based on keywords
**Enhanced:** Route to protocol for complex tasks

```python
# In skill_router.py
def route_task(task_description):
    # Check if protocol should be activated
    if should_activate_protocol(task_description):
        return SkillRole.SUPERINTELLIGENCE

    # Otherwise, use normal BMAD routing
    return standard_route(task_description)

def should_activate_protocol(task):
    indicators = [
        "architecture" in task.lower(),
        "design" in task.lower(),
        "complex" in task.lower(),
        len(task.split()) > 50,  # Long descriptions
        "uncertain" in task.lower()
    ]
    return sum(indicators) >= 2
```

---

## Implementation Files to Create

| File | Purpose | Phase |
|------|---------|-------|
| `skills/superintelligence-protocol.md` | Protocol skill definition | 1 |
| `lib/protocol_engine.py` | Protocol execution logic | 1 |
| `lib/protocol_analysis.py` | Analysis when no tasks exist | 2 |
| `shell/protocol-hook.sh` | Hook into ralf-loop.sh | 2 |
| `config/protocol.yaml` | Protocol configuration | 3 |
| `tasks/TEMPLATE-protocol.md` | Protocol task template | 3 |
| `metrics/protocol-metrics.json` | Track effectiveness | 4 |

---

## Testing Strategy

### Test 1: Protocol Skill Invocation
```bash
# Manual test
ralf SP "Analyze the memory system architecture"
# Should activate protocol and use expert roles
```

### Test 2: Automatic Activation
```bash
# Create task with complexity keywords
ralf "Design new authentication architecture"
# Should automatically trigger protocol
```

### Test 3: No-Tasks Analysis
```bash
# Clear all tasks and run RALF
rm 5-project-memory/blackbox5/.autonomous/tasks/active/*
ralf
# Should run protocol analysis and create tasks
```

### Test 4: Metrics Tracking
```bash
# Run 10 loops, check protocol metrics
tail -50 5-project-memory/blackbox5/.autonomous/ralf-metrics.jsonl
# Should show protocol activations and confidence scores
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Protocol Activations | >20% of complex tasks | Count in logs |
| Expert Role Usage | All 5 roles used | Role frequency |
| Context Gathering | <30 seconds | Timing logs |
| Task Quality | Reduced rework | Reopen rate |
| Confidence Scores | >85% average | Protocol output |
| RALF Self-Improvement | 1 improvement per 10 loops | Protocol recommendations |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Protocol adds too much overhead | Only activate for complex tasks (>2 hours) |
| Context gathering is slow | Implement caching, parallel scans |
| Expert roles conflict | Use consensus mechanism, track disagreements |
| Loop time increases | Time-box protocol phases (max 5 min) |
| False positives on activation | Tune activation criteria with feedback |

---

## Next Steps

1. **Create Protocol Skill** (Phase 1)
   - Write `skills/superintelligence-protocol.md`
   - Add to `skill_router.py`
   - Add route to `routes.yaml`

2. **Test Manual Activation**
   - Run `ralf SP "test task"`
   - Verify expert roles deploy
   - Check output format

3. **Implement Automatic Activation** (Phase 2)
   - Modify `ralf-loop.sh`
   - Create `protocol_analysis.py`
   - Test no-tasks scenario

4. **Deploy and Monitor** (Phase 3-4)
   - Run for 1 week
   - Collect metrics
   - Tune activation criteria
   - Document learnings

---

**Ready to implement?** Start with Phase 1 (Protocol Skill) and test manual activation.
