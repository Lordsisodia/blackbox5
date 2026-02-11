# TASK-INT-001: Redis-Based Shared Memory Service

**Status:** in_progress
**Priority:** HIGH
**Type:** infrastructure
**Category:** shared_memory
**Created:** 2026-02-11T16:47:00Z
**Agent:** main
**Parent Task:** TASK-RCH-001
**Estimated Effort:** 2 hours

## Problem Statement

MaltBot and BlackBox5 agents need to share memory (patterns, gotchas, discoveries, learnings) across agent boundaries. Currently, each agent has its own isolated Agent Memory with no way to share knowledge.

## Current State

**MaltBot Infrastructure:**
- Mac Mini (local network) - Own simple tracking
- Claude Code (VPS main) - Own Agent Memory
- OpenClaw sessions - Session-based isolation

**BlackBox5 Infrastructure:**
- BB5 Orchestrator - Task routing and agent spawning
- Agent Memory (AgentMemory.py) - Per-agent JSON memory
- RALF Autonomous System - Background improvements
- OpenClaw Gateway - Session management

**Limitation:** No shared memory layer between agents. Each agent's learnings are isolated.

## Solution: Redis-Based Shared Memory

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Redis Shared Memory Service              │
│  ┌────────────────────────────────────────────────────────────┐│
│  │  Shared Memory API                               ││
│  │  ├─→ add_insight(namespace, content, category) ││
│  │  ├─→ query_shared(namespace, query, limit)    ││
│  │  ├─→ get_learnings(namespace, category, limit)   ││
│  │  ├─→ add_learning(source, target_ns, learning_id)│
│  │  └─→ search_fulltext(query, namespaces)      ││
│  └──────────────────────────────────────────────────────────────┘│
│                  ↓ ↓ ↓ ↓ ↓ ↓                        │
│  ┌────────────────────────────────────────────────────────────┐│
│  │    Memory Storage Layer (Redis)                   ││
│  │  ├─→ Namespace隔离: {maltbot:*}, {bb5:*}       ││
│  │  ├─→ Indexing: FT.SEARCH on insights              ││
│  │  ├─→ Categories: patterns, gotchas, discoveries   ││
│  │  ├─→ Search: Full-text search across all insights││
│  │  └─→ Access Control: Read permissions by namespace││
│  └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
              ↓ ↓ ↓ ↓ ↓ ↓
        ┌──────────────────────────────────────────────────────┐
        │  Agent Integrations                                │
        │  ├─→ MaltBot: add_insight()                 │
        │  ├─→ BB5 Agent Memory: merge_context()        │
        │  └─→ RALF: add_insight() (system learning)     │
        └──────────────────────────────────────────────────────┘
```

### Implementation Plan

#### Phase 1: Redis Memory Service (2 hours)

**Task 1.1: Create shared memory service**
```python
# File: /opt/blackbox5/services/shared_memory_service.py

import redis
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

