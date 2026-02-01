# Critical Gaps Resolution Plan

**Purpose:** Fix 5 critical gaps in BlackBox5's core systems to enable safe, reliable autonomous operation.

**Date:** 2026-01-21
**Status:** 🟡 READY FOR EXECUTION
**Estimated Effort:** 3-5 days of focused work

---

## Executive Summary

We've identified 5 critical gaps through first-principles verification:

| Gap | Risk | Impact | Priority | Effort |
|-----|------|--------|----------|--------|
| 1. KillSwitch untested | 🔴 Catastrophic | Unlimited damage | P0 | 1 day |
| 2. StateManager races | 🔴 High | Lost work | P0 | 4 hours |
| 3. HealthMonitor no heal | 🟡 Med-High | Degraded performance | P1 | 1 day |
| 4. Orchestrator no resume | 🟡 Medium | Wasted compute | P1 | 4 hours |
| 5. ModelRouter unvalidated | 🟡 Medium | Wasted money | P2 | 1 day |

**Total Effort:** ~3-5 days
**Approach:** Fix in priority order, test each fix thoroughly before moving to next

---

## Gap 1: KillSwitch Never Tested 🔴 P0

### Problem
KillSwitch is designed to stop all agents in emergencies but has never been tested. No verification that:
- Broadcast reaches all agents
- Agents actually stop
- Recovery works after kill

### Risk Level
🔴 **CATASTROPHIC** - Rogue agent could cause unlimited damage

### Solution: 4-Phase Testing & Hardening

#### Phase 1: Add Delivery Confirmation (2 hours)

**File:** `2-engine/01-core/safety/kill_switch.py`

**Changes:**
```python
class KillSwitch:
    def __init__(self):
        self._acknowledgments = {}  # agent_id -> timestamp
        self._expected_agents = set()

    def trigger(self, reason: KillSwitchReason, message: str, source: str) -> bool:
        # ... existing code ...

        # 1. Get list of running agents
        self._expected_agents = self._get_running_agents()

        # 2. Broadcast trigger
        self._broadcast_trigger(reason, message, source)

        # 3. Wait for acknowledgments (with timeout)
        acked = await self._wait_for_acknowledgments(timeout=5.0)

        # 4. Check missing agents
        missing = self._expected_agents - set(acked.keys())
        if missing:
            logger.critical(f"Kill switch: Agents did not acknowledge: {missing}")
            # Don't return True - trigger failed

        return len(missing) == 0

    def register_acknowledgment(self, agent_id: str, stopped: bool):
        """Called by agents when they receive kill signal"""
        self._acknowledgments[agent_id] = {
            'timestamp': datetime.now(),
            'stopped': stopped
        }

    async def _wait_for_acknowledgments(self, timeout: float) -> Dict[str, Any]:
        """Wait for all agents to acknowledge kill signal"""
        started = datetime.now()

        while (datetime.now() - started).total_seconds() < timeout:
            acked = set(self._acknowledgments.keys())
            if acked == self._expected_agents:
                break
            await asyncio.sleep(0.1)

        return self._acknowledgments
```

**Test:**
```python
# test_kill_switch.py
async def test_delivery_confirmation():
    ks = get_kill_switch()

    # Register 3 mock agents
    agents = [MockAgent(f"agent-{i}") for i in range(3)]

    # Trigger kill switch
    triggered = ks.trigger(KillSwitchReason.MANUAL, "Test")

    # Verify all acknowledged
    assert len(ks._acknowledgments) == 3
    assert triggered == True
```

#### Phase 2: Add Compliance Verification (2 hours)

**File:** `2-engine/01-core/safety/kill_switch.py`

**Changes:**
```python
class KillSwitch:
    async def _verify_agents_stopped(self) -> bool:
        """Verify all agents actually stopped"""
        for agent_id in self._expected_agents:
            agent = self._get_agent(agent_id)

            # Check agent is not running
            if agent.is_running:
                logger.critical(f"Agent {agent_id} still running after kill!")
                return False

        return True

    def trigger(self, reason, message, source):
        # ... wait for acknowledgments ...

        # Verify agents stopped
        if not await self._verify_agents_stopped():
            logger.critical("Kill switch: Agents still running!")
            # Force kill via SIGKILL
            await self._force_kill_agents()
            return False

        return True
```

**Test:**
```python
async def test_compliance_verification():
    ks = get_kill_switch()

    # Create non-compliant agent (ignores kill signal)
    bad_agent = NonCompliantAgent()

    # Trigger should fail
    triggered = ks.trigger(KillSwitchReason.MANUAL, "Test")

    # Should have forced kill
    assert triggered == False
    assert bad_agent.was_killed == True
```

#### Phase 3: Add Recovery Testing (2 hours)

**File:** `2-engine/01-core/safety/kill_switch.py`

**Changes:**
```python
class KillSwitch:
    def test_recovery(self) -> bool:
        """Test that system can recover after kill"""
        logger.info("Testing kill switch recovery...")

        # 1. Save current state
        state_before = {
            'services': list(self._services.keys()),
            'health': self._check_health()
        }

        # 2. Trigger kill
        self.trigger(KillSwitchReason.MANUAL, "Recovery test")

        # 3. Attempt recovery
        recovered = self.recover("Recovery test complete")

        # 4. Verify system is functional
        if recovered:
            state_after = {
                'services': list(self._services.keys()),
                'health': self._check_health()
            }

            # Services should be running again
            assert state_after['services'] == state_before['services']
            assert state_after['health']['status'] == 'healthy'

        return recovered
```

