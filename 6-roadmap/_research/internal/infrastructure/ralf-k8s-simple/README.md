# Simple RALF Kubernetes Setup

Minimal, focused setup for running RALF autonomous agent on Kubernetes.

## What This Does

- Runs **one RALF agent** in a Kubernetes pod
- The agent continuously improves Blackbox5 (your project)
- Uses **Claude Code CLI** inside the container
- Persists code and runs using Kubernetes volumes

## Architecture

```
┌─────────────────────────────────────────┐
│         Hetzner Cloud (1 node)          │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │         Namespace: ralf         │   │
│  │                                 │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │      RALF Pod           │   │   │
│  │  │  ┌─────────────────┐    │   │   │
│  │  │  │  Claude Code    │    │   │   │
│  │  │  │  RALF Loop      │    │   │   │
│  │  │  │  Blackbox5 Repo │    │   │   │
│  │  │  └─────────────────┘    │   │   │
│  │  └─────────────────────────┘   │   │
│  │                                 │   │
│  │  Volumes:                       │   │
│  │  - 50GB for code (git repo)     │   │
│  │  - 20GB for runs/logs           │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Cost: ~£6.70/month (CPX21)             │
│                                         │
└─────────────────────────────────────────┘
```

## Prerequisites

1. **Kubernetes cluster** (k3s on Hetzner recommended)
2. **kubectl** configured to talk to your cluster
3. **Docker** for building the image
4. **API Keys:**
   - Anthropic API Key (for Claude)
   - GitHub Personal Access Token (for repo access)

## Quick Start

### 1. Provision Hetzner Server

```bash
# Create CPX21 (2 vCPU, 4GB RAM, £6.70/month)
# Install k3s:
curl -sfL https://get.k3s.io | sh -

# Copy kubeconfig
scp root@<server-ip>:/etc/rancher/k3s/k3s.yaml ~/.kube/config
```

### 2. Run Setup

```bash
cd /Users/shaansisodia/.blackbox5/6-roadmap/01-research/infrastructure/ralf-k8s-simple

# Run the setup script
./setup.sh
```

This will:
- Build the Docker image
- Create namespace and volumes
- Set up secrets
- Clone Blackbox5 repo
- Start RALF agent

### 3. Monitor RALF

```bash
# View logs (RALF output)
kubectl logs -n ralf deployment/ralf-agent -f

# Check status
kubectl get pods -n ralf

# Shell into container
kubectl exec -n ralf -it deployment/ralf-agent -- /bin/bash
```

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image with Claude Code + RALF |
| `entrypoint.sh` | Startup script inside container |
| `ralf-deployment.yaml` | Kubernetes deployment manifest |
| `setup.sh` | One-command setup script |

## How It Works

1. **Container starts** → Runs `entrypoint.sh`
2. **Waits for code** → Mounts persistent volume with Blackbox5
3. **Configures environment** → Sets up git, SSH, API keys
4. **Runs RALF** → Executes `bin/ralf` which starts Claude Code loop
5. **Continuous improvement** → RALF improves Blackbox5 24/7

## Scaling Up

To run multiple RALF agents:

```bash
# Scale to 3 agents
kubectl scale deployment ralf-agent -n ralf --replicas=3
```

Each agent gets its own pod but shares the code volume.

## Troubleshooting

### Pod not starting
```bash
kubectl describe pod -n ralf -l app=ralf
```

### Check logs
```bash
kubectl logs -n ralf deployment/ralf-agent
```

### Restart RALF
```bash
kubectl rollout restart deployment/ralf-agent -n ralf
```

## Cost

| Component | Cost |
|-----------|------|
| Hetzner CPX21 | €6.29 (~£5.25) |
| 70GB Storage | €3.08 (~£2.57) |
| **Total** | **~£7.82/month** |

## Next Steps

- [ ] Add web UI for monitoring
- [ ] Add REST API for controlling RALF
- [ ] Set up GitHub MCP server
- [ ] Add Prometheus metrics
