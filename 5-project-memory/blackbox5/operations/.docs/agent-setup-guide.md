# Agent Version Setup Guide

**Version:** 1.0.0
**Purpose:** Step-by-step guide for creating new agent versions
**Source:** IMP-1769903007 - Create Agent Version Setup Checklist

---

## Overview

Creating a new agent version requires more than just updating the main prompt file. This guide ensures you don't miss critical supporting infrastructure that makes the agent function properly in the RALF system.

### Why This Matters

Historical issues from incomplete agent setups:
- Agent-2.4 AGENT.md created but `metrics.jsonl` missing (dashboard showed "no metrics")
- Templates not copied from previous versions (runtime errors)
- Version references not updated (user confusion)
- Dashboard scripts broken (syntax errors)

---

## Quick Start

### Automated Setup (Recommended)

Use the setup script to automate the checklist:

```bash
# Create new agent version
2-engine/.autonomous/scripts/create-agent-version.sh v2.5 "RALF-Analyzer"

# Or with custom name
2-engine/.autonomous/scripts/create-agent-version.sh v2.5 "custom-agent-name"
```

### Manual Setup

If you prefer manual control, follow the [Complete Checklist](#complete-checklist) below.

---

## Complete Checklist

### Phase 1: Core Components (Required)

#### 1.1 Create Agent Definition

```bash
# Copy from previous version as starting point
cp 2-engine/.autonomous/prompts/ralf-executor.md \
   2-engine/.autonomous/prompts/ralf-{new-name}.md
```

**Update in the new file:**
- Version number in header
- Role/purpose description
- Any version-specific rules

**Validation:**
```bash
head -20 2-engine/.autonomous/prompts/ralf-{new-name}.md
```

#### 1.2 Create Agent Configuration

```bash
mkdir -p 2-engine/.autonomous/agents/{agent-name}
cat > 2-engine/.autonomous/agents/{agent-name}/config.yaml << 'EOF'
agent:
  name: "{agent-name}"
  version: "X.Y.Z"
  type: "executor|planner|analyzer"

capabilities:
  - capability1
  - capability2

settings:
  max_context: 80000
  timeout_seconds: 300
EOF
```

---

### Phase 2: Supporting Infrastructure (Required)

#### 2.1 Initialize Metrics Tracking

```bash
# Create metrics file with header
cat > ralf-metrics.jsonl << EOF
{"timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", "type": "metadata", "version": "X.Y.Z", "agent": "{agent-name}"}
EOF
```

**Why this matters:** Without this file, the dashboard will show "no metrics yet" indefinitely.

#### 2.2 Create Templates Directory

```bash
mkdir -p 2-engine/.autonomous/prompts/context/{agent-name}
mkdir -p 2-engine/.autonomous/prompts/exit/{agent-name}
```

**Copy from previous version:**
```bash
# Inherit templates - don't recreate from scratch
cp -r 2-engine/.autonomous/prompts/context/ralf-executor/* \
   2-engine/.autonomous/prompts/context/{agent-name}/
```

---

### Phase 3: Version-Specific Components

#### 3.1 Create Version Directory

```bash
mkdir -p 2-engine/.autonomous/prompt-progression/versions/v{X.Y}
mkdir -p 2-engine/.autonomous/prompt-progression/versions/v{X.Y}/templates
```

#### 3.2 Copy Templates from Previous Version

```bash
PREV_VERSION="2.4"  # Update as needed
NEW_VERSION="2.5"

cp -r 2-engine/.autonomous/prompt-progression/versions/v${PREV_VERSION}/templates/* \
   2-engine/.autonomous/prompt-progression/versions/v${NEW_VERSION}/templates/
```

#### 3.3 Create Version README

```bash
cat > 2-engine/.autonomous/prompt-progression/versions/v{X.Y}/README.md << 'EOF'
# Agent Version X.Y

**Release Date:** YYYY-MM-DD
**Previous Version:** X.(Y-1)

## What's New

- Feature 1
- Feature 2
- Feature 3

## Breaking Changes

None / List any breaking changes

## Migration Guide

See docs/migrations/v{X.Y}-migration.md
EOF
```

---

### Phase 4: Integration Points

#### 4.1 Update Entry Point

```bash
# Update bin/ralf.md (or equivalent entry point)
sed -i.bak 's/Agent-2.4/Agent-2.5/g' bin/ralf.md
```

**Verify the change:**
```bash
grep -n "Agent-" bin/ralf.md | head -5
```

#### 4.2 Check Dashboard Compatibility

```bash
# Test dashboard still works
./bin/ralf-dashboard

# Look for:
# - No syntax errors
# - Metrics display correctly
# - Version shows correctly
```

#### 4.3 Update Scripts

Check for hardcoded version references:

```bash
grep -r "Agent-2.4" 2-engine/.autonomous/scripts/ || echo "No hardcoded versions found"
```

---

### Phase 5: Documentation

#### 5.1 Update Changelog

```bash
cat >> CHANGELOG.md << 'EOF'

## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature

### Changed
- Modified behavior

### Fixed
- Bug fix
EOF
```

#### 5.2 Create Migration Guide (if needed)

```bash
mkdir -p docs/migrations
cat > docs/migrations/v{X.Y}-migration.md << 'EOF'
# Migration Guide: v{X.(Y-1)} to v{X.Y}

## Overview

This guide helps you migrate from version X.(Y-1) to X.Y.

## Steps

1. Step one
2. Step two
3. Step three

## Breaking Changes

- Change 1: How to handle it
- Change 2: How to handle it
EOF
```

---

## Validation

### Pre-Deployment Checklist

Run these commands before deploying:

```bash
# 1. Validate all YAML files
find 2-engine/.autonomous -name "*.yaml" -exec yamllint {} \;

# 2. Check shell scripts for syntax errors
find 2-engine/.autonomous -name "*.sh" -exec shellcheck {} \;

# 3. Verify version consistency
grep -r "version.*2\.[45]" 2-engine/.autonomous/prompts/ | grep -v ".md.bak"

# 4. Check metrics file exists
ls -la ralf-metrics.jsonl

# 5. Verify templates are inherited
ls -la 2-engine/.autonomous/prompt-progression/versions/v{X.Y}/templates/
```

### Post-Deployment Checklist

After deployment, verify:

```bash
# 1. Agent initializes without errors
ralf --version

# 2. Metrics file is writable
echo '{"test": true}' >> ralf-metrics.jsonl

# 3. Dashboard displays correctly
./bin/ralf-dashboard | head -20

# 4. First run completes successfully
# (Run the agent and check for errors)
```

---

## Common Issues

### Issue: Dashboard Shows "No Metrics Yet"

**Cause:** `ralf-metrics.jsonl` doesn't exist or is empty

**Fix:**
```bash
echo '{"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "type": "metadata", "version": "X.Y.Z"}' > ralf-metrics.jsonl
```

### Issue: Templates Missing Errors

**Cause:** Templates not copied from previous version

**Fix:**
```bash
cp -r 2-engine/.autonomous/prompt-progression/versions/v{PREV}/templates \
   2-engine/.autonomous/prompt-progression/versions/v{NEW}/
```

### Issue: Wrong Version Displayed

**Cause:** Entry point not updated

**Fix:**
```bash
sed -i 's/Agent-X.Y/Agent-X.Z/g' bin/ralf.md
```

### Issue: Script Syntax Errors

**Cause:** Shell syntax errors (e.g., missing `|` in pipes)

**Fix:**
```bash
# Check with shellcheck
shellcheck bin/ralf-dashboard

# Common fix: Add missing pipe
sed -i 's/echo "$line" jq/echo "$line" | jq/g' bin/ralf-dashboard
```

---

## Best Practices

### 1. Always Inherit Templates

Never recreate templates from scratch. Copy from the previous version and modify:

```bash
cp -r versions/v{PREV}/templates versions/v{NEW}/
```

### 2. Version Numbers

Use semantic versioning:
- **X.Y.Z** format
- Increment Y for new features
- Increment Z for bug fixes
- Increment X for breaking changes

### 3. Documentation First

Update documentation as part of setup, not after:

```bash
# Good: Documentation in same commit
git add docs/ 2-engine/ bin/
git commit -m "Add Agent-X.Y with complete documentation"

# Bad: Documentation in separate commit
git add 2-engine/ bin/
git commit -m "Add Agent-X.Y"
# ... later ...
git add docs/
git commit -m "Add documentation"
```

### 4. Test Before Committing

Always test the agent before finalizing:

```bash
# Run validation
./bin/ralf --validate

# Test first run
./bin/ralf run --dry-run
```

---

## Reference

### File Locations

| Component | Location |
|-----------|----------|
| Agent Definition | `2-engine/.autonomous/prompts/{name}.md` |
| Agent Config | `2-engine/.autonomous/agents/{name}/config.yaml` |
| Metrics | `ralf-metrics.jsonl` |
| Templates | `2-engine/.autonomous/prompt-progression/versions/v{X.Y}/templates/` |
| Entry Point | `bin/ralf.md` |
| Dashboard | `bin/ralf-dashboard` |

### Related Resources

- [Agent Setup Checklist](../agent-setup-checklist.yaml) - YAML version of this checklist
- [Create Agent Version Script](../../../2-engine/.autonomous/scripts/create-agent-version.sh) - Automated setup
- [Improvement Backlog](../improvement-backlog.yaml) - Source improvement task

---

## History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial version based on IMP-1769903007 |
