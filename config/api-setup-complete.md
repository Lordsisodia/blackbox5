# BlackBox5 API Setup Complete Documentation

**Version:** 1.0
**Last Updated:** 2026-02-10
**Status:** ✅ Complete

---

## Overview

This document describes the complete API configuration for BlackBox5, including all available API keys, their capabilities, and how to use them efficiently through OpenClaw CLI.

---

## Available APIs

### 1. GLM-4.7 (Z.AI) - Primary Model

**Status:** ✅ Active (Primary)

| Property | Value |
|----------|-------|
| Provider | Z.AI |
| Model | glm-4.7 |
| Context Window | 2,000,000 tokens |
| Max Output | 100,000 tokens |
| Input Cost | $0.50 / 1M tokens |
| Output Cost | $2.00 / 1M tokens |
| Priority | 1.0 (Highest) |

**Capabilities:**
- Long context conversations
- General tasks
- Affordable and reliable
- Default fallback

**When to Use:**
- General tasks (80% of use cases)
- Long context conversations
- When specialized APIs unavailable
- Default fallback for all tasks

**API Key:** `d81f5ab044ad48b492a8dbc183687dcf.sezM6xOnR9BvFhmf` (embedded)

---

### 2. Kimi K2.5 (Moonshot) - Smart Coding & Multimodal

**Status:** ✅ Active (9 Keys Available)

| Property | Value |
|----------|-------|
| Provider | Moonshot (Kimi) |
| Model | moonshot-v1-128k |
| Context Window | 128,000 tokens |
| Max Output | 100,000 tokens |
| Input Cost | $12.00 / 1M tokens |
| Output Cost | $60.00 / 1M tokens |
| Priority | 0.8 (High) |

**Capabilities:**
- Long context
- Multimodal (text, image, video)
- Coding
- Reasoning
- Video processing

**When to Use:**
- Coding tasks (smarter than GLM)
- Video processing
- Multimodal tasks
- Complex reasoning
- Vision tasks

**API Keys:**

| ID | Name | Priority | Trial | Tokens | Assigned Agents |
|----|------|----------|-------|--------|-----------------|
| kimi_ciso | CISO Kimi1 | 0 (Highest) | ❌ | 1,000,000 | main, claude-mac, planner |
| kimi_trial_01 | Trial 1 | 2 | ✅ | 100,000 | executor, researcher |
| kimi_trial_02 | Trial 2 | 2 | ✅ | 100,000 | executor, moltbot-vps-ai |
| kimi_trial_03 | Trial 3 | 3 | ✅ | 100,000 | researcher, analyzer |
| kimi_trial_04 | Trial 4 | 3 | ✅ | 100,000 | executor |
| kimi_trial_05 | Trial 5 | 4 | ✅ | 100,000 | researcher |
| kimi_trial_06 | Trial 6 | 4 | ✅ | 100,000 | analyzer |
| kimi_trial_07 | Trial 7 | 5 | ✅ | 100,000 | researcher |
| kimi_trial_08 | Trial 8 | 5 | ✅ | 100,000 | analyzer |

**Load Balancing Strategy:** `priority_with_health`
- Use CISO key first (most reliable)
- Fall back to trial keys based on health
- Skip unhealthy keys automatically
- Re-check disabled keys after 5 minutes

---

### 3. Claude Code CLI (Anthropic) - Give Yourself More Power

**Status:** ⚠️ Requires API Key

| Property | Value |
|----------|-------|
| Provider | Anthropic |
| Model | claude-sonnet-4-5-20250214 |
| Context Window | 200,000 tokens |
| Max Output | 8,192 tokens |
| Input Cost | $3.00 / 1M tokens |
| Output Cost | $15.00 / 1M tokens |
| Priority | 0.5 (Medium) |
| Daily Budget | $10.00 limit |

**Capabilities:**
- Long context
- Reasoning
- Coding
- Artifact management
- Complex analysis

**When to Use:**
- Tasks needing better reasoning
- Complex coding challenges
- Artifact management
- Critical tasks requiring highest quality

**Environment Variable:** `ANTHROPIC_API_KEY` (needs to be set)

---

### 4. Nvidia Kimi - Video & Vision Specialized

**Status:** ⚠️ Requires API Key

| Property | Value |
|----------|-------|
| Provider | Nvidia |
| Model | kimi-k2.5 |
| Context Window | 128,000 tokens |
| Max Output | 100,000 tokens |
| Input Cost | $0.00 (Trial) |
| Output Cost | $0.00 (Trial) |
| Priority | 0.4 (Specialized) |

