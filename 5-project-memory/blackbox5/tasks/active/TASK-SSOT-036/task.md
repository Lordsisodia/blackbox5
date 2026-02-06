# TASK-SSOT-036: Create Single Improvement Registry

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** SSOT Violations - Report Format Inconsistency

## Objective
Create a standardized report schema and unify report formats across all agents (Scout, Verifier, Executor, Planner) to eliminate parsing complexity and enable consistent report aggregation.

## Success Criteria
- [ ] Standard report schema defined in YAML format
- [ ] JSON Schema validation implemented for all reports
- [ ] Scout agent updated to produce standard format
- [ ] Verifier agent updated to produce standard format
- [ ] Executor agent updated to produce standard format
- [ ] Planner agent updated to produce standard format
- [ ] Migration script created for existing reports
- [ ] All historical reports migrated to new format

## Context
Different agents currently produce reports in different formats with varying schemas. This creates parsing complexity, inconsistent data representation, difficulty in aggregating reports, and maintenance overhead from supporting multiple formats. The solution requires a standard schema with validation, versioning support for schema evolution, and migration of existing reports.

## Approach
1. Define standard report schema with required fields (version, report_id, report_type, timestamp, metadata, summary, findings, recommendations)
2. Create JSON Schema validation using jsonschema library
3. Update each agent to produce reports in standard format
4. Create migration script to convert existing reports
5. Test validation and migration on sample reports

## Estimated Effort
3-4 hours

## Rollback Strategy
If issues arise, keep old reports backed up and revert agent code to previous version while fixing the standard format issues.