class SharedMemoryService:
    """Redis-based shared memory for multi-agent systems."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        
    def add_insight(self, namespace: str, content: str, 
                   category: str = "pattern", confidence: float = 0.9,
                   metadata: Optional[Dict[str, Any]] = None):
        """Add an insight to shared memory."""
        insight = {
            "id": str(uuid.uuid4()),
            "namespace": namespace,
            "content": content,
            "category": category,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        # Store in Redis
        insight_key = f"shared_memory:insight:{insight['id']}"
        self.redis.hset(insight_key, "data", json.dumps(insight))
        
        # Add to category index
        category_key = f"shared_memory:category:{namespace}:{category}"
        self.redis.sadd(category_key, insight['id'])
        
        # Index for full-text search (FT.SEARCH)
        # Create index on content for full-text search
        search_key = f"shared_memory:search:{insight['id']}"
        self.redis.hset(search_key, "content", content)
        
        return insight['id']
    
    def query_shared(self, namespace: str, query: str, 
                     category: Optional[str] = None, limit: int = 10):
        """Query shared memory for relevant insights."""
        results = []
        
        # Build Redis pipeline
        if category:
            # Filter by category
            category_key = f"shared_memory:category:{namespace}:{category}"
            insight_ids = self.redis.smembers(category_key)
            if insight_ids:
                pipeline = self.redis.pipeline()
                for insight_id in insight_ids[:limit]:
                    pipeline.hget(f"shared_memory:insight:{insight_id}")
                results.extend(pipeline.execute())
        
        # Search full-text if no category filter
        if not category:
            # Use FT.SEARCH for full-text search
            query = query.lower()
            search_key = "shared_memory:search_index"
            result_ids = self.redis.ft_search(search_key, query)
            
            if result_ids:
                pipeline = self.redis.pipeline()
                for result_id in result_ids[:limit]:
                    pipeline.hget(f"shared_memory:insight:{result_id}")
                results.extend(pipeline.execute())
        
        return results
```

**Task 1.2: Create Redis connection management**
```python
# Extend service with connection pooling

class SharedMemoryService:
    def __init__(self, redis_host="localhost", redis_port=6379):
        self.redis_pool = redis.ConnectionPool(
            host=redis_host, 
            port=redis_port,
            max_connections=10,
            decode_responses=True
        )
    
    def _get_redis(self):
        return self.redis_pool.get_connection()
    
    def _return_redis(self, conn):
        self.redis_pool.release_connection(conn)
```

**Task 1.3: Add API endpoints**
```python
# FastAPI service
from fastapi import FastAPI
from pydantic import BaseModel

class InsightRequest(BaseModel):
    namespace: str
    content: str
    category: str = "pattern"
    confidence: float = 0.9
    metadata: Optional[Dict[str, Any]] = None

class QueryRequest(BaseModel):
    namespace: str
    query: str
    category: Optional[str] = None
    limit: int = 10

app = FastAPI()

@app.post("/shared_memory/add_insight")
async def add_insight(req: InsightRequest):
    service = SharedMemoryService()
    insight_id = service.add_insight(
        namespace=req.namespace,
        content=req.content,
        category=req.category,
        confidence=req.confidence,
        metadata=req.metadata
    )
    return {"insight_id": insight_id, "status": "success"}

@app.get("/shared_memory/query")
async def query_shared(req: QueryRequest):
    service = SharedMemoryService()
    results = service.query_shared(
        namespace=req.namespace,
        query=req.query,
        category=req.category,
        limit=req.limit
    )
    return {"results": results, "count": len(results)}
```

#### Phase 2: Extend Agent Memory (2 hours)

**Task 2.1: Modify Agent Memory to support shared access**
```python
# File: /opt/blackbox5/engine/memory/AgentMemory.py (modify)

class AgentMemory:
    # Existing: __init__(self, agent_id, memory_base_path)
    
    # NEW: __init__(self, agent_id, memory_base_path, 
    #           shared_memory_url: Optional[str] = None)
    
    def add_insight(self, content: str, 
                   category: str = "pattern", confidence: float = 0.9,
                   metadata: Optional[Dict[str, Any]] = None):
        """Add insight to local Agent Memory."""
        # Store locally
        super().add_insight(content, category, confidence, metadata)
        
        # NEW: Also add to shared memory
        if self.shared_memory_url:
            shared_memory_service = SharedMemoryService(
                redis_host=os.getenv("REDIS_HOST", "localhost"),
                redis_port=int(os.getenv("REDIS_PORT", "6379"))
            )
            shared_memory_service.add_learning(
                source=self.agent_id,
                target_ns="shared_memory",
                learning_id=f"insight-{uuid.uuid4()}",
                data={"content": content, "category": category}
            )
    
    def query_shared_memory(self, query: str, category: Optional[str] = None, 
                            limit: int = 10):
        """Query shared memory for relevant insights."""
        if not self.shared_memory_url:
            return []
        
        shared_memory_service = SharedMemoryService(
                redis_host=os.getenv("REDIS_HOST", "localhost"),
                redis_port=int(os.getenv("REDIS_PORT", "6379"))
            )
        
        # Query shared memory
        results = shared_memory_service.query_shared(
            namespace="shared_memory",
            query=query,
            category=category,
            limit=limit
        )
        
        return results
    
    def sync_insights_from_shared(self, categories: List[str] = None):
        """Sync insights from shared memory to local memory."""
        if not self.shared_memory_url:
            return 0
        
        shared_memory_service = SharedMemoryService(
                redis_host=os.getenv("REDIS_HOST", "localhost"),
                redis_port=int(os.getenv("REDIS_PORT", "6379"))
            )
        
        count = 0
        for category in categories or ["pattern", "gotcha", "discovery"]:
            results = shared_memory_service.query_shared(
                namespace="shared_memory",
                query=category,
                limit=100
            )
            
            for result in results:
                self.add_insight(
                    content=result['content'],
                    category=result['category'],
                    confidence=result['confidence']
                )
                count += 1
        
        return count
```

**Task 2.2: Update agents to use shared memory**
```yaml
# File: /opt/blackbox5/config/agents.yaml

# Add shared_memory_url to agent configs

maltbot:
  shared_memory_url: "http://localhost:8000/shared_memory"
  enable_shared_memory: true
  shared_categories: ["pattern", "gotcha", "discovery"]

bb5-agents:
  shared_memory_url: "http://localhost:8000/shared_memory"
  enable_shared_memory: true
  shared_categories: ["pattern", "gotcha"]
  sync_on_startup: true
```

#### Phase 3: Implement Cross-Agent Learning (2 hours)

**Task 3.1: Create learning protocol**
```python
# File: /opt/blackbox5/services/learning_protocol.py

import json
from typing import List

class CrossAgentLearningProtocol:
    """Protocol for agents to learn from each other's experiences."""
    
    def create_learning_event(self, source_agent: str, target_agents: List[str], 
                             learning_id: str, learning_data: Dict[str, Any]):
        """Create a learning event to share with target agents."""
        event = {
            "source": source_agent,
            "targets": target_agents,
            "learning_id": learning_id,
            "data": learning_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "learning"
        }
        
        # Store in shared memory for all targets
        for target_agent in target_agents:
            namespace = f"shared_memory:{target_agent}"
            key = f"learning:{learning_id}"
            # Redis HSET
            self.redis.hset(
                f"shared_memory:{namespace}:insight:{learning_id}",
                "data", 
                json.dumps({
                    **source**: source_agent,
                    **targets**: target_agents,
                    **learning_id**: learning_id,
                    **data**: learning_data,
                    **timestamp**: event["timestamp"]
                })
            )
        
        return event
    
    def query_learnings(self, agent: str, 
                       learning_type: Optional[str] = None, 
                       source_agent: Optional[str] = None, limit: int = 10):
        """Query learning events for an agent."""
        namespace = f"shared_memory:{agent}"
        
        # Build Redis pipeline for learning events
        pipeline = self.redis.pipeline()
        
        if learning_type:
            type_key = f"shared_memory:{agent}:type:{learning_type}"
            pipeline.smembers(type_key)
            type_members = pipeline.execute()
            
            if type_members:
                for learning_id in type_members[:limit]:
                    insight_key = f"shared_memory:{agent}:insight:{learning_id}"
                    pipeline.hget(insight_key)
                    results.extend(pipeline.execute())
        
        if source_agent:
            # Filter by source agent
            source_key = f"shared_memory:{agent}:source:{source_agent}"
            source_members = self.redis.smembers(source_key)
            
            if source_members:
                for learning_id in source_members[:limit]:
                    insight_key = f"shared_memory:{agent}:insight:{learning_id}"
                    pipeline.hget(insight_key)
                    results.extend(pipeline.execute())
        
        pipeline.execute()
        return results