**Test:**
```python
async def test_recovery():
    ks = get_kill_switch()

    # Trigger and recover
    ks.trigger(KillSwitchReason.MANUAL, "Test")
    recovered = ks.recover("Recovery test")

    # Verify system is functional
    assert recovered == True
    assert kernel.is_operational()
```

#### Phase 4: Add Backup Trigger (2 hours)

**File:** `2-engine/01-core/safety/kill_switch.py`

**Changes:**
```python
class KillSwitch:
    def __init__(self):
        self._backup_trigger_file = Path(".kill_switch_backup")

    def _broadcast_trigger(self, reason, message, source):
        """Primary broadcast via event bus"""
        try:
            from ..communication.event_bus import get_event_bus
            event_bus = get_event_bus()
            event_bus.publish("safety.kill_switch.triggered", {...})
        except Exception as e:
            logger.error(f"Event bus broadcast failed: {e}")
            # Use backup trigger
            self._backup_trigger(reason, message, source)

    def _backup_trigger(self, reason, message, source):
        """Backup trigger via filesystem"""
        logger.warning("Using backup trigger (filesystem)")

        self._backup_trigger_file.write_text(json.dumps({
            'reason': reason.value,
            'message': message,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }))

    def check_backup_trigger(self) -> bool:
        """Check for backup trigger signal"""
        if self._backup_trigger_file.exists():
            data = json.loads(self._backup_trigger_file.read_text())
            reason = KillSwitchReason(data['reason'])
            self.trigger(reason, data['message'], data['source'])
            self._backup_trigger_file.unlink()
            return True
        return False
```

**Add to agent startup:**
```python
class BaseAgent:
    async def start(self):
        # Check for backup trigger on startup
        ks = get_kill_switch()
        if ks.check_backup_trigger():
            # Kill switch was triggered while agent was down
            return False

        # Normal startup
        # ...
```

#### Phase 5: Integration Test (2 hours)

**File:** `2-engine/01-core/safety/tests/test_kill_switch_integration.py`

**Test:**
```python
async def test_kill_switch_full_emergency():
    """Simulate real emergency scenario"""

    # Setup: Start multiple agents
    agents = [start_agent(f"agent-{i}") for i in range(5)]

    # Simulate: Agent-2 goes rogue (deleting files)
    rogue_agent = agents[2]
    rogue_agent.start_corrupting_files()

    # Trigger emergency kill
    ks = get_kill_switch()
    triggered = ks.trigger(
        KillSwitchReason.SAFETY_VIOLATION,
        "Agent deleting files",
        source="file_monitor"
    )

    # Verify: All agents acknowledged
    assert len(ks._acknowledgments) == 5

    # Verify: All agents stopped
    for agent in agents:
        assert agent.is_running == False

    # Verify: Rogue agent stopped
    assert rogue_agent.is_corrupting == False

    # Verify: System can recover
    recovered = ks.recover("Rogue agent stopped")
    assert recovered == True

    # Verify: Agents can restart
    for agent in agents:
        await agent.start()
        assert agent.is_running == True
```

### Success Criteria
✅ Kill switch reaches all agents (verified via acknowledgments)
✅ All agents stop when triggered (verified via compliance check)
✅ System can recover after kill (verified via recovery test)
✅ Backup trigger works if event bus fails

### Estimated Time: 1 day (8 hours)

---

## Gap 2: StateManager Race Conditions 🔴 P0

### Problem
Multiple processes can write to STATE.md simultaneously → file corruption

### Risk Level
🔴 **HIGH** - Workflow corruption = lost work

### Solution: File Locking + Backups + Validation

#### Fix 1: Add File Locking (2 hours)

**File:** `2-engine/01-core/state/state_manager.py`

**Changes:**
```python
import fcntl
import errno
from contextlib import contextmanager

class StateManager:
    def __init__(self, state_path: Optional[Path] = None):
        self.state_path = state_path or Path("STATE.md")
        self._lock_file = self.state_path.with_suffix('.lock')

    @contextmanager
    def _lock_state(self):
        """Acquire exclusive lock on STATE.md"""
        # Open lock file
        lock_file = open(self._lock_file, 'w')

        try:
            # Try to acquire exclusive lock
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Acquired lock
            yield lock_file

        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                raise RuntimeError(
                    f"STATE.md is locked by another process. "
                    f"If stale, delete {self._lock_file}"
                )
            raise
        finally:
            # Release lock
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()

    def update(self, workflow_id, ...):
        with self._lock_state():
            # Read current state
            if self.state_path.exists():
                content = self.state_path.read_text()
                existing_state = self.parse_state(content)

            # ... modify state ...

            # Write NEW state atomically
            self._write_state_atomic(workflow_state)

    def _write_state_atomic(self, workflow_state):
        """Write state atomically with backup"""
        # 1. Create backup
        if self.state_path.exists():
            backup_path = self.state_path.with_suffix('.backup')
            self.state_path.replace(backup_path)

        # 2. Write to temp file
        temp_path = self.state_path.with_suffix('.tmp')
        content = workflow_state.to_markdown()
        temp_path.write_text(content, encoding='utf-8')

        # 3. Atomic rename
        temp_path.rename(self.state_path)
```

