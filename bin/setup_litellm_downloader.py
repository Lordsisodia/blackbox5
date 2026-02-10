#!/usr/bin/env python3
"""
Setup litellm downloader for Kimi K2.5 model
Installs and configures litellm to work with the load balancer
"""

import os
import subprocess
import sys
import yaml
import json
from pathlib import Path

def install_litellm():
    """Install litellm package"""
    print("Installing litellm...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'litellm[proxy]'],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ litellm installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install litellm: {e}")
        return False

def create_env_file():
    """Create .env file with API keys"""
    env_path = Path('/opt/blackbox5/.env')
    env_example_path = Path('/opt/blackbox5/.env.example')

    # Create example file
    example_content = """
# Kimi API Keys
KIMI_CISO_KEY=your-ciso-key-here
KIMI_TRIAL_KEY_01=your-trial-key-1-here
KIMI_TRIAL_KEY_02=your-trial-key-2-here
KIMI_TRIAL_KEY_03=your-trial-key-3-here
KIMI_TRIAL_KEY_04=your-trial-key-4-here
KIMI_TRIAL_KEY_05=your-trial-key-5-here
KIMI_TRIAL_KEY_06=your-trial-key-6-here
KIMI_TRIAL_KEY_07=your-trial-key-7-here
KIMI_TRIAL_KEY_08=your-trial-key-8-here

# litellm Master Key (for admin access)
LITELLM_MASTER_KEY=sk-master-change-this-to-secure-random-string

# Optional: Alert Webhook URL
# ALERT_WEBHOOK_URL=https://hooks.slack.com/services/...
"""

    env_example_path.write_text(example_content.strip())
    print(f"✓ Created .env.example at {env_example_path}")

    # Check if .env exists
    if not env_path.exists():
        env_path.write_text(example_content.strip())
        print(f"✓ Created .env at {env_path}")
        print("  ⚠ Please edit /opt/blackbox5/.env and add your actual API keys")
    else:
        print(f"✓ .env already exists at {env_path}")

def create_start_script():
    """Create startup script for litellm proxy with load balancer"""
    script_path = Path('/opt/blackbox5/bin/start_litellm_proxy.sh')
    script_content = """#!/bin/bash
# Start litellm proxy with Kimi load balancer

set -e

# Load environment variables
if [ -f /opt/blackbox5/.env ]; then
    export $(cat /opt/blackbox5/.env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Create logs directory
mkdir -p /opt/blackbox5/logs
mkdir -p /opt/blackbox5/data

# Start litellm proxy
echo "Starting litellm proxy on port 4000..."
echo "Config: /opt/blackbox5/config/litellm-config.yaml"

cd /opt/blackbox5

litellm --config /opt/blackbox5/config/litellm-config.yaml \\
       --port 4000 \\
       --host 0.0.0.0 \\
       --detailed_debug \\
       > /opt/blackbox5/logs/litellm-proxy.log 2>&1 &

LITELLM_PID=$!
echo $LITELLM_PID > /opt/blackbox5/.litellm-proxy.pid

echo "✓ litellm proxy started (PID: $LITELLM_PID)"
echo "  API endpoint: http://localhost:4000"
echo "  Health check: http://localhost:4000/health"
echo "  Metrics: http://localhost:4000/metrics"
"""

    script_path.write_text(script_content.strip())
    os.chmod(script_path, 0o755)
    print(f"✓ Created startup script at {script_path}")

def create_stop_script():
    """Create stop script for litellm proxy"""
    script_path = Path('/opt/blackbox5/bin/stop_litellm_proxy.sh')
    script_content = """#!/bin/bash
# Stop litellm proxy

PID_FILE="/opt/blackbox5/.litellm-proxy.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping litellm proxy (PID: $PID)..."
        kill "$PID"
        rm "$PID_FILE"
        echo "✓ litellm proxy stopped"
    else
        echo "Process not running, removing PID file"
        rm "$PID_FILE"
    fi
else
    echo "No PID file found, trying to find process..."
    pkill -f "litellm.*--port 4000" || echo "No litellm proxy process found"
fi
"""

    script_path.write_text(script_content.strip())
    os.chmod(script_path, 0o755)
    print(f"✓ Created stop script at {script_path}")

def create_service_file():
    """Create systemd service file for litellm proxy"""
    service_path = Path('/opt/blackbox5/config/litellm-proxy.service')
    service_content = """[Unit]
Description=litellm Proxy with Kimi Load Balancer
After=network.target
Wants=network.target

[Service]
Type=simple
User=bb5-runner
Group=bb5-runner
WorkingDirectory=/opt/blackbox5
EnvironmentFile=/opt/blackbox5/.env
ExecStart=/usr/bin/python3 -m litellm --config /opt/blackbox5/config/litellm-config.yaml --port 4000 --host 0.0.0.0 --detailed_debug
Restart=always
RestartSec=10
StandardOutput=append:/opt/blackbox5/logs/litellm-proxy.log
StandardError=append:/opt/blackbox5/logs/litellm-proxy.log

[Install]
WantedBy=multi-user.target
"""

    service_path.write_text(service_content.strip())
    print(f"✓ Created systemd service file at {service_path}")
    print("  To install: sudo cp /opt/blackbox5/config/litellm-proxy.service /etc/systemd/system/")
    print("  To enable: sudo systemctl enable litellm-proxy")
    print("  To start: sudo systemctl start litellm-proxy")

