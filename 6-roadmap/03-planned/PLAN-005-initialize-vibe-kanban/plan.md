# PLAN-005: Initialize Vibe Kanban Database

**Priority:** 🔴 HIGH
**Status:** Planned
**Estimated Effort:** 1-2 hours
**Dependencies:** None (can parallel with all)
**Validation Agent:** Agent 6 (Integration & MCP)

---

## Problem Statement

Vibe Kanban database **not initialized**, causing API errors.

**Evidence:**
```python
# VibeKanbanManager.list_projects()
ERROR: API Error: 500 {"error": "Database not initialized"}
```

**Impact:**
- Can't create tasks programmatically
- Can't update task status
- Manual workflow only
- Planning Agent can't integrate

---

## Root Cause Analysis

### Vibe Kanban Server Running but No Database

**Check 1: Is Vibe Kanban server running?**
```bash
curl http://localhost:3001/health
# Expected: {"status": "ok"}
```

**Check 2: Is database initialized?**
```bash
curl http://localhost:3001/api/projects
# Actual: 500 Database not initialized
```

**Root Cause:** Vibe Kanban server started but database migrations not run

---

## Solution Design

### Phase 1: Locate Vibe Kanban Setup (15 min)

**Find Vibe Kanban installation:**
```bash
# Check if Vibe Kanban is in PATH
which vibe-kanban

# Check if running as service
ps aux | grep vibe-kanban

# Check local installation
ls -la blackbox5/vibe-kanban/
ls -la node_modules/.bin/ | grep vibe
```

**Find database setup scripts:**
```bash
# Look for migration scripts
find . -name "*migrate*" -o -name "*setup*" -o -name "*init*db*" | grep -i vibe

# Check package.json for setup commands
cat blackbox5/vibe-kanban/package.json | grep -A 5 "scripts"
```

---

### Phase 2: Initialize Database (30 min)

**Option A: Using CLI (if available)**
```bash
# Run database initialization
vibe-kanban db init

# Or
npm run db:init

# Or
yarn db:init
```

**Option B: Using migration script**
```bash
# Find migration script
cd blackbox5/vibe-kanban/

# Run migrations
npm run migrate

# Or
./scripts/migrate.sh

# Or
npx prisma migrate deploy
```

**Option C: Manual setup (if no scripts)**
```bash
# Create database
createdb vibe_kanban

# Or for SQLite
touch vibe_kanban.db

# Run schema
psql vibe_kanban < schema.sql

# Or for SQLite
sqlite3 vibe_kanban.db < schema.sql
```

---

### Phase 3: Verify Initialization (15 min)

**Test 1: Health check**
```bash
curl http://localhost:3001/health
# Expected: {"status": "ok", "database": "connected"}
```

**Test 2: List projects**
```python
from blackbox5.engine.integrations.vibe import VibeKanbanManager

manager = VibeKanbanManager(api_url="http://localhost:3001")
projects = await manager.list_projects()

print(f"✅ Found {len(projects)} projects")
```

**Test 3: Create test project**
```python
# Create test project
project = await manager.create_project(
    name="Test Project",
    description="Testing Vibe Kanban initialization"
)

print(f"✅ Created project: {project['id']}")
```

---

### Phase 4: Create BlackBox5 Project (15 min)

**Create main project:**
```python
# create_blackbox5_project.py

from blackbox5.engine.integrations.vibe import VibeKanbanManager

async def main():
    manager = VibeKanbanManager(api_url="http://localhost:3001")

    # Create BlackBox5 project
    project = await manager.create_project(
        name="BlackBox5",
        description="BlackBox5 AI Agent System Development"
    )

    print(f"Created project: {project['id']}")

    # Create columns
    columns = [
        {"name": "Backlog", "order": 1},
        {"name": "Todo", "order": 2},
        {"name": "In Progress", "order": 3},
        {"name": "In Review", "order": 4},
        {"name": "Done", "order": 5}
    ]

    for column in columns:
        col = await manager.create_column(
            project_id=project["id"],
            name=column["name"],
            order=column["order"]
        )
        print(f"Created column: {col['name']}")

    print("\n✅ Vibe Kanban ready for BlackBox5!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## Implementation Plan

### Step 1: Locate Vibe Kanban (15 min)
1. Check if Vibe Kanban installed
2. Find installation directory
3. Find setup scripts

### Step 2: Initialize Database (30 min)
1. Run database initialization
2. Run migrations
3. Verify database created

### Step 3: Test API (15 min)
1. Health check
2. List projects
3. Create test project

### Step 4: Setup BlackBox5 Project (15 min)
1. Create BlackBox5 project
2. Create columns
3. Verify ready for use

---

## Success Criteria

- ✅ Database initialized
- ✅ Migrations run successfully
- ✅ Health check passes
- ✅ Can list projects
- ✅ Can create projects
- ✅ Can create columns
- ✅ Can create cards
- ✅ API returns 200 (not 500)

---

## Rollout Plan

### Pre-conditions
- [ ] Vibe Kanban server located
- [ ] Database setup script found
- [ ] Server running

### Execution
1. Stop Vibe Kanban server (if running)
2. Initialize database
3. Run migrations
4. Start server
5. Test API
6. Create BlackBox5 project

### Post-conditions
- [ ] Database initialized
- [ ] API working
- [ ] BlackBox5 project created
- [ ] Ready for Planning Agent integration

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Setup script not found | Medium | Medium | Manual setup |
| Database permissions | Low | High | Check permissions first |
| Server not running | Low | Medium | Start server |
| Wrong database type | Low | Medium | Check configuration |

---

## Dependencies

**Blocks:**
- PLAN-003: Implement Planning Agent (needs Vibe Kanban)
- Task creation automation
- End-to-end workflow

**Blocked By:**
- None

**Can Parallel With:**
- ALL other plans (PLAN-001 through PLAN-004, PLAN-006, PLAN-007)

---

## Quick Start Commands

```bash
# 1. Locate Vibe Kanban
which vibe-kanban
ls -la blackbox5/vibe-kanban/

# 2. Initialize database (choose one)
npm run db:init        # If npm script exists
./scripts/migrate.sh   # If migration script exists
vibe-kanban db init    # If CLI exists

# 3. Start server (if not running)
npm start
# or
yarn start

# 4. Test API
curl http://localhost:3001/health

# 5. Create BlackBox5 project
python3 scripts/create-blackbox5-project.py
```

---

## Next Steps

1. Locate Vibe Kanban installation (15 min)
2. Initialize database (30 min)
3. Test API endpoints (15 min)
4. Create BlackBox5 project (15 min)

**Total Estimated Time:** 1-2 hours

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🔴 HIGH (blocks Planning Agent and automation)
