#!/usr/bin/env python3
"""
Test script for Shared Memory Service
Verifies basic functionality of Redis-based shared memory.
"""

import sys
sys.path.insert(0, "/opt/blackbox5")

from services.shared_memory_service import SharedMemoryService

def test_redis_connection():
    """Test Redis connection."""
    print("\n=== Test 0: Redis Connection ===")
    
    service = SharedMemoryService()
    
    # Test connection via ping
    is_connected = service._ping()
    
    if is_connected:
        print("✓ PASS: Redis connection working")
    else:
        print("✗ FAIL: Redis connection failed")
    
    return is_connected

def test_add_insight():
    """Test adding an insight to shared memory."""
    print("\n=== Test 1: Add Insight ===")
    
    service = SharedMemoryService()
    
    # Add a test insight
    insight_id = service.add_insight(
        namespace="test-maltbot",
        content="Test pattern discovered",
        category="pattern",
        confidence=0.9,
        metadata={"test": True, "source": "manual_test"}
    )
    
    print(f"✓ PASS: Added insight {insight_id}")
    
    # Verify by retrieving
    import time
    time.sleep(0.1)
    
    insights = service.query_shared(
        namespace="test-maltbot",
        query="pattern",
        category="pattern",
        limit=10
    )
    
    print(f"✓ PASS: Retrieved {len(insights)} insights")
    
    # Verify our insight is in results
    found = False
    for insight in insights:
        if insight['content'] == "Test pattern discovered":
            found = True
            print(f"✓ PASS: Found our insight in results")
            break
    
    if found:
        print("✓ PASS: Insight storage and retrieval working")
    else:
        print("✗ FAIL: Insight not found in query results")
    
    return found

def test_query_all():
    """Test querying all insights (no category filter)."""
    print("\n=== Test 2: Query All (No Category) ===")
    
    service = SharedMemoryService()
    
    # Query all insights in test-maltbot namespace (no category filter)
    insights = service.query_shared(
        namespace="test-maltbot",
        query="",  # No query to get all
        limit=10
    )
    
    print(f"✓ PASS: Retrieved {len(insights)} insights")
    
    return len(insights) > 0

def main():
    """Run all tests."""
    print("=" * 60)
    print("Shared Memory Service - Test Suite")
    print("=" * 60)
    
    # Run all tests
    results = []
    
    results.append(("Redis Connection", test_redis_connection()))
    results.append(("Add Insight", test_add_insight()))
    results.append(("Query All", test_query_all()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Shared Memory Service is working!")
    else:
        print("✗ SOME TESTS FAILED - Check Redis connection")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
