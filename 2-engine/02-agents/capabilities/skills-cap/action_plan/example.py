"""
Action Plan System - Example Usage

Demonstrates how to use the Action Plan system for complex task execution.
"""

from datetime import datetime
from action_plan import (
    create_action_plan,
    TaskContext,
    Constraint,
    Assumption,
    ConstraintType
)


def example_basic_action_plan():
    """
    Basic example: Create a simple action plan with phases and tasks.
    """
    print("=" * 80)
    print("Example 1: Basic Action Plan")
    print("=" * 80)

    # Create an action plan
    plan = create_action_plan(
        name="Build User Authentication System",
        description="Implement secure user authentication with JWT tokens",
        apply_first_principles=True
    )

    # Add Phase 1: Analysis
    phase1 = plan.add_phase(
        name="Requirements Analysis",
        description="Analyze requirements and constraints for authentication system",
        exit_criteria=[
            "All requirements documented",
            "Security constraints identified",
            "Technical approach decided"
        ]
    )

    # Create task in Phase 1
    task1_1 = plan.create_task(
        phase_id=phase1.id,
        title="Identify Security Requirements",
        description="Document all security requirements for the authentication system",
        context_template=TaskContext(
            objective="Identify and document security requirements",
            constraints=[
                Constraint(
                    text="Must use industry-standard encryption",
                    type=ConstraintType.HARD,
                    source="security_policy"
                ),
                Constraint(
                    text="Should support OAuth 2.0",
                    type=ConstraintType.SOFT,
                    source="product_requirement"
                )
            ],
            assumptions=[
                Assumption(
                    text="JWT tokens are appropriate for this use case",
                    confidence="high",
                    test="Research JWT best practices"
                ),
                Assumption(
                    text="Users will access from web and mobile",
                    confidence="medium",
                    test="Verify with product team"
                )
            ],
            resources=[
                "OWASP Authentication Cheat Sheet",
                "JWT specification (RFC 7519)",
                "Company security guidelines"
            ],
            success_criteria=[
                "All security requirements documented",
                "Threat model completed",
                "Compliance checklist completed"
            ],
            thinking_process="""
            First Principles Analysis:
            1. What problem are we ACTUALLY solving?
               - Need to verify user identity and protect resources

            2. What do we know to be TRUE?
               - Security is critical for authentication
               - Industry standards exist for a reason
               - Compliance requirements must be met

            3. What are we assuming?
               - JWT is the right approach (need to validate)
               - OAuth 2.0 is desirable but optional

            4. What MUST be included?
               - Secure password storage
               - Secure token generation
               - Protection against common attacks

            5. What can we eliminate?
               - Custom crypto implementations (use proven libraries)
               - Non-standard authentication methods
            """
        )
    )

    # Add subtasks
    plan.add_subtask(
        task_id=task1_1.id,
        title="Review OWASP guidelines",
        description="Review OWASP Authentication Cheat Sheet",
        thinking_process="Industry-standard security guidelines must be followed",
        order=1
    )

    plan.add_subtask(
        task_id=task1_1.id,
        title="Document threat model",
        description="Create threat model for authentication system",
        thinking_process="Understanding threats is fundamental to security",
        order=2
    )

    # Add Phase 2: Implementation
    phase2 = plan.add_phase(
        name="Implementation",
        description="Implement the authentication system",
        dependencies=[phase1.id],  # Depends on analysis phase
        exit_criteria=[
            "All authentication endpoints implemented",
            "Security tests passing",
            "Documentation complete"
        ]
    )

    # Create task in Phase 2
    task2_1 = plan.create_task(
        phase_id=phase2.id,
        title="Implement Login Endpoint",
        description="Create secure login endpoint with JWT token generation",
        context_template=TaskContext(
            objective="Implement login endpoint",
            constraints=[
                Constraint(
                    text="Must use bcrypt for password hashing",
                    type=ConstraintType.HARD,
                    source="security_policy"
                ),
                Constraint(
                    text="Must implement rate limiting",
                    type=ConstraintType.HARD,
                    source="security_policy"
                )
            ],
            assumptions=[
                Assumption(
                    text="User repository exists",
                    confidence="high",
                    test="Verify User model is implemented"
                )
            ],
            resources=[
                "bcrypt library documentation",
                "JWT library documentation",
                "API design guidelines"
            ],
            success_criteria=[
                "Login endpoint accepts username/password",
                "Passwords hashed with bcrypt",
                "JWT token returned on successful login",
                "Rate limiting implemented",
                "Unit tests passing"
            ],
            thinking_process="""
            First Principles Analysis:
            1. What problem are we ACTUALLY solving?
               - Verify user credentials and issue authentication token

            2. What do we know to be TRUE?
               - Passwords must never be stored in plain text
               - Bcrypt is proven for password hashing
               - Rate limiting prevents brute force attacks

            3. What MUST be included?
               - Secure password verification
               - JWT token generation
               - Rate limiting
               - Error handling without information leakage

            4. What can we eliminate?
               - Custom hash functions (use bcrypt)
               - Detailed error messages (help attackers)
            """
        )
    )

    # Print the plan
    print("\n" + plan.generate_report())

    # Get progress
    progress = plan.get_progress()
    print(f"\nProgress: {progress['task_progress']} tasks complete ({progress['percent_complete']:.1f}%)")

    return plan


