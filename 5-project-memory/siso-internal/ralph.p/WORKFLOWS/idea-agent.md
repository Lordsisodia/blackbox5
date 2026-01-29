# Idea Generation Agent Workflow

**Purpose**: Organize documents, identify gaps, generate feature ideas
**Trigger**: Scheduled (daily at 9 AM) or on-demand
**Mode**: `idea_generation`

---

## Workflow Steps

### 1. Document Discovery

```yaml
step: discover_documents
actions:
  - Scan project for documents:
      - README files
      - PRDs
      - Architecture docs
      - Meeting notes
      - Research documents
      - User feedback

  - Categorize by:
      - Type: requirements, research, feedback, technical
      - Status: active, archived, draft
      - Project: ecommerce-client, siso-internal

  - Create document index
```

### 2. Gap Analysis

```yaml
step: analyze_gaps
actions:
  - Compare documents to STATE.yaml:
      - Are all features documented?
      - Are all requirements captured?
      - Are there orphaned documents?

  - Identify missing documentation:
      - Features without PRDs
      - PRDs without epics
      - Epics without tasks

  - Identify outdated docs:
      - Documents older than 30 days
      - Documents contradicting STATE.yaml
      - Documents with TODOs not tracked

  - Report gaps
```

### 3. Use Case Extraction

```yaml
step: extract_use_cases
actions:
  - Read all requirements documents
  - Extract use cases:
      - Actor
      - Action
      - Goal
      - Current status

  - Map use cases to features:
      - Which use cases are covered?
      - Which are not?
      - Which could be improved?

  - Create use case matrix
```

### 4. Idea Generation

```yaml
step: generate_ideas
actions:
  - Based on gaps and use cases:
      - Generate feature ideas
      - Suggest improvements
      - Identify opportunities

  - For each idea:
      - Title
      - Description
      - Problem it solves
      - Estimated effort
      - Priority (high/medium/low)
      - Project fit

  - Filter ideas:
      - Must align with project goals
      - Must be technically feasible
      - Must fit within constraints
```

### 5. Idea Evaluation

```yaml
step: evaluate_ideas
actions:
  - Score each idea:
      - Impact: 1-5
      - Effort: 1-5 (inverse)
      - Alignment: 1-5
      - Feasibility: 1-5

  - Calculate priority score:
      - Score = (Impact + Alignment + Feasibility) / Effort

  - Rank ideas by score
  - Select top ideas for PRD creation
```

### 6. PRD Creation

```yaml
step: create_prds
actions:
  - For top-ranked ideas:
      - Create PRD following template
      - Include:
          - Overview
          - Requirements (functional/non-functional)
          - Acceptance criteria
          - Technical notes
          - Open questions

  - Save to: plans/prds/proposed/
  - Add to FEATURE-BACKLOG.yaml
  - Link to any related documents
```

### 7. Documentation Update

```yaml
step: update_documentation
actions:
  - Update document index
  - Cross-reference new PRDs with existing docs
  - Update knowledge base with learnings
  - Mark outdated docs as archived
```

### 8. Report Generation

```yaml
step: generate_report
output: STATE/idea-report-{date}.yaml
content:
  - date
  - documents_scanned: N
  - gaps_found: N
  - use_cases_extracted: N
  - ideas_generated: N
  - prds_created: N
  - top_ideas:
      - title
      - score
      - prd_path
  - recommendations: []
```

---

## Decision Points

### If Too Many Ideas
```
Action: Filter aggressively
- Keep only top 10 by score
- Archive others with note
- Focus on high-impact, low-effort
```

### If No Ideas Generated
```
Action: Expand search
- Look at competitor features
- Review user feedback more deeply
- Check industry trends
- Suggest research tasks
```

### If Documents Contradict
```
Action: Flag for review
- Document contradictions
- Suggest clarification task
- Do not create PRDs until resolved
```

---

## Output

### Success
```yaml
status: success
date: "2026-01-30"
results:
  documents_scanned: 25
  gaps_found: 3
  use_cases_extracted: 12
  ideas_generated: 8
  prds_created: 3

  top_ideas:
    - title: "Auto-save for forms"
      score: 4.5
      prd: "plans/prds/proposed/auto-save.md"
    - title: "Bulk operations"
      score: 4.2
      prd: "plans/prds/proposed/bulk-ops.md"
    - title: "Export to CSV"
      score: 3.8
      prd: "plans/prds/proposed/export-csv.md"

  gaps:
    - "No PRD for checkout flow"
    - "User feedback not analyzed"
    - "Missing API documentation"

  next_actions:
    - "Review proposed PRDs"
    - "Prioritize for development"
```

### No Ideas
```yaml
status: no_ideas
date: "2026-01-30"
message: "No new ideas generated"
recommendations:
  - "Review competitor features"
  - "Gather more user feedback"
  - "Schedule brainstorming session"
```

---

## Integration with Other Agents

After idea generation:
1. Signal feature-dev agent if PRDs are approved
2. Update STATE.yaml with new features
3. Update FEATURE-BACKLOG.yaml
4. Log to WORK-LOG.md
