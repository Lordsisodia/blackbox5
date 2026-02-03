# SISO Research Organization

## Overview

A network of interconnected repositories for the SISO (Shaan's Intelligent Systems Organization) research ecosystem. Each repo can be used standalone or as part of the larger BlackBox5 system.

## Repository Architecture

### Core Infrastructure

| Repo | Source Folder | Purpose | Deploy To |
|------|--------------|---------|-----------|
| **siso-engine** | `2-engine/` | Core agent engine, RALF runtime | PyPI, Docker |
| **siso-skills** | `skills/` (to be created) | Reusable skill library | PyPI |
| **siso-cli** | `bin/` | Command-line tools | Homebrew, npm |

### Research Projects

| Repo | Source Folder | Purpose | Deploy To |
|------|--------------|---------|-----------|
| **youtube-ai-research** | `6-roadmap/research/external/YouTube/AI-Improvement-Research/` | YouTube video scraping & analysis | Render, GitHub Actions |
| **siso-research-bank** | `6-roadmap/research/` | All research projects combined | GitHub Pages |
| **docs-scraper** | `6-roadmap/research/documentation/` | Documentation scraping system | Render |
| **github-research** | `6-roadmap/research/github/` | GitHub automation & analysis | Render |

### Project Memory

| Repo | Source Folder | Purpose | Deploy To |
|------|--------------|---------|-----------|
| **siso-internal-memory** | `5-project-memory/siso-internal/` | SISO Internal project memory | Supabase, Vercel |
| **blackbox5-memory** | `5-project-memory/blackbox5/` | BlackBox5 project memory | Supabase, Vercel |
| **team-entrepreneurship-memory** | `5-project-memory/team-entrepreneurship-memory/` | Team entrepreneurship memory | Supabase, Vercel |

### BlackBox5 (Hub)

| Repo | Purpose |
|------|---------|
| **blackbox5** | Main monorepo - contains all source code, syncs to other repos |

---

## Repository Relationships

```
blackbox5 (monorepo - source of truth)
    ├── mirrors to → siso-engine
    ├── mirrors to → siso-skills
    ├── mirrors to → siso-cli
    ├── mirrors to → youtube-ai-research
    ├── mirrors to → siso-research-bank
    ├── mirrors to → docs-scraper
    ├── mirrors to → github-research
    ├── mirrors to → siso-internal-memory
    ├── mirrors to → blackbox5-memory
    └── mirrors to → team-entrepreneurship-memory

siso-engine (standalone usable)
    └── used by → all other repos

siso-skills (standalone usable)
    └── used by → siso-engine, youtube-ai-research

youtube-ai-research (standalone usable)
    └── depends on → siso-engine (optional)
```

---

## Quick Links

### Core
- [siso-engine](https://github.com/lordsisodia/siso-engine) - Agent runtime
- [siso-skills](https://github.com/lordsisodia/siso-skills) - Skill library
- [siso-cli](https://github.com/lordsisodia/siso-cli) - CLI tools

### Research
- [youtube-ai-research](https://github.com/lordsisodia/youtube-ai-research) - YouTube scraping
- [siso-research-bank](https://github.com/lordsisodia/siso-research-bank) - Research archive
- [docs-scraper](https://github.com/lordsisodia/docs-scraper) - Documentation scraper
- [github-research](https://github.com/lordsisodia/github-research) - GitHub analysis

### Memory
- [siso-internal-memory](https://github.com/lordsisodia/siso-internal-memory) - SISO Internal
- [blackbox5-memory](https://github.com/lordsisodia/blackbox5-memory) - BlackBox5
- [team-entrepreneurship-memory](https://github.com/lordsisodia/team-entrepreneurship-memory) - Team projects

---

## Setup Instructions

### For Users (Standalone)

```bash
# Install core
pip install siso-engine
pip install siso-skills

# Clone specific research project
git clone https://github.com/lordsisodia/youtube-ai-research.git
cd youtube-ai-research
pip install -r requirements.txt
python scripts/collect_all.py
```

### For Developers (Full BlackBox5)

```bash
# Clone main monorepo
git clone https://github.com/lordsisodia/blackbox5.git
cd blackbox5

# All code is here, organized by function
# Changes auto-sync to standalone repos via GitHub Actions
```

---

## Mirror Workflows

Each standalone repo is automatically synced from BlackBox5 via GitHub Actions:

```yaml
# In BlackBox5/.github/workflows/mirror-{repo}.yml
name: Mirror to {repo}
on:
  push:
    paths: ['path/to/folder/**']
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: git subtree split --prefix=path/to/folder -b temp
      - run: git push https://x-access-token:${{ secrets.TOKEN }}@github.com/lordsisodia/{repo}.git temp:main --force
```

---

## Contributing

1. **Work in BlackBox5** - This is the source of truth
2. **Test standalone** - Ensure it works independently
3. **Commit to BlackBox5** - Auto-syncs to standalone repos
4. **Version in standalone** - Tags/releases happen in standalone repos

---

## License

Private research repositories.
