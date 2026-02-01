# Accelerated Skills Integration Plan for Black Box 5

**Date**: 2026-01-28
**Status**: Ready for Implementation
**Timeline**: 1-2 weeks (down from 4 weeks)
**Approach**: Leverage existing BB5 components + open source tools

---

## Executive Summary

**Key Finding**: Black Box 5 already has 60-70% of the needed infrastructure. By extending existing components rather than rebuilding, we can reduce implementation time from 4 weeks to 1-2 weeks.

**Existing Components to Leverage**:
1. `Orchestrator.py` - Extend for skill orchestration
2. `BaseAgent.py` - Add skill loading methods
3. `SkillManager.py` - Add Tier 2 Agent Skills support
4. `ClaudeCodeAgentMixin.py` - Already handles CLI execution

**Open Source Tools to Integrate**:
1. `philschmid/mcp-cli` - MCP discovery and testing
2. `mcp2skill` - MCP-to-skill conversion
3. Agent Skills standard implementations

---

## What We Already Have (Existing BB5 Components)

### 1. Orchestrator.py
**Location**: `blackbox5/2-engine/01-core/orchestration/Orchestrator.py`

**Current Capabilities**:
- Multi-agent workflow coordination
- Step dependency resolution
- Agent lifecycle management

**What to Add**:
- Skill discovery layer
- Skill routing (Tier 1 vs Tier 2)
- Skill caching for token efficiency

**Extension Approach**:
```python
# Extend existing Orchestrator class
class SkillOrchestratorMixin:
    """Add skill orchestration to existing Orchestrator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._skill_cache: Dict[str, Any] = {}
        self._skill_scanner = SkillScanner()

    async def discover_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """Check if skill exists in Tier 1 or Tier 2"""

    async def load_skill_for_agent(self, agent: BaseAgent, skill_name: str):
        """Load skill into agent context with caching"""
```

### 2. BaseAgent.py
**Location**: `blackbox5/2-engine/01-core/agents/core/base_agent.py`

**Current Capabilities**:
- Agent configuration and lifecycle
- `_skills` list for tracking available skills
- Task execution framework

**What to Add**:
- `load_skill()` method
- `use_skill()` method
- Skill context injection

**Extension Approach**:
```python
# Add methods to existing BaseAgent
class BaseAgent(ABC):
    # ... existing code ...

    async def load_skill(self, skill_name: str) -> bool:
        """Load a skill on-demand"""
        if skill_name in self._loaded_skills:
            return True  # Already loaded

        skill_content = await self.orchestrator.load_skill_for_agent(
            self, skill_name
        )
        if skill_content:
            self._loaded_skills[skill_name] = skill_content
            return True
        return False

    async def use_skill(self, skill_name: str, context: Dict[str, Any]):
        """Use a loaded skill with context"""
        if skill_name not in self._loaded_skills:
            await self.load_skill(skill_name)
        # Use the skill
```

### 3. SkillManager.py
**Location**: `blackbox5/2-engine/01-core/agents/core/skill_manager.py`

**Current Capabilities**:
- Tier 1 Python skill loading
- JSON metadata parsing
- Skill categorization

**What to Add**:
- Tier 2 Agent Skills Standard support
- `~/.claude/skills/` directory scanning
- YAML frontmatter parsing

**Extension Approach**:
```python
# Extend existing SkillManager
class SkillManager:
    # ... existing code ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tier2_skills_path = Path.home() / ".claude" / "skills"
        self._tier2_skills: Dict[str, AgentSkill] = {}

    async def load_tier2_skills(self):
        """Load Agent Skills Standard files from ~/.claude/skills/"""
        for skill_dir in self._tier2_skills_path.iterdir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill = AgentSkill.from_markdown(skill_md)
                self._tier2_skills[skill.name] = skill

    async def get_skill(self, name: str) -> Optional[Union[Skill, AgentSkill]]:
        """Get skill from Tier 1 or Tier 2"""
        # Check Tier 2 first (more token efficient)
        if name in self._tier2_skills:
            return self._tier2_skills[name]
        # Fall back to Tier 1
        return self._skills.get(name)
```

### 4. ClaudeCodeAgentMixin.py
**Location**: `blackbox5/2-engine/01-core/client/ClaudeCodeAgentMixin.py`

