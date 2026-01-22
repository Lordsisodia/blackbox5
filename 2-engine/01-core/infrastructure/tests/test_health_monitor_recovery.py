"""
Tests for HealthMonitor automatic recovery and alerting.

Tests that unhealthy services are automatically recovered, alerts are sent,
and recovery attempts are tracked properly.
"""

import pytest
import asyncio
import sys
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from typing import List
from pathlib import Path

# Add the 2-engine/01-core directory to the path
engine_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(engine_path))

from infrastructure.health import (
    HealthMonitor,
    HealthStatus,
    HealthCheck,
    SystemHealth
)


# Test Fixtures

@pytest.fixture
def health_monitor():
    """Create a HealthMonitor instance with auto-recovery enabled."""
    return HealthMonitor(service_registry=None, auto_recover=True)


@pytest.fixture
def health_monitor_no_recovery():
    """Create a HealthMonitor instance with auto-recovery disabled."""
    return HealthMonitor(service_registry=None, auto_recover=False)


@pytest.fixture
def mock_alert_handler():
    """Create a mock alert handler to capture alerts."""
    handler = Mock()
    handler.reset_mock()
    return handler


# Test: Automatic Recovery

class TestAutomaticRecovery:
    """Test automatic service recovery functionality."""

    @pytest.mark.asyncio
    async def test_flaky_service_auto_recovery(self, health_monitor):
        """Test that a flaky service (fails then recovers) is automatically handled."""

        # Create a service that fails first 3 checks, then recovers
        fail_count = 0

        def flaky_check():
            nonlocal fail_count
            fail_count += 1
            return fail_count > 3

        # Register the flaky service
        health_monitor.register_check(
            "flaky",
            flaky_check,
            interval=1,
            timeout=1
        )

        # Run health checks - should detect failures
        await health_monitor.check_all()

        health = health_monitor.get_current_health()
        assert health['checks']['flaky']['consecutive_failures'] == 1
        assert health['checks']['flaky']['healthy'] == False

        # Run again - still failing
        await health_monitor.check_all()
        health = health_monitor.get_current_health()
        assert health['checks']['flaky']['consecutive_failures'] == 2

        # Run again - should attempt recovery (threshold = 3)
        await health_monitor.check_all()
        health = health_monitor.get_current_health()
        assert health['checks']['flaky']['consecutive_failures'] == 3

        # Run again - should recover now
        await health_monitor.check_all()
        health = health_monitor.get_current_health()
        assert health['checks']['flaky']['healthy'] == True
        # consecutive_failures reset to 0 after successful check
        assert health['checks']['flaky']['consecutive_failures'] == 0

    @pytest.mark.asyncio
    async def test_permanent_failure_max_retries(self, health_monitor, mock_alert_handler):
        """Test that permanently failing services trigger alerts after max retries."""

        # Create a service that always fails
        def failing_check():
            return False

        # Register alert handler
        health_monitor.add_alert_handler(mock_alert_handler)

        # Register the failing service
        health_monitor.register_check(
            "failing",
            failing_check,
            interval=1,
            timeout=1
        )

        # Fail enough times to trigger recovery attempts and exceed max retries
        # Each 3 failures = 1 recovery attempt. Need 10 failures to get past max_retries=3
        for i in range(10):
            await health_monitor.check_all()

            recovery_status = health_monitor.get_recovery_status()
            attempts = recovery_status.get('services', {}).get('failing', {}).get('attempts', 0)

            # Should stop attempting after max_retries (3)
            if attempts >= 3:
                break

        # Verify max retries reached
        recovery_status = health_monitor.get_recovery_status()
        assert recovery_status['services']['failing']['attempts'] == 3
        assert recovery_status['services']['failing']['can_recover'] == False

        # Verify alert was sent
        assert mock_alert_handler.called
        alerts = [call[0][0] for call in mock_alert_handler.call_args_list]

        # Should have max_retries_exceeded alert
        critical_alerts = [a for a in alerts if a.get('reason') == 'max_retries_exceeded']
        assert len(critical_alerts) > 0
        assert critical_alerts[0]['severity'] == 'critical'

    @pytest.mark.asyncio
    async def test_custom_recovery_function(self, health_monitor):
        """Test that custom recovery functions are called."""

        recovery_called = []

        def custom_recovery():
            recovery_called.append(True)
            return True

        def failing_check():
            return False

        # Register with custom recovery function
        health_monitor.register_check(
            "custom-recover",
            failing_check,
            interval=1,
            timeout=1,
            recovery_func=custom_recovery
        )

        # Trigger recovery (fail 3 times)
        for _ in range(3):
            await health_monitor.check_all()

        # Verify custom recovery was called
        assert len(recovery_called) > 0
        recovery_status = health_monitor.get_recovery_status()
        assert recovery_status['services']['custom-recover']['attempts'] == 0  # Reset on success

    @pytest.mark.asyncio
    async def test_recovery_disabled(self, health_monitor_no_recovery):
        """Test that recovery doesn't happen when auto_recover=False."""

        def failing_check():
            return False

        health_monitor_no_recovery.register_check(
            "failing",
            failing_check,
            interval=1,
            timeout=1
        )

        # Fail multiple times
        for _ in range(5):
            await health_monitor_no_recovery.check_all()

        # Should not have any recovery attempts
        recovery_status = health_monitor_no_recovery.get_recovery_status()
        assert len(recovery_status['services']) == 0

    @pytest.mark.asyncio
    async def test_service_recovery_resets_on_health(self, health_monitor):
        """Test that recovery attempts reset when service becomes healthy."""

        # Use enough states to ensure recovery attempts fail
        # Need: 3 initial failures + 3 recovery retries = 6 states minimum
        health_states = [False, False, False, False, False, False, True]  # 6 failures, then recovers
        state_index = [0]

        def recovering_check():
            idx = state_index[0]
            state_index[0] += 1
            if idx < len(health_states):
                return health_states[idx]
            return True

        health_monitor.register_check(
            "recovering",
            recovering_check,
            interval=1,
            timeout=1
        )

        # Fail 6 times to trigger recovery attempts
        # 3 failures = 1st recovery attempt (retries check #4)
        # 4 failures = 2nd recovery attempt (retries check #5)
        # 5 failures = 3rd recovery attempt (retries check #6)
        # 6 failures = max retries exceeded
        for i in range(6):
            await health_monitor.check_all()

        recovery_status = health_monitor.get_recovery_status()
        # Recovery was attempted multiple times
        assert recovery_status['services']['recovering']['attempts'] >= 1

        # Now recover (7th check passes)
        await health_monitor.check_all()

        # Recovery attempts should be reset after successful health check
        recovery_status = health_monitor.get_recovery_status()
        assert recovery_status['services']['recovering']['attempts'] == 0


