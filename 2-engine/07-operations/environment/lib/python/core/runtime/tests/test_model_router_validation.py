#!/usr/bin/env python3
"""
Tests for ModelRouter cost tracking and quality measurement
"""

import pytest
import random
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from model_router import ModelRouter, ModelConfig, TaskComplexity


class TestCostTracking:
    """Test cost tracking functionality"""

    def test_cost_tracking_basic(self):
        """Test that costs are tracked accurately"""

        router = ModelRouter()

        # Route a task
        task = {
            'id': 'test-1',
            'type': 'validation',
            'description': 'Check if code is valid'
        }

        model_config = router.route(task, {})

        # Record result
        router.record_result(
            task_id='test-1',
            model_config=model_config,
            input_tokens=100,
            output_tokens=50,
            success=True,
            quality_score=0.9
        )

        # Verify tracking
        stats = router.get_cost_statistics()

        assert stats['total_tasks'] == 1
        assert stats['total_tokens'] == 150
        assert stats['total_cost'] > 0
        assert 'by_tier' in stats
        assert len(router._cost_history) == 1
        assert len(router._quality_history) == 1

    def test_cost_tracking_multiple_tasks(self):
        """Test cost tracking across multiple tasks"""

        router = ModelRouter()

        # Simulate multiple tasks
        for i in range(10):
            task = {
                'id': f'task-{i}',
                'type': 'validation' if i % 2 == 0 else 'implementation',
                'description': f'Task number {i}'
            }

            model_config = router.route(task, {})

            router.record_result(
                task_id=f'task-{i}',
                model_config=model_config,
                input_tokens=100 + i * 10,
                output_tokens=50 + i * 5,
                success=True,
                quality_score=0.7 + (i % 3) * 0.1
            )

        # Verify tracking
        stats = router.get_cost_statistics()

        assert stats['total_tasks'] == 10
        assert stats['total_tokens'] > 0
        assert stats['total_cost'] > 0
        assert len(stats['by_tier']) > 0

    def test_cost_tracking_by_tier(self):
        """Test that costs are properly categorized by tier"""

        router = ModelRouter()

        # Route tasks of different complexities to hit different tiers
        tasks = [
            {'id': 'simple-1', 'type': 'validation', 'description': 'Simple check'},  # Fast tier
            {'id': 'complex-1', 'type': 'planning', 'description': 'Strategic planning'},  # HQ tier
            {'id': 'standard-1', 'type': 'implementation', 'description': 'Standard task'},  # Balanced tier
        ]

        for task in tasks:
            model_config = router.route(task, {})
            router.record_result(
                task_id=task['id'],
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=True,
                quality_score=0.8
            )

        stats = router.get_cost_statistics()

        # Verify we have stats for multiple tiers
        assert len(stats['by_tier']) >= 1

        # Verify each tier has proper stats
        for tier, tier_stats in stats['by_tier'].items():
            assert 'count' in tier_stats
            assert 'cost' in tier_stats
            assert 'tokens' in tier_stats
            assert 'avg_cost' in tier_stats
            assert 'avg_tokens' in tier_stats
            assert 'avg_quality' in tier_stats

    def test_cost_accuracy_tracking(self):
        """Test that cost accuracy is tracked"""

        router = ModelRouter()

        task = {'id': 'test-1', 'type': 'validation', 'description': 'Test task'}
        model_config = router.route(task, {})

        # Record with specific token counts
        router.record_result(
            task_id='test-1',
            model_config=model_config,
            input_tokens=1000,
            output_tokens=500,
            success=True,
            quality_score=0.8
        )

        # Check the routing decision was updated
        decision = next(d for d in router._routing_decisions if d['task_id'] == 'test-1')

        assert 'actual_cost' in decision
        assert 'estimated_cost' in decision
        assert 'cost_diff' in decision
        assert 'cost_accuracy' in decision

    def test_history_trimming(self):
        """Test that history is trimmed to 1000 entries"""

        router = ModelRouter()

        # Add more than 1000 entries
        for i in range(1100):
            task = {'id': f'task-{i}', 'type': 'validation', 'description': 'Test'}
            model_config = router.route(task, {})
            router.record_result(
                task_id=f'task-{i}',
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=True,
                quality_score=0.8
            )

        # Verify history was trimmed
        assert len(router._cost_history) == 1000
        assert len(router._quality_history) == 1000

    def test_empty_statistics(self):
        """Test statistics when no data available"""

        router = ModelRouter()

        stats = router.get_cost_statistics()

        assert 'message' in stats
        assert stats['message'] == 'No cost data available'


class TestQualityMeasurement:
    """Test quality measurement functionality"""

    def test_quality_measurement_perfect(self):
        """Test quality measurement for perfect result"""

        router = ModelRouter()

        result = {
            'success': True,
            'error': None,
            'output': 'This is a substantial output with meaningful content and no errors'
        }

        task = {'description': 'Test task'}

        quality = router.measure_quality(result, task)

        assert quality > 0.8  # Should be high quality

    def test_quality_measurement_failed(self):
        """Test quality measurement for failed result"""

        router = ModelRouter()

        result = {
            'success': False,
            'error': 'Something went wrong',
            'output': 'Error: failed to complete'
        }

        task = {'description': 'Test task'}

        quality = router.measure_quality(result, task)

        assert quality < 0.5  # Should be low quality

    def test_quality_measurement_no_output(self):
        """Test quality measurement with minimal output"""

        router = ModelRouter()

        result = {
            'success': True,
            'error': None,
            'output': 'Short'
        }

        task = {'description': 'Test task'}

        quality = router.measure_quality(result, task)

        # Should have base quality from success + no error, but low output quality
        assert 0.4 <= quality <= 0.7

    def test_quality_with_error_patterns(self):
        """Test quality measurement detects error patterns in output"""

        router = ModelRouter()

        result = {
            'success': True,
            'error': None,
            'output': 'This output contains an exception error and failed to complete'
        }

        task = {'description': 'Test task'}

        quality = router.measure_quality(result, task)

        # Should penalize for error patterns in output
        assert quality < 0.7


