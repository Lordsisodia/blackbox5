"""
Kimi Load Balancer - Enhanced with priority-based rotation and health monitoring
Manages 9 Kimi keys (1 CISO + 8 trials) with intelligent selection.
"""

import os
import yaml
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)


class KeyStatus(Enum):
    """Status of an API key"""
    ACTIVE = "active"
    DEGRADED = "degraded"
    DISABLED = "disabled"
    EXPIRED = "expired"


@dataclass
class KeyMetrics:
    """Performance metrics for a key"""
    request_count: int = 0
    success_count: int = 0
    error_count: int = 0
    tokens_used: int = 0
    total_latency_ms: float = 0.0
    last_used: Optional[datetime] = None
    last_error: Optional[str] = None
    consecutive_failures: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.request_count == 0:
            return 1.0
        return (self.success_count / self.request_count) * 100

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency"""
        if self.request_count == 0:
            return 0.0
        return self.total_latency_ms / self.request_count


@dataclass
class APIKey:
    """Configuration and state for a single API key"""
    id: str
    name: str
    key: str
    priority: int  # Lower is higher priority
    trial: bool
    max_tokens: int
    expires: Optional[str]  # ISO format or None
    assigned_agents: List[str]
    status: KeyStatus = KeyStatus.ACTIVE
    metrics: KeyMetrics = field(default_factory=KeyMetrics)

    def is_expired(self) -> bool:
        """Check if key is expired"""
        if not self.expires:
            return False
        try:
            expiry_date = datetime.fromisoformat(self.expires)
            return datetime.utcnow() > expiry_date
        except:
            return False

    def is_available(self) -> bool:
        """Check if key is available for use"""
        return self.status == KeyStatus.ACTIVE and not self.is_expired()


class KimiLoadBalancer:
    """
    Enhanced load balancer for Kimi API keys.

    Features:
    - Priority-based selection (CISO key first)
    - Health monitoring
    - Trial key management
    - Automatic fallback
    - Usage tracking
    """

    def __init__(self, config_path: str = None):
        """Initialize load balancer"""
        self.config_path = config_path or "/opt/blackbox5/config/api-keys.yaml"
        self.keys: Dict[str, APIKey] = {}
        self.fallback_provider = "glm"  # Fallback to GLM-4.7

        self.load_config()
        self.check_expirations()

    def load_config(self):
        """Load key configuration from YAML"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            kimi_config = config.get('providers', {}).get('kimi', {})

            if not kimi_config.get('enabled', False):
                logger.warning("Kimi provider is disabled in config")
                return

            # Load keys from configuration
            keys_config = kimi_config.get('keys', [])

            for key_config in keys_config:
                key_id = key_config.get('id')
                
                # Get key value, expand shell-style ${VAR:-default} syntax
                key_value = key_config.get('key', '')
                
                # Try environment variable based on key name first
                env_var_name = key_config.get('name', '').upper().replace('-', '_')
                api_key = os.getenv(env_var_name, '')
                
                # If not found, try expanding ${VAR:-default} syntax
                if not api_key and key_value.startswith('${') and key_value.endswith('}'):
                    # Parse ${VAR:-default} format
                    inner = key_value[2:-1]  # Remove ${ and }
                    if ':-' in inner:
                        var_name, default_value = inner.split(':-', 1)
                        api_key = os.getenv(var_name, default_value)
                    elif '-' in inner:
                        var_name, default_value = inner.split('-', 1)
                        api_key = os.getenv(var_name, default_value)
                    else:
                        api_key = os.getenv(inner, '')
                elif not api_key:
                    api_key = key_value

                if not api_key or api_key.startswith('${'):
                    logger.warning(f"No API key found for {key_id}, skipping")
                    continue

                self.keys[key_id] = APIKey(
                    id=key_id,
                    name=key_config.get('name', key_id),
                    key=api_key,
                    priority=key_config.get('priority', 999),
                    trial=key_config.get('trial', False),
                    max_tokens=key_config.get('max_tokens', 0),
                    expires=key_config.get('expires'),
                    assigned_agents=key_config.get('assigned_agents', []),
                    status=KeyStatus.ACTIVE
                )

            logger.info(f"Loaded {len(self.keys)} Kimi keys")

        except Exception as e:
            logger.error(f"Error loading Kimi config: {e}")

    def check_expirations(self):
        """Check and mark expired keys"""
        expired_count = 0
        for key in self.keys.values():
            if key.is_expired():
                key.status = KeyStatus.EXPIRED
                expired_count += 1
                logger.warning(f"Key {key.id} is expired")

        if expired_count > 0:
            logger.warning(f"Disabled {expired_count} expired keys")

    def get_key(
        self,
        agent: str = None,
        required_tokens: int = 0,
        strategy: str = "priority_with_health"
    ) -> Optional[APIKey]:
        """
        Get the best available key.

        Args:
            agent: Agent making the request
            required_tokens: Required token capacity
            strategy: Selection strategy

        Returns:
            Best available APIKey or None if no keys available
        """
        available_keys = [
            k for k in self.keys.values()
            if k.is_available()
        ]

        if not available_keys:
            logger.warning("No available Kimi keys")
            return None

        # Filter by agent assignment if specified
        if agent:
            agent_assigned = [
                k for k in available_keys
                if agent in k.assigned_agents
            ]
            if agent_assigned:
                available_keys = agent_assigned

        # Select based on strategy
        if strategy == "priority_with_health":
            return self._select_priority_with_health(available_keys)
        elif strategy == "least_used":
            return self._select_least_used(available_keys)
        elif strategy == "round_robin":
            return self._select_round_robin(available_keys)
        else:
            return available_keys[0]

    def _select_priority_with_health(self, keys: List[APIKey]) -> APIKey:
        """Select key by priority, preferring healthy ones"""
        # Sort by priority (lower is better), then by success rate
        sorted_keys = sorted(
            keys,
            key=lambda k: (k.priority, -k.metrics.success_rate)
        )
        return sorted_keys[0]

    def _select_least_used(self, keys: List[APIKey]) -> APIKey:
        """Select key with lowest usage"""
        return min(keys, key=lambda k: k.metrics.tokens_used)

    def _select_round_robin(self, keys: List[APIKey]) -> APIKey:
        """Select key in round-robin fashion"""
        # Simple round-robin based on request count
        return min(keys, key=lambda k: k.metrics.request_count)

    def report_usage(
        self,
        key_id: str,
        tokens_used: int = 0,
        latency_ms: float = 0,
        success: bool = True,
        error_message: str = None
    ):
        """Report usage for a key"""
        if key_id not in self.keys:
            logger.warning(f"Unknown key ID: {key_id}")
            return

        key = self.keys[key_id]
        metrics = key.metrics

        metrics.request_count += 1
        metrics.tokens_used += tokens_used
        metrics.total_latency_ms += latency_ms
        metrics.last_used = datetime.utcnow()

        if success:
            metrics.success_count += 1
            metrics.consecutive_failures = 0
        else:
            metrics.error_count += 1
            metrics.consecutive_failures += 1
            metrics.last_error = error_message

            # Disable key if too many consecutive failures
            if metrics.consecutive_failures >= 5:
                key.status = KeyStatus.DISABLED
                logger.warning(f"Disabled key {key_id} after {metrics.consecutive_failures} failures")

        # Update status based on health
        self._update_key_status(key)

    def _update_key_status(self, key: APIKey):
        """Update key status based on metrics"""
        if key.status == KeyStatus.DISABLED or key.status == KeyStatus.EXPIRED:
            return

        # Mark as degraded if high error rate or slow
        if key.metrics.request_count >= 10:
            if key.metrics.success_rate < 90:
                key.status = KeyStatus.DEGRADED
                logger.info(f"Key {key.id} degraded (success rate: {key.metrics.success_rate:.1f}%)")
            elif key.metrics.avg_latency_ms > 5000:
                key.status = KeyStatus.DEGRADED
                logger.info(f"Key {key.id} degraded (latency: {key.metrics.avg_latency_ms:.0f}ms)")
            else:
                key.status = KeyStatus.ACTIVE

    def get_key_status(self) -> Dict[str, Any]:
        """Get status of all keys"""
        return {
            key_id: {
                "name": key.name,
                "priority": key.priority,
                "trial": key.trial,
                "status": key.status.value,
                "is_expired": key.is_expired(),
                "metrics": {
                    "request_count": key.metrics.request_count,
                    "success_rate": round(key.metrics.success_rate, 2),
                    "avg_latency_ms": round(key.metrics.avg_latency_ms, 2),
                    "tokens_used": key.metrics.tokens_used,
                    "last_used": key.metrics.last_used.isoformat() if key.metrics.last_used else None
                }
            }
            for key_id, key in self.keys.items()
        }

    def get_best_key_summary(self) -> Dict[str, Any]:
        """Get summary of best key for dashboard"""
        best_key = self.get_key(strategy="priority_with_health")

        available_count = sum(1 for k in self.keys.values() if k.is_available())

        return {
            "best_key": best_key.id if best_key else None,
            "best_key_name": best_key.name if best_key else None,
            "available_keys": available_count,
            "total_keys": len(self.keys),
            "all_keys_disabled": available_count == 0,
            "fallback_provider": self.fallback_provider if available_count == 0 else None
        }

    def reenable_key(self, key_id: str):
        """Manually re-enable a disabled key"""
        if key_id in self.keys:
            self.keys[key_id].status = KeyStatus.ACTIVE
            self.keys[key_id].metrics.consecutive_failures = 0
            logger.info(f"Re-enabled key {key_id}")

    def get_recommended_rotation(self) -> List[str]:
        """
        Get recommended key rotation order based on health and usage.

        Returns:
            List of key IDs in recommended rotation order
        """
        # Sort by: status (active first), priority, success rate
        sorted_keys = sorted(
            self.keys.values(),
            key=lambda k: (
                0 if k.status == KeyStatus.ACTIVE else 1 if k.status == KeyStatus.DEGRADED else 2,
                k.priority,
                -k.metrics.success_rate
            )
        )

        return [k.id for k in sorted_keys if k.is_available()]

    def export_metrics(self) -> str:
        """Export metrics as JSON for monitoring"""
        return json.dumps(self.get_key_status(), indent=2, default=str)