# Test: Alerting

class TestAlerting:
    """Test alert handler functionality."""

    @pytest.mark.asyncio
    async def test_log_alert_handler(self, health_monitor):
        """Test that log alert handler writes to logs."""
        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check, interval=1, timeout=1)

        # Trigger max retries
        for _ in range(10):
            await health_monitor.check_all()

        # Should have logged alerts (verify no exceptions thrown)
        # The log handler is registered by default

    @pytest.mark.asyncio
    async def test_custom_alert_handler(self, health_monitor):
        """Test that custom alert handlers are called."""
        alerts_received = []

        def custom_handler(alert):
            alerts_received.append(alert)

        health_monitor.add_alert_handler(custom_handler)

        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check, interval=1, timeout=1)

        # Trigger alerts
        for _ in range(5):
            await health_monitor.check_all()

        # Verify custom handler received alerts
        assert len(alerts_received) > 0

        # Check alert structure
        alert = alerts_received[0]
        assert 'service' in alert
        assert 'reason' in alert
        assert 'timestamp' in alert
        assert 'severity' in alert
        assert alert['service'] == 'failing'

    @pytest.mark.asyncio
    async def test_alert_severity_levels(self, health_monitor, mock_alert_handler):
        """Test that alerts have appropriate severity levels."""
        health_monitor.add_alert_handler(mock_alert_handler)

        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check, interval=1, timeout=1)

        # Trigger max retries for critical alert
        for _ in range(10):
            await health_monitor.check_all()

        # Check severity levels
        alerts = [call[0][0] for call in mock_alert_handler.call_args_list]

        # Should have critical severity for max_retries_exceeded
        critical_alerts = [a for a in alerts if a.get('severity') == 'critical']
        assert len(critical_alerts) > 0

        # Should have warning severity for recovery_failed
        warning_alerts = [a for a in alerts if a.get('severity') == 'warning']
        assert len(warning_alerts) > 0

    @pytest.mark.asyncio
    async def test_alert_handler_exception_handling(self, health_monitor):
        """Test that exceptions in alert handlers don't crash monitoring."""

        def failing_handler(alert):
            raise Exception("Handler error!")

        def working_handler(alert):
            pass

        health_monitor.add_alert_handler(failing_handler)
        health_monitor.add_alert_handler(working_handler)

        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check, interval=1, timeout=1)

        # Should not raise exception even though handler fails
        for _ in range(5):
            await health_monitor.check_all()

    @pytest.mark.asyncio
    async def test_async_alert_handler(self, health_monitor):
        """Test that async alert handlers work correctly."""
        alerts_received = []

        async def async_handler(alert):
            await asyncio.sleep(0.01)  # Simulate async operation
            alerts_received.append(alert)

        health_monitor.add_alert_handler(async_handler)

        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check, interval=1, timeout=1)

        # Trigger alerts
        for _ in range(5):
            await health_monitor.check_all()

        # Verify async handler was called
        assert len(alerts_received) > 0


