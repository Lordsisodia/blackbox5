# Integration & MCP Validation - Action Checklist

**Generated:** 2026-01-20
**Agent:** Agent 6 - Integration & MCP Validator

---

## Priority 1: URGENT (Blocker)

### Fix Vibe Kanban Database ⚠️

**Status:** Database not initialized, API returns "unable to open database file"

**Steps:**
- [ ] Navigate to vibe-kanban directory: `cd /blackbox5/vibe-kanban`
- [ ] Check for database setup scripts: `ls -la scripts/`
- [ ] Check for migration files: `ls -la crates/db/migrations/`
- [ ] Look for README or SETUP documentation: `cat README.md | grep -i database`
- [ ] Run database initialization (one of these):
  ```bash
  # Option A: If setup script exists
  ./scripts/setup-db.sh

  # Option B: If migration system exists
  cargo run --bin db-migrate

  # Option C: If SQLx needs offline prep
  pnpm run prepare-db

  # Option D: Manual creation
  sqlite3 vibe-kanban.db < schema.sql
  ```
- [ ] Verify database created: `ls -lh *.db`
- [ ] Test API: `curl http://localhost:3001/api/projects`
- [ ] Test MCP tool: Try `list_projects` via vibe-kanban MCP
- [ ] Document the fix in vibe-kanban README

**Estimated Time:** 10-15 minutes

**Verification:**
```bash
curl http://localhost:3001/api/projects
# Should return: {"success":true,"data":[...]}
```

---

## Priority 2: HIGH (Recommended)

### Activate MCP Crash Prevention

**Status:** Setup script exists but not executed

**Steps:**
- [ ] Navigate to runtime directory: `cd /blackbox5/.runtime/mcp`
- [ ] Review setup script: `cat setup.sh`
- [ ] Run setup: `./setup.sh`
- [ ] Verify installation:
  ```bash
  ls -la ~/.mcp-logs/
  cat ~/.mcp-logs/mcp-state.json
  ```
- [ ] Check daemon status:
  ```bash
  launchctl list | grep mcp-monitor
  ```
- [ ] Test aliases: `mcp-status`
- [ ] Monitor logs: `mcp-logs`
- [ ] Verify auto-cleanup: Wait 60 seconds, check `mcp-status` again

**Estimated Time:** 5 minutes

**Verification:**
```bash
cat ~/.mcp-logs/mcp-state.json
# Should show: {"timestamp": "...", "servers": {...}, "last_cleanup": "..."}
```

---

## Priority 3: MEDIUM (Quality)

### Add Missing Integration Tests

**Status:** 4 integrations lack test coverage

**Integrations needing tests:**
- [ ] GitHub (`github/manager.py`)
- [ ] GitHub Actions (`github-actions/manager.py`)
- [ ] Vercel (`vercel/manager.py`)
- [ ] Vibe (`vibe/manager.py`)

**Steps for each integration:**

1. Create test directory structure:
   ```bash
   cd /blackbox5/2-engine/06-integrations/{integration}/
   mkdir -p tests
   touch tests/__init__.py
   touch tests/test_integration.py
   ```

2. Add basic test template:
   ```python
   import pytest
   from {integration}.manager import {Integration}Manager

   def test_manager_imports():
       # Test 1: Manager class can be imported
       assert True

   @pytest.mark.skipif(no_credentials, reason="No API credentials")
   def test_manager_connection():
       # Test 2: Manager can connect to API
       pass

   @pytest.mark.skipif(no_credentials, reason="No API credentials")
   def test_basic_operation():
       # Test 3: Manager can perform basic operation
       pass
   ```

3. Run tests:
   ```bash
   cd /blackbox5/2-engine
   pytest 06-integrations/{integration}/tests/
   ```

**Estimated Time:** 1-2 hours total (15-30 minutes per integration)

**Verification:**
```bash
pytest /blackbox5/2-engine/06-integrations/*/tests/
# All tests should pass
```

---

## Priority 4: MEDIUM (Standards)

### Standardize Configuration Files

**Status:** 6 of 9 integrations lack `config.py`

**Integrations needing config:**
- [ ] GitHub
- [ ] GitHub Actions
- [ ] Vercel
- [ ] Vibe
- [ ] Obsidian (may not need)
- [ ] MCP (may not need)

**Steps:**

1. Use template as reference: `_template/config.py`

2. Create config file with:
   ```python
   """
   Configuration for {Integration} integration.
   """
   from pathlib import Path
   from typing import Optional

   class {Integration}Config:
       """Configuration for {Integration} API."""

       def __init__(
           self,
           api_key: Optional[str] = None,
           base_url: Optional[str] = None,
           # Add integration-specific config
       ):
           self.api_key = api_key or self._get_env_var()
           self.base_url = base_url or "https://api.{integration}.com"

       def _get_env_var(self) -> Optional[str]:
           import os
           return os.environ.get("{INTEGRATION}_API_KEY")

       def validate(self) -> bool:
           """Validate configuration."""
           return bool(self.api_key)
   ```

