# TASK: Analyze BlackBox5 for Mirror Candidates

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-03
**Context:** Mirror system now exists, need to identify what else to mirror

---

## Objective

Analyze BlackBox5 folder structure to identify which folders would benefit from being mirrored to standalone repos.

---

## Background

We've built a mirror system that syncs folders from BlackBox5 to standalone GitHub repos. This enables:
- Independent deployment (Render, Vercel, etc.)
- Sharing specific components without exposing everything
- Separate CI/CD pipelines per component

YouTube Research is already mirrored. Now we need to identify other candidates.

---

## Analysis Criteria

For each folder, evaluate:

1. **Deployment Need**
   - Does it need its own server/service?
   - Would it benefit from GitHub Actions?
   - Is it deployable (has requirements.txt, Procfile, etc.)?

2. **Independence**
   - Can it work standalone?
   - Are dependencies clearly defined?
   - Would others want to use it alone?

3. **Value**
   - Is it a reusable component?
   - Does it have value outside BlackBox5?
   - Is it worth the maintenance overhead?

4. **Complexity**
   - How hard to extract?
   - How many internal dependencies?
   - Is it tightly coupled to BlackBox5 core?

---

## Folders to Analyze

### High Priority Candidates

- [ ] `skills/` - Skill library
- [ ] `5-project-memory/` - Project memory system
- [ ] `2-engine/agents/` - Agent implementations
- [ ] `2-engine/ralf/` - RALF system
- [ ] `bin/` - CLI tools

### Medium Priority Candidates

- [ ] `6-roadmap/research/documentation/` - Documentation scraper
- [ ] `6-roadmap/research/github/` - GitHub automation
- [ ] `operations/` - Operations tools
- [ ] `.autonomous/` - Autonomous agent system

### Low Priority Candidates

- [ ] `1-docs/` - Documentation
- [ ] `3-experiments/` - Experiments
- [ ] `4-archive/` - Archive

---

## Deliverable

Create a report with:
1. List of recommended mirrors (ranked)
2. For each: rationale, deployment target, complexity
3. Suggested repo names
4. Implementation priority

---

## Related Files

- `.github/MIRROR-SYSTEM.md` - How mirroring works
- `.github/templates/mirror-template.yml` - Template for new mirrors
- `.github/workflows/mirror-youtube-research.yml` - Working example