# Test: Recovery Status

class TestRecoveryStatus:
    """Test recovery status tracking and reporting."""

    @pytest.mark.asyncio
    async def test_get_recovery_status_empty(self, health_monitor):
        """Test recovery status when no services are registered."""
        status = health_monitor.get_recovery_status()

        assert status['auto_recover_enabled'] == True
        assert status['max_recovery_attempts'] == 3
        assert status['services'] == {}

    @pytest.mark.asyncio
    async def test_get_recovery_status_with_failures(self, health_monitor):
        """Test recovery status after failures."""
        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check)

        # Trigger recovery
        for _ in range(3):
            await health_monitor.check_all()

        status = health_monitor.get_recovery_status()

        assert 'failing' in status['services']
        assert status['services']['failing']['attempts'] == 1
        assert status['services']['failing']['can_recover'] == True

    @pytest.mark.asyncio
    async def test_get_recovery_status_max_retries(self, health_monitor):
        """Test recovery status after max retries."""
        def failing_check():
            return False

        health_monitor.register_check("failing", failing_check)

        # Exhaust recovery attempts
        for _ in range(10):
            await health_monitor.check_all()

        status = health_monitor.get_recovery_status()

        assert status['services']['failing']['attempts'] == 3
        assert status['services']['failing']['can_recover'] == False


# Test: Integration with Service Registry

class TestServiceRegistryIntegration:
    """Test integration with ServiceRegistry for service recovery."""

    @pytest.mark.asyncio
    async def test_service_restart_via_registry(self):
        """Test that services can be restarted via registry."""

        # Create mock service with restart method
        mock_service = Mock()
        mock_service.restart = AsyncMock(return_value=True)

        # Create mock registry that returns empty health status dict
        mock_registry = Mock()
        mock_registry.get = AsyncMock(return_value=mock_service)
        mock_registry.health_status = Mock(return_value={})

        # Create monitor with registry
        monitor = HealthMonitor(service_registry=mock_registry, auto_recover=True)

        def failing_check():
            return False

        monitor.register_check("test-service", failing_check, interval=1, timeout=1)

        # Trigger recovery
        for _ in range(3):
            await monitor.check_all()

        # Verify restart was called
        mock_service.restart.assert_called()

    @pytest.mark.asyncio
    async def test_service_custom_recover_via_registry(self):
        """Test that services can use custom recover method via registry."""

        # Create mock service with recover method (no restart)
        mock_service = Mock()
        mock_service.recover = AsyncMock(return_value=True)
        # Remove restart to test custom recover path
        del mock_service.restart

        # Create mock registry that returns empty health status dict
        mock_registry = Mock()
        mock_registry.get = AsyncMock(return_value=mock_service)
        mock_registry.health_status = Mock(return_value={})

        # Create monitor with registry
        monitor = HealthMonitor(service_registry=mock_registry, auto_recover=True)

        def failing_check():
            return False

        monitor.register_check("test-service", failing_check, interval=1, timeout=1)

        # Trigger recovery
        for _ in range(3):
            await monitor.check_all()

        # Verify recover was called (since restart doesn't exist)
        mock_service.recover.assert_called()

    @pytest.mark.asyncio
    async def test_service_not_in_registry(self, health_monitor):
        """Test behavior when service is not in registry."""
        # No registry configured, should still work
        def failing_check():
            return False

        health_monitor.register_check("missing-service", failing_check, interval=1, timeout=1)

        # Should not raise exception
        for _ in range(3):
            await health_monitor.check_all()


