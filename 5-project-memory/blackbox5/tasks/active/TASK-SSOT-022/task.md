# TASK-SSOT-022: Create Unified Task Repository

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Create a single TaskRepository that consolidates all 6 incompatible Task class implementations.

## Success Criteria
- [ ] Design unified Task dataclass schema
- [ ] Create `storage/repository/base.py` with Repository[T] ABC
- [ ] Create `storage/repository/task_repository.py`
- [ ] Implement caching layer
- [ ] Implement query methods (by status, priority, tags)
- [ ] Migrate bb5-queue-manager.py to use TaskRepository
- [ ] Migrate bb5-reanalysis-engine.py to use TaskRepository
- [ ] Deprecate old Task classes

## Context
6 incompatible Task classes found:
1. bb5-queue-manager.py - Task with ROI fields
2. bb5-reanalysis-engine.py - Task with analytics fields
3. bb5-metrics-collector.py - TaskMetrics
4. 2-engine/schemas/task.py - Task with checkpointing
5. task_router.py - Task with capabilities
6. task_agent.py - Task with acceptance criteria

## Unified Schema Requirements
- Common fields: id, title, description, status, priority, timestamps
- Dependency fields: depends_on, blocked_by, blocks
- Execution fields: assignee, estimated_minutes, duration_minutes
- Analytics fields: success_rate, failure_count, retry_count
- Metadata fields: tags, files_referenced, epic_id, goal

## Related Files
- task-class-duplication-analysis.md
- bb5-queue-manager.py
- bb5-reanalysis-engine.py

## Rollback Strategy
Keep old Task classes until migration complete.
