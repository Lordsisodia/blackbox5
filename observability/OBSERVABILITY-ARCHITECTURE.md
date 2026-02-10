# BlackBox5 Observability Dashboard - Architecture

## Overview

A comprehensive observability system providing full visibility into BlackBox5 operations, built on the existing `health_monitor` library.

## Components

### 1. Core Infrastructure (Existing)
- **Location:** `/opt/blackbox5/bin/lib/health_monitor/`
- **Features:**
  - SQLite database for metrics storage
  - Health scoring algorithms
  - Agent heartbeat monitoring
  - Task queue tracking
  - Stuck task detection
  - Alert system
  - Daemon for continuous monitoring

### 2. New Components

#### A. Observability Dashboard Web UI
- **Location:** `/opt/blackbox5/observability/dashboard/`
- **Framework:** FastAPI backend + React frontend
- **Features:**
  - Real-time metrics visualization
  - Agent status monitoring
  - Task queue overview
  - Cost tracking dashboard
  - Log viewer
  - Historical trend analysis

#### B. Cost Tracker
- **Location:** `/opt/blackbox5/observability/cost_tracker/`
- **Features:**
  - Token usage tracking per agent/API
  - Cost calculation by provider (OpenAI, Claude, Kimi, Google, etc.)
  - Budget alerts
  - Historical cost reports

#### C. Log Aggregation Pipeline
- **Location:** `/opt/blackbox5/observability/log_pipeline/`
- **Features:**
  - Centralized log collection from all agents
  - Log parsing and indexing
  - Search and filtering
  - Real-time log streaming

#### D. Health Check Endpoints
- **Location:** `/opt/blackbox5/observability/health_checks/`
- **Features:**
  - HTTP endpoints for all services
  - Agent liveness checks
  - API status monitoring
  - Cron job status tracking

#### E. Metrics Exporter
- **Location:** `/opt/blackbox5/observability/metrics_exporter/`
- **Features:**
  - Prometheus-compatible metrics endpoint
  - Grafana dashboard templates
  - Custom metric collection

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      BlackBox5 Agents                            │
│  (moltbot-vps-ai, claude-mac, moltbot-macmini-01, etc.)        │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ├─→ Metrics (token usage, API calls, errors)
               ├─→ Logs (agent activity, errors, debug)
               ├─→ Heartbeats (liveness, current task)
               └─→ Events (task completion, failures)
               │
┌──────────────▼──────────────────────────────────────────────────┐
│              Health Monitor Daemon                              │
│         (existing: /opt/blackbox5/bin/lib/health_monitor)      │
│  - Collects metrics from queue.yaml, heartbeat.yaml, events.yaml│
│  - Calculates health scores                                     │
│  - Detects stuck tasks                                           │
│  - Saves to SQLite database                                     │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ├─→ Health Snapshots → SQLite
               ├─→ Metrics → SQLite
               └─→ Alerts → Alert Manager
               │
┌──────────────▼──────────────────────────────────────────────────┐
│              Observability Components                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Cost Tracker → Token costs by provider/agent                │
│  2. Log Pipeline → Centralized logs from Redis streams         │
│  3. Health Checks → HTTP /health endpoints                     │
│  4. Metrics Exporter → Prometheus format                       │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│              Dashboard Web UI                                    │
│         (FastAPI backend + React frontend)                      │
│  - Real-time WebSocket updates                                  │
│  - REST API for data queries                                    │
│  - Interactive charts and graphs                               │
│  - Cost tracking visualization                                  │
│  - Log viewer                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema

### health.db (SQLite)
Existing tables:
- `snapshots`: Health snapshots with system metrics
- `metrics`: Time-series metrics

New tables to add:
- `api_costs`: API usage and costs
- `agent_logs`: Centralized log entries
- `service_health`: Service health check results
- `budget_alerts`: Budget threshold alerts

## API Endpoints

### Observability API (FastAPI)

```
GET  /api/health              # Overall system health
GET  /api/agents              # Agent status
GET  /api/queue               # Task queue status
GET  /api/metrics             # Time-series metrics
GET  /api/costs               # Cost tracking data
GET  /api/logs                # Log entries with filters
GET  /api/alerts              # Active alerts
WS   /api/stream              # Real-time updates

GET  /api/costs/by-provider   # Costs by API provider
GET  /api/costs/by-agent      # Costs by agent
GET  /api/costs/trends        # Historical cost trends
GET  /api/logs/search         # Search logs
GET  /api/logs/stream         # Stream logs in real-time
```

### Health Check Endpoints

```
GET  /health                  # Overall health
GET  /health/database         # Database connectivity
GET  /health/redis            # Redis status
GET  /health/nats             # NATS status
GET  /health/agents           # All agents status
GET  /health/agents/{name}    # Specific agent status
GET  /health/cron             # Cron job status
```

### Prometheus Metrics

```
GET  /metrics                 # Prometheus-compatible metrics
```

## Alert Configuration

Alerts are configured in `/opt/blackbox5/observability/config/alerts.yaml`:

```yaml
alerts:
  - name: health_score_critical
    threshold: < 60
    severity: critical
    channels: [telegram, email]

  - name: agent_timeout
    threshold: > 120s
    severity: critical
    channels: [telegram]

  - name: budget_exceeded
    threshold: > 90% of monthly budget
    severity: warning
    channels: [telegram, email]
```

## Integration Points

### With BlackBox5 Scribe
- Export observability reports to Scribe documentation
- Auto-generate incident reports
- Log metric anomalies to Scribe

### With Redis Streams
- Subscribe to `stream:messages` for agent communication logs
- Subscribe to `stream:responses` for response metrics
- Subscribe to `stream:claude` for Claude-specific metrics

### With NATS JetStream
- Persistent message delivery for critical alerts
- Historical message replay for debugging

## Deployment

### Start Observability Stack

```bash
# Start all components
cd /opt/blackbox5
./bin/observability-start.sh

# Start individual components
./bin/observability-dashboard start    # Web UI
./bin/observability-cost-tracker start # Cost tracking
./bin/observability-log-pipeline start  # Log aggregation
./bin/observability-health-checks start # Health endpoints
```

### Stop Observability Stack

```bash
./bin/observability-stop.sh
```

## Configuration

All configuration in `/opt/blackbox5/observability/config/`:

- `dashboard.yaml`: Dashboard settings
- `costs.yaml`: API pricing and budgets
- `alerts.yaml`: Alert thresholds and channels
- `logging.yaml`: Log pipeline configuration
- `database.yaml`: Database settings

## Access

- **Dashboard UI:** http://77.42.66.40:8080
- **API Documentation:** http://77.42.66.40:8080/docs
- **Metrics Endpoint:** http://77.42.66.40:9090/metrics
- **Health Checks:** http://77.42.66.40:8080/health

## Future Enhancements

1. ML-based anomaly detection
2. Predictive cost forecasting
3. Automated incident response
4. Integration with PagerDuty/OpsGenie
5. Custom dashboards per team
6. Mobile app
7. Slack integration
