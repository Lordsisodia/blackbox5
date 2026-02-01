# Black Box 5 Skills Integration Plan

**Date**: 2026-01-28
**Version**: 1.0.0
**Status**: Ready for Implementation
**Owner**: SISO Internal Team

---

## Executive Summary

This plan outlines how to integrate the Agent Skills Standard into Black Box 5's agent system, enabling agents to discover, load, and use skills efficiently while maintaining the existing Python-based engine skills.

**Goal**: Enable BB5 agents to use both Tier 1 (engine) and Tier 2 (Agent Skills Standard) skills seamlessly.

**Timeline**: 4 weeks (1 month)
**Effort**: Medium (requires engine modifications + skill conversion)

---

## Current State Analysis

### Existing Agent System

**Agent Types**:
- **Amelia 💻** (Developer): Implementation, debugging, testing
- **Mary 📊** (Analyst): Research, analysis, data insights
- **Alex 🏗️** (Architect): System design, architecture, patterns
- **John 📋** (Product Manager): PRDs, epics, requirements

**Current Skill Access**:
- Engine skills: Via SkillManager (Python API)
- Agent skills: Via filesystem reads (manual)
- MCP skills: Via MCP server integration

**Issues**:
- No unified skill discovery
- No on-demand loading (token inefficient)
- No Agent Skills Standard compatibility
- Manual skill loading process

### Target State

**What We Want**:
1. Agents discover skills automatically
2. Skills loaded on-demand (token efficient)
3. Agents use both engine and Agent Skills Standard
4. Seamless integration with Claude Code
5. Unified skill interface

---

## Integration Architecture

### Two-Tier Skills System

```
┌─────────────────────────────────────────────────────────────────┐
│                     Black Box 5 Agent                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Skill Orchestration Layer (NEW)                      │    │
│  │  ────────────────────────────────────────────────────  │    │
│  │  • Unified skill discovery                             │    │
│  │  • On-demand loading (token efficient)                │    │
│  │  • Skill routing (Tier 1 vs Tier 2)                   │    │
│  │  • Caching and context management                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                          ↕                                      │
│           ┌──────────────┴──────────────┐                    │
│           ↓                             ↓                    │
│  ┌─────────────────────┐   ┌─────────────────────────┐    │
│  │  Tier 1: Engine     │   │  Tier 2: Agent Skills   │    │
│  │  Skills            │   │  (Agent Skills Standard)│    │
│  ├─────────────────────┤   ├─────────────────────────┤    │
│  │ • SkillManager     │   │ • ~/.claude/skills/     │    │
│  │ • Python classes   │   │ • SKILL.md files       │    │
│  │ • JSON metadata    │   │ • YAML frontmatter     │    │
│  │ • Runtime import   │   │ • On-demand load       │    │
│  │ • Engine-internal  │   │ • Cross-platform       │    │
│  └─────────────────────┘   └─────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Skill Loading Flow

```
Agent Request
     │
     ↓
┌─────────────────┐
│ Skill Discovery  │ ← Check both tiers
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌────────────┐
│ Tier 1 │ │  Tier 2    │
│ Skills │ │  Skills    │
└────┬────┘ └─────┬──────┘
     │            │
     ↓            ↓
┌─────────────────────────┐
│ Skill Orchestration     │
│ • Load skill            │
│ • Inject context        │
│ • Cache for reuse      │
└─────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

#### 1.1 Create Skill Orchestration Layer

**File**: `2-engine/02-orchestration/skills/orchestrator.py`

**Purpose**: Unified skill discovery and loading

**Key Features**:
- Scan both Tier 1 and Tier 2 skill directories
- Parse YAML frontmatter from SKILL.md files
- Maintain skill registry (metadata)
- Route skill requests to appropriate tier
- Implement on-demand loading
- Cache loaded skills

**Interface**:
```python
class SkillOrchestrator:
    """Unified skill discovery and loading"""

    def __init__(self):
        self.tier1_manager = SkillManager()  # Existing
        self.tier2_scanner = SkillScanner()   # New
        self.skill_cache = {}                  # New
        self.skill_registry = {}               # New

    async def discover_skills(self) -> List[SkillMetadata]:
        """Discover all skills from both tiers"""
        pass

    async def load_skill(self, skill_name: str) -> str:
        """Load skill content on-demand"""
        pass

    async def search_skills(self, query: str) -> List[SkillMetadata]:
        """Search skills by name, description, tags"""
        pass

    def get_skill_for_agent(self, agent_name: str,
                           task: str) -> Optional[str]:
        """Get appropriate skill for agent and task"""
        pass
```

#### 1.2 Create Skill Scanner for Tier 2

**File**: `2-engine/02-orchestration/skills/scanner.py`

**Purpose**: Scan and parse Agent Skills Standard files

**Key Features**:
- Scan `~/.claude/skills/` directory
- Parse YAML frontmatter
- Extract metadata (name, description, tags)
- Index skills for search
- Validate SKILL.md format

