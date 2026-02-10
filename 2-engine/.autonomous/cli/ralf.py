#!/usr/bin/env python3
"""
RALF CLI - Command-line interface for RALF autonomous system
Version: 1.0.0
"""
import os
import sys
import click
import json
import yaml
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Project paths - auto-detect from current directory
def find_blackbox5_root():
    """Find blackbox5 root directory by searching upward."""
    current = Path.cwd()

    # Search upward for blackbox5 directory
    while current.parent != current:
        if current.name == 'blackbox5' or (current / '5-project-memory' / 'blackbox5').exists():
            # Found it - determine if it's the project root or parent
            if current.name == 'blackbox5':
                return current
            else:
                return current / '5-project-memory' / 'blackbox5'
        current = current.parent

    # Fallback to default
    return Path.home() / '.blackbox5' / '5-project-memory' / 'blackbox5'

BLACKBOX5_ROOT = find_blackbox5_root()

# Try both possible communication directory locations
COMM_DIR = BLACKBOX5_ROOT / '.autonomous' / 'agents' / 'communications'
if not COMM_DIR.exists():
    # Try without agents/ subdirectory
    COMM_DIR = BLACKBOX5_ROOT / '.autonomous' / 'communications'

# ANSI colors for severity
COLOR_ERROR = Fore.RED
COLOR_WARNING = Fore.YELLOW
COLOR_SUCCESS = Fore.GREEN
COLOR_INFO = Fore.CYAN
COLOR_RESET = Style.RESET_ALL

def print_error(msg):
    """Print error message in red."""
    print(f"{COLOR_ERROR}✗ {msg}{COLOR_RESET}")

def print_success(msg):
    """Print success message in green."""
    print(f"{COLOR_SUCCESS}✓ {msg}{COLOR_RESET}")

def print_warning(msg):
    """Print warning message in yellow."""
    print(f"{COLOR_WARNING}⚠ {msg}{COLOR_RESET}")

def print_info(msg):
    """Print info message in cyan."""
    print(f"{COLOR_INFO}ℹ {msg}{COLOR_RESET}")

