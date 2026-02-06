# PLAN.md: Analyze BlackBox5 for Mirror Candidates

**Task ID:** TASK-analyze-mirror-candidates
**Status:** Planning
**Priority:** MEDIUM
**Created:** 2026-02-03
**Estimated Effort:** 90 minutes

---

## 1. First Principles Analysis

### Why Mirror Components?

1. **Independent Deployment**: Components can be deployed separately (Render, Vercel, etc.)
2. **Selective Sharing**: Share specific components without exposing everything
3. **Separate CI/CD**: Each component has its own pipeline
4. **Focused Development**: Contributors work on specific repos
5. **Version Management**: Components versioned independently

### What Happens Without Mirroring?

| Problem | Impact | Severity |
|---------|--------|----------|
| Monolithic deployment | All or nothing deployment | Medium |
| Access control | Cannot grant limited access | Medium |
| CI/CD complexity | Single pipeline for everything | Medium |
| Contributor friction | Must understand entire system | Low |
| Scaling limitations | Cannot scale components independently | Low |

### How Should Mirror Candidates Be Evaluated?

**Four Criteria Framework:**
1. **Deployment Need**: Does it need its own server/service?
2. **Independence**: Can it work standalone?
3. **Value**: Is it reusable outside BlackBox5?
4. **Complexity**: How hard to extract?

---

## 2. Current State Assessment

### Existing Mirror System

**Location:** `.github/workflows/mirror-*.yml`

**How It Works:**
- GitHub Actions workflow triggers on changes
- Syncs specific folder to standalone repo
- Maintains bidirectional or unidirectional sync
- YouTube Research already mirrored

**YouTube Research Mirror:**
- Source: `6-roadmap/research/external/YouTube/AI-Improvement-Research/`
- Target: Standalone GitHub repo
- Deployment: Render/Vercel ready

### Folder Structure to Analyze

```
~/.blackbox5/
├── 1-docs/                    # Documentation
├── 2-engine/                  # Core engine (RALF, agents)
│   ├── .autonomous/agents/    # Agent implementations
│   ├── .autonomous/lib/       # Shared libraries
│   ├── core/                  # Core interfaces
│   └── ralf/                  # RALF system
├── 3-experiments/             # Experiments
├── 4-archive/                 # Archive
├── 5-project-memory/          # Project workspaces
│   └── [project]/
│       ├── .autonomous/       # Autonomous agent system
│       ├── knowledge/         # Research, patterns
│       ├── operations/        # Operations tools
│       └── tasks/             # Task management
├── 6-roadmap/                 # Plans and roadmaps
│   └── research/              # Research projects
│       ├── documentation/     # Documentation scraper
│       ├── external/          # External projects
│       └── github/            # GitHub automation
└── bin/                       # CLI tools
```

---

## 3. Proposed Solution

### Mirror Candidate Evaluation Matrix

**Scoring:**
- Deployment Need: 0-3 (0=none, 3=critical)
- Independence: 0-3 (0=tightly coupled, 3=standalone)
- Value: 0-3 (0=internal only, 3=widely useful)
- Complexity: 0-3 (0=hard, 3=easy)

**Total Score = Deployment + Independence + Value + (3 - Complexity)**

### High Priority Candidates (Score 8+)

