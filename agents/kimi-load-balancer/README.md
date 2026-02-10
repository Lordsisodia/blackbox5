# Kimi Load Balancer (Enhanced)

## Purpose
Intelligent load balancer for Kimi API keys with priority-based rotation (CISO key first, then trials).

## Features
- Priority-based key selection (CISO → trials by priority)
- Health monitoring (response time, error rate)
- Trial key management (track expiration, disable when expired)
- Smart rotation based on token efficiency
- Automatic fallback to GLM-4.7 when all Kimi keys exhausted
- Usage tracking per key

## Configuration
Uses `/opt/blackbox5/config/api-keys.yaml` for key configuration.

## Usage
```python
from agents.kimi_load_balancer import KimiLoadBalancer

balancer = KimiLoadBalancer()

# Get best key
key = balancer.get_key(agent="main")

# Report usage
balancer.report_usage(key_id, tokens_used=5000, success=True)

# Get key status
status = balancer.get_key_status()
```
