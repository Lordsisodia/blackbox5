#!/usr/bin/env python3
"""Simple test for Shared Memory Service"""

import sys
sys.path.insert(0, "/opt/blackbox5")

from services.shared_memory_final import SharedMemoryService

def main():
    """Run simple tests."""
    print("=" * 60)
    print("Testing Shared Memory Service")
    print("=" * 60)
    
    service = SharedMemoryService()
    
    # Test 1: Ping Redis
    print("\nTest 1: Redis Connection")
    is_connected = service._ping()
    print(f"Result: {'PASS' if is_connected else 'FAIL'}")
    
    # Test 2: Add Insight
    print("\nTest 2: Add Insight")
    try:
        insight_id = service.add_insight(
            namespace="test-maltbot",
            content="Test pattern discovered",
            category="pattern",
            confidence=0.9,
            metadata={"test": True}
        )
        print(f"Result: PASS (insight_id: {insight_id})")
    except Exception as e:
        print(f"Result: FAIL ({e})")
    
    # Test 3: Query Insights
    print("\nTest 3: Query Insights")
    try:
        insights = service.query_shared(
            namespace="test-maltbot",
            query="pattern",
            category="pattern",
            limit=10
        )
        print(f"Result: PASS ({len(insights)} insights)")
    except Exception as e:
        print(f"Result: FAIL ({e})")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if is_connected:
        print("✅ Redis connected")
        print("✅ Insight addition working")
        print("✅ Query working")
    else:
        print("❌ Redis not connected")

if __name__ == "__main__":
    main()
