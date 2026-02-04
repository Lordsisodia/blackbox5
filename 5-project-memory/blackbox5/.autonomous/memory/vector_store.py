#!/usr/bin/env python3
"""
Vector Store for Hindsight Memory

Hybrid approach: JSON storage + in-memory vectors
- Stores memories in JSON files (refactor-proof)
- Generates embeddings on-the-fly
- Keeps vectors in memory for fast similarity search
- Scales to ~10K memories before needing SQLite

Usage:
    store = VectorStore()
    store.add_memory(memory)
    results = store.search("query", top_k=5)
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class VectorMemory:
    """Memory with vector embedding"""
    id: str
    content: str
    network: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "network": self.network,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VectorMemory":
        return cls(
            id=data["id"],
            content=data["content"],
            network=data["network"],
            embedding=data.get("embedding"),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
        )


class VectorStore:
    """
    Vector store with JSON persistence and in-memory search.

    Stores memories as JSON files, loads vectors into memory for fast search.
    Generates embeddings on-demand if not cached.
    """

    def __init__(self, storage_dir: Optional[Path] = None, openai_api_key: Optional[str] = None):
        """
        Initialize vector store.

        Args:
            storage_dir: Directory for JSON storage (default: .autonomous/memory/data/)
            openai_api_key: OpenAI API key for embeddings (or set OPENAI_API_KEY env var)
        """
        if storage_dir is None:
            storage_dir = Path(__file__).parent / "data"

        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # OpenAI API key
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        # In-memory cache
        self.memories: Dict[str, VectorMemory] = {}
        self.vectors: Dict[str, np.ndarray] = {}

        # Embedding cache to avoid redundant API calls
        self._embedding_cache: Dict[str, np.ndarray] = {}
        self._cache_file = self.storage_dir / ".embedding_cache.json"
        self._load_embedding_cache()

        # Load existing memories
        self._load_all()

    def _load_all(self):
        """Load all memories from disk into memory"""
        json_file = self.storage_dir / "memories.json"
        if json_file.exists():
            with open(json_file) as f:
                data = json.load(f)
                for item in data:
                    memory = VectorMemory.from_dict(item)
                    self.memories[memory.id] = memory
                    if memory.embedding:
                        self.vectors[memory.id] = np.array(memory.embedding)

        print(f"Loaded {len(self.memories)} memories into vector store")

    def _save_all(self):
        """Save all memories to disk"""
        json_file = self.storage_dir / "memories.json"
        data = [m.to_dict() for m in self.memories.values()]
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content"""
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _load_embedding_cache(self):
        """Load embedding cache from disk"""
        if self._cache_file.exists():
            try:
                with open(self._cache_file) as f:
                    cache_data = json.load(f)
                    for text_hash, embedding_list in cache_data.items():
                        self._embedding_cache[text_hash] = np.array(embedding_list)
                print(f"Loaded {len(self._embedding_cache)} cached embeddings")
            except Exception as e:
                print(f"Warning: Could not load embedding cache: {e}")

    def _save_embedding_cache(self):
        """Save embedding cache to disk"""
        try:
            cache_data = {
                text_hash: embedding.tolist()
                for text_hash, embedding in self._embedding_cache.items()
            }
            with open(self._cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Warning: Could not save embedding cache: {e}")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text using OpenAI API.

        Falls back to simple hashing if OpenAI is not available.
        Uses caching to avoid redundant API calls.
        """
        # Check cache first
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash in self._embedding_cache:
            return self._embedding_cache[text_hash]

        # Try OpenAI if API key is available
        if self.openai_api_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.openai_api_key)

                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text[:8000],  # OpenAI limit
                )

                embedding = np.array(response.data[0].embedding)

                # Cache and save
                self._embedding_cache[text_hash] = embedding
                self._save_embedding_cache()

                return embedding

            except Exception as e:
                print(f"OpenAI embedding failed: {e}")
                print("Falling back to local embedding...")

        # Fallback: Simple bag-of-words embedding
        words = text.lower().split()
        embedding = np.zeros(384)
        for i, word in enumerate(words[:50]):
            idx = hash(word) % 384
            embedding[idx] += 1
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        # Cache even fallback embeddings
        self._embedding_cache[text_hash] = embedding

        return embedding

    def add_memory(self, content: str, network: str, metadata: Optional[Dict] = None) -> str:
        """
        Add a memory to the store.

        Args:
            content: Memory content
            network: Memory network (world/experience/opinion/observation)
            metadata: Optional metadata

        Returns:
            Memory ID
        """
        memory_id = self._generate_id(content)

        # Generate embedding
        embedding = self._generate_embedding(content)

        # Create memory
        memory = VectorMemory(
            id=memory_id,
            content=content,
            network=network,
            embedding=embedding.tolist(),
            metadata=metadata or {},
        )

        # Store in memory
        self.memories[memory_id] = memory
        self.vectors[memory_id] = embedding

        # Persist to disk
        self._save_all()

        return memory_id

    def search(self, query: str, top_k: int = 5, network: Optional[str] = None) -> List[Tuple[VectorMemory, float]]:
        """
        Search for similar memories.

        Args:
            query: Search query
            top_k: Number of results to return
            network: Filter by network (optional)

        Returns:
            List of (memory, similarity_score) tuples
        """
        if not self.memories:
            return []

        # Generate query embedding
        query_vec = self._generate_embedding(query)

        # Calculate similarities
        results = []
        for memory_id, memory in self.memories.items():
            # Filter by network if specified
            if network and memory.network != network:
                continue

            # Get vector
            vec = self.vectors.get(memory_id)
            if vec is None:
                continue

            # Cosine similarity
            norm_product = np.linalg.norm(query_vec) * np.linalg.norm(vec)
            if norm_product == 0:
                similarity = 0.0
            else:
                similarity = np.dot(query_vec, vec) / norm_product

            results.append((memory, float(similarity)))

        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def get_memory(self, memory_id: str) -> Optional[VectorMemory]:
        """Get a memory by ID"""
        return self.memories.get(memory_id)

    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory"""
        if memory_id in self.memories:
            del self.memories[memory_id]
            del self.vectors[memory_id]
            self._save_all()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics"""
        networks = {}
        for memory in self.memories.values():
            networks[memory.network] = networks.get(memory.network, 0) + 1

        # Calculate timeline
        dates = {}
        for memory in self.memories.values():
            date = memory.created_at[:10] if memory.created_at else "unknown"
            dates[date] = dates.get(date, 0) + 1

        # Get recent memories
        recent = sorted(
            self.memories.values(),
            key=lambda m: m.created_at or "",
            reverse=True
        )[:5]

        return {
            "total_memories": len(self.memories),
            "networks": networks,
            "storage_dir": str(self.storage_dir),
            "timeline": dates,
            "recent_memories": [
                {"id": m.id, "content": m.content[:80] + "...", "network": m.network, "created": m.created_at}
                for m in recent
            ],
            "embedding_cache_size": len(self._embedding_cache),
        }

    def get_all_memories(self) -> List[VectorMemory]:
        """Get all memories as a list"""
        return list(self.memories.values())

    def clear_cache(self):
        """Clear the embedding cache"""
        self._embedding_cache.clear()
        if self._cache_file.exists():
            self._cache_file.unlink()


# Simple CLI for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Vector Store CLI")
    parser.add_argument("--add", help="Add a memory")
    parser.add_argument("--network", default="observation", help="Memory network")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    args = parser.parse_args()

    store = VectorStore()

    if args.add:
        memory_id = store.add_memory(args.add, args.network)
        print(f"Added memory: {memory_id}")

    elif args.search:
        results = store.search(args.search, top_k=args.top_k)
        print(f"\nSearch results for: {args.search}\n")
        for i, (memory, score) in enumerate(results, 1):
            print(f"{i}. [{memory.network}] Score: {score:.3f}")
            print(f"   {memory.content[:100]}...")
            print()

    elif args.stats:
        stats = store.get_stats()
        print(f"Total memories: {stats['total_memories']}")
        print(f"By network: {stats['networks']}")

    else:
        parser.print_help()
