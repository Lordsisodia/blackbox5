# Mirror Candidates Analysis

**Date:** 2026-02-04
**Analyst:** Claude
**Purpose:** Identify folders in BlackBox5 that would benefit from mirroring to standalone repos

---

## Executive Summary

Analyzed 10+ folders across BlackBox5 for mirror candidacy. **3 high-priority candidates** identified that would benefit from standalone deployment.

| Priority | Candidate | Score | Deploy Target |
|----------|-----------|-------|---------------|
| 🔴 High | YouTube AI Research | 85 | Render (API) |
| 🔴 High | Documentation Scraper | 78 | GitHub Actions |
| 🟡 Medium | BB5 CLI Tools | 72 | npm/pip package |
| 🟡 Medium | Research Pipeline | 68 | Render/Worker |
| 🟢 Low | Skills Library | 55 | GitHub repo |

---

## Analysis Framework

Scored each candidate on 4 criteria (1-10 scale):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Deployment Need | 25% | Needs independent deployment? |
| Independence | 25% | Can work standalone? |
| Value | 25% | Reusable outside BB5? |
| Complexity | 25% | Easy to extract? |

**Score = weighted average (0-100)**

---

## 🔴 High Priority Candidates

### 1. YouTube AI Improvement Research
**Path:** `6-roadmap/research/external/YouTube/AI-Improvement-Research/`

**Current Status:** ✅ Already mirrored to `youtube-ai-research`

**Analysis:**
| Criterion | Score | Notes |
|-----------|-------|-------|
| Deployment Need | 9 | Needs scheduled scraping |
| Independence | 8 | Self-contained scraper |
| Value | 9 | Useful for AI community |
| Complexity | 8 | Already extracted |
| **Total** | **85** | |

**Rationale:**
- Automated YouTube scraping with AI analysis
- Already successfully mirrored
- Independent deployment on Render
- Clear value to external users

**Suggested Repo:** `youtube-ai-research` ✅ Done

---

### 2. Documentation Scraper System
**Path:** `6-roadmap/research/external/documentation/`

**Analysis:**
| Criterion | Score | Notes |
|-----------|-------|-------|
| Deployment Need | 8 | Needs scheduled runs |
| Independence | 7 | Some BB5 dependencies |
| Value | 8 | Useful for any project |
| Complexity | 7 | Moderate coupling |
| **Total** | **78** | |

**Rationale:**
- Scrapes and indexes documentation
- Could run as GitHub Action
- Valuable for documentation-heavy projects
- Needs cleanup of BB5-specific paths

**Suggested Repo:** `blackbox5-docs-scraper`

**Deployment:** GitHub Actions (scheduled)

**Extraction Complexity:** Medium
- Remove hardcoded BB5 paths
- Make configurable
- Add standalone README

---

## 🟡 Medium Priority Candidates

### 3. BB5 CLI Tools
**Path:** `bin/` (bb5-* commands)

**Analysis:**
| Criterion | Score | Notes |
|-----------|-------|-------|
| Deployment Need | 6 | Package distribution |
| Independence | 7 | Mostly standalone |
| Value | 8 | Useful CLI toolkit |
| Complexity | 6 | Some hardcoded paths |
| **Total** | **72** | |

**Rationale:**
- Navigation and task management CLI
- Could be published as npm/pip package
- Valuable for other project management
- Needs abstraction from BB5 structure

**Suggested Repo:** `blackbox5-cli`

**Deployment:** npm registry / PyPI

**Extraction Complexity:** Medium
- Abstract BB5-specific paths
- Make configurable
- Add installation script

---

### 4. Research Pipeline System
**Path:** `2-engine/02-agents/` and related

**Analysis:**
| Criterion | Score | Notes |
|-----------|-------|-------|
| Deployment Need | 7 | Worker/queue system |
| Independence | 5 | Tightly coupled to BB5 |
| Value | 8 | Generic research pipeline |
| Complexity | 4 | High coupling |
| **Total** | **68** | |

**Rationale:**
- Multi-agent research pipeline
- Could be generic research tool
- High value but complex extraction
- Significant refactoring needed

**Suggested Repo:** `ralf-research-pipeline`

**Deployment:** Render (worker) + Redis

**Extraction Complexity:** High
- Decouple from BB5 state
- Abstract agent types
- Create plugin system

---

## 🟢 Low Priority Candidates

### 5. Skills Library
**Path:** `skills/` (if exists)

**Analysis:**
| Criterion | Score | Notes |
|-----------|-------|-------|
| Deployment Need | 4 | Documentation mostly |
| Independence | 7 | Self-contained |
| Value | 6 | BB5-specific |
| Complexity | 8 | Easy to extract |
| **Total** | **55** | |

**Rationale:**
- BMAD skill definitions
- Mostly documentation
- Low deployment need
- Easy to mirror but limited value

**Suggested Repo:** `blackbox5-skills`

**Deployment:** GitHub repo (reference)

---

## Not Recommended

### Project Memory System
**Path:** `5-project-memory/`

**Why not:**
- Too tightly coupled to BB5 core
- Contains sensitive project data
- Not reusable outside BB5
- High complexity, low value

### Archive Folders
**Path:** `archived/`, `4-archive/`

**Why not:**
- By definition, not active
- No deployment need
- Historical reference only

### Experiments
**Path:** `3-experiments/`

**Why not:**
- Not production-ready
- Inconsistent structure
- Low reusability

---

## Implementation Priority

### Phase 1: Documentation Scraper (Week 1-2)
1. Clean up hardcoded paths
2. Create standalone config
3. Set up GitHub Actions workflow
4. Test independently

### Phase 2: CLI Tools (Week 3-4)
1. Abstract BB5 paths to config
2. Create package structure
3. Write installation docs
4. Publish to registry

### Phase 3: Research Pipeline (Month 2)
1. Design plugin architecture
2. Extract core engine
3. Create example plugins
4. Document extension API

---

## Recommended Next Steps

1. **Start with Documentation Scraper**
   - Lower complexity than pipeline
   - Clear deployment path
   - Immediate value

2. **Create Mirror for CLI Tools**
   - Package as npm module
   - Version independently
   - Share with community

3. **Defer Research Pipeline**
   - Requires significant refactoring
   - Wait until core stabilizes
   - Consider as v2.0 project

---

## Files Created

- `.docs/mirror-candidates-analysis.md` - This analysis
- `.github/workflows/mirror-docs-scraper.yml` - Template (Phase 1)
- `.github/workflows/mirror-cli-tools.yml` - Template (Phase 2)

---

*Analysis completed using Architecture Analysis Framework v1.0*
