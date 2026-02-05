# TASK-SSOT-027: Create SQLite Storage Layer for Relational Data

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Create SQLite storage layer for relational data that currently exists in scattered YAML files.

## Success Criteria
- [ ] Design SQLite schema for Tasks, Goals, Plans, Skills, Runs, Events
- [ ] Create storage/sqlite/ module with connection management
- [ ] Implement TaskRepository with SQLite backend
- [ ] Implement GoalRepository with SQLite backend
- [ ] Implement EventStore for time-series events
- [ ] Create migration scripts from YAML to SQLite
- [ ] Add query methods for complex relationships
- [ ] Maintain YAML files for content, SQLite for metadata

## Context
60-70% of YAML data would benefit from SQLite:
- Task → Goal → Plan hierarchy (many-to-many)
- Task dependency graph (needs fast traversal)
- Skill → Task usage (analytics queries)
- Event timeline (time-series queries)

## Schema Requirements
```sql
CREATE TABLE tasks (id TEXT PRIMARY KEY, title TEXT, status TEXT, goal_id TEXT, ...);
CREATE TABLE task_dependencies (task_id TEXT, depends_on_task_id TEXT, ...);
CREATE TABLE goals (id TEXT PRIMARY KEY, name TEXT, status TEXT, ...);
CREATE TABLE events (id INTEGER PRIMARY KEY, type TEXT, occurred_at TIMESTAMP, ...);
CREATE INDEX idx_tasks_goal ON tasks(goal_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

## Related Files
- database-storage-needs.md
- All YAML files in tasks/, goals/, events.yaml

## Rollback Strategy
Keep YAML files as source of truth until SQLite proven stable.
