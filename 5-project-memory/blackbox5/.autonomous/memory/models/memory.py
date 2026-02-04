"""
Data models for Hindsight Memory Architecture

Defines the core data structures for the 4-network memory system:
- World (W): Objective facts
- Experience (B): First-person actions
- Opinion (O): Beliefs with confidence
- Observation (S): Synthesized insights
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import json


class MemoryNetwork(Enum):
    """Hindsight's 4 memory networks"""
    WORLD = "world"           # Objective facts
    EXPERIENCE = "experience" # First-person actions
    OPINION = "opinion"       # Beliefs with confidence
    OBSERVATION = "observation"  # Synthesized summaries

    @classmethod
    def from_string(cls, value: str) -> "MemoryNetwork":
        """Create from string, case-insensitive"""
        mapping = {
            "world": cls.WORLD,
            "w": cls.WORLD,
            "experience": cls.EXPERIENCE,
            "b": cls.EXPERIENCE,  # Beta (experience)
            "opinion": cls.OPINION,
            "o": cls.OPINION,
            "observation": cls.OBSERVATION,
            "s": cls.OBSERVATION,  # Sigma (observation)
        }
        return mapping.get(value.lower(), cls.WORLD)


class MemoryCategory(Enum):
    """Categories for memories within networks"""
    # World categories
    TECHNICAL = "technical"
    DECISION = "decision"
    ENTITY = "entity"
    RELATIONSHIP = "relationship"

    # Experience categories
    ACTION = "action"
    INVESTIGATION = "investigation"
    IMPLEMENTATION = "implementation"
    LEARNING = "learning"
    INTERACTION = "interaction"

    # Opinion categories
    BELIEF = "belief"
    EVALUATION = "evaluation"
    PREFERENCE = "preference"
    STRATEGIC = "strategic"
    ETHICAL = "ethical"

    # Observation categories
    PATTERN = "pattern"
    SYNTHESIS = "synthesis"
    ANOMALY = "anomaly"
    PREDICTION = "prediction"
    CONNECTION = "connection"


@dataclass
class Memory:
    """
    Core memory unit for Hindsight architecture

    Represents a single memory across any of the 4 networks.
    Stored in PostgreSQL with vector embedding.
    """
    # Core fields
    id: Optional[str] = None  # UUID, auto-generated
    network: MemoryNetwork = MemoryNetwork.WORLD
    content: str = ""
    confidence: float = 0.8

    # Categorization
    category: Optional[str] = None  # MemoryCategory value
    subcategory: Optional[str] = None

    # Source tracking
    source: str = ""  # File path or task ID
    source_type: str = "task"  # task, run, thoughts, decisions, etc.
    task_id: Optional[str] = None
    run_id: Optional[str] = None

    # Temporal
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None  # For time-bounded memories

    # Content metadata
    entities: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None  # Vector embedding

    # Relationships (stored in Neo4j)
    related_memories: List[str] = field(default_factory=list)  # Memory IDs
    related_entities: List[str] = field(default_factory=list)  # Entity names

    # For opinions: belief tracking
    belief_version: int = 1  # Incremented on updates
    superseded_by: Optional[str] = None  # ID of newer version

    # For observations: evidence base
    evidence: List[Dict[str, Any]] = field(default_factory=list)

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Set defaults after initialization"""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "network": self.network.value,
            "content": self.content,
            "confidence": self.confidence,
            "category": self.category,
            "subcategory": self.subcategory,
            "source": self.source,
            "source_type": self.source_type,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "entities": self.entities,
            "keywords": self.keywords,
            "related_memories": self.related_memories,
            "belief_version": self.belief_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Memory":
        """Create from dictionary"""
        # Parse datetime fields
        for field_name in ["created_at", "updated_at", "valid_from", "valid_until"]:
            if data.get(field_name):
                if isinstance(data[field_name], str):
                    data[field_name] = datetime.fromisoformat(data[field_name].replace('Z', '+00:00'))

        # Parse network enum
        if "network" in data:
            data["network"] = MemoryNetwork.from_string(data["network"])

        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict(), indent=2, default=str)

    @classmethod
    def from_json(cls, json_str: str) -> "Memory":
        """Deserialize from JSON string"""
        return cls.from_dict(json.loads(json_str))


@dataclass
class Entity:
    """
    Entity extracted from memories

    Stored in Neo4j with relationships to memories and other entities.
    """
    id: Optional[str] = None
    name: str = ""
    type: str = "concept"  # person, organization, technology, concept, location, event
    aliases: List[str] = field(default_factory=list)

    # Metadata
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    mention_count: int = 0

    # Properties
    properties: Dict[str, Any] = field(default_factory=dict)

    # Source tracking
    sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.first_seen is None:
            self.first_seen = datetime.utcnow()
        if self.last_seen is None:
            self.last_seen = self.first_seen

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "aliases": self.aliases,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "mention_count": self.mention_count,
            "properties": self.properties,
        }


@dataclass
class Relationship:
    """
    Relationship between entities

    Stored as edges in Neo4j.
    """
    id: Optional[str] = None
    subject: str = ""  # Entity name or ID
    predicate: str = ""  # Relationship type
    object: str = ""  # Entity name or ID
    confidence: float = 0.8

    # Source
    source: str = ""  # Where this relationship was extracted from
    memory_id: Optional[str] = None  # Link to source memory

    # Temporal
    first_observed: Optional[datetime] = None
    last_observed: Optional[datetime] = None
    observation_count: int = 1

    # Properties
    properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.first_observed is None:
            self.first_observed = datetime.utcnow()
        if self.last_observed is None:
            self.last_observed = self.first_observed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "confidence": self.confidence,
            "source": self.source,
            "memory_id": self.memory_id,
            "observation_count": self.observation_count,
        }


@dataclass
class RecallQuery:
    """
    Query for RECALL operation

    Supports multi-strategy retrieval with filters.
    """
    query: str = ""  # Natural language query
    embedding: Optional[List[float]] = None  # Pre-computed embedding

    # Filters
    networks: List[MemoryNetwork] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    min_confidence: float = 0.0
    max_confidence: float = 1.0

    # Temporal filters
    since: Optional[datetime] = None
    until: Optional[datetime] = None

    # Source filters
    source_types: List[str] = field(default_factory=list)
    task_ids: List[str] = field(default_factory=list)

    # Retrieval options
    strategies: List[str] = field(default_factory=lambda: ["semantic", "keyword"])
    limit: int = 10
    offset: int = 0

    # RRF parameters
    rrf_k: int = 60  # Reciprocal Rank Fusion constant

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "networks": [n.value for n in self.networks] if self.networks else [],
            "categories": self.categories,
            "entities": self.entities,
            "min_confidence": self.min_confidence,
            "max_confidence": self.max_confidence,
            "since": self.since.isoformat() if self.since else None,
            "until": self.until.isoformat() if self.until else None,
            "strategies": self.strategies,
            "limit": self.limit,
        }


@dataclass
class RecallResult:
    """
    Result from RECALL operation

    Includes the memory and relevance scoring.
    """
    memory: Memory
    score: float  # Combined relevance score
    strategy_scores: Dict[str, float] = field(default_factory=dict)  # Per-strategy scores
    rank: int = 0  # Final rank after RRF

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory": self.memory.to_dict(),
            "score": self.score,
            "strategy_scores": self.strategy_scores,
            "rank": self.rank,
        }
