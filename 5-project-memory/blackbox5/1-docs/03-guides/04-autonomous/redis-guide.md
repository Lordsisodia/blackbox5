# Redis Guide: Autonomous Agent Coordination

> **Complete guide to using Redis for event-driven multi-agent systems**

## What is Redis?

**Redis** = **RE**mote **DI**ctionary **S**erver

Think of it as a super-fast shared notepad that all your agents can read and write to at the same time.

**Key characteristics:**
- **In-memory**: Data stored in RAM (not disk)
- **Fast**: Sub-millisecond operations
- **Shared**: All agents see the same data
- **Persistent**: Can save to disk (optional)
- **Multi-paradigm**: Not just a key-value store

---

## Why Redis for Autonomous Agents?

### The Problem: Coordination

**Without Redis** (polling approach):
```python
# Agent A
while True:
    check_for_tasks()  # Am I needed?
    sleep(10)          # Wait 10 seconds

# Agent B
while True:
    check_for_tasks()  # Am I needed?
    sleep(10)          # Wait 10 seconds

# Agent C
while True:
    check_for_tasks()  # Am I needed?
    sleep(10)          # Wait 10 seconds
```

**Problems:**
- ❌ 10 second delay before any agent reacts
- ❌ Wastes CPU (checking when nothing there)
- ❌ 100 agents = 1000 useless operations every 10 seconds

**With Redis** (event-driven):
```python
# Agent A
redis.subscribe("tasks:new", lambda task: handle(task))
# Do nothing until notification received

# Agent B
redis.subscribe("tasks:new", lambda task: handle(task))
# Do nothing until notification received

# Agent C
redis.subscribe("tasks:new", lambda task: handle(task))
# Do nothing until notification received
```

**Benefits:**
- ✅ 1 millisecond delay (10,000x faster)
- ✅ Zero waste (only act when needed)
- ✅ Scales infinitely (one notification, all agents see it)

---

## Redis Data Structures for Agents

### 1. Strings (Simple Values)

```python
# Set a value
redis.set("agent:status:agent-1", "working")

# Get a value
status = redis.get("agent:status:agent-1")
# → "working"

# With expiration (TTL)
redis.setex("agent:status:agent-1", 3600, "working")
# Expires after 1 hour
```

**Use cases:**
- Agent status tracking
- Simple configuration values
- Locks with expiration

### 2. Hashes (Objects)

```python
# Store task details
redis.hset("task:123", {
    "title": "Write authentication code",
    "status": "in_progress",
    "agent": "agent-1",
    "created_at": "2026-01-28T10:00:00Z"
})

# Get specific field
title = redis.hget("task:123", "title")
# → "Write authentication code"

# Get all fields
task = redis.hgetall("task:123")
# → {"title": "...", "status": "...", ...}

# Update specific field
redis.hset("task:123", "status", "complete")
```

**Use cases:**
- Task objects (multiple fields)
- Agent profiles
- Project configuration

### 3. Lists (Queues)

```python
# Add to end of list (push)
redis.rpush("tasks:pending", {
    "task_id": "task-123",
    "type": "development",
    "priority": "high"
})

# Remove from front (pop)
task = redis.lpop("tasks:pending")
# → First task in queue

# Block until available (pop with timeout)
task = redis.blpop("tasks:pending", timeout=10)
# → Waits up to 10 seconds for a task
```

**Use cases:**
- Task queues
- Work queues
- FIFO processing

### 4. Sets (Unique Collections)

```python
# Add to set
redis.sadd("agents:available", "agent-1", "agent-2", "agent-3")

# Check if member exists
is_available = redis.sismember("agents:available", "agent-1")
# → True

# Get all members
available_agents = redis.smembers("agents:available")
# → {"agent-1", "agent-2", "agent-3"}

# Remove from set
redis.srem("agents:available", "agent-1")
```

**Use cases:**
- Available agents
- Active projects
- Completed tasks

### 5. Sorted Sets (Priority Queues)

```python
# Add with score (priority)
redis.zadd("tasks:priority", {
    "task-123": 1,      # Priority 1 (high)
    "task-124": 5,      # Priority 5 (medium)
    "task-125": 10      # Priority 10 (low)
})

# Get by score range (highest priority first)
high_priority_tasks = redis.zrangebyscore(
    "tasks:priority",
    0, 3,  # Scores 0-3
    start=0,
    num=10  # Top 10
)
# → ["task-123"]

# Remove and return highest priority
task = redis.zpopmin("tasks:priority")
# → "task-123" (with score 1)
```

