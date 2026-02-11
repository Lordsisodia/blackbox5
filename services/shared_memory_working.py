#!/usr/bin/env python3
"""Simple Shared Memory Wrapper - WORKING VERSION"""

import redis
import json
import uuid
import os
import sys

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


class SimpleSharedMemory:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
                socket_keepalive=True
            )
        except Exception:
            print("[ERROR] Redis connection failed")
            self.redis = None
    
    def add_insight(self, content, category="pattern", confidence=0.9):
        if not self.redis:
            print("[ERROR] Redis not connected")
            return None
        
        try:
            insight_id = str(uuid.uuid4())
            timestamp = os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
            
            insight_data = {
                "id": insight_id,
                "namespace": "maltbot",
                "content": content,
                "category": category,
                "confidence": confidence,
                "timestamp": timestamp
            }
            
            insight_key = f"shared_memory:insight:{insight_id}"
            self.redis.hset(insight_key, "data", json.dumps(insight_data))
            
            category_key = f"shared_memory:category:maltbot:{category}"
            self.redis.sadd(category_key, insight_id)
            
            search_key = f"shared_memory:search:{insight_id}"
            self.redis.hset(search_key, "content", content)
            
            return insight_id
            
        except Exception:
            return None
    
    def get_insights(self, category=None, limit=10):
        if not self.redis:
            return []
        
        results = []
        
        try:
            if category:
                category_key = f"shared_memory:category:maltbot:{category}"
                insight_ids = list(self.redis.smembers(category_key))
                
                for insight_id in insight_ids[:limit]:
                    insight_key = f"shared_memory:insight:{insight_id}"
                    insight_json = self.redis.hget(insight_key)
                    if insight_json:
                        try:
                            results.append(json.loads(insight_json))
                        except:
                            pass
            
            else:
                pattern = f"shared_memory:insight:*"
                all_keys = list(self.redis.keys(pattern))
                
                for insight_key in all_keys[:limit]:
                    insight_json = self.redis.hget(insight_key)
                    if insight_json:
                        try:
                            results.append(json.loads(insight_json))
                        except:
                            pass
            
            return results
            
        except Exception:
            return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=REDIS_HOST)
    parser.add_argument("--port", type=int, default=REDIS_PORT)
    parser.add_argument("--add", help="Add an insight")
    parser.add_argument("--list", help="List insights")
    parser.add_argument("--category", help="Filter by category")
    
    args = parser.parse_args()
    memory = SimpleSharedMemory()
    
    # Test Redis
    try:
        memory.redis.ping()
        print(f"[INFO] Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except:
        print(f"[ERROR] Cannot connect to Redis at {REDIS_HOST}:{REDIS_PORT}")
        sys.exit(1)
    
    if args.add:
        print(f"\n[INFO] Adding insight: {args.add}")
        insight_id = memory.add_insight(content=args.add, category=args.category)
        if insight_id:
            print(f"[SUCCESS] Added insight: {insight_id}")
        else:
            print("[ERROR] Failed to add insight")
    
    if args.list:
        print(f"\n[INFO] Listing insights (category: {args.category})")
        insights = memory.get_insights(category=args.category, limit=10)
        print(f"[SUCCESS] Found {len(insights)} insights:")
        for insight in insights:
            print(f"  [{insight['category']}] {insight['content']}")


if __name__ == "__main__":
    main()
