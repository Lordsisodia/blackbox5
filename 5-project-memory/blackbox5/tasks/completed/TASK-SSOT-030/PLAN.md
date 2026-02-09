# PLAN.md: Migrate Complexity Metrics to SQLite

**Task:** TASK-SSOT-030 - Complexity metrics in YAML should be in SQLite
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Complexity metrics are stored in YAML files:
- `5-project-memory/blackbox5/operations/skill-metrics.yaml`
- `5-project-memory/blackbox5/operations/improvement-metrics.yaml`
- Hard to query and aggregate
- No time-series analysis
- Difficult to generate reports

This creates:
1. **Query Difficulty**: Must load entire files to query
2. **No Aggregation**: Hard to calculate averages, trends
3. **No Time Series**: Can't track metrics over time
4. **Performance Issues**: Slow with large datasets
5. **Maintenance Burden**: Custom parsing logic

### First Principles Solution
- **SQLite Storage**: Structured storage for metrics
- **Time Series**: Track metrics over time
- **Query Interface**: SQL for complex queries
- **Aggregation**: Easy statistical analysis
- **Migration**: Move existing data to SQLite

---

## 2. Current State Analysis

### Current YAML Storage

```yaml
# operations/skill-metrics.yaml
skill_metrics:
  git-commit:
    effectiveness_score: 0.92
    success_rate: 0.95
    usage_count: 47
    last_used: "2026-02-05"

# operations/improvement-metrics.yaml
improvements:
  - date: "2026-02-05"
    category: "performance"
    metric: "task_completion_time"
    before: 120
    after: 90
    improvement_percent: 25
```

### Query Limitations

| Query | Current Approach | Problem |
|-------|-----------------|---------|
| Average effectiveness | Load all, calculate | Slow |
| Trend over time | Not possible | No time series |
| Top skills | Load all, sort | Inefficient |
| Compare periods | Manual calculation | Error prone |

---

## 3. Proposed Solution

### SQLite Schema for Metrics

```sql
-- Skill metrics time series
CREATE TABLE skill_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    effectiveness_score REAL,
    success_rate REAL,
    usage_count INTEGER,
    average_duration_seconds REAL,
    metadata TEXT  -- JSON
);

-- Improvement metrics
CREATE TABLE improvement_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    category TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value_before REAL,
    value_after REAL,
    improvement_percent REAL,
    description TEXT
);

-- Task complexity metrics
CREATE TABLE task_complexity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    estimated_hours REAL,
    actual_hours REAL,
    complexity_score INTEGER,  -- 1-10
    lines_of_code INTEGER,
    files_modified INTEGER,
    UNIQUE(task_id, timestamp)
);

-- System metrics
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    unit TEXT,
    metadata TEXT  -- JSON
);

-- Indexes for performance
CREATE INDEX idx_skill_metrics_name ON skill_metrics(skill_name);
CREATE INDEX idx_skill_metrics_time ON skill_metrics(timestamp);
CREATE INDEX idx_improvement_category ON improvement_metrics(category);
CREATE INDEX idx_improvement_time ON improvement_metrics(timestamp);
CREATE INDEX idx_task_complexity_task ON task_complexity(task_id);
CREATE INDEX idx_system_metrics_name ON system_metrics(metric_name);
CREATE INDEX idx_system_metrics_time ON system_metrics(timestamp);
```

### Metrics Repository

**File:** `2-engine/.autonomous/lib/metrics_repository.py`

