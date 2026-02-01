---
catalog_type: blackbox5_universal_index
version: 5.0.0
generated: 2026-01-20T10:45:49.562932
total_agents: 21
total_tools: 106
total_integrations: 9
---

# BLACKBOX5 Universal Catalog

> The master index of all BLACKBOX5 components. This file makes every agent, tool, integration, and capability discoverable with minimal context.

## 📊 Quick Stats

| Category | Count |
|----------|-------|
| **Agents** | 21 |
| **Tools** | 106 |
| **Integrations** | 9 |
| **Capabilities** | 20 |
| **Knowledge Systems** | 7 |
| **Operations** | 8 |

---

## 🤖 AGENTS (21)

### Core Agents (3)

**ArchitectAgent**
- **Location:** `2-engine/01-core/agents/ArchitectAgent.py`
- **Description:** Architect Agent - Alex 🏗️

Specializes in:
- System architecture
- Design patterns
- Technical plann...

**AnalystAgent**
- **Location:** `2-engine/01-core/agents/AnalystAgent.py`
- **Description:** Analyst Agent - Mary 📊

Specializes in:
- Research and investigation
- Data analysis
- Competitive a...

**DeveloperAgent**
- **Location:** `2-engine/01-core/agents/DeveloperAgent.py`
- **Description:** Developer Agent - Amelia 💻

Specializes in:
- Code implementation
- Debugging and troubleshooting
- ...

### Specialist Agents (18)


**Research Specialist**
- **ID:** `specialists/research-specialist`
- **Role:** Technical Research and Analysis Specialist
- **Location:** `2-engine/01-core/agents/research-specialist.yaml`
- **Description:** Expert technical researcher specializing in comprehensive technology research, competitive analysis,...

**Monitoring & Observability Specialist**
- **ID:** `specialists/monitoring-specialist`
- **Role:** Application monitoring and observability specialist
- **Location:** `2-engine/01-core/agents/monitoring-specialist.yaml`
- **Description:** Expert in implementing comprehensive monitoring solutions that provide visibility into system health...

**Backend Specialist**
- **ID:** `specialists/backend-specialist`
- **Role:** Backend Development and Server Architecture Specialist
- **Location:** `2-engine/01-core/agents/backend-specialist.yaml`
- **Description:** Expert backend developer specializing in scalable server-side solutions, RESTful and GraphQL APIs, m...

**Frontend Specialist**
- **ID:** `specialists/frontend-specialist`
- **Role:** Frontend Development and UI/UX Architecture Specialist
- **Location:** `2-engine/01-core/agents/frontend-specialist.yaml`
- **Description:** Expert frontend developer specializing in modern JavaScript frameworks, responsive design, and user ...

**Database Specialist**
- **ID:** `specialists/database-specialist`
- **Role:** Database design and optimization specialist
- **Location:** `2-engine/01-core/agents/database-specialist.yaml`
- **Description:** Database expert focused on designing efficient, scalable database schemas and optimizing query perfo...

**UI/UX Specialist**
- **ID:** `specialists/ui-ux-specialist`
- **Role:** UI/UX design and user experience specialist
- **Location:** `2-engine/01-core/agents/ui-ux-specialist.yaml`
- **Description:** Expert in crafting intuitive, accessible, and delightful user interfaces. Focuses on user-centered d...

**Performance Specialist**
- **ID:** `specialists/performance-specialist`
- **Role:** Performance optimization and profiling specialist
- **Location:** `2-engine/01-core/agents/performance-specialist.yaml`
- **Description:** Performance optimization expert focused on identifying bottlenecks, improving application speed, and...

**Machine Learning Specialist**
- **ID:** `specialists/ml-specialist`
- **Role:** Machine Learning and AI Development Specialist
- **Location:** `2-engine/01-core/agents/ml-specialist.yaml`
- **Description:** Expert machine learning engineer specializing in model development, training pipelines, deployment, ...

**Accessibility Specialist**
- **ID:** `specialists/accessibility-specialist`
- **Role:** Accessibility and inclusive design specialist
- **Location:** `2-engine/01-core/agents/accessibility-specialist.yaml`
- **Description:** Expert in ensuring digital products are accessible to all users, regardless of ability. Deep knowled...

**Mobile Development Specialist**
- **ID:** `specialists/mobile-specialist`
- **Role:** Mobile development and mobile-first design specialist
- **Location:** `2-engine/01-core/agents/mobile-specialist.yaml`
- **Description:** Expert in building high-quality mobile applications across iOS, Android, and cross-platform framewor...

