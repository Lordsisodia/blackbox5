# MCP Configuration System

## Overview

The MCP (Model Context Protocol) connection system now uses centralized configuration instead of hardcoded values. This improves security, maintainability, and deployment flexibility.

## Configuration Sources

Configuration is loaded in the following priority order:

1. **Default values** (in `RedisConfig`, `NATSConfig`, `VPSConfig` classes)
2. **YAML configuration file** at `blackbox5/config.yml`
3. **Environment variables** (highest priority)

## Environment Variables

You can override any configuration setting using environment variables:

### Redis Configuration
- `REDIS_HOST` - Redis server hostname (default: `127.0.0.1`)
- `REDIS_PORT` - Redis server port (default: `6379`)
- `REDIS_DB` - Redis database number (default: `0`)
- `REDIS_PASSWORD` - Redis password (optional)
- `REDIS_MAX_CONNECTIONS` - Max connection pool size (default: `50`)
- `REDIS_SOCKET_TIMEOUT` - Socket timeout in seconds (default: `5`)

### NATS Configuration
- `NATS_HOST` - NATS server hostname (default: `127.0.0.1`)
- `NATS_PORT` - NATS server port (default: `4222`)
- `NATS_MAX_RECONNECT_ATTEMPTS` - Max reconnection attempts, -1 for infinite (default: `-1`)
- `NATS_RECONNECT_WAIT` - Wait time between reconnection attempts in seconds (default: `2`)

### VPS Configuration
- `VPS_IP` - VPS IP address (default: `127.0.0.1`)
- `VPS_USER` - SSH username (default: `root`)
- `VPS_SSH_KEY_PATH` - Path to SSH private key (optional)
- `VPS_SSH_PORT` - SSH port (default: `22`)

## YAML Configuration File

Create a `blackbox5/config.yml` file to override defaults:

```yaml
redis:
  host: "127.0.0.1"
  port: 6379
  db: 0
  password: null
  max_connections: 50
  socket_timeout: 5
  socket_connect_timeout: 5

nats:
  host: "127.0.0.1"
  port: 4222
  max_reconnect_attempts: -1
  reconnect_wait: 2
  timeout: 10

vps:
  ip: "127.0.0.1"
  user: "root"
  ssh_key_path: null
  ssh_port: 22
```

## Usage in Code

### Import Configuration Helpers

```python
from engine.connections.mcp import get_redis_config, get_nats_config, get_vps_config

# Get configuration
redis_config = get_redis_config()
nats_config = get_nats_config()
vps_config = get_vps_config()

# Use configuration
import redis
client = redis.Redis(
    host=redis_config.host,
    port=redis_config.port,
    db=redis_config.db
)
```

### Example: Connecting to Redis

```python
from engine.connections.mcp import get_redis_config
import redis

redis_config = get_redis_config()
client = redis.Redis(
    host=redis_config.host,
    port=redis_config.port,
    db=redis_config.db,
    password=redis_config.password,
    max_connections=redis_config.max_connections
)
```

### Example: Connecting to VPS via SSH

```python
from engine.connections.mcp import get_vps_config
import subprocess
import os

vps_config = get_vps_config()
ssh_key = os.path.expanduser(vps_config.ssh_key_path) if vps_config.ssh_key_path else None

result = subprocess.run([
    "ssh", "-i", ssh_key,
    f"{vps_config.user}@{vps_config.ip}",
    "command"
])
```

## Migration Guide

### Before (Hardcoded)

```python
# Old approach - hardcoded values
VPS_IP = "77.42.66.40"
REDIS_HOST = "77.42.66.40"
```

### After (Centralized)

```python
# New approach - centralized configuration
from engine.connections.mcp import get_vps_config, get_redis_config

vps_config = get_vps_config()
redis_config = get_redis_config()

VPS_IP = vps_config.ip
REDIS_HOST = redis_config.host
```

## Benefits

1. **Security**: No hardcoded credentials or IPs in source code
2. **Maintainability**: Single source of truth for configuration
3. **Flexibility**: Easy to change settings for different environments (dev, staging, production)
4. **Deployment**: Can configure via environment variables for containers/cloud deployments
5. **Testing**: Easier to mock configuration for unit tests

## Files Updated

The following files were updated to use the centralized configuration:

### MCP Clients
- `connections/mcp/clients/mcp-openclaw-direct.py`

### MCP Servers
- `connections/mcp/servers/mcp-server-moltbot.py`
- `connections/mcp/servers/mcp-server-moltbot-scheduler.py`
- `connections/mcp/servers/mcp-server-moltbot-simple.py`
- `connections/mcp/servers/mcp-openclaw-ssh-bridge.py`

### MCP Bridges (Archive)
- `connections/mcp/bridges/archive/intelligent-agent-bridge.py`
- `connections/mcp/bridges/archive/mcp-hybrid-bridge.py`
- `connections/mcp/bridges/archive/mcp-moltbot-bridge.py`
- `connections/mcp/bridges/archive/mcp-openclaw-websocket.py`
- `connections/mcp/bridges/archive/mcp-real-moltbot-bridge.py`
- `connections/mcp/bridges/archive/mcp-redis-bridge.py`

## Testing Configuration

To test your configuration:

```python
from engine.connections.mcp import get_redis_config, get_nats_config, get_vps_config

print("Redis Config:", get_redis_config())
print("NATS Config:", get_nats_config())
print("VPS Config:", get_vps_config())
```

## Security Notes

1. Never commit `blackbox5/config.yml` with real credentials to version control
2. Use environment variables for sensitive information (passwords, tokens)
3. Use `.env` files for local development (add to `.gitignore`)
4. Consider using secret management systems for production (HashiCorp Vault, AWS Secrets Manager, etc.)
