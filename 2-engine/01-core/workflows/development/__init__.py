"""
Development Workflows
""")
    print(f"  ✅ Created workflows/development/")

    # Create planning/ subdirectory
    plan_dir = workflows_dir / "planning"
    plan_dir.mkdir(exist_ok=True)

    (plan_dir / "__init__.py").write_text(
Planning Workflows