3. Update manager.py to use config:
   ```python
   from .config import {Integration}Config

   class {Integration}Manager:
       def __init__(self, config: Optional[{Integration}Config] = None):
           self.config = config or {Integration}Config()
           if not self.config.validate():
               raise ValueError("Invalid configuration")
   ```

**Estimated Time:** 30 minutes total (5 minutes per integration)

**Verification:**
```bash
for dir in /blackbox5/2-engine/06-integrations/*/; do
  if [ -f "$dir/manager.py" ]; then
    echo "$(basename $dir): $(test -f $dir/config.py && echo '✅' || echo '❌')"
  fi
done
```

---

## Priority 5: LOW (Cleanup)

### Add Environment Setup Guide

**Steps:**
- [ ] Create `.env.example` in project root:
  ```bash
  # GitHub Integration
  GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
  GITHUB_REPO=owner/repo

  # Supabase Integration
  SUPABASE_ACCESS_TOKEN=sbp_xxx

  # Vercel Integration
  VERCEL_TOKEN=xxxxxxxxxxxxx
  ```

- [ ] Create `/blackbox5/2-engine/06-integrations/.env.example`

- [ ] Update each integration's README with environment setup section

- [ ] Add setup script: `/blackbox5/2-engine/06-integrations/setup.sh`
  ```bash
  #!/bin/bash
  echo "Setting up BlackBox5 Integrations..."
  cp .env.example .env
  echo "Edit .env with your API keys"
  ```

**Estimated Time:** 20 minutes

---

### Cleanup Unused MCP Servers

**Steps:**
- [ ] Review running MCP servers: `ps aux | grep mcp`
- [ ] Identify duplicates or unused servers
- [ ] Update `.mcp.json` to remove unused entries
- [ ] Kill unused processes: `pkill -f "unused-mcp-server"`
- [ ] Verify still-need servers are running

**Current duplicates detected:**
- chrome-devtools-mcp: 2 instances (keep 1)
- memory-bank-mcp: 2 instances (keep 1)
- vibe-kanban-mcp: 2 instances, 2 versions (keep latest)

**Estimated Time:** 5 minutes

---

## Priority 6: LOW (Documentation)

### Update Integration Documentation

**Steps:**
- [ ] Add troubleshooting section to each integration README
- [ ] Document common errors and solutions
- [ ] Add example usage for each manager method
- [ ] Create `/blackbox5/2-engine/06-integrations/TROUBLESHOOTING.md`
- [ ] Add diagrams showing integration architecture

**Content template for TROUBLESHOOTING.md:**
```markdown
# Integration Troubleshooting

## GitHub Integration

### Issue: "401 Unauthorized"
**Solution:** Check GITHUB_TOKEN is valid and has correct scopes

### Issue: "Repository not found"
**Solution:** Verify repo format is "owner/repo"

## Vibe Kanban Integration

### Issue: "Database not found"
**Solution:** Run database initialization script

## MCP Integration

### Issue: "MCP server not starting"
**Solution:** Check command is valid and dependencies installed

### Issue: "Too many MCP processes"
**Solution:** Run `mcp-cleanup` or activate crash prevention
```

**Estimated Time:** 1 hour

---

## Verification Checklist

After completing all priorities, verify:

### Integration Health
- [ ] All 9 managers can be imported: `from integrations.* import *Manager`
- [ ] All 9 managers have basic documentation
- [ ] All integrations with external APIs have config files
- [ ] All integrations have at least basic tests

### MCP Health
- [ ] MCP Manager can discover servers
- [ ] Crash prevention daemon is running (if activated)
- [ ] No duplicate MCP servers running
- [ ] All MCP servers respond to tool calls

### Vibe Kanban Health
- [ ] Database file exists
- [ ] `/api/health` returns success
- [ ] `/api/projects` returns data (not error)
- [ ] MCP tools can list/create/update tasks

### GitHub Integration Health
- [ ] Can create issue (if token provided)
- [ ] Can create PR (if token provided)
- [ ] Repository auto-detection works
- [ ] Safety checks work

---

## Progress Tracking

**Total Tasks:** 6 priorities, 25+ individual tasks

**Completed:**
- [ ] Priority 1: Vibe Kanban database fix
- [ ] Priority 2: MCP crash prevention activation
- [ ] Priority 3: Add missing tests
- [ ] Priority 4: Standardize configs
- [ ] Priority 5: Environment setup
- [ ] Priority 6: Documentation updates

**Time Estimate:**
- Priority 1: 10-15 minutes
- Priority 2: 5 minutes
- Priority 3: 1-2 hours
- Priority 4: 30 minutes
- Priority 5: 20 minutes
- Priority 6: 1 hour

**Total Time:** 3-4 hours for complete cleanup

---

**Next Steps:**
1. Start with Priority 1 (URGENT) - Vibe Kanban database
2. Continue with Priority 2 (HIGH) - MCP crash prevention
3. Address remaining priorities as time permits

**Resources:**
- Full findings: `VALIDATION-FINDINGS.md`
- Quick summary: `QUICK-SUMMARY.md`
- This checklist: `ACTION-CHECKLIST.md`
