#!/usr/bin/env python3
"""
Blackbox5 Command Interface
Simple command-line interface for Blackbox5 operations.

Usage:
    python blackbox.py start                    # Start everything
    python blackbox.py start --api-only         # Start API only
    python blackbox.py start --gui-only         # Start GUI only
    python blackbox.py status                   # Check status
    python blackbox.py agents                   # List all agents
    python blackbox.py chat "What is 2+2?"      # Send a chat message
    python blackbox.py stop                     # Stop all services
"""

import sys
import os
import subprocess
import signal
import time
import requests
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
ENGINE_DIR = Path(__file__).parent / "2-engine" / "01-core"
# Vibe Kanban GUI removed - not used


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_success(msg):
    """Print success message."""
    print(f"✅ {msg}")


def print_error(msg):
    """Print error message."""
    print(f"❌ {msg}")


def print_info(msg):
    """Print info message."""
    print(f"ℹ️  {msg}")


def is_running(url):
    """Check if a service is running."""
    try:
        response = requests.get(f"{url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def start_api():
    """Start the Blackbox5 API server."""
    print_info("Starting Blackbox5 API server...")

    if is_running(API_URL):
        print_success("API server is already running!")
        return

    try:
        # Change to engine directory
        os.chdir(ENGINE_DIR)

        # Start API server in background
        process = subprocess.Popen(
            [sys.executable, "-m", "interface.api.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )

        # Wait for startup
        for _ in range(10):
            time.sleep(1)
            if is_running(API_URL):
                print_success(f"API server started on {API_URL}")
                print_info(f"API docs available at {API_URL}/docs")
                return process

        print_error("API server failed to start")
        return None

    except Exception as e:
        print_error(f"Failed to start API: {e}")
        return None


def start_gui():
    """Vibe Kanban GUI removed - not implemented."""
    print_info("GUI not implemented")
    return None


def stop_services():
    """Stop all Blackbox5 services."""
    print_info("Stopping Blackbox5 services...")

    # Kill API process by port
    try:
        result = subprocess.run(
            ["lsof", "-t", "-i", ":8000"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
            print_success("API server stopped (port 8000)")
    except:
        pass


def check_status():
    """Check the status of all services."""
    print_header("BLACKBOX5 STATUS")

    # Check API
    if is_running(API_URL):
        print_success(f"API Server:     Running ({API_URL})")

        # Try to get agent count
        try:
            response = requests.get(f"{API_URL}/agents", timeout=2)
            if response.status_code == 200:
                agents = response.json()
                print_info(f"   Agents:       {len(agents)} loaded")
        except:
            pass
    else:
        print_error(f"API Server:     Not running")

    print()


def list_agents():
    """List all available agents."""
    if not is_running(API_URL):
        print_error("API server is not running. Start it with: python blackbox.py start")
        return

    try:
        response = requests.get(f"{API_URL}/agents", timeout=5)
        if response.status_code == 200:
            agents = response.json()

            print_header(f"AVAILABLE AGENTS ({len(agents)})")

            # Group by category
            from collections import defaultdict
            by_category = defaultdict(list)
            for agent in agents:
                cat = agent.get('category', 'general')
                by_category[cat].append(agent)

            for category, agents_list in sorted(by_category.items()):
                print(f"\n{category.upper()} ({len(agents_list)}):")
                for agent in agents_list:
                    print(f"  • {agent['name']}")
                    if agent.get('description'):
                        print(f"    {agent['description'][:80]}...")

            print()
        else:
            print_error("Failed to fetch agents")
    except Exception as e:
        print_error(f"Error: {e}")


def send_chat(message, agent=None):
    """Send a chat message to Blackbox5."""
    if not is_running(API_URL):
        print_error("API server is not running. Start it with: python blackbox.py start")
        return

    print_info(f"Sending message to Blackbox5...")

    payload = {"message": message}
    if agent:
        payload["agent"] = agent

    try:
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()

            if result.get('success'):
                print_header("RESPONSE")

                # Show routing info
                if result.get('routing'):
                    routing = result['routing']
                    print(f"Agent:    {routing.get('selected_agent', 'N/A')}")
                    print(f"Strategy: {routing.get('strategy', 'N/A')}")
                    print()

                # Show result
                if result.get('result'):
                    r = result['result']
                    if r.get('output'):
                        print(r['output'])
            else:
                print_error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            print_error(f"HTTP {response.status_code}: {response.text}")

    except Exception as e:
        print_error(f"Error: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == "start":
        print_header("🚀 STARTING BLACKBOX5")

        api_process = start_api()

        if api_process:
            print_success("\n🎉 Blackbox5 is ready!")
            print_info("\nUse Ctrl+C to stop, or run: python blackbox.py stop")

            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                stop_services()

    elif command == "status":
        check_status()

    elif command == "agents":
        list_agents()

    elif command == "chat":
        if len(sys.argv) < 3:
            print_error("Usage: python blackbox.py chat \"your message here\"")
            return
        message = ' '.join(sys.argv[2:])
        send_chat(message)

    elif command == "stop":
        stop_services()

    else:
        print_error(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
