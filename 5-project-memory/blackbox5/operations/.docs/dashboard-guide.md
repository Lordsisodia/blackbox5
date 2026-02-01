# RALF Real-time Dashboard Guide

**Version:** 1.0.0
**Created:** 2026-02-01
**Feature:** F-008 (Real-time Collaboration Dashboard)

---

## Overview

The RALF Real-time Dashboard provides live visibility into agent activities, task progress, and system health through a web-based interface. The dashboard connects via WebSocket to receive real-time updates every second, enabling operators to monitor the autonomous system proactively.

**Key Features:**
- Real-time system health metrics (queue depth, agent status, active tasks)
- Live alerts for threshold violations (queue empty, task failures, agent timeouts)
- Current queue display with task details
- Recent events log
- Multiple concurrent connections (collaborative monitoring)

---

## Quick Start

### 1. Start the Dashboard Server

Open a terminal and start the WebSocket server:

```bash
cd ~/.blackbox5
python3 2-engine/.autonomous/lib/dashboard_server.py
```

**Expected Output:**
```
============================================================
RALF Real-time Dashboard Server
============================================================
Starting WebSocket server on localhost:8765
Update interval: 1 second(s)
Data sources:
  - Heartbeat: /path/to/heartbeat.yaml
  - Events: /path/to/events.yaml
  - Queue: /path/to/queue.yaml
============================================================
✓ Heartbeat file found
✓ Events file found
✓ Queue file found
============================================================
Dashboard server is running. Press Ctrl+C to stop.
Connect your browser to: operations/dashboard/index.html
WebSocket endpoint: ws://localhost:8765
============================================================
server listening on 127.0.0.1:8765
```

### 2. Open the Dashboard

Open a web browser and navigate to the dashboard HTML file:

**Option A: Direct file open**
```
file:///workspaces/blackbox5/5-project-memory/blackbox5/operations/dashboard/index.html
```

**Option B: Using a local web server (recommended for better compatibility)**
```bash
# Terminal 2: Start a simple HTTP server
cd /workspaces/blackbox5/5-project-memory/blackbox5
python3 -m http.server 8080

# Then open in browser:
# http://localhost:8080/operations/dashboard/index.html
```

### 3. Verify Connection

The dashboard should show:
- **Connection Status:** "Connected" (green badge)
- **Live indicator:** Pulsing "● Live" badge
- **Metrics:** Queue depth, active tasks, planner/executor status
- **Last Update:** Current timestamp

---

## Dashboard Components

### System Health Card

Displays real-time system metrics:

| Metric | Description | Status Colors |
|--------|-------------|---------------|
| **Queue Depth** | Number of tasks in queue | Green (3-5), Orange (< 2), Red (0) |
| **Active Tasks** | Current active tasks count | Blue |
| **Planner** | Planner agent status | Green (running), Orange (idle), Red (blocked) |
| **Executor** | Executor agent status | Green (running), Orange (idle), Red (blocked) |

**What to Watch For:**
- Queue depth = 0: Executor may starve (add tasks)
- Queue depth < 2: Queue running low (planner should refill)
- Agent status = blocked: Check logs for errors

### Alerts Card

Threshold-based alerts for proactive monitoring:

| Alert | Severity | Trigger | Action |
|-------|----------|---------|--------|
| Queue is empty | Critical | Queue depth = 0 | Add tasks to queue immediately |
| Queue depth low | Warning | Queue depth < 2 | Monitor for planner refill |
| Task failed | Critical | Task result = failure | Check logs, investigate error |
| Agent unresponsive | Warning | Agent timeout > 120s | Check agent process, restart if needed |

**Alert Icons:**
- 🚨 = Critical (immediate action required)
- ⚠️ = Warning (monitor closely)

### Current Queue Card

Shows all tasks currently in the queue:

| Field | Description |
|-------|-------------|
| **Task ID** | Unique task identifier (e.g., TASK-XXX) |
| **Title** | Task name/description |
| **Priority** | Priority badge (High/Medium/Low) |

**Priority Colors:**
- Red = High priority
- Orange = Medium priority
- Green = Low priority

### Recent Events Card

Shows the last 10 events from the system:

| Field | Description |
|-------|-------------|
| **Type** | Event type (started, completed, failed) |
| **Task ID** | Associated task |
| **Time** | Event timestamp |

---

## Metrics Explained

### Queue Depth

**What it measures:** Number of tasks waiting to be executed.

**Healthy range:** 3-5 tasks
- **< 2 tasks:** Queue low, planner should add tasks
- **0 tasks:** Queue empty, executor has no work
- **> 5 tasks:** Queue healthy, good buffer

