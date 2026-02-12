# TASK-PROC-033: Learnings

## L-PROC-033-001

**Category:** Process
**Observation:** Extraction rates vary dramatically by task source. Autonomous runs (RALF) achieve 50% extraction rates while manual tasks average 5.6% for learnings and 0% for decisions.
**Action Item:** Apply RALF's structured documentation approach to manual tasks - enforce LEARNINGS.md and DECISIONS.md creation at task completion.

## L-PROC-033-002

**Category:** Process
**Observation:** Process-type tasks have the highest extraction rate (33.3%) among manual tasks, suggesting that process-focused work naturally generates more documented insights.
**Action Item:** Leverage process tasks as templates for documentation practices that can be applied to other task types.

## L-PROC-033-003

**Category:** Technical
**Observation:** Parsing unstructured learnings (bullet points) vs structured learnings (with IDs, categories) requires different regex patterns. Structured formats are more reliable for extraction tracking.
**Action Item:** Standardize on structured learning format (## L-XXX with Category/Observation/Action Item fields) for all future documentation.

## L-PROC-033-004

**Category:** Infrastructure
**Observation:** The .autonomous/runs directory contains significant documentation (4 learnings, 31 decisions) that wasn't being tracked alongside regular tasks.
**Action Item:** Always include .autonomous/runs in extraction tracking scans to get complete picture of knowledge capture.

## L-PROC-033-005

**Category:** Process
**Observation:** 85 out of 87 tasks (97.7%) are missing both learnings and decisions, indicating a systemic documentation gap rather than isolated incidents.
**Action Item:** Implement mandatory documentation checkpoints at task completion - block task closure until LEARNINGS.md exists with at least one entry.
