#!/bin/bash
# Initialize Luminell Project in BB5 Memory
# Usage: ./init-luminell-project.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_DIR="$BB5_DIR/5-project-memory/luminell"

echo "🚀 Initializing Luminell Project in BB5 Memory..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$PROJECT_DIR"/{.autonomous/{tasks/{active,completed},memory/data,agents/communications},runs,context}

# Create goals.yaml
echo "🎯 Creating goals.yaml..."
cat > "$PROJECT_DIR/goals.yaml" << 'EOF'
project: Luminell
organization: SISO Internal
description: AI-powered business intelligence platform for enterprise clients
status: active
created: 2026-02-09

# Why this project exists
core_goals:
  - id: LG-001
    title: Deliver MVP
    description: Build and deploy minimum viable product
    status: active
    priority: critical
    target_date: 2026-03-31

  - id: LG-002
    title: Client Acquisition
    description: Acquire first 3 paying customers
    status: pending
    priority: critical
    target_date: 2026-04-30

  - id: LG-003
    title: Platform Stability
    description: Achieve 99.9% uptime
    status: pending
    priority: high
    target_date: 2026-06-30

# How we get better
improvement_goals:
  - id: LI-001
    title: Query Performance
    description: Sub-second query response times
    status: pending
    priority: high

  - id: LI-002
    title: Developer Experience
    description: Streamlined deployment and debugging
    status: pending
    priority: medium

  - id: LI-003
    title: Documentation
    description: Complete API and user documentation
    status: pending
    priority: medium

# What we need to know
data_goals:
  - id: LD-001
    title: User Analytics
    description: Track user behavior and feature usage
    status: pending
    priority: high

  - id: LD-002
    title: Performance Metrics
    description: Monitor system performance
    status: pending
    priority: high

review_schedule:
  every_5_runs: true
  monthly: true
  quarterly: true
EOF

# Create CLAUDE.md
echo "📝 Creating CLAUDE.md..."
cat > "$PROJECT_DIR/CLAUDE.md" << 'EOF'
# Luminell Project - Claude Configuration

## Project Overview
Luminell is an AI-powered business intelligence platform being developed for SISO Internal.

## Key Information
- **Status:** Active development
- **Priority:** Critical
- **Team:** SISO Internal
- **Tech Stack:** See context/tech-stack.md

## Quick Links
- Goals: `./goals.yaml`
- Architecture: `./context/architecture.md`
- Requirements: `./context/requirements.md`
- Stakeholders: `./context/stakeholders.md`

## BB5 Integration
This project uses BB5 infrastructure:
- Agent teams for complex tasks
- Memory system for knowledge retention
- Task tracking in `.autonomous/tasks/`
- Run documentation in `runs/`

## When Working on Luminell
1. Check `goals.yaml` for current priorities
2. Read relevant context files
3. Use Luminell-specific agents:
   - luminell-context-collector
   - luminell-architect
   - luminell-developer
4. Document in project memory (THOUGHTS.md, DECISIONS.md, LEARNINGS.md)

## Stop Conditions
- Requirements unclear → Ask stakeholder
- Scope creep → Check against goals
- Blocked → Escalate to project lead
EOF

# Create context files
echo "📋 Creating context files..."

cat > "$PROJECT_DIR/context/stakeholders.md" << 'EOF'
# Luminell Stakeholders

## Internal Team
| Name | Role | Responsibility | Contact |
|------|------|----------------|---------|
| TBD | Product Owner | Requirements, prioritization | - |
| TBD | Tech Lead | Architecture, technical decisions | - |
| TBD | Developer | Implementation | - |

## Clients
| Client | Status | Contact | Notes |
|--------|--------|---------|-------|
| - | - | - | - |

## Decision Makers
- Product Owner: Feature priorities
- Tech Lead: Architecture decisions
- BB5 Agent Teams: Implementation
EOF

cat > "$PROJECT_DIR/context/tech-stack.md" << 'EOF'
# Luminell Tech Stack

## Frontend
- Framework: TBD
- UI Library: TBD
- State Management: TBD

## Backend
- Runtime: TBD
- API: TBD
- Database: TBD

## Infrastructure
- Hosting: TBD
- CI/CD: TBD
- Monitoring: TBD

## AI/ML
- Model: TBD
- Training Pipeline: TBD
- Inference: TBD

## Integrations
- Authentication: TBD
- Payment: TBD
- Analytics: TBD
EOF

cat > "$PROJECT_DIR/context/architecture.md" << 'EOF'
# Luminell Architecture

## System Overview
[High-level description of the Luminell platform]

## Components
| Component | Purpose | Technology | Status |
|-----------|---------|------------|--------|
| Web App | User interface | TBD | Planned |
| API Server | Backend services | TBD | Planned |
| Database | Data storage | TBD | Planned |
| AI Engine | Intelligence layer | TBD | Planned |

## Data Flow
[Diagram or description of data flow]

## API Design
[Key API endpoints and specifications]

## Security
[Authentication, authorization, data protection]
EOF

cat > "$PROJECT_DIR/context/requirements.md" << 'EOF'
# Luminell Requirements

## MVP Features
- [ ] User authentication
- [ ] Dashboard
- [ ] Data visualization
- [ ] Report generation
- [ ] AI insights

## Future Features
- [ ] Advanced analytics
- [ ] Custom integrations
- [ ] Mobile app
- [ ] White-label option

## Non-Functional Requirements
- Performance: Sub-second response
- Scalability: 1000+ concurrent users
- Security: SOC 2 compliance
- Reliability: 99.9% uptime
EOF

# Create initial memory files
echo "🧠 Creating memory files..."
touch "$PROJECT_DIR/THOUGHTS.md"
touch "$PROJECT_DIR/DECISIONS.md"
touch "$PROJECT_DIR/LEARNINGS.md"
touch "$PROJECT_DIR/RESULTS.md"

# Create agent team activation
cat > "$PROJECT_DIR/.autonomous/agents/communications/agent-state.yaml" << EOF
project: luminell
status: initialized
initialized_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
available_agents:
  - luminell-context-collector
  - luminell-architect
  - luminell-developer
  - luminell-scribe
EOF

echo ""
echo "✅ Luminell Project Initialized!"
echo ""
echo "Location: $PROJECT_DIR"
echo ""
echo "Next steps:"
echo "1. Populate context files with actual project details"
echo "2. Update stakeholders, tech stack, architecture"
echo "3. Set specific goals and target dates"
echo "4. Create first tasks in .autonomous/tasks/active/"
echo "5. Start work - BB5 agent teams will auto-activate"
echo ""
echo "To activate:"
echo "  cd $BB5_DIR"
echo "  claude"
echo "  # Then: 'Work on Luminell project'"
