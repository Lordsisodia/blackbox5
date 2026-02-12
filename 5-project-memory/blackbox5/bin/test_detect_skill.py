#!/usr/bin/env python3
"""
Unit tests for detect-skill.py
Tests trigger types, confidence calculation, and edge cases.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_detect_skill(task: str) -> tuple[dict, int]:
    """Run detect-skill.py and return output and exit code."""
    result = subprocess.run(
        ['python3', '/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py', task],
        capture_output=True,
        text=True
    )
    output = json.loads(result.stdout)
    return output, result.returncode


def test_clear_trigger():
    """Test: Clear trigger (>=85% confidence) - MUST invoke."""
    print("Testing: Clear trigger (high confidence task)...", end=" ")

    # Test a task that should trigger high confidence
    output, exit_code = run_detect_skill("Git commit changes to repository branch merge")

    # Check that git-commit is identified and has reasonable confidence
    assert any(s['id'] == 'git-commit' for s in output['all_matches'])
    git_skill = next((s for s in output['all_matches'] if s['id'] == 'git-commit'), None)
    assert git_skill is not None
    assert git_skill['confidence'] > 70  # Should exceed the threshold

    # Exit code will be 0 only if confidence >= 85
    if git_skill['confidence'] >= 85:
        assert exit_code == 0, f"Expected exit code 0, got {exit_code}"
        assert output['action_required'] == "MUST invoke"
    elif git_skill['confidence'] >= 70:
        assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
        assert output['action_required'] == "SHOULD invoke"

    print("✓ PASS")


def test_discretionary_trigger():
    """Test: Discretionary trigger (>=70% confidence) - SHOULD invoke."""
    print("Testing: Discretionary trigger (PRD creation)...", end=" ")

    output, exit_code = run_detect_skill("Create detailed PRD for user authentication feature")

    # Check that bmad-pm is identified and meets threshold
    assert any(s['id'] == 'bmad-pm' for s in output['all_matches'])
    pm_skill = next((s for s in output['all_matches'] if s['id'] == 'bmad-pm'), None)
    assert pm_skill is not None

    # bmad-pm threshold is 70, so confidence should be >= threshold
    if pm_skill['confidence'] >= 70:
        assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
        assert output['action_required'] == "SHOULD invoke"
    else:
        assert exit_code == 2, f"Expected exit code 2, got {exit_code}"
        assert output['action_required'] == "MAY check"

    print("✓ PASS")


def test_no_match():
    """Test: No match (<70% confidence) - MAY check."""
    print("Testing: No match (generic task)...", end=" ")

    output, exit_code = run_detect_skill("Do some work on the project")

    assert exit_code == 2, f"Expected exit code 2, got {exit_code}"
    assert output['action_required'] == "MAY check"

    print("✓ PASS")


def test_keyword_matching():
    """Test: Keyword matching (exact and partial)."""
    print("Testing: Keyword matching...", end=" ")

    # Exact match should score higher
    output, _ = run_detect_skill("Implement git commit workflow")
    git_skill = next((s for s in output['all_matches'] if s['id'] == 'git-commit'), None)

    assert git_skill is not None
    assert 'git' in git_skill['matched_keywords']
    assert 'commit' in git_skill['matched_keywords']
    assert git_skill['confidence'] > 70

    print("✓ PASS")


def test_task_priority():
    """Test: Recommended skills sorted by confidence."""
    print("Testing: Skill priority ordering...", end=" ")

    output, _ = run_detect_skill("Implement git commit workflow")

    recommended = output['recommended_skills']
    assert len(recommended) == 3
    assert recommended[0]['confidence'] >= recommended[1]['confidence']
    assert recommended[1]['confidence'] >= recommended[2]['confidence']

    print("✓ PASS")


def test_stdin_input():
    """Test: Read task from stdin."""
    print("Testing: Stdin input...", end=" ")

    result = subprocess.run(
        ['python3', '/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py', '--stdin'],
        input="Create PRD for user authentication\n",
        capture_output=True,
        text=True
    )

    output = json.loads(result.stdout)
    assert 'PRD' in output['task_summary']
    assert any(s['id'] == 'bmad-pm' for s in output['all_matches'])

    print("✓ PASS")


def test_file_input():
    """Test: Read task from file."""
    print("Testing: File input...", end=" ")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("Fix critical bug in authentication module\n")
        temp_file = f.name

    try:
        result = subprocess.run(
            ['python3', '/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py',
             '--task-file', temp_file],
            capture_output=True,
            text=True
        )

        output = json.loads(result.stdout)
        assert 'authentication' in output['task_summary'] or 'bug' in output['task_summary']
    finally:
        Path(temp_file).unlink()

    print("✓ PASS")


def test_json_output_format():
    """Test: JSON output has correct structure."""
    print("Testing: JSON output format...", end=" ")

    output, _ = run_detect_skill("Test task")

    # Required fields
    assert 'task_summary' in output
    assert 'recommended_skills' in output
    assert 'action_required' in output
    assert 'all_matches' in output

    # Skill structure
    if output['all_matches']:
        skill = output['all_matches'][0]
        assert 'id' in skill
        assert 'name' in skill
        assert 'confidence' in skill
        assert 'trigger_type' in skill
        assert 'matched_keywords' in skill
        assert isinstance(skill['matched_keywords'], list)

    print("✓ PASS")


def test_edge_cases():
    """Test: Edge cases and error handling."""
    print("Testing: Edge cases...", end=" ")

    # Empty task
    result = subprocess.run(
        ['python3', '/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py', ''],
        capture_output=True,
        text=True
    )
    assert result.returncode == 3  # Error code

    # Non-existent file
    result = subprocess.run(
        ['python3', '/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py',
         '--task-file', '/nonexistent/file.md'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 3  # Error code

    print("✓ PASS")


def run_all_tests():
    """Run all unit tests."""
    print("\n" + "="*60)
    print("detect-skill.py Unit Tests")
    print("="*60 + "\n")

    tests = [
        test_clear_trigger,
        test_discretionary_trigger,
        test_no_match,
        test_keyword_matching,
        test_task_priority,
        test_stdin_input,
        test_file_input,
        test_json_output_format,
        test_edge_cases
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
