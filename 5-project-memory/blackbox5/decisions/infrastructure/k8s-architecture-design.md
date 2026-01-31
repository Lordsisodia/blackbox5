# Decision: Kubernetes Infrastructure for Blackbox5

**Date:** 2026-01-31
**Status:** Approved
**Decision Maker:** shaansisodia
**Context:** RALF autonomous agents need 24/7 cloud operation with GitHub integration

---

## Problem Statement

We need to run RALF (Recursive Autonomous Learning Framework) agents in the cloud with:
- 24/7 autonomous operation
- Multiple RALF instances running simultaneously
- GitHub integration with MCP
- Shared code storage
- Ability to start/stop/control agents remotely

## Decision

**Use Kubernetes (k3s) on Hetzner Cloud** as the infrastructure platform.

### Rationale

1. **Cost-effective at scale** - €61/month for 3-node cluster vs $70+ on Render for equivalent compute
2. **Native container orchestration** - Perfect fit for RALF as containerized agents
3. **Persistent storage** - Shared volumes for code repository access
4. **Scalability** - Easy to add more RALF instances by scaling pods
5. **Control** - Full control over networking, security, and resource allocation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Hetzner Cloud (k3s)                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    blackbox5-system Namespace                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │ RALF Operator│  │ Control API  │  │  Agent Scheduler     │  │   │
│  │  │ (CRD Watcher)│  │ (REST/gRPC)  │  │  (Loop Controller)   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    blackbox5-agents Namespace                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │   │
│  │  │ RALF-001 │ │ RALF-002 │ │ RALF-003 │ │ RALF-00N │            │   │
│  │  │ (blackbox│ │ (siso-   │ │ (research│ │ (custom) │            │   │
│  │  │    5)    │ │ internal)│ │   loop)  │ │          │            │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    blackbox5-storage Namespace                   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                    │   │
│  │  │  Code Volume     │  │  Redis Cluster   │                    │   │
│  │  │  (ReadWriteMany) │  │  (State/Coord)   │                    │   │
│  │  │  100GB+ NFS/Ceph │  │  3-node cluster  │                    │   │
│  │  └──────────────────┘  └──────────────────┘                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    blackbox5-mcp Namespace                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │   │
│  │  │ GitHub MCP   │  │ Filesystem   │  │  Serena      │          │   │
│  │  │  Server      │  │ MCP Server   │  │  (Code)      │          │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. RALF Agent Pods
- Run the RALF loop (`ralf-loop.sh`) continuously
- Mount shared code volume at `/opt/blackbox5`
- Connect to Redis for state management
- Access MCP servers for GitHub integration

### 2. Control Plane
- REST API for managing RALF instances
- Custom Resource Definition (CRD) for `RALFInstance`
- WebSocket gateway for real-time communication

### 3. Storage
- **Code Volume**: Shared ReadWriteMany PVC for git repository
- **Runs Volume**: Persistent storage for run directories
- **Redis**: State management and task queue

### 4. MCP Servers
- GitHub MCP for repository operations
- Filesystem MCP for file access
- Serena MCP for code search

## Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| 3x CPX31 (4 vCPU/8GB) | €37.20 |
| 210GB Storage | €10.50 |
| Load Balancer | €5.39 |
| Floating IP | €1.09 |
| Backups | €7.44 |
| **Total** | **€61.62 (~$67 USD)** |

## Implementation Phases

### Phase 1: Infrastructure (Week 1)
- Provision Hetzner servers
- Install k3s cluster
- Set up storage (Hetzner CSI)
- Deploy Redis cluster

### Phase 2: Core Deployment (Week 2)
- Build container images
- Deploy control plane
- Deploy first RALF instance
- Test GitHub integration

### Phase 3: Multi-Agent (Week 3)
- Deploy RALF Operator
- Implement CRD-based agent creation
- Add monitoring (Prometheus/Grafana)

### Phase 4: Production (Week 4)
- Security hardening
- Backup configuration
- Documentation

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Render | Simple, managed | Expensive at scale ($70+), limited control | ❌ Rejected |
| Railway | Easy deploy | $5/month min, less mature | ❌ Rejected |
| AWS EKS | Enterprise features | Complex, expensive ($150+/month) | ❌ Rejected |
| **Hetzner + k3s** | **Cost-effective, full control** | **More setup required** | ✅ **Selected** |

## Consequences

### Positive
- Run 5-10 RALF agents for cost of 1 Render service
- Full control over networking and security
- Easy to scale horizontally
- Persistent shared storage for code

### Negative
- Requires Kubernetes knowledge
- More complex initial setup
- Self-managed (no managed Kubernetes)
- Need to handle backups and monitoring

## Related Files

- `2-engine/.autonomous/shell/ralf-loop.sh` - Core RALF loop
- `bin/ralf` - Entry point script
- `.mcp.json` - MCP configuration
- `5-project-memory/blackbox5/.autonomous/routes.yaml` - Project routing

## Next Steps

1. Provision Hetzner Cloud servers
2. Install k3s cluster
3. Create container images
4. Deploy first RALF instance
5. Test GitHub integration

---

**Decision Record ID:** INFRA-001
