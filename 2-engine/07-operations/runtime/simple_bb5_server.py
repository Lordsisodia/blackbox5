#!/usr/bin/env python3
"""
Simple BLACKBOX5 API Server - Standalone

A minimal FastAPI server that provides the BLACKBOX5 API endpoints
without the complex infrastructure imports that are causing issues.

This is a temporary solution for overnight monitoring.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENGINE_ROOT = PROJECT_ROOT / "2-engine" / "01-core"
sys.path.insert(0, str(ENGINE_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler("/tmp/blackbox5_simple_server.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SimpleBB5Server")

# FastAPI app
app = FastAPI(
    title="BLACKBOX5 API",
    description="Simple standalone API server for BLACKBOX5",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_server_start_time = datetime.now()
_request_count = 0


# Pydantic models
class Message(BaseModel):
    message: str
    session_id: Optional[str] = None


class AgentInfo(BaseModel):
    id: str
    name: str
    category: str
    role: str
    capabilities: List[str]


class ChatResponse(BaseModel):
    response: str
    agent: str
    routing_metadata: Dict[str, Any]
    timestamp: str


# Sample agents data (in production, this would be loaded from actual agents)
SAMPLE_AGENTS = [
    {
        "id": "architect",
        "name": "architect",
        "category": "core",
        "role": "System Architect",
        "capabilities": [
            "Design system architectures",
            "Plan complex multi-step tasks",
            "Coordinate between agents",
            "Make technical decisions",
            "Review and approve designs"
        ]
    },
    {
        "id": "frontend-specialist",
        "name": "Frontend Specialist",
        "category": "specialists",
        "role": "Frontend Development Expert",
        "capabilities": [
            "Create React components",
            "Build user interfaces",
            "Implement responsive designs",
            "Handle frontend state management",
            "Work with TypeScript"
        ]
    },
    {
        "id": "backend-specialist",
        "name": "Backend Specialist",
        "category": "specialists",
        "role": "Backend Development Expert",
        "capabilities": [
            "Implement REST APIs",
            "Build server-side logic",
            "Handle authentication",
            "Work with databases",
            "Design microservices"
        ]
    },
    {
        "id": "ui-ux-specialist",
        "name": "UI/UX Specialist",
        "category": "specialists",
        "role": "User Experience Designer",
        "capabilities": [
            "Design user flows",
            "Create wireframes",
            "Build prototypes",
            "Conduct UX research",
            "Develop design systems"
        ]
    },
    {
        "id": "testing-specialist",
        "name": "Testing Specialist",
        "category": "specialists",
        "role": "Quality Assurance Expert",
        "capabilities": [
            "Write unit tests",
            "Create integration tests",
            "Design test strategies",
            "Implement TDD/BDD",
            "Debug failing tests"
        ]
    },
    {
        "id": "security-specialist",
        "name": "Security Specialist",
        "category": "specialists",
        "role": "Security Expert",
        "capabilities": [
            "Audit code for vulnerabilities",
            "Implement security measures",
            "Review authentication",
            "Handle encryption",
            "Perform security assessments"
        ]
    },
    {
        "id": "database-specialist",
        "name": "Database Specialist",
        "category": "specialists",
        "role": "Database Expert",
        "capabilities": [
            "Optimize database queries",
            "Design schemas",
            "Handle migrations",
            "Improve performance",
            "Manage database operations"
        ]
    },
    {
        "id": "devops-specialist",
        "name": "DevOps Specialist",
        "category": "specialists",
        "role": "DevOps Engineer",
        "capabilities": [
            "Deploy to Kubernetes",
            "Manage infrastructure",
            "Set up CI/CD pipelines",
            "Handle deployments",
            "Configure cloud services"
        ]
    },
    {
        "id": "mobile-specialist",
        "name": "Mobile Development Specialist",
        "category": "specialists",
        "role": "Mobile Development Expert",
        "capabilities": [
            "Build mobile apps",
            "Implement push notifications",
            "Handle iOS/Android development",
            "Work with React Native",
            "Configure mobile services"
        ]
    },
    {
        "id": "ml-specialist",
        "name": "Machine Learning Specialist",
        "category": "specialists",
        "role": "ML Engineer",
        "capabilities": [
            "Implement ML models",
            "Train neural networks",
            "Handle recommendations",
            "Process data",
            "Deploy ML services"
        ]
    }
]


# Simple routing logic based on keywords
def route_message(message: str) -> str:
    """
    Simple keyword-based routing for demonstration.
    In production, this would use the actual TaskRouter.
    """
    message_lower = message.lower()

    # Check for specific keywords
    if any(word in message_lower for word in ['architecture', 'design system', 'plan', 'coordinate']):
        return "architect"
    elif any(word in message_lower for word in ['react', 'component', 'frontend', 'ui', 'interface', 'typescript']):
        return "frontend-specialist"
    elif any(word in message_lower for word in ['api', 'backend', 'server', 'auth', 'microservices']):
        return "backend-specialist"
    elif any(word in message_lower for word in ['ux', 'user onboarding', 'wireframe', 'prototype', 'design flow']):
        return "ui-ux-specialist"
    elif any(word in message_lower for word in ['test', 'unit test', 'testing', 'tdd', 'bdd']):
        return "testing-specialist"
    elif any(word in message_lower for word in ['security', 'vulnerability', 'audit', 'penetration', 'encrypt']):
        return "security-specialist"
    elif any(word in message_lower for word in ['database', 'sql', 'query', 'optimization', 'schema']):
        return "database-specialist"
    elif any(word in message_lower for word in ['kubernetes', 'deploy', 'docker', 'ci/cd', 'devops']):
        return "devops-specialist"
    elif any(word in message_lower for word in ['mobile', 'ios', 'android', 'push notification', 'react native']):
        return "mobile-specialist"
    elif any(word in message_lower for word in ['ml', 'machine learning', 'model', 'recommendation', 'tensorflow']):
        return "ml-specialist"
    else:
        return "architect"  # Default


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "BLACKBOX5 API",
        "status": "running",
        "version": "1.0.0",
        "start_time": _server_start_time.isoformat()
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    uptime = (datetime.now() - _server_start_time).total_seconds()

    return {
        "status": "healthy",
        "uptime_seconds": uptime,
        "request_count": _request_count,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": SAMPLE_AGENTS,
        "count": len(SAMPLE_AGENTS)
    }


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get details of a specific agent"""
    agent = next((a for a in SAMPLE_AGENTS if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return agent


@app.post("/chat")
async def chat(message: Message):
    """
    Chat endpoint - processes a message through the BLACKBOX5 system

    For this simple server, it just does routing and returns a mock response.
    """
    global _request_count
    _request_count += 1

    # Route the message
    agent_id = route_message(message.message)
    agent = next((a for a in SAMPLE_AGENTS if a["id"] == agent_id), SAMPLE_AGENTS[0])

    # Mock response
    response = f"This is a mock response from {agent['name']}. The full BLACKBOX5 engine is not running."

    return ChatResponse(
        response=response,
        agent=agent["name"],
        routing_metadata={
            "selected_agent": agent_id,
            "agent_category": agent["category"],
            "confidence": 0.85,
            "routing_method": "keyword_match"
        },
        timestamp=datetime.now().isoformat()
    )


@app.get("/stats")
async def stats():
    """Get server statistics"""
    uptime = (datetime.now() - _server_start_time).total_seconds()

    return {
        "uptime_seconds": uptime,
        "request_count": _request_count,
        "agents_available": len(SAMPLE_AGENTS),
        "start_time": _server_start_time.isoformat()
    }


def main():
    """Run the server"""
    logger.info("=" * 60)
    logger.info("BLACKBOX5 Simple API Server Starting")
    logger.info("=" * 60)
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Engine root: {ENGINE_ROOT}")
    logger.info(f"Agents available: {len(SAMPLE_AGENTS)}")
    logger.info("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
