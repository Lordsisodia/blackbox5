---
name: Security Audit Auto-Activation
trigger:
  - "security check"
  - "vulnerability scan"
  - "OWASP"
  - "security audit"
  - "safe to merge"
  - "auth code"
  - "payment code"
alwaysApply: false
priority: 90
---

# Security Audit Auto-Activation

## Activation

Activate for security verification.

## Triggers

- "security check"
- "vulnerability scan"
- "OWASP"
- "security audit"
- "safe to merge"
- "auth code changes"
- "payment code changes"

## Purpose

Vulnerability scanning and OWASP compliance checking.

## Checks

- OWASP Top 10
- Secrets exposure
- Injection vulnerabilities
- Insecure dependencies

## Output

security_report.yaml
