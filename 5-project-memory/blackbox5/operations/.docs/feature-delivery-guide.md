# Feature Delivery Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Purpose:** Guide for creating, prioritizing, and delivering user-facing features

---

## Table of Contents

1. [Feature vs Improvement](#feature-vs-improvement)
2. [Feature Identification](#feature-identification)
3. [Feature Task Creation](#feature-task-creation)
4. [Feature Execution](#feature-execution)
5. [Feature Completion](#feature-completion)
6. [Examples](#examples)

---

## Feature vs Improvement

### Key Differences

| Aspect | **Improvement** | **Feature** |
|--------|----------------|-------------|
| **Purpose** | Fix problem, optimize process | Add new capability, create user value |
| **Source** | Learnings from runs, system friction | Product roadmap, strategic goals, user needs |
| **Impact** | Internal (system health, velocity) | External (user-facing value) |
| **Metrics** | Time saved, errors reduced | Features delivered, value created |
| **Example** | "Fix duration tracking" | "Add dark mode support" |
| **Template** | `.templates/tasks/task-specification.md.template` | `.templates/tasks/feature-specification.md.template` |

### Decision Tree

```
Is this task addressing a problem/gap in the existing system?
├─ YES → This is an IMPROVEMENT
│         Use: task-specification.md.template
│         Source: operations/improvement-backlog.yaml
│
└─ NO → Is this task adding NEW capability?
    ├─ YES → This is a FEATURE
    │         Use: feature-specification.md.template
    │         Source: plans/features/BACKLOG.md
    │
    └─ NO → This is OTHER (bug fix, refactor, maintenance)
               Use: task-specification.md.template
```

### Examples

**Improvement Examples:**
- "Fix duration tracking metadata bug"
- "Optimize executor startup time"
- "Improve error messages in queue sync"
- "Add validation to roadmap sync"

**Feature Examples:**
- "Multi-Agent Coordination System"
- "Advanced Skills Library Expansion"
- "Performance Monitoring Dashboard"
- "Automated Testing Framework"

---

## Feature Identification

### Where Do Features Come From?

**1. Strategic Roadmap**
- Long-term vision for BlackBox5
- Major capability additions
- Architectural evolution

**2. User Feedback**
- Feedback from feedback/incoming/
- User requests and pain points
- Usage patterns and analytics

**3. System Analysis**
- Gaps in current capabilities
- Opportunities for automation
- Competitive analysis

**4. Brainstorming**
- "What would make this system amazing?"
- "What's missing from our current capabilities?"
- "What would 10x our value?"

### Feature Prioritization

Use **Impact vs Effort** matrix:

```
        HIGH IMPACT
            ↑
            |
   Q1       |       Q2
 QUICK WIN  |  MAJOR BET
   DO IT    |  SCHEDULE IT
            |
------------+------------→ HIGH EFFORT
            |
   Q3       |       Q4
 FILLER     |  MONEY PIT
  (AVOID)   |  (AVOID)
            |
            ↓
        LOW IMPACT
```

**Priority Guidelines:**
- **Q1 (High Impact, Low Effort):** Do immediately (quick wins)
- **Q2 (High Impact, High Effort):** Schedule carefully (major bets)
- **Q3 (Low Impact, Low Effort):** Fillers (only if time permits)
- **Q4 (Low Impact, High Effort):** Avoid (money pits)

### When to Create Feature Tasks

**Create feature task when:**
- Clear user value is identified
- Success criteria can be defined
- Effort can be reasonably estimated
- Dependencies are understood
- Strategic value is evident

**Do NOT create feature task when:**
- Idea is vague or undefined
- Success criteria unclear
- Too many unknown dependencies
- Low strategic value
- Better suited as improvement

---

## Feature Task Creation

### Step 1: Use Feature Template

Use `.templates/tasks/feature-specification.md.template` for all features.

**Template sections:**
1. **User Value** - Who benefits and what problem it solves
2. **Feature Scope** - MVP vs future enhancements
3. **Context & Background** - Why this feature matters
4. **Success Criteria** - SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
5. **Technical Approach** - Implementation plan and architecture
6. **Dependencies** - Prerequisites and dependents
7. **Rollout Plan** - Testing and deployment strategy
8. **Risk Assessment** - Technical and operational risks
9. **Effort Estimation** - Breakdown by phase

### Step 2: Define User Value (CRITICAL)

Every feature MUST answer:
- **Who benefits?** (Target user or system component)
- **What problem does it solve?** (Clear problem statement)
- **What value does it create?** (Measurable benefit)

**Good user value example:**
```
Who: RALF agents (planner and executor)
Problem: Cannot collaborate on complex, multi-step tasks
Value: Enables task distribution, 3x throughput improvement
```

**Bad user value example:**
```
Who: Users
Problem: Need better stuff
Value: Improvement
```

### Step 3: Define MVP Scope

**MVP (Minimum Viable Product):**
- Core capabilities that deliver value
- Smallest testable feature
- Can be completed in 1-3 iterations

**Future Enhancements:**
- Nice-to-have capabilities
- Can be added later
- Not required for initial value

**Scope Boundaries:**
- Clearly state what's IN
- Clearly state what's OUT
- Prevents scope creep

### Step 4: Write Success Criteria

Use **SMART** criteria:
- **Specific** - Clear and unambiguous
- **Measurable** - Can verify completion
- **Achievable** - Realistic given constraints
- **Relevant** - Aligns with feature goals
- **Time-bound** - Can estimate effort

**Example success criteria:**
```
Must-Have:
- [ ] Multi-agent task distribution system implemented
- [ ] 2+ agents can collaborate on single task
- [ ] Task state synchronized across agents

Should-Have:
- [ ] Agent discovery mechanism
- [ ] Conflict resolution for concurrent updates

Nice-to-Have:
- [ ] Visual task coordination dashboard
```

### Step 5: Save Feature File

**Location:** `plans/features/FEATURE-[ID]-[slug].md`

**Example:** `plans/features/FEATURE-001-multi-agent-coordination.md`

**Add to backlog:**
- Update `plans/features/BACKLOG.md`
- Include: ID, name, priority, status, user value

---

## Feature Execution

### Claim and Execute

**For Executor:**
1. Feature task appears in `tasks/active/`
2. Claim feature (same process as improvements)
3. Execute following technical approach
4. Test and validate

**For Planner:**
1. Feature backlog review (every 5 loops)
2. Select high-priority features
3. Create feature tasks from backlog
4. Add to `tasks/active/`

### Execution Checklist

**Before starting:**
- [ ] Read feature spec completely
- [ ] Understand user value
- [ ] Verify dependencies are met
- [ ] Check for related work in runs/

**During implementation:**
- [ ] Follow MVP scope (avoid scope creep)
- [ ] Test each component
- [ ] Document decisions
- [ ] Update progress in feature file

**Before completion:**
- [ ] All acceptance criteria met
- [ ] Testing complete
- [ ] Documentation updated
- [ ] Rollout plan executed

---

## Feature Completion

### Completion Steps

1. **Verify Success Criteria**
   - Check all Must-Have criteria
   - Verify Should-Have if completed
   - Note Nice-to-Have status

2. **Testing**
   - Unit tests pass
   - Integration tests pass
   - Manual testing complete
   - Documentation reviewed

3. **Documentation**
   - Update feature file with completion date
   - Document learnings
   - Update backlog (move to completed)
   - Update events.yaml

4. **Rollout**
   - Execute deployment plan
   - Monitor metrics
   - Handle issues if they arise

5. **Move to Completed**
   - Move feature file: `plans/features/completed/`
   - Update BACKLOG.md
   - Record in events.yaml

### Feature Metrics

Track these metrics for each feature:
- **Cycle Time:** From task creation to completion
- **Effort Accuracy:** Estimated vs actual effort
- **Success Rate:** Features completed vs started
- **User Value:** Did we deliver the promised value?

---

## Examples

### Example Feature: Multi-Agent Coordination

**User Value:**
```
Who: RALF agents (planner, executor, analyst)
Problem: Cannot collaborate on complex tasks
Value: Enables parallel task execution, 3x throughput
```

**MVP Scope:**
```
IN SCOPE:
- Agent discovery mechanism
- Task distribution protocol
- State synchronization

OUT OF SCOPE:
- Visual coordination dashboard
- Advanced conflict resolution
- Auto-scaling agent pool
```

**Success Criteria:**
```
Must-Have:
- [ ] Agent can discover other agents
- [ ] Task can be split among 2+ agents
- [ ] Agent state synchronized in real-time
- [ ] Conflict resolution for concurrent updates

Verification:
- Integration test: 3 agents collaborate on single task
- Manual test: Create multi-agent task, verify completion
```

**Files to Modify:**
```
New:
- 2-engine/.autonomous/lib/agent_discovery.py
- 2-engine/.autonomous/lib/task_distribution.py
- 2-engine/.autonomous/lib/state_sync.py

Modify:
- .autonomous/prompts/planner-v2.md (add coordination capability)
- operations/.docs/agent-coordination-guide.md (create)
```

### Example Feature: Skill Usage Dashboard

**User Value:**
```
Who: RALF operators (humans monitoring system)
Problem: Cannot see skill usage patterns or effectiveness
Value: Visibility into skill system, data-driven optimization
```

**MVP Scope:**
```
IN SCOPE:
- Dashboard UI (markdown-based)
- Skill invocation metrics
- Skill effectiveness tracking

OUT OF SCOPE:
- Real-time updates
- Advanced analytics
- Custom visualization
```

**Success Criteria:**
```
Must-Have:
- [ ] Dashboard displays skill usage metrics
- [ ] Effectiveness scores calculated
- [ ] Trends visible over time
- [ ] Markdown format (viewable in GitHub)

Verification:
- Manual test: View dashboard, verify metrics accurate
- Data test: Compare dashboard vs skill-usage.yaml
```

---

## Best Practices

### DO:
- Start with user value
- Define MVP clearly
- Test incrementally
- Document decisions
- Track metrics
- Learn from failures

### DON'T:
- Scope creep (stick to MVP)
- Ignore user value
- Skip testing
- Forget documentation
- Over-engineer
- Ignore risks

---

## Related Documents

- `.templates/tasks/feature-specification.md.template` - Feature task template
- `.templates/tasks/task-specification.md.template` - Improvement task template
- `plans/features/BACKLOG.md` - Feature backlog
- `operations/improvement-backlog.yaml` - Improvement backlog
- `operations/skill-selection.yaml` - Skill selection framework

---

## FAQ

**Q: When should I create a feature vs an improvement?**
A: Use the decision tree above. If it adds NEW capability → feature. If it fixes EXISTING problem → improvement.

**Q: Can a feature be too small?**
A: Yes. If it's < 30 minutes, consider if it's actually a bug fix or minor improvement.

**Q: Can a feature be too big?**
A: Yes. Break it into smaller features. Aim for 1-3 iterations per feature.

**Q: What if I'm not sure if it's a feature or improvement?**
A: Start with improvement template. If it becomes clear it's a feature during planning, convert it.

**Q: How many features should be in the backlog?**
A: Aim for 5-10 planned features. Too many = overwhelming. Too few = no strategic vision.

**Q: How often should we review the feature backlog?**
A: Every 5 planner loops. Add new features, update priorities, archive completed features.

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial version - Feature delivery framework |