**Use cases:**
- Priority task queues
- Leaderboards
- Time-based scheduling

### 6. Pub/Sub (Publish/Subscribe)

**The most important feature for autonomous agents!**

```python
# Publisher (Supervisor Agent)
redis.publish("tasks:new", json.dumps({
    "task_id": "task-123",
    "type": "development",
    "priority": "high"
}))
# All subscribers receive this message instantly

# Subscriber (Autonomous Agent)
pubsub = redis.pubsub()
pubsub.subscribe("tasks:new")

for message in pubsub.listen():
    task = json.loads(message["data"])
    handle_task(task)
    # Reacts instantly when published
```

**Use cases:**
- **Task notifications**: New task available
- **State changes**: Task completed, failed, blocked
- **Agent coordination**: Agent-to-agent communication
- **System events**: Errors, alerts, status updates

### 7. Streams (Event Logs)

```python
# Add event to stream
redis.xadd("events:task-123", {
    "timestamp": "2026-01-28T10:00:00Z",
    "event": "task_assigned",
    "agent": "agent-1",
    "data": json.dumps({...})
})

# Read events from stream
events = redis.xread({
    "events:task-123": "0"  # Read from beginning
}, count=10)

# Replay from specific timestamp
events = redis.xread({
    "events:task-123": "1706462400000-0"  # Specific ID
}, count=10)
```

**Use cases:**
- **Event sourcing**: Complete history of all changes
- **Debugging**: Replay execution history
- **Audit trails**: Who did what when
- **Recovery**: Rebuild state from events

---

## Autonomous Agent Patterns with Redis

### Pattern 1: Task Distribution (Pub/Sub + Sorted Set)

**Scenario**: Supervisor creates tasks, agents claim them

```python
# Supervisor Agent
def create_task(task_data):
    # 1. Store task details
    task_id = f"task-{uuid.uuid4()}"
    redis.hset(f"task:{task_id}", task_data)

    # 2. Add to priority queue
    redis.zadd("tasks:pending", {
        task_id: task_data["priority"]  # Score = priority
    })

    # 3. Notify all agents
    redis.publish("tasks:new", json.dumps({
        "task_id": task_id,
        "type": task_data["type"],
        "priority": task_data["priority"]
    }))

# Autonomous Agent
def autonomous_loop():
    pubsub = redis.pubsub()
    pubsub.subscribe("tasks:new")

    for message in pubsub.listen():
        task_notification = json.loads(message["data"])

        # Can I handle this task?
        if can_i_handle(task_notification):
            # Try to claim it
            task_id = task_notification["task_id"]

            # Remove from pending queue (atomic)
            claimed = redis.zrem("tasks:pending", task_id)

            if claimed:
                # We got it!
                redis.hset(f"task:{task_id}", {
                    "status": "claimed",
                    "agent": "my-id",
                    "claimed_at": datetime.now().isoformat()
                })

                # Do the work
                result = execute_task(task_id)

                # Publish completion
                redis.publish("tasks:complete", json.dumps({
                    "task_id": task_id,
                    "result": result
                }))
```

**Why this works:**
- ✅ Atomic claim (zrem) prevents conflicts
- ✅ Priority queue ensures important tasks done first
- ✅ Pub/sub enables instant notification
- ✅ No polling, no wasted resources

### Pattern 2: State Synchronization (Pub/Sub + Hash)

**Scenario**: Track agent status across all agents

```python
# Agent updates its status
def update_status(status):
    redis.hset(f"agent:{AGENT_ID}", {
        "status": status,
        "updated_at": datetime.now().isoformat()
    })

    # Notify others
    redis.publish("agents:status", json.dumps({
        "agent_id": AGENT_ID,
        "status": status
    }))

# Other agents monitor
pubsub = redis.pubsub()
pubsub.subscribe("agents:status")

for message in pubsub.listen():
    status_update = json.loads(message["data"])
    print(f"Agent {status_update['agent_id']} is {status_update['status']}")

    # Update local cache
    local_cache[status_update['agent_id']] = status_update['status']
```

**Why this works:**
- ✅ All agents see all status changes instantly
- ✅ No need to query each agent individually
- ✅ Real-time coordination

### Pattern 3: Event Sourcing (Streams + Pub/Sub)

**Scenario**: Complete history of all task events for replay/debugging

