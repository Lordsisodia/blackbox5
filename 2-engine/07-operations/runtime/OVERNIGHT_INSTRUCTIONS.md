# BLACKBOX5 Overnight Monitoring - Setup Instructions

## Status: ⚠️ Server Start Issues Detected

The BLACKBOX5 server is currently experiencing module import issues and cannot start automatically.

## Quick Setup for Overnight Monitoring

### Option 1: Manual Server Start + Monitor (Recommended)

1. **Start the BLACKBOX5 server manually** in a terminal:
   ```bash
   cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/01-core
   python3 -m uvicorn interface.api.server:app --host 0.0.0.0 --port 8000
   ```

   Keep this terminal open.

2. **In another terminal, start the overnight monitor**:
   ```bash
   cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/07-operations/runtime
   nohup python3 overnight_monitor.py > /tmp/overnight_monitor.out 2>&1 &
   ```

3. **Monitor the logs**:
   ```bash
   tail -f /tmp/blackbox5_overnight.log
   ```

### Option 2: Check Existing Setup

The autonomous tester may have already started the server. Check:
```bash
curl -s http://localhost:8000/health
```

If this returns a JSON response, the server is running and you can just start the monitor:
```bash
cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5/2-engine/07-operations/runtime
nohup python3 overnight_monitor.py > /tmp/overnight_monitor.out 2>&1 &
```

## What the Monitor Does

The overnight monitor:
- ✅ Checks BLACKBOX5 health every 60 seconds
- ✅ Checks agents endpoint availability
- ✅ Logs all health status to `/tmp/blackbox5_overnight.log`
- ✅ Logs structured data to `/tmp/blackbox5_health.jsonl`
- ✅ Alerts on 3+ consecutive failures
- ✅ Does NOT modify any code
- ✅ Does NOT restart the server (avoiding crashes)

## Logs to Check

- **Monitor log**: `tail -f /tmp/blackbox5_overnight.log`
- **Health data**: `cat /tmp/blackbox5_health.jsonl`
- **Monitor output**: `tail -f /tmp/overnight_monitor.out`

## Stopping the Monitor

```bash
pkill -f "overnight_monitor.py"
```

## Tomorrow Morning

1. Check the summary at the end of the log file
2. Review health data in `/tmp/blackbox5_health.jsonl`
3. Count failures/success rate

## Current Issues to Fix Tomorrow

1. **Server Import Errors**: The `interface.api.server:app` cannot import `core.kernel`
   - File: `interface/api/server.py` line 24
   - Error: `ModuleNotFoundError: No module named 'core'`
   - Fix needed: Update import paths or PYTHONPATH

2. **Routing Issues**: The autonomous tester was adding tags but routing still fails
   - Root cause: `architect` agent has overly broad capabilities
   - Fix needed: Rebalance architect capabilities or adjust routing weights

3. **Server Instability**: Server crashes during restarts in autonomous tester
   - Fix needed: Better startup sequencing or avoid restarts altogether

## Process Status

To check if processes are running:
```bash
# Check server
ps aux | grep uvicorn

# Check monitor
ps aux | grep overnight_monitor

# Check port 8000
lsof -i :8000
```
