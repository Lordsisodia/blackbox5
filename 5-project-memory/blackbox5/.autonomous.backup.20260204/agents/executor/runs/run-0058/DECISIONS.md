# Decisions - TASK-1769954137

**Task:** TASK-1769954137 - Implement Feature F-008 (Real-time Collaboration Dashboard)
**Run:** 58
**Date:** 2026-02-01
**Feature:** F-008 Real-time Collaboration Dashboard

---

## Decision 1: WebSocket-based Architecture

**Context:** Need to provide real-time updates to monitoring dashboard.

**Options Considered:**
- **Option A:** WebSocket server with web UI (chosen)
- **Option B:** CLI-based dashboard with ncurses/rich
- **Option C:** REST API with client-side polling

**Selected:** Option A (WebSocket server with web UI)

**Rationale:**
1. **User Experience:** Web UI is modern, user-friendly, and accessible
2. **Collaboration:** Multiple operators can monitor simultaneously
3. **Real-time:** Server pushes updates (1-second latency) vs. polling (delayed)
4. **Performance:** Lower server load (no continuous polling requests)
5. **Extensibility:** Easy to add features (charts, themes, customization)
6. **Industry Standard:** WebSocket is the standard for real-time web apps

**Trade-offs:**
- **Pro:** Modern interface, multiple viewers, real-time updates
- **Con:** Requires websockets library (lightweight dependency)
- **Con:** Additional background process to manage
- **Pro:** Worth it for improved UX and collaboration

**Alternatives Rejected:**
- **Option B (CLI):** Single-user only, less accessible, limited UI
- **Option C (Polling):** Higher server load, delayed updates, poorer UX

**Reversibility:** LOW
- Significant effort to switch to CLI after implementing web UI
- However, web UI provides superior user experience
- CLI could be added as complementary interface in future

**Impact:**
- Positive: Enables collaborative monitoring, better UX
- Positive: Real-time updates (1-second latency)
- Positive: Foundation for future enhancements (charts, themes)
- Minimal: One additional background process (~50MB RAM)

---

## Decision 2: Update Frequency (1 Second)

**Context:** How often should the server send updates to connected clients?

**Options Considered:**
- **Option A:** 1 second (chosen)
- **Option B:** 5 seconds
- **Option C:** 10 seconds

**Selected:** Option A (1 second)

**Rationale:**
1. **Real-time Feel:** 1-second updates feel "live" to users
2. **Alert Latency:** Critical alerts (queue empty) detected within 1 second
3. **CPU Impact:** Minimal (JSON serialization is fast)
4. **User Expectations:** Monitoring dashboards expected to update frequently
5. **Industry Standard:** Most monitoring tools update every 1-5 seconds

**Trade-offs:**
- **Pro:** Low latency (users see changes within 1 second)
- **Pro:** Real-time monitoring experience
- **Con:** Slightly higher CPU usage vs. 5-second updates
- **Con:** More network traffic (1KB per client per second)

**Calculation:**
- CPU per update: ~10ms (JSON serialization)
- Updates per second: 1
- CPU utilization: < 1% (acceptable)

**Reversibility:** HIGH
- Configurable via `UPDATE_INTERVAL` constant in dashboard_server.py
- Can be adjusted based on performance feedback
- No code changes required, just configuration

**Impact:**
- Positive: Real-time monitoring experience
- Positive: Fast alert detection (1-second latency)
- Minimal: Slightly higher CPU usage (acceptable)
- Minimal: More network traffic (acceptable for local monitoring)

---

## Decision 3: Single-Page HTML Application

**Context:** How to structure the web dashboard UI?

**Options Considered:**
- **Option A:** Single HTML file with embedded CSS/JS (chosen)
- **Option B:** Separate HTML, CSS, JS files
- **Option C:** React/Vue frontend framework with build step

**Selected:** Option A (Single HTML file)

**Rationale:**
1. **Simplicity:** One file to deploy and maintain
2. **No Build Step:** No npm, webpack, or build process required
3. **Easy to Modify:** Developers can edit directly without toolchain
4. **MVP Appropriate:** Sufficient for current complexity (420 lines)
5. **Fast Development:** No setup time, instant iterations