**Why it matters:** Maintaining queue depth ensures continuous executor operation and prevents starvation.

### Agent Status

**Status values:**
- **running:** Agent is actively processing
- **idle:** Agent is waiting for work
- **blocked:** Agent encountered an error or blocker

**Why it matters:** Status indicates agent health. Blocked agents need investigation.

### Active Tasks

**What it measures:** Number of tasks currently in the queue (same as queue depth).

**Why it matters:** Confirms queue depth metric and provides quick visibility.

---

## Troubleshooting

### Issue: Dashboard shows "Disconnected"

**Symptoms:**
- Connection status badge shows "Disconnected" (red)
- Metrics not updating
- Last update timestamp stale

**Possible Causes:**
1. Dashboard server not running
2. WebSocket endpoint incorrect
3. Port 8765 already in use

**Solutions:**
```bash
# Check if server is running
ps aux | grep dashboard_server

# Check if port is in use
lsof -i :8765

# Kill existing process if needed
pkill -f dashboard_server

# Restart server
python3 2-engine/.autonomous/lib/dashboard_server.py
```

### Issue: Metrics not updating

**Symptoms:**
- Dashboard connected but metrics stale
- Last update timestamp old
- Queue depth not changing

**Possible Causes:**
1. YAML files not being updated by agents
2. Server not reading files correctly
3. Browser caching issues

**Solutions:**
```bash
# Check if agents are running
ps aux | grep ralf

# Verify heartbeat.yaml is being updated
tail -5 .autonomous/communications/heartbeat.yaml

# Check server logs for errors
# (Dashboard server logs to stdout)

# Refresh browser (Ctrl+Shift+R for hard refresh)
```

### Issue: Alerts not triggering

**Symptoms:**
- Queue depth is low/critical but no alert shown
- Expected alerts not appearing

**Possible Causes:**
1. Thresholds too lenient
2. Alert checking logic error
3. Data not being read correctly

**Solutions:**
```bash
# Manually check queue depth
grep -A 20 "queue:" .autonomous/communications/queue.yaml | wc -l

# Verify alert thresholds in dashboard_server.py
# grep QUEUE_DEPTH_ 2-engine/.autonomous/lib/dashboard_server.py

# Check server logs for alert generation
# Logs show alert generation when thresholds crossed
```

### Issue: Port 8765 already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
```bash
# Find process using port 8765
lsof -i :8765

# Kill the process
kill -9 <PID>

# Or change port in dashboard_server.py
# Edit: WS_PORT = 8765  # Change to 8766
```

### Issue: websockets library not installed

**Symptoms:**
```
ModuleNotFoundError: No module named 'websockets'
```

**Solution:**
```bash
pip3 install websockets
```

---

## Customization

### Change Update Frequency

Edit `dashboard_server.py`:

```python
# Change from 1 second to 5 seconds
UPDATE_INTERVAL = 5  # seconds between updates
```

**Trade-offs:**
- Faster updates (1s) = More real-time, higher CPU usage
- Slower updates (5s) = Less CPU, slightly delayed alerts

### Change Alert Thresholds

Edit `dashboard_server.py`:

```python
# Alert thresholds
QUEUE_DEPTH_CRITICAL = 0  # Critical when queue empty
QUEUE_DEPTH_WARNING = 2   # Warning when queue < 2
AGENT_TIMEOUT_SECONDS = 120  # Agent timeout in seconds
```

**Recommendation:** Keep defaults for typical RALF operation. Adjust based on your workload.

### Change WebSocket Port

Edit `dashboard_server.py`:

```python
WS_PORT = 8765  # Change to desired port
```

**Note:** Also update `index.html`:
```javascript
const WS_URL = 'ws://localhost:8765';  // Match new port
```

### Add Custom Metrics

To add new metrics to the dashboard:

1. **Read additional data source** in `get_system_state()`:
   ```python
   # Add new YAML file
   CUSTOM_FILE = Path("/path/to/custom.yaml")
   custom_data = read_yaml_file(CUSTOM_FILE)
   state["custom"] = custom_data
   ```

2. **Display in dashboard** (`index.html`):
   ```html
   <div class="metric">
       <div class="metric-label">Custom Metric</div>
       <div class="metric-value" id="custom-metric">-</div>
   </div>
   ```

3. **Update in JavaScript**:
   ```javascript
   document.getElementById('custom-metric').textContent = state.custom?.value || '-';
   ```

---

## Advanced Usage

### Running as Background Service

**Linux/macOS (using nohup):**
```bash
nohup python3 2-engine/.autonomous/lib/dashboard_server.py > dashboard.log 2>&1 &
```