#### Fix 2: Add Markdown Validation (1 hour)

**File:** `2-engine/01-core/state/state_manager.py`

**Changes:**
```python
class StateManager:
    def validate_markdown(self, content: str) -> List[str]:
        """Validate STATE.md markdown format"""
        errors = []

        # Check 1: Must have workflow header
        if not re.search(r'^# Workflow:', content, re.MULTILINE):
            errors.append("Missing '# Workflow:' header")

        # Check 2: Must have status line
        if 'Wave' not in content or '/' not in content:
            errors.append("Missing 'Wave X/Y' status line")

        # Check 3: Must have at least one section
        if not re.search(r'^## ', content, re.MULTILINE):
            errors.append("Missing sections (## Completed, etc.)")

        # Check 4: Checkboxes must be valid
        invalid_lines = re.findall(r'^- \[[^x~ ]\]', content, re.MULTILINE)
        if invalid_lines:
            errors.append(f"Invalid checkboxes: {invalid_lines}")

        return errors

    def parse_state(self, content: str) -> Optional[WorkflowState]:
        """Parse STATE.md with validation"""
        # Validate first
        errors = self.validate_markdown(content)
        if errors:
            logger.error(f"Invalid STATE.md: {errors}")
            # Try to parse anyway, but log errors
            # Could raise exception here instead

        # ... existing parse logic ...
```

#### Fix 3: Add Concurrent Write Recovery (1 hour)

**File:** `2-engine/01-core/state/state_manager.py`

**Changes:**
```python
class StateManager:
    def update(self, workflow_id, ...):
        max_retries = 3
        retry_delay = 0.5  # seconds

        for attempt in range(max_retries):
            try:
                with self._lock_state():
                    # ... update logic ...
                    return

            except RuntimeError as e:
                if "locked by another process" in str(e):
                    if attempt < max_retries - 1:
                        logger.warning(f"STATE.md locked, retrying ({attempt+1}/{max_retries})")
                        await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        logger.error(f"Could not acquire lock after {max_retries} attempts")
                        raise
```

#### Test: (1 hour)

**File:** `2-engine/01-core/state/tests/test_state_manager_concurrent.py`

```python
async def test_concurrent_updates():
    """Test that concurrent updates don't corrupt STATE.md"""
    sm = StateManager()

    # Initialize state
    sm.initialize("wf-1", "Test Workflow", 5, [...])

    # Simulate 10 concurrent updates
    tasks = []
    for i in range(10):
        task = asyncio.create_task(
            sm.update("wf-1", "Test", i, 5, [...], [...], [...])
        )
        tasks.append(task)

    # Wait for all to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Verify: No exceptions
    for result in results:
        assert not isinstance(result, Exception)

    # Verify: STATE.md is valid
    content = sm.state_path.read_text()
    state = sm.parse_state(content)
    assert state is not None
    assert state.current_wave == 9  # Last update should win
```

### Success Criteria
✅ Concurrent writes don't corrupt STATE.md
✅ Backup file created before each write
✅ Invalid markdown detected and rejected
✅ Lock acquisition retries with exponential backoff

### Estimated Time: 4 hours

---

## Gap 3: HealthMonitor No Self-Healing 🟡 P1

### Problem
HealthMonitor detects degradation but doesn't automatically fix it

### Risk Level
🟡 **MEDIUM-HIGH** - System runs degraded until human notices

### Solution: Automatic Recovery + Alerting

#### Fix 1: Implement Automatic Recovery (3 hours)

**File:** `2-engine/01-core/infrastructure/health.py`

**Changes:**
```python
class HealthMonitor:
    def __init__(self, service_registry=None):
        self._registry = service_registry
        self._recovery_attempts = {}  # service -> count

    async def _check_all_services(self) -> SystemHealth:
        for name, check in self._checks.items():
            if not check.enabled:
                continue

            try:
                result = await asyncio.wait_for(
                    asyncio.to_thread(check.check_func),
                    timeout=check.timeout
                )

                if result:
                    # Service is healthy, reset recovery count
                    check.consecutive_failures = 0
                    self._recovery_attempts[name] = 0
                else:
                    # Service is unhealthy, attempt recovery
                    check.consecutive_failures += 1

                    if check.consecutive_failures >= self._failure_threshold:
                        await self._attempt_recovery(name, check)

            except asyncio.TimeoutError:
                logger.warning(f"Health check timed out: {name}")
                check.consecutive_failures += 1

    async def _attempt_recovery(self, service_name: str, health_check: HealthCheck):
        """Attempt to recover an unhealthy service"""

        # Check if we've exceeded max attempts
        attempts = self._recovery_attempts.get(service_name, 0)
        if attempts >= 3:
            logger.error(f"Max recovery attempts exceeded for {service_name}")
            await self._alert_humans(service_name, "max_retries_exceeded")
            return

        logger.warning(f"Attempting recovery for {service_name} (attempt {attempts + 1})")

        try:
            # Get the service
            if self._registry:
                service = await self._registry.get(service_name)

                if service:
                    # Try to recover
                    success = await service.recover()

                    if success:
                        logger.info(f"✅ Recovery successful for {service_name}")
                        self._recovery_attempts[service_name] = 0
                    else:
                        logger.error(f"❌ Recovery failed for {service_name}")
                        self._recovery_attempts[service_name] = attempts + 1
                        await self._alert_humans(service_name, "recovery_failed")

        except Exception as e:
            logger.error(f"Error during recovery of {service_name}: {e}")
            self._recovery_attempts[service_name] = attempts + 1
            await self._alert_humans(service_name, f"recovery_error: {e}")
```

