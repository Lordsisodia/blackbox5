#!/usr/bin/env python3
"""
Redis-Based Shared Memory Service
Simple version - no complex error handling.
"""

import redis
import json
import uuid
import os
from datetime import datetime, timezone

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


def add_insight(redis_client, namespace, content, category, confidence, metadata):
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
        
        print(f"[{timestamp}] Added insight {insight_id}")
        return insight_id
    except Exception as e:
        print(f"[{timestamp}] Error: {e}")
        return None


def query_shared(redis_client, namespace, query, category=None, limit=10):
    """Query shared memory for relevant insights."""
    results = []
    timestamp = datetime.now(timezone.utc).isoformat()
    
    try:
        if category:
            category_key = f"shared_memory:category:{namespace}:{category}"
            insight_ids = list(redis_client.smembers(category_key))
            
            for insight_id in insight_ids[:limit]:
                insight_key = f"shared_memory:insight:{insight_id}"
                insight_json = redis_client.hget(insight_key)
                if insight_json:
                    results.append(json.loads(insight_json))
        
        else:
            query_lower = query.lower()
            all_keys = list(redis_client.keys("shared_memory:insight:*"))
            
            for insight_key in all_keys:
                insight_json = redis_client.hget(insight_key)
                if insight_json:
                    insight = json.loads(insight_json)
                    content_lower = insight.get('content', '').lower()
                    if query_lower in content_lower:
                        results.append(insight)
                        if len(results) >= limit:
                            break
        
        return results
    except Exception as e:
        print(f"[{timestamp}] Error: {e}")
        return results


def health_check(redis_client):
    """Check Redis connection."""
    try:
        return redis_client.ping()
    except:
        return False


def main():
    """Run shared memory service."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Shared Memory Service")
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
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service on {args.host}:{args.port}")
    
    if args.health:
        is_redis_up = health_check(redis_client)
        print(f"[{datetime.now(timezone.utc).isoformat()}] Redis: {is_redis_up}")
        return
    
    if args.test:
        print("\n=== Testing Shared Memory Service ===")
        
        is_healthy = health_check(redis_client)
        if not is_healthy:
            print("❌ Redis connection failed. Cannot test.")
            return
        
        print("✅ Redis connection working")
        
        insight_id = add_insight(
            redis_client=redis_client,
            namespace="test-maltbot",
            content="Test pattern discovered",
            category="pattern",
            confidence=0.9,
            metadata={"test": True}
        )
        
        if insight_id:
            print(f"✅ Added insight: {insight_id}")
            
            insights = query_shared(
                redis_client=redis_client,
                namespace="test-maltbot",
                query="pattern",
                category="pattern",
                limit=10
            )
            
            print(f"✅ Retrieved {len(insights)} insights")
            
            found = False
            for insight in insights:
                if insight.get('content') == "Test pattern discovered":
                    found = True
                    print("✅ Found test insight")
                    break
            
            if found:
                print("✅ Test PASSED: Service is working!")
            else:
                print("❌ Test FAILED: Insight not found")
        else:
            print("❌ Insight creation failed")
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Service running...")
    
    import time
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
