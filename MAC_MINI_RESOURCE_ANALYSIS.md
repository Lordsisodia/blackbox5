# Mac Mini Resource Analysis & Optimization

## Current State

### Hardware
- **Model**: Mac Mini M4 (Apple Silicon)
- **RAM**: 16GB
- **Storage**: 228GB (73% used)
- **OS**: macOS 15.5

### Resource Usage Summary
```
CPU: 23.68% user, 9.64% sys, 66.66% idle
Load Avg: 5.67, 5.87, 5.85
Memory: 15G used, 302M unused
Processes: 423 total
```

## What's Running

### 🔴 High Resource Usage

1. **Docker Desktop** (219% CPU, 8GB RAM allocated)
   - Using 10 CPUs
   - 8GB memory allocated to VM
   - Process: `com.apple.Virtualization.VirtualMachine`
   - Likely running Linux containers

### 🟡 Our Services

2. **YouTube Worker** (Your user - shaansisodia)
   - PID: 49408
   - CPU: 0.0%
   - MEM: 0.2% (29MB)
   - Status: ✅ Running properly
   - Config: Daily limit 100, 3s delay, batch 5

3. **YouTube Worker** (Old - youtube-pipeline user)
   - PID: 33437
   - CPU: 0.0%
   - MEM: 0.0%
   - Status: ⚠️ Still running from old setup
   - Config: Daily limit 1000, 5s delay, batch 3

4. **MoltBot/OpenClaw**
   - LaunchAgent status: `1` (exited)
   - Status: ❌ Not currently running
   - Needs investigation

### 🟢 System Processes

5. **Google Chrome** - Multiple helpers (257MB+ RAM)
6. **RustDesk** - Remote desktop (running)
7. **Various macOS services** - Normal system processes

## Issues Found

### 1. Duplicate YouTube Workers
**Problem**: Two workers running simultaneously
- Your user (shaansisodia): 49408
- Old user (youtube-pipeline): 33437

**Impact**: Double the API requests to YouTube, both getting blocked

**Solution**: Kill the old youtube-pipeline worker

### 2. Docker Using 8GB RAM
**Problem**: Docker Desktop VM allocated 8GB of 16GB RAM

**Impact**: Leaves only ~8GB for everything else

**Options**:
- Reduce Docker memory to 4GB (if containers allow)
- Stop Docker if not needed
- Keep as-is if actively using containers

### 3. MoltBot Not Running
**Problem**: LaunchAgent shows status `1` (exited)

**Possible causes**:
- OpenClaw not properly installed
- Configuration issue
- Missing dependencies

### 4. Chrome Using Significant RAM
**Problem**: Multiple Chrome helpers using 257MB+

**Impact**: Normal for browser usage, but could be optimized

## Optimization Recommendations

### Immediate Actions

1. **Stop duplicate YouTube worker**
   ```bash
   sudo kill 33437
   # Or
   sudo -u youtube-pipeline launchctl unload ~/Library/LaunchAgents/com.youtube.transcript-worker.plist
   ```

2. **Fix MoltBot**
   ```bash
   # Check why it exited
   tail -50 ~/Projects/moltbot/logs/moltbot-error.log

   # Try manual start to see errors
   ~/.local/bin/openclaw gateway
   ```

3. **Optimize Docker (if keeping)**
   - Open Docker Desktop
   - Settings > Resources > Advanced
   - Reduce CPUs from 10 to 4
   - Reduce Memory from 8GB to 4GB
   - Apply & Restart

### Resource Allocation Plan

| Service | CPU | RAM | Priority |
|---------|-----|-----|----------|
| macOS System | 2 cores | 2GB | Required |
| Docker (if needed) | 4 cores | 4GB | Optional |
| YouTube Worker | 1 core | 512MB | Low |
| MoltBot/OpenClaw | 1 core | 1GB | Medium |
| Chrome/Browsers | 2 cores | 2GB | User activity |
| Free/Buffer | 6 cores | 6GB | - |

### Monitoring Commands

```bash
# Check resource usage
ssh mac-mini "top -l 1 -n 10 -o cpu"

# Check memory
ssh mac-mini "vm_stat && echo '---' && echo '16GB Total'"

# Check our services
ssh mac-mini "ps aux | grep -E 'youtube|moltbot|openclaw' | grep -v grep"

# Check Docker
ssh mac-mini "docker stats --no-stream 2>/dev/null || echo 'Docker not running'"
```

## Questions for You

1. **Docker**: Are you actively using Docker containers? If not, we can stop it to free 8GB RAM.

2. **youtube-pipeline user**: This appears to be from a previous setup. Safe to remove?

3. **MoltBot**: Do you want me to troubleshoot why it's not starting?

4. **Chrome**: Are you actively using Chrome on the Mac Mini, or can it be closed?

## Quick Wins

1. ✅ YouTube worker IS running (yours)
2. ⚠️ Stop duplicate youtube-pipeline worker
3. ⚠️ Reduce Docker memory OR stop Docker
4. ⚠️ Fix MoltBot startup
5. ⚠️ Close unused Chrome tabs/windows

## Expected After Optimization

- **RAM Available**: ~10-12GB free
- **CPU Available**: 60-70% idle
- **Services Running**: YouTube + MoltBot smoothly
- **Headroom**: For additional workloads
