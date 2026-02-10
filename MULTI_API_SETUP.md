# BlackBox5 Multi-API Setup

## Overview
Intelligent multi-API provider system with automatic routing, load balancing, and cost optimization.

## Features

### 1. API Selector Agent
- **Purpose:** Automatically selects optimal API provider based on task requirements
- **Capabilities:**
  - Task requirement analysis (context length, capabilities needed)
  - Provider selection by priority, health, cost, and availability
  - Automatic fallback and retry logic
  - Health monitoring

### 2. API Usage Tracker
- **Purpose:** Tracks token usage, rate limits, and costs across all providers
- **Capabilities:**
  - Real-time usage tracking per provider
  - Rate limit monitoring
  - Cost estimation
  - Usage reports and analytics

### 3. Kimi Load Balancer (Enhanced)
- **Purpose:** Intelligent load balancing for 9 Kimi keys (1 CISO + 8 trials)
- **Capabilities:**
  - Priority-based selection (CISO key first)
  - Health monitoring
  - Trial key management (expiration tracking)
  - Automatic fallback to GLM-4.7

### 4. Nvidia Kimi Integration
- **Purpose:** Specialized integration for video and vision tasks
- **Capabilities:**
  - Video processing
  - Image analysis
  - Rate limiting for trial keys

## Configuration

### Main Config File: `/opt/blackbox5/config/api-keys.yaml`

The configuration includes:
- All API providers sorted by priority
- Task routing rules
- Cost optimization settings
- Rate limiting configuration

### API Keys Setup

Set these environment variables:

```bash
# Kimi CISO Key (primary)
export KIMI_CISO_KEY="sk-kimi-..."

# Kimi Trial Keys (optional - can be set in config)
export KIMI_TRIAL_KEY_01="sk-kimi-..."
# ... up to KIMI_TRIAL_KEY_08

# Nvidia Kimi Key
export NVIDIA_KIMI_KEY="sk-kimi-..."

# Anthropic Claude Key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Provider Priority & Capabilities

| Provider | Priority | Capabilities | Use Cases |
|----------|----------|---------------|-----------|
| **GLM-4.7** | 1 (primary) | long_context, reliable, general | General tasks, long conversations, default |
| **Kimi K2.5** | 0.8 | long_context, multimodal, coding, reasoning | Coding, video processing, vision tasks |
| **Claude Code** | 0.5 | long_context, reasoning, coding | Complex reasoning, critical tasks |
| **Nvidia Kimi** | 0.4 | vision, multimodal, video | Video processing, image analysis |

## Task Routing

Automatic routing based on task type:

| Task Type | Provider Priority | Strategy |
|-----------|------------------|----------|
| `long_context` | GLM → Claude → Kimi | cost_optimized |
| `coding` | Kimi → Claude → GLM | quality_first |
| `reasoning` | Claude → Kimi → GLM | quality_first |
| `video_processing` | Nvidia → Kimi | specialized_first |
| `vision` | Nvidia → Kimi | specialized_first |
| `general` | GLM → Kimi → Claude | availability_first |

## Usage

### Quick Start

```bash
# Run setup script
cd /opt/blackbox5
python3 scripts/setup_multi_api.py
```

### Programmatic Usage

```python
from agents.api_selector import APISelector

selector = APISelector()

# Select best provider for a task
selection = selector.select_provider(
    task_type="coding",
    required_capabilities=["coding", "reasoning"],
    criticality="high"
)

print(f"Selected: {selection.provider.name}")
print(f"API Key: {selection.provider.api_key}")
print(f"Base URL: {selection.provider.base_url}")

# Use the provider...
# Track usage
from agents.api_usage_tracker import APIUsageTracker

tracker = APIUsageTracker()
tracker.track_usage(
    provider=selection.provider.id,
    agent="main",
    task_type="coding",
    tokens_used=5000,
    duration_ms=1234,
    success=True
)
```

### Kimi Load Balancer

```python
from agents.kimi_load_balancer import KimiLoadBalancer

balancer = KimiLoadBalancer()

# Get best key
key = balancer.get_key(agent="main")

# Use the key...
# Report usage
balancer.report_usage(
    key_id=key.id,
    tokens_used=5000,
    latency_ms=1234,
    success=True
)