**Interface**:
```python
class SkillScanner:
    """Scan and parse Agent Skills Standard files"""

    def __init__(self, skills_path: Path = Path("~/.claude/skills")):
        self.skills_path = skills_path.expanduser()
        self.skill_index = {}

    async def scan_all(self) -> Dict[str, SkillMetadata]:
        """Scan all skills and build index"""
        pass

    async def parse_skill(self, skill_path: Path) -> SkillMetadata:
        """Parse SKILL.md file and extract metadata"""
        pass

    async def load_skill_content(self, skill_name: str) -> str:
        """Load full skill content"""
        pass

    def search(self, query: str) -> List[SkillMetadata]:
        """Search skills by name, description, tags"""
        pass
```

#### 1.3 Create Skills Directory Structure

**Actions**:
```bash
# Create global skills directory
mkdir -p ~/.claude/skills

# Create project-specific skills directory
mkdir -p blackbox5/.claude/skills

# Create engine skills directory (if not exists)
mkdir -p blackbox5/2-engine/01-core/agents/skills
```

**Documentation**:
- Document directory structure
- Explain when to use global vs project-specific
- Provide examples

#### 1.4 Update Agent Configuration

**File**: `2-engine/01-core/agents/base/agent.py`

**Changes**:
- Add `skill_orchestrator` to agent initialization
- Add `load_skill()` method to agent interface
- Add `use_skill()` method for skill execution
- Update agent prompt to include skill availability

**Interface**:
```python
class Agent:
    """Base agent class with skill support"""

    def __init__(self, ...):
        # Existing initialization
        self.skill_orchestrator = SkillOrchestrator()

    async def load_skill(self, skill_name: str) -> str:
        """Load skill and inject into context"""
        pass

    async def use_skill(self, skill_name: str,
                       task: str) -> AgentResponse:
        """Use skill to complete task"""
        pass

    def get_available_skills(self) -> List[str]:
        """Get list of available skills"""
        pass
```

**Deliverables**:
- ✅ SkillOrchestrator implementation
- ✅ SkillScanner implementation
- ✅ Directory structure created
- ✅ Agent base class updated
- ✅ Unit tests for orchestration layer

---

### Phase 2: Skill Conversion (Week 2)

#### 2.1 Convert High-Priority Skills

**Skills to Convert** (Priority Order):

1. **supabase-operations**
   - Source: `supabase-ddl-rls.md`
   - Target: `~/.claude/skills/supabase-operations/SKILL.md`
   - Type: Database operations
   - Complexity: Medium

2. **siso-tasks-cli**
   - Source: `siso-tasks/` (MCP-based)
   - Target: `~/.claude/skills/siso-tasks-cli/SKILL.md`
   - Type: MCP-to-CLI conversion
   - Complexity: High

3. **feedback-triage**
   - Source: `feedback-triage.md`
   - Target: `~/.claude/skills/feedback-triage/SKILL.md`
   - Type: Process/workflow
   - Complexity: Low (already structured)

4. **git-workflows**
   - Source: `repo-codebase-navigation.md`
   - Target: `~/.claude/skills/git-workflows/SKILL.md`
   - Type: Development workflow
   - Complexity: Medium

5. **testing-patterns**
   - Source: `testing-playbook.md`
   - Target: `~/.claude/skills/testing-patterns/SKILL.md`
   - Type: Testing workflow
   - Complexity: Medium

6. **notifications-local**
   - Source: `notifications-local.md`
   - Target: `~/.claude/skills/notifications-local/SKILL.md`
   - Type: Integration
   - Complexity: Low

**Conversion Process** (Per Skill):
```bash
# 1. Create skill directory
mkdir -p ~/.claude/skills/<skill-name>

# 2. Create SKILL.md
# (Use template from migration guide)

# 3. Add supporting files
mkdir -p ~/.claude/skills/<skill-name>/{scripts,examples,templates}

# 4. Test with Claude Code
claude-code "Use the <skill-name> skill to..."

# 5. Verify in registry
python -m blackbox5.skills.registry list
```

**Deliverables**:
- ✅ 6 converted skills (SKILL.md format)
- ✅ Supporting files (templates, examples)
- ✅ Test results for each skill
- ✅ Updated skills registry

#### 2.2 Create Multi-Project Supabase Skills

**Challenge**: Multiple Supabase projects with different credentials

**Solution**: Environment-specific skills

**Structure**:
```
~/.claude/skills/
├── supabase-project1/
│   ├── SKILL.md
│   └── env.sh
├── supabase-project2/
│   ├── SKILL.md
│   └── env.sh
└── supabase-common/
    ├── SKILL.md
    └── scripts/
        └── supabase-wrapper.sh
```

**Skill Template**:
```yaml
---
name: supabase-project1
description: Supabase operations for Project1
tags: [supabase, project1, production]
project_id: proj1_***
env_file: ~/.supabase/project1.env
---

# Supabase Project1

## Environment Setup
```bash
source ~/.claude/skills/supabase-project1/env.sh
```

## Commands
### Database Push
```bash
supabase-wrapper.sh project1 db push
```
```