**Current Capabilities**:
- Claude Code CLI execution
- Prompt building
- Structured output parsing

**What to Add**:
- Nothing! Already handles CLI execution perfectly

**How to Use**:
```python
# This already works, just use it for skill execution
class Amelia(ClaudeCodeAgentMixin, BaseAgent):
    async def execute_skill(self, skill_name: str, task: str):
        # ClaudeCodeAgentMixin provides execute_with_claude()
        result = await self.execute_with_claude(
            task_description=f"Use {skill_name} skill to: {task}",
            context=self._loaded_skills.get(skill_name)
        )
        return result
```

---

## Open Source Tools to Integrate

### 1. mcp-cli (philschmid/mcp-cli)
**Purpose**: Lightweight CLI for MCP discovery and testing

**Installation**:
```bash
pip install mcp-cli
```

**Usage for Skill Development**:
```bash
# Discover what tools an MCP server provides
mcp-cli describe <server-name>

# Test MCP tool invocation
mcp-cli <server-name>/<tool-name> --args '{"key": "value"}'

# Use this info to create CLI-based skills
```

**Integration**: Use during skill development to document MCP tool behavior, then convert to CLI skills

### 2. mcp2skill
**Purpose**: Convert MCP servers to Agent Skills

**Installation**:
```bash
pip install mcp2skill
# or use web app: https://mcp2skill.streamlit.app/
```

**Usage**:
```bash
# Convert SISO tasks MCP to skill
mcp2skill siso-tasks --output ~/.claude/skills/siso-tasks-cli

# Generates SKILL.md with CLI invocation patterns
```

**Integration**: Automated conversion of existing MCP-based skills

---

## Implementation Roadmap (1-2 Weeks)

### Week 1: Foundation (3 days)

**Day 1: Extend SkillManager**
- [ ] Add Tier 2 support to `SkillManager.py`
- [ ] Implement `~/.claude/skills/` scanning
- [ ] Add YAML frontmatter parsing
- [ ] Create `AgentSkill` dataclass

**Day 2: Extend BaseAgent**
- [ ] Add `load_skill()` method
- [ ] Add `use_skill()` method
- [ ] Add `_loaded_skills` dict
- [ ] Implement skill context injection

**Day 3: Extend Orchestrator**
- [ ] Add `SkillOrchestratorMixin`
- [ ] Implement skill discovery
- [ ] Add skill caching
- [ ] Create tier routing logic

### Week 1-2: Skills Conversion (2-3 days)

**Day 4: Convert High-Priority Skills**
- [ ] Convert `supabase-operations` (simple MD → SKILL.md)
- [ ] Convert `siso-tasks-cli` (MCP → CLI skill using mcp2skill)
- [ ] Convert `feedback-triage` (structured MD → SKILL.md)

**Day 5: Create Skill Templates**
- [ ] Create base SKILL.md template
- [ ] Create MCP-to-CLI conversion template
- [ ] Document conversion patterns

**Day 6: Testing & Integration**
- [ ] Test skill loading with agents
- [ ] Test token efficiency
- [ ] Verify Claude Code compatibility
- [ ] Document results

### Week 2: Polish & Deploy (2 days)

**Day 7: Agent Integration**
- [ ] Update Amelia (Developer) to use skills
- [ ] Update Mary (Analyst) to use skills
- [ ] Update agent prompts
- [ ] Create agent-skill mappings

**Day 8: Documentation & Deploy**
- [ ] Update all documentation
- [ ] Create quick start guide
- [ ] Deploy to production
- [ ] Train team

---

## Code Examples

### Complete: Extended SkillManager

