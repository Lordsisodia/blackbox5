# BlackBox5 Mirror System

## What is this?

A system to sync folders from BlackBox5 monorepo to standalone GitHub repos. This lets you:
- Work in BlackBox5's organized structure
- Deploy individual projects to Render/Vercel/etc
- Share specific projects without exposing everything

## How It Works

```
BlackBox5 (monorepo - you work here)
├── 6-roadmap/research/external/YouTube/AI-Improvement-Research/
├── skills/
├── 5-project-memory/
└── ...

    ↓ (GitHub Action on every push)

Standalone Repos (for deployment/sharing)
├── youtube-ai-research ← mirror of YouTube folder
├── blackbox5-skills ← mirror of skills folder
├── project-memory ← mirror of project-memory folder
└── ...
```

## Setup Instructions

### 1. Create Target Repo

Go to https://github.com/new and create a public repo (e.g., `youtube-ai-research`)

### 2. Add Secrets to BlackBox5

Go to BlackBox5 repo → Settings → Secrets and variables → Actions

Add these secrets:
- `MIRROR_TOKEN`: GitHub Personal Access Token with `repo` scope
  - Create at: https://github.com/settings/tokens
  - Needs access to both BlackBox5 and target repos
- `YOUTUBE_RESEARCH_REPO`: `lordsisodia/youtube-ai-research`

### 3. Copy Template

```bash
# From BlackBox5 root
cp .github/templates/mirror-template.yml .github/workflows/mirror-youtube-research.yml

# Edit the file:
# - Replace FOLDER_NAME with actual name
# - Replace FOLDER_PATH with actual path
# - Replace TARGET_REPO_SECRET_NAME with secret name
```

### 4. Commit and Push

```bash
git add .github/workflows/mirror-youtube-research.yml
git commit -m "Add mirror workflow for YouTube research"
git push
```

### 5. Verify

- Make a change in the YouTube folder
- Push to BlackBox5
- Check standalone repo - it should have the change

## Current Mirrors

| Folder | Target Repo | Status |
|--------|-------------|--------|
| `6-roadmap/research/external/YouTube/AI-Improvement-Research/` | `lordsisodia/youtube-ai-research` | ✅ Active |

## Potential Mirrors

These folders could benefit from mirroring:

### High Priority
- `skills/` → Deployable skill library
- `5-project-memory/` → Standalone memory system
- `2-engine/agents/` → Agent marketplace

### Medium Priority
- `6-roadmap/research/documentation/` → Docs scraper
- `6-roadmap/research/github/` → GitHub automation
- `bin/` → CLI tools package

### Low Priority
- `.autonomous/` → RALF system (maybe too core)
- `operations/` → Ops tools

## How to Add a New Mirror

1. **Decide if it needs standalone deployment**
   - Does it need its own Render/Vercel instance?
   - Will others want to use it independently?
   - Does it have different CI/CD needs?

2. **Create target repo**
   ```bash
   # Manual: https://github.com/new
   # Or via CLI:
   gh repo create lordsisodia/REPO_NAME --public
   ```

3. **Add secret to BlackBox5**
   - Name: `REPO_NAME_REPO` (e.g., `SKILLS_REPO`)
   - Value: `lordsisodia/REPO_NAME`

4. **Copy and customize template**
   ```bash
   cp .github/templates/mirror-template.yml .github/workflows/mirror-REPO_NAME.yml
   # Edit: folder path, secret name, etc.
   ```

5. **Test**
   - Make a small change
   - Push to BlackBox5
   - Verify sync worked

## Troubleshooting

**Mirror not working?**
- Check Actions tab for errors
- Verify `MIRROR_TOKEN` has correct permissions
- Ensure target repo exists and is accessible

**Want to exclude files?**
Add to target repo's `.gitignore` after first sync

**Want bidirectional sync?**
Don't. BlackBox5 is source of truth. Edit there, mirror out.

## Architecture Notes

- Uses `git subtree split` to extract folder history
- Force pushes to standalone repo (overwrites history)
- Standalone repo is disposable - source of truth is BlackBox5
- Each mirror is independent

## Future Enhancements

- [ ] Auto-create target repos via GitHub API
- [ ] Sync multiple folders to one repo (combined mirror)
- [ ] Mirror only specific branches
- [ ] Add pre-sync validation