```python
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import sqlite3
import json

class MetricsRepository:
    """Repository for complexity and performance metrics."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(METRICS_SCHEMA)

    # Skill Metrics
    def record_skill_metric(
        self,
        skill_name: str,
        effectiveness_score: float,
        success_rate: float,
        usage_count: int,
        average_duration_seconds: Optional[float] = None,
        metadata: Optional[Dict] = None
    ):
        """Record skill metric snapshot."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO skill_metrics
                (skill_name, timestamp, effectiveness_score, success_rate,
                 usage_count, average_duration_seconds, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                skill_name,
                datetime.now().isoformat(),
                effectiveness_score,
                success_rate,
                usage_count,
                average_duration_seconds,
                json.dumps(metadata) if metadata else None
            ))

    def get_skill_trend(
        self,
        skill_name: str,
        days: int = 30
    ) -> List[Dict]:
        """Get skill metrics trend over time."""
        since = (datetime.now() - timedelta(days=days)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM skill_metrics
                WHERE skill_name = ? AND timestamp > ?
                ORDER BY timestamp
            """, (skill_name, since))

            return [dict(row) for row in cursor.fetchall()]

    def get_top_skills(
        self,
        metric: str = "effectiveness_score",
        limit: int = 10
    ) -> List[Dict]:
        """Get top skills by metric."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(f"""
                SELECT skill_name, AVG({metric}) as avg_metric
                FROM skill_metrics
                GROUP BY skill_name
                ORDER BY avg_metric DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]

    # Improvement Metrics
    def record_improvement(
        self,
        category: str,
        metric_name: str,
        value_before: float,
        value_after: float,
        description: Optional[str] = None
    ):
        """Record improvement metric."""
        improvement = ((value_after - value_before) / value_before * 100) \
                      if value_before != 0 else 0

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO improvement_metrics
                (timestamp, category, metric_name, value_before,
                 value_after, improvement_percent, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                category,
                metric_name,
                value_before,
                value_after,
                improvement,
                description
            ))

    def get_improvement_summary(
        self,
        days: int = 30
    ) -> Dict:
        """Get improvement summary."""
        since = (datetime.now() - timedelta(days=days)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_improvements,
                    AVG(improvement_percent) as avg_improvement,
                    category
                FROM improvement_metrics
                WHERE timestamp > ?
                GROUP BY category
            """, (since,))

            return {
                row[2]: {
                    'count': row[0],
                    'avg_improvement': row[1]
                }
                for row in cursor.fetchall()
            }

    # Task Complexity
    def record_task_complexity(
        self,
        task_id: str,
        estimated_hours: float,
        actual_hours: float,
        complexity_score: int,
        lines_of_code: Optional[int] = None,
        files_modified: Optional[int] = None
    ):
        """Record task complexity metrics."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO task_complexity
                (task_id, timestamp, estimated_hours, actual_hours,
                 complexity_score, lines_of_code, files_modified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task_id,
                datetime.now().isoformat(),
                estimated_hours,
                actual_hours,
                complexity_score,
                lines_of_code,
                files_modified
            ))

    def get_complexity_stats(self) -> Dict:
        """Get complexity statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    AVG(complexity_score) as avg_complexity,
                    AVG(actual_hours / estimated_hours) as estimation_accuracy,
                    AVG(lines_of_code) as avg_loc
                FROM task_complexity
            """)

            row = cursor.fetchone()
            return {
                'avg_complexity': row[0],
                'estimation_accuracy': row[1],
                'avg_lines_of_code': row[2]
            }

    # Reporting
    def generate_report(self, days: int = 30) -> Dict:
        """Generate comprehensive metrics report."""
        return {
            'period_days': days,
            'skill_summary': self.get_top_skills(limit=5),
            'improvement_summary': self.get_improvement_summary(days),
            'complexity_stats': self.get_complexity_stats(),
            'generated_at': datetime.now().isoformat()
        }
```

### Implementation Plan

#### Phase 1: Create Schema (30 min)

1. Define tables for skill, improvement, task metrics
2. Create indexes
3. Set up migration script

#### Phase 2: Create Repository (2 hours)

1. Implement MetricsRepository
2. Add CRUD operations
3. Add query methods
4. Add reporting

#### Phase 3: Create Migration Script (1 hour)

**File:** `2-engine/.autonomous/bin/migrate-metrics.py`

```python
#!/usr/bin/env python3
"""Migrate metrics from YAML to SQLite."""

def migrate_skill_metrics(yaml_path: str, repo: MetricsRepository):
    """Migrate skill metrics from YAML."""
    import yaml

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    for skill_name, metrics in data.get('skill_metrics', {}).items():
        repo.record_skill_metric(
            skill_name=skill_name,
            effectiveness_score=metrics.get('effectiveness_score', 0),
            success_rate=metrics.get('success_rate', 0),
            usage_count=metrics.get('usage_count', 0)
        )
        print(f"Migrated skill: {skill_name}")
```

#### Phase 4: Update Metrics Collection (1 hour)

Update scripts to write to SQLite instead of YAML:

```python
# Before
with open('skill-metrics.yaml') as f:
    metrics = yaml.safe_load(f)
metrics[skill_name] = new_data
with open('skill-metrics.yaml', 'w') as f:
    yaml.dump(metrics, f)

# After
repo = MetricsRepository(DB_PATH)
repo.record_skill_metric(skill_name, ...)
```

#### Phase 5: Create Dashboard Queries (30 min)

Add queries for health dashboard:
- Top skills
- Improvement trends
- Complexity distribution

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/metrics_repository.py` - Metrics repository
2. `2-engine/.autonomous/bin/migrate-metrics.py` - Migration script

### Modified Files
1. Metrics collection scripts
2. Health dashboard to use SQL queries

---

## 5. Success Criteria

- [ ] SQLite schema created
- [ ] MetricsRepository implemented
- [ ] Existing data migrated
- [ ] Metrics collection updated
- [ ] Dashboard queries working
- [ ] Reports generating correctly

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep YAML files as backup
2. **Fix**: Debug repository
3. **Re-migrate**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 30 min | 30 min |
| Phase 2: Repository | 2 hours | 2.5 hours |
| Phase 3: Migration | 1 hour | 3.5 hours |
| Phase 4: Collection | 1 hour | 4.5 hours |
| Phase 5: Dashboard | 30 min | 5 hours |
| **Total** | | **4-5 hours** |

---

*Plan created based on SSOT violation analysis - Complexity metrics in YAML*
