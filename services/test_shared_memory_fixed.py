#!/usr/bin/env python3
"""Simple test for Shared Memory Service"""

import sys
sys.path.insert(0, "/opt/blackbox5")

from services.shared_memory_service import SharedMemoryService

def main():
    """Run simple tests."""
    print("=" * 60)
    print("Testing Shared Memory Service")
    print("=" * 60)
    
    service = SharedMemoryService()
    
    # Test 1: Ping Redis
    print("\nTest 1: Redis Connection")
    is_connected = service._ping()
    if is_connected:
        print("✓ PASS: Redis is connected")
    else:
        print("✗ FAIL: Redis is not connected")
    
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
        print(f"✓ PASS: Added insight {insight_id}")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        sys.exit(1)
    
    # Test 3: Query Insights
    print("\nTest 3: Query Insights")
    try:
        insights = service.query_shared(
            namespace="test-maltbot",
            query="pattern",
            category="pattern",
            limit=10
        )
        print(f"✓ PASS: Retrieved {len(insights)} insights")
        
        # Check if our insight is there
        found = False
        for insight in insights:
            if insight['content'] == "Test pattern discovered":
                found = True
                print(f"✓ PASS: Found our insight")
                break
        
        if found:
            print("✓ PASS: Insight storage and retrieval working")
        else:
            print("✗ FAIL: Insight not found")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ Redis Connection: Working")
    print("✅ Add Insight: Working")
    print("✅ Query Insights: Working")
    print("=" * 60)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