**Deliverables**:
- ✅ Per-project Supabase skills
- ✅ Environment configuration files
- ✅ CLI wrapper script
- ✅ Documentation

#### 2.3 Create Skill Templates

**File**: `blackbox5/1-docs/02-implementation/06-tools/skills/SKILLS-TEMPLATES.md`

**Templates to Create**:

1. **Basic Skill Template**
   - YAML frontmatter
   - Content structure
   - Common sections

2. **Database Operations Template**
   - Commands for CRUD
   - Migration workflows
   - Troubleshooting

3. **Development Workflow Template**
   - Git commands
   - Testing procedures
   - Debugging workflows

4. **Process/Workflow Template**
   - Step-by-step procedures
   - Decision trees
   - Checklists

5. **Integration Template**
   - API interactions
   - Webhook handling
   - Third-party services

**Deliverables**:
- ✅ 5 skill templates
- ✅ Template documentation
- ✅ Usage examples

---

### Phase 3: Agent Integration (Week 3)

#### 3.1 Update Agent Prompts

**File**: `2-engine/01-core/agents/prompts/base_prompt.py`

**Add to System Prompt**:
```python
SKILLS_SYSTEM_PROMPT = """
## Available Skills

You have access to skills that help you complete tasks more effectively.

### How to Use Skills

1. **Discover Skills**: Ask "What skills are available?" to see all skills
2. **Load Skill**: Ask "Load the <skill-name> skill" to load a skill
3. **Use Skill**: Ask "Use the <skill-name> skill to <task>" to use a skill

### Skill Categories

- **Database Operations**: Supabase, SQL, migrations
- **Development**: Git workflows, testing, debugging
- **Process**: Feedback triage, planning, documentation
- **Integration**: Notifications, APIs, webhooks

### When to Use Skills

- When you need specific domain knowledge
- When following established workflows
- When using tools you're not familiar with
- When you need step-by-step guidance

### Skill Loading

Skills are loaded on-demand when you need them. This saves tokens and keeps your context focused.

### Available Skills

{SKILL_LIST}
"""
```

**Deliverables**:
- ✅ Updated system prompt
- ✅ Skill usage instructions
- ✅ Dynamic skill list generation

#### 3.2 Implement Skill Loading in Agents

**File**: `2-engine/01-core/agents/base/agent.py`

**Add Methods**:
```python
class Agent:
    async def load_skill(self, skill_name: str) -> bool:
        """
        Load a skill and inject into context.

        Args:
            skill_name: Name of skill to load

        Returns:
            True if loaded successfully, False otherwise
        """
        skill_metadata = await self.skill_orchestrator.discover_skill(skill_name)
        if not skill_metadata:
            return False

        skill_content = await self.skill_orchestrator.load_skill(skill_name)
        if not skill_content:
            return False

        # Inject into agent context
        self.context.add_skill(skill_name, skill_content)
        return True

    async def use_skill(self, skill_name: str, task: str) -> AgentResponse:
        """
        Use a skill to complete a task.

        Args:
            skill_name: Name of skill to use
            task: Task description

        Returns:
            Agent response with skill execution results
        """
        # Load skill if not already loaded
        if skill_name not in self.context.skills:
            if not await self.load_skill(skill_name):
                return AgentResponse.error(f"Skill not found: {skill_name}")

        # Execute task with skill context
        response = await self.execute_with_skill(task, skill_name)
        return response

    def get_available_skills(self) -> List[SkillMetadata]:
        """Get list of available skills for this agent"""
        all_skills = await self.skill_orchestrator.discover_skills()
        # Filter by agent type and permissions
        return self._filter_skills_for_agent(all_skills)
```

**Deliverables**:
- ✅ Skill loading implementation
- ✅ Skill usage implementation
- ✅ Context management updates
- ✅ Error handling

#### 3.3 Create Agent-Specific Skill Mappings

**File**: `2-engine/02-orchestration/skills/mappings.py`

**Purpose**: Map skills to agent types

**Configuration**:
```python
AGENT_SKILL_MAPPINGS = {
    "amelia": {  # Developer
        "required": ["git-workflows", "testing-patterns", "supabase-operations"],
        "optional": ["debugging-systematic", "code-generation"]
    },
    "mary": {  # Analyst
        "required": ["data-analysis", "reporting", "visualization"],
        "optional": ["statistics", "research-methods"]
    },
    "alex": {  # Architect
        "required": ["system-design", "architecture-patterns", "documentation"],
        "optional": ["design-patterns", "tech-stack-decisions"]
    },
    "john": {  # Product Manager
        "required": ["feedback-triage", "feature-planning", "prd-creation"],
        "optional": ["stakeholder-management", "roadmap-planning"]
    }
}
```

