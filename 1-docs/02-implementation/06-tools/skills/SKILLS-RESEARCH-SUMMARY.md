# Black Box 5 Skills: Research Summary & Action Plan

**Date**: 2026-01-28
**Status**: Research Complete
**Purpose**: Summary of MCP/CLI/Skills research and implementation plan

---

## Executive Summary

**What We Found**:
1. CLI tools CAN outperform MCP in many scenarios (token efficiency, capability access)
2. The person you encountered was RIGHT about CLI being better for agents
3. Black Box 5 has a custom Python skills system that differs from the Agent Skills standard
4. A hybrid approach is BEST for your use case

**What We Created**:
1. Complete analysis of BB5's current skills system
2. Comparison with Agent Skills standard
3. Migration guide for converting skills
4. Complete skills registry
5. Action plan for implementation

---

## Research Findings

### 1. CLI vs MCP: CLI Wins in Key Areas

**Evidence from Benchmarks**:

| Metric | CLI | MCP | Winner |
|--------|-----|-----|--------|
| Browser automation score | 77/100 | 60/100 | CLI +17 pts |
| Token efficiency | 202.1 TES | 152.3 TES | CLI +33% |
| Amazon page (tokens) | 1,200 | 52,000 | CLI 43x better |
| Capability access | Full (300+ CDP) | Limited | CLI |
| Success rate | 100% | 100% | Tie |

**Why CLI Wins**:
- LLMs already trained on bash/CLI commands
- More token-efficient (no protocol overhead)
- Full capability access (no MCP limitations)
- Unix composability (pipes, redirection)
- Predictable output sizing

**When MCP Makes Sense**:
- Cross-platform integration needed
- Sandboxed environments required
- Stateful tools easier to implement as MCP
- Ecosystem standardization important

### 2. Best Frameworks for Agent Skills

**Agent Skills Standard** (agentskills.io):
- **Status**: Universal standard (published Dec 18, 2025)
- **Format**: SKILL.md (YAML frontmatter + Markdown)
- **Platforms**: Claude Code, OpenCode, Gemini CLI (in progress)
- **Discovery**: Filesystem scanning, automatic loading
- **Token Efficiency**: On-demand loading (progressive disclosure)

**BB5 Custom System**:
- **Status**: BB5-specific, not portable
- **Format**: Python classes + JSON + Markdown
- **Platforms**: Black Box 5 only
- **Discovery**: Custom SkillManager
- **Token Efficiency**: Not optimized for LLM context

**Recommendation**: Hybrid approach
- Keep BB5 Python skills for engine-internal operations
- Adopt Agent Skills standard for agent capabilities
- Bridge the two tiers with CLI wrappers

### 3. Getting Agents to Use CLI Effectively

**Key Principles** (from research):

1. **Assume Agent Brilliance**
   - Only add context agent doesn't have
   - Don't over-explain basics

2. **Provide Concrete Examples**
   - Real commands with actual output
   - Common workflow patterns
   - Error handling examples

3. **Selective Queries Over Bulk Dumps**
   - Let agents request what they need
   - Don't dump everything upfront
   - Predictable output sizing

4. **Full Capability Access**
   - Expose all underlying capabilities
   - Don't pre-decide what agents "need"
   - Let agents figure it out

5. **Structured Output**
   - JSON with consistent schemas
   - Parseable by other tools
   - Composable via pipes

**What Works Best**:
```yaml
---
name: example-skill
description: Clear, concise description
tags: [relevant, discoverable, tags]
---

# Skill Title

## Commands

### Command Name
```bash
command --args
```

**Description**: What it does
**Example**: (with real output)
**Expected**: (what you should see)

## Workflows
(Step-by-step procedures)
```

### 4. Multiple Supabase Projects/Accounts

**Challenge**: Different Supabase projects, different credentials

**Solution Options**:

**Option 1: Environment Variables** (Recommended)
```bash
# Project 1
export SUPABASE_ACCESS_TOKEN=spb_project1
export SUPABASE_PROJECT_ID=proj1_***

# Project 2
export SUPABASE_ACCESS_TOKEN=spb_project2
export SUPABASE_PROJECT_ID=proj2_***
```

**Option 2: Per-Project Skills**
```
~/.claude/skills/
├── supabase-project1/SKILL.md
├── supabase-project2/SKILL.md
└── supabase-common/SKILL.md
```

**Option 3: CLI Wrapper Script**
```bash
#!/bin/bash
PROJECT=$1
COMMAND=${@:2}

case $PROJECT in
  "project1")
    export SUPABASE_ACCESS_TOKEN=spb_***
    export SUPABASE_PROJECT_ID=proj1_***
    ;;
  "project2")
    export SUPABASE_ACCESS_TOKEN=spb_***
    export SUPABASE_PROJECT_ID=proj2_***
    ;;
esac

supabase $COMMAND
```