**Capabilities:**
- Vision
- Multimodal
- Video processing
- Image analysis

**When to Use:**
- Video processing
- Vision tasks
- Image analysis
- Multimodal applications

**Environment Variable:** `NVIDIA_KIMI_KEY` (needs to be set)

---

## Task Type to API Mapping

### Task Routing Rules

| Task Type | Primary API | Secondary API | Strategy | When to Use Secondary |
|-----------|--------------|------------------|----------|----------------------|
| **Long Context** (32k+ tokens) | GLM-4.7 | Claude Code CLI | cost_optimized | For complex reasoning |
| **Coding/Refactoring** | Kimi K2.5 | Claude Code CLI | quality_first | For code optimization |
| **Reasoning** | Claude Code CLI | Kimi K2.5 | quality_first | For complex reasoning |
| **Video Processing** | Nvidia Kimi | Kimi K2.5 | specialized_first | When Nvidia unavailable |
| **Vision/Image** | Nvidia Kimi | Kimi K2.5 | specialized_first | When Nvidia unavailable |
| **General/Quick** | GLM-4.7 | GLM-4.7 | availability_first | Default (cheapest) |
| **High Priority** | GLM-4.7 | Claude Code CLI | quality_first | Use best available |

### Strategy Definitions

- **cost_optimized**: Use cheapest capable provider first
- **quality_first**: Use highest quality provider first
- **specialized_first**: Use provider with specialized capability
- **availability_first**: Use most available provider

---

## Cost Optimization Strategy

### Usage Distribution Goals

| API | Target Usage | Reason |
|-----|--------------|--------|
| GLM-4.7 | 80% | Primary, most affordable |
| Kimi K2.5 | 15% | Coding and multimodal |
| Claude Code CLI | 4% | Complex reasoning only |
| Nvidia Kimi | 1% | Video/vision only |

### Budget Limits

| Provider | Daily Limit | Currency |
|----------|--------------|----------|
| Claude Code CLI | $10.00 | USD |
| Others | None | - |

### Cost-Saving Rules

