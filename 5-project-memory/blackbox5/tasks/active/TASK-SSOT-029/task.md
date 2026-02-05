# TASK-SSOT-029: Optimize Serialization Formats

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Optimize serialization formats for better performance and storage efficiency.

## Success Criteria
- [ ] Migrate events.yaml (152KB) to SQLite or line-delimited JSON
- [ ] Convert memories.json (428KB) to MessagePack format
- [ ] Add frontmatter caching for 1000+ task files
- [ ] Implement format detection in StorageBackend
- [ ] Add MessagePackStorage implementation
- [ ] Measure size and performance improvements

## Context
Current format issues:
- events.yaml: YAML for append-heavy logs is WRONG format
- memories.json: JSON for float arrays is SUBOPTIMAL
- Task frontmatter: Re-parsed on every read (inefficient)
- Total data: 27.7MB across all formats

## Format Recommendations
| Data Type | Current | Better Format | Expected Improvement |
|-----------|---------|---------------|---------------------|
| events.yaml | YAML | SQLite or LDJSON | 100x query speed |
| memories.json | JSON | MessagePack | 50% size reduction |
| Task metadata | Markdown | SQLite index | Sub-second queries |
| Metrics | YAML | SQLite | SQL aggregation |

## Related Files
- serialization-format-analysis.md
- events.yaml
- memories.json
- All task.md files

## Rollback Strategy
Keep original formats until new formats proven.
