---
name: Triage Auto-Activation
trigger:
  - "complex"
  - "multi-domain"
  - "unclear"
  - "which specialist"
  - "route this"
alwaysApply: false
priority: 95
---

# Triage Auto-Activation

## Activation

Activate when request complexity exceeds threshold or routing is unclear.

## Triggers

- "complex request"
- "multi-domain"
- "unclear which specialist"
- "route this"
- "which agent should handle"

## Purpose

Classify intent and assign specialists for complex requests that the orchestrator cannot easily categorize.

## Output

Specialist assignment with confidence score.
