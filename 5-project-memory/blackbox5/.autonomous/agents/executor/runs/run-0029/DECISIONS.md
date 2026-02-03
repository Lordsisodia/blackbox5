# Decisions - TASK-1769910001

## Dashboard Format: YAML vs JSON

**Context:** Need to choose format for dashboard data
**Selected:** YAML
**Rationale:**
- More human-readable for documentation purposes
- Native support in Claude's environment
- Easy to edit manually when needed
- Comments supported (JSON doesn't allow comments)
**Reversibility:** HIGH - Can convert to JSON if needed

## Metric Granularity: Summary vs Detailed

**Context:** How much detail to include for each run
**Selected:** Summary with key fields (id, task, type, status, duration, files, skill_used)
**Rationale:**
- Full metadata available in individual run directories
- Dashboard should provide quick overview, not replace run files
- 20 runs with summary = manageable file size
**Reversibility:** MEDIUM - Can add more fields if needed

## Historical Data Range: 20 Runs

**Context:** How many historical runs to include
**Selected:** Last 20 runs
**Rationale:**
- Provides meaningful trend analysis
- Not so many that file becomes unwieldy
- Aligns with task requirement for "last 20 runs"
- Older runs still accessible in directory structure
**Reversibility:** HIGH - Can adjust range in future updates

## Alert Levels: Info/Warning/Critical

**Context:** Need consistent alert classification
**Selected:** Three-tier system
**Rationale:**
- Info: Monitor but no action needed
- Warning: Investigate within 24 hours
- Critical: Immediate attention required
- Matches common monitoring conventions
**Reversibility:** HIGH - Can add more levels if needed

## Automated vs Manual Metrics

**Context:** Some metrics can be auto-calculated, others need manual input
**Selected:** Hybrid approach with clear labeling
**Rationale:**
- Success rate, completion time: automated from metadata
- Quality scores, user satisfaction: manual assessment
- Documented which are which in dashboard
**Reversibility:** HIGH - Can automate more metrics over time
