# BlackBox5 GitHub Actions Workflows

This directory contains automated CI/CD pipelines for BlackBox5.

## Workflows Overview

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `ci.yml` | Push/PR to main | Code quality, security, unit tests |
| **Test Suite** | `test.yml` | Schedule, manual, labeled PRs | Full test suite including integration |
| **Documentation** | `docs.yml` | Docs changes, manual | Build and deploy docs |
| **PR Checks** | `pr-checks.yml` | All PRs | Validate PR standards |
| **Scheduled** | `scheduled.yml` | Daily cron | Maintenance tasks |

## Quick Links

- [Full Documentation](../../1-docs/development/ci-cd/README.md)
- [Setup Guide](../../1-docs/development/ci-cd/SETUP.md)
- [Dependabot Config](../dependabot.yml)

## Status Badges

Add these to your main README.md:

```markdown
![CI](https://github.com/YOUR_USERNAME/blackbox5/actions/workflows/ci.yml/badge.svg)
![Tests](https://github.com/YOUR_USERNAME/blackbox5/actions/workflows/test.yml/badge.svg)
![Docs](https://github.com/YOUR_USERNAME/blackbox5/actions/workflows/docs.yml/badge.svg)
```
