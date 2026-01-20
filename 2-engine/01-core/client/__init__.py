"""
Client module for Blackbox5 agents.

Provides various client implementations for agent execution:
- ClaudeCodeClient: Execute tasks via Claude Code CLI (preferred)
- ClaudeCodeAgentMixin: Mixin for adding Claude Code execution to agents
- AgentClient: Generic agent client with multiple backends
- GLMClient: GLM API client
"""

from client.ClaudeCodeClient import (
    ClaudeCodeClient,
    ClaudeCodeRequest,
    ClaudeCodeResult,
    execute,
    execute_async,
    get_client
)

from client.ClaudeCodeAgentMixin import (
    ClaudeCodeAgentMixin,
    ClaudeCodeAgentTemplate
)

__all__ = [
    # Claude Code CLI Client
    "ClaudeCodeClient",
    "ClaudeCodeRequest",
    "ClaudeCodeResult",
    "execute",
    "execute_async",
    "get_client",

    # Claude Code Agent Mixin
    "ClaudeCodeAgentMixin",
    "ClaudeCodeAgentTemplate",
]