**Usage**:
```bash
supabase-wrapper.sh project1 db push
supabase-wrapper.sh project2 functions deploy
```

### 5. MCP-to-CLI Skills Conversion

**Tool**: mcp2skill
- **Repo**: github.com/fenwei-dev/mcp2skill
- **Web**: mcp2skill.streamlit.app
- **Purpose**: Convert MCP servers to Agent Skills

**How It Works**:
1. Extract MCP server instructions
2. Generate SKILL.md with tool descriptions
3. Create CLI invocation patterns
4. Add progressive disclosure for efficiency

**Manual Conversion Process**:

**Step 1**: Analyze MCP server
```bash
mcp-cli describe <server>
mcp-cli <server>/<tool>
```

**Step 2**: Identify underlying CLI
- Many MCPs are thin wrappers around existing CLIs
- Example: GitHub MCP → `gh` CLI
- Example: Supabase MCP → `supabase` CLI

**Step 3**: Create SKILL.md
```yaml
---
name: <mcp-name>-cli
description: CLI interface for <MCP> functionality
tags: [mcp, converted, cli]
---

# <MCP Name> - CLI Edition

## Why CLI Over MCP?
- LLMs trained on bash
- Token efficiency
- Full capability access

## Tool Reference

| MCP Tool | CLI Command | Notes |
|----------|-------------|-------|
| mcp_tool_1 | cli command one | Direct |
| mcp_tool_2 | cli command two --json | Add flag |
```

**Step 4**: Add supporting files
- Scripts/ directory
- Examples/ directory
- Templates/

---

## Black Box 5 Current Implementation

### What You Have

**Two-Tier System** (already!):

**Tier 1: Engine Skills** (Python)
- Location: `2-engine/01-core/agents/skills/`
- Format: Python classes + JSON
- Purpose: Engine-internal operations
- Loading: SkillManager runtime import

**Tier 2: Agent Skills** (Mixed formats)
- Location: `2-engine/04-work/modules/skills/`
- Formats: Markdown (simple), MCP-based
- Purpose: Agent capabilities
- Status: NOT using Agent Skills standard

### What's Missing

**Tier 2 Issues**:
- ❌ No YAML frontmatter (not discoverable)
- ❌ Not in Agent Skills standard format
- ❌ Mixed formats (inconsistent)
- ❌ Not compatible with Claude Code/agents ecosystem
- ❌ No token optimization

### What You Need

**Adopt Agent Skills Standard for Tier 2**:
- ✅ Create `~/.claude/skills/` directory
- ✅ Convert current skills to SKILL.md format
- ✅ Add YAML frontmatter for discovery
- ✅ Implement on-demand loading
- ✅ Ensure Claude Code compatibility

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Actions**:
1. Create `~/.claude/skills/` directory
2. Convert top 3 high-priority skills:
   - `supabase-operations` (from `supabase-ddl-rls.md`)
   - `siso-tasks-cli` (MCP-to-CLI conversion)
   - `feedback-triage` (structured MD → SKILL.md)
3. Test with Claude Code
4. Document results

**Deliverables**:
- 3 converted skills
- Test results
- Lessons learned

### Phase 2: Expansion (Week 2)

**Actions**:
1. Convert remaining 3 skills:
   - `git-workflows`
   - `testing-patterns`
   - `notifications-local`
2. Create skill templates
3. Document best practices
4. Build skills registry

**Deliverables**:
- 6 total converted skills
- Skill templates
- Best practices guide
- Complete registry

### Phase 3: Integration (Week 3-4)

**Actions**:
1. Bridge Tier 1 and Tier 2 skills
2. Create CLI wrappers for engine operations
3. Integrate with BB5 engine
4. Test complete system

**Deliverables**:
- Working hybrid system
- Integration documentation
- Testing framework
- Complete system docs

### Phase 4: Optimization (Month 2+)

**Actions**:
1. Optimize token usage
2. Improve discovery mechanism
3. Add skill testing
4. Create skill analytics

**Deliverables**:
- Token-optimized skills
- Better discovery
- Testing framework
- Analytics dashboard

---

## Documentation Created

### 1. Complete Analysis
**File**: `BLACKBOX5-SKILLS-ANALYSIS.md`
- BB5 current system vs Agent Skills standard
- Detailed comparison
- Best practices
- Hybrid approach recommendation

### 2. Migration Guide
**File**: `SKILLS-MIGRATION-GUIDE.md`
- Step-by-step conversion process
- Conversion templates
- Testing procedures
- Rollback plan

### 3. Complete Registry
**File**: `SKILLS-COMPLETE-REGISTRY.md`
- Inventory of all skills (47 total)
- Conversion status
- Usage statistics
- Maintenance guide

### 4. This Summary
**File**: `SKILLS-RESEARCH-SUMMARY.md`
- Research findings
- Action plan
- Next steps

---

## Action Items