**Compliance & Governance Specialist**
- **ID:** `specialists/compliance-specialist`
- **Role:** Regulatory compliance and governance specialist
- **Location:** `2-engine/01-core/agents/compliance-specialist.yaml`
- **Description:** Expert in navigating complex regulatory landscapes and ensuring organizational compliance. Deep know...

**Testing Specialist**
- **ID:** `specialists/testing-specialist`
- **Role:** Test strategy and quality assurance specialist
- **Location:** `2-engine/01-core/agents/testing-specialist.yaml`
- **Description:** Quality assurance expert focused on comprehensive testing strategies, test-driven development, and e...

**Documentation Specialist**
- **ID:** `specialists/documentation-specialist`
- **Role:** Technical documentation and API documentation specialist
- **Location:** `2-engine/01-core/agents/documentation-specialist.yaml`
- **Description:** Technical writing expert focused on creating clear, comprehensive documentation that helps developer...

**API Specialist**
- **ID:** `specialists/api-specialist`
- **Role:** API design and integration specialist
- **Location:** `2-engine/01-core/agents/api-specialist.yaml`
- **Description:** API architecture expert focused on designing robust, scalable APIs and seamless integrations. Specia...

**Integration Specialist**
- **ID:** `specialists/integration-specialist`
- **Role:** Third-party integrations and API specialist
- **Location:** `2-engine/01-core/agents/integration-specialist.yaml`
- **Description:** Expert in connecting systems with external services and APIs. Specializes in planning, implementing,...

**DevOps Specialist**
- **ID:** `specialists/devops-specialist`
- **Role:** DevOps and Deployment Automation Specialist
- **Location:** `2-engine/01-core/agents/devops-specialist.yaml`
- **Description:** Expert DevOps engineer specializing in continuous integration/deployment pipelines, container orches...

**Data Specialist**
- **ID:** `specialists/data-specialist`
- **Role:** Data Engineering and ETL Pipeline Specialist
- **Location:** `2-engine/01-core/agents/data-specialist.yaml`
- **Description:** Expert data engineer specializing in building scalable data pipelines, ETL/ELT processes, data wareh...

**Security Specialist**
- **ID:** `specialists/security-specialist`
- **Role:** Security analysis and vulnerability detection specialist
- **Location:** `2-engine/01-core/agents/security-specialist.yaml`
- **Description:** Expert security specialist focused on identifying vulnerabilities, ensuring secure coding practices,...

---

## 🛠️ TOOLS (106)

### Core (23)

- **get_global_registry** - `2-engine/05-tools/core/registry.py`
- **_register_default_tools** - `2-engine/05-tools/core/registry.py`
- **get_tool** - `2-engine/05-tools/core/registry.py`
- **register_tool** - `2-engine/05-tools/core/registry.py`
- **list_tools** - `2-engine/05-tools/core/registry.py`
- _... and 18 more_

### Data_Tools (50)

- **main** - `2-engine/05-tools/data_tools/domain_scanner.py`
- **__init__** - `2-engine/05-tools/data_tools/domain_scanner.py`
- **scan_all** - `2-engine/05-tools/data_tools/domain_scanner.py`
- **_scan_domain** - `2-engine/05-tools/data_tools/domain_scanner.py`
- **_determine_domain_type** - `2-engine/05-tools/data_tools/domain_scanner.py`
- _... and 45 more_

### Execution (2)

- **_is_dangerous_command** - `2-engine/05-tools/execution/bash_tool.py`
- **generate_index** - `2-engine/05-tools/execution/indexer.py`

### File-Ops (4)

- **_collect_files** - `2-engine/05-tools/file-ops/search_tool.py`
- **_is_path_allowed** - `2-engine/05-tools/file-ops/search_tool.py`
- **_is_path_allowed** - `2-engine/05-tools/file-ops/file_tools.py`
- **_is_path_allowed** - `2-engine/05-tools/file-ops/file_tools.py`

### Git (9)

- **run_cmd** - `2-engine/05-tools/git/git_ops.py`
- **status** - `2-engine/05-tools/git/git_ops.py`
- **check_clean_state** - `2-engine/05-tools/git/git_ops.py`
- **get_modified_files** - `2-engine/05-tools/git/git_ops.py`
- **commit_task** - `2-engine/05-tools/git/git_ops.py`
- _... and 4 more_

### Utils (18)

