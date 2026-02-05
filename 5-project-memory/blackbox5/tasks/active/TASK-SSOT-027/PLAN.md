# PLAN.md: Create SQLite Storage Backend

**Task:** TASK-SSOT-027 - Create SQLite storage backend for structured data
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 6-8 hours
**Importance:** 75 (High)

---

## 1. First Principles Analysis

### The Core Problem
All data is stored in YAML files which:
- Don't scale well with large datasets
- Don't support efficient querying
- Don't have ACID properties
- Are hard to aggregate across files
- Have no schema enforcement

This creates:
1. **Performance Issues**: Slow queries on large datasets
2. **Data Integrity**: No constraints or validation
3. **Query Complexity**: Must load entire files
4. **No Transactions**: Partial updates possible
5. **Maintenance Burden**: Custom query logic everywhere

### First Principles Solution
- **SQLite Backend**: For structured, query-heavy data
- **Hybrid Storage**: YAML for documents, SQLite for structured data
- **Repository Pattern**: Abstract storage details
- **Migration Path**: Gradual migration from YAML
- **Query Interface**: SQL for complex queries

---

## 2. Current State Analysis

### Current YAML Storage

```yaml
# tasks/active/TASK-001/task.yaml
id: "TASK-001"
title: "Fix bug"
status: "in_progress"
priority: "HIGH"
created_at: "2026-02-05T10:00:00Z"
assigned_to: "claude"
```

### Query Patterns

| Query | Current Approach | Problem |
|-------|-----------------|---------|
| All pending tasks | Load all task files, filter | Slow with many tasks |
| Tasks by assignee | Load all, filter | Inefficient |
| Task count by status | Load all, count | Expensive |
| Recent tasks | Load all, sort, limit | Very slow |

---

## 3. Proposed Solution

### SQLite Schema

**File:** `5-project-memory/blackbox5/.autonomous/data/blackbox5.db`

```sql
-- Tasks table
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    assigned_to TEXT,
    description TEXT,
    parent_task_id TEXT,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(id)
);

-- Task tags (many-to-many)
CREATE TABLE task_tags (
    task_id TEXT,
    tag TEXT,
    PRIMARY KEY (task_id, tag),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Task acceptance criteria
CREATE TABLE task_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT,
    criterion TEXT,
    completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Goals table
CREATE TABLE goals (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    description TEXT
);

-- Runs table
CREATE TABLE runs (
    id TEXT PRIMARY KEY,
    task_id TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status TEXT,
    duration_seconds INTEGER,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Events table (for timeline)
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    entity_type TEXT,
    entity_id TEXT,
    timestamp TIMESTAMP NOT NULL,
    payload TEXT,  -- JSON
    source TEXT
);

-- Indexes for performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assignee ON tasks(assigned_to);
CREATE INDEX idx_tasks_created ON tasks(created_at);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_entity ON events(entity_type, entity_id);
```

### SQLite Storage Backend

**File:** `2-engine/.autonomous/lib/sqlite_backend.py`