```python
# blackbox5/2-engine/01-core/agents/core/skill_manager.py

from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import yaml
import frontmatter

@dataclass
class AgentSkill:
    """Agent Skills Standard skill"""
    name: str
    description: str
    tags: List[str]
    content: str
    author: Optional[str] = None
    version: Optional[str] = None

    @classmethod
    def from_markdown(cls, path: Path) -> 'AgentSkill':
        """Parse SKILL.md with YAML frontmatter"""
        with open(path) as f:
            post = frontmatter.load(f)

        return cls(
            name=post.get('name', path.parent.name),
            description=post.get('description', ''),
            tags=post.get('tags', []),
            content=post.content,
            author=post.get('author'),
            version=post.get('version')
        )

class SkillManager:
    """Extended to support both Tier 1 and Tier 2 skills"""

    def __init__(self, skills_path: Optional[Path] = None):
        # Tier 1: Existing Python skills
        self.skills_path = skills_path or Path.cwd() / ".skills"
        self._skills: Dict[str, Skill] = {}
        self._skills_by_category: Dict[str, List[str]] = {}

        # Tier 2: Agent Skills Standard (NEW)
        self._tier2_skills_path = Path.home() / ".claude" / "skills"
        self._tier2_skills: Dict[str, AgentSkill] = {}
        self._skill_cache: Dict[str, str] = {}  # Token-efficient caching

    async def load_all(self) -> List[Union[Skill, AgentSkill]]:
        """Load both Tier 1 and Tier 2 skills"""
        await self._load_json_skills()
        await self._load_python_skills()
        await self._load_tier2_skills()  # NEW

        return list(self._skills.values()) + list(self._tier2_skills.values())

    async def _load_tier2_skills(self):
        """Load Agent Skills Standard files"""
        if not self._tier2_skills_path.exists():
            return

        for skill_dir in self._tier2_skills_path.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill = AgentSkill.from_markdown(skill_md)
                self._tier2_skills[skill.name] = skill

    async def get_skill(self, name: str) -> Optional[Union[Skill, AgentSkill]]:
        """Get skill from Tier 1 or Tier 2 (Tier 2 checked first)"""
        # Check cache first
        if name in self._skill_cache:
            return self._skill_cache[name]

        # Check Tier 2 first (more token efficient)
        if name in self._tier2_skills:
            return self._tier2_skills[name]

        # Fall back to Tier 1
        return self._skills.get(name)

    async def get_skill_content(self, name: str, use_progressive: bool = True) -> str:
        """Get skill content with progressive disclosure for token efficiency"""
        skill = await self.get_skill(name)

        if isinstance(skill, AgentSkill):
            if use_progressive:
                # Return summary first, full content on demand
                return f"# {skill.name}\n\n{skill.description}\n\nTags: {', '.join(skill.tags)}\n\n[Use load_skill_full for complete content]"
            else:
                return skill.content

        # Tier 1 skills
        return str(skill)
```

### Complete: Extended BaseAgent

```python
# blackbox5/2-engine/01-core/agents/core/base_agent.py

from typing import Dict, List, Optional
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Extended base agent with skill support"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self._skills: List[str] = config.skills or []  # From config

        # NEW: Skill loading
        self._loaded_skills: Dict[str, str] = {}
        self._skill_manager = SkillManager()

    # ... existing methods ...

    async def load_skill(self, skill_name: str, full: bool = False) -> bool:
        """Load a skill on-demand (token efficient)"""
        # Check if already loaded
        if skill_name in self._loaded_skills:
            return True

        # Get skill content
        content = await self._skill_manager.get_skill_content(
            skill_name,
            use_progressive=not full
        )

        if content:
            self._loaded_skills[skill_name] = content
            return True

        return False

    async def use_skill(self, skill_name: str, context: Optional[Dict] = None):
        """Use a loaded skill with context"""
        # Ensure skill is loaded
        if skill_name not in self._loaded_skills:
            await self.load_skill(skill_name)

        # Get skill content
        skill_content = self._loaded_skills[skill_name]

        # Inject skill into agent context
        # Agent-specific implementation in subclasses
        return await self._execute_with_skill(skill_name, skill_content, context)

    async def _execute_with_skill(
        self,
        skill_name: str,
        skill_content: str,
        context: Optional[Dict] = None
    ):
        """Execute task with skill context (to be implemented by subclasses)"""
        raise NotImplementedError

    async def list_available_skills(self) -> List[str]:
        """List all available skills (Tier 1 + Tier 2)"""
        tier1 = list(self._skill_manager._skills.keys())
        tier2 = list(self._skill_manager._tier2_skills.keys())
        return tier1 + tier2

    async def list_loaded_skills(self) -> List[str]:
        """List currently loaded skills (for token tracking)"""
        return list(self._loaded_skills.keys())
```

### Complete: Skill Orchestrator Mixin