- **check_health** - `2-engine/05-tools/utils/context_manager.py`
- **__post_init__** - `2-engine/05-tools/utils/tui_logger.py`
- **to_dict** - `2-engine/05-tools/utils/tui_logger.py`
- **__init__** - `2-engine/05-tools/utils/tui_logger.py`
- **save_task_context** - `2-engine/05-tools/utils/tui_logger.py`
- _... and 13 more_

---

## 🔌 INTEGRATIONS (9)

- **vercel** - `2-engine/06-integrations/vercel`
- **cloudflare** - `2-engine/06-integrations/cloudflare`
- **mcp** - `2-engine/06-integrations/mcp`
- **notion** - `2-engine/06-integrations/notion`
- **supabase** - `2-engine/06-integrations/supabase`
- **github** - `2-engine/06-integrations/github`
- **obsidian** - `2-engine/06-integrations/obsidian`
- **vibe** - `2-engine/06-integrations/vibe`
- **github-actions** - `2-engine/06-integrations/github-actions`

---

## 📁 DIRECTORY STRUCTURE

- **01-core** - `01-core` - 
- **2-engine** - `2-engine` - Multi-agent orchestration system with intelligent task routing, wave-based parallelization, and proa
- **3-gui** - `3-gui` - This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.
- **5-project-memory** - `5-project-memory` - This folder contains project-specific memory structures for BlackBox5.
- **6-roadmap** - `6-roadmap` - 


---

## 🔍 SEARCH INDEX

Quick keyword lookup for common searches:

| Want to find... | Look in... |
|----------------|------------|
| Start Blackbox5 | `start.sh`, `blackbox.py` |
| All agents | `2-engine/01-core/agents/` |
| API server | `2-engine/01-core/interface/api/main.py` |
| Vibe Kanban | `3-gui/vibe-kanban/` |
| Tools | `2-engine/05-tools/` |
| Integrations | `2-engine/06-integrations/` |
| Agent capabilities | `2-engine/02-agents/capabilities/` |
| Knowledge systems | `2-engine/03-knowledge/` |
| Runtime operations | `2-engine/07-operations/` |
| Project memory | `5-project-memory/` |
| Roadmap | `6-roadmap/` |

---

## 💡 How AI Agents Use This Catalog

1. **Finding Components:** Read the relevant section to get exact file paths
2. **Understanding Structure:** Check DIRECTORY STRUCTURE for overview
3. **Locating Functions:** Use SEARCH INDEX for quick lookups
4. **Agent Selection:** Review AGENTS section to pick the right agent

---

## 🔎 CODE SEARCH

BLACKBOX5 provides two powerful search systems for navigating the codebase:

### 1. Code Search Utility (ripgrep-all)

**Location:** `2-engine/01-core/utilities/code_search.py`

Fast, comprehensive search across 150+ file types including code, documentation, PDFs, and archives.

**Usage:**
```python
from utilities.code_search import quick_search, find_files, find_symbol

# Quick search
results = quick_search("AgentLoader")
for r in results.results:
    print(f"{r.path}:{r.line_number} - {r.content}")

# Find files by pattern
files = find_files("*.yaml")

# Find symbol references
refs = find_symbol("AgentTask", file_type="py")
```

**Features:**
- Search across source code, docs, PDFs, archives
- Context-aware results (configurable lines before/after)
- File type filtering (py, md, json, etc.)
- Case-insensitive by default
- Excludes build artifacts (.git, node_modules, etc.)

### 2. Tree-sitter MCP Server

**Location:** Configured in `2-engine/.config/mcp-servers.json`

Provides semantic code understanding through Abstract Syntax Tree (AST) parsing.

**Capabilities:**
- Code structure analysis
- Definition and reference search
- Function/class extraction
- Syntax-aware navigation

**MCP Tools Available:**
- `code_parser.parse_file` - Parse a file into AST
- `code_parser.find_definitions` - Find symbol definitions
- `code_parser.find_references` - Find symbol references
- `code_parser.get_structure` - Get file structure

### Search Comparison

| Feature | ripgrep-all | Tree-sitter MCP |
|---------|-------------|-----------------|
| Speed | Instant | Fast |
| Scope | All file types | Code files only |
| Understanding | Text-based | Semantic (AST) |
| Best For | Quick searches, docs | Code navigation, refactoring |

---

## 🔄 Updating This Catalog

This catalog is auto-generated by `scripts/generate_catalog.py`. To update:

```bash
python scripts/generate_catalog.py > CATALOG.md
```

Always regenerate after:
- Adding new agents
- Adding new tools
- Restructuring directories
- Major code changes

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*BLACKBOX5 Version: 5.0.0*
