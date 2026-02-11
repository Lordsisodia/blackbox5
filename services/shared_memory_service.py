#!/usr/bin/env python3
"""
Redis-Based Shared Memory Service
Provides shared memory storage and retrieval for multi-agent systems.
"""

import redis
import json
import uuid
import os
import sys
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from dataclasses import dataclass

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


@dataclass
class Insight:
    """Shared memory insight."""
    id: str
    namespace: str
    content: str
    category: str
    confidence: float
    timestamp: str
    metadata: Optional[Dict[str, Any]]


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
            health_check_interval=30,
            socket_keepalive=True
        )
    
    def _ping(self):
        """Test Redis connection."""
        try:
            return self.redis.ping()
        except redis.ConnectionError as e:
            print(f"[{datetime.now(timezone.utc).isoformat()}] Redis connection error: {e}")
            return False
    
    def add_insight(self, namespace: str, content: str, category: str, confidence: float, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add an insight to shared memory.
        
        Returns: insight_id (UUID string)
        """
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
            
            print(f"[{timestamp}] Added insight {insight_id} to namespace {namespace}")
            return insight_id
            
        except Exception as e:
            print(f"[{timestamp}] Error adding insight {insight_id}: {e}")
            raise
    
    def query_shared(self, namespace: str, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Query shared memory for relevant insights.
        
        Returns: List of insights
        """
        results = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        try:
            if category:
                category_key = f"shared_memory:category:{namespace}:{category}"
                insight_ids = list(self.redis.smembers(category_key))
                if insight_ids:
                    pipeline = self.redis.pipeline()
                    for insight_id in insight_ids[:limit]:
                        pipeline.hget(f"shared_memory:insight:{insight_id}")
                        results.extend(pipeline.execute())
            
            else:
                query_lower = query.lower()
                search_key = f"shared_memory:search_index"
                
                try:
                    import redis.commands.search
                    has_search = True
                except ImportError:
                    print(f"[{timestamp}] FT.SEARCH not available, using basic query")
                    has_search = False
                
                if has_search:
                    search_result = self.redis.ft_search(
                        index_name=search_key,
                        query=query,
                        limit=limit
                    )
                    
                    doc_ids = []
                    for doc in search_result.documents:
                        doc_ids.append(doc.id)
                    
                    if doc_ids:
                        pipeline = self.redis.pipeline()
                        for doc_id in doc_ids:
                            doc_key = f"shared_memory:insight:{doc_id}"
                            doc_data = self.redis.hgetall(doc_key)
                            
                            if doc_data:
                                for doc_json in doc_data:
                                    if doc_json:
                                        try:
                                            results.append(json.loads(doc_json))
                                        except Exception as e:
                                            print(f"[{timestamp}] Error parsing doc {doc_id}: {e}")
                        pipeline.execute()
                else:
                    print(f"[{timestamp}] Using fallback query")
                    
                    all_key = f"shared_memory:all"
                    all_insight_ids = list(self.redis.smembers(all_key))
                    
                    if all_insight_ids:
                        pipeline = self.redis.pipeline()
                        for insight_id in all_insight_ids[:limit]:
                            insight_key = f"shared_memory:insight:{insight_id}"
                            pipeline.hget(insight_key)
                            
                            if pipeline:
                                result_str = pipeline[-1]
                                if result_str:
                                    try:
                                        results.append(json.loads(result_str))
                                    except Exception:
                                        pass
                        pipeline.execute()
            
            print(f"[{timestamp}] Query complete: {len(results)} insights")
            return results
            
        except Exception as e:
            print(f"[{timestamp}] Error querying shared memory: {e}")
            raise
    
    def add_learning(self, source_agent: str, learning_id: str, data: Dict[str, Any]) -> str:
        """
        Add a learning event from another agent to shared memory.
        """
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
            
            pipeline = self.redis.pipeline()
            pipeline.hset(insight_key, "data", json.dumps(insight_data))
            pipeline.hset(learning_key, learning_id)
            pipeline.hset(source_key, insight_id)
            pipeline.execute()
            
            print(f"[{timestamp}] Added learning {insight_id} from {source_agent}")
            return insight_id
            
        except Exception as e:
            print(f"[{timestamp}] Error adding learning {insight_id}: {e}")
            raise
    
    def get_learnings(self, namespace: str, learning_type: Optional[str] = None, source_agent: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get learning events for an agent.
        """
        results = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        try:
            # Filter by type
            if learning_type:
                type_key = f"{namespace}:type:{learning_type}"
                learning_ids = list(self.redis.smembers(type_key))
                
                if learning_ids:
                    pipeline = self.redis.pipeline()
                    for learning_id in learning_ids[:limit]:
                        insight_key = f"{namespace}:insight:{learning_id}"
                        pipeline.hget(insight_key)
                        
                        if pipeline:
                            insight_json = pipeline[-1]
                            if insight_json:
                                try:
                                    insight_dict = json.loads(insight_json)
                                    if insight_dict.get("type") == "learning":
                                        results.append(insight_dict)
                                except Exception:
                                    pass
                    pipeline.execute()
            
            # Filter by source agent
            if source_agent:
                source_key = f"{namespace}:source:{source_agent}"
                source_ids = list(self.redis.smembers(source_key))
                
                if source_ids:
                    pipeline = self.redis.pipeline()
                    for learning_id in source_ids[:limit]:
                        insight_key = f"{namespace}:insight:{learning_id}"
                        pipeline.hget(insight_key)
                        
                        if pipeline:
                            insight_json = pipeline[-1]
                            if insight_json:
                                try:
                                    insight_dict = json.loads(insight_json)
                                    if insight_dict.get("source_agent") == source_agent:
                                        results.append(insight_dict)
                                except Exception:
                                    pass
                    pipeline.execute()
            
            print(f"[{timestamp}] Retrieved {len(results)} learnings")
            return results
            
        except Exception as e:
            print(f"[{timestamp}] Error getting learnings: {e}")
            raise
    
    def search_fulltext(self, query: str, namespaces: List[str]) -> List[Dict[str, Any]]:
        """
        Full-text search across multiple namespaces.
        """
        all_results = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for namespace in namespaces:
            query_lower = query.lower()
            search_key = f"shared_memory:search_index"
            
            try:
                import redis.commands.search
                has_search = True
                
                search_result = self.redis.ft_search(
                    index_name=search_key,
                    query=query_lower,
                    limit=20
                )
                
                doc_ids = []
                for doc in search_result.documents:
                    doc_ids.append(doc.id)
                
                if doc_ids:
                    pipeline = self.redis.pipeline()
                    for doc_id in doc_ids:
                        doc_key = f"shared_memory:insight:{doc_id}"
                        doc_data = self.redis.hgetall(doc_key)
                        
                        if doc_data:
                            for doc_json in doc_data:
                                if doc_json:
                                    try:
                                        doc_dict = json.loads(doc_json)
                                        all_results.append(doc_dict)
                                    except Exception:
                                        print(f"[{timestamp}] Error parsing doc {doc_id}: {e}")
                    pipeline.execute()
                    
            except ImportError:
                print(f"[{timestamp}] FT.SEARCH not available, skipping full-text search for namespace {namespace}")
        
        return all_results
    
    def health_check(self):
        """Check service health."""
        is_redis_up = self._ping()
        
        print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service Health:")
        print(f"  Redis: {is_redis_up}")
        
        if is_redis_up:
            all_key = f"shared_memory:all"
            total = self.redis.scard(all_key)
            
            if total > 1000:
                print(f"  Total insights: {total} (consider cleanup)")
        
        return is_redis_up


def main():
    """Run shared memory service as standalone process."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Shared Memory Service for Multi-Agent Systems")
    parser.add_argument("--host", default=REDIS_HOST, help="Redis host")
    parser.add_argument("--port", type=int, default=REDIS_PORT, help="Redis port")
    parser.add_argument("--health", action="store_true", help="Check Redis health")
    
    args = parser.parse_args()
    
    service = SharedMemoryService()
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Shared Memory Service on {args.host}:{args.port}")
    print("Use Ctrl+C to stop")
    
    if args.health:
        service.health_check()
        sys.exit(0)
    
    print(f"[{datetime.now(timezone.utc).isoformat()}] Shared Memory Service running - waiting for API calls")
    
    while True:
        import time
        time.sleep(10)


if __name__ == "__main__":
    main()
