---
name: Git Safety Protocol
trigger:
  - git
  - commit
  - push
  - branch
paths:
  - ".git/**"
alwaysApply: true
priority: 100
---

# Git Safety Protocol

## NEVER Do
- Update git config
- Run destructive commands (push --force, reset --hard, checkout ., restore ., clean -f, branch -D) unless explicitly requested
- Skip hooks (--no-verify, --no-gpg-sign) unless explicitly requested
- Force push to main/master (warn user if requested)
- Amend published commits (create NEW commits instead)

## ALWAYS Do
- Create NEW commits rather than amending (unless user explicitly requests amend)
- Stage specific files by name (avoid `git add -A` or `git add .`)
- Ask before committing unless explicitly requested
- Check for secrets before committing (.env, credentials.json)

## Why
Safety first. Git operations can be destructive and hard to reverse.

## Source
- CLAUDE.md Git Safety Protocol
- LEGACY.md git workflows
