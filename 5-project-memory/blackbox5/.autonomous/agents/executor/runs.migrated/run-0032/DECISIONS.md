# Decisions - TASK-1769914000

## Decision 1: Dashboard Structure

**Context:** Needed to design the schema for improvement metrics
**Selected:** Four-stage pipeline structure (Learnings → Improvements → Tasks → Completed)
**Rationale:**
- Matches actual workflow in BlackBox5
- Clear visibility into drop-off points
- Easy to calculate conversion rates at each stage
- Aligns with existing backlog structure

**Reversibility:** HIGH - Can restructure if needed

## Decision 2: Integration Approach

**Context:** How to integrate with existing executor dashboard
**Selected:** Add dedicated improvement_metrics section rather than mixing metrics
**Rationale:**
- Maintains separation of concerns
- Allows independent updates
- Prevents cluttering existing dashboard
- Provides clear reference point

**Reversibility:** MEDIUM - Could merge later if preferred

## Decision 3: Manual vs Automated Metrics

**Context:** Some metrics require subjective assessment
**Selected:** Split into automated and manual categories
**Rationale:**
- Automated: backlog counts, completion rates, dates
- Manual: impact assessment, effectiveness scores
- Clear documentation of what updates automatically
- Sets expectations for maintenance

**Reversibility:** HIGH - Can automate more over time

## Decision 4: Alert Thresholds

**Context:** Need thresholds for active alerts
**Selected:**
- Extraction rate target: 15%
- Completion rate target: 70%
- High priority target: 80%
- Velocity target: 2 improvements/day

**Rationale:**
- Based on current performance (12.5%, 40%, 0%, 4/day)
- Targets are aspirational but achievable
- Will drive focus on underperforming areas
- Can adjust based on future data

**Reversibility:** HIGH - Thresholds are configuration

## Decision 5: File Organization

**Context:** Where to place dashboard and documentation
**Selected:**
- Main dashboard: operations/improvement-metrics.yaml
- Documentation: operations/.docs/improvement-metrics-guide.md

**Rationale:**
- Consistent with existing file structure
- operations/ is the right place for operational dashboards
- .docs/ subfolder for documentation is established pattern
- Easy to discover and reference

**Reversibility:** MEDIUM - Files can be moved if structure changes
