# TASK-MANU-041 Analysis: Manual Steps for GitHub Actions Setup

## Task Summary

GitHub repository creation and initial setup requires manual steps that could be automated using the GitHub CLI (`gh`). The mirror workflows exist but setup of new repos still involves manual configuration.

## Key Files Involved

- `/Users/shaansisodia/.blackbox5/.github/workflows/` - 11 workflow files including mirror workflows
- `/Users/shaansisodia/.blackbox5/.github/templates/mirror-template.yml` - Template for mirroring
- `/Users/shaansisodia/.blackbox5/.github/MIRROR-SYSTEM.md` - Documentation for mirroring
- Missing: Automated repo creation script

## Estimated Complexity

**Simple** - Requires:
1. Creating a script using `gh` CLI for repo creation
2. Setting up secrets/tokens
3. Automating workflow file deployment

## Dependencies

- GitHub CLI (`gh`) must be installed and authenticated
- GitHub token with repo creation permissions
- May depend on organization permissions

## Recommended Approach

1. **Create `bb5-create-repo` script** - Wrapper around `gh repo create`
2. **Automate secret setup** - Use `gh secret set` for MIRROR_TOKEN, etc.
3. **Template workflow deployment** - Copy relevant workflows to new repo
4. **Document the automation** - Update MIRROR-SYSTEM.md with automated approach

## Current State

From `/Users/shaansisodia/.blackbox5/.github/templates/mirror-template.yml`:
```yaml
# Instructions:
# 1. Copy this file to .github/workflows/mirror-{folder-name}.yml
# 2. Replace PLACEHOLDER values below
# 3. Create GitHub secret for the target repo
# 4. Commit and push
```

This is currently a manual 4-step process per mirror target.

## Existing Mirror Workflows

- `mirror-bin.yml` - Mirrors bin/ folder
- `mirror-blackbox5-memory.yml` - Mirrors 5-project-memory/
- `mirror-siso-engine.yml` - Mirrors 2-engine/
- `mirror-siso-internal-memory.yml` - Mirrors internal memory
- `mirror-siso-research-bank.yml` - Mirrors research bank
- `mirror-youtube-research.yml` - Mirrors YouTube research

## Suggested Implementation

Create `/Users/shaansisodia/.blackbox5/bin/bb5-create-mirror-repo`:
```bash
#!/bin/bash
# Usage: bb5-create-mirror-repo <folder-path> <target-repo-name>
# Creates repo, sets secrets, generates workflow file
```