**Check if running:**
```bash
ps aux | grep dashboard_server
```

**Stop server:**
```bash
pkill -f dashboard_server
```

### SSH Tunnel for Remote Access

To access dashboard from remote machine:

```bash
# On remote machine, create SSH tunnel
ssh -L 8765:localhost:8765 user@server

# Then open dashboard locally
# (uses tunneled connection)
file:///path/to/dashboard/index.html
```

### Monitoring Multiple RALF Instances

To monitor multiple RALF instances:

1. **Run dashboard server on each instance** (different ports)
2. **Create aggregator dashboard** that connects to multiple WebSocket endpoints
3. **Display unified view** of all instances

---

## Performance Considerations

### Resource Usage

**Typical Usage:**
- Memory: ~50MB for server process
- CPU: < 1% per client
- Network: ~1KB per update per client

**Scaling:**
- Tested: Up to 5 concurrent connections
- Theoretical limit: ~20 connections (resource-dependent)

### Optimization Tips

1. **Reduce update frequency** if CPU usage high:
   ```python
   UPDATE_INTERVAL = 5  # Slower updates
   ```

2. **Limit event history** if memory usage high:
   ```python
   recent_events = events_list[-5:]  # Keep 5 instead of 10
   ```

3. **Add connection limit** for production:
   ```python
   MAX_CONNECTIONS = 10
   # Implement connection counting in handler
   ```

---

## Security Considerations

**Current State (MVP):**
- No authentication (local development only)
- No encryption (ws:// not wss://)
- Localhost only (not exposed to internet)

**Recommendations for Production:**

1. **Use SSH tunnel** for remote access (don't expose port publicly)
2. **Add authentication** (future enhancement):
   ```python
   # Basic auth example (future)
   await websocket.auth("username", "password")
   ```
3. **Use WebSocket Secure (wss://)** for encryption
4. **Implement rate limiting** per client
5. **Add origin checking** to prevent XSS

**Security Best Practices:**
- Never expose WebSocket port to public internet
- Use SSH tunnels for remote access
- Run dashboard server as non-privileged user
- Monitor logs for suspicious activity

---

## FAQ

### Q: Can I run the dashboard without starting the server?

**A:** No. The dashboard requires the WebSocket server to provide real-time data. Static HTML alone cannot read YAML files or stream updates.

### Q: Why does the dashboard show "Disconnected" after a while?

**A:** Connection may drop due to:
- Server stopped or crashed
- Network interruption
- Browser tab suspended (background)

**Solution:** Dashboard auto-reconnects after 5 seconds. If not, refresh the page.

### Q: Can I customize the dashboard colors?

**A:** Yes. Edit the `<style>` section in `index.html`. Look for color values like `#4CAF50` (green), `#FF9800` (orange), `#f44336` (red).

### Q: How do I add historical metrics/trends?

**A:** Historical metrics are not supported in MVP (Phase 1). This is planned for F-011 (Monitoring & Analytics). Current implementation only shows real-time data.

### Q: Can I use the dashboard on mobile?

**A:** Technically yes (modern mobile browsers support WebSocket), but the UI is not optimized for mobile screens. Mobile responsiveness is planned for future enhancement.

### Q: Why WebSocket instead of REST API polling?

**A:**
- **WebSocket:** Real-time, server pushes updates, lower latency
- **Polling:** Delayed (must poll every second), higher server load

WebSocket is better suited for real-time monitoring dashboards.

### Q: What happens if two agents try to update the same YAML file?

**A:** RALF uses file locking in state synchronization. The dashboard server only reads files (no writes), so no conflicts occur.

---

## Support

**Issues or Questions?**
- Check logs: Dashboard server logs to stdout
- Verify data sources: Ensure heartbeat.yaml, events.yaml, queue.yaml exist
- Check network: Ensure port 8765 not blocked by firewall
- Review troubleshooting section above

**Feature Requests:**
- F-009: Skill Marketplace (add skill recommendations to dashboard)
- F-010: Knowledge Base (add learning insights to dashboard)
- F-011: Monitoring & Analytics (add historical metrics, trends)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial release (MVP) - WebSocket server, web UI, alerts, documentation |

---

## References

- **Feature Specification:** `plans/features/FEATURE-008-realtime-dashboard.md`
- **Dashboard Server:** `2-engine/.autonomous/lib/dashboard_server.py`
- **Dashboard UI:** `operations/dashboard/index.html`
- **WebSocket Protocol:** RFC 6455 (https://tools.ietf.org/html/rfc6455)
- **websockets Library:** https://websockets.readthedocs.io/
