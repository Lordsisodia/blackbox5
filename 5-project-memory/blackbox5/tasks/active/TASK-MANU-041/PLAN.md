# PLAN.md: Automate GitHub Actions Setup

**Task ID:** TASK-MANU-041
**Status:** Planning
**Priority:** LOW
**Created:** 2026-02-05
**Estimated Effort:** 60 minutes
**Source:** Scout opportunity process-008 (Score: 7.0)

---

## 1. First Principles Analysis

### Why Automate GitHub Setup?

1. **Reduce Manual Steps**: Current process requires manual repo creation
2. **Consistency**: Automated setup ensures same configuration every time
3. **Speed**: Faster onboarding for new mirrors/components
4. **Error Reduction**: Eliminates human error in setup
5. **Scalability**: Easy to create multiple repos

### What Happens With Manual Setup?

| Problem | Impact | Severity |
|---------|--------|----------|
| Inconsistent setup | Different repos have different settings | Medium |
| Time consuming | Manual steps for each new repo | Medium |
| Errors | Forgotten settings, wrong permissions | High |
| Knowledge silo | Only some people know the process | Medium |
| Delayed deployment | Waiting for manual setup | Medium |

### How Should GitHub Setup Work?

**Full Automation:**
- Use GitHub CLI (`gh`) for repo creation
- Script the entire setup process
- Configure settings, secrets, and workflows
- One command to create fully configured repo

---

## 2. Current State Assessment

### Current Mirror Setup Process

**Manual Steps (estimated):**
1. Create repo on GitHub (web UI or `gh repo create`)
2. Clone empty repo locally
3. Copy files from BB5 folder
4. Set up GitHub Actions secrets
5. Configure branch protection
6. Push initial commit
7. Verify Actions are working

**Files Involved:**
- `.github/MIRROR-SYSTEM.md` - Documentation
- `.github/templates/mirror-template.yml` - Workflow template
- `.github/workflows/mirror-*.yml` - Existing mirror workflows

### GitHub CLI Capabilities

**Available Commands:**
```bash
gh repo create [name] --public/--private
gh repo clone [name]
gh secret set [name] --body [value]
gh workflow enable [workflow]
gh api repos/{owner}/{repo}/branches/main/protection
```

---

## 3. Proposed Solution

### Automated Setup Script

**Script:** `bin/bb5-create-mirror-repo`

```bash
#!/bin/bash
# Automated mirror repo creation

SOURCE_PATH="$1"
REPO_NAME="$2"
VISIBILITY="${3:-public}"

# 1. Create repo
gh repo create "$REPO_NAME" --"$VISIBILITY" --source="." --remote="origin"

# 2. Copy files from BB5
rsync -av "$SOURCE_PATH/" .

# 3. Set up secrets
gh secret set RENDER_API_KEY --body "$RENDER_API_KEY"
gh secret set OTHER_SECRETS...

# 4. Configure branch protection
gh api repos/{owner}/"$REPO_NAME"/branches/main/protection \
  --input branch-protection.json

# 5. Push
 git push -u origin main

# 6. Verify
gh workflow list
```

### Extended Automation

**Integration with Mirror System:**
- Add to mirror creation workflow
- Trigger on new mirror definition
- Auto-configure based on mirror type

---

## 4. Implementation Plan

### Phase 1: Design Script (15 min)

1. **Define requirements**
   - Required parameters (source path, repo name)
   - Optional parameters (visibility, description)
   - Secrets to configure
   - Settings to apply

2. **Design CLI interface**
   ```
   bb5-create-mirror-repo <source-path> <repo-name> [options]

   Options:
     --private          Create private repo
     --description      Repo description
     --no-workflows     Skip workflow setup
   ```

3. **Document workflow**
   - Step-by-step process
   - Error handling
   - Verification steps

### Phase 2: Implement Script (30 min)

1. **Create base script**
   - Argument parsing
   - Validation
   - Error handling

2. **Add gh CLI integration**
   - Repo creation
   - Secret management
   - Branch protection

3. **Add file operations**
   - Copy from source
   - Initialize git
   - Commit and push

4. **Add verification**
   - Check repo exists
   - Verify workflows
   - Test secrets

### Phase 3: Test and Document (15 min)

1. **Test script**
   - Test with dry-run mode
   - Verify each step
   - Check error handling

2. **Update documentation**
   - Add to MIRROR-SYSTEM.md
   - Create usage examples
   - Document prerequisites

3. **Add to bin/**
   - Make executable
   - Add to PATH if needed
   - Create symlink if appropriate

---

## 5. Success Criteria

- [ ] Script creates repo with one command
- [ ] All required secrets configured
- [ ] Branch protection enabled
- [ ] Files copied from source
- [ ] Workflows functional after creation
- [ ] Documentation updated
- [ ] Error handling tested

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Design | 15 min | 15 min |
| Phase 2: Implement | 30 min | 45 min |
| Phase 3: Test & Doc | 15 min | 60 min |
| **Total** | **60 min** | **~1 hour** |

---

## 7. Rollback Strategy

If script causes issues:

1. **Immediate:** Delete created repo
   ```bash
   gh repo delete owner/repo-name --yes
   ```

2. **Fix:** Debug and fix script
3. **Re-test:** Use dry-run mode first

**Dry-Run Mode:**
```bash
bb5-create-mirror-repo --dry-run <args>
# Shows what would be done without making changes
```

---

## 8. Files to Modify/Create

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `bin/bb5-create-mirror-repo` | Main script | ~150 |
| `bin/bb5-setup-mirror-secrets` | Secret configuration helper | ~80 |

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `.github/MIRROR-SYSTEM.md` | Document automation | +30 |

---

## 9. Prerequisites

**Required:**
- GitHub CLI (`gh`) installed
- Authenticated with `gh auth login`
- Appropriate permissions on GitHub org

**Optional:**
- Render API key (for Render deployment)
- Other service credentials

---

*Plan created: 2026-02-06*
*Ready for implementation*
