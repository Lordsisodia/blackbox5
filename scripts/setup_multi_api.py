#!/usr/bin/env python3
"""
BlackBox5 Multi-API Setup Script
Configures and integrates all API providers with intelligent routing.
"""

import os
import sys
import yaml
import json
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.api_selector import APISelector
from agents.api_usage_tracker import APIUsageTracker
from agents.kimi_load_balancer import KimiLoadBalancer
from agents.nvidia_kimi_integration import NvidiaKimiClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiAPISetup:
    """Setup and integration for multi-API system"""

    def __init__(self):
        self.config_path = "/opt/blackbox5/config/api-keys.yaml"
        self.setup_complete = False

    def verify_config(self) -> bool:
        """Verify configuration file exists and is valid"""
        if not Path(self.config_path).exists():
            logger.error(f"Configuration file not found: {self.config_path}")
            return False

        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Verify required sections
            required_sections = ['providers', 'task_routing', 'global_settings']
            for section in required_sections:
                if section not in config:
                    logger.error(f"Missing required section: {section}")
                    return False

            logger.info("Configuration file is valid")
            return True

        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML configuration: {e}")
            return False

    def verify_api_keys(self) -> Dict[str, bool]:
        """Verify which API keys are configured"""
        results = {}

        # Check for environment variables
        env_keys = {
            'KIMI_CISO_KEY': 'Kimi CISO key',
            'NVIDIA_KIMI_KEY': 'Nvidia Kimi key',
            'ANTHROPIC_API_KEY': 'Anthropic Claude key',
        }

        for env_var, name in env_keys.items():
            key = os.getenv(env_var)
            results[env_var] = {
                'configured': bool(key),
                'name': name,
                'has_value': bool(key and not key.startswith('${'))
            }

            if key and not key.startswith('${'):
                # Show key prefix (first 10 chars)
                results[env_var]['prefix'] = key[:10] + '...'

        return results

    def initialize_components(self) -> bool:
        """Initialize all multi-API components"""
        try:
            logger.info("Initializing API Selector...")
            selector = APISelector(self.config_path)
            logger.info(f"  API Selector loaded {len(selector.providers)} providers")

            logger.info("Initializing Usage Tracker...")
            tracker = APIUsageTracker()
            logger.info("  Usage Tracker initialized")

            logger.info("Initializing Kimi Load Balancer...")
            kimi_lb = KimiLoadBalancer(self.config_path)
            logger.info(f"  Kimi Load Balancer loaded {len(kimi_lb.keys)} keys")

            logger.info("Initializing Nvidia Kimi Client...")
            nvidia_client = NvidiaKimiClient(self.config_path)
            nvidia_available = nvidia_client.is_available()
            logger.info(f"  Nvidia Kimi Client {'available' if nvidia_available else 'not available'}")

            self.setup_complete = True
            return True

        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False

    def test_provider_selection(self) -> bool:
        """Test provider selection for various task types"""
        try:
            selector = APISelector(self.config_path)

            logger.info("\n=== Testing Provider Selection ===\n")

            test_cases = [
                ("coding", ["coding"], "high", "Code generation task"),
                ("long_context", ["long_context"], "medium", "Long conversation task"),
                ("video_processing", ["video_processing"], "medium", "Video analysis task"),
                ("reasoning", ["reasoning"], "high", "Complex reasoning task"),
                ("general", [], "low", "General task"),
            ]

            all_passed = True

            for task_type, capabilities, criticality, description in test_cases:
                try:
                    selection = selector.select_provider(
                        task_type=task_type,
                        required_capabilities=capabilities,
                        criticality=criticality
                    )

                    logger.info(f"✓ {description}")
                    logger.info(f"  Provider: {selection.provider.name} (priority: {selection.provider.priority})")
                    logger.info(f"  Reason: {selection.reason}")
                    logger.info(f"  Confidence: {selection.confidence}")
                    logger.info(f"  Fallbacks: {', '.join(selection.fallback_chain) or 'none'}")
                    logger.info("")

                except Exception as e:
                    logger.error(f"✗ {description}: {e}")
                    all_passed = False

            return all_passed

        except Exception as e:
            logger.error(f"Error testing provider selection: {e}")
            return False

    def generate_setup_report(self) -> Dict[str, Any]:
        """Generate comprehensive setup report"""
        selector = APISelector(self.config_path)
        tracker = APIUsageTracker()
        kimi_lb = KimiLoadBalancer(self.config_path)
        nvidia_client = NvidiaKimiClient(self.config_path)

        # Get provider status
        provider_status = selector.get_provider_status()

        # Get Kimi status
        kimi_status = kimi_lb.get_key_status()

        # Get Nvidia status
        nvidia_status = nvidia_client.get_status()

        return {
            "setup_timestamp": datetime.utcnow().isoformat(),
            "configuration": {
                "config_path": self.config_path,
                "valid": self.verify_config(),
                "api_keys_configured": self.verify_api_keys()
            },
            "providers": provider_status,
            "kimi_keys": {
                "total_keys": len(kimi_status),
                "available_keys": sum(1 for k in kimi_status.values() if k['status'] == 'active'),
                "details": kimi_status
            },
            "nvidia_kimi": nvidia_status,
            "components": {
                "api_selector": "initialized",
                "usage_tracker": "initialized",
                "kimi_load_balancer": "initialized",
                "nvidia_client": "available" if nvidia_client.is_available() else "configured"
            },
            "task_routing": selector.task_routing,
            "recommendations": self._generate_recommendations()
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate setup recommendations"""
        recommendations = []

        # Check for missing API keys
        api_keys = self.verify_api_keys()
        for env_var, info in api_keys.items():
            if not info['has_value']:
                recommendations.append(
                    f"Set {env_var} environment variable for {info['name']}"
                )

        # Check provider status
        selector = APISelector(self.config_path)
        provider_status = selector.get_provider_status()

        for provider_id, status in provider_status.items():
            if not status['enabled']:
                recommendations.append(
                    f"Provider {provider_id} is disabled - consider enabling if needed"
                )

            if status['error_count'] > 0:
                recommendations.append(
                    f"Provider {provider_id} has {status['error_count']} errors - check configuration"
                )

        return recommendations if recommendations else ["All components configured correctly"]


def main():
    """Main setup function"""
    print("=" * 80)
    print("BlackBox5 Multi-API Setup")
    print("=" * 80)
    print()

    setup = MultiAPISetup()

    # Step 1: Verify configuration
    print("Step 1: Verifying configuration...")
    if not setup.verify_config():
        print("❌ Configuration verification failed")
        return 1
    print("✓ Configuration verified\n")

    # Step 2: Check API keys
    print("Step 2: Checking API keys...")
    api_keys = setup.verify_api_keys()
    print("API Key Status:")
    for env_var, info in api_keys.items():
        status = "✓" if info['has_value'] else "✗"
        prefix = info.get('prefix', 'not set')
        print(f"  {status} {info['name']}: {prefix}")
    print()

    # Step 3: Initialize components
    print("Step 3: Initializing components...")
    if not setup.initialize_components():
        print("❌ Component initialization failed")
        return 1
    print("✓ All components initialized\n")

    # Step 4: Test provider selection
    print("Step 4: Testing provider selection...")
    if not setup.test_provider_selection():
        print("⚠ Some provider selection tests failed")
    print()

    # Step 5: Generate report
    print("Step 5: Generating setup report...")
    report = setup.generate_setup_report()

    # Save report
    report_path = "/opt/blackbox5/data/multi-api-setup-report.json"
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"✓ Report saved to {report_path}\n")

    # Summary
    print("=" * 80)
    print("Setup Summary")
    print("=" * 80)
    print(f"✓ Multi-API setup complete")
    print(f"✓ {len(report['providers'])} providers configured")
    print(f"✓ {report['kimi_keys']['available_keys']}/{report['kimi_keys']['total_keys']} Kimi keys available")
    print(f"✓ Nvidia Kimi: {report['nvidia_kimi']['enabled']}")
    print()

    # Recommendations
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    print()

    print("=" * 80)
    print("Setup Complete!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