**Deliverables**:
- ✅ Agent-skill mappings
- ✅ Skill assignment logic
- ✅ Permission system

#### 3.4 Implement Skill Caching

**File**: `2-engine/02-orchestration/skills/cache.py`

**Purpose**: Cache loaded skills for efficiency

**Interface**:
```python
class SkillCache:
    """Cache for loaded skills"""

    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}

    async def get(self, skill_name: str) -> Optional[str]:
        """Get skill from cache"""
        pass

    async def put(self, skill_name: str, content: str) -> None:
        """Put skill in cache"""
        pass

    async def invalidate(self, skill_name: str) -> None:
        """Invalidate cached skill"""
        pass

    def clear(self) -> None:
        """Clear all cache"""
        pass
```

**Caching Strategy**:
- LRU eviction policy
- TTL for skill content (1 hour)
- Size limit (100 skills max)
- Invalidation on skill update

**Deliverables**:
- ✅ SkillCache implementation
- ✅ Cache integration with orchestrator
- ✅ Cache statistics

---

### Phase 4: Testing & Optimization (Week 4)

#### 4.1 Create Skill Testing Framework

**File**: `2-engine/tests/skills/test_skills.py`

**Purpose**: Test skill discovery, loading, and usage

**Test Cases**:
```python
class TestSkillOrchestrator:
    def test_discover_tier1_skills(self):
        """Test Tier 1 skill discovery"""
        pass

    def test_discover_tier2_skills(self):
        """Test Tier 2 skill discovery"""
        pass

    def test_load_skill_on_demand(self):
        """Test on-demand skill loading"""
        pass

    def test_skill_caching(self):
        """Test skill caching"""
        pass

    def test_skill_search(self):
        """Test skill search functionality"""
        pass

class TestAgentSkillUsage:
    def test_agent_loads_skill(self):
        """Test agent can load skills"""
        pass

    def test_agent_uses_skill(self):
        """Test agent can use skills"""
        pass

    def test_agent_skill_context(self):
        """Test skill context injection"""
        pass
```

**Deliverables**:
- ✅ Test suite for skills
- ✅ Test suite for agents
- ✅ Integration tests
- ✅ Performance tests

#### 4.2 Measure Token Efficiency

**Metrics to Track**:
1. Token usage before vs after
2. Skill load time
3. Cache hit rate
4. Agent response time
5. Error rate

**Benchmark Tests**:
```python
async def benchmark_skill_loading():
    """Benchmark skill loading performance"""

    # Test 1: Load skill without cache
    start = time.time()
    await orchestrator.load_skill("supabase-operations")
    no_cache_time = time.time() - start

    # Test 2: Load skill with cache
    start = time.time()
    await orchestrator.load_skill("supabase-operations")
    cache_time = time.time() - start

    # Test 3: Token usage
    tokens_before = count_tokens(agent.context)
    await agent.use_skill("supabase-operations", task)
    tokens_after = count_tokens(agent.context)
    tokens_used = tokens_after - tokens_before

    return {
        "no_cache_time": no_cache_time,
        "cache_time": cache_time,
        "tokens_used": tokens_used
    }
```

**Deliverables**:
- ✅ Benchmark suite
- ✅ Performance metrics
- ✅ Optimization report

#### 4.3 Create Skill Analytics

**File**: `2-engine/02-orchestration/skills/analytics.py`

**Purpose**: Track skill usage and effectiveness

**Metrics**:
- Skill discovery rate
- Skill loading success rate
- Skill usage frequency
- Token usage per skill
- Agent satisfaction

**Interface**:
```python
class SkillAnalytics:
    """Track and analyze skill usage"""

    async def track_skill_discovery(self, skill_name: str,
                                   agent: str, success: bool):
        """Track skill discovery attempt"""
        pass

    async def track_skill_load(self, skill_name: str,
                             agent: str, load_time: float):
        """Track skill load"""
        pass

    async def track_skill_usage(self, skill_name: str,
                              agent: str, task: str,
                              success: bool, duration: float):
        """Track skill usage"""
        pass

    async def generate_report(self, period: str) -> SkillReport:
        """Generate usage report"""
        pass
```

**Deliverables**:
- ✅ Analytics implementation
- ✅ Usage dashboard
- ✅ Monthly reports

#### 4.4 Documentation & Training

**Documentation to Create**:

1. **Agent Developer Guide**
   - How to create agent-compatible skills
   - How to map skills to agents
   - Best practices for skill design

2. **Agent User Guide**
   - How agents use skills
   - How to request skills
   - How to provide feedback

3. **System Administrator Guide**
   - How to deploy skills
   - How to monitor skill usage
   - How to troubleshoot issues

**Deliverables**:
- ✅ Developer guide
- ✅ User guide
- ✅ Admin guide
- ✅ Training materials

---

## Implementation Details

### Skill Orchestration Layer

**File**: `2-engine/02-orchestration/skills/orchestrator.py`

