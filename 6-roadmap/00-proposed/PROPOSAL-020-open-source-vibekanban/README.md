# PROPOSAL-020: Open Source Black Box with VibeKanban Integration

**Status:** 💡 Proposed
**Priority:** 🔴 High
**Domain:** Product / Integrations
**Created:** 2026-01-20

---

## Overview

Transform Black Box 5 into an open-source GitHub repository with integrated VibeKanban task management, creating a unified platform that cross-promotes SISO Agency's capabilities.

---

## The Vision

### Core Idea
1. **Fork and rebrand VibeKanban** as "CISO Blackbox" or "SISO Task Manager"
2. **Make Black Box 5 open-source** on GitHub
3. **Create a landing page** on sisos.agency showcasing the project
4. **Build content around** "Building the Black Box" - dev journey

### Cross-Promotion Strategy
```
Black Box OSS (GitHub)
    ↓
SISO Agency Landing Page
    ↓
Content: "Building the Black Box"
    ↓
Showcases:
  • App development for e-commerce
  • AI agent orchestration
  • Task management systems
  • Agency technical capabilities
```

---

## Why This Matters

### For SISO Agency
- ✅ **Portfolio piece** - Working open-source project
- ✅ **Technical showcase** - Demonstrates AI engineering
- ✅ **Content engine** - Endless blog/video topics
- ✅ **Lead magnet** - Attracts clients interested in AI dev

### For Black Box
- ✅ **Community contributions** - Open-source collaborators
- ✅ **Credibility** - Public GitHub history
- ✅ **Task management** - VibeKanban UI built-in
- ✅ **Integration** - Single unified platform

### For Users
- ✅ **Free tool** - Open-source AI agent platform
- ✅ **Professional UI** - Battle-tested VibeKanban interface
- ✅ **Extensible** - Can fork and customize

---

## Technical Approach

### Option A: Fork & Rebrand (Recommended)

**Structure:**
```
blackbox5/
├── vibe-kanban/          ← Forked VibeKanban (branded)
│   ├── frontend/
│   ├── crates/
│   └── db.sqlite
├── 2-engine/             ← Black Box engine
├── 5-project-memory/     ← Memory system
└── 1-agents/             ← Agent system
```

**Changes to VibeKanban:**
1. Replace logos (SVG files)
2. Update app name (3 files)
3. Change GitHub links
4. Optionally update colors

**Upstream Integration:**
```bash
git remote add upstream https://github.com/BloopAI/vibe-kanban.git
git fetch upstream
git merge upstream/main
```

### Launch Strategy
```bash
# One-package launcher
#!/bin/bash
cd vibe-kanban
npm exec vibe-kanban@latest &  # UI (branded as CISO Blackbox)

cd ../2-engine
python engine.py --mcp-host localhost --mcp-port 3001 &
```

---

## Implementation Checklist

### Phase 1: Fork & Rebrand
- [ ] Create GitHub fork: `sisos-internal/vibe-kanban`
- [ ] Replace logo SVGs
- [ ] Update `frontend/index.html` title
- [ ] Update `site.webmanifest` app name
- [ ] Update i18n strings (all languages)
- [ ] Update GitHub links in code/docs
- [ ] Test build locally

### Phase 2: Open Source Prep
- [ ] Add LICENSE file
- [ ] Create CONTRIBUTING.md
- [ ] Add README with quick start
- [ ] Set up GitHub Actions (CI)
- [ ] Create issue templates
- [ ] Add PR templates

### Phase 3: SISO Agency Integration
- [ ] Design landing page (sisos.agency/blackbox)
- [ ] Write "About" page
- [ ] Create demo video
- [ ] Set up analytics
- [ ] Add CTA for agency services

### Phase 4: Content Launch
- [ ] Blog post: "Introducing Black Box 5"
- [ ] Video series: "Building the Black Box"
- [ ] Case studies: e-commerce apps built with Black Box
- [ ] Developer tutorials
- [ ] Agency service pages

---

## Success Metrics

### Product Metrics
- ⭐ GitHub stars
- 🍴 Forks and contributors
- 📥 npm/package downloads
- 🌐 Web traffic to landing page

### Business Metrics
- 📧 Agency leads from Black Box
- 💰 Client projects referencing Black Box
- 🎤 Speaking opportunities
- 📰 Press mentions

### Content Metrics
- 📺 Video views
- 📝 Blog readership
- 🐦 Social engagement
- 🔗 Backlinks to SISO Agency

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fork maintenance overhead | Medium | Keep branding changes minimal; automate upstream merges |
| Competitors copy approach | Low | Focus on agency services and expertise |
| Time distraction from client work | Medium | Content creates same value as client work |
| Open-source security issues | Medium | Security audit before launch; dependency scanning |

---

## Dependencies

**Blocks:** Nothing
**Blocked By:** Nothing
**Requires:**
- VibeKanban fork setup
- GitHub organization setup
- Landing page design/development

---

## Related Items

- **PROPOSAL-013:** Integrations Research
- **PLAN-005:** Initialize Vibe Kanban Database
- **Roadmap Item:** SISO Agency website development

---

## Next Steps

1. **Validate feasibility** - Can we legally fork VibeKanban?
2. **Scope branding changes** - What exactly needs to change?
3. **Design landing page** - Mock up the SISO Agency page
4. **Plan content calendar** - What to publish and when?
5. **Set up GitHub repo** - Create organization and repository

---

**Discussion:** This proposal is open for feedback. Should we prioritize this higher or lower? What risks am I missing?

**Last Updated:** 2026-01-20
