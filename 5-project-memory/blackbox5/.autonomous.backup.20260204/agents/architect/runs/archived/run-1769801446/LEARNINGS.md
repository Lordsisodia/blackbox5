# LEARNINGS - Run 1769801446

**Task:** Initialize Vibe Kanban Database
**Date:** 2026-01-31T02:57:26Z
**Agent:** Agent-2.3

---

## Key Learnings

### Learning 1: Vibe Kanban Architecture
**Discovery:** Vibe Kanban is NOT a Node.js app - it's a Rust application distributed via npm.

**Implications:**
- npm package is just a wrapper/downloader
- Binary is downloaded from releases on startup
- Migrations are embedded in the binary
- Database initialization happens automatically

**Future Reference:** When troubleshooting "npm" packages that behave unexpectedly, check if they're actually compiled binaries.

---

### Learning 2: Dynamic Port Allocation
**Discovery:** Vibe Kanban intentionally uses random ports to avoid conflicts.

**Why This Matters:**
- Users can run multiple instances (if needed)
- No "port already in use" errors
- Requires auto-detection for client integration

**Pattern for Integration:**
```python
# Bad: Hardcoded port
API_URL = "http://localhost:3001"

# Good: Auto-detection
def detect_port():
    # Use lsof, ps, or scan approach
    return f"http://localhost:{detected_port}"
```

---

### Learning 3: The "Update First" Principle
**Discovery:** Version mismatch errors often resolve with updates.

**Pattern:**
1. See migration/schema error
2. Check for updates first
3. Try manual setup only after update fails

**Why:**
- Developers fix migration issues in updates
- Manual work might be unnecessary
- Updates are safer than manual surgery

---

### Learning 4: API Testing Before Coding
**Discovery:** Testing the API directly (`curl`) revealed it was already working.

**Benefits:**
- Confirmed the problem was client-side (wrong port)
- Saved time investigating server issues
- Provided immediate feedback

**Workflow:**
```
Problem → API Test → If works → Fix client code
                     If fails → Fix server
```

---

### Learning 5: Existing State Verification
**Discovery:** The BlackBox5 project already existed with 13 tasks.

**Lesson:** Always verify current state before:
- Creating resources
- Running initialization
- Making destructive changes

**Quick Checks:**
```bash
# Check existing projects
curl http://localhost:PORT/api/projects

# Check existing tasks
curl http://localhost:PORT/api/tasks?project_id=XXX
```

---

## Technical Discoveries

### Vibe Kanban API Structure
- **Base:** `/api`
- **Projects:** `/api/projects` (GET)
- **Tasks:** `/api/tasks?project_id=XXX` (GET)
- **Task Attempts:** `/api/task-attempts` (POST)

### Port Detection Methods (in order of reliability)
1. **lsof** - Most accurate for running processes
2. **ps + grep** - Find process, then check connections
3. **Port scanning** - Last resort, slower

### Vibe Kanban File Locations
- **Binary:** `~/.vibe-kanban/bin/v0.0.166-*/macos-arm64/vibe-kanban`
- **Profiles:** `~/Library/Application Support/ai.bloop.vibe-kanban/profiles.json`
- **Logs:** `~/.vibe-kanban-data/vibe-kanban.log`
- **Database:** (location not yet discovered - likely in data directory)

---

## Process Improvements

### Future Task Approach
1. **Verify actual state** before following task descriptions
2. **Test APIs directly** before writing integration code
3. **Update first** for version errors
4. **Check for existing resources** before creating new ones

### Documentation Gaps Found
- No mention of dynamic port allocation in README
- No API documentation available
- Database location not documented
- Migration process is opaque

---

## Unresolved Questions

1. **Where is the SQLite database stored?**
   - Not found in `~/.vibe-kanban-data/`
   - Not found in `~/Library/Application Support/ai.bloop.vibe-kanban/`
   - May be in temp directory or hidden location

2. **How to configure Vibe Kanban to use a fixed port?**
   - No obvious configuration option
   - May require environment variable or config file

3. **What happens when multiple instances start?**
   - Do they coordinate?
   - Can they share a database?
   - Need to test this scenario

4. **Is there a health check endpoint?**
   - `/health` returns HTML (frontend)
   - No dedicated health endpoint found