```python
import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage_backend import StorageBackend

class SQLiteBackend(StorageBackend):
    """SQLite implementation of StorageBackend."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)

    def read(self, path: str) -> Any:
        """Read from SQLite.

        Path format: "table/id" or "table?query"
        """
        if '/' in path:
            # Read single record
            table, record_id = path.split('/', 1)
            return self._read_record(table, record_id)
        elif '?' in path:
            # Query
            table, query = path.split('?', 1)
            return self._query(table, query)
        else:
            # Read all from table
            return self._read_all(path)

    def _read_record(self, table: str, record_id: str) -> Optional[Dict]:
        """Read single record."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM {table} WHERE id = ?",
                (record_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def _query(self, table: str, query: str) -> List[Dict]:
        """Execute query."""
        # Parse query string (e.g., "status=pending&priority=HIGH")
        conditions = []
        params = []
        for condition in query.split('&'):
            if '=' in condition:
                key, value = condition.split('=', 1)
                conditions.append(f"{key} = ?")
                params.append(value)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM {table} WHERE {where_clause}",
                params
            )
            return [dict(row) for row in cursor.fetchall()]

    def write(self, path: str, data: Any) -> None:
        """Write to SQLite."""
        table, record_id = path.split('/', 1)

        # Check if exists
        exists = self._read_record(table, record_id) is not None

        if exists:
            self._update_record(table, record_id, data)
        else:
            self._insert_record(table, record_id, data)

    def _insert_record(self, table: str, record_id: str, data: Dict):
        """Insert new record."""
        data['id'] = record_id

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                values
            )

    def _update_record(self, table: str, record_id: str, data: Dict):
        """Update existing record."""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + [record_id]

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"UPDATE {table} SET {set_clause} WHERE id = ?",
                values
            )

    def exists(self, path: str) -> bool:
        """Check if record exists."""
        return self.read(path) is not None

    def delete(self, path: str) -> None:
        """Delete record."""
        table, record_id = path.split('/', 1)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))

    def list(self, path: str) -> List[str]:
        """List all IDs in table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"SELECT id FROM {path}")
            return [row[0] for row in cursor.fetchall()]

    @contextmanager
    def transaction(self):
        """Transaction context manager."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
```

### Implementation Plan

#### Phase 1: Design Schema (1 hour)

1. Define tables for tasks, goals, runs, events
2. Define relationships
3. Define indexes
4. Create migration plan

#### Phase 2: Implement SQLite Backend (2 hours)

1. Create SQLiteBackend class
2. Implement all StorageBackend methods
3. Add query capabilities
4. Add transaction support

#### Phase 3: Create Migration Script (2 hours)

**File:** `2-engine/.autonomous/bin/migrate-to-sqlite.py`

```python
#!/usr/bin/env python3
"""Migrate YAML data to SQLite."""

def migrate_tasks(project_path: str, db_path: str):
    """Migrate tasks from YAML to SQLite."""
    from sqlite_backend import SQLiteBackend
    from pathlib import Path
    import yaml

    storage = SQLiteBackend(db_path)

    tasks_dir = Path(project_path) / "tasks" / "active"
    for task_dir in tasks_dir.iterdir():
        if task_dir.is_dir():
            task_file = task_dir / "task.yaml"
            if task_file.exists():
                with open(task_file) as f:
                    task = yaml.safe_load(f)
                storage.write(f"tasks/{task['id']}", task)
                print(f"Migrated task: {task['id']}")
```

#### Phase 4: Update Repositories (2 hours)

Update TaskRepository, GoalRepository to use SQLite:

```python
class TaskRepository:
    def __init__(self, use_sqlite: bool = True):
        if use_sqlite:
            self.storage = SQLiteBackend(DB_PATH)
        else:
            self.storage = FileSystemBackend(PROJECT_PATH)
```

#### Phase 5: Testing (1 hour)

1. Test migrations
2. Test queries
3. Test transactions
4. Performance benchmarks

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/sqlite_backend.py` - SQLite backend
2. `2-engine/.autonomous/bin/migrate-to-sqlite.py` - Migration script
3. `5-project-memory/blackbox5/.autonomous/data/` - Database directory

### Modified Files
1. Repository classes to support SQLite
2. Configuration for storage backend selection

---

## 5. Success Criteria

- [ ] SQLite schema created
- [ ] SQLiteBackend implemented
- [ ] Migration script working
- [ ] Data migrated successfully
- [ ] Queries working efficiently
- [ ] Performance improved

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Switch back to FileSystemBackend
2. **Fix**: Debug SQLite backend
3. **Re-migrate**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 1 hour | 1 hour |
| Phase 2: Backend | 2 hours | 3 hours |
| Phase 3: Migration | 2 hours | 5 hours |
| Phase 4: Repositories | 2 hours | 7 hours |
| Phase 5: Testing | 1 hour | 8 hours |
| **Total** | | **6-8 hours** |

---

*Plan created based on SSOT violation analysis - Need SQLite for structured data*