**Trade-offs:**
- **Pro:** Simple deployment (copy one file)
- **Pro:** No build toolchain required
- **Pro:** Easy to customize and modify
- **Con:** Harder to split if file grows beyond 1000 lines
- **Con:** No code organization benefits of separate files

**When to Reconsider:**
- If file grows beyond 1000 lines
- If multiple developers working on UI simultaneously
- If need for reusable components arises

**Reversibility:** LOW
- Splitting single file into multiple files is mechanical but tedious
- However, single file works well for MVP complexity
- Can refactor in future if needed (not urgent)

**Impact:**
- Positive: Simple deployment (one file)
- Positive: Fast development (no build step)
- Positive: Easy to modify (edit HTML directly)
- Neutral: File size (420 lines is manageable)
- Neutral: Future refactoring may be needed (not urgent)

---

## Decision 4: Alert Severity Levels (Critical/Warning)

**Context:** How to categorize and display alerts?

**Options Considered:**
- **Option A:** Binary (alert vs no alert)
- **Option B:** Three-level (critical/warning/info) (chosen)
- **Option C:** Five-level (critical/error/warning/notice/info)

**Selected:** Option B (Three-level: critical/warning)

**Rationale:**
1. **Actionable:** Critical = immediate action, Warning = monitor
2. **Simple:** Easy to understand (two levels)
3. **Matches Industry:** Prometheus, Grafana use similar levels
4. **UI Clarity:** Two colors (red/orange) are clear
5. **Sufficient:** Covers all use cases without overcomplicating

**Alert Thresholds:**
| Level | Trigger | Icon | Color | Action |
|-------|---------|------|-------|--------|
| Critical | Queue depth = 0 | 🚨 | Red | Immediate action |
| Critical | Task failed | 🚨 | Red | Investigate error |
| Warning | Queue depth < 2 | ⚠️ | Orange | Monitor |
| Warning | Agent timeout > 120s | ⚠️ | Orange | Check process |

**Trade-offs:**
- **Pro:** Simple and actionable
- **Pro:** Clear visual indicators (red/orange)
- **Pro:** Matches common monitoring tools
- **Con:** Less granular than 5-level system
- **Con:** May need "info" level in future

**Reversibility:** LOW
- Changing levels requires updating:
  - Server alert generation logic
  - UI alert display (icons, colors)
  - Documentation
- However, two levels are sufficient for current needs
- "Info" level can be added in future if needed

**Impact:**
- Positive: Simple, actionable alerts
- Positive: Clear visual indicators
- Positive: Matches industry standards
- Neutral: Future expansion may add "info" level
- Minimal: Two levels sufficient for current use cases

---

## Decision 5: Port 8765 for WebSocket

**Context:** Which port should the WebSocket server listen on?

**Options Considered:**
- **Option A:** Port 8765 (chosen)
- **Option B:** Port 8080 (common HTTP port)
- **Option C:** Port 3000 (common dev port)

**Selected:** Option A (Port 8765)

**Rationale:**
1. **Uncommon:** Not conflicting with common services (80, 443, 8080, 3000)
2. **Memorable:** Easy to remember (8765)
3. **Available:** Typically available on development machines
4. **Documented:** Clearly documented in guide and logs

**Trade-offs:**
- **Pro:** Unlikely to conflict with other services
- **Pro:** Easy to remember
- **Con:** Not a standard port (custom)
- **Con:** May need to change if already in use

**Conflict Resolution:**
- If port 8765 is in use:
  1. Check with `lsof -i :8765`
  2. Kill existing process OR
  3. Change port in dashboard_server.py

**Reversibility:** HIGH
- Configurable via `WS_PORT` constant in dashboard_server.py
- Can be changed without code restructuring
- Just update constant and restart server

**Impact:**
- Positive: Unlikely to conflict with other services
- Positive: Easy to remember
- Neutral: Custom port (not standard)
- Minimal: Documented clearly in guide

---

## Decision 6: No Authentication (MVP)

**Context:** Should the dashboard require authentication?

**Options Considered:**
- **Option A:** No authentication (chosen - MVP)
- **Option B:** Basic authentication (username/password)
- **Option C:** Token-based authentication (JWT)

**Selected:** Option A (No authentication - MVP)

**Rationale:**
1. **Local Development:** Dashboard runs on localhost only
2. **MVP Scope:** Authentication is nice-to-have, not must-have
3. **Simplicity:** No additional complexity for MVP
4. **Remote Access:** Can use SSH tunnel for secure remote access
5. **Future Enhancement:** Authentication can be added later