# Test: Health History and Recovery

class TestHealthHistoryWithRecovery:
    """Test health history tracking with recovery events."""

    @pytest.mark.asyncio
    async def test_recovery_tracked_in_history(self, health_monitor):
        """Test that recovery events are reflected in health history."""

        fail_count = 0

        def flaky_check():
            nonlocal fail_count
            fail_count += 1
            return fail_count > 3

        health_monitor.register_check("flaky", flaky_check, interval=1, timeout=1)

        # Run checks - should see failures first
        await health_monitor.check_all()  # fail 1
        await health_monitor.check_all()  # fail 2
        await health_monitor.check_all()  # fail 3

        # Get history
        history = health_monitor.get_health_history(limit=10)

        # Should have history entries
        assert len(history) > 0

        # Should see degraded or unhealthy status during failures
        degraded_or_unhealthy = [h for h in history if h['status'] in ('degraded', 'unhealthy')]
        assert len(degraded_or_unhealthy) > 0, f"Expected degraded/unhealthy entries, got statuses: {[h['status'] for h in history]}"

    @pytest.mark.asyncio
    async def test_uptime_with_recoveries(self, health_monitor):
        """Test uptime calculation with recovery events."""

        always_healthy = lambda: True

        health_monitor.register_check("always-healthy", always_healthy, interval=1, timeout=1)

        # Run checks
        for _ in range(10):
            await health_monitor.check_all()

        uptime = health_monitor.get_uptime()

        assert uptime['uptime_percentage'] == 100.0
        assert uptime['total_checks'] == 10
        assert uptime['healthy_checks'] == 10


# Test: Edge Cases

class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_recovery_function_raises_exception(self, health_monitor, mock_alert_handler):
        """Test that exceptions in recovery functions are handled."""

        def bad_recovery():
            raise RuntimeError("Recovery failed!")

        def failing_check():
            return False

        health_monitor.add_alert_handler(mock_alert_handler)
        health_monitor.register_check(
            "bad-recovery",
            failing_check,
            interval=1,
            timeout=1,
            recovery_func=bad_recovery
        )

        # Should not crash, but should alert
        for _ in range(3):
            await health_monitor.check_all()

        # Verify alert was sent for recovery failure
        assert mock_alert_handler.called
        alerts = [call[0][0] for call in mock_alert_handler.call_args_list]
        # Should have recovery_failed alert (when custom recovery function fails)
        failed_alerts = [a for a in alerts if a.get('reason') == 'recovery_failed']
        assert len(failed_alerts) > 0
        # Verify severity is warning
        assert failed_alerts[0]['severity'] == 'warning'

    @pytest.mark.asyncio
    async def test_health_check_timeout_during_recovery(self, health_monitor):
        """Test behavior when health check times out."""

        import time

        def slow_check():
            time.sleep(2)  # Longer than timeout
            return True

        health_monitor.register_check("slow", slow_check, interval=1, timeout=0.1)

        # Should handle timeout gracefully
        await health_monitor.check_all()

        health = health_monitor.get_current_health()
        assert health['checks']['slow']['healthy'] == False

    @pytest.mark.asyncio
    async def test_concurrent_health_checks(self, health_monitor):
        """Test that multiple health checks can run concurrently."""

        def check(name):
            def inner():
                return True
            inner.__name__ = name
            return inner

        # Register multiple checks
        for i in range(5):
            health_monitor.register_check(f"check-{i}", check(f"check-{i}"), interval=1, timeout=1)

        # Run all checks
        await health_monitor.check_all()

        health = health_monitor.get_current_health()

        # All should be checked
        for i in range(5):
            assert f"check-{i}" in health['checks']
            assert health['checks'][f"check-{i}"]['healthy'] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