# CLI for testing
if __name__ == "__main__":
    balancer = KimiLoadBalancer()

    print("=== Kimi Load Balancer Test ===\n")

    # Show all keys
    status = balancer.get_key_status()
    print("All keys:")
    for key_id, info in status.items():
        print(f"  {key_id}: {info['status']} (priority: {info['priority']})")
    print()

    # Get best key
    best_key = balancer.get_key(agent="main")
    if best_key:
        print(f"Best key for 'main' agent: {best_key.name} (id: {best_key.id})")
    else:
        print("No available keys")

    # Get summary
    summary = balancer.get_best_key_summary()
    print(f"\nSummary: {json.dumps(summary, indent=2)}")

    # Recommended rotation
    rotation = balancer.get_recommended_rotation()
    print(f"\nRecommended rotation: {' -> '.join(rotation)}")

    # Simulate usage
    if best_key:
        print(f"\nSimulating usage with {best_key.id}...")
        balancer.report_usage(best_key.id, tokens_used=5000, latency_ms=1234, success=True)
        balancer.report_usage(best_key.id, tokens_used=3000, latency_ms=987, success=True)
        balancer.report_usage(best_key.id, tokens_used=2000, latency_ms=567, success=True)

        updated_status = balancer.get_key_status()
        print(f"Updated metrics for {best_key.id}:")
        print(f"  Requests: {updated_status[best_key.id]['metrics']['request_count']}")
        print(f"  Tokens: {updated_status[best_key.id]['metrics']['tokens_used']}")
        print(f"  Success rate: {updated_status[best_key.id]['metrics']['success_rate']}%")
