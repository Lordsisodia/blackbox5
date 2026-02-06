# TASK-SSOT-035: Consolidate Communication Channels

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 60

---

## Objective

Extract analysis data from embedded report files into separate structured analysis files to enable aggregation, improve queryability, and separate data from interpretation.

---

## Success Criteria

- [ ] Extraction script created to parse analysis from reports
- [ ] All existing reports processed and analysis files created
- [ ] Analysis files follow standardized schema
- [ ] Analysis index created for searchability
- [ ] Report generators updated to create separate analysis files

---

## Context

Analysis is currently embedded within report files:
- Scout reports contain raw data + analysis together
- Verifier reports contain tests + analysis together
- No separation between data and interpretation

This creates:
1. **Extraction Difficulty**: Hard to get just the analysis without parsing entire reports
2. **Mixed Concerns**: Data and analysis together violates separation of concerns
3. **No Aggregation**: Cannot easily aggregate analysis across multiple reports
4. **Duplication**: Same analysis patterns repeated in multiple reports

---

## Approach

### Phase 1: Create Extraction Script (2 hours)
1. Build Python script to extract analysis from reports
2. Parse scout reports and extract findings with analysis
3. Parse verifier reports and extract test analysis
4. Output structured analysis files

### Phase 2: Run Extraction (1 hour)
1. Process all existing reports in `.autonomous/analysis/reports/`
2. Create corresponding analysis files in `.autonomous/analysis/analyses/`
3. Verify extraction accuracy
4. Handle edge cases

### Phase 3: Update Report Generation (1 hour)
1. Update scout report generator to create separate analysis file
2. Update verifier report generator
3. Ensure analysis references source report ID

### Phase 4: Create Analysis Index (1 hour)
1. Build searchable index of all analyses
2. Enable filtering by category, severity, date
3. Support trend analysis across reports

---

## Rollback Strategy

If separate analysis files cause issues:
1. Keep embedded analysis in reports during transition
2. Can regenerate analysis files from reports if needed
3. Document relationship between reports and analyses

---

## Notes

**Key Insight:** This follows the Single Source of Truth principle:
- Reports = raw data (what was found)
- Analyses = interpretation (what it means)

**Directory Structure:**
```
.autonomous/analysis/
├── reports/
│   └── scout-report-20260205.yaml      # Raw data
├── analyses/
│   └── scout-report-20260205.analysis.yaml  # Analysis
└── index.yaml                          # Searchable index
```

**Analysis Schema:**
- analysis_id: Unique identifier
- report_id: Reference to source report
- summary: Overall assessment and confidence
- key_findings: Structured findings with recommendations
- trends: Pattern analysis across time