**Complete Implementation**:
```python
"""
Skill Orchestration Layer for Black Box 5

Provides unified skill discovery and loading for both
Tier 1 (engine) and Tier 2 (Agent Skills Standard) skills.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..tier1.skill_manager import SkillManager
from .scanner import SkillScanner
from .cache import SkillCache
from .analytics import SkillAnalytics

logger = logging.getLogger(__name__)


@dataclass
class SkillMetadata:
    """Metadata for a skill"""
    name: str
    tier: str  # "tier1" or "tier2"
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    author: str = ""
    file_path: Optional[Path] = None
    last_modified: Optional[datetime] = None

    def matches_query(self, query: str) -> bool:
        """Check if skill matches search query"""
        query_lower = query.lower()
        return (
            query_lower in self.name.lower() or
            query_lower in self.description.lower() or
            any(query_lower in tag.lower() for tag in self.tags)
        )


class SkillOrchestrator:
    """
    Unified skill discovery and loading for Black Box 5.

    Manages both Tier 1 (engine) and Tier 2 (Agent Skills Standard)
    skills with on-demand loading, caching, and analytics.
    """

    def __init__(self,
                 tier1_path: Optional[Path] = None,
                 tier2_path: Optional[Path] = None):
        """
        Initialize the skill orchestrator.

        Args:
            tier1_path: Path to Tier 1 (engine) skills
            tier2_path: Path to Tier 2 (Agent Skills Standard) skills
        """
        self.tier1_manager = SkillManager(tier1_path)
        self.tier2_scanner = SkillScanner(tier2_path)
        self.cache = SkillCache(max_size=100)
        self.analytics = SkillAnalytics()

        self._skill_registry: Dict[str, SkillMetadata] = {}
        self._initialized = False

        logger.info("SkillOrchestrator initialized")

    async def initialize(self) -> None:
        """Initialize the orchestrator (discover all skills)"""
        if self._initialized:
            return

        logger.info("Initializing SkillOrchestrator...")

        # Discover Tier 1 skills
        await self._discover_tier1_skills()

        # Discover Tier 2 skills
        await self._discover_tier2_skills()

        self._initialized = True
        logger.info(f"SkillOrchestrator initialized with {len(self._skill_registry)} skills")

    async def _discover_tier1_skills(self) -> None:
        """Discover Tier 1 (engine) skills"""
        logger.info("Discovering Tier 1 skills...")

        try:
            tier1_skills = await self.tier1_manager.load_all()
            for skill in tier1_skills:
                metadata = SkillMetadata(
                    name=skill.name,
                    tier="tier1",
                    description=skill.description,
                    category=skill.category,
                    tags=skill.capabilities,
                    metadata=skill.metadata
                )
                self._skill_registry[skill.name] = metadata

            logger.info(f"Discovered {len(tier1_skills)} Tier 1 skills")
        except Exception as e:
            logger.error(f"Error discovering Tier 1 skills: {e}")

    async def _discover_tier2_skills(self) -> None:
        """Discover Tier 2 (Agent Skills Standard) skills"""
        logger.info("Discovering Tier 2 skills...")

        try:
            tier2_skills = await self.tier2_scanner.scan_all()
            for skill_name, metadata in tier2_skills.items():
                metadata.tier = "tier2"
                self._skill_registry[skill_name] = metadata

            logger.info(f"Discovered {len(tier2_skills)} Tier 2 skills")
        except Exception as e:
            logger.error(f"Error discovering Tier 2 skills: {e}")

    async def discover_all(self) -> List[SkillMetadata]:
        """
        Discover all available skills from both tiers.

        Returns:
            List of all skill metadata
        """
        if not self._initialized:
            await self.initialize()

        return list(self._skill_registry.values())

    async def discover_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """
        Discover a specific skill by name.

        Args:
            skill_name: Name of skill to discover

        Returns:
            Skill metadata or None if not found
        """
        if not self._initialized:
            await self.initialize()

        return self._skill_registry.get(skill_name)

    async def load_skill(self, skill_name: str) -> Optional[str]:
        """
        Load a skill's content on-demand.

        Args:
            skill_name: Name of skill to load

        Returns:
            Skill content (markdown) or None if not found
        """
        # Check cache first
        cached_content = await self.cache.get(skill_name)
        if cached_content is not None:
            logger.debug(f"Skill {skill_name} loaded from cache")
            return cached_content

        # Get skill metadata
        metadata = await self.discover_skill(skill_name)
        if metadata is None:
            logger.warning(f"Skill not found: {skill_name}")
            await self.analytics.track_skill_discovery(
                skill_name, "unknown", False
            )
            return None

        # Load from appropriate tier
        start_time = datetime.now()

        if metadata.tier == "tier1":
            content = await self._load_tier1_skill(metadata)
        else:  # tier2
            content = await self._load_tier2_skill(metadata)

        load_time = (datetime.now() - start_time).total_seconds()

        if content:
            # Cache the content
            await self.cache.put(skill_name, content)
            await self.analytics.track_skill_load(
                skill_name, "agent", load_time
            )
            logger.info(f"Loaded skill {skill_name} in {load_time:.2f}s")
        else:
            logger.error(f"Failed to load skill {skill_name}")

        return content

    async def _load_tier1_skill(self, metadata: SkillMetadata) -> Optional[str]:
        """Load Tier 1 (engine) skill content"""
        try:
            skill = self.tier1_manager.get_skill(metadata.name)
            if skill is None:
                return None

            # Convert Python skill to markdown for agent consumption
            content = self._format_tier1_skill(skill, metadata)
            return content
        except Exception as e:
            logger.error(f"Error loading Tier 1 skill {metadata.name}: {e}")
            return None

    async def _load_tier2_skill(self, metadata: SkillMetadata) -> Optional[str]:
        """Load Tier 2 (Agent Skills Standard) skill content"""
        try:
            content = await self.tier2_scanner.load_skill_content(metadata.name)
            return content
        except Exception as e:
            logger.error(f"Error loading Tier 2 skill {metadata.name}: {e}")
            return None

    def _format_tier1_skill(self, skill: Any, metadata: SkillMetadata) -> str:
        """Format Tier 1 skill as markdown for agents"""
        # Convert Python skill/class to markdown documentation
        lines = [
            f"# {skill.name}\n",
            f"**Tier**: Engine Skill\n",
            f"**Category**: {metadata.category}\n",
            f"**Description**: {metadata.description}\n",
            "\n## Capabilities\n"
        ]

        for capability in metadata.tags:
            lines.append(f"- {capability}")

        if skill.__doc__:
            lines.extend([
                "\n## Documentation\n",
                skill.__doc__
            ])

        return "\n".join(lines)

    async def search_skills(self, query: str) -> List[SkillMetadata]:
        """
        Search for skills by name, description, or tags.

        Args:
            query: Search query

        Returns:
            List of matching skills
        """
        if not self._initialized:
            await self.initialize()

        results = [
            metadata for metadata in self._skill_registry.values()
            if metadata.matches_query(query)
        ]

        return results

    async def get_skills_for_agent(self, agent_name: str) -> List[SkillMetadata]:
        """
        Get skills available for a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of skills available to the agent
        """
        from .mappings import AGENT_SKILL_MAPPINGS

        if agent_name not in AGENT_SKILL_MAPPINGS:
            # Return all enabled skills by default
            return [
                metadata for metadata in self._skill_registry.values()
                if metadata.name not in ARCHIVED_SKILLS
            ]

        mapping = AGENT_SKILL_MAPPINGS[agent_name]
        required_skills = mapping.get("required", [])
        optional_skills = mapping.get("optional", [])

        skill_names = required_skills + optional_skills
        skills = []

        for skill_name in skill_names:
            metadata = await self.discover_skill(skill_name)
            if metadata:
                skills.append(metadata)

        return skills

    async def use_skill(self,
                        skill_name: str,
                        agent_name: str,
                        task: str) -> Dict[str, Any]:
        """
        Use a skill to complete a task (with analytics).

        Args:
            skill_name: Name of skill to use
            agent_name: Name of the agent using the skill
            task: Task description

        Returns:
            Usage result with metadata
        """
        start_time = datetime.now()

        # Load skill
        content = await self.load_skill(skill_name)
        if content is None:
            return {
                "success": False,
                "error": f"Skill not found: {skill_name}",
                "skill_name": skill_name,
                "agent": agent_name
            }

        # Execute task with skill
        # (This would be handled by the agent)
        duration = (datetime.now() - start_time).total_seconds()

        result = {
            "success": True,
            "skill_name": skill_name,
            "agent": agent_name,
            "task": task,
            "duration": duration,
            "content": content
        }

        # Track usage
        await self.analytics.track_skill_usage(
            skill_name, agent_name, task, True, duration
        )

        return result

    async def invalidate_skill(self, skill_name: str) -> None:
        """
        Invalidate a cached skill.

        Args:
            skill_name: Name of skill to invalidate
        """
        await self.cache.invalidate(skill_name)
        logger.info(f"Invalidated skill: {skill_name}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get orchestrator statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "total_skills": len(self._skill_registry),
            "tier1_count": sum(1 for s in self._skill_registry.values() if s.tier == "tier1"),
            "tier2_count": sum(1 for s in self._skill_registry.values() if s.tier == "tier2"),
            "cache_size": self.cache.size,
            "cache_hits": self.cache.hits,
            "cache_misses": self.cache.misses
        }
```

