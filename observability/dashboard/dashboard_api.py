#!/usr/bin/env python3
"""
Observability Dashboard API for BlackBox5.

FastAPI backend serving real-time metrics, costs, logs, and health checks.
Provides WebSocket for live updates and REST API for data queries.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bin" / "lib"))

# Add observability components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from health_monitor import (
    collect_queue,
    collect_heartbeat,
    collect_events,
    collect_metrics,
    calculate_health_score,
    calculate_queue_health,
    calculate_agent_health,
    calculate_throughput,
    detect_stuck_tasks,
    get_recent_snapshots,
    HealthSnapshot,
    HealthStatus,
)

from health_checks import HealthChecker, HealthStatus as HC_HealthStatus
from cost_tracker import CostTracker, APIProvider, ModelType
from log_pipeline import LogPipeline, LogLevel, LogSource

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BlackBox5 Observability API",
    description="Real-time monitoring and observability for BlackBox5 autonomous systems",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
health_checker = HealthChecker()
cost_tracker = CostTracker()
log_pipeline = LogPipeline()

# WebSocket connection manager
class ConnectionManager:
    """Manage WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: Dict):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()


# Pydantic models
class HealthResponse(BaseModel):
    """Health check response."""
    timestamp: str
    overall_status: str
    checks: Dict[str, Dict]


class MetricsResponse(BaseModel):
    """Metrics response."""
    timestamp: str
    health_score: int
    status: str
    queue: Dict
    agents: Dict
    throughput: Dict
    stuck_tasks: List


class CostsResponse(BaseModel):
    """Cost tracking response."""
    summary: Dict
    by_provider: Dict
    by_agent: Dict
    trends: List


class LogsResponse(BaseModel):
    """Logs response."""
    logs: List
    stats: Dict


# Background task for broadcasting updates
async def broadcast_updates():
    """Broadcast updates to all WebSocket clients every 5 seconds."""
    while True:
        try:
            # Collect current metrics
            tasks = collect_queue()
            agents = collect_heartbeat()
            events = collect_events()
            metrics = collect_metrics()

            score, status, _ = calculate_health_score(tasks, agents, events, metrics)
            queue_score, queue_status = calculate_queue_health(tasks)
            agent_score, agent_status = calculate_agent_health(agents)
            throughput = calculate_throughput(tasks)
            stuck = detect_stuck_tasks(tasks, events)

            pending = sum(1 for t in tasks if t.is_pending)
            in_progress = sum(1 for t in tasks if t.is_in_progress)
            completed = sum(1 for t in tasks if t.is_completed)
            blocked = sum(1 for t in tasks if t.status.value == "blocked")

            online = sum(1 for a in agents if a.is_online())
            stale = sum(1 for a in agents if a.is_stale())
            offline = len(agents) - online - stale

            data = {
                "type": "update",
                "timestamp": datetime.now().isoformat(),
                "health_score": score,
                "status": status.value,
                "queue": {
                    "pending": pending,
                    "in_progress": in_progress,
                    "completed": completed,
                    "blocked": blocked,
                    "total": len(tasks),
                    "score": queue_score,
                    "status": queue_status,
                },
                "agents": {
                    "online": online,
                    "stale": stale,
                    "offline": offline,
                    "total": len(agents),
                    "score": agent_score,
                    "status": agent_status,
                },
                "throughput": {
                    "tasks_per_day": round(throughput, 2),
                    "target": 5,
                },
                "stuck_tasks": [
                    {
                        "id": st.task.id,
                        "title": st.task.title,
                        "reason": st.reason,
                        "duration": st.stuck_duration,
                    }
                    for st in stuck
                ],
            }

            await manager.broadcast(data)

        except Exception as e:
            logger.error(f"Error broadcasting updates: {e}")

        await asyncio.sleep(5)


# Start background task on startup
@app.on_event("startup")
async def startup_event():
    """Initialize background tasks."""
    logger.info("Starting BlackBox5 Observability API")
    asyncio.create_task(broadcast_updates())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down BlackBox5 Observability API")
    await health_checker.close()


# Health endpoints
@app.get("/health", response_model=Dict)
async def get_health():
    """Get overall system health."""
    checks = health_checker.check_all()

    # Determine overall status
    statuses = [r.status.value for r in checks.values()]
    if "unhealthy" in statuses:
        overall = "unhealthy"
    elif "degraded" in statuses:
        overall = "degraded"
    else:
        overall = "healthy"

    return {
        "timestamp": datetime.now().isoformat(),
        "overall_status": overall,
        "checks": {k: v.to_dict() for k, v in checks.items()},
    }


