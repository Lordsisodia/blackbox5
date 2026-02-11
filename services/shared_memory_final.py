#!/usr/bin/env python3
"""
Redis-Based Shared Memory Service
Simple, tested version for reliable operation.
"""

import redis
import json
import uuid
import os
import sys
from typing import List, Optional, Dict, Any
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
        print(f"[{timestamp}] Error adding insight {insight_id}: {e}")
        return None


def query_shared(redis_client, namespace, query, category=None, limit=10):
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
                    pipeline.hget(insight_key)
                results.extend(pipeline.execute())
        else:
            query_lower = query.lower()
            pattern = f"shared_memory:insight:*"
            all_insight_keys = list(redis_client.keys(pattern))
            
            if all_insight_keys:
                pipeline = redis_client.pipeline()
                for insight_id in all_insight_keys[:limit]:
                    insight_key = f"shared_memory:insight:{insight_id}"
                    insight_json = pipeline.hget(insight_key)
                    
                    if insight_json:
                        try:
                            insight_dict = json.loads(insight_json)
                            content_lower = insight_dict.get('content', '').lower()
                            if query_lower in content_lower:
                                results.append(insight_dict)
                        except Exception as e:
                            pass
                pipeline.execute()
            
        print(f"[{timestamp}] Query complete: {len(results)} insights")
        return results
            
    except Exception as e:
        print(f"[{timestamp}] Error querying shared memory: {e}")
        raise


def add_learning(redis_client, source_agent, learning_id, data):
    """Add a learning event from another agent."""
    insight_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    insight_data = {
        "id": insight_id,
        "namespace": "shared_memory",
        "source_agent": source_agent,
        "learning_id": learning_id,
        "type": "learning",
        "content": f"Learned from {source_agent}",
        "category": "learning",
        "confidence": 0.9,
        "timestamp": timestamp,
        "metadata": data
    }
    
    try:
        insight_key = f"shared_memory:insight:{insight_id}"
        learning_key = f"shared_memory:learning:{insight_id}"
        source_key = f"shared_memory:source:{source_agent}:{insight_id}"
        
        pipeline = redis_client.pipeline()
        pipeline.hset(insight_key, "data", json.dumps(insight_data))
        pipeline.hset(learning_key, learning_id)
        pipeline.hset(source_key, insight_id)
        pipeline.execute()
        
        print(f"[{timestamp}] Added learning {insight_id} from {source_agent}")
        return insight_id
            
    except Exception as e:
        print(f"[{timestamp}] Error adding learning {insight_id}: {e}")
        raise


def health_check(redis_client):
    """Check service health."""
    try:
        return redis_client.ping()
    except:
        return False


def main():
    """Run shared memory service."""
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service running on {REDIS_HOST}:{REDIS_PORT}")
    print("Use Ctrl+C to stop")
    
    import time
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
