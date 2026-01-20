#!/usr/bin/env python3
"""
Quick test to verify Claude Code CLI integration is working.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from infrastructure.main import Blackbox5


async def main():
    print("="*60)
    print("Claude Code CLI Integration Test")
    print("="*60)

    core = Blackbox5()
    await core.initialize()

    # Test 1: Check that agents have Claude Code integration
    print("\n1. Checking agents for Claude Code integration...")

    agents_to_check = [
        ('DeveloperAgent', 'Python agent'),
        ('ArchitectAgent', 'Python agent'),
        ('AnalystAgent', 'Python agent'),
        ('specialists_security-specialist', 'YAML agent'),
    ]

    for agent_key, agent_type in agents_to_check:
        agent = core._agents.get(agent_key)
        if agent:
            has_claude = hasattr(agent, 'execute_with_claude')
            print(f"  {agent_key}: {'✅' if has_claude else '❌'} ({agent_type})")
        else:
            print(f"  {agent_key}: ❌ Not found")

    # Test 2: Verify YamlAgent has persona prompt builder
    print("\n2. Checking YAML agent features...")
    yaml_agent = core._agents.get('specialists_security-specialist')
    if yaml_agent:
        has_persona = hasattr(yaml_agent, '_build_persona_prompt')
        has_profile = hasattr(yaml_agent, '_select_mcp_profile')
        print(f"  Persona prompt builder: {'✅' if has_persona else '❌'}")
        print(f"  MCP profile selector: {'✅' if has_profile else '❌'}")

    # Test 3: Simple execution test ( DeveloperAgent with a simple task)
    print("\n3. Testing simple execution with DeveloperAgent...")
    result = await core.process_request(
        request="What is 2 + 2?",
        context={"forced_agent": "developer"}
    )

    # The result structure is: { "result": AgentResult, "routing": {...}, ... }
    agent_result = result.get("result", {})
    agent_metadata = agent_result.get("metadata", {})

    success = agent_result.get("success", False)
    execution_engine = agent_metadata.get("execution_engine", "unknown")

    print(f"  Success: {'✅' if success else '❌'}")
    print(f"  Execution Engine: {execution_engine}")

    if execution_engine == "claude-code-cli":
        print("\n" + "="*60)
        print("🎉 Claude Code CLI integration is working!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("⚠️  Execution engine not detected properly")
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
