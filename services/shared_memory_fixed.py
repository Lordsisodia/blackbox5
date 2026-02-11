#!/usr/bin/env python3
"""
Redis-Based Shared Memory Service (FIXED)
Fixed query_shared function to avoid syntax errors.
"""

import redis
import json
import uuid
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


def add_insight(redis_client, namespace: str, content: str, category: str, confidence: float, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Add an insight to shared memory."""
    insight_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    insight_data = {
        "id": insight_id,
        "namespace": namespace,
        "content": content,
        "category": category,
        "confidence": confidence,
        "timestamp": timestamp,
        "metadata": metadata
    }
    
    try:
        insight_key = f"shared_memory:insight:{insight_id}"
        redis_client.hset(insight_key, "data", json.dumps(insight_data))
        
        category_key = f"shared_memory:category:{namespace}:{category}"
        redis_client.sadd(category_key, insight_id)
        
        search_key = f"shared_memory:search:{insight_id}"
        redis_client.hset(search_key, "content", content)
        
        print(f"[{timestamp}] Added insight {insight_id} to namespace {namespace}")
        return insight_id
            
    except Exception as e:
        print(f"[{timestamp}] Error adding insight {insight_id}: {e}")
        raise


def query_shared(redis_client, namespace: str, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Query shared memory for relevant insights."""
    results = []
    timestamp = datetime.now(timezone.utc).isoformat()
    
    try:
        if category:
            category_key = f"shared_memory:category:{namespace}:{category}"
            insight_ids = list(redis_client.smembers(category_key))
            
            if insight_ids:
                pipeline = redis_client.pipeline()
                for insight_id in insight_ids[:limit]:
                    insight_key = f"shared_memory:insight:{insight_id}"
                    insight_json = pipeline.hget(insight_key)
                    if insight_json:
                        results.append(json.loads(insight_json))
                pipeline.execute()
            
        else:
            query_lower = query.lower()
            search_key = f"shared_memory:search_index"
            
            try:
                import redis.commands.search
                has_search = True
            except ImportError:
                has_search = False
            
            if has_search:
                try:
                    search_result = redis_client.ft_search(
                        index_name=search_key,
                        query=query,
                        limit=limit
                    )
                    
                    if hasattr(search_result, 'documents'):
                        for doc in search_result.documents:
                            insight_key = f"shared_memory:insight:{doc.id}"
                            doc_json = redis_client.hgetall(insight_key)
                            
                            if doc_json:
                                for field_name, field_value in doc_json.items():
                                    if field_name == "data":
                                        results.append(json.loads(field_value))
                    else:
                        all_keys = list(redis_client.keys("shared_memory:insight:*"))
                        
                        if all_keys:
                            pipeline = redis_client.pipeline()
                            for insight_id in all_keys[:limit]:
                                insight_key = f"shared_memory:insight:{insight_id}"
                                doc_json = redis_client.hgetall(insight_key)
                                
                                if doc_json:
                                    for field_name, field_value in doc_json.items():
                                        if field_name == "data":
                                            results.append(json.loads(field_value))
                            pipeline.execute()
            
            print(f"[{timestamp}] Query complete: {len(results)} insights")
            return results
            
        except Exception as e:
            print(f"[{timestamp}] Error querying shared memory: {e}")
            raise


def health_check(redis_client):
    """Check service health."""
    try:
        return redis_client.ping()
    except:
        return False


def main():
    """Run shared memory service."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Shared Memory Service (Fixed)")
    parser.add_argument("--host", default=REDIS_HOST, help="Redis host")
    parser.add_argument("--port", type=int, default=REDIS_PORT, help="Redis port")
    parser.add_argument("--health", action="store_true", help="Check Redis health")
    parser.add_argument("--test", action="store_true", help="Run tests")
    
    args = parser.parse_args()
    redis_client = redis.Redis(
        host=args.host,
        port=args.port,
        db=REDIS_DB,
        decode_responses=True
    )
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Shared Memory Service on {args.host}:{args.port}")
    print("Use Ctrl+C to stop")
    
    if args.health:
        is_healthy = health_check(redis_client)
        print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service Health:")
        print(f"  Redis: {is_healthy}")
        
        if is_healthy:
            pattern = f"shared_memory:insight:*"
            total = redis_client.scard(pattern)
            
            if total > 1000:
                print(f"  Total insights: {total} (consider cleanup)")
        
        return
    
    if args.test:
        print("\n=== Test 1: Add Insight ===")
        try:
            insight_id = add_insight(
                redis_client=redis_client,
                namespace="test-maltbot",
                content="Test pattern discovered",
                category="pattern",
                confidence=0.9,
                metadata={"test": True, "source": "manual_test"}
            )
            print(f"✓ Added insight: {insight_id}")
        except Exception as e:
            print(f"✗ FAIL: {e}")
            sys.exit(1)
        
        print("\n=== Test 2: Query Insights ===")
        try:
            insights = query_shared(
                redis_client=redis_client,
                namespace="test-maltbot",
                query="pattern",
                category="pattern",
                limit=10
            )
            print(f"✓ Retrieved {len(insights)} insights")
            
            found = False
            for insight in insights:
                if insight.get('content') == "Test pattern discovered":
                    found = True
                    print(f"✓ Found our insight in results")
                    break
            
            if found:
                print("✓ PASS: Insight storage and retrieval working")
            else:
                print("✗ FAIL: Insight not found in query results")
                sys.exit(1)
        
        print("\n=== Test 3: Health Check ===")
        is_healthy = health_check(redis_client)
        if is_healthy:
            print("✅ PASS: Service is healthy")
        else:
            print("✗ FAIL: Service is unhealthy")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Shared Memory Service is working!")
        print("=" * 60)
        sys.exit(0)
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service running - waiting for API calls")
    
    import time
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
