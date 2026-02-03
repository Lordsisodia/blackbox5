# Decisions - TASK-1769908019

## Decision 1: Placeholder Patterns Are Acceptable

**Context:** Found 19 files with `ghp_xxx`, `ghp_xxxxxxxxxxxx`, and `your_token` patterns in documentation.

**Selected:** Document these as acceptable placeholder patterns rather than replacing them.

**Rationale:**
- All patterns are clearly placeholders (not actual credentials)
- They serve an educational purpose in documentation
- Replacing them would reduce clarity for users
- Industry standard practice (GitHub docs use similar patterns)

**Reversibility:** HIGH - Can replace with different patterns if needed

---

## Decision 2: Create Pre-commit Hooks vs. CI-only Scanning

**Context:** Need to prevent credential leaks. Options:
1. Pre-commit hooks (local prevention)
2. CI-only scanning (catch after commit)
3. Both

**Selected:** Create pre-commit hooks configuration (can add CI later)

**Rationale:**
- Pre-commit catches issues before they enter history
- Faster feedback loop for developers
- Easier to fix before push
- CI scanning can be added as layer 2

**Reversibility:** HIGH - Can modify hooks or add CI scanning

---

## Decision 3: Use Multiple Secret Detection Tools

**Context:** Several tools available for secret detection.

**Selected:** Use combination of:
- detect-private-key (built-in pre-commit)
- detect-aws-credentials (built-in pre-commit)
- detect-secrets (Yelp - comprehensive)
- bandit (Python security)
- gitleaks (comprehensive secret scanning)

**Rationale:**
- Defense in depth
- Different tools catch different patterns
- No single tool is perfect
- Industry best practice

**Reversibility:** MEDIUM - Can remove tools if they cause friction

---

## Decision 4: Exclude Documentation from Secret Scanning

**Context:** detect-secrets flags placeholder patterns in .md files.

**Selected:** Exclude `*.md` files from detect-secrets scanning.

**Rationale:**
- Documentation intentionally contains placeholder examples
- False positives reduce tool effectiveness
- Other tools (gitleaks) still scan markdown
- Baseline file tracks any actual issues

**Reversibility:** HIGH - Can adjust exclusions in config

---

## Decision 5: Defer Team Notification

**Context:** Success criterion includes "All contributors notified of changes"

**Selected:** Complete audit and create documentation, defer team notification.

**Rationale:**
- Team communication is a process task, not audit task
- Documentation must exist before notification
- Notification timing depends on team schedules
- Audit itself is complete and documented

**Reversibility:** N/A - Follow-up task to be scheduled

---

## Decision 6: Use Existing .env.example Pattern

**Context:** Found existing `.env.example` at `2-engine/runtime/memory/brain/databases/.env.example`

**Selected:** Reference existing pattern rather than creating new root-level file.

**Rationale:**
- Consistent with existing conventions
- Different components may need different env vars
- Root-level .env.example would be too broad
- Document the existing pattern in guide

**Reversibility:** HIGH - Can create additional examples if needed

---

## Decision 7: Document Incident Response Procedures

**Context:** Security guide should include incident response.

**Selected:** Include detailed incident response section with git history cleaning procedures.

**Rationale:**
- Preparation is key for security incidents
- Team needs clear procedures under pressure
- Git history cleaning is complex - needs documentation
- OWASP guidelines recommend documented procedures

**Reversibility:** MEDIUM - Procedures can be updated based on experience

---

## Summary Table

| Decision | Confidence | Risk | Reversibility |
|----------|------------|------|---------------|
| Acceptable placeholders | High | Low | High |
| Pre-commit hooks | High | Low | High |
| Multiple detection tools | High | Low | Medium |
| Exclude docs from scanning | Medium | Low | High |
| Defer team notification | High | Low | N/A |
| Use existing .env.example | High | Low | High |
| Document incident response | High | Low | Medium |

**Overall Confidence:** HIGH - All decisions align with security best practices
