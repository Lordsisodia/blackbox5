"""Alert management for BB5 Health Monitor."""

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


@dataclass
class AlertConfig:
    """Configuration for alerts."""
    telegram_enabled: bool = False
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    webhook_enabled: bool = False
    webhook_url: Optional[str] = None
    min_severity: str = "warning"
    cooldown_seconds: int = 300


class AlertManager:
    """Manages alerts with cooldown tracking."""

    def __init__(self, config: AlertConfig):
        self.config = config
        self.cooldowns: Dict[str, datetime] = {}

    def _in_cooldown(self, alert_key: str) -> bool:
        """Check if alert is in cooldown period."""
        if alert_key not in self.cooldowns:
            return False
        elapsed = datetime.now() - self.cooldowns[alert_key]
        return elapsed.total_seconds() < self.config.cooldown_seconds

    def _update_cooldown(self, alert_key: str) -> None:
        """Update cooldown timestamp for alert."""
        self.cooldowns[alert_key] = datetime.now()

    def _should_alert(self, severity: str) -> bool:
        """Check if severity meets minimum threshold."""
        levels = {"info": 0, "warning": 1, "critical": 2}
        return levels.get(severity, 0) >= levels.get(self.config.min_severity, 1)

    def send_alert(self, severity: str, component: str, message: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Send alert if not in cooldown and meets severity threshold."""
        if not self._should_alert(severity):
            return False

        alert_key = f"{severity}:{component}"
        if self._in_cooldown(alert_key):
            logger.debug(f"Alert {alert_key} in cooldown")
            return False

        success = False

        if severity == "critical":
            if self.config.telegram_enabled:
                success = self._send_telegram(message, severity, context) or success
            if self.config.webhook_enabled:
                success = self._send_webhook(message, severity, context) or success
        elif severity == "warning":
            if self.config.telegram_enabled:
                success = self._send_telegram(message, severity, context) or success

        if success:
            self._update_cooldown(alert_key)

        return success

    def _send_telegram(self, message: str, severity: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Send Telegram notification."""
        try:
            import telegram

            bot = telegram.Bot(token=self.config.telegram_bot_token)
            formatted = self._format_telegram(message, severity, context)

            bot.send_message(
                chat_id=self.config.telegram_chat_id,
                text=formatted,
                parse_mode="Markdown"
            )

            logger.info(f"Telegram alert sent: {message[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False

    def _send_webhook(self, message: str, severity: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Send webhook notification."""
        try:
            import requests

            payload = {
                "severity": severity,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "context": context or {},
            }

            response = requests.post(
                self.config.webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Webhook alert sent: {message[:50]}...")
                return True
            else:
                logger.warning(f"Webhook returned {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            return False

    def _format_telegram(self, message: str, severity: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Format message for Telegram."""
        emoji = "🚨" if severity == "critical" else "⚠️"

        lines = [
            f"{emoji} *BB5 ALERT [{severity.upper()}]*",
            "",
            f"*Message:* {message}",
        ]

        if context:
            if "health_score" in context:
                lines.append(f"*Health Score:* {context['health_score']}/100")
            if "queue" in context:
                q = context["queue"]
                lines.append(f"*Queue:* {q.get('pending', 0)} pending, {q.get('in_progress', 0)} in progress")

        lines.extend([
            "",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        ])

        return "\n".join(lines)


def create_alert_manager_from_env() -> AlertManager:
    """Create alert manager from environment variables."""
    config = AlertConfig(
        telegram_enabled=bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
        telegram_bot_token=os.environ.get("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
        webhook_enabled=bool(os.environ.get("WEBHOOK_URL")),
        webhook_url=os.environ.get("WEBHOOK_URL"),
        min_severity=os.environ.get("ALERT_MIN_SEVERITY", "warning"),
        cooldown_seconds=int(os.environ.get("ALERT_COOLDOWN_SECONDS", "300")),
    )
    return AlertManager(config)
