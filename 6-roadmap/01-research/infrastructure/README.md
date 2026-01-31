# Blackbox5 Kubernetes Infrastructure

Cloud-native infrastructure for running RALF autonomous agents on Kubernetes.

## Overview

This infrastructure enables:
- **24/7 autonomous RALF agents** running in the cloud
- **Multiple RALF instances** for different projects
- **GitHub integration** via MCP servers
- **Shared code storage** with persistent volumes
- **Remote control** via REST API

## Architecture

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

## Prerequisites

1. **Hetzner Cloud account** - https://console.hetzner.cloud
2. **kubectl** installed locally
3. **k3sup** (optional) for easy k3s installation
4. **API tokens:**
   - Anthropic API key
   - GitHub Personal Access Token
   - GitHub SSH key

## Quick Start

### 1. Provision Infrastructure

```bash
# Create 3x CPX31 servers in Hetzner Cloud
# - 1 control plane (4 vCPU, 8GB RAM)
# - 2 workers (4 vCPU, 8GB RAM each)

# Install k3s on control plane
ssh root@<control-plane-ip>
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san=<floating-ip>

# Get kubeconfig
scp root@<control-plane-ip>:/etc/rancher/k3s/k3s.yaml ~/.kube/config

# Join workers
curl -sfL https://get.k3s.io | K3S_URL=https://<master-ip>:6443 \
  K3S_TOKEN=<token> sh -s - agent
```

### 2. Install Hetzner CSI

```bash
kubectl apply -f https://raw.githubusercontent.com/hetznercloud/csi-driver/v2.5.1/deploy/kubernetes/hcloud-csi.yml
```

### 3. Deploy Blackbox5

```bash
# Create namespaces
kubectl apply -f k8s-manifests/namespaces.yaml

# Configure secrets (edit first!)
cp k8s-manifests/secrets/secrets-template.yaml k8s-manifests/secrets/secrets.yaml
# Edit secrets.yaml with your actual values
kubectl apply -f k8s-manifests/secrets/secrets.yaml

# Deploy storage
kubectl apply -f k8s-manifests/storage/

# Deploy RBAC
kubectl apply -f k8s-manifests/control-plane/rbac.yaml

# Deploy MCP config
kubectl apply -f k8s-manifests/mcp/mcp-config.yaml

# Deploy first RALF agent
kubectl apply -f k8s-manifests/agents/ralf-blackbox5.yaml
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n blackbox5-agents

# View RALF logs
kubectl logs -n blackbox5-agents deployment/ralf-blackbox5 -f

# Check storage
kubectl get pvc -n blackbox5-storage
```

## Directory Structure

```
k8s-manifests/
├── namespaces.yaml          # Namespace definitions
├── storage/
│   ├── storage-class.yaml   # Hetzner CSI storage classes
│   └── pvc.yaml            # Persistent volume claims
├── control-plane/
│   └── rbac.yaml           # Service accounts and permissions
├── agents/
│   └── ralf-blackbox5.yaml # RALF agent deployment
├── mcp/
│   └── mcp-config.yaml     # MCP server configuration
└── secrets/
    └── secrets-template.yaml # Secret templates (copy and edit)
```

## Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| 3x CPX31 (4 vCPU/8GB) | €37.20 |
| 200GB Storage | €10.50 |
| Load Balancer | €5.39 |
| Floating IP | €1.09 |
| Backups | €7.44 |
| **Total** | **€61.62 (~$67 USD)** |

## Scaling

### Add More RALF Agents

```bash
# Scale existing deployment
kubectl scale deployment ralf-blackbox5 -n blackbox5-agents --replicas=3

# Or create new agent for different project
kubectl apply -f k8s-manifests/agents/ralf-siso-internal.yaml
```

### Add More Nodes

```bash
# Provision new server in Hetzner
# Join to cluster
curl -sfL https://get.k3s.io | K3S_URL=https://<master-ip>:6443 \
  K3S_TOKEN=<token> sh -s - agent
```

## Troubleshooting

### Check Pod Status
```bash
kubectl describe pod -n blackbox5-agents <pod-name>
```

### View Logs
```bash
kubectl logs -n blackbox5-agents deployment/ralf-blackbox5
```

### Exec Into Pod
```bash
kubectl exec -it -n blackbox5-agents deployment/ralf-blackbox5 -- /bin/bash
```

### Check Events
```bash
kubectl get events -n blackbox5-agents --sort-by='.lastTimestamp'
```

## Next Steps

1. Build container images (`Dockerfile.ralf-agent`)
2. Deploy Redis cluster for state management
3. Deploy MCP servers (GitHub, etc.)
4. Set up monitoring (Prometheus/Grafana)
5. Configure backups (Velero)

## References

- [k3s Documentation](https://docs.k3s.io/)
- [Hetzner Cloud](https://docs.hetzner.cloud/)
- [RALF Loop](../../../../../2-engine/.autonomous/shell/ralf-loop.sh)
- [Decision Record](../../../../../5-project-memory/blackbox5/decisions/infrastructure/k8s-architecture-design.md)
