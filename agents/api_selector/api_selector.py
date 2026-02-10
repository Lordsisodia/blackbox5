"""
API Selector - Intelligent API Provider Selection for BlackBox5
Analyzes task requirements and selects optimal API provider with fallback support.
"""

import os
import yaml
import json
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import sqlite3
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Task types supported by the API selector"""
    LONG_CONTEXT = "long_context"
    CODING = "coding"
    REASONING = "reasoning"
    VIDEO_PROCESSING = "video_processing"
    VISION = "vision"
    GENERAL = "general"


@dataclass
class ProviderConfig:
    """Configuration for a single API provider"""
    id: str
    name: str
    enabled: bool
    priority: float
    model: str
    api_key: str
    base_url: str
    capabilities: List[str]
    context_window: int
    max_tokens: int
    timeout: int
    costs: Dict[str, Any]
    use_cases: List[str]
    fallback_providers: List[str]
    health_status: str = "active"  # active, degraded, disabled
    last_health_check: Optional[datetime] = None
    error_count: int = 0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0


@dataclass
class ProviderSelection:
    """Result of provider selection"""
    provider: ProviderConfig
    reason: str
    confidence: float
    fallback_chain: List[str] = field(default_factory=list)


class APISelector:
    """
    Intelligent API provider selector for BlackBox5.

    Analyzes task requirements and selects the best provider based on:
    - Required capabilities
    - Provider health and availability
    - Cost optimization
    - Priority and task routing rules
    """

    def __init__(self, config_path: str = None):
        """Initialize API selector with configuration"""
        self.config_path = config_path or "/opt/blackbox5/config/api-keys.yaml"
        self.config: Dict = {}
        self.providers: Dict[str, ProviderConfig] = {}
        self.task_routing: Dict[str, Dict] = {}
        self.usage_db_path = "/opt/blackbox5/data/api-usage.db"

        self.load_config()
        self.init_usage_db()

    def load_config(self):
        """Load API configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)

            # Load providers
            self._load_providers()

            # Load task routing
            self.task_routing = self.config.get('task_routing', {})

            logger.info(f"Loaded configuration with {len(self.providers)} providers")

        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config: {e}")
            raise

    def _load_providers(self):
        """Load provider configurations"""
        providers_config = self.config.get('providers', {})

        # Load GLM provider
        if 'glm' in providers_config:
            glm_config = providers_config['glm']
            if glm_config.get('enabled', False):
                self.providers['glm'] = ProviderConfig(
                    id='glm',
                    name='GLM-4.7',
                    enabled=True,
                    priority=glm_config.get('priority', 1.0),
                    model=glm_config.get('model', 'glm-4.7'),
                    api_key=glm_config.get('api_key', ''),
                    base_url=glm_config.get('base_url', ''),
                    capabilities=glm_config.get('capabilities', []),
                    context_window=glm_config.get('context_window', 2000000),
                    max_tokens=glm_config.get('max_tokens', 100000),
                    timeout=glm_config.get('timeout', 120),
                    costs=glm_config.get('costs', {}),
                    use_cases=glm_config.get('use_cases', []),
                    fallback_providers=glm_config.get('fallback_providers', [])
                )

        # Load Kimi provider with multiple keys
        if 'kimi' in providers_config:
            kimi_config = providers_config['kimi']
            if kimi_config.get('enabled', False):
                # Add main Kimi provider (CISO key first)
                keys = kimi_config.get('keys', [])
                if keys:
                    ciso_key = next((k for k in keys if k.get('priority') == 0), keys[0])
                    self.providers['kimi'] = ProviderConfig(
                        id='kimi',
                        name='Kimi K2.5',
                        enabled=True,
                        priority=kimi_config.get('priority', 0.8),
                        model=kimi_config.get('model', 'moonshot-v1-128k'),
                        api_key=ciso_key.get('key', ''),
                        base_url=kimi_config.get('base_url', ''),
                        capabilities=kimi_config.get('capabilities', []),
                        context_window=kimi_config.get('context_window', 128000),
                        max_tokens=kimi_config.get('max_tokens', 100000),
                        timeout=kimi_config.get('timeout', 120),
                        costs=kimi_config.get('costs', {}),
                        use_cases=kimi_config.get('use_cases', []),
                        fallback_providers=kimi_config.get('fallback_providers', [])
                    )

        # Load Claude Code provider
        if 'claude_code' in providers_config:
            claude_config = providers_config['claude_code']
            if claude_config.get('enabled', False):
                api_key = claude_config.get('api_key', os.getenv('ANTHROPIC_API_KEY', ''))
                self.providers['claude_code'] = ProviderConfig(
                    id='claude_code',
                    name='Claude Code CLI',
                    enabled=bool(api_key),
                    priority=claude_config.get('priority', 0.5),
                    model=claude_config.get('model', 'claude-sonnet-4-5-20250214'),
                    api_key=api_key,
                    base_url=claude_config.get('base_url', ''),
                    capabilities=claude_config.get('capabilities', []),
                    context_window=claude_config.get('context_window', 200000),
                    max_tokens=claude_config.get('max_tokens', 8192),
                    timeout=claude_config.get('timeout', 180),
                    costs=claude_config.get('costs', {}),
                    use_cases=claude_config.get('use_cases', []),
                    fallback_providers=claude_config.get('fallback_providers', [])
                )

        # Load Nvidia Kimi provider
        if 'nvidia_kimi' in providers_config:
            nvidia_config = providers_config['nvidia_kimi']
            if nvidia_config.get('enabled', False):
                api_key = nvidia_config.get('api_key', os.getenv('NVIDIA_KIMI_KEY', ''))
                self.providers['nvidia_kimi'] = ProviderConfig(
                    id='nvidia_kimi',
                    name='Nvidia Kimi',
                    enabled=bool(api_key),
                    priority=nvidia_config.get('priority', 0.4),
                    model=nvidia_config.get('model', 'kimi-k2.5'),
                    api_key=api_key,
                    base_url=nvidia_config.get('base_url', ''),
                    capabilities=nvidia_config.get('capabilities', []),
                    context_window=nvidia_config.get('context_window', 128000),
                    max_tokens=nvidia_config.get('max_tokens', 100000),
                    timeout=nvidia_config.get('timeout', 180),
                    costs=nvidia_config.get('costs', {}),
                    use_cases=nvidia_config.get('use_cases', []),
                    fallback_providers=nvidia_config.get('fallback_providers', [])
                )

        # Sort by priority (lower is higher priority)
        self.providers = dict(sorted(
            self.providers.items(),
            key=lambda x: x[1].priority
        ))

    def init_usage_db(self):
        """Initialize usage tracking database"""
        Path(self.usage_db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.usage_db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                provider TEXT NOT NULL,
                agent TEXT,
                task_type TEXT,
                tokens_used INTEGER,
                request_duration_ms INTEGER,
                success BOOLEAN,
                error_message TEXT
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_provider ON api_usage(provider);
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON api_usage(timestamp);
        ''')

        conn.commit()
        conn.close()

    def select_provider(
        self,
        task_type: str = "general",
        context_length: int = 0,
        required_capabilities: List[str] = None,
        criticality: str = "medium",
        agent: str = None
    ) -> ProviderSelection:
        """
        Select the optimal provider for a task.

        Args:
            task_type: Type of task (long_context, coding, reasoning, etc.)
            context_length: Estimated context length in tokens
            required_capabilities: List of required capabilities
            criticality: Task criticality (low, medium, high)
            agent: Agent making the request

        Returns:
            ProviderSelection with selected provider and reasoning
        """
        required_capabilities = required_capabilities or []

        logger.info(f"Selecting provider for task_type={task_type}, criticality={criticality}")

        # Get routing configuration for task type
        task_config = self.task_routing.get(task_type, {})
        provider_ids = task_config.get('providers', list(self.providers.keys()))
        strategy = task_config.get('strategy', 'availability_first')

        # Filter providers by required capabilities
        capable_providers = []
        for provider_id in provider_ids:
            if provider_id not in self.providers:
                continue
            provider = self.providers[provider_id]

            # Check if enabled and healthy
            if not provider.enabled or provider.health_status == "disabled":
                continue

            # Check if has required capabilities
            if required_capabilities:
                has_capabilities = all(
                    cap in provider.capabilities
                    for cap in required_capabilities
                )
                if not has_capabilities:
                    continue

            # Check context window
            if context_length > 0 and context_length > provider.context_window:
                continue

            capable_providers.append(provider)

        if not capable_providers:
            logger.warning(f"No capable providers found, falling back to default")
            # Fall back to any enabled provider
            capable_providers = [
                p for p in self.providers.values()
                if p.enabled and p.health_status != "disabled"
            ]

        if not capable_providers:
            raise RuntimeError("No available API providers")

        # Select based on strategy
        selected_provider = self._select_by_strategy(
            capable_providers,
            strategy,
            criticality
        )

        # Build fallback chain
        fallback_chain = [
            p.id for p in capable_providers
            if p.id != selected_provider.id
        ]

        # Determine reasoning
        reason = self._generate_reasoning(
            selected_provider,
            task_type,
            strategy,
            criticality
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            selected_provider,
            capable_providers
        )

        logger.info(f"Selected provider: {selected_provider.id} ({reason})")

        return ProviderSelection(
            provider=selected_provider,
            reason=reason,
            confidence=confidence,
            fallback_chain=fallback_chain
        )

    def _select_by_strategy(
        self,
        providers: List[ProviderConfig],
        strategy: str,
        criticality: str
    ) -> ProviderConfig:
        """Select provider based on strategy"""
        if strategy == "cost_optimized":
            # Prefer cheaper providers for non-critical tasks
            if criticality != "high":
                providers = sorted(
                    providers,
                    key=lambda p: p.costs.get('input_per_million', 1000)
                )
            return providers[0]

        elif strategy == "quality_first":
            # Prefer higher priority (better quality) providers
            return min(providers, key=lambda p: p.priority)

        elif strategy == "specialized_first":
            # Prefer providers with specialized capabilities
            for provider in providers:
                if 'video_processing' in provider.capabilities:
                    return provider
            return providers[0]

        else:  # availability_first or default
            # Prefer healthy providers, then by priority
            healthy_providers = [
                p for p in providers
                if p.health_status == "active"
            ]
            if healthy_providers:
                return min(healthy_providers, key=lambda p: p.priority)
            return providers[0]

    def _generate_reasoning(
        self,
        provider: ProviderConfig,
        task_type: str,
        strategy: str,
        criticality: str
    ) -> str:
        """Generate human-readable reasoning for selection"""
        reasons = []

        if task_type != "general":
            reasons.append(f"matched task type '{task_type}'")

        if provider.health_status == "active":
            reasons.append("healthy status")

        if criticality == "high" and provider.priority < 1.0:
            reasons.append("high capability for critical task")

        if strategy == "cost_optimized":
            reasons.append("cost-optimized selection")
        elif strategy == "quality_first":
            reasons.append("quality-prioritized selection")

        return ", ".join(reasons) or "available provider"

    def _calculate_confidence(
        self,
        selected: ProviderConfig,
        capable: List[ProviderConfig]
    ) -> float:
        """Calculate confidence in selection (0.0 to 1.0)"""
        # Base confidence on health status
        base_confidence = {
            "active": 0.9,
            "degraded": 0.7,
            "disabled": 0.0
        }.get(selected.health_status, 0.5)

        # Reduce if many capable alternatives (less clear winner)
        if len(capable) > 3:
            base_confidence *= 0.9
        elif len(capable) == 1:
            base_confidence = 1.0  # Only option

        return round(base_confidence, 2)

    def track_usage(
        self,
        provider_id: str,
        agent: str,
        task_type: str,
        tokens_used: int,
        duration_ms: int,
        success: bool,
        error_message: str = None
    ):
        """Track API usage for analytics"""
        try:
            conn = sqlite3.connect(self.usage_db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO api_usage
                (provider, agent, task_type, tokens_used, request_duration_ms, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (provider_id, agent, task_type, tokens_used, duration_ms, success, error_message))

            conn.commit()
            conn.close()

            # Update provider health stats
            if provider_id in self.providers:
                provider = self.providers[provider_id]
                if success:
                    # Update moving average latency
                    if provider.avg_latency_ms == 0:
                        provider.avg_latency_ms = duration_ms
                    else:
                        provider.avg_latency_ms = (
                            provider.avg_latency_ms * 0.9 + duration_ms * 0.1
                        )
                else:
                    provider.error_count += 1

        except Exception as e:
            logger.error(f"Error tracking usage: {e}")

    def get_provider_status(self) -> Dict[str, Dict]:
        """Get status of all providers"""
        return {
            provider_id: {
                "name": provider.name,
                "enabled": provider.enabled,
                "health_status": provider.health_status,
                "error_count": provider.error_count,
                "avg_latency_ms": round(provider.avg_latency_ms, 2),
                "capabilities": provider.capabilities
            }
            for provider_id, provider in self.providers.items()
        }

    def get_usage_stats(
        self,
        provider: str = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get usage statistics for analytics"""
        conn = sqlite3.connect(self.usage_db_path)
        cursor = conn.cursor()

        query = '''
            SELECT
                provider,
                COUNT(*) as requests,
                SUM(tokens_used) as total_tokens,
                AVG(request_duration_ms) as avg_duration,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed
            FROM api_usage
            WHERE timestamp >= datetime('now', ?)
        '''

        params = [f'-{days} days']

        if provider:
            query += ' AND provider = ?'
            params.append(provider)

        query += ' GROUP BY provider'

        cursor.execute(query, params)
        rows = cursor.fetchall()

        conn.close()

        stats = {}
        for row in rows:
            provider_id, requests, total_tokens, avg_duration, successful, failed = row
            stats[provider_id] = {
                "requests": requests,
                "total_tokens": total_tokens or 0,
                "avg_duration_ms": round(avg_duration or 0, 2),
                "success_rate": round((successful / requests * 100) if requests > 0 else 0, 2),
                "error_rate": round((failed / requests * 100) if requests > 0 else 0, 2)
            }

        return stats


# CLI interface for testing
if __name__ == "__main__":
    selector = APISelector()

    # Test selections
    print("\n=== API Selector Test ===\n")

    test_cases = [
        ("coding", ["coding"], "high"),
        ("long_context", ["long_context"], "medium"),
        ("video_processing", ["video_processing"], "medium"),
        ("general", [], "low"),
    ]

    for task_type, caps, criticality in test_cases:
        selection = selector.select_provider(
            task_type=task_type,
            required_capabilities=caps,
            criticality=criticality
        )

        print(f"Task: {task_type} (criticality={criticality})")
        print(f"  Selected: {selection.provider.name} (priority={selection.provider.priority})")
        print(f"  Reason: {selection.reason}")
        print(f"  Confidence: {selection.confidence}")
        print(f"  Fallbacks: {', '.join(selection.fallback_chain) or 'none'}")
        print()

    # Show provider status
    print("=== Provider Status ===")
    status = selector.get_provider_status()
    for provider_id, info in status.items():
        print(f"{provider_id}: {info['health_status']} (errors: {info['error_count']})")