| Component | Deploy | Indep | Value | Complexity | Score | Rationale |
|-----------|--------|-------|-------|------------|-------|-----------|
| **skills/** | 3 | 3 | 3 | 2 | 10 | Reusable skill library |
| **2-engine/agents/** | 3 | 2 | 2 | 2 | 8 | Agent framework |
| **2-engine/ralf/** | 3 | 2 | 2 | 1 | 8 | RALF orchestration |
| **bin/** | 2 | 3 | 2 | 2 | 8 | CLI toolkit |

### Medium Priority Candidates (Score 6-7)

| Component | Deploy | Indep | Value | Complexity | Score | Rationale |
|-----------|--------|-------|-------|------------|-------|-----------|
| **6-roadmap/research/documentation/** | 2 | 3 | 2 | 2 | 7 | Doc scraper service |
| **6-roadmap/research/github/** | 2 | 2 | 2 | 2 | 6 | GitHub automation |
| **5-project-memory/[project]/.autonomous/** | 2 | 2 | 1 | 2 | 6 | Autonomous system |
| **operations/** | 1 | 2 | 2 | 2 | 6 | Operations tools |

### Low Priority Candidates (Score < 6)

| Component | Deploy | Indep | Value | Complexity | Score | Rationale |
|-----------|--------|-------|-------|------------|-------|-----------|
| **1-docs/** | 1 | 3 | 1 | 3 | 5 | Documentation site |
| **3-experiments/** | 1 | 2 | 1 | 2 | 4 | Experimental |
| **4-archive/** | 0 | 1 | 0 | 3 | 1 | Archive only |

---

## 4. Implementation Plan

### Phase 1: Deep Analysis (30 min)

1. **Analyze each high-priority candidate**
   - Review folder structure
   - Identify dependencies
   - Check for deployment artifacts (requirements.txt, Procfile, etc.)
   - Document internal coupling

2. **Evaluate deployment targets**
   - Render (good for Python services)
   - Vercel (good for static sites/Next.js)
   - GitHub Actions (good for automation)
   - npm/pip registry (good for libraries)

3. **Assess extraction complexity**
   - Count internal dependencies
   - Identify hardcoded paths
   - Document required refactoring

### Phase 2: Create Recommendations (30 min)

1. **Rank candidates by score and effort**
   - High value + low effort = immediate
   - High value + high effort = planned
   - Low value = deferred

2. **Define repo names**
   - Follow naming conventions
   - Check availability on GitHub
   - Consider organization structure

3. **Create implementation priority**
   - Quick wins first
   - Dependencies considered
   - Resource requirements

### Phase 3: Generate Report (30 min)

1. **Create analysis report**
   - Executive summary
   - Detailed candidate analysis
   - Implementation roadmap
   - Resource requirements

2. **Document in BB5**
   - Add to knowledge/research/
   - Link from mirror system docs
   - Update .github/MIRROR-SYSTEM.md

---

## 5. Success Criteria

- [ ] All folders analyzed against 4 criteria
- [ ] Scoring completed for each candidate
- [ ] Deployment targets identified
- [ ] Extraction complexity assessed
- [ ] Recommendations ranked by priority
- [ ] Suggested repo names defined
- [ ] Implementation roadmap created
- [ ] Report documented in BB5

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Deep Analysis | 30 min | 30 min |
| Phase 2: Recommendations | 30 min | 60 min |
| Phase 3: Report | 30 min | 90 min |
| **Total** | **90 min** | **~1.5 hours** |

---

## 7. Deliverables

### Mirror Candidates Report

**Structure:**
```markdown
# BB5 Mirror Candidates Analysis

## Executive Summary
- Total candidates analyzed: X
- Recommended for immediate mirroring: Y
- Planned for future: Z
- Deferred: W

## High Priority Candidates

### 1. skills/ Library
**Score:** 10/12
**Rationale:** [explanation]
**Deployment Target:** pip registry + GitHub
**Complexity:** Medium
**Suggested Repo:** blackbox5-skills

[Detailed analysis...]

## Implementation Roadmap

### Phase 1 (Immediate)
- [ ] skills/ extraction
- [ ] bin/ CLI toolkit

### Phase 2 (Planned)
- [ ] 2-engine/agents/
- [ ] 2-engine/ralf/

### Phase 3 (Future)
- [ ] Documentation scraper
- [ ] GitHub automation
```

---

## 8. Related Files

- `.github/MIRROR-SYSTEM.md` - How mirroring works
- `.github/templates/mirror-template.yml` - Template for new mirrors
- `.github/workflows/mirror-youtube-research.yml` - Working example

---

*Plan created: 2026-02-06*
*Ready for implementation*
