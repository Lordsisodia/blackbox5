#!/usr/bin/env python3
"""
Redis-Based Shared Memory Service
Provides shared memory storage and retrieval for multi-agent systems.
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


class SharedMemoryService:
    """Redis-based shared memory service for multi-agent systems."""
    
    def __init__(self):
        """Initialize Redis connection."""
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            socket_keepalive=True
        )
    
    def _ping(self) -> bool:
        """Test Redis connection."""
        try:
            return self.redis.ping()
        except redis.ConnectionError:
            return False
    
    def add_insight(self, namespace: str, content: str, category: str, confidence: float, metadata: Optional[Dict[str, Any]] = None) -> str:
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
            self.redis.hset(insight_key, "data", json.dumps(insight_data))
            
            category_key = f"shared_memory:category:{namespace}:{category}"
            self.redis.sadd(category_key, insight_id)
            
            search_key = f"shared_memory:search:{insight_id}"
            self.redis.hset(search_key, "content", content)
            
            return insight_id
            
        except Exception as e:
            raise Exception(f"Error adding insight {insight_id}: {e}")
    
    def query_shared(self, namespace: str, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Query shared memory for relevant insights."""
        results = []
        
        try:
            if category:
                category_key = f"shared_memory:category:{namespace}:{category}"
                insight_ids = list(self.redis.smembers(category_key))
                
                if insight_ids:
                    for insight_id in insight_ids[:limit]:
                        insight_key = f"shared_memory:insight:{insight_id}"
                        insight_json = self.redis.hget(insight_key)
                        if insight_json:
                            try:
                                results.append(json.loads(insight_json))
                            except:
                                pass
            
            else:
                query_lower = query.lower()
                search_key = f"shared_memory:search_index"
                
                try:
                    import redis.commands.search
                    has_search = True
                    
                    search_result = self.redis.ft_search(
                        index_name=search_key,
                        query=query,
                        limit=limit
                    )
                    
                    if hasattr(search_result, 'documents'):
                        doc_ids = [doc.id for doc in search_result.documents]
                    else:
                        doc_ids = []
                    
                    if doc_ids:
                        for doc_id in doc_ids:
                            doc_key = f"shared_memory:insight:{doc_id}"
                            doc_json = self.redis.hgetall(doc_key)
                            if doc_json:
                                for field_name, field_value in doc_json.items():
                                    if field_value:
                                        results.append(json.loads(field_value))
            
            return results
            
        except Exception as e:
            raise Exception(f"Error querying shared memory: {e}")
    
    def health_check(self) -> bool:
        """Check service health."""
        is_redis_up = self._ping()
        
        print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service Health:")
        print(f"  Redis: {is_redis_up}")
        
        if is_redis_up:
            pattern = f"shared_memory:insight:*"
            total = self.redis.scard(pattern)
            
            if total > 1000:
                print(f"  Total insights: {total} (consider cleanup)")
        
        return is_redis_up


def main():
    """Run shared memory service."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Shared Memory Service for Multi-Agent Systems")
    parser.add_argument("--host", default=REDIS_HOST, help="Redis host")
    parser.add_argument("--port", type=int, default=REDIS_PORT, help="Redis port")
    parser.add_argument("--health", action="store_true", help="Check Redis health")
    parser.add_argument("--test", action="store_true", help="Run tests")
    
    args = parser.parse_args()
    service = SharedMemoryService()
    
    if args.health:
        is_healthy = service.health_check()
        sys.exit(0 if is_healthy else 1)
    
    if args.test:
        print("\n=== Test 1: Add Insight ===")
        try:
            insight_id = service.add_insight(
                namespace="test-maltbot",
                content="Test pattern discovered",
                category="pattern",
                confidence=0.9
            )
            print(f"✓ Added insight {insight_id}")
        except Exception as e:
            print(f"✗ FAIL: {e}")
            sys.exit(1)
        
        print("\n=== Test 2: Query Insights ===")
        try:
            insights = service.query_shared(
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
                    break
            
            if found:
                print("✓ PASS: Insight storage and retrieval working")
            else:
                print("✗ FAIL: Insight not found")
                sys.exit(1)
            
        print("\n=== Test 3: Health Check ===")
        is_healthy = service.health_check()
        print(f"✓ PASS" if is_healthy else "✗ FAIL")
        sys.exit(0 if is_healthy else 1)
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Shared Memory Service on {args.host}:{args.port}")
    print("Use Ctrl+C to stop")
    
    import time
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