**Deliverables**:
- ✅ SkillOrchestrator implementation
- ✅ SkillMetadata dataclass
- ✅ Complete error handling
- ✅ Analytics integration

---

## Skill Scanner Implementation

**File**: `2-engine/02-orchestration/skills/scanner.py`

```python
"""
Skill Scanner for Agent Skills Standard

Scans ~/.claude/skills/ directory for SKILL.md files
and parses YAML frontmatter for discovery.
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from datetime import datetime

logger = logging.getLogger(__name__)


class SkillScanner:
    """Scan and parse Agent Skills Standard files"""

    def __init__(self, skills_path: Optional[Path] = None):
        """
        Initialize the skill scanner.

        Args:
            skills_path: Path to skills directory (defaults to ~/.claude/skills/)
        """
        if skills_path is None:
            skills_path = Path.home() / ".claude" / "skills"

        self.skills_path = skills_path.expanduser()
        self.skill_index: Dict[str, Dict[str, any]] = {}

        logger.info(f"SkillScanner initialized with path: {self.skills_path}")

    async def scan_all(self) -> Dict[str, Dict[str, any]]:
        """
        Scan all skills in the skills directory.

        Returns:
            Dictionary mapping skill names to metadata
        """
        if not self.skills_path.exists():
            logger.warning(f"Skills path does not exist: {self.skills_path}")
            return {}

        logger.info(f"Scanning for skills in: {self.skills_path}")

        # Find all SKILL.md files
        skill_files = list(self.skills_path.rglob("SKILL.md"))

        # Parse each skill file
        tasks = []
        for skill_file in skill_files:
            tasks.append(self._parse_skill_file(skill_file))

        # Wait for all parsing to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Build index from successful results
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error parsing skill: {result}")
                continue

            if result and "name" in result:
                skill_name = result["name"]
                self.skill_index[skill_name] = result
                logger.debug(f"Scanned skill: {skill_name}")

        logger.info(f"Scanned {len(self.skill_index)} skills")
        return self.skill_index

    async def _parse_skill_file(self, skill_file: Path) -> Optional[Dict[str, any]]:
        """
        Parse a SKILL.md file and extract metadata.

        Args:
            skill_file: Path to SKILL.md file

        Returns:
            Skill metadata dictionary or None if parsing fails
        """
        try:
            content = skill_file.read_text()

            # Extract YAML frontmatter
            match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if not match:
                logger.warning(f"No YAML frontmatter found in: {skill_file}")
                return None

            frontmatter_yaml = match.group(1)
            markdown_content = match.group(2)

            # Parse YAML frontmatter
            frontmatter = yaml.safe_load(frontmatter_yaml)

            # Extract required fields
            name = frontmatter.get("name")
            description = frontmatter.get("description")

            if not name or not description:
                logger.warning(f"Missing required fields in: {skill_file}")
                return None

            # Build metadata
            metadata = {
                "name": name,
                "description": description,
                "tags": frontmatter.get("tags", []),
                "author": frontmatter.get("author", ""),
                "version": frontmatter.get("version", "1.0.0"),
                "file_path": str(skill_file),
                "category": self._infer_category(skill_file),
                "last_modified": datetime.fromtimestamp(skill_file.stat().st_mtime),
                "content": markdown_content,
                "frontmatter": frontmatter
            }

            return metadata

        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in {skill_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading skill file {skill_file}: {e}")
            return None

    def _infer_category(self, skill_file: Path) -> str:
        """
        Infer skill category from directory structure.

        Args:
            skill_file: Path to skill file

        Returns:
            Category name
        """
        # Get parent directory name as category
        category = skill_file.parent.name
        return category

    async def load_skill_content(self, skill_name: str) -> Optional[str]:
        """
        Load full skill content by name.

        Args:
            skill_name: Name of skill to load

        Returns:
            Full skill content (markdown) or None if not found
        """
        if skill_name not in self.skill_index:
            return None

        metadata = self.skill_index[skill_name]
        return metadata.get("content")

    def search(self, query: str) -> List[Dict[str, any]]:
        """
        Search skills by name, description, or tags.

        Args:
            query: Search query

        Returns:
            List of matching skill metadata
        """
        query_lower = query.lower()
        results = []

        for skill_name, metadata in self.skill_index.items():
            # Search in name
            if query_lower in skill_name.lower():
                results.append(metadata)
                continue

            # Search in description
            if query_lower in metadata["description"].lower():
                results.append(metadata)
                continue

            # Search in tags
            tags = metadata.get("tags", [])
            if any(query_lower in tag.lower() for tag in tags):
                results.append(metadata)

        return results
```