def create_wrapper_script():
    """Create wrapper script that integrates load balancer with litellm"""
    script_path = Path('/opt/blackbox5/bin/kimi_litellm_wrapper.py')
    script_content = """#!/usr/bin/env python3
"""
Wrapper script for litellm that integrates with Kimi load balancer
Dynamically rotates API keys and handles health monitoring
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add bin directory to path
sys.path.insert(0, '/opt/blackbox5/bin')

from kimi_load_balancer import KimiLoadBalancer
import requests

class KimiLitellmWrapper:
    def __init__(self):
        self.lb = KimiLoadBalancer()
        self.health_check_thread = None
        self.running = False

    def start(self):
        """Start the wrapper with health checks"""
        self.running = True

        # Start health check thread
        self.health_check_thread = threading.Thread(target=self._health_check_loop, daemon=True)
        self.health_check_thread.start()

        print("✓ Kimi litellm wrapper started")
        print("  Health checks running every 60 seconds")

    def _health_check_loop(self):
        """Periodic health check loop"""
        while self.running:
            try:
                self.lb.check_all_keys()
            except Exception as e:
                print(f"Health check error: {e}")
            time.sleep(60)

    def get_api_key(self, agent: str = None, task_type: str = None) -> tuple:
        """Get API key from load balancer"""
        return self.lb.get_key(agent, task_type)

    def record_request(self, key_id: str, agent: str, task_type: str,
                      tokens_input: int, tokens_output: int,
                      success: bool, error: str = None, latency_ms: int = None):
        """Record request statistics"""
        self.lb.record_usage(key_id, agent, task_type,
                            tokens_input, tokens_output,
                            success, error, latency_ms)

    def get_stats(self) -> dict:
        """Get usage statistics"""
        return self.lb.get_stats()

    def get_summary(self) -> dict:
        """Get usage summary"""
        return self.lb.get_summary()

# Singleton instance
_wrapper = None

def get_wrapper() -> KimiLitellmWrapper:
    global _wrapper
    if _wrapper is None:
        _wrapper = KimiLitellmWrapper()
        _wrapper.start()
    return _wrapper

if __name__ == '__main__':
    import json

    wrapper = get_wrapper()

    # Test key selection
    print("\\nTesting key selection:")
    for i in range(5):
        key = wrapper.get_api_key(agent='main', task_type='planning')
        print(f"  Request {i+1}: {key}")

    # Print summary
    print("\\nSummary:")
    print(json.dumps(wrapper.get_summary(), indent=2))
"""

    script_path.write_text(script_content.strip())
    os.chmod(script_path, 0o755)
    print(f"✓ Created wrapper script at {script_path}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Setting up litellm for Kimi API Load Balancer")
    print("=" * 60)
    print()

    # Install litellm
    if not install_litellm():
        print("✗ Setup failed - could not install litellm")
        return 1

    print()

    # Create .env file
    create_env_file()
    print()

    # Create startup script
    create_start_script()
    print()

    # Create stop script
    create_stop_script()
    print()

    # Create service file
    create_service_file()
    print()

    # Create wrapper script
    create_wrapper_script()
    print()

    # Create data directory
    data_dir = Path('/opt/blackbox5/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created data directory at {data_dir}")

    print()
    print("=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit /opt/blackbox5/.env and add your API keys")
    print("2. Start the proxy:")
    print("   - Manual: /opt/blackbox5/bin/start_litellm_proxy.sh")
    print("   - Or as service:")
    print("     sudo cp /opt/blackbox5/config/litellm-proxy.service /etc/systemd/system/")
    print("     sudo systemctl enable litellm-proxy")
    print("     sudo systemctl start litellm-proxy")
    print("3. Test the proxy:")
    print("   curl http://localhost:4000/v1/models")
    print("4. View metrics:")
    print("   curl http://localhost:4000/metrics")
    print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
"""

    script_path.write_text(script_content.strip())
    os.chmod(script_path, 0o755)
    print(f"✓ Created wrapper script at {script_path}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Setting up litellm for Kimi API Load Balancer")
    print("=" * 60)
    print()

    # Install litellm
    if not install_litellm():
        print("✗ Setup failed - could not install litellm")
        return 1

    print()

    # Create .env file
    create_env_file()
    print()

    # Create startup script
    create_start_script()
    print()

    # Create stop script
    create_stop_script()
    print()

    # Create service file
    create_service_file()
    print()

    # Create wrapper script
    create_wrapper_script()
    print()

    # Create data directory
    data_dir = Path('/opt/blackbox5/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created data directory at {data_dir}")

    print()
    print("=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit /opt/blackbox5/.env and add your API keys")
    print("2. Start the proxy:")
    print("   - Manual: /opt/blackbox5/bin/start_litellm_proxy.sh")
    print("   - Or as service:")
    print("     sudo cp /opt/blackbox5/config/litellm-proxy.service /etc/systemd/system/")
    print("     sudo systemctl enable litellm-proxy")
    print("     sudo systemctl start litellm-proxy")
    print("3. Test the proxy:")
    print("   curl http://localhost:4000/v1/models")
    print("4. View metrics:")
    print("   curl http://localhost:4000/metrics")
    print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