```python
# blackbox5/2-engine/01-core/orchestration/skills.py

from typing import Dict, Optional, Any
from pathlib import Path

class SkillOrchestratorMixin:
    """Add skill orchestration to existing Orchestrator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._skill_cache: Dict[str, Any] = {}
        self._skill_scanner = SkillScanner()
        self._skill_manager = SkillManager()

    async def discover_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """Discover if skill exists in Tier 1 or Tier 2"""
        # Check Tier 2 first (Agent Skills Standard)
        tier2_path = Path.home() / ".claude" / "skills" / skill_name / "SKILL.md"
        if tier2_path.exists():
            return SkillMetadata(
                name=skill_name,
                tier=2,
                path=tier2_path,
                type="agent-skill"
            )

        # Check Tier 1 (Python skills)
        tier1_path = Path.cwd() / ".skills" / f"{skill_name}.py"
        if tier1_path.exists():
            return SkillMetadata(
                name=skill_name,
                tier=1,
                path=tier1_path,
                type="python-skill"
            )

        return None

    async def load_skill_for_agent(
        self,
        agent: BaseAgent,
        skill_name: str,
        force_full: bool = False
    ) -> Optional[str]:
        """Load skill into agent context with caching"""
        # Check cache
        cache_key = f"{agent.name}:{skill_name}"
        if cache_key in self._skill_cache and not force_full:
            return self._skill_cache[cache_key]

        # Get skill content
        content = await self._skill_manager.get_skill_content(
            skill_name,
            use_progressive=not force_full
        )

        if content:
            # Cache for reuse
            self._skill_cache[cache_key] = content
            return content

        return None

    def clear_skill_cache(self, agent: Optional[BaseAgent] = None):
        """Clear skill cache (for token management)"""
        if agent:
            # Clear cache for specific agent
            keys_to_remove = [k for k in self._skill_cache if k.startswith(f"{agent.name}:")]
            for key in keys_to_remove:
                del self._skill_cache[key]
        else:
            # Clear all cache
            self._skill_cache.clear()

@dataclass
class SkillMetadata:
    """Metadata about a skill"""
    name: str
    tier: int  # 1 or 2
    path: Path
    type: str
```

---

## Conversion Examples

### Example 1: Convert Simple MD to SKILL.md

**Before** (`supabase-ddl-rls.md`):
```markdown
# Supabase DDL and RLS

This skill helps with database operations...

## Commands

supabase db push
```

**After** (`~/.claude/skills/supabase-operations/SKILL.md`):
```yaml
---
name: supabase-operations
description: Database operations for Supabase including DDL, RLS, and migrations
tags: [database, supabase, ddl, rls, migration]
author: SISO Internal
version: 1.0.0
---

# Supabase Operations

## Purpose

This skill provides complete database operations for Supabase projects including DDL execution, Row Level Security (RLS) management, and migrations.

## Prerequisites

- Supabase CLI installed
- Valid SUPABASE_ACCESS_TOKEN
- Project initialized with `supabase init`

## Commands

### Database Push

```bash
supabase db push
```

**Description**: Push local schema changes to remote database
**Use When**: After modifying schema.sql or creating migrations

### Generate Migration

```bash
supabase db diff -f <name>
```

**Description**: Generate a new migration from schema changes
**Example**: `supabase db diff -f add_user_preferences`

## Workflows

### Creating a New Table

1. Modify `supabase/migrations/[timestamp]_create_table.sql`
2. Run `supabase db push`
3. Verify in Supabase dashboard

### Adding RLS Policy

1. Create migration: `supabase db diff -f add_rls_policy`
2. Edit the generated migration file
3. Push: `supabase db push`

## Troubleshooting

**Migration fails**: Check `supabase/migrations/` for conflicts
**RLS not working**: Verify `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`

## Related Skills

- [database-schema](../database-schema/SKILL.md) - Schema design patterns
- [supabase-auth](../supabase-auth/SKILL.md) - Authentication setup
```

### Example 2: Convert MCP to CLI Skill

**Using mcp2tool**:
```bash
# Convert SISO tasks MCP to CLI skill
mcp2skill siso-tasks \
  --output ~/.claude/skills/siso-tasks-cli \
  --format cli
```

**Manual Approach**:
1. Use `mcp-cli describe siso-tasks` to discover tools
2. Map each MCP tool to equivalent CLI command
3. Create SKILL.md with CLI invocation patterns

