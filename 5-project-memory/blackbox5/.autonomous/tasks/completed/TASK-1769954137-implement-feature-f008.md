# TASK-1769954137: Implement Feature F-008 (Real-time Collaboration Dashboard)

**Type:** implement (feature)
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T19:21:37Z
**Estimated Minutes:** 120 (~2 hours)

## Objective

Implement the Real-time Collaboration Dashboard (F-008), enabling RALF operators to monitor agent activities, task progress, and system health in real-time with live updates and threshold-based alerts.

## Context

**Strategic Importance:**
- **Visibility feature:** Score 4.0 (medium priority, good value)
- **Quick win:** 120 minutes estimated, immediate operational benefit
- **Category balance:** UI feature (different from F-006 config, F-007 CI/CD)

**Feature Context (from BACKLOG.md):**
- **User Value:** RALF operators (humans monitoring system)
- **Problem:** No visibility into agent activities or system health in real-time. Current metrics are static.
- **Value:** Monitor agent activities, task progress, and system health in real-time with alerts.

**Why This Task Matters:**
Currently, operators must check log files and YAML files to understand system state. A real-time dashboard provides live visibility into agent activities, queue depth, task progress, and system health. Threshold-based alerts proactively notify operators of issues (e.g., queue depth low, task failures).

**Dependencies:**
- TASK-1769916004 (Feature Framework) - ✅ COMPLETE (Run 48)
- TASK-1769916006 (Feature Backlog) - ✅ COMPLETE (Run 51)

**Queue Context:**
- This task restores queue depth from 2 → 3 tasks (target: 3-5)
- Ensures sustained feature delivery while F-006 executes

## Success Criteria

- [ ] WebSocket server for real-time updates implemented
- [ ] Live metrics dashboard created (web UI or CLI interface)
- [ ] Real-time agent activity visible (planner/executor status)
- [ ] System health metrics update live (queue depth, task progress)
- [ ] Alert system triggers on thresholds (queue depth < 2, task failure, etc.)
- [ ] Dashboard accessible via web browser or CLI
- [ ] Documented in operations/.docs/dashboard-guide.md

## Approach

### Phase 1: Feature Specification Creation (15 minutes)

**NOTE:** Feature specification does not exist yet. Create it first:

1. **Read the backlog entry** for F-008 from plans/features/BACKLOG.md
2. **Create feature specification** at plans/features/FEATURE-008-realtime-dashboard.md
3. **Document:**
   - User value (operators need visibility)
   - MVP scope (WebSocket server, live metrics, alert system)
   - Success criteria (from backlog)
   - Technical approach (WebSocket vs polling, web vs CLI)
   - Dependencies (heartbeat.yaml, events.yaml as data sources)
   - Rollout plan (start with CLI, add web UI later)
   - Risk assessment (performance impact, resource usage)

### Phase 2: Architecture Design (15 minutes)

**Data Sources:**
- `heartbeat.yaml` - Agent health status (planner, executor)
- `events.yaml` - Task completion events
- `queue.yaml` - Current queue depth and tasks
- `runs/executor/run-NN/metadata.yaml` - Active run progress

**Architecture Options:**

**Option A: WebSocket-based Web Dashboard (RECOMMENDED)**
- WebSocket server: `2-engine/.autonomous/lib/dashboard_server.py`
- Web UI: `operations/dashboard/index.html` (static HTML + JS)
- Real-time updates: WebSocket pushes updates to connected clients
- Pros: Modern, user-friendly, multiple concurrent viewers
- Cons: Requires WebSocket library (websockets or aiohttp)

**Option B: CLI-based Dashboard (Fallback)**
- CLI tool: `bin/dashboard.sh` (bash + ncurses or rich)
- Terminal-based UI with live updates
- Pros: No web dependencies, simple
- Cons: Single user, less accessible

**Decision:** Start with Option A (WebSocket web dashboard). Falls back to Option B if WebSocket setup is complex.

**Alert System Design:**
- Thresholds:
  - Queue depth < 2: "Queue low" warning
  - Queue depth = 0: "Queue empty" critical
  - Task failure: "Task failed" alert
  - Agent timeout > 120 sec: "Agent unresponsive" warning
- Alert delivery: Web notification (toast message), log entry to events.yaml

### Phase 3: WebSocket Server Implementation (40 minutes)

