# Decisions - TASK-1769896000

## Weighted Scoring Components

**Context:** Needed to determine how to calculate an overall effectiveness score from multiple metrics.

**Selected:** Weighted composite with 5 components
- Success Rate: 35% (highest priority)
- Time Efficiency: 25%
- Trigger Accuracy: 20%
- Quality Score: 15%
- Reuse Rate: 5%

**Rationale:**
- Success rate is most important - a skill that doesn't help complete tasks is not useful
- Time efficiency balances speed with quality (not just fast, but effective)
- Trigger accuracy ensures we're using skills appropriately
- Quality score captures outcome excellence
- Reuse rate indicates long-term value

**Reversibility:** MEDIUM - Weights can be adjusted based on data, but will affect historical comparisons

## Separate Files for Usage vs Metrics

**Context:** Decided whether to extend skill-usage.yaml or create a new file.

**Selected:** Create new skill-metrics.yaml file

**Rationale:**
- skill-usage.yaml focuses on raw counts and invocation tracking
- skill-metrics.yaml focuses on calculated effectiveness and ROI
- Separation allows independent updates and versioning
- Clearer mental model: usage = input, metrics = analysis
- Consistent with operations/ pattern (context-gathering.yaml, validation-checklist.yaml)

**Reversibility:** HIGH - Could merge later if needed, but separation is cleaner

## Null vs Zero for Initial Values

**Context:** Decided how to represent "no data yet" for metrics.

**Selected:** Use null for all initial metric values

**Rationale:**
- Distinguishes "no data" from "zero performance"
- Prevents misleading calculations (e.g., averaging nulls vs zeros)
- Clearer for consumers of the data
- Allows conditional logic: "if metric is null, show 'insufficient data'"

**Reversibility:** HIGH - Can change to 0 if tools require it

## Baseline Minutes Estimation

**Context:** Needed baseline times for each skill to calculate time efficiency.

**Selected:** Estimated baselines based on skill purpose and typical task complexity

**Rationale:**
- bmad-architect: 60 min (complex design work)
- bmad-quick-flow: 15 min (simple tasks)
- core skills: 5-10 min (quick operations)
- Baselines represent estimated time WITHOUT using the skill
- Will refine based on actual data

**Reversibility:** HIGH - Baselines can be adjusted as real data comes in

## Manual vs Automated Task Outcome Recording

**Context:** Decided how task outcomes get into the system.

**Selected:** Manual recording initially, with automation potential

**Rationale:**
- Manual ensures thoughtful evaluation (quality ratings, trigger accuracy)
- Some fields require human judgment (would_use_again, notes)
- Can automate population from run completion later
- task_outcomes structure supports both approaches

**Reversibility:** HIGH - Can add automation without changing schema

## Weekly Review Cycle

**Context:** Decided how often to calculate and review metrics.

**Selected:** Weekly calculation, monthly deep review

**Rationale:**
- Weekly keeps metrics fresh without excessive overhead
- Monthly allows pattern identification
- Balances responsiveness with effort
- next_calculation_due field tracks schedule

**Reversibility:** HIGH - Can adjust frequency based on task volume