---

## Success Criteria

### Phase 1 Success (Week 1)
- [ ] SkillOrchestrator implemented and tested
- [ ] SkillScanner can parse SKILL.md files
- [ ] Directory structure created
- [ ] Agent base class updated with skill methods
- [ ] Unit tests passing

### Phase 2 Success (Week 2)
- [ ] 6 high-priority skills converted
- [ ] All skills in Agent Skills Standard format
- [ ] Multi-project Supabase skills created
- [ ] Skill templates created
- [ ] Skills registry updated

### Phase 3 Success (Week 3)
- [ ] Agents can load skills on-demand
- [ ] Agents can use skills effectively
- [ ] Skill mappings configured per agent
- [ ] Skill caching working
- [ ] Integration tests passing

### Phase 4 Success (Week 4)
- [ ] Token efficiency improved >50%
- [ ] Agent response time maintained
- [ ] Skill analytics tracking usage
- [ ] Documentation complete
- [ ] Training materials ready

### Overall Success
- [ ] All agents using both Tier 1 and Tier 2 skills
- [ ] Token usage reduced by >50%
- [ ] Skill discovery working automatically
- [ ] Claude Code compatibility verified
- [ ] System stable and performant

---

## Risk Mitigation

### Risk 1: Breaking Existing Functionality