**Create `2-engine/.autonomous/lib/dashboard_server.py`:**
```python
#!/usr/bin/env python3
"""
Real-time Dashboard Server
Provides WebSocket API for live system monitoring
"""

import asyncio
import websockets
import json
import yaml
from pathlib import Path
from datetime import datetime

# Data sources
HEARTBEAT_FILE = Path("/workspaces/blackbox5/5-project-memory/blackbox5/.autonomous/communications/heartbeat.yaml")
EVENTS_FILE = Path("/workspaces/blackbox5/5-project-memory/blackbox5/.autonomous/communications/events.yaml")
QUEUE_FILE = Path("/workspaces/blackbox5/5-project-memory/blackbox5/.autonomous/communications/queue.yaml")

async def get_system_state():
    """Read current system state from YAML files"""
    # Read heartbeat
    with open(HEARTBEAT_FILE) as f:
        heartbeat = yaml.safe_load(f)

    # Read events (last 10)
    with open(EVENTS_FILE) as f:
        events = yaml.safe_load(f).get('events', [])[-10:]

    # Read queue
    with open(QUEUE_FILE) as f:
        queue = yaml.safe_load(f)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "heartbeat": heartbeat,
        "recent_events": events,
        "queue": queue
    }

async def dashboard_handler(websocket, path):
    """Handle WebSocket connections"""
    print(f"Client connected: {websocket.remote_address}")

    try:
        # Send initial state
        state = await get_system_state()
        await websocket.send(json.dumps(state))

        # Stream updates every 1 second
        while True:
            await asyncio.sleep(1)
            state = await get_system_state()

            # Check for alerts
            alerts = check_alerts(state)
            if alerts:
                state["alerts"] = alerts

            await websocket.send(json.dumps(state))

    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

def check_alerts(state):
    """Check thresholds and generate alerts"""
    alerts = []

    # Check queue depth
    queue_depth = len(state["queue"].get("queue", []))
    if queue_depth == 0:
        alerts.append({
            "severity": "critical",
            "message": "Queue is empty! Executor may starve."
        })
    elif queue_depth < 2:
        alerts.append({
            "severity": "warning",
            "message": f"Queue depth low ({queue_depth} tasks). Target: 3-5."
        })

    # Check agent health
    heartbeat = state["heartbeat"].get("heartbeats", {})
    for agent, data in heartbeat.items():
        last_seen = data.get("last_seen")
        if last_seen:
            # Parse timestamp and check if > 120 seconds ago
            # (simplified for MVP)
            pass

    return alerts

async def main():
    """Start WebSocket server"""
    async with websockets.serve(dashboard_handler, "localhost", 8765):
        print("Dashboard server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
```

### Phase 4: Web Dashboard UI (30 minutes)

**Create `operations/dashboard/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>RALF Real-time Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin-right: 30px; }
        .metric-label { font-size: 14px; color: #666; }
        .metric-value { font-size: 24px; font-weight: bold; color: #333; }
        .status-healthy { color: #4CAF50; }
        .status-warning { color: #FF9800; }
        .status-critical { color: #F44336; }
        .alert { padding: 10px; margin-bottom: 10px; border-radius: 4px; }
        .alert-warning { background: #FFF3E0; border-left: 4px solid #FF9800; }
        .alert-critical { background: #FFEBEE; border-left: 4px solid #F44336; }
        .task-list { list-style: none; padding: 0; }
        .task-item { padding: 10px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>RALF Real-time Dashboard</h1>

        <div class="card">
            <h2>System Health</h2>
            <div class="metric">
                <div class="metric-label">Queue Depth</div>
                <div class="metric-value" id="queue-depth">-</div>
            </div>
            <div class="metric">
                <div class="metric-label">Planner Status</div>
                <div class="metric-value" id="planner-status">-</div>
            </div>
            <div class="metric">
                <div class="metric-label">Executor Status</div>
                <div class="metric-value" id="executor-status">-</div>
            </div>
            <div class="metric">
                <div class="metric-label">Active Tasks</div>
                <div class="metric-value" id="active-tasks">-</div>
            </div>
        </div>

        <div class="card">
            <h2>Alerts</h2>
            <div id="alerts"></div>
        </div>

        <div class="card">
            <h2>Current Queue</h2>
            <ul class="task-list" id="queue-list"></ul>
        </div>

        <div class="card">
            <h2>Recent Events</h2>
            <ul class="task-list" id="events-list"></ul>
        </div>
    </div>

    <script>
        const ws = new WebSocket("ws://localhost:8765");

        ws.onmessage = function(event) {
            const state = JSON.parse(event.data);
            updateDashboard(state);
        };

        function updateDashboard(state) {
            // Update metrics
            document.getElementById("queue-depth").textContent = state.queue.queue.length;
            document.getElementById("planner-status").textContent = state.heartbeat.heartbeats.planner.status;
            document.getElementById("executor-status").textContent = state.heartbeat.heartbeats.executor.status;
            document.getElementById("active-tasks").textContent = state.queue.queue.length;

            // Update alerts
            const alertsDiv = document.getElementById("alerts");
            if (state.alerts && state.alerts.length > 0) {
                alertsDiv.innerHTML = state.alerts.map(alert =>
                    `<div class="alert alert-${alert.severity}">${alert.message}</div>`
                ).join("");
            } else {
                alertsDiv.innerHTML = "<p>No alerts</p>";
            }

            // Update queue
            const queueList = document.getElementById("queue-list");
            queueList.innerHTML = state.queue.queue.map(task =>
                `<li class="task-item">${.task}</li>`
            ).join("") || "<li>No tasks in queue</li>";

            // Update events
            const eventsList = document.getElementById("events-list");
            eventsList.innerHTML = state.recent_events.map(event =>
                `<li class="task-item">${event.type}: ${event.task_id} (${event.timestamp})</li>`
            ).join("") || "<li>No recent events</li>";
        }
    </script>
</body>
</html>
```

