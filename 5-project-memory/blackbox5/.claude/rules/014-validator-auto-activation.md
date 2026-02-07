---
name: Validator Auto-Activation
trigger:
  - "validate"
  - "verify"
  - "check"
  - "quality gate"
  - "pre-merge"
  - "review this"
alwaysApply: false
priority: 85
---

# Validator Auto-Activation

## Activation

Activate for quality verification.

## Triggers

- "validate"
- "verify"
- "check"
- "quality gate"
- "pre-merge check"
- "review this"

## Purpose

3-level verification (existence/substantive/wired). Quality gate before merge.

## Levels

1. **Existence** - Files exist?
2. **Substantive** - Content is meaningful?
3. **Wired** - Everything connects?

## Output

validator_report.yaml with score and grade
