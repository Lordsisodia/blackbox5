"""
Client module for Blackbox5 agents.

Provides various client implementations for agent execution:
- ClaudeCodeClient: Execute tasks via Claude Code CLI (preferred)
- ClaudeCodeAgentMixin: Mixin for adding Claude Code execution to agents
- AgentClient: Generic agent client with multiple backends
- GLMClient: GLM API client
- AgentOutputParser: Parse structured outputs from agents
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

from client.AgentOutputParser import (
    ParsedAgentOutput,
    AgentOutputParserError,
    parse_agent_output,
    parse_agent_output_lax,
    extract_status,
    extract_deliverables,
    extract_next_steps,
    create_agent_output,
    validate_agent_output,
    handle_agent_response,
    chain_agent_outputs,
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

    # Agent Output Parser
    "ParsedAgentOutput",
    "AgentOutputParserError",
    "parse_agent_output",
    "parse_agent_output_lax",
    "extract_status",
    "extract_deliverables",
    "extract_next_steps",
    "create_agent_output",
    "validate_agent_output",
    "handle_agent_response",
    "chain_agent_outputs",
]