---

## Quick Start

### For Developers

**Day 1**: Extend SkillManager
```bash
# Edit blackbox5/2-engine/01-core/agents/core/skill_manager.py
# Add AgentSkill dataclass and _load_tier2_skills method
```

**Day 2**: Test with first skill
```bash
# Create directory
mkdir -p ~/.claude/skills/test-skill

# Create SKILL.md
cat > ~/.claude/skills/test-skill/SKILL.md << 'EOF'
---
name: test-skill
description: A test skill to verify integration
tags: [test]
---

# Test Skill

This is a test skill to verify the integration works.
EOF

# Test loading
python -c "
import asyncio
from blackbox5.engine.agents.core.skill_manager import SkillManager

async def test():
    sm = SkillManager()
    await sm.load_all()
    skill = await sm.get_skill('test-skill')
    print(f'Found skill: {skill.name}')

asyncio.run(test())
"
```

**Day 3**: Test with agent
```python
# Create test agent
from blackbox5.engine.agents.core.base_agent import BaseAgent

class TestAgent(BaseAgent):
    async def test_skill_loading(self):
        # List available skills
        skills = await self.list_available_skills()
        print(f"Available skills: {skills}")

        # Load a skill
        success = await self.load_skill('test-skill')
        print(f"Skill loaded: {success}")

        # List loaded skills
        loaded = await self.list_loaded_skills()
        print(f"Loaded skills: {loaded}")

agent = TestAgent(config)
await agent.test_skill_loading()
```

---

## Token Efficiency Strategy

### Progressive Disclosure

**Initial Load** (summary only):
```yaml
---
name: supabase-operations
description: Database operations for Supabase
tags: [database, supabase]
---

# Supabase Operations

Summary: Database operations including DDL, RLS, and migrations.

Use `load_skill_full` for complete documentation.
```

**Full Load** (on-demand):
```yaml
Complete content with all commands, workflows, examples
```

### Caching Strategy

```python
# L1 Cache: In-memory (within agent session)
self._loaded_skills: Dict[str, str] = {}

# L2 Cache: Orchestrator-level (across agents)
self._skill_cache: Dict[str, str] = {}

# L3 Cache: Filesystem (persisted across sessions)
# ~/.claude/skills/.cache/
```

---

## Success Criteria

### Week 1 Complete When:
- [ ] SkillManager extended with Tier 2 support
- [ ] BaseAgent extended with skill loading
- [ ] 3 skills converted and tested
- [ ] Token efficiency measured

### Week 2 Complete When:
- [ ] All agents using skills
- [ ] Token usage reduced by >50%
- [ ] Claude Code compatibility verified
- [ ] Documentation complete

---

## Risk Mitigation

### Low Risk
- **Breaking changes**: Extending existing classes, not replacing
- **Performance**: Reusing proven patterns
- **Adoption**: Gradual rollout, backward compatible

### Medium Risk
- **Token usage**: Progressive disclosure minimizes this
- **Skill quality**: Testing framework catches issues early

### Rollback Plan
- Keep existing Tier 1 system untouched
- Feature flags for Tier 2 enablement
- Can disable Tier 2 without affecting Tier 1

---

## Summary

**What Changed**:
- 4 weeks → 1-2 weeks (60-75% time reduction)
- Building from scratch → Extending existing components
- Custom implementation → Leveraging open source tools

**Key Leverage Points**:
1. Extend `SkillManager.py` for Tier 2 (not new implementation)
2. Extend `BaseAgent.py` for skill loading (not new agent class)
3. Extend `Orchestrator.py` for skill orchestration (not new orchestrator)
4. Use `ClaudeCodeAgentMixin.py` as-is (already handles CLI execution)
5. Use `mcp-cli` for MCP discovery (not building custom)
6. Use `mcp2skill` for conversion (not manual)

**Next Steps**:
1. Review and approve this plan
2. Begin Day 1: Extend SkillManager
3. Convert first 3 skills (Days 4-6)
4. Test with agents (Day 7)
5. Deploy (Day 8)

---

**Plan Version**: 1.0.0
**Last Updated**: 2026-01-28
**Status**: Ready for Implementation
**Original Timeline**: 4 weeks
**Accelerated Timeline**: 1-2 weeks (60-75% reduction)