#### Fix 2: Implement Alerting (2 hours)

**File:** `2-engine/01-core/infrastructure/health.py`

**Changes:**
```python
class HealthMonitor:
    def __init__(self, service_registry=None):
        # ... existing ...
        self._alert_handlers = []

        # Register default alert handlers
        self._register_default_alerts()

    def _register_default_alerts(self):
        """Register default alert handlers"""

        # Log to file
        self.add_alert_handler(self._alert_log)

        # Send to event bus
        self.add_alert_handler(self._alert_event_bus)

    def add_alert_handler(self, handler: Callable):
        """Add a custom alert handler"""
        self._alert_handlers.append(handler)

    async def _alert_humans(self, service_name: str, reason: str):
        """Alert humans about unhealthy service"""

        alert = {
            'service': service_name,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'severity': 'critical' if reason == 'max_retries_exceeded' else 'warning'
        }

        # Call all alert handlers
        for handler in self._alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert)
                else:
                    handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")

    def _alert_log(self, alert):
        """Log alert to file"""
        logger.critical(f"HEALTH ALERT: {alert['service']} - {alert['reason']}")

    async def _alert_event_bus(self, alert):
        """Send alert to event bus"""
        try:
            from ..communication.event_bus import get_event_bus
            event_bus = get_event_bus()
            await event_bus.publish(
                "health.alert",
                alert
            )
        except Exception as e:
            logger.error(f"Could not publish alert to event bus: {e}")
```

#### Fix 3: Add Custom Alert Handlers (1 hour)

**File:** `2-engine/01-core/infrastructure/health.py`

**Example:**
```python
# Custom alert handler: Email
def send_email_alert(alert):
    """Send email alert"""
    if alert['severity'] == 'critical':
        send_email(
            to="oncall@example.com",
            subject=f"🚨 Health Alert: {alert['service']}",
            body=f"Service {alert['service']} is unhealthy: {alert['reason']}"
        )

# Custom alert handler: Slack
async def send_slack_alert(alert):
    """Send Slack alert"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json={
                'text': f"🚨 Health Alert: {alert['service']} - {alert['reason']}"
            })

# Register custom handlers
health_monitor = HealthMonitor()
health_monitor.add_alert_handler(send_email_alert)
health_monitor.add_alert_handler(send_slack_alert)
```

#### Test: (2 hours)

**File:** `2-engine/01-core/infrastructure/tests/test_health_monitor_recovery.py`

```python
async def test_automatic_recovery():
    """Test that unhealthy services are automatically recovered"""

    # Create a service that fails then recovers
    class FlakyService(Service):
        def __init__(self):
            super().__init__("flaky")
            self.fail_count = 0

        async def initialize(self):
            self._initialized = True

        async def start(self):
            self._started = True

        async def stop(self):
            self._started = False

        def is_healthy(self):
            # Fail first 2 checks, then recover
            self.fail_count += 1
            return self.fail_count > 2

    # Create health monitor
    monitor = HealthMonitor()

    # Register flaky service
    monitor.register_check(
        "flaky",
        flaky_service.is_healthy,
        interval=1,
        timeout=1
    )

    # Run health checks
    await monitor.check_all()

    # Verify: Service was unhealthy initially
    health = monitor.get_current_health()
    assert health['checks']['flaky']['consecutive_failures'] > 0

    # Wait for recovery
    await asyncio.sleep(3)
    await monitor.check_all()

    # Verify: Service recovered
    health = monitor.get_current_health()
    assert health['checks']['flaky']['healthy'] == True
```

### Success Criteria
✅ Unhealthy services automatically recovered
✅ Max 3 recovery attempts, then alert humans
✅ Alerts sent via multiple channels (log, event bus, email/slack)
✅ Recovery attempts tracked and logged

### Estimated Time: 1 day (8 hours)

---

## Gap 4: Orchestrator No Checkpoint/Resume 🟡 P1

### Problem
Long-running workflows can't resume after crash - have to restart from beginning

### Risk Level
🟡 **MEDIUM** - Wasted compute, humans give up

### Solution: Checkpointing + Resume Capability

#### Fix 1: Add Checkpointing (2 hours)

**File:** `2-engine/01-core/orchestration/Orchestrator.py`