**Security Mitigations:**
- Dashboard binds to localhost only (not 0.0.0.0)
- Remote access via SSH tunnel (encrypted)
- No exposure to public internet

**Trade-offs:**
- **Pro:** Simple implementation (no auth code)
- **Pro:** No password management overhead
- **Pro:** Sufficient for local development
- **Con:** Not suitable for production deployment
- **Con:** Anyone on localhost can access

**When to Add Authentication:**
- If deploying to production server
- If multiple users need different access levels
- If dashboard exposed to network (not localhost)

**Reversibility:** MEDIUM
- Adding authentication later requires:
  - Server-side auth logic
  - Client-side login UI
  - Credential storage (config file or database)
- However, localhost-only access is sufficient for MVP
- SSH tunnel provides secure remote access

**Impact:**
- Positive: Simple MVP implementation
- Positive: No credential management
- Positive: Sufficient for local development
- Negative: Not production-ready (acceptable for MVP)
- Neutral: Can be added in future (not urgent)

---

## Decision 7: Data Source Integration (Read-Only)

**Context:** How should the dashboard integrate with existing YAML files?

**Options Considered:**
- **Option A:** Read-only (chosen)
- **Option B:** Read-write (dashboard can modify YAML files)

**Selected:** Option A (Read-only)

**Rationale:**
1. **Separation of Concerns:** Dashboard is monitoring-only (not control)
2. **Safety:** No risk of dashboard corrupting YAML files
3. **Simplicity:** No write logic or file locking needed
4. **Existing Agents:** Planner/Executor already manage YAML files
5. **Future:** Control features can be added later (if needed)

**What Dashboard Reads:**
- `heartbeat.yaml` - Agent health status
- `events.yaml` - Event log
- `queue.yaml` - Task queue state

**What Dashboard Does NOT Do:**
- Modify YAML files
- Write events
- Update queue
- Control agent behavior

**Trade-offs:**
- **Pro:** Safe (no risk of data corruption)
- **Pro:** Simple (no write logic)
- **Pro:** Clear separation (monitoring vs control)
- **Con:** Cannot control agents from dashboard
- **Con:** Cannot add tasks from dashboard

**Future Control Features:**
- Add task to queue (button in dashboard)
- Pause/resume agents (control buttons)
- Trigger manual sync (action button)
- Edit configuration (settings panel)

**Reversibility:** LOW
- Adding write capability later requires:
  - File locking logic (prevent concurrent writes)
  - YAML write and validation
  - UI for control features
- However, read-only is appropriate for monitoring dashboard
- Control features are separate concern (future enhancement)

**Impact:**
- Positive: Safe (no data corruption risk)
- Positive: Simple (no write logic)
- Positive: Clear separation of concerns
- Neutral: No control features (monitoring-only is MVP scope)
- Neutral: Future control features can be added

---

## Summary of Decisions

| Decision | Choice | Reversibility | Rationale |
|----------|--------|---------------|-----------|
| Architecture | WebSocket + Web UI | LOW | Modern UX, collaboration, real-time |
| Update Frequency | 1 second | HIGH | Real-time feel, low CPU |
| UI Structure | Single HTML file | LOW | Simple, no build step |
| Alert Levels | Critical/Warning | LOW | Actionable, simple |
| WebSocket Port | 8765 | HIGH | Uncommon, memorable |
| Authentication | None (MVP) | MEDIUM | Local dev, SSH tunnel |
| Data Access | Read-only | LOW | Safe, simple, separation of concerns |

**Overall Philosophy:**
- **Simplicity First:** Single-file HTML, no build step, no auth (MVP)
- **Real-time Focus:** 1-second updates, WebSocket push
- **Safety:** Read-only access, localhost-only
- **Extensibility:** Easy to add features later (configurable thresholds, auth, control)

**Key Trade-offs:**
- Chose modern UX (web UI) over simplicity (CLI)
- Chose real-time (1s updates) over efficiency (5s updates)
- Chose safety (read-only) over capability (control)
- Chose simplicity (no auth) over security (authentication)

**All decisions aligned with MVP goals:** deliver a functional, useful monitoring dashboard quickly, with clear paths for future enhancements.