# Get status
status = balancer.get_key_status()
print(status)
```

### Nvidia Kimi Client

```python
from agents.nvidia_kimi_integration import NvidiaKimiClient

client = NvidiaKimiClient()

# Process video
result = client.process_video(
    video_path="/path/to/video.mp4",
    prompt="Summarize this video"
)

# Analyze image
result = client.analyze_image(
    image_path="/path/to/image.jpg",
    prompt="What's in this image?"
)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Task Request                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Selector Agent                         │
│  • Analyzes task requirements                               │
│  • Checks provider capabilities                             │
│  • Selects optimal provider                                 │
│  • Provides fallback chain                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│    GLM-4.7  │ │   Kimi K2.5 │ │   Claude    │
│ (Primary)   │ │  (Load Bal.)│ │   Code      │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │                │                │
       │                ▼                │
       │       ┌──────────────┐         │
       │       │ Kimi Keys    │         │
       │       │ 1 CISO + 8   │         │
       │       │  trials      │         │
       │       └──────────────┘         │
       │                                  │
       ▼                                  ▼
┌──────────────────────────────────────────┐
│         API Usage Tracker                │
│  • Tracks tokens & costs                 │
│  • Monitors rate limits                 │
│  • Generates reports                     │
└──────────────────────────────────────────┘
```

## Monitoring & Reporting

### Generate Usage Report

```python
from agents.api_usage_tracker import APIUsageTracker

tracker = APIUsageTracker()
report = tracker.generate_report(days=7)

print(json.dumps(report, indent=2))
```

### Check Alerts

```python
alerts = tracker.check_alerts()
for alert in alerts:
    print(f"[{alert.level.upper()}] {alert.message}")
```

### Provider Status

```python
from agents.api_selector import APISelector

selector = APISelector()
status = selector.get_provider_status()
print(status)
```

## File Structure

```
/opt/blackbox5/
├── config/
│   └── api-keys.yaml              # Main configuration
├── agents/
│   ├── api-selector/              # API selector agent
│   ├── api-usage-tracker/         # Usage tracking
│   ├── kimi-load-balancer/        # Kimi key management
│   └── nvidia-kimi-integration/   # Nvidia integration
├── data/
│   ├── api-usage.db               # SQLite usage database
│   └── multi-api-setup-report.json  # Setup report
├── logs/
│   └── api-selector.log           # Selector logs
└── scripts/
    └── setup_multi_api.py         # Setup script
```

## Success Criteria

✅ **Configuration**
- API keys sorted by priority and capability
- GLM-4.7 set as primary model
- Kimi rotation configured (CISO → trials)
- Nvidia Kimi added and prioritized for video tasks
- Claude Code CLI integrated for complex reasoning
- Automatic API switching based on task requirements

✅ **Functionality**
- Task analyzer automatically selects best API
- API selector agent provides recommendations
- Kimi load balancer smartly rotates keys
- Usage tracker monitors all providers
- Fallback strategies when APIs hit limits
- Dashboard shows all providers and their status

✅ **Performance**
- Faster task completion (use best API for each task)
- Cost optimization (avoid expensive providers unless needed)
- Reliability through key rotation and fallbacks
- More computational power (9 Kimi + Nvidia + Claude)

## Troubleshooting

### No available providers
- Check configuration file exists: `/opt/blackbox5/config/api-keys.yaml`
- Verify API keys are set in environment variables
- Check provider `enabled` status in config

### High error rates
- Check API key validity
- Verify rate limits are not exceeded
- Check network connectivity to API endpoints

### Kimi keys not working
- Verify `KIMI_CISO_KEY` is set
- Check trial keys have not expired
- Review load balancer status for disabled keys

### Nvidia Kimi unavailable
- Ensure `NVIDIA_KIMI_KEY` is set in environment
- Check rate limits (trial key may be limited)
- Verify provider is `enabled` in config

## Next Steps

1. Run setup script: `python3 scripts/setup_multi_api.py`
2. Review setup report: `/opt/blackbox5/data/multi-api-setup-report.json`
3. Set missing API keys based on recommendations
4. Test provider selection with different task types
5. Monitor usage and costs through the tracker

## Support

For issues or questions:
- Check logs: `/opt/blackbox5/logs/api-selector.log`
- Review setup report for recommendations
- Verify API key configuration
- Check provider status and health metrics