**Changes:**
```python
class AgentOrchestrator:
    def __init__(self, ...):
        # ... existing ...
        self._checkpoint_dir = memory_base_path / "checkpoints" if memory_base_path else Path("checkpoints")
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)

    async def execute_workflow(self, workflow: Workflow) -> Workflow:
        logger.info(f"Starting workflow: {workflow.name}")

        # TRY TO RESUME FROM CHECKPOINT
        checkpoint = self._load_checkpoint(workflow.id)
        if checkpoint:
            completed_steps = set(checkpoint['completed_steps'])
            logger.info(f"Resuming from checkpoint: {len(completed_steps)} steps already completed")
            workflow.status = WorkflowStatus.RUNNING
        else:
            completed_steps = set()
            workflow.status = WorkflowStatus.RUNNING

        workflow.started_at = datetime.now().isoformat()

        try:
            # Execute steps
            while len(completed_steps) < len(workflow.steps):
                progress_made = False

                for step in workflow.steps:
                    if step.id in completed_steps:
                        continue

                    if not all(dep_id in completed_steps for dep_id in step.depends_on):
                        continue

                    # Execute step
                    try:
                        result = await self._execute_step(step)
                        step.status = WorkflowStatus.COMPLETED
                        step.result = result
                        step.completed_at = datetime.now().isoformat()
                        completed_steps.add(step.id)
                        progress_made = True

                        # SAVE CHECKPOINT
                        self._save_checkpoint(workflow.id, completed_steps)

                    except Exception as e:
                        # ... error handling ...

                if not progress_made:
                    raise RuntimeError("Workflow stuck")

        finally:
            # Clean up checkpoint on completion
            if workflow.status == WorkflowStatus.COMPLETED:
                self._delete_checkpoint(workflow.id)

        return workflow

    def _save_checkpoint(self, workflow_id: str, completed_steps: set):
        """Save workflow checkpoint"""
        checkpoint_path = self._checkpoint_dir / f"{workflow_id}.json"

        checkpoint_data = {
            'workflow_id': workflow_id,
            'completed_steps': list(completed_steps),
            'timestamp': datetime.now().isoformat()
        }

        checkpoint_path.write_text(json.dumps(checkpoint_data, indent=2))
        logger.debug(f"Saved checkpoint: {len(completed_steps)} steps completed")

    def _load_checkpoint(self, workflow_id: str) -> Optional[dict]:
        """Load workflow checkpoint if exists"""
        checkpoint_path = self._checkpoint_dir / f"{workflow_id}.json"

        if not checkpoint_path.exists():
            return None

        try:
            data = json.loads(checkpoint_path.read_text())
            logger.info(f"Loaded checkpoint: {len(data['completed_steps'])} steps completed")
            return data
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None

    def _delete_checkpoint(self, workflow_id: str):
        """Delete workflow checkpoint after completion"""
        checkpoint_path = self._checkpoint_dir / f"{workflow_id}.json"
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            logger.debug(f"Deleted checkpoint for {workflow_id}")
```

#### Fix 2: Add Deadlock Detection (2 hours)

**File:** `2-engine/01-core/orchestration/Orchestrator.py`

**Changes:**
```python
class AgentOrchestrator:
    async def execute_workflow(self, workflow: Workflow) -> Workflow:
        completed_steps = set()
        no_progress_count = 0
        max_no_progress = len(workflow.steps)  # Should make progress each iteration

        while len(completed_steps) < len(workflow.steps):
            previous_count = len(completed_steps)
            progress_made = False

            for step in workflow.steps:
                # ... execute step ...

            # Check for progress
            current_count = len(completed_steps)
            if current_count == previous_count:
                no_progress_count += 1
            else:
                no_progress_count = 0

            # Detect deadlock
            if no_progress_count > max_no_progress:
                # Build dependency graph for debugging
                deps = self._build_dependency_graph(workflow, completed_steps)

                raise RuntimeError(
                    f"Workflow deadlock detected. "
                    f"Completed: {len(completed_steps)}/{len(workflow.steps)}. "
                    f"Blocked steps: {deps['blocked']}. "
                    f"Circular dependencies: {deps['circular']}"
                )

    def _build_dependency_graph(self, workflow: Workflow, completed_steps: set) -> dict:
        """Build dependency graph to debug deadlocks"""

        # Find blocked steps (not completed, dependencies not met)
        blocked = []
        for step in workflow.steps:
            if step.id not in completed_steps:
                unmet_deps = [d for d in step.depends_on if d not in completed_steps]
                if unmet_deps:
                    blocked.append({
                        'step': step.id,
                        'waiting_for': unmet_deps
                    })

        # Check for circular dependencies
        graph = {}
        for step in workflow.steps:
            graph[step.id] = step.depends_on

        circular = self._detect_circular_dependencies(graph)

        return {
            'blocked': blocked,
            'circular': circular
        }

    def _detect_circular_dependencies(self, graph: dict) -> list:
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])

            rec_stack.remove(node)
            path.pop()

        for node in graph:
            if node not in visited:
                dfs(node, [])

        return cycles
```

#### Test: (2 hours)

**File:** `2-engine/01-core/orchestration/tests/test_orchestrator_checkpoint.py`

