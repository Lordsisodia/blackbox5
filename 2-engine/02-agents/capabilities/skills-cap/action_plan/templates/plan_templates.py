"""
Action Plan Templates for Common Workflows

Provides pre-built Action Plan templates for common development workflows.
Each template returns a dictionary of phases with tasks that can be loaded into
an ActionPlan.
"""

from typing import Dict, List, Any, Optional
from dataclasses import field

# Try to import models, handle both relative and absolute imports
try:
    from .models import (
        ActionPhase,
        ActionTask,
        ActionSubtask,
        TaskContext,
        Constraint,
        Assumption,
        ConstraintType
    )
except ImportError:
    from models import (
        ActionPhase,
        ActionTask,
        ActionSubtask,
        TaskContext,
        Constraint,
        Assumption,
        ConstraintType
    )


# ============================================================================
# TEMPLATE 1: Feature Development
# ============================================================================

def feature_development_template(feature_name: str, description: str) -> Dict[str, Any]:
    """
    Template for developing a new feature.

    Phases:
    1. Requirements Analysis
    2. Design
    3. Implementation
    4. Testing
    5. Documentation
    6. Deployment
    """
    return {
        "plan_name": f"Develop {feature_name}",
        "description": description,
        "phases": [
            {
                "name": "Requirements Analysis",
                "description": "Gather and document requirements for the feature",
                "order": 1,
                "exit_criteria": [
                    "Requirements documented",
                    "Stakeholders agree on scope",
                    "Edge cases identified"
                ],
                "tasks": [
                    {
                        "title": "Gather Requirements",
                        "description": "Interview stakeholders and document requirements",
                        "context_template": TaskContext(
                            objective=f"Document requirements for {feature_name}",
                            constraints=[
                                Constraint(
                                    text="Must align with product roadmap",
                                    type=ConstraintType.HARD,
                                    source="product"
                                ),
                                Constraint(
                                    text="Should consider technical debt",
                                    type=ConstraintType.SOFT,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Stakeholders are available for interviews",
                                    confidence="high",
                                    test="Schedule stakeholder meetings"
                                ),
                                Assumption(
                                    text="Requirements are stable",
                                    confidence="medium",
                                    test="Review historical requirement changes"
                                )
                            ],
                            resources=[
                                "Product requirements document",
                                "User stories",
                                "Competitive analysis"
                            ],
                            success_criteria=[
                                "All stakeholder requirements documented",
                                "Acceptance criteria defined",
                                "Edge cases identified"
                            ],
                            thinking_process=f"""First Principles for {feature_name} Requirements:

1. What problem are we ACTUALLY solving?
   → User pain point that {feature_name} addresses
   → Business value being created

2. What do we know to be TRUE?
   → Users have expressed need for this feature
   → Technical feasibility needs verification
   → Resource constraints exist

3. What are we assuming?
   → Requirements are stable (MEDIUM confidence)
   → Stakeholders agree on priorities (MEDIUM confidence)
   → Technical approach is viable (HIGH confidence - needs validation)

4. What MUST be included?
   → Core user value proposition
   → Essential functionality
   → Error handling
   → Performance requirements

5. What can we eliminate?
   → Nice-to-have features (move to backlog)
   → Edge cases that can be handled later
   → Unnecessary complexity
"""
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Define Acceptance Criteria",
                        "description": "Create clear, testable acceptance criteria",
                        "context_template": TaskContext(
                            objective="Define testable acceptance criteria",
                            constraints=[
                                Constraint(
                                    text="Criteria must be measurable",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="QA team can provide input",
                                    confidence="high",
                                    test="Consult with QA lead"
                                )
                            ],
                            resources=["Gherkin syntax guide", "Previous feature specs"],
                            success_criteria=[
                                "Each requirement has testable criteria",
                                "QA team approval obtained"
                            ],
                            thinking_process="Acceptance criteria must be specific, measurable, and testable to enable clear validation."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Design",
                "description": "Design the solution architecture and UI/UX",
                "order": 2,
                "dependencies": ["Requirements Analysis"],
                "exit_criteria": [
                    "Technical design approved",
                    "UI/UX mockups complete",
                    "API contracts defined"
                ],
                "tasks": [
                    {
                        "title": "Create Technical Design",
                        "description": "Design system architecture and data models",
                        "context_template": TaskContext(
                            objective="Design technical architecture for the feature",
                            constraints=[
                                Constraint(
                                    text="Must follow existing architectural patterns",
                                    type=ConstraintType.HARD,
                                    source="architecture"
                                ),
                                Constraint(
                                    text="Should be performant (<200ms response)",
                                    type=ConstraintType.SOFT,
                                    source="performance"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Existing infrastructure can support feature",
                                    confidence="high",
                                    test="Load testing"
                                )
                            ],
                            resources=[
                                "System architecture docs",
                                "Database schema",
                                "API design guidelines"
                            ],
                            success_criteria=[
                                "Architecture diagram created",
                                "Data models designed",
                                "API endpoints specified",
                                "Security review passed"
                            ],
                            thinking_process="""Technical Design First Principles:

1. What's the simplest solution that meets requirements?
2. How does this integrate with existing systems?
3. What are the failure modes and mitigations?
4. Is the design scalable for expected growth?
5. Are there security or privacy implications?
"""
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Design UI/UX",
                        "description": "Create user interface mockups and flows",
                        "context_template": TaskContext(
                            objective="Design intuitive user interface",
                            constraints=[
                                Constraint(
                                    text="Must follow design system guidelines",
                                    type=ConstraintType.HARD,
                                    source="design"
                                ),
                                Constraint(
                                    text="Should be accessible (WCAG 2.1 AA)",
                                    type=ConstraintType.SOFT,
                                    source="accessibility"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Design system components are available",
                                    confidence="high",
                                    test="Check component library"
                                )
                            ],
                            resources=[
                                "Design system documentation",
                                "User research",
                                "Accessibility guidelines"
                            ],
                            success_criteria=[
                                "Mockups for all screens created",
                                "User flows documented",
                                "Accessibility review passed"
                            ],
                            thinking_process="User experience should be intuitive, efficient, and accessible."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Implementation",
                "description": "Implement the feature according to design",
                "order": 3,
                "dependencies": ["Design"],
                "exit_criteria": [
                    "All code written and reviewed",
                    "Unit tests passing",
                    "Code coverage >= 80%"
                ],
                "tasks": [
                    {
                        "title": "Implement Backend",
                        "description": "Implement server-side logic and APIs",
                        "context_template": TaskContext(
                            objective="Implement backend functionality",
                            constraints=[
                                Constraint(
                                    text="Must follow code style guidelines",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                ),
                                Constraint(
                                    text="Should have comprehensive error handling",
                                    type=ConstraintType.HARD,
                                    source="reliability"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Required libraries are available",
                                    confidence="high",
                                    test="Check package registry"
                                )
                            ],
                            resources=[
                                "Technical design document",
                                "API specifications",
                                "Coding standards"
                            ],
                            success_criteria=[
                                "API endpoints implemented",
                                "Unit tests written",
                                "Code review approved",
                                "Documentation updated"
                            ],
                            thinking_process="""Backend Implementation Principles:

1. Write clean, readable code
2. Handle errors gracefully
3. Log appropriately for debugging
4. Validate all inputs
5. Use transactions for data consistency
"""
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Implement Frontend",
                        "description": "Implement user interface",
                        "context_template": TaskContext(
                            objective="Implement frontend components",
                            constraints=[
                                Constraint(
                                    text="Must match approved designs",
                                    type=ConstraintType.HARD,
                                    source="design"
                                ),
                                Constraint(
                                    text="Should be responsive",
                                    type=ConstraintType.SOFT,
                                    source="ux"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Design system components work as expected",
                                    confidence="medium",
                                    test="Component testing"
                                )
                            ],
                            resources=[
                                "UI mockups",
                                "Design system components",
                                "Frontend framework docs"
                            ],
                            success_criteria=[
                                "All screens implemented",
                                "Responsive design working",
                                "Browser compatibility verified"
                            ],
                            thinking_process="Frontend should be pixel-perfect, responsive, and performant."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Testing",
                "description": "Test the feature thoroughly",
                "order": 4,
                "dependencies": ["Implementation"],
                "exit_criteria": [
                    "All tests passing",
                    "No critical bugs",
                    "Performance benchmarks met"
                ],
                "tasks": [
                    {
                        "title": "Write Integration Tests",
                        "description": "Test integration points and workflows",
                        "context_template": TaskContext(
                            objective="Ensure components work together correctly",
                            constraints=[
                                Constraint(
                                    text="Must test all critical paths",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Test environment is available",
                                    confidence="high",
                                    test="Verify test environment setup"
                                )
                            ],
                            resources=["Test framework docs", "User stories"],
                            success_criteria=[
                                "All user journeys tested",
                                "Edge cases covered",
                                "Tests are reliable and fast"
                            ],
                            thinking_process="Integration tests should verify that components work together as expected."
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Perform QA Testing",
                        "description": "Manual QA testing and bug reporting",
                        "context_template": TaskContext(
                            objective="Find and fix bugs before release",
                            constraints=[
                                Constraint(
                                    text="Must test on all supported platforms",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="QA devices are available",
                                    confidence="high",
                                    test="Check device inventory"
                                )
                            ],
                            resources=["Test cases", "Bug tracking system"],
                            success_criteria=[
                                "All test cases executed",
                                "Critical bugs fixed",
                                "No regressions found"
                            ],
                            thinking_process="Thorough QA prevents production issues and user frustration."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Documentation",
                "description": "Document the feature for users and developers",
                "order": 5,
                "dependencies": ["Testing"],
                "exit_criteria": [
                    "User documentation complete",
                    "API documentation updated",
                    "Developer documentation current"
                ],
                "tasks": [
                    {
                        "title": "Write User Documentation",
                        "description": "Create user guides and help content",
                        "context_template": TaskContext(
                            objective="Help users understand and use the feature",
                            constraints=[
                                Constraint(
                                    text="Must be clear and non-technical",
                                    type=ConstraintType.HARD,
                                    source="ux"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Technical writer is available",
                                    confidence="medium",
                                    test="Check writer availability"
                                )
                            ],
                            resources=[
                                "Style guide",
                                "Documentation platform",
                                "User feedback"
                            ],
                            success_criteria=[
                                "User guide published",
                                "Help articles complete",
                                "Screenshots included"
                            ],
                            thinking_process="Good documentation reduces support burden and increases user adoption."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Deployment",
                "description": "Deploy the feature to production",
                "order": 6,
                "dependencies": ["Documentation"],
                "exit_criteria": [
                    "Feature deployed to production",
                    "Monitoring in place",
                    "Rollback plan tested"
                ],
                "tasks": [
                    {
                        "title": "Deploy to Staging",
                        "description": "Deploy to staging environment for final verification",
                        "context_template": TaskContext(
                            objective="Verify deployment process",
                            constraints=[
                                Constraint(
                                    text="Must follow deployment checklist",
                                    type=ConstraintType.HARD,
                                    source="devops"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Staging environment is stable",
                                    confidence="high",
                                    test="Run health check"
                                )
                            ],
                            resources=["Deployment playbook", "Runbook"],
                            success_criteria=[
                                "Deployment successful",
                                "Smoke tests pass",
                                "No errors in logs"
                            ],
                            thinking_process="Staging deployment is a dress rehearsal for production."
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Deploy to Production",
                        "description": "Deploy feature to production",
                        "context_template": TaskContext(
                            objective="Release feature to users",
                            constraints=[
                                Constraint(
                                    text="Must have rollback plan ready",
                                    type=ConstraintType.HARD,
                                    source="devops"
                                ),
                                Constraint(
                                    text="Should deploy during low-traffic hours",
                                    type=ConstraintType.SOFT,
                                    source="product"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="No critical issues will occur",
                                    confidence="high",
                                    test="Verify staging stability"
                                )
                            ],
                            resources=[
                                "Deployment automation",
                                "Monitoring dashboard",
                                "Runbook"
                            ],
                            success_criteria=[
                                "Deployment successful",
                                "Monitoring shows healthy state",
                                "No user-facing errors"
                            ],
                            thinking_process="Production deployment requires careful planning and monitoring."
                        ),
                        "dependencies": []
                    }
                ]
            }
        ]
    }


# ============================================================================
# TEMPLATE 2: Bug Investigation and Fix
# ============================================================================

def bug_investigation_template(bug_description: str, severity: str = "medium") -> Dict[str, Any]:
    """
    Template for investigating and fixing bugs.

    Phases:
    1. Investigation
    2. Root Cause Analysis
    3. Fix Development
    4. Testing
    5. Deployment
    """
    return {
        "plan_name": f"Fix Bug: {bug_description[:50]}...",
        "description": f"Investigate and fix bug: {bug_description}",
        "phases": [
            {
                "name": "Investigation",
                "description": "Investigate the bug and understand the issue",
                "order": 1,
                "exit_criteria": [
                    "Bug is reproducible",
                    "Affected components identified",
                    "Impact assessed"
                ],
                "tasks": [
                    {
                        "title": "Reproduce the Bug",
                        "description": "Create reliable reproduction steps",
                        "context_template": TaskContext(
                            objective="Reproduce the bug reliably",
                            constraints=[
                                Constraint(
                                    text="Must have clear reproduction steps",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Bug is reproducible in test environment",
                                    confidence="high",
                                    test="Attempt reproduction"
                                )
                            ],
                            resources=["Bug report", "Test environment access"],
                            success_criteria=[
                                "Bug reproduced consistently",
                                "Reproduction steps documented"
                            ],
                            thinking_process=f"""First Principles Bug Investigation:

1. What problem are we ACTUALLY seeing?
   → {bug_description}

2. What do we know to be TRUE?
   → Bug was reported (severity: {severity})
   → User impact exists
   → Expected behavior != actual behavior

3. What are we assuming?
   → Bug is reproducible (HIGH confidence - needs verification)
   → Single root cause exists (MEDIUM confidence)
   → Fix is straightforward (UNKNOWN - need investigation)

4. What MUST we determine?
   → Exact steps to reproduce
   → Scope of impact
   → Risk level of fix
"""
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Root Cause Analysis",
                "description": "Identify the root cause of the bug",
                "order": 2,
                "dependencies": ["Investigation"],
                "exit_criteria": [
                    "Root cause identified",
                    "Fix approach determined",
                    "Risk assessed"
                ],
                "tasks": [
                    {
                        "title": "Analyze Code and Logs",
                        "description": "Examine code and logs to find root cause",
                        "context_template": TaskContext(
                            objective="Find the root cause of the bug",
                            constraints=[
                                Constraint(
                                    text="Must understand the bug deeply before fixing",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Logs contain useful information",
                                    confidence="medium",
                                    test="Review log files"
                                )
                            ],
                            resources=[
                                "Source code",
                                "Application logs",
                                "Error tracking system"
                            ],
                            success_criteria=[
                                "Root cause identified",
                                "Code path to fix determined",
                                "Potential side effects identified"
                            ],
                            thinking_process="""Root Cause Analysis:

1. Trace the execution path
2. Identify where expected behavior diverges from actual
3. Understand why the bug occurs
4. Consider similar issues in codebase
5. Assess fix complexity and risk
"""
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Fix Development",
                "description": "Develop and implement the fix",
                "order": 3,
                "dependencies": ["Root Cause Analysis"],
                "exit_criteria": [
                    "Fix implemented",
                    "Code reviewed",
                    "Unit tests added"
                ],
                "tasks": [
                    {
                        "title": "Implement Fix",
                        "description": "Write code to fix the bug",
                        "context_template": TaskContext(
                            objective="Fix the bug without introducing new issues",
                            constraints=[
                                Constraint(
                                    text="Must not break existing functionality",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                ),
                                Constraint(
                                    text="Should be minimal change",
                                    type=ConstraintType.SOFT,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Simple fix will work",
                                    confidence="medium",
                                    test="Implement and test"
                                )
                            ],
                            resources=[
                                "Source code",
                                "Test suite",
                                "Coding standards"
                            ],
                            success_criteria=[
                                "Fix implemented",
                                "Unit tests added/updated",
                                "Edge cases considered"
                            ],
                            thinking_process="Bug fixes should be minimal, targeted, and well-tested."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Testing",
                "description": "Test the fix thoroughly",
                "order": 4,
                "dependencies": ["Fix Development"],
                "exit_criteria": [
                    "Fix verified in test environment",
                    "No regressions found",
                    "Original bug resolved"
                ],
                "tasks": [
                    {
                        "title": "Verify Fix",
                        "description": "Verify the bug is fixed",
                        "context_template": TaskContext(
                            objective="Confirm the bug is resolved",
                            constraints=[
                                Constraint(
                                    text="Must verify original reproduction steps",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Test environment matches production",
                                    confidence="medium",
                                    test="Environment comparison"
                                )
                            ],
                            resources=["Test environment", "Reproduction steps"],
                            success_criteria=[
                                "Bug no longer reproducible",
                                "Related functionality works",
                                "No new issues found"
                            ],
                            thinking_process="Verification must match the original bug report exactly."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Deployment",
                "description": "Deploy the fix to production",
                "order": 5,
                "dependencies": ["Testing"],
                "exit_criteria": [
                    "Fix deployed",
                    "Monitoring confirms no issues"
                ],
                "tasks": [
                    {
                        "title": "Deploy Fix",
                        "description": "Deploy the bug fix to production",
                        "context_template": TaskContext(
                            objective="Release the fix to users",
                            constraints=[
                                Constraint(
                                    text="Must have rollback plan",
                                    type=ConstraintType.HARD,
                                    source="devops"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Fix will not cause issues",
                                    confidence="high",
                                    test="Comprehensive testing"
                                )
                            ],
                            resources=["Deployment system", "Monitoring"],
                            success_criteria=[
                                "Deployment successful",
                                "No errors in logs",
                                "User complaints stopped"
                            ],
                            thinking_process="Bug fixes require careful monitoring after deployment."
                        ),
                        "dependencies": []
                    }
                ]
            }
        ]
    }


# ============================================================================
# TEMPLATE 3: Security Review
# ============================================================================

def security_review_template(scope: str) -> Dict[str, Any]:
    """
    Template for conducting a security review.

    Phases:
    1. Scope Definition
    2. Threat Modeling
    3. Vulnerability Assessment
    4. Remediation
    5. Verification
    """
    return {
        "plan_name": f"Security Review: {scope}",
        "description": f"Conduct comprehensive security review of {scope}",
        "phases": [
            {
                "name": "Scope Definition",
                "description": "Define what will be reviewed",
                "order": 1,
                "exit_criteria": [
                    "Scope documented",
                    "Assets identified",
                    "Review criteria established"
                ],
                "tasks": [
                    {
                        "title": "Define Review Scope",
                        "description": "Identify systems, data, and processes to review",
                        "context_template": TaskContext(
                            objective="Clearly define security review boundaries",
                            constraints=[
                                Constraint(
                                    text="Must cover all critical assets",
                                    type=ConstraintType.HARD,
                                    source="security"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="All systems are documented",
                                    confidence="medium",
                                    test="Check system inventory"
                                )
                            ],
                            resources=[
                                "System inventory",
                                "Data flow diagrams",
                                "Asset registry"
                            ],
                            success_criteria=[
                                "In-scope assets listed",
                                "Out-of-scope items documented",
                                "Review criteria defined"
                            ],
                            thinking_process="Clear scope prevents scope creep and ensures comprehensive coverage."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Threat Modeling",
                "description": "Identify potential threats and attack vectors",
                "order": 2,
                "dependencies": ["Scope Definition"],
                "exit_criteria": [
                    "Threats identified",
                    "Attack vectors documented",
                    "Risk ratings assigned"
                ],
                "tasks": [
                    {
                        "title": "Conduct Threat Modeling",
                        "description": "Use STRIDE or similar methodology",
                        "context_template": TaskContext(
                            objective="Identify all potential security threats",
                            constraints=[
                                Constraint(
                                    text="Must use structured methodology",
                                    type=ConstraintType.HARD,
                                    source="security"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Team has security expertise",
                                    confidence="medium",
                                    test="Review team credentials"
                                )
                            ],
                            resources=[
                                "OWASP resources",
                                "STRIDE methodology",
                                "Threat modeling tools"
                            ],
                            success_criteria=[
                                "Threat model documented",
                                "Risk ratings assigned",
                                "Mitigation strategies proposed"
                            ],
                            thinking_process="""Threat Modeling First Principles:

1. What are we protecting?
2. Who are the potential attackers?
3. What are the attack vectors?
4. What is the impact of each threat?
5. What mitigations are needed?
"""
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Vulnerability Assessment",
                "description": "Scan and test for vulnerabilities",
                "order": 3,
                "dependencies": ["Threat Modeling"],
                "exit_criteria": [
                    "Vulnerabilities identified",
                    "Severity ratings assigned",
                    "Recommendations documented"
                ],
                "tasks": [
                    {
                        "title": "Run Security Scans",
                        "description": "Execute automated and manual security tests",
                        "context_template": TaskContext(
                            objective="Find all security vulnerabilities",
                            constraints=[
                                Constraint(
                                    text="Must use multiple scanning tools",
                                    type=ConstraintType.HARD,
                                    source="security"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Scanning tools are up to date",
                                    confidence="high",
                                    test="Check tool versions"
                                )
                            ],
                            resources=[
                                "SAST/DAST tools",
                                "Dependency scanners",
                                "Manual testing procedures"
                            ],
                            success_criteria=[
                                "All scans completed",
                                "False positives filtered",
                                "Vulnerabilities categorized"
                            ],
                            thinking_process="Comprehensive scanning finds issues before attackers do."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Remediation",
                "description": "Fix identified vulnerabilities",
                "order": 4,
                "dependencies": ["Vulnerability Assessment"],
                "exit_criteria": [
                    "Critical vulnerabilities fixed",
                    "High-priority issues addressed",
                    "Lower-priority items backlogged"
                ],
                "tasks": [
                    {
                        "title": "Fix Critical Vulnerabilities",
                        "description": "Address all critical and high-severity issues",
                        "context_template": TaskContext(
                            objective="Eliminate critical security risks",
                            constraints=[
                                Constraint(
                                    text="Must fix all critical vulnerabilities",
                                    type=ConstraintType.HARD,
                                    source="security"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Fixes won't break functionality",
                                    confidence="medium",
                                    test="Regression testing"
                                )
                            ],
                            resources=["Development team", "Testing environment"],
                            success_criteria=[
                                "Critical issues resolved",
                                "Tests pass",
                                "No regressions"
                            ],
                            thinking_process="Security fixes must be implemented carefully to avoid introducing new issues."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Verification",
                "description": "Verify fixes and document findings",
                "order": 5,
                "dependencies": ["Remediation"],
                "exit_criteria": [
                    "All fixes verified",
                    "Security report complete",
                    "Recommendations for future"
                ],
                "tasks": [
                    {
                        "title": "Verify Remediation",
                        "description": "Confirm all vulnerabilities are fixed",
                        "context_template": TaskContext(
                            objective="Ensure security issues are resolved",
                            constraints=[
                                Constraint(
                                    text="Must re-scan to verify fixes",
                                    type=ConstraintType.HARD,
                                    source="security"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Fixes are effective",
                                    confidence="high",
                                    test="Re-scan"
                                )
                            ],
                            resources=["Scanning tools", "Test environment"],
                            success_criteria=[
                                "No critical/high vulnerabilities remain",
                                "Re-scan confirms fixes",
                                "Documentation complete"
                            ],
                            thinking_process="Verification ensures the remediation was effective."
                        ),
                        "dependencies": []
                    }
                ]
            }
        ]
    }


# ============================================================================
# TEMPLATE 4: Performance Optimization
# ============================================================================

def performance_optimization_template(target: str, goal: str) -> Dict[str, Any]:
    """
    Template for performance optimization work.

    Args:
        target: What is being optimized (API, database, frontend, etc.)
        goal: Performance goal (e.g., "reduce API response time to <100ms")
    """
    return {
        "plan_name": f"Optimize {target} Performance",
        "description": f"Performance optimization: {goal}",
        "phases": [
            {
                "name": "Baseline Measurement",
                "description": "Establish current performance baseline",
                "order": 1,
                "exit_criteria": [
                    "Baseline metrics established",
                    "Bottlenecks identified",
                    "Optimization targets set"
                ],
                "tasks": [
                    {
                        "title": "Measure Current Performance",
                        "description": "Establish comprehensive baseline metrics",
                        "context_template": TaskContext(
                            objective=f"Measure current {target} performance",
                            constraints=[
                                Constraint(
                                    text="Must measure under realistic load",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Production-like environment is available",
                                    confidence="high",
                                    test="Verify test environment"
                                )
                            ],
                            resources=[
                                "Profiling tools",
                                "Load testing framework",
                                "Monitoring data"
                            ],
                            success_criteria=[
                                "Baseline metrics documented",
                                "Performance profile created",
                                "Primary bottlenecks identified"
                            ],
                            thinking_process=f"""Performance Optimization First Principles:

1. What is the ACTUAL problem?
   → {target} is not meeting performance goal: {goal}

2. What do we know to be TRUE?
   → Current performance is unacceptable
   → Improvement is needed
   → Optimization has a cost

3. What are we assuming?
   → Bottlenecks are identifiable (HIGH confidence)
   → Optimizations won't break functionality (MEDIUM confidence - needs testing)
   → Goal is achievable (UNKNOWN - needs validation)

4. What MUST we measure?
   → Response times
   → Throughput
   → Resource utilization
   → User experience impact

5. Optimization strategy:
   → Measure first
   → Identify biggest bottleneck
   → Optimize
   → Verify improvement
   → Repeat
"""
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Bottleneck Analysis",
                "description": "Identify and prioritize optimization opportunities",
                "order": 2,
                "dependencies": ["Baseline Measurement"],
                "exit_criteria": [
                    "Bottlenecks ranked",
                    "Quick wins identified",
                    "Complex optimizations planned"
                ],
                "tasks": [
                    {
                        "title": "Profile and Analyze",
                        "description": "Deep dive into performance bottlenecks",
                        "context_template": TaskContext(
                            objective="Find the root causes of performance issues",
                            constraints=[
                                Constraint(
                                    text="Must use data-driven approach",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Profiling tools will reveal issues",
                                    confidence="high",
                                    test="Run profiler"
                                )
                            ],
                            resources=["Profilers", "APM tools", "Code analysis"],
                            success_criteria=[
                                "Top bottlenecks identified",
                                "Optimization impact estimated",
                                "Priority list created"
                            ],
                            thinking_process="Focus on optimizations with the highest impact first."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Implementation",
                "description": "Implement performance optimizations",
                "order": 3,
                "dependencies": ["Bottleneck Analysis"],
                "exit_criteria": [
                    "Optimizations implemented",
                    "Tests pass",
                    "No regressions"
                ],
                "tasks": [
                    {
                        "title": "Implement Quick Wins",
                        "description": "Implement high-impact, low-risk optimizations first",
                        "context_template": TaskContext(
                            objective="Achieve quick performance improvements",
                            constraints=[
                                Constraint(
                                    text="Must not change behavior",
                                    type=ConstraintType.HARD,
                                    source="qa"
                                ),
                                Constraint(
                                    text="Should be simple changes",
                                    type=ConstraintType.SOFT,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Quick wins are available",
                                    confidence="high",
                                    test="Review analysis"
                                )
                            ],
                            resources=["Codebase", "Test suite"],
                            success_criteria=[
                                "Quick wins implemented",
                                "Performance improved",
                                "No behavior changes"
                            ],
                            thinking_process="Quick wins build momentum and provide immediate value."
                        ),
                        "dependencies": []
                    },
                    {
                        "title": "Implement Complex Optimizations",
                        "description": "Implement more significant optimizations",
                        "context_template": TaskContext(
                            objective="Achieve performance goals through deeper changes",
                            constraints=[
                                Constraint(
                                    text="Must maintain correctness",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Complex optimizations are worth the effort",
                                    confidence="medium",
                                    test="Cost-benefit analysis"
                                )
                            ],
                            resources=["Development team", "Test environment"],
                            success_criteria=[
                                "Complex optimizations implemented",
                                "Goal achieved or approached",
                                "Comprehensive testing complete"
                            ],
                            thinking_process="Complex optimizations require careful testing and validation."
                        ),
                        "dependencies": []
                    }
                ]
            },
            {
                "name": "Validation",
                "description": "Verify performance improvements",
                "order": 4,
                "dependencies": ["Implementation"],
                "exit_criteria": [
                    "Goals achieved or documented",
                    "No regressions",
                    "Monitoring in place"
                ],
                "tasks": [
                    {
                        "title": "Measure Performance Improvements",
                        "description": "Compare against baseline",
                        "context_template": TaskContext(
                            objective="Verify performance goals are met",
                            constraints=[
                                Constraint(
                                    text="Must use same measurement as baseline",
                                    type=ConstraintType.HARD,
                                    source="engineering"
                                )
                            ],
                            assumptions=[
                                Assumption(
                                    text="Improvements are consistent",
                                    confidence="high",
                                    test="Multiple runs"
                                )
                            ],
                            resources=["Profiling tools", "Load testing framework"],
                            success_criteria=[
                                "Performance improved",
                                "Goal achieved or gap documented",
                                "No regressions"
                            ],
                            thinking_process="Validation confirms the optimization effort was successful."
                        ),
                        "dependencies": []
                    }
                ]
            }
        ]
    }


# ============================================================================
# Helper Functions
# ============================================================================

def list_templates() -> List[str]:
    """Return list of available template names."""
    return [
        "feature_development_template",
        "bug_investigation_template",
        "security_review_template",
        "performance_optimization_template"
    ]


def get_template(name: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get a template by name.

    Args:
        name: Template name
        **kwargs: Arguments to pass to template function

    Returns:
        Template dictionary or None if not found
    """
    templates = {
        "feature_development": feature_development_template,
        "bug_investigation": bug_investigation_template,
        "security_review": security_review_template,
        "performance_optimization": performance_optimization_template
    }

    template_func = templates.get(name)
    if template_func:
        return template_func(**kwargs)
    return None
