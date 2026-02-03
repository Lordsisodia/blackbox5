# Aqua Voice AI-Optimized Prompts

**Project:** Voice transcription optimization for AI consumption
**Started:** 2026-02-04
**Status:** Active iteration

## Overview

This directory contains iterative versions of custom instructions for Aqua Voice (voice transcription app) to optimize output for AI consumption—particularly Claude Code CLI.

## Directory Structure

```
aqua-voice-prompts/
├── README.md                 # This file
├── ITERATION_LOG.md          # Chronological log of changes
├── TEST_RESULTS.md           # A/B testing results
├── CURRENT.md                # Symlink to current version
├── versions/
│   ├── v1.0.0-baseline/      # Initial research-based prompt
│   ├── v1.1.0-*/             # Future iterations
│   └── ...
└── research/
    ├── findings.md           # Research synthesis
    └── references/           # External sources
```

## Version Naming Convention

- `v{major}.{minor}.{patch}-{descriptor}`
- **Major:** Significant architectural changes
- **Minor:** New features or modes
- **Patch:** Bug fixes, tweaks
- **Descriptor:** Brief context (e.g., `baseline`, `code-focused`, `minimal`)

## Iteration Process

1. **Test** current version in real scenarios
2. **Document** issues, successes, observations in ITERATION_LOG.md
3. **Analyze** patterns across multiple uses
4. **Design** improvements
5. **Create** new version folder with updated prompt
6. **A/B test** against previous version
7. **Promote** to CURRENT.md if better

## Active Versions

| Version | Status | Focus | Last Tested |
|---------|--------|-------|-------------|
| v1.0.0-baseline | Current | Balanced starter | 2026-02-04 |

## Quick Start

Copy the content from `CURRENT.md` (or latest version) into Aqua Voice's custom instructions field.