def load_queue():
    """Load queue.yaml and return tasks."""
    queue_file = COMM_DIR / 'queue.yaml'
    if not queue_file.exists():
        print_error(f"Queue file not found: {queue_file}")
        return []

    try:
        with open(queue_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('tasks', [])
    except Exception as e:
        print_error(f"Failed to load queue: {e}")
        return []

def load_heartbeat():
    """Load heartbeat.yaml and return agent status."""
    heartbeat_file = COMM_DIR / 'heartbeat.yaml'
    if not heartbeat_file.exists():
        print_error(f"Heartbeat file not found: {heartbeat_file}")
        return {}

    try:
        with open(heartbeat_file, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print_error(f"Failed to load heartbeat: {e}")
        return {}

@click.group()
@click.version_option(version='1.0.0')
@click.help_option('-h', '--help')
def ralf():
    """RALF CLI - Command-line interface for RALF autonomous system."""
    pass

@ralf.group()
def task():
    """Task management commands."""
    pass

@task.command('list')
@click.option('--output', '-o', type=click.Choice(['table', 'json']), default='table',
              help='Output format')
def task_list(output):
    """List current active tasks."""
    tasks = load_queue()

    if not tasks:
        print_warning("No tasks found in queue")
        return

    # Filter for pending/in_progress tasks
    active_tasks = [t for t in tasks if t.get('status') in ['pending', 'in_progress']]

    if output == 'json':
        print(json.dumps(active_tasks, indent=2))
        return

    # Print table format
    print(f"\n{COLOR_INFO}Active Tasks ({len(active_tasks)}){COLOR_RESET}\n")

    for t in active_tasks:
        status_color = COLOR_WARNING if t.get('status') == 'pending' else COLOR_SUCCESS
        status = f"{status_color}{t.get('status', 'unknown').upper()}{COLOR_RESET}"
        priority = t.get('priority', 'N/A')
        task_id = t.get('id', 'N/A')
        title = t.get('title', 'No title')

        print(f"  {task_id}")
        print(f"    Status: {status}")
        print(f"    Priority: {priority}")
        print(f"    Title: {title}")
        print()

@task.command('show')
@click.argument('task_id')
@click.option('--output', '-o', type=click.Choice(['table', 'json']), default='table',
              help='Output format')
def task_show(task_id, output):
    """Show full task details."""
    tasks = load_queue()

    # Find task by ID
    task = next((t for t in tasks if t.get('id') == task_id), None)

    if not task:
        print_error(f"Task not found: {task_id}")
        return

    if output == 'json':
        print(json.dumps(task, indent=2))
        return

    # Print table format
    print(f"\n{COLOR_INFO}Task Details: {task_id}{COLOR_RESET}\n")
    print(f"  Title: {task.get('title', 'No title')}")
    print(f"  Status: {task.get('status', 'unknown').upper()}")
    print(f"  Priority: {task.get('priority', 'N/A')}")
    print(f"  Type: {task.get('type', 'N/A')}")

    if 'roi' in task:
        roi = task['roi']
        print(f"  Estimated Effort: {roi.get('effort', 'N/A')} minutes")
        print(f"  Impact Score: {roi.get('impact', 'N/A')}")

    if 'blockedBy' in task and task['blockedBy']:
        print(f"  Blocked By: {', '.join(task['blockedBy'])}")

    if 'blocks' in task and task['blocks']:
        print(f"  Blocks: {', '.join(task['blocks'])}")

    print()

@ralf.group()
def queue():
    """Queue management commands."""
    pass

@queue.command('show')
@click.option('--output', '-o', type=click.Choice(['table', 'json']), default='table',
              help='Output format')
@click.option('--all', is_flag=True, help='Show all tasks (including completed)')
def queue_show(output, all):
    """Display queue with priority scores."""
    tasks = load_queue()

    if not tasks:
        print_warning("No tasks found in queue")
        return

    # Sort by priority_score (descending)
    sorted_tasks = sorted(tasks, key=lambda t: t.get('priority_score', 0), reverse=True)

    if output == 'json':
        print(json.dumps(sorted_tasks, indent=2))
        return

    # Print table format
    print(f"\n{COLOR_INFO}Queue ({len(sorted_tasks)} tasks){COLOR_RESET}\n")

    for i, t in enumerate(sorted_tasks, 1):
        status = t.get('status', 'unknown')
        priority = t.get('priority', 'N/A')
        score = t.get('priority_score', 0)
        task_id = t.get('id', 'N/A')

        # Color by status
        if not all and status == 'completed':
            continue  # Skip completed tasks unless --all

        status_color = COLOR_SUCCESS if status == 'completed' else (COLOR_WARNING if status == 'pending' else COLOR_INFO)
        status_text = f"{status_color}{status.upper()}{COLOR_RESET}"

        # Priority color
        priority_color = COLOR_ERROR if priority == 'CRITICAL' else (COLOR_WARNING if priority == 'HIGH' else COLOR_SUCCESS)

        print(f"  {i}. {task_id}")
        print(f"     Status: {status_text} | Priority: {priority_color}{priority}{COLOR_RESET} | Score: {score}")
        print(f"     Title: {t.get('title', 'No title')}")
        print()

@ralf.group()
def agent():
    """Agent status and management commands."""
    pass

@agent.command('status')
@click.option('--output', '-o', type=click.Choice(['table', 'json']), default='table',
              help='Output format')
def agent_status(output):
    """Show planner/executor health."""
    heartbeat = load_heartbeat()

    if not heartbeat:
        print_warning("No heartbeat data available")
        return

    # Get heartbeats
    heartbeats = heartbeat.get('heartbeats', {})

    if output == 'json':
        print(json.dumps(heartbeats, indent=2))
        return

    # Print table format
    print(f"\n{COLOR_INFO}Agent Status{COLOR_RESET}\n")

    current_time = os.popen('date +%s').read().strip()

    for agent_id, data in heartbeats.items():
        last_seen = data.get('last_seen', 'N/A')
        status_str = data.get('status', 'unknown')

        # Calculate time since last seen
        if last_seen != 'N/A':
            try:
                last_time = int(os.popen(f"date -d '{last_seen}' +%s").read().strip())
                seconds_ago = int(current_time) - last_time
                minutes_ago = seconds_ago // 60
                hours_ago = minutes_ago // 60

                if hours_ago > 2:
                    status_color = COLOR_ERROR
                    status_text = f"stale ({hours_ago}h ago)"
                elif minutes_ago > 5:
                    status_color = COLOR_WARNING
                    status_text = f"warning ({minutes_ago}m ago)"
                else:
                    status_color = COLOR_SUCCESS
                    status_text = f"online ({minutes_ago}m ago)"
            except:
                status_color = COLOR_WARNING
                status_text = "unknown"
        else:
            status_color = COLOR_ERROR
            status_text = "never seen"

        print(f"  {agent_id}")
        print(f"    Status: {status_color}{status_text}{COLOR_RESET}")
        print(f"    Last Seen: {last_seen}")
        print(f"    Status Type: {status_str}")
        print()

@ralf.group()
def system():
    """System health and status commands."""
    pass

@system.command('health')
@click.option('--output', '-o', type=click.Choice(['table', 'json']), default='table',
              help='Output format')
def system_health(output):
    """Display overall system status."""
    tasks = load_queue()
    heartbeat = load_heartbeat()

    # Calculate metrics
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.get('status') == 'pending'])
    in_progress_tasks = len([t for t in tasks if t.get('status') == 'in_progress'])
    completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])

    # Agent health
    heartbeats = heartbeat.get('heartbeats', {})
    online_agents = 0
    stale_agents = 0

    current_time = os.popen('date +%s').read().strip()
    for agent_id, data in heartbeats.items():
        last_seen = data.get('last_seen', 'N/A')
        if last_seen != 'N/A':
            try:
                last_time = int(os.popen(f"date -d '{last_seen}' +%s").read().strip())
                seconds_ago = int(current_time) - last_time
                if seconds_ago < 300:  # 5 minutes
                    online_agents += 1
                else:
                    stale_agents += 1
            except:
                stale_agents += 1
        else:
            stale_agents += 1

    # Calculate health score
    if output == 'json':
        health_data = {
            'tasks': {
                'total': total_tasks,
                'pending': pending_tasks,
                'in_progress': in_progress_tasks,
                'completed': completed_tasks
            },
            'agents': {
                'total': len(heartbeats),
                'online': online_agents,
                'stale': stale_agents
            },
            'health_score': calculate_health_score(pending_tasks, in_progress_tasks, online_agents, stale_agents)
        }
        print(json.dumps(health_data, indent=2))
        return

    # Print table format
    print(f"\n{COLOR_INFO}=== RALF System Health ==={COLOR_RESET}\n")

    # Tasks section
    print(f"{COLOR_INFO}Tasks:{COLOR_RESET}")
    print(f"  Total: {total_tasks}")
    print(f"  {COLOR_WARNING}Pending: {pending_tasks}{COLOR_RESET}")
    print(f"  {COLOR_INFO}In Progress: {in_progress_tasks}{COLOR_RESET}")
    print(f"  {COLOR_SUCCESS}Completed: {completed_tasks}{COLOR_RESET}")
    print()

    # Agents section
    print(f"{COLOR_INFO}Agents:{COLOR_RESET}")
    print(f"  Total: {len(heartbeats)}")
    print(f"  {COLOR_SUCCESS}Online: {online_agents}{COLOR_RESET}")
    print(f"  {COLOR_ERROR}Stale: {stale_agents}{COLOR_RESET}")
    print()

    # Health score
    health_score = calculate_health_score(pending_tasks, in_progress_tasks, online_agents, stale_agents)
    score_color = COLOR_SUCCESS if health_score >= 80 else (COLOR_WARNING if health_score >= 50 else COLOR_ERROR)
    print(f"{COLOR_INFO}Health Score:{COLOR_RESET} {score_color}{health_score:.0f}/100{COLOR_RESET}")
    print()

def calculate_health_score(pending, in_progress, online, stale):
    """Calculate overall health score."""
    if stale == 0:
        agent_score = 100
    else:
        agent_score = (online / (online + stale)) * 100

    task_score = 0
    total = pending + in_progress
    if total > 0:
        task_score = (in_progress / total) * 100
    else:
        task_score = 100

    # Weighted: agents 40%, tasks 60%
    health_score = (agent_score * 0.4) + (task_score * 0.6)

    return health_score

if __name__ == '__main__':
    ralf()