def example_execution_simulation():
    """
    Example 2: Simulate executing tasks in an action plan.
    """
    print("\n" + "=" * 80)
    print("Example 2: Task Execution Simulation")
    print("=" * 80)

    from action_plan import TaskResult

    # Create a plan
    plan = create_action_plan(
        name="Fix Critical Bug",
        description="Fix authentication bypass vulnerability",
        apply_first_principles=True
    )

    # Add phases and tasks
    phase1 = plan.add_phase(
        name="Investigation",
        description="Investigate the vulnerability",
        exit_criteria=["Root cause identified"]
    )

    task1 = plan.create_task(
        phase_id=phase1.id,
        title="Reproduce the Bug",
        description="Create reproduction case for the vulnerability",
        context_template=TaskContext(
            objective="Reproduce the authentication bypass",
            constraints=[],
            assumptions=[],
            resources=["Bug report", "Test environment"],
            success_criteria=["Bug reproduced", "Test case created"]
        )
    )

    # Simulate getting next task
    next_task = plan.get_next_task()
    if next_task:
        print(f"\nNext task to execute: {next_task.title}")
        print(f"Description: {next_task.description}")

        # Mark as started
        plan.start_task(next_task)

        # Simulate completion
        result = TaskResult(
            task_id=next_task.id,
            success=True,
            output="Bug successfully reproduced. Created test case in tests/test_auth_bypass.py",
            artifacts={
                'test_case': 'tests/test_auth_bypass.py',
                'steps_to_reproduce': 'bug_report.md'
            },
            thinking_steps=[
                "Analyzed bug report",
                "Set up test environment",
                "Reproduced vulnerability",
                "Documented reproduction steps"
            ],
            duration=1800.0  # 30 minutes
        )

        plan.complete_task(next_task.id, result)
        print(f"✓ Task completed successfully")

        # Save checkpoint
        checkpoint_id = plan.create_checkpoint()
        print(f"✓ Checkpoint saved: {checkpoint_id}")

    # Show progress
    progress = plan.get_progress()
    print(f"\nCurrent progress: {progress['task_progress']}")

    return plan


def example_checkpoint_recovery():
    """
    Example 3: Demonstrate checkpoint recovery.
    """
    print("\n" + "=" * 80)
    print("Example 3: Checkpoint Recovery")
    print("=" * 80)

    # Create a plan and execute some tasks
    plan = create_action_plan(
        name="Database Migration",
        description="Migrate database to new schema",
        apply_first_principles=True
    )

    phase1 = plan.add_phase(
        name="Planning",
        description="Plan the migration",
        exit_criteria=["Migration plan approved"]
    )

    task1 = plan.create_task(
        phase_id=phase1.id,
        title="Create Migration Plan",
        description="Document the migration strategy",
        context_template=TaskContext(
            objective="Create comprehensive migration plan",
            constraints=[
                Constraint(
                    text="Zero downtime required",
                    type=ConstraintType.HARD,
                    source="sla"
                )
            ],
            assumptions=[
                Assumption(
                    text="Can use blue-green deployment",
                    confidence="high",
                    test="Verify infrastructure supports it"
                )
            ],
            resources=["Database documentation", "Migration tools"],
            success_criteria=["Migration plan documented", "Rollback plan documented"]
        )
    )

    # Simulate execution
    from action_plan import TaskResult

    next_task = plan.get_next_task()
    plan.start_task(next_task)
    plan.complete_task(next_task.id, TaskResult(
        task_id=next_task.id,
        success=True,
        output="Migration plan created"
    ))

    # Create checkpoint
    checkpoint_id = plan.create_checkpoint()
    print(f"Checkpoint created: {checkpoint_id}")

    # Simulate crash and recovery
    print("\n⚠️  Simulating crash...")

    # Create new plan instance and recover
    new_plan = create_action_plan(
        name=plan.name,
        description=plan.description,
        workspace_path=plan.workspace_path,
        apply_first_principles=False  # Don't re-analyze
    )

    # Load the checkpoint
    recovered = new_plan.load_checkpoint(checkpoint_id)
    if recovered:
        print(f"✓ Successfully recovered from checkpoint")
        print(f"  Completed tasks: {len(new_plan.completed_task_ids)}")
        print(f"  Current phase: {new_plan.current_phase_id}")

    return new_plan


def example_first_principles_integration():
    """
    Example 4: Demonstrate first principles integration.
    """
    print("\n" + "=" * 80)
    print("Example 4: First Principles Integration")
    print("=" * 80)

    from action_plan import FirstPrinciplesIntegration

    # Create a first principles analyzer
    fp = FirstPrinciplesIntegration()

    # Analyze a problem
    problem = "Build a scalable microservices architecture for an e-commerce platform"

    analysis = fp.analyze_problem(problem)

    print(f"\nProblem: {problem}")
    print(f"\nTrue Problem: {analysis.true_problem}")
    print(f"\nFundamental Truths:")
    for truth in analysis.fundamental_truths:
        print(f"  - {truth}")

    print(f"\nAssumptions:")
    for assumption in analysis.assumptions:
        print(f"  - {assumption.text} (confidence: {assumption.confidence})")

    print(f"\nEssential Requirements:")
    for req in analysis.essential_requirements:
        print(f"  - {req}")

    print(f"\nOptional Elements:")
    for opt in analysis.optional_elements:
        print(f"  - {opt}")

    # Generate hypotheses
    from action_plan import Constraint
    constraints = [
        Constraint("Must handle 10,000 requests per second", ConstraintType.HARD, "performance_requirement"),
        Constraint("Should use Kubernetes", ConstraintType.SOFT, "infrastructure_preference")
    ]

    hypotheses = fp.generate_hypotheses(analysis, constraints)
    print(f"\nGenerated Hypotheses:")
    for hypothesis in hypotheses:
        print(f"\n{hypothesis}")

    return analysis


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("ACTION PLAN SYSTEM - EXAMPLES")
    print("=" * 80)

    # Run examples
    example_basic_action_plan()
    example_execution_simulation()
    example_checkpoint_recovery()
    example_first_principles_integration()

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
