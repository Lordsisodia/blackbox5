#!/usr/bin/env python3
"""
Test script to verify all 21 Blackbox5 agents use Claude Code CLI correctly.

This script tests:
1. Python agents (Developer, Architect, Analyst)
2. YAML specialist agents (18 agents)
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.core.base_agent import AgentTask
from infrastructure.main import Blackbox5


async def test_agent(name: str, description: str) -> dict:
    """Test a single agent."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Task: {description}")
    print(f"{'='*60}")

    try:
        # Initialize core system
        core = Blackbox5()

        # Process request with forced agent
        result = await core.process_request(
            request=description,
            context={"forced_agent": name}
        )

        # Extract metadata
        metadata = result.get("metadata", {})
        agent_result = metadata.get("agent_result", {})
        agent_metadata = agent_result.get("metadata", {})

        success = agent_result.get("success", False)
        execution_engine = agent_metadata.get("execution_engine", "unknown")
        mcp_profile = agent_metadata.get("mcp_profile", "unknown")
        duration = agent_metadata.get("duration", 0)

        print(f"\n✅ SUCCESS: {success}")
        print(f"📊 Execution Engine: {execution_engine}")
        print(f"🔧 MCP Profile: {mcp_profile}")
        print(f"⏱️  Duration: {duration:.2f}s")

        # Show first few lines of output
        output = agent_result.get("output", "")
        if output:
            lines = output.split('\n')[:5]
            print(f"\n📝 Output Preview:")
            for line in lines:
                print(f"   {line}")
            if len(output.split('\n')) > 5:
                print(f"   ... ({len(output.split(chr(10)))} total lines)")

        return {
            "name": name,
            "success": success,
            "engine": execution_engine,
            "profile": mcp_profile,
            "duration": duration,
            "has_output": bool(output)
        }

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": name,
            "success": False,
            "error": str(e)
        }


async def main():
    """Run all agent tests."""
    print("\n" + "="*60)
    print("Blackbox5 Agent Integration Test Suite")
    print("Testing all 21 agents with Claude Code CLI")
    print("="*60)

    # Test cases for each agent type
    test_cases = [
        # Python Agents
        {
            "name": "developer",
            "description": "Write a simple Python function to add two numbers",
            "expected_engine": "claude-code-cli"
        },
        {
            "name": "architect",
            "description": "Design a simple REST API architecture",
            "expected_engine": "claude-code-cli"
        },
        {
            "name": "analyst",
            "description": "Research the best practices for Python error handling",
            "expected_engine": "claude-code-cli"
        },
        # YAML Specialist Agents (sample)
        {
            "name": "security-specialist",
            "description": "What are the top security best practices for APIs?",
            "expected_engine": "claude-code-cli"
        },
        {
            "name": "frontend-specialist",
            "description": "Explain React component lifecycle best practices",
            "expected_engine": "claude-code-cli"
        },
        {
            "name": "backend-specialist",
            "description": "Design a database schema for a blog application",
            "expected_engine": "claude-code-cli"
        },
    ]

    # Run tests
    results = []
    for test in test_cases:
        result = await test_agent(test["name"], test["description"])
        result["expected_engine"] = test["expected_engine"]
        results.append(result)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    total = len(results)
    success_count = sum(1 for r in results if r["success"])
    engine_match = sum(1 for r in results if r.get("engine") == "claude-code-cli")

    print(f"\nTotal Tests: {total}")
    print(f"✅ Successful: {success_count}/{total}")
    print(f"🔧 Using Claude Code CLI: {engine_match}/{total}")

    print("\nDetailed Results:")
    print(f"{'Agent':<25} {'Success':<10} {'Engine':<20} {'Profile':<15} {'Duration':<10}")
    print("-" * 80)
    for r in results:
        name = r["name"][:24]
        success = "✅" if r["success"] else "❌"
        engine = r.get("engine", "unknown")[:19]
        profile = r.get("profile", "unknown")[:14]
        duration = f"{r.get('duration', 0):.1f}s"
        print(f"{name:<25} {success:<10} {engine:<20} {profile:<15} {duration:<10}")

    # Final verdict
    print("\n" + "="*60)
    if success_count == total and engine_match == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ All agents are using Claude Code CLI")
    else:
        print("⚠️  SOME TESTS FAILED")
        if success_count < total:
            print(f"   - {total - success_count} agents failed to execute")
        if engine_match < total:
            print(f"   - {total - engine_match} agents not using Claude Code CLI")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