```python
async def test_checkpoint_resume():
    """Test that workflows can resume from checkpoint"""

    # Create workflow with 5 steps
    workflow = Workflow(name="Test Workflow")
    for i in range(5):
        workflow.steps.append(WorkflowStep(
            name=f"Step {i}",
            agent_name="test-agent",
            depends_on=[f"step-{i-1}"] if i > 0 else []
        ))

    orchestrator = AgentOrchestrator()

    # Start execution
    task = asyncio.create_task(orchestrator.execute_workflow(workflow))

    # Wait for step 2 to complete
    await asyncio.sleep(2)

    # Simulate crash: cancel task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    # Verify checkpoint exists
    checkpoint = orchestrator._load_checkpoint(workflow.id)
    assert checkpoint is not None
    assert len(checkpoint['completed_steps']) >= 1

    # Resume workflow
    workflow2 = orchestrator.execute_workflow(workflow)

    # Verify: Didn't redo completed steps
    assert workflow2.status == WorkflowStatus.COMPLETED

    # Clean up
    orchestrator._delete_checkpoint(workflow.id)

async def test_deadlock_detection():
    """Test that circular dependencies are detected"""

    # Create workflow with circular dependency
    workflow = Workflow(name="Circular Workflow")

    step1 = WorkflowStep(id="step-1", depends_on=["step-2"])
    step2 = WorkflowStep(id="step-2", depends_on=["step-1"])

    workflow.steps = [step1, step2]

    orchestrator = AgentOrchestrator()

    # Should detect deadlock
    with pytest.raises(RuntimeError, match="deadlock"):
        await orchestrator.execute_workflow(workflow)
```

### Success Criteria
✅ Workflow progress saved after each step
✅ Resuming from checkpoint skips completed steps
✅ Checkpoint deleted after workflow completion
✅ Circular dependencies detected and reported

### Estimated Time: 4 hours

---

## Gap 5: ModelRouter Cost Unvalidated 🟡 P2

### Problem
ModelRouter optimizes cost but has never been validated - don't know if it actually saves money

### Risk Level
🟡 **MEDIUM** - Wasted money or quality issues

### Solution: Cost Tracking + Quality Measurement + Feedback Loop

#### Fix 1: Add Cost Tracking (2 hours)

**File:** `2-engine/07-operations/environment/lib/python/core/runtime/model_router.py`

**Changes:**
```python
class ModelRouter:
    def __init__(self, config_path: Optional[Path] = None):
        # ... existing ...
        self._cost_history = []
        self._quality_history = []
        self._routing_decisions = []

    def route(self, task, context) -> ModelConfig:
        """Route task to appropriate model"""
        complexity = self._analyze_complexity(task, context)
        model_config = self._get_model_for_complexity(complexity)

        # Estimate cost
        estimated_input = self._estimate_tokens(task.get('description', ''))
        estimated_cost = self.estimate_cost(
            model_config,
            estimated_input,
            estimated_input * 2  # Assume output is 2x input
        )

        # Record routing decision
        decision = {
            'task_id': task.get('id', 'unknown'),
            'complexity': complexity.value,
            'model': model_config.model,
            'tier': self.models[model_config.model]['tier'],
            'estimated_cost': estimated_cost,
            'timestamp': datetime.now().isoformat()
        }

        self._routing_decisions.append(decision)

        return model_config, estimated_cost

    def record_result(self, task_id: str, model_config: ModelConfig,
                     input_tokens: int, output_tokens: int,
                     success: bool, quality_score: float):
        """Record actual cost and quality after task completion"""

        actual_cost = self.estimate_cost(model_config, input_tokens, output_tokens)

        # Find the routing decision
        decision = next((d for d in self._routing_decisions if d['task_id'] == task_id), None)

        if decision:
            # Update with actual results
            decision['actual_cost'] = actual_cost
            decision['input_tokens'] = input_tokens
            decision['output_tokens'] = output_tokens
            decision['total_tokens'] = input_tokens + output_tokens
            decision['success'] = success
            decision['quality_score'] = quality_score

            # Calculate cost difference
            decision['cost_diff'] = actual_cost - decision['estimated_cost']
            decision['cost_accuracy'] = abs(decision['cost_diff'] / actual_cost) if actual_cost > 0 else 0

        # Store in history
        self._cost_history.append(decision)

        # Trim history to last 1000 entries
        if len(self._cost_history) > 1000:
            self._cost_history = self._cost_history[-1000:]
```

#### Fix 2: Add Quality Measurement (2 hours)

**File:** `2-engine/07-operations/environment/lib/python/core/runtime/model_router.py`

**Changes:**
```python
class ModelRouter:
    def _measure_quality(self, result: Any, task: dict) -> float:
        """Measure quality of task result (0.0 to 1.0)"""

        quality_score = 0.0

        # Factor 1: Success (40%)
        if result.get('success', False):
            quality_score += 0.4

        # Factor 2: No errors (30%)
        if not result.get('error'):
            quality_score += 0.3

        # Factor 3: Output quality (30%)
        output = result.get('output', '')
        if output:
            # Check for meaningful output (not empty/error messages)
            if len(output) > 100:  # Substantial output
                quality_score += 0.15

            # Check for no error patterns
            error_patterns = ['error', 'failed', 'exception', 'cannot']
            if not any(p in output.lower() for p in error_patterns):
                quality_score += 0.15

        return min(quality_score, 1.0)

    def get_cost_statistics(self) -> dict:
        """Get cost and quality statistics"""

        if not self._cost_history:
            return {'message': 'No cost data available'}

        # Calculate statistics
        total_cost = sum(d.get('actual_cost', d.get('estimated_cost', 0)) for d in self._cost_history)
        total_tokens = sum(d.get('total_tokens', 0) for d in self._cost_history)

        # By tier
        by_tier = {}
        for decision in self._cost_history:
            tier = decision.get('tier', 'unknown')
            if tier not in by_tier:
                by_tier[tier] = {
                    'count': 0,
                    'cost': 0,
                    'tokens': 0,
                    'avg_quality': 0
                }

            by_tier[tier]['count'] += 1
            by_tier[tier]['cost'] += decision.get('actual_cost', 0)
            by_tier[tier]['tokens'] += decision.get('total_tokens', 0)

        # Calculate averages
        for tier, stats in by_tier.items():
            stats['avg_cost'] = stats['cost'] / stats['count']
            stats['avg_tokens'] = stats['tokens'] / stats['count']

            # Get quality scores for this tier
            qualities = [d.get('quality_score', 0) for d in self._cost_history if d.get('tier') == tier]
            stats['avg_quality'] = sum(qualities) / len(qualities) if qualities else 0

        return {
            'total_cost': total_cost,
            'total_tokens': total_tokens,
            'total_tasks': len(self._cost_history),
            'by_tier': by_tier,
            'cost_accuracy': sum(d.get('cost_accuracy', 0) for d in self._cost_history) / len(self._cost_history)
        }
```