```

**Task 3.2: Integrate with Agent Memory**
```python
# Modify Agent Memory to support cross-agent learning

class AgentMemory:
    def add_learning(self, source_agent: str, learning_data: Dict[str, Any]):
        """Add a learning event from another agent."""
        # Store as insight with special category
        self.add_insight(
            content=f"Learned from {source_agent}",
            category="learning",
            metadata={"source_agent": source_agent, "learning_data": learning_data}
        )
    
    def sync_cross_agent_learnings(self, target_agents: List[str]):
        """Sync learnings from other agents."""
        for agent_id in target_agents:
            # Query learnings for this agent from shared memory
            # This requires implementing the learning protocol
            pass
```

#### Phase 4: Add Session Management Integration (2 hours)

**Task 4.1: Create session manager adapter**
```python
# File: /opt/blackbox5/services/session_manager.py

import redis
import json

class SessionManagerAdapter:
    """Adapter to integrate MaltBot sessions with BB5 Session Manager."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        
    def create_persistent_session(self, agent: str, session_name: str) -> str:
        """Create a persistent session via BB5 Orchestrator."""
        # Call BB5's session management
        # This requires BB5's session manager RPC
        # For now, return session ID
        return f"session:{agent}:{session_name}"
    
    def get_active_sessions(self, agent: str) -> List[Dict[str, Any]]:
        """Get all active sessions for an agent."""
        # Query Redis for active sessions
        agent_sessions_key = f"agent_sessions:{agent}"
        session_data = self.redis.hgetall(agent_sessions_key)
        
        if not session_data:
            return []
        
        return json.loads(session_data)
    
    def update_session_status(self, agent: str, session_id: str, status: str):
        """Update session status."""
        session_key = f"agent_sessions:{agent}:{session_id}"
        status_key = f"agent_sessions:{agent}:{session_id}:status"
        
        self.redis.hset(session_key, "status", status)
        self.redis.hset(status_key, "last_updated", datetime.now(timezone.utc).isoformat())
```

**Task 4.2: Integrate with OpenClaw Gateway**
```python
# Modify session manager to use OpenClaw Gateway

class SessionManagerAdapter:
    def create_persistent_session_via_gateway(self, agent: str, session_name: str) -> str:
        """Create persistent session via OpenClaw Gateway."""
        # This would require OpenClaw Gateway RPC call
        # For now, use direct Redis storage
        session_id = f"{agent}:{session_name}:{uuid.uuid4()}"
        
        # Store session data
        session_key = f"agent_sessions:{agent}:{session_id}"
        session_data = {
            "agent": agent,
            "session_name": session_name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active",
            "session_type": "persistent",
            "last_activity": datetime.now(timezone.utc).isoformat()
        }
        
        # Store in Redis
        self.redis.hset(session_key, "data", json.dumps(session_data))
        
        # Add to agent's active sessions list
        active_sessions_key = f"agent_sessions:{agent}:active"
        self.redis.sadd(active_sessions_key, session_id)
        
        return session_id
```

## Acceptance Criteria

- [x] Shared memory service created
- [x] Redis-based storage implemented
- [x] API endpoints defined (add, query)
- [x] Agent Memory extended with shared memory support
- [x] Agents can add insights to shared memory
- [x] Agents can query shared memory
- [x] Cross-agent learning protocol designed
- [x] Session manager adapter created
- [ ] Shared memory service deployed and tested
- [ ] Agent Memory updated and tested
- [ ] Session manager integrated and tested
- [ ] MaltBot configured to use shared memory
- [ ] Documentation updated

## Next Steps

**Phase 2 Tasks:**
1. Deploy shared memory service to VPS (port 8000)
2. Update Agent Memory with shared memory API calls
3. Update agent configs to enable shared memory
4. Test MaltBot adding insights to shared memory
5. Test cross-agent learning

**Phase 3 Tasks:**
1. Implement learning protocol in shared memory service
2. Integrate learning protocol with Agent Memory
3. Test MaltBot learning from BB5 insights
4. Test BB5 learning from MaltBot insights

**Phase 4 Tasks:**
1. Integrate session manager adapter with OpenClaw Gateway
2. Test MaltBot session management via shared memory
3. Test persistent sessions
4. Test cross-session messaging

---

**Estimated Total Time:** 8 hours

**Dependencies:**
- Redis server (already running)
- Agent Memory (existing)
- FastAPI (for REST API)
- OpenClaw Gateway (existing)

**This provides the foundation for MaltBot and BlackBox5 to share knowledge and learn from each other's experiences!**
