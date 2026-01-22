#!/usr/bin/env python3
"""
Model Router - Smart routing for GLM-4 and other models
Implements hierarchical model selection based on task complexity
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum
import re
from datetime import datetime


class TaskComplexity(Enum):
    """Task complexity levels"""
    STRATEGIC_THINKING = "strategic_thinking"  # HQ model required
    CODE_WITH_FRAMEWORK = "code_with_framework"  # Balanced with framework
    STANDARD_EXECUTION = "standard_execution"  # Balanced
    VALIDATION = "validation"  # Fast model
    SIMPLE_OPERATION = "simple_operation"  # Fastest model


class ModelConfig:
    """Model configuration"""
    def __init__(self,
                 model: str,
                 provider: str,
                 temperature: float,
                 max_tokens: int,
                 framework: Optional[str] = None,
                 reason: str = ""):
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.framework = framework
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "model": self.model,
            "provider": self.provider,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "framework": self.framework,
            "reason": self.reason
        }


class ModelRouter:
    """
    Routes tasks to appropriate models based on complexity

    Routing Strategy:
    - Strategic Thinking: GLM-4 Plus (current) → Claude Opus (future)
    - Code with Framework: Claude Sonnet / GLM-4 with framework
    - Standard Execution: Claude Sonnet / GLM-4
    - Validation: Claude Haiku / GLM-4 Fast
    - Simple Operations: Claude Haiku / GLM-4 Fast
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize model router"""
        self.config_path = config_path or Path(__file__).parent.parent.parent / "shared" / "schemas" / "model-router.yaml"

        # Load model configurations
        self.models = self._load_models()

        # Default to GLM-4 if available
        self.primary_model = "glm-4-plus"
        self.fallback_model = "claude-sonnet"

        # Cost tracking and quality measurement
        self._cost_history = []
        self._quality_history = []
        self._routing_decisions = []

    def _load_models(self) -> Dict[str, Dict[str, Any]]:
        """Load available model configurations"""
        # Current models (GLM-4)
        # Future models (Claude)
        return {
            "glm-4-plus": {
                "provider": "zhipu",
                "model": "glm-4-plus",
                "temperature": 0.3,
                "max_tokens": 128000,
                "tier": "hq",
                "cost_per_1k_tokens": 0.005
            },
            "glm-4": {
                "provider": "zhipu",
                "model": "glm-4",
                "temperature": 0.5,
                "max_tokens": 128000,
                "tier": "balanced",
                "cost_per_1k_tokens": 0.003
            },
            "glm-4-flash": {
                "provider": "zhipu",
                "model": "glm-4-flash",
                "temperature": 0.7,
                "max_tokens": 128000,
                "tier": "fast",
                "cost_per_1k_tokens": 0.0001
            },
            "claude-opus": {
                "provider": "anthropic",
                "model": "claude-opus-4-20250514",
                "temperature": 0.3,
                "max_tokens": 200000,
                "tier": "hq",
                "cost_per_1k_tokens": 0.015
            },
            "claude-sonnet": {
                "provider": "anthropic",
                "model": "claude-sonnet-4-20250514",
                "temperature": 0.5,
                "max_tokens": 200000,
                "tier": "balanced",
                "cost_per_1k_tokens": 0.003
            },
            "claude-haiku": {
                "provider": "anthropic",
                "model": "claude-haiku-4-20250514",
                "temperature": 0.7,
                "max_tokens": 200000,
                "tier": "fast",
                "cost_per_1k_tokens": 0.001
            }
        }

    def route(self,
              task: Any,
              context: Optional[Dict[str, Any]] = None) -> ModelConfig:
        """
        Route task to appropriate model

        Args:
            task: Task (dict or Task object) with description, type, etc.
            context: Additional context (codebase, patterns, etc.)

        Returns:
            ModelConfig for the task
        """
        complexity = self._analyze_complexity(task, context)

        # Route based on complexity
        if complexity == TaskComplexity.STRATEGIC_THINKING:
            model_config = self._get_hq_config()
        elif complexity == TaskComplexity.CODE_WITH_FRAMEWORK:
            model_config = self._get_framework_config(context)
        elif complexity == TaskComplexity.STANDARD_EXECUTION:
            model_config = self._get_balanced_config()
        elif complexity == TaskComplexity.VALIDATION:
            model_config = self._get_fast_config()
        else:  # SIMPLE_OPERATION
            model_config = self._get_fastest_config()

        # Estimate cost for tracking
        task_id = self._get_task_id(task)
        estimated_input = self._estimate_tokens(self._get_task_description(task))
        estimated_cost = self.estimate_cost(
            model_config,
            estimated_input,
            estimated_input * 2  # Assume output is 2x input
        )

        # Record routing decision
        decision = {
            'task_id': task_id,
            'complexity': complexity.value,
            'model': model_config.model,
            'tier': self.models[model_config.model]['tier'],
            'estimated_cost': estimated_cost,
            'estimated_tokens': estimated_input * 3,  # input + output (2x)
            'timestamp': datetime.now().isoformat()
        }

        self._routing_decisions.append(decision)

        return model_config

    def _get_task_id(self, task: Any) -> str:
        """Extract task ID from task"""
        if hasattr(task, 'id'):
            return task.id
        return task.get('id', 'unknown')

    def _get_task_description(self, task: Any) -> str:
        """Extract task description from task"""
        if hasattr(task, 'description'):
            return task.description
        return task.get('description', '')

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count from text (rough approximation)"""
        # Rough estimate: 1 token ~= 4 characters for English
        # This is a simple heuristic - in production you'd use a proper tokenizer
        return len(text) // 4

    def _analyze_complexity(self,
                           task: Any,
                           context: Optional[Dict[str, Any]]) -> TaskComplexity:
        """Analyze task complexity"""

        # Handle both dict and Task objects
        if hasattr(task, 'type'):
            task_type = task.type.lower()
            description = task.description.lower()
            importance = getattr(task, 'importance', None)
        else:
            task_type = task.get("type", "").lower()
            description = task.get("description", "").lower()
            importance = task.get("importance", None)

        # Strategic thinking indicators
        strategic_keywords = [
            "architect", "design", "plan", "strategy", "analyze",
            "research", "break down", "decompose", "evaluate",
            "complex", "system", "architecture"
        ]

        # Code with framework indicators
        framework_keywords = [
            "implement", "code", "build", "create", "feature",
            "function", "component", "module"
        ]

        # Validation indicators
        validation_keywords = [
            "validate", "check", "verify", "test", "review",
            "lint", "format", "inspect"
        ]

        # Simple operation indicators
        simple_keywords = [
            "list", "show", "get", "fetch", "read",
            "display", "print", "log"
        ]

        # Check for strategic thinking
        if (task_type in ["planning", "architecture", "analysis"] or
            any(kw in description for kw in strategic_keywords) or
            importance == "high"):
            return TaskComplexity.STRATEGIC_THINKING

        # Check for code with framework
        if (context and context.get("framework") or
            task_type in ["implementation", "coding"] or
            any(kw in description for kw in framework_keywords)):
            return TaskComplexity.CODE_WITH_FRAMEWORK

        # Check for validation
        if (task_type in ["validation", "testing", "review"] or
            any(kw in description for kw in validation_keywords)):
            return TaskComplexity.VALIDATION

        # Check for simple operations
        if (task_type in ["information", "listing"] or
            any(kw in description for kw in simple_keywords)):
            return TaskComplexity.SIMPLE_OPERATION

        # Default to standard execution
        return TaskComplexity.STANDARD_EXECUTION

    def _get_hq_config(self) -> ModelConfig:
        """Get HQ model configuration (for strategic thinking)"""
        # Prefer GLM-4 Plus (current), fallback to Claude Opus (future)
        if self.primary_model in ["glm-4-plus", "claude-opus"]:
            model_config = self.models[self.primary_model]
        else:
            model_config = self.models["glm-4-plus"]

        return ModelConfig(
            model=model_config["model"],
            provider=model_config["provider"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            reason="Strategic thinking requires highest quality reasoning"
        )

    def _get_framework_config(self, context: Dict[str, Any]) -> ModelConfig:
        """Get framework-aware model configuration"""
        framework = context.get("framework", "standard") if context else "standard"

        # For framework-based tasks, use balanced model
        model_config = self.models[self.primary_model]
        if model_config["tier"] == "hq":
            # Downgrade to balanced if primary is HQ
            model_config = self.models["glm-4"]

        return ModelConfig(
            model=model_config["model"],
            provider=model_config["provider"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            framework=framework,
            reason=f"Code execution with {framework} framework"
        )

    def _get_balanced_config(self) -> ModelConfig:
        """Get balanced model configuration"""
        model_config = self.models[self.primary_model]
        if model_config["tier"] == "hq":
            model_config = self.models["glm-4"]

        return ModelConfig(
            model=model_config["model"],
            provider=model_config["provider"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            reason="Standard execution requires balanced quality/speed"
        )

    def _get_fast_config(self) -> ModelConfig:
        """Get fast model configuration"""
        # Use fastest available model
        if "glm-4-flash" in self.models:
            model_config = self.models["glm-4-flash"]
        else:
            model_config = self.models["claude-haiku"]

        return ModelConfig(
            model=model_config["model"],
            provider=model_config["provider"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            reason="Validation and quick checks use fast model"
        )

    def _get_fastest_config(self) -> ModelConfig:
        """Get fastest model configuration"""
        # Use absolute fastest
        if "glm-4-flash" in self.models:
            model_config = self.models["glm-4-flash"]
        else:
            model_config = self.models["claude-haiku"]

        return ModelConfig(
            model=model_config["model"],
            provider=model_config["provider"],
            temperature=0.7,  # Higher temp for creative tasks
            max_tokens=model_config["max_tokens"],
            reason="Simple operations use fastest model"
        )

    def estimate_cost(self,
                      model_config: ModelConfig,
                      input_tokens: int,
                      output_tokens: int) -> float:
        """Estimate cost for a task"""
        model_name = model_config.model

        if model_name in self.models:
            cost_per_1k = self.models[model_name]["cost_per_1k_tokens"]
            total_tokens = input_tokens + output_tokens
            return (total_tokens / 1000) * cost_per_1k

        return 0.0

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        models_list = []

        for model_name, config in self.models.items():
            models_list.append({
                "name": model_name,
                "provider": config["provider"],
                "tier": config["tier"],
                "max_tokens": config["max_tokens"],
                "cost_per_1k": config["cost_per_1k_tokens"]
            })

        return sorted(models_list, key=lambda x: x["cost_per_1k"])

    def set_primary_model(self, model_name: str):
        """Set primary model (for GLM-4 vs Claude preference)"""
        if model_name in self.models:
            self.primary_model = model_name
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def record_result(self, task_id: str, model_config: ModelConfig,
                     input_tokens: int, output_tokens: int,
                     success: bool, quality_score: float):
        """Record actual cost and quality after task completion"""

        actual_cost = self.estimate_cost(model_config, input_tokens, output_tokens)

        # Find the routing decision
        decision = next((d for d in self._routing_decisions if d['task_id'] == task_id), None)

        if decision:
            # Update with actual results
            decision['actual_cost'] = actual_cost
            decision['input_tokens'] = input_tokens
            decision['output_tokens'] = output_tokens
            decision['total_tokens'] = input_tokens + output_tokens
            decision['success'] = success
            decision['quality_score'] = quality_score

            # Calculate cost difference
            if actual_cost > 0:
                decision['cost_diff'] = actual_cost - decision['estimated_cost']
                decision['cost_accuracy'] = abs(decision['cost_diff'] / actual_cost)
            else:
                decision['cost_diff'] = 0
                decision['cost_accuracy'] = 0

        # Store in history
        self._cost_history.append(decision)
        self._quality_history.append(quality_score)

        # Trim history to last 1000 entries
        if len(self._cost_history) > 1000:
            self._cost_history = self._cost_history[-1000:]
        if len(self._quality_history) > 1000:
            self._quality_history = self._quality_history[-1000:]

    def measure_quality(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        """Measure quality of task result (0.0 to 1.0)"""

        quality_score = 0.0

        # Factor 1: Success (40%)
        if result.get('success', False):
            quality_score += 0.4

        # Factor 2: No errors (30%)
        if not result.get('error'):
            quality_score += 0.3

        # Factor 3: Output quality (30%)
        output = result.get('output', '')
        if output:
            # Check for meaningful output (not empty/error messages)
            if len(output) > 100:  # Substantial output
                quality_score += 0.15

            # Check for no error patterns
            error_patterns = ['error', 'failed', 'exception', 'cannot']
            if not any(p in output.lower() for p in error_patterns):
                quality_score += 0.15

        return min(quality_score, 1.0)

    def get_cost_statistics(self) -> Dict[str, Any]:
        """Get cost and quality statistics by tier"""

        if not self._cost_history:
            return {'message': 'No cost data available'}

        # Calculate statistics
        total_cost = sum(d.get('actual_cost', d.get('estimated_cost', 0)) for d in self._cost_history)
        total_tokens = sum(d.get('total_tokens', 0) for d in self._cost_history)

        # By tier
        by_tier = {}
        for decision in self._cost_history:
            tier = decision.get('tier', 'unknown')
            if tier not in by_tier:
                by_tier[tier] = {
                    'count': 0,
                    'cost': 0,
                    'tokens': 0,
                    'avg_quality': 0
                }

            by_tier[tier]['count'] += 1
            by_tier[tier]['cost'] += decision.get('actual_cost', 0)
            by_tier[tier]['tokens'] += decision.get('total_tokens', 0)

        # Calculate averages
        for tier, stats in by_tier.items():
            stats['avg_cost'] = stats['cost'] / stats['count']
            stats['avg_tokens'] = stats['tokens'] / stats['count']

            # Get quality scores for this tier
            qualities = [d.get('quality_score', 0) for d in self._cost_history if d.get('tier') == tier]
            stats['avg_quality'] = sum(qualities) / len(qualities) if qualities else 0

        # Calculate cost accuracy
        cost_accuracies = [d.get('cost_accuracy', 0) for d in self._cost_history if d.get('cost_accuracy', 0) > 0]
        avg_cost_accuracy = sum(cost_accuracies) / len(cost_accuracies) if cost_accuracies else 0

        return {
            'total_cost': total_cost,
            'total_tokens': total_tokens,
            'total_tasks': len(self._cost_history),
            'by_tier': by_tier,
            'cost_accuracy': avg_cost_accuracy
        }

    def analyze_routing_effectiveness(self) -> Dict[str, Any]:
        """Analyze if routing decisions were effective"""

        stats = self.get_cost_statistics()

        if 'message' in stats:
            return {
                'statistics': stats,
                'insights': [{'severity': 'info', 'message': 'No data available for analysis'}],
                'recommendations': []
            }

        insights = []

        # Insight 1: Quality by tier
        by_tier = stats.get('by_tier', {})
        for tier, tier_stats in by_tier.items():
            if tier_stats['avg_quality'] < 0.7:
                insights.append({
                    'severity': 'warning',
                    'message': f"Tier '{tier}' has low quality ({tier_stats['avg_quality']:.2f}). Consider using higher tier."
                })
            elif tier_stats['avg_quality'] > 0.95:
                insights.append({
                    'severity': 'info',
                    'message': f"Tier '{tier}' has excellent quality ({tier_stats['avg_quality']:.2f}). Could use lower tier."
                })

        # Insight 2: Cost overruns
        cost_accuracy = stats.get('cost_accuracy', 0)
        if cost_accuracy > 0.3:
            insights.append({
                'severity': 'warning',
                'message': f"Cost estimates are off by {cost_accuracy*100:.1f}%. Calibrate token estimation."
            })

        # Insight 3: Routing distribution
        tier_counts = {tier: s['count'] for tier, s in by_tier.items()}
        if tier_counts.get('hq', 0) > tier_counts.get('fast', 0) * 2:
            insights.append({
                'severity': 'info',
                'message': f"Overusing HQ model. {tier_counts['hq']} HQ vs {tier_counts.get('fast', 0)} fast tasks."
            })

        return {
            'statistics': stats,
            'insights': insights,
            'recommendations': self._generate_recommendations(stats)
        }

    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""

        recommendations = []

        # Recommendation 1: If fast tier quality is high, use it more
        by_tier = stats.get('by_tier', {})
        if 'fast' in by_tier and by_tier['fast']['avg_quality'] > 0.8:
            fast_count = by_tier['fast']['count']
            total_count = stats['total_tasks']
            if fast_count / total_count < 0.3:
                recommendations.append(
                    f"Fast tier quality is good (>{by_tier['fast']['avg_quality']:.2f}). "
                    "Consider routing more simple tasks to fast tier to reduce costs."
                )

        # Recommendation 2: If HQ tier is overused
        if 'hq' in by_tier:
            hq_count = by_tier['hq']['count']
            total_count = stats['total_tasks']
            if hq_count / total_count > 0.5:
                recommendations.append(
                    f"HQ model used for {hq_count/total_count*100:.1f}% of tasks. "
                    "Review if all require highest quality."
                )

        # Recommendation 3: Cost accuracy issues
        if stats.get('cost_accuracy', 0) > 0.3:
            recommendations.append(
                "Calibrate token estimation - current estimates are off by "
                f"{stats['cost_accuracy']*100:.1f}% on average."
            )

        return recommendations


# Singleton instance
_router_instance = None

def get_router() -> ModelRouter:
    """Get singleton router instance"""
    global _router_instance
    if _router_instance is None:
        _router_instance = ModelRouter()
    return _router_instance