#### Fix 3: Add Feedback Loop (2 hours)

**File:** `2-engine/07-operations/environment/lib/python/core/runtime/model_router.py`

**Changes:**
```python
class ModelRouter:
    def analyze_routing_effectiveness(self) -> dict:
        """Analyze if routing decisions were effective"""

        stats = self.get_cost_statistics()

        insights = []

        # Insight 1: Quality by tier
        by_tier = stats['by_tier']
        for tier, tier_stats in by_tier.items():
            if tier_stats['avg_quality'] < 0.7:
                insights.append({
                    'severity': 'warning',
                    'message': f"Tier '{tier}' has low quality ({tier_stats['avg_quality']:.2f}). Consider using higher tier."
                })
            elif tier_stats['avg_quality'] > 0.95:
                insights.append({
                    'severity': 'info',
                    'message': f"Tier '{tier}' has excellent quality ({tier_stats['avg_quality']:.2f}). Could use lower tier."
                })

        # Insight 2: Cost overruns
        cost_accuracy = stats.get('cost_accuracy', 0)
        if cost_accuracy > 0.3:
            insights.append({
                'severity': 'warning',
                'message': f"Cost estimates are off by {cost_accuracy*100:.1f}%. Calibrate token estimation."
            })

        # Insight 3: Routing distribution
        tier_counts = {tier: s['count'] for tier, s in by_tier.items()}
        if tier_counts.get('hq', 0) > tier_counts.get('fast', 0) * 2:
            insights.append({
                'severity': 'info',
                'message': f"Overusing HQ model. {tier_counts['hq']} HQ vs {tier_counts.get('fast', 0)} fast tasks."
            })

        return {
            'statistics': stats,
            'insights': insights,
            'recommendations': self._generate_recommendations(stats)
        }

    def _generate_recommendations(self, stats: dict) -> list:
        """Generate actionable recommendations"""

        recommendations = []

        # Recommendation 1: If fast tier quality is high, use it more
        by_tier = stats.get('by_tier', {})
        if 'fast' in by_tier and by_tier['fast']['avg_quality'] > 0.8:
            fast_count = by_tier['fast']['count']
            total_count = stats['total_tasks']
            if fast_count / total_count < 0.3:
                recommendations.append(
                    "Fast tier quality is good (>%s). Consider routing more simple tasks to fast tier to reduce costs." %
                    by_tier['fast']['avg_quality']
                )

        # Recommendation 2: If HQ tier is overused
        if 'hq' in by_tier:
            hq_count = by_tier['hq']['count']
            total_count = stats['total_tasks']
            if hq_count / total_count > 0.5:
                recommendations.append(
                    f"HQ model used for {hq_count/total_count*100:.1f}% of tasks. "
                    "Review if all require highest quality."
                )

        return recommendations
```

#### Test: (2 hours)

**File:** `2-engine/07-operations/environment/lib/python/core/runtime/tests/test_model_router_validation.py`

```python
async def test_cost_tracking():
    """Test that costs are tracked accurately"""

    router = ModelRouter()

    # Route a task
    task = {
        'id': 'test-1',
        'type': 'validation',
        'description': 'Check if code is valid'
    }

    model_config, estimated_cost = router.route(task, {})

    # Record result
    router.record_result(
        task_id='test-1',
        model_config=model_config,
        input_tokens=100,
        output_tokens=50,
        success=True,
        quality_score=0.9
    )

    # Verify tracking
    stats = router.get_cost_statistics()

    assert stats['total_tasks'] == 1
    assert stats['total_tokens'] == 150
    assert stats['total_cost'] > 0

async def test_routing_analysis():
    """Test that routing effectiveness is analyzed"""

    router = ModelRouter()

    # Simulate various routing decisions
    for i in range(100):
        task = {'id': f'task-{i}', 'type': 'validation'}
        model_config, _ = router.route(task, {})

        # Simulate results
        router.record_result(
            task_id=f'task-{i}',
            model_config=model_config,
            input_tokens=100,
            output_tokens=50,
            success=True,
            quality_score=random.uniform(0.6, 0.95)
        )

    # Analyze effectiveness
    analysis = router.analyze_routing_effectiveness()

    # Verify insights generated
    assert 'statistics' in analysis
    assert 'insights' in analysis
    assert 'recommendations' in analysis

    print(json.dumps(analysis, indent=2))
```

