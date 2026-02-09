# PLAN.md: Archive Old Run Folders

**Task:** TASK-SSOT-038 - Old run folders need archival/cleanup
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 55 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Run folders accumulate over time:
- Hundreds of run folders
- Taking up disk space
- Slowing down operations
- No archival policy

This creates:
1. **Storage Waste**: Old runs consuming space
2. **Performance Issues**: Slow directory listings
3. **Clutter**: Hard to find relevant runs
4. **No Policy**: Unclear what to keep

### First Principles Solution
- **Archival Policy**: Define what to keep and for how long
- **Automated Cleanup**: Archive old runs automatically
- **Compression**: Compress archived runs
- **Searchable Index**: Find archived runs easily

---

## 2. Proposed Solution

### Archival Policy

```yaml
# archive-policy.yaml
policy:
  # Keep recent runs
  keep_last_n: 50

  # Keep runs for active tasks
  keep_active_task_runs: true

  # Archive runs older than
  archive_after_days: 30

  # Delete archived runs after
  delete_archived_after_days: 365

  # Always keep runs with these tags
  always_keep_tags:
    - "milestone"
    - "important"
    - "reference"

  # Compression settings
  compression:
    format: "gz"  # gz, bz2, xz
    level: 6
```

### Archive Structure

```
runs/
├── active/              # Recent runs (symlinks)
├── archive/
│   ├── 2026-01.tar.gz  # Monthly archives
│   └── 2025-12.tar.gz
└── index.yaml          # Archive index
```

### Implementation Plan

#### Phase 1: Create Archival Script (1 hour)

```python
#!/usr/bin/env python3
"""Archive old run folders."""

import tarfile
import gzip
from datetime import datetime, timedelta
from pathlib import Path

def archive_old_runs(runs_dir: Path, archive_dir: Path, days: int = 30):
    """Archive runs older than specified days."""
    cutoff = datetime.now() - timedelta(days=days)

    for run_dir in runs_dir.iterdir():
        if not run_dir.is_dir():
            continue

        # Parse run date from name (run-YYYYMMDD_HHMMSS)
        run_date = parse_run_date(run_dir.name)
        if run_date > cutoff:
            continue

        # Create monthly archive
        month_key = run_date.strftime("%Y-%m")
        archive_path = archive_dir / f"{month_key}.tar.gz"

        # Add to archive
        with tarfile.open(archive_path, 'a:gz') as tar:
            tar.add(run_dir, arcname=run_dir.name)

        # Remove original
        import shutil
        shutil.rmtree(run_dir)

        print(f"Archived: {run_dir.name}")

def parse_run_date(run_name: str) -> datetime:
    """Parse date from run folder name."""
    # run-20260205_143022
    date_str = run_name.replace('run-', '').split('_')[0]
    return datetime.strptime(date_str, "%Y%m%d")
```

#### Phase 2: Create Archive Index (1 hour)

```python
def update_archive_index(archive_dir: Path):
    """Update searchable index of archived runs."""
    index = {'archives': []}

    for archive_file in archive_dir.glob("*.tar.gz"):
        with tarfile.open(archive_file, 'r:gz') as tar:
            runs = [m.name for m in tar.getmembers() if m.isdir()]

        index['archives'].append({
            'file': str(archive_file),
            'month': archive_file.stem.replace('.tar', ''),
            'run_count': len(runs),
            'runs': runs
        })

    with open(archive_dir / 'index.yaml', 'w') as f:
        yaml.dump(index, f)
```

#### Phase 3: Create Cleanup Schedule (30 min)

Add to cron or scheduler:
```bash
# Run archival weekly
0 2 * * 0 ~/.blackbox5/2-engine/.autonomous/bin/archive-runs.py
```

#### Phase 4: Create Restore Function (30 min)

```python
def restore_run(archive_dir: Path, run_id: str, output_dir: Path):
    """Restore a run from archive."""
    # Find in index
    index = yaml.safe_load((archive_dir / 'index.yaml').read_text())

    for archive in index['archives']:
        if run_id in archive['runs']:
            # Extract from archive
            with tarfile.open(archive['file'], 'r:gz') as tar:
                tar.extract(run_id, output_dir)
            print(f"Restored: {run_id}")
            return True

    return False
```

---

## 3. Success Criteria

- [ ] Archival script created
- [ ] Archive index working
- [ ] Cleanup scheduled
- [ ] Restore function working

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Script | 1 hour |
| Index | 1 hour |
| Schedule | 30 min |
| Restore | 30 min |
| **Total** | **2-3 hours** |

---

*Plan created based on SSOT violation analysis*