```python
# Task event logger
def log_event(task_id, event_type, data):
    # Add to stream
    redis.xadd(f"events:task:{task_id}", {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": json.dumps(data)
    })

    # Also notify for real-time reactions
    redis.publish(f"events:task:{task_id}", json.dumps({
        "event_type": event_type,
        "data": data
    }))

# Usage
log_event("task-123", "created", {...})
log_event("task-123", "assigned", {"agent": "agent-1"})
log_event("task-123", "started", {"at": "..."})
log_event("task-123", "completed", {"result": "..."})

# Replay events for debugging
def replay_task(task_id):
    events = redis.xrevrange(f"events:task:{task_id}", "+", "-")
    for event in events:
        print(f"[{event[1]['timestamp']}] {event[1]['event_type']}")
        # → [2026-01-28T10:00:00Z] created
        # → [2026-01-28T10:01:00Z] assigned
        # → [2026-01-28T10:05:00Z] started
        # → [2026-01-28T10:10:00Z] completed
```

**Why this works:**
- ✅ Complete audit trail
- ✅ Replayable debugging
- ✅ State can be rebuilt from events

---

## Production Configuration

### Redis Setup

**Installation (macOS):**
```bash
brew install redis
brew services start redis
```

**Installation (Ubuntu):**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**Configuration (redis.conf):**
```conf
# Memory limits
maxmemory 2gb
maxmemory-policy allkeys-lru  # Evict old keys when full

# Persistence (optional)
save 900 1      # Save after 900s if 1+ changes
save 300 10     # Save after 300s if 10+ changes
save 60 10000    # Save after 60s if 10000+ changes

# Expiration on keys
# Use TTL for auto-cleanup
```

### Connection Pooling

```python
import redis
from redis.connection import ConnectionPool

# Connection pool (better performance)
pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50,  # Pool size
    decode_responses=True  # Return strings, not bytes
)

redis_client = redis.Redis(connection_pool=pool)
```

### Best Practices

1. **Use TTL for temporary data**
   ```python
   # Auto-expire after 1 hour
   redis.setex("temp:task-123", 3600, data)
   ```

2. **Use pipelines for batch operations**
   ```python
   pipe = redis.pipeline()
   for i in range(100):
       pipe.set(f"key:{i}", f"value:{i}")
   pipe.execute()  # Send all at once
   ```

3. **Use transactions for atomic operations**
   ```python
   # Both succeed or both fail
   with redis.pipeline() as pipe:
       pipe.multi()
       pipe.set("key1", "value1")
       pipe.set("key2", "value2")
       pipe.execute()
   ```

4. **Handle connection failures**
   ```python
   from redis.exceptions import ConnectionError
   import time

   def safe_redis_operation(operation):
       max_retries = 3
       for attempt in range(max_retries):
           try:
               return operation()
           except ConnectionError:
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)
               else:
                   raise
   ```

---

## Complete Example: Multi-Agent Task System

```python
import redis
import json
from datetime import datetime
import uuid

# Initialize Redis
redis_client = redis.Redis(decode_responses=True)

# ============ SUPERVISOR AGENT ============
class SupervisorAgent:
    def create_tasks(self, goal: str):
        """Break goal into tasks"""
        tasks = self.breakdown_goal(goal)

        for task in tasks:
            task_id = f"task-{uuid.uuid4()}"

            # 1. Store task details
            redis_client.hset(f"task:{task_id}", {
                "id": task_id,
                "title": task["title"],
                "description": task["description"],
                "type": task["type"],
                "priority": task["priority"],
                "status": "pending",
                "created_at": datetime.now().isoformat()
            })

            # 2. Add to priority queue
            redis_client.zadd("tasks:pending", {
                task_id: task["priority"]
            })

            # 3. Notify all agents
            redis_client.publish("tasks:new", json.dumps({
                "task_id": task_id,
                "type": task["type"]
            }))

# ============ AUTONOMOUS AGENT ============
class AutonomousAgent:
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities

    def start(self):
        """Main autonomous loop"""
        pubsub = redis_client.pubsub()
        pubsub.subscribe("tasks:new")

        print(f"Agent {self.agent_id} started, waiting for tasks...")

        for message in pubsub.listen():
            task_notification = json.loads(message["data"])
            self.consider_task(task_notification)

    def consider_task(self, task_notification):
        """Check if we should handle this task"""
        task_id = task_notification["task_id"]

        # Get full task details
        task = redis_client.hgetall(f"task:{task_id}")

        # Can I handle this type?
        if task["type"] not in self.capabilities:
            return  # Not for me

        # Try to claim it
        claimed = redis_client.zrem("tasks:pending", task_id)

        if not claimed:
            return  # Someone else got it

        # We got it!
        print(f"Agent {self.agent_id} claimed task {task_id}")

        # Update status
        redis_client.hset(f"task:{task_id}", {
            "status": "claimed",
            "agent": self.agent_id,
            "claimed_at": datetime.now().isoformat()
        })

        # Execute task
        try:
            result = self.execute_task(task)

            # Mark complete
            redis_client.hset(f"task:{task_id}", {
                "status": "complete",
                "result": json.dumps(result),
                "completed_at": datetime.now().isoformat()
            })

            # Notify completion
            redis_client.publish("tasks:complete", json.dumps({
                "task_id": task_id,
                "agent": self.agent_id,
                "result": result
            }))

        except Exception as e:
            # Mark failed
            redis_client.hset(f"task:{task_id}", {
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.now().isoformat()
            })

            # Notify failure
            redis_client.publish("tasks:failed", json.dumps({
                "task_id": task_id,
                "agent": self.agent_id,
                "error": str(e)
            }))

    def execute_task(self, task):
        """Override in subclass"""
        # Implement actual work here
        print(f"Executing: {task['title']}")
        return {"success": True}

# ============ USAGE ============
if __name__ == "__main__":
    # Start supervisor
    supervisor = SupervisorAgent()
    supervisor.create_tasks("Build user authentication system")

    # Start autonomous agents
    agent_1 = AutonomousAgent(
        agent_id="agent-1",
        capabilities=["development", "testing"]
    )
    agent_1.start()

    agent_2 = AutonomousAgent(
        agent_id="agent-2",
        capabilities=["documentation", "analysis"]
    )
    agent_2.start()
```

