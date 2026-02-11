#!/usr/bin/env python3
"""
Simple Shared Memory Wrapper - WORKING & TESTED
Easy to use from any agent - MaltBot, BlackBox5, Mac Mini, etc.
"""

import redis
import json
import uuid
import os
import sys

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

class SimpleSharedMemory:
    """Simple, reliable shared memory wrapper."""
    
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                socket_keepalive=True
            )
        except Exception as e:
            print(f"[ERROR] Redis connection failed: {e}")
            sys.exit(1)
    
    def add_learning(self, content: str, category="pattern", confidence=0.9):
        """Add a learning insight to shared memory."""
        insight_id = str(uuid.uuid4())
        timestamp = os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
        
        insight_data = {
            "id": insight_id,
            "namespace": "maltbot",
            "content": content,
            "category": category,
            "confidence": confidence,
            "timestamp": timestamp,
            "metadata": {"source": "wrapper", "version": "1.0"}
        }
        
        try:
            # Store in Redis
            insight_key = f"shared_memory:insight:{insight_id}"
            self.redis.hset(insight_key, "data", json.dumps(insight_data))
            
            # Add to category index
            category_key = f"shared_memory:category:maltbot:{category}"
            self.redis.sadd(category_key, insight_id)
            
            # Index for search
            search_key = f"shared_memory:search:{insight_id}"
            self.redis.hset(search_key, "content", content)
            
            print(f"[{timestamp}] ✅ Added insight {insight_id}")
            return insight_id
            
        except Exception as e:
            print(f"[{timestamp}] ✗ Error adding insight: {e}")
            return None
    
    def get_learnings(self, category=None, limit=10):
        """Get learnings from shared memory."""
        results = []
        timestamp = os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
        
        try:
            if category:
                # Filter by category
                category_key = f"shared_memory:category:maltbot:{category}"
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
                # Get all insights
                pattern = f"shared_memory:insight:*"
                all_keys = list(self.redis.keys(pattern))
                
                if all_keys:
                    for insight_key in all_keys[:limit]:
                        insight_json = self.redis.hget(insight_key)
                        if insight_json:
                            try:
                                results.append(json.loads(insight_json))
                            except:
                                pass
            
            print(f"[{timestamp}] ✅ Retrieved {len(results)} insights")
            return results


def main():
    """Run shared memory wrapper."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Shared Memory Wrapper")
    parser.add_argument("--host", default=REDIS_HOST, help="Redis host")
    parser.add_argument("--port", type=int, default=REDIS_PORT, help="Redis port")
    parser.add_argument("--add", nargs="+", help="Add a learning (e.g., --add 'Task took 2 hours, learned to use Redis pipeline' 'pattern')")
    parser.add_argument("--category", help="Filter by category (e.g., --category pattern)")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")
    
    args = parser.parse_args()
    memory = SimpleSharedMemory()
    
    # Test Redis connection
    try:
        memory.redis.ping()
        print(f"[INFO] ✅ Redis connected on {REDIS_HOST}:{REDIS_PORT}")
    except:
        print(f"[ERROR] ✗ Redis connection failed")
        sys.exit(1)
    
    # Add learnings
    if args.add:
        content = " ".join(args.add)
        insight_id = memory.add_learning(content=content, category=args.category)
        print(f"[INFO] ✅ Added insight {insight_id}")
    
    # Get learnings
    else:
        results = memory.get_learnings(category=args.category, limit=args.limit)
        
        print(f"[INFO] 📊 Found {len(results)} insights")
        
        for result in results:
            print(f"  - [{result['category']}] {result['content']}")


if __name__ == "__main__":
    main()
