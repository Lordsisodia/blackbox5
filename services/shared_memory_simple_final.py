#!/usr/bin/env python3
"""Simple Shared Memory Wrapper - FINAL VERSION"""

import redis
import json
import os
import sys
import subprocess

REDIS_HOST = "localhost"
REDIS_PORT = 6379


class SimpleSharedMemory:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                socket_keepalive=True
            )
        except Exception:
            self.redis = None
            print("[ERROR] Redis connection failed")
    
    def add_insight(self, content, category="pattern", confidence=0.9):
        if not self.redis:
            print("[ERROR] Redis not connected")
            return None
        
        try:
            import uuid
            insight_id = str(uuid.uuid4())
            
            insight_data = {
                "id": insight_id,
                "namespace": "maltbot",
                "content": content,
                "category": category,
                "confidence": confidence,
                "timestamp": subprocess.getoutput("date -u +\"%Y-%m-%dT%H:%M:%SZ\"").strip()
            }
            
            insight_key = f"shared_memory:insight:{insight_id}"
            self.redis.hset(insight_key, "data", json.dumps(insight_data))
            
            cat_key = f"shared_memory:category:maltbot:{category}"
            self.redis.sadd(cat_key, insight_id)
            
            search_key = f"shared_memory:search:{insight_id}"
            self.redis.hset(search_key, "content", content)
            
            return insight_id
        
        except Exception as e:
            return None
    
    def get_insights(self, category=None, limit=10):
        if not self.redis:
            return []
        
        try:
            insights = []
            
            if category:
                cat_key = f"shared_memory:category:maltbot:{category}"
                insight_ids = list(self.redis.smembers(cat_key))
                
                for insight_id in insight_ids[:limit]:
                    insight_key = f"shared_memory:insight:{insight_id}"
                    insight_json = self.redis.hget(insight_key)
                    if insight_json:
                        insights.append(json.loads(insight_json))
            
            else:
                pattern = f"shared_memory:insight:*"
                all_keys = list(self.redis.keys(pattern))
                
                for insight_key in all_keys[:limit]:
                    insight_json = self.redis.hget(insight_key)
                    if insight_json:
                        insights.append(json.loads(insight_json))
            
            return insights
        
        except Exception:
            return []


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", help="Add an insight")
    parser.add_argument("--list", help="List insights")
    parser.add_argument("--category", help="Filter by category")
    
    args = parser.parse_args()
    memory = SimpleSharedMemory()
    
    print("=== Simple Shared Memory Wrapper ===")
    
    if args.add:
        insight_id = memory.add_insight(content=args.add, category=args.category)
        if insight_id:
            print(f"[SUCCESS] Added insight: {insight_id}")
        else:
            print("[ERROR] Failed to add insight")
    
    if args.list:
        insights = memory.get_insights(category=args.category)
        print(f"[SUCCESS] Found {len(insights)} insights")
        for insight in insights:
            print(f"  [{insight['category']}] {insight['content']}")


if __name__ == "__main__":
    main()