class TestRoutingAnalysis:
    """Test routing effectiveness analysis"""

    def test_routing_analysis_empty(self):
        """Test analysis with no data"""

        router = ModelRouter()

        analysis = router.analyze_routing_effectiveness()

        assert 'statistics' in analysis
        assert 'insights' in analysis
        assert 'recommendations' in analysis

    def test_routing_analysis_with_data(self):
        """Test analysis generates insights"""

        router = ModelRouter()

        # Simulate various routing decisions
        for i in range(50):
            task = {'id': f'task-{i}', 'type': 'validation', 'description': 'Test task'}
            model_config = router.route(task, {})

            # Simulate results with varying quality
            router.record_result(
                task_id=f'task-{i}',
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=True,
                quality_score=random.uniform(0.6, 0.95)
            )

        # Analyze effectiveness
        analysis = router.analyze_routing_effectiveness()

        # Verify structure
        assert 'statistics' in analysis
        assert 'insights' in analysis
        assert 'recommendations' in analysis

        # Verify statistics
        stats = analysis['statistics']
        assert stats['total_tasks'] == 50
        assert 'by_tier' in stats

    def test_routing_analysis_low_quality_warning(self):
        """Test analysis warns about low quality tiers"""

        router = ModelRouter()

        # Simulate low quality results for fast tier
        for i in range(10):
            task = {'id': f'low-q-{i}', 'type': 'validation', 'description': 'Test'}
            model_config = router.route(task, {})

            router.record_result(
                task_id=f'low-q-{i}',
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=True,
                quality_score=0.5  # Low quality
            )

        analysis = router.analyze_routing_effectiveness()

        # Check for warnings
        insights = analysis['insights']
        warning_insights = [i for i in insights if i['severity'] == 'warning']

        # Should have at least one warning about quality
        assert any('quality' in i['message'].lower() for i in warning_insights)

    def test_routing_analysis_cost_overrun_warning(self):
        """Test analysis warns about cost estimate inaccuracies"""

        router = ModelRouter()

        # Force cost inaccuracy by routing with wrong estimates
        task = {'id': 'cost-test', 'type': 'validation', 'description': 'A' * 1000}
        model_config = router.route(task, {})

        # Record much higher actual cost
        router.record_result(
            task_id='cost-test',
            model_config=model_config,
            input_tokens=10000,  # Much higher than estimated
            output_tokens=5000,
            success=True,
            quality_score=0.8
        )

        analysis = router.analyze_routing_effectiveness()

        # Should have warning about cost accuracy
        insights = analysis['insights']
        cost_insights = [i for i in insights if 'cost' in i['message'].lower()]

        assert len(cost_insights) > 0

    def test_generate_recommendations(self):
        """Test recommendations generation"""

        router = ModelRouter()

        # Create scenario where fast tier is used infrequently but has high quality
        for i in range(20):
            task = {
                'id': f'task-{i}',
                'type': 'validation',
                'description': 'Test validation task'
            }
            model_config = router.route(task, {})

            router.record_result(
                task_id=f'task-{i}',
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=True,
                quality_score=0.9  # High quality
            )

        analysis = router.analyze_routing_effectiveness()
        recommendations = analysis['recommendations']

        # Should have at least some recommendations
        assert isinstance(recommendations, list)


class TestIntegration:
    """Integration tests for cost tracking workflow"""

    def test_full_workflow(self):
        """Test complete workflow from routing to analysis"""

        router = ModelRouter()

        # Simulate realistic workflow
        tasks = [
            {'id': 't1', 'type': 'validation', 'description': 'Validate code'},
            {'id': 't2', 'type': 'planning', 'description': 'Plan architecture'},
            {'id': 't3', 'type': 'implementation', 'description': 'Implement feature'},
            {'id': 't4', 'type': 'validation', 'description': 'Check implementation'},
            {'id': 't5', 'type': 'simple', 'description': 'List files'},
        ]

        # Route all tasks
        for task in tasks:
            model_config = router.route(task, {})

            # Simulate execution and record results
            result = {
                'success': True,
                'error': None,
                'output': f'Output for {task["id"]}'
            }

            quality = router.measure_quality(result, task)

            router.record_result(
                task_id=task['id'],
                model_config=model_config,
                input_tokens=100,
                output_tokens=50,
                success=result['success'],
                quality_score=quality
            )

        # Get statistics
        stats = router.get_cost_statistics()
        assert stats['total_tasks'] == 5

        # Analyze effectiveness
        analysis = router.analyze_routing_effectiveness()
        assert 'statistics' in analysis
        assert 'insights' in analysis
        assert 'recommendations' in analysis

        # Verify all tasks were tracked
        assert len(router._routing_decisions) == 5
        assert len(router._cost_history) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
