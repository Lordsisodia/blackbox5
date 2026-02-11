# Project Memory Sync Scripts

This directory contains scripts for managing and synchronizing project memory.

## sync-project-memory.sh

Compares a target project memory against the BlackBox5 template and optionally syncs missing files/folders.

### Usage

```bash
./sync-project-memory.sh [OPTIONS] <target-path>
```

### Options

| Option | Description |
|--------|-------------|
| `-d, --dry-run` | Show what would be changed without making changes |
| `-f, --fix` | Actually copy missing files/folders |
| `-v, --verbose` | Show detailed output |
| `-h, --help` | Show help |

### Examples

**Check only (no changes):**
```bash
./sync-project-memory.sh /Users/shaansisodia/DEV/client-projects/lumelle/blackbox5/5-project-memory/lumelle
```

**Dry run (see what would change):**
```bash
./sync-project-memory.sh -d -v /Users/shaansisodia/DEV/client-projects/lumelle/blackbox5/5-project-memory/lumelle
```

**Fix (actually copy missing files):**
```bash
./sync-project-memory.sh -f /Users/shaansisodia/DEV/client-projects/lumelle/blackbox5/5-project-memory/lumelle
```

### What It Does

1. Compares directory structure between template and target
2. Identifies missing directories
3. Identifies missing files
4. Optionally copies missing files from template to target

### Exclusions

The following are excluded from comparison:
- `.archived/` directories
- `.Autonomous/` directories
- `runs/` directories
- `.git/` directories
- Session-specific data (`sessions/session-*`)
- Agent history (`agents/history/sessions/*`)
- Data folders (`data/*`)
- Backup files (`*.backup*`)
- Runtime files (`WORK-LOG.md`, `ACTIVE.md`)

### Template Source

The script uses `/Users/shaansisodia/blackbox5/5-project-memory/siso-internal` as the template source.