### Immediate (This Week)

1. **✅ Review research documents**
2. **Create `~/.claude/skills/` directory**
3. **Convert first skill** (`supabase-operations`)
4. **Test with Claude Code**

### Short-term (Next 2 Weeks)

1. **Convert 5 more skills** to Agent Skills standard
2. **Create skill templates** for common patterns
3. **Set up multi-project Supabase skills**
4. **Document conversion process**

### Long-term (Next Month)

1. **Convert all remaining skills** (11 total)
2. **Build skills testing framework**
3. **Integrate with BB5 engine**
4. **Create skill analytics**

---

## Best Practices Summary

### For Creating Agent Skills

**YAML Frontmatter** (required):
```yaml
---
name: skill-name (kebab-case)
description: Clear, concise description
tags: [relevant, discoverable, tags]
author: Attribution (optional)
version: 1.0.0 (optional)
---
```

**Content Sections**:
- Purpose (why)
- Prerequisites (what's needed)
- Core commands (how to use)
- Common workflows (typical use cases)
- Troubleshooting (common issues)
- Related skills (cross-references)

**Token Efficiency**:
- Progressive disclosure (load details when needed)
- Don't dump everything upfront
- Use examples sparingly (real, not hypothetical)

**For BB5 Engine Skills**:
- Keep Python-based for complex operations
- Use JSON metadata for simple operations
- Maintain clean separation from agent skills

---

## Key Takeaways

1. **CLI is better than MCP** for agent capabilities (evidence supports this)
2. **Agent Skills standard** is the way to go for universal compatibility
3. **Hybrid approach** is best for BB5 (keep engine skills, adopt agent skills)
4. **Convert current skills** to Agent Skills standard (6 high-priority skills)
5. **Multi-project Supabase** needs environment-specific skills or wrapper scripts

---

## Success Criteria

**Migration Successful When**:
- [ ] All 6 high-priority skills converted to SKILL.md format
- [ ] Skills discoverable by Claude Code
- [ ] Skills work with multiple agent platforms
- [ ] Token usage optimized (on-demand loading)
- [ ] Documentation comprehensive and up-to-date

**System Successful When**:
- [ ] Tier 1 (engine) and Tier 2 (agent) skills integrated
- [ ] Bridge layer working (CLI wrappers)
- [ ] Complete system tested and documented
- [ ] Token efficiency improved by >50%
- [ ] Agent success rate improved by >20%

---

## Next Steps

1. **Review this research** with team
2. **Decide on hybrid approach** (recommended)
3. **Create migration plan** (prioritize skills)
4. **Begin conversion** (start with high-priority)
5. **Test and iterate** (learn and improve)

---

## Resources

### Documentation
- [BLACKBOX5-SKILLS-ANALYSIS.md](./BLACKBOX5-SKILLS-ANALYSIS.md) - Complete analysis
- [SKILLS-MIGRATION-GUIDE.md](./SKILLS-MIGRATION-GUIDE.md) - How to convert
- [SKILLS-COMPLETE-REGISTRY.md](./SKILLS-COMPLETE-REGISTRY.md) - All skills inventory

### External Resources
- [Agent Skills Specification](https://agentskills.io/specification) - Official spec
- [mcp2skill GitHub](https://github.com/fenwei-dev/mcp2skill) - MCP conversion tool
- [mcp2skill Web App](https://mcp2skill.streamlit.app/) - Web interface
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Research Sources
- [MCP vs CLI Benchmark](https://gist.github.com/szymdzum/c3acad9ea58f2982548ef3a9b2cdccce) - CLI 77 vs MCP 60
- [MCP vs CLI Blog](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/) - 120 evaluation runs
- [Did Skills Kill MCP?](https://block.github.io/goose/blog/2025/12/22/agent-skills-vs-mcp/) - Skills vs MCP
- [MCP Token Reduction](https://www.speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2) - 96% reduction

---

**Summary Version**: 1.0.0
**Last Updated**: 2026-01-28
**Status**: Research Complete, Ready for Implementation
**Next Review**: After Phase 1 completion

---

## Conclusion

**The person you encountered was right**: CLI tools are better than MCP for agent capabilities in most scenarios. The evidence shows significant advantages in token efficiency, capability access, and overall performance.

**Black Box 5 is well-positioned**: You already have a two-tier system (engine skills + agent skills). The key is to adopt the Agent Skills standard for Tier 2 while keeping your Python-based Tier 1 engine skills.

**Best path forward**: Hybrid approach - keep what works (engine skills), adopt what's better (Agent Skills standard), and bridge them with CLI wrappers. This gives you the best of both worlds: engine performance and universal agent compatibility.

**Let's get started**: Create `~/.claude/skills/`, convert your top skills, and test with Claude Code. The migration guide has everything you need.

---

**Questions?** Refer to the detailed documentation created, or ask for clarification on any aspect.