@app.get("/health/database")
async def get_database_health():
    """Get database health."""
    result = health_checker.check_database()
    return result.to_dict()


@app.get("/health/redis")
async def get_redis_health():
    """Get Redis health."""
    result = health_checker.check_redis()
    return result.to_dict()


@app.get("/health/nats")
async def get_nats_health():
    """Get NATS health."""
    result = health_checker.check_nats()
    return result.to_dict()


@app.get("/health/agents")
async def get_agents_health():
    """Get all agents health."""
    result = health_checker.check_agents()
    return result.to_dict()


@app.get("/health/agents/{agent_name}")
async def get_agent_health(agent_name: str):
    """Get specific agent health."""
    result = health_checker.check_agent(agent_name)
    return result.to_dict()


@app.get("/health/queue")
async def get_queue_health():
    """Get task queue health."""
    result = health_checker.check_queue()
    return result.to_dict()


@app.get("/health/cron")
async def get_cron_health():
    """Get cron job health."""
    result = health_checker.check_cron_jobs()
    return result.to_dict()


# Metrics endpoints
@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current system metrics."""
    tasks = collect_queue()
    agents = collect_heartbeat()
    events = collect_events()
    metrics = collect_metrics()

    score, status, _ = calculate_health_score(tasks, agents, events, metrics)
    queue_score, queue_status = calculate_queue_health(tasks)
    agent_score, agent_status = calculate_agent_health(agents)
    throughput = calculate_throughput(tasks)
    stuck = detect_stuck_tasks(tasks, events)

    pending = sum(1 for t in tasks if t.is_pending)
    in_progress = sum(1 for t in tasks if t.is_in_progress)
    completed = sum(1 for t in tasks if t.is_completed)
    blocked = sum(1 for t in tasks if t.status.value == "blocked")

    online = sum(1 for a in agents if a.is_online())
    stale = sum(1 for a in agents if a.is_stale())
    offline = len(agents) - online - stale

    return MetricsResponse(
        timestamp=datetime.now().isoformat(),
        health_score=score,
        status=status.value,
        queue={
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "blocked": blocked,
            "total": len(tasks),
            "score": queue_score,
            "status": queue_status,
        },
        agents={
            "online": online,
            "stale": stale,
            "offline": offline,
            "total": len(agents),
            "score": agent_score,
            "status": agent_status,
        },
        throughput={
            "tasks_per_day": round(throughput, 2),
            "target": 5,
        },
        stuck_tasks=[
            {
                "id": st.task.id,
                "title": st.task.title,
                "reason": st.reason,
                "duration": st.stuck_duration,
            }
            for st in stuck
        ],
    )


@app.get("/api/metrics/history")
async def get_metrics_history(hours: int = Query(24, ge=1, le=168)):
    """Get historical metrics data."""
    snapshots = get_recent_snapshots(hours=hours)

    return {
        "data": [s.to_dict() for s in snapshots],
    }


# Agents endpoints
@app.get("/api/agents")
async def get_agents():
    """Get all agents with their status."""
    agents = collect_heartbeat()

    return {
        "agents": [
            {
                "name": a.name,
                "status": a.get_status().value,
                "last_seen": a.last_seen.isoformat(),
                "seconds_since_seen": a.seconds_since_seen(),
                "current_task": a.current_task,
                "loop_number": a.loop_number,
            }
            for a in agents
        ],
        "total": len(agents),
    }


@app.get("/api/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """Get details for a specific agent."""
    agents = collect_heartbeat()

    agent = next((a for a in agents if a.name == agent_name), None)

    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

    return {
        "name": agent.name,
        "status": agent.get_status().value,
        "last_seen": agent.last_seen.isoformat(),
        "seconds_since_seen": agent.seconds_since_seen(),
        "current_task": agent.current_task,
        "loop_number": agent.loop_number,
        "is_online": agent.is_online(),
        "is_stale": agent.is_stale(),
    }


# Queue endpoints
@app.get("/api/queue")
async def get_queue():
    """Get task queue status."""
    tasks = collect_queue()

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status.value,
                "priority": t.priority,
                "estimated_minutes": t.estimated_minutes,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "started_at": t.started_at.isoformat() if t.started_at else None,
                "agent": t.agent,
                "tags": t.tags,
            }
            for t in tasks
        ],
        "summary": {
            "pending": sum(1 for t in tasks if t.is_pending),
            "in_progress": sum(1 for t in tasks if t.is_in_progress),
            "completed": sum(1 for t in tasks if t.is_completed),
            "blocked": sum(1 for t in tasks if t.status.value == "blocked"),
            "total": len(tasks),
        },
    }


@app.get("/api/queue/{task_id}")
async def get_task_details(task_id: str):
    """Get details for a specific task."""
    tasks = collect_queue()

    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {
        "id": task.id,
        "title": task.title,
        "status": task.status.value,
        "priority": task.priority,
        "estimated_minutes": task.estimated_minutes,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "agent": task.agent,
        "elapsed_minutes": task.elapsed_minutes(),
        "blocked_by": task.blocked_by,
        "tags": task.tags,
    }


# Cost endpoints
@app.get("/api/costs", response_model=CostsResponse)
async def get_costs(since_days: int = Query(7, ge=1, le=90)):
    """Get cost tracking data."""
    start_date = datetime.now() - timedelta(days=since_days)
    end_date = datetime.now()

    summary = cost_tracker.get_cost_summary(start_date, end_date)
    by_provider = cost_tracker.get_costs_by_provider(start_date, end_date)
    by_agent = cost_tracker.get_costs_by_agent(start_date, end_date)
    trends = cost_tracker.get_cost_trends(days=since_days)

    return CostsResponse(
        summary={
            "start_date": summary.start_date.isoformat(),
            "end_date": summary.end_date.isoformat(),
            "total_cost": summary.total_cost,
            "total_tokens": summary.total_tokens,
            "total_calls": summary.total_calls,
            "successful_calls": summary.successful_calls,
            "failed_calls": summary.failed_calls,
        },
        by_provider=by_provider,
        by_agent=by_agent,
        trends=trends,
    )


@app.get("/api/costs/budget")
async def check_budget_alerts(
    monthly_budget: float = Query(..., gt=0),
    threshold: float = Query(0.9, ge=0.5, le=1.0),
):
    """Check if budget thresholds have been exceeded."""
    alerts = cost_tracker.check_budget_alerts(monthly_budget, threshold)

    return {
        "monthly_budget": monthly_budget,
        "threshold_percent": threshold,
        "alerts": alerts,
    }


# Logs endpoints
@app.get("/api/logs")
async def get_logs(
    query: str = Query(""),
    agent: Optional[str] = None,
    level: Optional[str] = Query(None, regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"),
    task_id: Optional[str] = None,
    since_hours: int = Query(24, ge=1, le=168),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get log entries with filters."""
    start_date = datetime.now() - timedelta(hours=since_hours)

    if task_id:
        logs = log_pipeline.get_logs_by_task(task_id, limit=limit)
        stats = {}
    else:
        logs = log_pipeline.search_logs(
            query=query,
            start_date=start_date,
            agent=agent,
            level=LogLevel(level.upper()) if level else None,
            limit=limit,
        )
        stats = log_pipeline.get_log_stats(start_date=start_date)

    return {
        "logs": [l.to_dict() for l in logs],
        "stats": stats,
        "count": len(logs),
    }