### Success Criteria
✅ Actual costs tracked for all routed tasks
✅ Quality scores measured for all results
✅ Statistics available by model tier
✅ Insights and recommendations generated

### Estimated Time: 1 day (8 hours)

---

## Implementation Plan

### Phase 1: Quick Wins (Day 1)

**Morning (4 hours):**
- ✅ Fix StateManager race conditions (Gap 2)
  - Add file locking (2h)
  - Add backups + validation (2h)

**Afternoon (4 hours):**
- ✅ Add Orchestrator checkpointing (Gap 4)
  - Implement checkpoint/save/resume (2h)
  - Add deadlock detection (2h)

**End of Day 1:**
- StateManager safe from concurrent writes
- Workflows can resume after crash

---

### Phase 2: Critical Safety (Day 2)

**Full day (8 hours):**
- ✅ Test and harden KillSwitch (Gap 1)
  - Add delivery confirmation (2h)
  - Add compliance verification (2h)
  - Add recovery testing (2h)
  - Add backup trigger (2h)
  - Integration testing (2h)

**End of Day 2:**
- KillSwitch verified to work in emergencies
- Confidence that system can be stopped

---

### Phase 3: Autonomous Recovery (Day 3)

**Morning (4 hours):**
- ✅ Implement HealthMonitor self-healing (Gap 3)
  - Add automatic recovery (3h)
  - Add alerting (1h)

**Afternoon (4 hours):**
- ✅ Add ModelRouter validation (Gap 5)
  - Add cost tracking (2h)
  - Add quality measurement (2h)

**End of Day 3:**
- System heals itself automatically
- Costs are tracked and validated

---

### Phase 4: Polish and Testing (Day 4-5)

**Day 4:**
- ✅ Write comprehensive tests for all fixes
- ✅ Run integration tests
- ✅ Document new features

**Day 5:**
- ✅ Fix any bugs found in testing
- ✅ Add monitoring dashboards
- ✅ Update documentation

---

## Testing Strategy

### Unit Tests
Each fix has unit tests covering:
- Normal operation
- Error cases
- Edge cases
- Concurrent access (where relevant)

### Integration Tests
Test interactions between components:
- KillSwitch + Event Bus + Agents
- StateManager + multiple processes
- HealthMonitor + ServiceRegistry
- Orchestrator + Checkpointing

### Scenario Tests
Real-world scenarios:
- **Emergency Scenario:** Agent goes rogue, kill switch triggered
- **Crash Recovery:** Workflow crashes at step 47/100, resumes
- **Concurrent Access:** 10 processes updating STATE.md
- **Health Degradation:** Service memory leak, auto-recovery

### Load Tests
Stress tests:
- 1000 workflow steps with checkpointing
- 100 concurrent STATE.md updates
- Kill switch with 50 agents

---

## Rollback Plan

Each fix is designed to be non-breaking:

### Gap 1: KillSwitch
- Changes additive (new features)
- Old behavior preserved if new features fail
- Can disable via config

### Gap 2: StateManager
- File locking is best-effort (logs warning if fails)
- Backups created before writes
- Can fall back to non-locked mode

### Gap 3: HealthMonitor
- Self-healing opt-in (auto_recover flag)
- Alert handlers optional
- No changes if not enabled

### Gap 4: Orchestrator
- Checkpointing transparent if enabled
- No checkpoint = normal behavior
- Deadlock detection is read-only

### Gap 5: ModelRouter
- Tracking is transparent
- No routing logic changed
- Can disable tracking

---

## Success Metrics

### Quantitative
- ✅ Kill switch stops 100% of agents in <5 seconds
- ✅ StateManager handles 10 concurrent writers without corruption
- ✅ HealthMonitor recovers 90%+ of unhealthy services
- ✅ Workflows resume from checkpoint in <1 second
- ✅ ModelRouter cost estimates within 20% of actual

### Qualitative
- ✅ Confidence that emergency stop works
- ✅ No lost work from concurrent access
- ✅ System heals without human intervention
- ✅ Long workflows complete reliably
- ✅ Cost optimization is real, not theoretical

---

## Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|-----------|
| File locking not portable | Use platform-specific locking (fcntl for Unix, msvcrt for Windows) |
| Checkpoint overhead | Minimal (one file write per step) |
| False health alerts | Consecutive failure threshold (3 strikes) |
| Kill switch not tested | Comprehensive testing before deploy |
| Cost tracking overhead | Async writes, batch updates |

### Operational Risks
| Risk | Mitigation |
|------|-----------|
| Breaking changes | Feature flags, backward compatible |
| Deployment issues | Staged rollout, monitor closely |
| Performance impact | Benchmark before/after |

---

## Next Steps

1. **Review this plan** with team
2. **Prioritize phases** based on risk tolerance
3. **Set up feature flags** for safe rollout
4. **Begin implementation** with Phase 1
5. **Test thoroughly** before production deploy

**After completion:**
- All 5 critical gaps resolved
- System safe for autonomous operation
- Confidence in emergency handling
- Ready for analysis loops

---

**Status:** 🟡 READY FOR EXECUTION
**Estimated Completion:** 3-5 days
**Confidence Level:** HIGH (all fixes are well-understood patterns)