**Mitigation**:
- Maintain backward compatibility with existing engine skills
- Add new features without removing old ones
- Comprehensive testing before deployment
- Rollback plan ready

### Risk 2: Token Usage Increases

**Mitigation**:
- Implement on-demand loading (not upfront)
- Use skill caching effectively
- Monitor token usage closely
- Optimize based on analytics

### Risk 3: Performance Degradation

**Mitigation**:
- Benchmark before and after
- Cache skill content aggressively
- Use async loading (non-blocking)
- Monitor response times

### Risk 4: Skill Discovery Fails

**Mitigation**:
- Multiple discovery methods (filesystem + config)
- Fallback to manual skill loading
- Comprehensive error handling
- Monitoring and alerts

---

## Monitoring & Metrics

### Key Metrics to Track

**Skill Discovery**:
- Number of skills discovered
- Discovery success rate
- Discovery time
- Failed discoveries

**Skill Loading**:
- Load time per skill
- Cache hit rate
- Load success rate
- Token usage per load

**Skill Usage**:
- Most used skills
- Least used skills
- Agent-specific usage
- Task completion rate with skills

**System Performance**:
- Agent response time
- Token efficiency (before/after)
- Error rates
- Cache effectiveness

### Dashboard Metrics

**Real-time**:
- Active skills count
- Recent skill loads
- Current cache size
- Active agents using skills

**Daily**:
- Skills used per day
- Token usage trends
- Error rates
- Performance metrics

**Monthly**:
- Skill usage report
- Token efficiency report
- Agent satisfaction report
- System health report

---

## Rollback Plan

If integration fails:

### Phase 1 Rollback
- Revert SkillOrchestrator changes
- Keep existing SkillManager
- Restore original agent configuration

### Phase 2 Rollback
- Archive converted skills
- Keep original skill files
- Document conversion issues

### Phase 3 Rollback
- Remove skill methods from agents
- Restore original agent prompts
- Disable skill orchestration

### Phase 4 Rollback
- Disable analytics
- Remove caching layer
- Restore original system

---

## Next Steps

### Immediate (This Week)
1. **Review plan with team**
2. **Set up development environment**
3. **Create directory structure**
4. **Begin SkillOrchestrator implementation**

### Short-term (Next 2 Weeks)
1. **Implement SkillOrchestrator and SkillScanner**
2. **Convert 6 high-priority skills**
3. **Update agent base class**
4. **Begin integration testing**

### Long-term (Next Month)
1. **Complete agent integration**
2. **Deploy to production**
3. **Monitor and optimize**
4. **Gather feedback and iterate**

---

## Appendix: Code Examples

### Example 1: Agent Using a Skill

**Before** (current):
```python
# Agent has to manually load skill
skill_content = read_skill_file("supabase-ddl-rls.md")
agent.context.add("skill", skill_content)
```

**After** (with orchestration):
```python
# Agent requests skill automatically
skill_content = await agent.load_skill("supabase-operations")
if skill_content:
    agent.context.add_skill("supabase-operations", skill_content)
```

### Example 2: Skill Discovery

**Before**:
```python
# Agent doesn't know what skills exist
available_skills = list_known_skills()
```

**After**:
```python
# Agent can discover skills
available_skills = await agent.get_available_skills()
# Or search for specific skills
database_skills = await agent.skill_orchestrator.search_skills("database")
```

### Example 3: Skill Usage

**Before**:
```python
# Manual skill invocation
result = execute_with_skill(task, skill_content)
```

**After**:
```python
# Automatic skill usage with analytics
result = await agent.use_skill("supabase-operations", task)
# Analytics tracked automatically
```

---

## Conclusion

This integration plan provides a complete roadmap for incorporating the Agent Skills Standard into Black Box 5's agent system. The hybrid approach maintains the strengths of your existing Python-based engine skills while adding the universal compatibility and token efficiency of the Agent Skills Standard.

**Key Benefits**:
- ✅ Unified skill discovery and loading
- ✅ Token-efficient on-demand loading
- ✅ Agent Skills Standard compatibility
- ✅ Claude Code integration
- ✅ Comprehensive analytics

**Timeline**: 4 weeks to full implementation
**Effort**: Medium (requires engine modifications + skill conversion)
**Risk**: Low (gradual rollout with rollback options)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-28
**Status**: Ready for Review and Implementation
**Owner**: SISO Internal Team

**Next Action**: Review plan with team and begin Phase 1