@app.get("/api/logs/stats")
async def get_log_stats(since_hours: int = Query(24, ge=1, le=168)):
    """Get log statistics."""
    start_date = datetime.now() - timedelta(hours=since_hours)
    stats = log_pipeline.get_log_stats(start_date=start_date)

    return stats


# Alerts endpoints
@app.get("/api/alerts")
async def get_alerts(
    hours: int = Query(24, ge=1, le=168),
):
    """Get recent alerts."""
    # This would be implemented when we have a proper alert storage system
    return {
        "alerts": [],
        "count": 0,
    }


# WebSocket endpoint
@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)

    try:
        # Send initial data
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to BlackBox5 Observability",
            "timestamp": datetime.now().isoformat(),
        })

        # Keep connection alive and handle client messages
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client requests
            await websocket.send_json({
                "type": "echo",
                "message": data,
                "timestamp": datetime.now().isoformat(),
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "BlackBox5 Observability API",
        "version": "1.0.0",
        "description": "Real-time monitoring and observability for BlackBox5",
        "endpoints": {
            "health": "/health",
            "metrics": "/api/metrics",
            "agents": "/api/agents",
            "queue": "/api/queue",
            "costs": "/api/costs",
            "logs": "/api/logs",
            "websocket": "/api/stream",
        },
        "docs": "/docs",
    }


def main():
    """Run the API server."""
    import uvicorn

    uvicorn.run(
        "dashboard_api:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