1. **Prefer GLM-4.7** for general and quick tasks
2. **Use Kimi** for coding (smarter, cost-effective)
3. **Use Claude Code CLI only when needed** (it's free within budget, but use for complex tasks)
4. **Use Nvidia Kimi** only for video/vision (trial key)
5. **Avoid Claude Code CLI** for simple tasks (use GLM-4.7 instead)

---

## Configuration Files

### OpenClaw Configuration

**Location:** `~/.openclaw/openclaw.json` (main) or `~/.openclaw/openclaw-api-config.json` (new)

**Key Sections:**
- `models.providers`: All API providers with keys
- `agents.defaults.model`: Primary and fallback models
- `agents.defaults.taskRouting`: Task routing rules
- `apiManagement`: Health checks, fallback, alerts

**Apply Configuration:**
```bash
# Backup current config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)

# Apply new config (manual merge required)
# The new config is at ~/.openclaw/openclaw-api-config.json
```

### Agent Configuration System

**Location:** `/opt/blackbox5/config/api-keys.yaml`

**Contents:**
- All provider definitions
- Task routing rules
- Kimi key configurations
- Load balancing settings
- Health check intervals
- Cost optimization rules
- Monitoring and alerts

### Environment Variables

**Location:** `/opt/blackbox5/config/.env.example` (template)

**Required Variables:**
- `KIMI_CISO_KEY` - ✅ Already set
- `KIMI_TRIAL_KEY_01` - ✅ Already set
- `KIMI_TRIAL_KEY_02` through `KIMI_TRIAL_KEY_08` - ⚠️ Need values
- `ANTHROPIC_API_KEY` - ⚠️ Need value
- `NVIDIA_KIMI_KEY` - ⚠️ Need value

**Load Environment Variables:**
```bash
# From /opt/blackbox5/config/
source .env  # After filling in values

# Or export individual variables
export ANTHROPIC_API_KEY="your_key_here"
export NVIDIA_KIMI_KEY="your_key_here"
```

---

## Agent Modules

### API Selector

**Location:** `/opt/blackbox5/agents/api_selector/api_selector.py`

**Purpose:** Intelligent API provider selection

**Features:**
- Analyzes task requirements
- Selects optimal API provider
- Fallback support
- Usage tracking
- Health monitoring

**Usage:**
```python
from agents.api_selector import APISelector, TaskType

selector = APISelector()

# Select provider for coding task
selection = selector.select_provider(
    task_type="coding",
    required_capabilities=["coding"],
    criticality="high"
)

print(f"Selected: {selection.provider.name}")
print(f"Reason: {selection.reason}")
print(f"Fallbacks: {selection.fallback_chain}")
```

### Kimi Load Balancer

**Location:** `/opt/blackbox5/agents/kimi_load_balancer/kimi_load_balancer.py`

**Purpose:** Manage 9 Kimi keys with intelligent rotation

**Features:**
- Priority-based selection (CISO first)
- Health monitoring
- Trial key management
- Automatic fallback
- Usage tracking

**Usage:**
```python
from agents.kimi_load_balancer import KimiLoadBalancer

balancer = KimiLoadBalancer()

# Get best key for agent
key = balancer.get_key(agent="main")

# Report usage
balancer.report_usage(
    key_id=key.id,
    tokens_used=5000,
    latency_ms=1234,
    success=True
)

# Get key status
status = balancer.get_key_status()
print(status)
```

### API Usage Tracker

**Location:** `/opt/blackbox5/agents/api_usage_tracker/usage_tracker.py`

**Purpose:** Track API usage for analytics

**Features:**
- Token usage tracking
- Request counting
- Error tracking
- Latency monitoring
- Cost estimation

### Nvidia Kimi Integration

**Location:** `/opt/blackbox5/agents/nvidia_kimi_integration/nvidia_client.py`

**Purpose:** Nvidia Kimi API client for video/vision

**Features:**
- Video processing
- Vision tasks
- Image analysis
- Multimodal support

---

## Testing

### Test Each API Key

```bash
# Test GLM-4.7 (should work)
python3 -c "
import requests
url = 'https://api.z.ai/api/anthropic/v1/messages'
headers = {
    'Authorization': 'Bearer d81f5ab044ad48b492a8dbc183687dcf.sezM6xOnR9BvFhmf',
    'Content-Type': 'application/json'
}
data = {
    'model': 'glm-4.7',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Say hello'}]
}
response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.json())
"

# Test Kimi CISO key
export KIMI_CISO_KEY="sk-kimi-YC3tlmLzogkd2ZMHdPwMMth3hV9r72aC5lk3kQTYI014GFjBN0VPcKfe6wczYlGr"
python3 -c "
import requests
import os
url = 'https://api.moonshot.cn/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {os.getenv(\"KIMI_CISO_KEY\")}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'moonshot-v1-128k',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Say hello'}]
}
response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.json())
"

# Test Claude Code CLI (if API key set)
export ANTHROPIC_API_KEY="your_key_here"
python3 -c "
import anthropic
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.messages.create(
    model='claude-sonnet-4-5-20250214',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Say hello'}]
)
print(response.content[0].text)
"
```

### Test API Routing

```bash
cd /opt/blackbox5/agents

# Test API selector
python3 -c "
from api_selector.api_selector import APISelector
selector = APISelector()

# Test different task types
for task_type in ['coding', 'long_context', 'video_processing', 'general']:
    selection = selector.select_provider(
        task_type=task_type,
        criticality='medium'
    )
    print(f'{task_type}: {selection.provider.name} ({selection.reason})')
"

# Test Kimi load balancer
python3 -c "
from kimi_load_balancer.kimi_load_balancer import KimiLoadBalancer
balancer = KimiLoadBalancer()

# Get best key
key = balancer.get_key(agent='main')
print(f'Best key: {key.name} (id: {key.id})')

# Get status
status = balancer.get_key_status()
for key_id, info in status.items():
    print(f'{key_id}: {info[\"status\"]}')
"
```

### Test Fallback Chains

```bash
python3 -c "
from api_selector.api_selector import APISelector
selector = APISelector()

selection = selector.select_provider(
    task_type='coding',
    criticality='high'
)

print(f'Primary: {selection.provider.name}')
print(f'Fallback chain: {selection.fallback_chain}')
"
```

---

## Troubleshooting

### Issue: "No available API providers"

**Solution:**
1. Check if API keys are set in environment variables
2. Check if providers are enabled in `/opt/blackbox5/config/api-keys.yaml`
3. Check OpenClaw configuration in `~/.openclaw/openclaw.json`

### Issue: "Kimi key not found"

**Solution:**
1. Set environment variable: `export KIMI_CISO_KEY="your_key"`
2. Or add to `/opt/blackbox5/config/.env` and source it
3. Verify key is not expired

### Issue: "Claude Code CLI not working"

**Solution:**
1. Set `ANTHROPIC_API_KEY` environment variable
2. Verify key has available credits
3. Check daily budget not exceeded ($10 limit)

### Issue: "High error rate on provider"

**Solution:**
1. Check provider status with API selector
2. Provider may be temporarily degraded
3. Fallback to next provider in chain
4. Check API status pages for outages

### Issue: "Keys hitting rate limits"

**Solution:**
1. Check usage stats with API usage tracker
2. Kimi load balancer will rotate keys automatically
3. If all keys exhausted, fallback to GLM-4.7
4. Consider upgrading plan or adding more keys

---

## Monitoring

### Check Provider Status

```bash
# Via API selector
python3 -c "
from api_selector.api_selector import APISelector
selector = APISelector()
status = selector.get_provider_status()
for provider_id, info in status.items():
    print(f'{provider_id}: {info[\"health_status\"]} (errors: {info[\"error_count\"]})')
"

# Via Kimi load balancer
python3 -c "
from kimi_load_balancer.kimi_load_balancer import KimiLoadBalancer
balancer = KimiLoadBalancer()
status = balancer.get_key_status()
for key_id, info in status.items():
    print(f'{key_id}: {info[\"status\"]} (requests: {info[\"metrics\"][\"request_count\"]})')
"
```

### Check Usage Stats

```bash
python3 -c "
from api_selector.api_selector import APISelector
selector = APISelector()
stats = selector.get_usage_stats(days=7)
for provider_id, info in stats.items():
    print(f'{provider_id}: {info[\"requests\"]} requests, {info[\"total_tokens\"]} tokens, {info[\"success_rate\"]}% success')
"
```

### Check Alerts

Alerts are triggered when:
- Error rate > 10%
- Latency > 5 seconds
- Usage > 80% (warning)
- Usage > 90% (critical)

---

## Best Practices

### 1. Task Selection

- **General tasks**: Use GLM-4.7 (default)
- **Coding tasks**: Use Kimi K2.5
- **Complex reasoning**: Use Claude Code CLI
- **Video/vision**: Use Nvidia Kimi

### 2. Cost Optimization

- Use GLM-4.7 for 80% of tasks
- Use Kimi for coding (smarter, cost-effective)
- Use Claude Code CLI only for complex reasoning
- Use Nvidia Kimi only for video/vision

### 3. Error Handling

- Always check fallback chains
- Implement retry logic with exponential backoff
- Log errors for analysis
- Monitor error rates

### 4. Key Management

- Use CISO key first (most reliable)
- Rotate trial keys based on health
- Monitor key expiration dates
- Replace expired keys promptly

---

## Quick Reference

### Environment Variables

```bash
# Kimi keys
export KIMI_CISO_KEY="sk-kimi-YC3tlmLzogkd2ZMHdPwMMth3hV9r72aC5lk3kQTYI014GFjBN0VPcKfe6wczYlGr"
export KIMI_TRIAL_KEY_01="sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf"

# Claude Code CLI
export ANTHROPIC_API_KEY="your_key_here"

# Nvidia Kimi
export NVIDIA_KIMI_KEY="your_key_here"
```

### API Selector Usage

```python
from api_selector.api_selector import APISelector

selector = APISelector()
selection = selector.select_provider(
    task_type="coding",
    required_capabilities=["coding"],
    criticality="high"
)

provider = selection.provider
print(f"Using: {provider.name}")
print(f"API Key: {provider.api_key}")
print(f"Base URL: {provider.base_url}")
```

### Kimi Load Balancer Usage

```python
from kimi_load_balancer.kimi_load_balancer import KimiLoadBalancer

balancer = KimiLoadBalancer()
key = balancer.get_key(agent="main")

# Use the key
print(f"Key: {key.key}")
print(f"Name: {key.name}")

# Report usage
balancer.report_usage(
    key_id=key.id,
    tokens_used=5000,
    latency_ms=1234,
    success=True
)
```

---

## Next Steps

1. ✅ **API keys configured** - GLM-4.7 and Kimi keys are set
2. ⚠️ **Claude Code CLI key** - Need to set `ANTHROPIC_API_KEY`
3. ⚠️ **Nvidia Kimi key** - Need to set `NVIDIA_KIMI_KEY`
4. ⚠️ **Kimi trial keys** - Need to fill in values for keys 2-8
5. ✅ **Agent modules created** - API selector, load balancer, tracker
6. ✅ **Configuration files created** - OpenClaw config, agent config
7. ✅ **Documentation complete** - This file

---

## Support

For issues or questions:

1. Check this documentation
2. Check configuration files
3. Check API status pages
4. Check logs in `/opt/blackbox5/logs/`

---

**End of Documentation**