### Phase 5: Testing (15 minutes)

**Test WebSocket server:**
1. Start server: `python3 2-engine/.autonomous/lib/dashboard_server.py`
2. Verify WebSocket listens on `ws://localhost:8765`
3. Check logs: "Dashboard server running on ws://localhost:8765"

**Test web dashboard:**
1. Open `operations/dashboard/index.html` in browser
2. Verify metrics update every 1 second
3. Check queue depth reflects current state
4. Verify alerts appear when thresholds triggered

**Test alert system:**
1. Drain queue to 0 tasks (trigger critical alert)
2. Verify "Queue is empty!" alert appears
3. Add task back (alert clears)

### Phase 6: Documentation (5 minutes)

**Create dashboard guide:**
- File: `operations/.docs/dashboard-guide.md`
- Sections:
  - Overview (real-time monitoring, live updates)
  - Starting the server (python3 dashboard_server.py)
  - Accessing the dashboard (open index.html in browser)
  - Metrics explained (queue depth, agent status, alerts)
  - Troubleshooting (server not starting, connection issues)
  - Customization (changing thresholds, update frequency)

## Files to Create

- `plans/features/FEATURE-008-realtime-dashboard.md` (feature spec)
- `2-engine/.autonomous/lib/dashboard_server.py` (WebSocket server)
- `operations/dashboard/index.html` (web UI)
- `operations/.docs/dashboard-guide.md` (documentation)

## Files to Modify

- None (all new files)

## Notes

**Warnings:**
- WebSocket server adds resource usage (~50MB RAM)
- Polling YAML files every 1 second may impact performance
- Multiple dashboard viewers increase load

**Dependencies:**
- `websockets` library (install via `pip install websockets`)
- Modern web browser with WebSocket support

**Integration Points:**
- heartbeat.yaml (agent health data source)
- events.yaml (event log data source)
- queue.yaml (queue state data source)
- runs/*/metadata.yaml (active run data)

**Testing Strategy:**
- Start WebSocket server manually first (MVP)
- Verify browser connects and receives updates
- Check metrics reflect current system state
- Trigger alerts by draining queue

**Risk Assessment:**
- **Risk:** WebSocket library not installed
- **Mitigation:** Fall back to CLI-based dashboard (ncurses/rich)
- **Risk:** Performance impact from polling
- **Mitigation:** Cache data, reduce update frequency to 5 seconds

**Success Indicators:**
- WebSocket server starts without errors
- Browser connects and displays dashboard
- Metrics update every 1 second
- Alerts trigger on threshold violations
- Multiple users can view simultaneously

**Estimated Breakdown:**
- Feature spec: 15 min
- Architecture design: 15 min
- WebSocket server: 40 min
- Web dashboard UI: 30 min
- Testing: 15 min
- Documentation: 5 min
- **Total: 120 min (2 hours)**

**Priority Score:** 4.0
- Value: 7/10 (good visibility, monitoring value)
- Effort: 2 hours
- Score: (7 × 10) / 2 = 70 / 17.5 = 4.0

**Strategic Value:**
- Enables operational monitoring
- Improves system observability
- Proactive alerting prevents issues
- Foundation for future enhancements (historical metrics, trends)

**Queue Context:**
- Restores queue depth from 2 → 3 tasks (target: 3-5)
- Quick win (120 min) for sustained feature delivery
- UI variety (different from F-006 config, F-007 CI/CD)
