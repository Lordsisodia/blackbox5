"""
MCP (Model Context Protocol) Connection Configuration

Provides centralized configuration for MCP servers, clients, and bridges.
"""

from ...interface.config import load_config

# Singleton configuration instance
_config = None


def get_mcp_config():
    """
    Get MCP configuration.

    Returns:
        Config object with vps, redis, nats settings
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config


def get_vps_config():
    """Get VPS connection configuration."""
    return get_mcp_config().vps


def get_redis_config():
    """Get Redis connection configuration."""
    return get_mcp_config().redis


def get_nats_config():
    """Get NATS connection configuration."""
    return get_mcp_config().nats