---

## Performance Benchmarks

Based on production research:

| Operation | Latency | Throughput |
|-----------|---------|------------|
| **SET** | 0.1ms | 100,000 ops/sec |
| **GET** | 0.1ms | 100,000 ops/sec |
| **PUBLISH** | 0.1ms | 100,000 ops/sec |
| **SUBSCRIBE receive** | <1ms | Real-time |
| **LPUSH/RPOP** | 0.2ms | 80,000 ops/sec |
| **ZADD/ZPOP** | 0.3ms | 50,000 ops/sec |
| **XADD** | 0.5ms | 20,000 ops/sec |

**Key insight**: Redis is fast enough that it's rarely the bottleneck.

---

## Common Patterns

### 1. Leader Election

```python
# Agents elect a leader
def elect_leader(agent_id):
    # Try to become leader
    leader = redis_client.set("leader", agent_id, nx=True, ex=10)

    if leader:
        print(f"I am the leader!")
        # Do leader things
    else:
        print(f"Following {redis_client.get('leader')}")
        # Follow the leader
```

### 2. Distributed Lock

```python
from redis.lock import Lock

lock = Lock(redis_client, "lock:task-123", timeout=30)

if lock.acquire(blocking=False):
    try:
        # Do work with lock
        execute_task()
    finally:
        lock.release()
else:
    # Someone else has the lock
    pass
```

### 3. Rate Limiting

```python
def check_rate_limit(agent_id, max_calls=100, window=60):
    key = f"rate:{agent_id}"

    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, window)

    if current > max_calls:
        raise RateLimitError("Too many calls")
```

---

## Monitoring

### Key Metrics to Track

```python
# Task queue depth
queue_depth = redis_client.zcard("tasks:pending")

# Agent status
for agent_id in redis_client.smembers("agents:active"):
    status = redis_client.hget(f"agent:{agent_id}", "status")
    print(f"{agent_id}: {status}")

# Task completion rate
completed = redis_client.get("stats:completed")
total = redis_client.get("stats:total")
completion_rate = int(completed) / int(total) if total else 0
```

---

## Summary

**Redis for autonomous agents means:**
- ⚡ **Instant coordination** (1ms latency)
- 🔄 **Event-driven** (react, don't poll)
- 📊 **Multiple data structures** (queues, pub/sub, streams)
- 🚀 **Scales infinitely** (horizontal scaling)
- 💾 **Optional persistence** (survives restarts)

**It's the backbone that makes autonomous agent systems possible.**

---

## Sources

- [Redis Official Documentation](https://redis.io/docs/)
- [Redis Pub/Sub Tutorial](https://redis.io/docs/manual/pubsub/)
- [AI Agent Orchestration for Production Systems](https://redis.io/blog/ai-agent-orchestration/)
- [Agentic Reasoning in AI](https://redis.io/blog/agentic-reasoning/)
- [Production Redis Patterns](https://redis.io/commands/)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-28
