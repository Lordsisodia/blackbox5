# API Documentation

*This documentation was automatically generated from code files.*

---


## /workspaces/blackbox5/2-engine/.autonomous/lib/agent_discovery.py

Agent Discovery Service for RALF Multi-Agent Coordination

This module provides functionality to discover active RALF agents by reading
the heartbeat.yaml file that all agents update.

Usage:
    from agent_discovery import discover_agents, get_agent_info

    # Discover all active agents
    agents = discover_agents()
    print(f"Found {len(agents)} active agents")

    # Get info about specific agent
    planner_info = get_agent_info("planner")

### Functions

#### __init__(self, agent_id: str, last_seen: str, status: str,
                 current_action: str, loop_number: int, run_number: int)

Check if agent is considered active based on last_seen timestamp.

        Args:
            timeout_seconds: Seconds before agent considered inactive

        Returns:
            True if agent is active, False otherwise

#### is_active(self, timeout_seconds: int = AGENT_TIMEOUT_SECONDS) -> bool:
        """
        Check if agent is considered active based on last_seen timestamp.

        Args:
            timeout_seconds: Seconds before agent considered inactive

        Returns:
            True if agent is active, False otherwise
        """
        try:
            last_seen_dt = datetime.fromisoformat(self.last_seen.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            delta = (now - last_seen_dt).total_seconds()
            return delta < timeout_seconds
        except Exception as e:
            print(f"Warning: Could not parse timestamp for {self.agent_id}: {e}")
            return False

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "agent_id": self.agent_id,
            "last_seen": self.last_seen,
            "status": self.status,
            "current_action": self.current_action,
            "loop_number": self.loop_number,
            "run_number": self.run_number,
            "is_active": self.is_active()
        }

    def __repr__(self) -> str:
        return f"AgentInfo(id={self.agent_id}, status={self.status}, active={self.is_active()})"


def discover_agents(heartbeat_file: str = DEFAULT_HEARTBEAT_FILE,
                    timeout_seconds: int = AGENT_TIMEOUT_SECONDS) -> List[AgentInfo]:
    """
    Discover all active RALF agents from heartbeat.yaml.

    Args:
        heartbeat_file: Path to heartbeat.yaml file
        timeout_seconds: Seconds before agent considered inactive

    Returns:
        List of AgentInfo objects for active agents

    Example:
        >>> agents = discover_agents()
        >>> for agent in agents:
        ...     print(f"{agent.agent_id}: {agent.current_action}")
    """
    heartbeat_path = Path(heartbeat_file)

    if not heartbeat_path.exists()

Get information about a specific agent.

    Args:
        agent_id: ID of the agent to lookup (e.g., "planner", "executor")
        heartbeat_file: Path to heartbeat.yaml file

    Returns:
        AgentInfo object if found, None otherwise

    Example:
        >>> planner = get_agent_info("planner")
        >>> if planner:
        ...     print(f"Planner status: {planner.status}")



---

*Generated: {{timestamp}}*
