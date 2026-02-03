# Token Prioritization Strategy

**Project:** Build Automated Research Pipeline Agentic Team
**Version:** 1.0
**Date:** 2026-02-04

---

## Executive Summary

This document outlines the token allocation strategy for the 4-agent research pipeline. The goal is to maximize value-per-token by prioritizing high-impact agents and optimizing execution frequency.

**Key Principle:** Not all agents are equal. Allocate tokens based on value density, not just workload.

---

## Agent Token Cost Analysis

### Cost per Run

| Agent | Avg Tokens/Run | Complexity | Primary Operation |
|-------|---------------|------------|-------------------|
| **Scout** | 500-1,000 | Low | API calls, regex extraction, simple parsing |
| **Analyst** | 3,000-5,000 | High | Complex reasoning, ranking algorithms, synthesis |
| **Planner** | 2,000-3,000 | Medium | Task decomposition, structure creation |
| **Executor** | 4,000-8,000 | Variable | Implementation, testing, documentation |

### Daily Token Budget (1M tokens)

| Agent | Frequency | Daily Runs | Daily Tokens | % of Budget |
|-------|-----------|------------|--------------|-------------|
| **Scout** | Every 2 min | 720 | ~540K | 54% |
| **Analyst** | Every 6 min | 240 | ~960K | 96% |
| **Planner** | On approval (~5/day) | 5 | ~12K | 1.2% |
| **Executor** | 3 tasks/day | 3 | ~18K | 1.8% |

**Problem:** Analyst alone exceeds budget. Need optimization.

---

## Optimized Token Allocation

### Strategy: Batching + Selective Analysis

**Analyst Optimization:**
- Batch 5 patterns per analysis run
- Analyze only top 20% of discoveries (filter by simple heuristics first)
- Reduce Analyst runs from 240/day to 48/day

**Optimized Daily Budget:**

| Agent | Frequency | Daily Runs | Tokens/Run | Daily Tokens | % of Budget |
|-------|-----------|------------|------------|--------------|-------------|
| **Scout** | Every 2 min | 720 | 750 | 540K | 54% |
| **Analyst** | Every 30 min | 48 | 5,000 | 240K | 24% |
| **Planner** | On approval | 5 | 2,500 | 12.5K | 1.3% |
| **Executor** | 3 tasks/day | 3 | 6,000 | 18K | 1.8% |
| **Buffer** | - | - | - | 189.5K | 19% |
| **TOTAL** | - | - | - | **1M** | **100%** |

---

## Optimal Agent Ratio

### Value-Weighted Ratio

```
Final Ratio: 10 Scout : 2 Analyst : 0.2 Planner : 0.1 Executor

For every 100 Scout discoveries:
- 20 get analyzed (Analyst filters 80% out)
- 4 generate task plans (Planner)
- 2 get executed (Executor)

Funnel: 100 → 20 → 4 → 2
```

### Why This Ratio?

1. **Scout (10x):** Low cost, high volume. Cast wide net.
2. **Analyst (2x):** High cost, high value. Focus on best patterns.
3. **Planner (0.2x):** Medium cost, only for approved recommendations.
4. **Executor (0.1x):** Highest cost, only highest-value tasks.

---

## Tier-Based Token Allocation

### Tier 1 - Discovery (60% of budget)
**Agents:** Scout + Analyst
**Goal:** Find and validate patterns

```yaml
scout:
  budget_percentage: 40
  daily_tokens: 400K
  runs_per_day: 720
  tokens_per_run: 550
  strategy: Continuous scanning with caching

analyst:
  budget_percentage: 20
  daily_tokens: 200K
  runs_per_day: 40
  tokens_per_run: 5,000
  strategy: Batch analysis (5 patterns per run)
```

### Tier 2 - Planning (15% of budget)
**Agent:** Planner
**Goal:** Transform recommendations into tasks

```yaml
planner:
  budget_percentage: 15
  daily_tokens: 150K
  runs_per_day: 10
  tokens_per_run: 3,000
  strategy: Triggered only on human approval
  max_queue_size: 5  # Don't plan more than 5 tasks ahead
```

### Tier 3 - Execution (15% of budget)
**Agent:** Executor
**Goal:** Implement tasks with quality

```yaml
executor:
  budget_percentage: 15
  daily_tokens: 150K
  runs_per_day: 3
  tokens_per_run: 8,000
  strategy: One task at a time, focus on quality
  max_duration: 4 hours
```

### Tier 4 - Buffer (10% of budget)
**Purpose:** Handle spikes, retries, emergencies

```yaml
buffer:
  budget_percentage: 10
  daily_tokens: 100K
  use_cases:
    - Retry failed analyses
    - Handle high-priority discoveries
    - Emergency task execution
```

---

## Frequency Configuration

### Scout Configuration

```yaml
scout:
  mode: continuous
  interval_seconds: 120  # Every 2 minutes
  max_concurrent: 10
  token_budget_per_run: 750

  # Caching to reduce tokens
  cache_ttl: 3600  # 1 hour
  cache_key: "{source_url}:{last_modified}"

  # Early exit conditions
  skip_if_no_changes: true
  skip_if_rate_limited: true
```

### Analyst Configuration

```yaml
analyst:
  mode: event_driven
  trigger: scout_batch_ready
  batch_size: 5  # Analyze 5 patterns at once
  max_frequency_seconds: 1800  # Every 30 minutes max
  token_budget_per_run: 5000

  # Pre-filtering to save tokens
  min_pattern_confidence: 0.7
  min_source_quality: 0.6
  skip_duplicate_patterns: true

  # Dynamic adjustment
  increase_frequency_if_backlog: 50
  decrease_frequency_if_low_quality: 0.3
```

### Planner Configuration

```yaml
planner:
  mode: triggered
  trigger: human_approval
  token_budget_per_run: 3000
  max_concurrent_plans: 3

  # Planning reuse
  cache_similar_patterns: true
  similarity_threshold: 0.85
```

### Executor Configuration

```yaml
executor:
  mode: selective
  max_concurrent: 1
  max_daily: 3
  token_budget_per_task: 8000
  max_duration_minutes: 240

  # Checkpointing to save tokens on failure
  checkpoint_interval_minutes: 15
  resume_from_checkpoint: true
```

---

## Dynamic Token Management

### TokenManager Implementation

```python
class TokenManager:
    def __init__(self):
        self.daily_budget = 1_000_000
        self.hourly_budget = self.daily_budget / 24

        self.tier_allocations = {
            'scout': 0.40,
            'analyst': 0.20,
            'planner': 0.15,
            'executor': 0.15,
            'buffer': 0.10
        }

        self.usage = {tier: 0 for tier in self.tier_allocations}

    def should_run_agent(self, agent_type: str) -> bool:
        """Check if agent can run within budget"""
        tier = self.get_tier(agent_type)
        current_usage = self.usage[tier]
        budget = self.daily_budget * self.tier_allocations[tier]

        # Allow up to 95% of budget
        if current_usage >= budget * 0.95:
            return False

        # For expensive agents, be more conservative
        if agent_type == 'analyst' and current_usage >= budget * 0.80:
            return False

        return True

    def record_usage(self, agent_type: str, tokens: int):
        """Record token usage"""
        tier = self.get_tier(agent_type)
        self.usage[tier] += tokens

    def adjust_for_backlog(self):
        """Dynamically adjust frequencies based on backlog"""
        analyst_backlog = self.get_analyst_queue_size()
        executor_backlog = self.get_executor_queue_size()

        # If Executor can't keep up, slow down discovery
        if executor_backlog > 10:
            self.reduce_scout_frequency(factor=1.5)
            self.increase_analyst_batch_size(factor=1.5)

        # If Analyst queue is growing, process faster
        if analyst_backlog > 50:
            self.increase_analyst_frequency(factor=1.3)

        # If everything is caught up, increase quality
        if analyst_backlog < 10 and executor_backlog < 3:
            self.increase_analyst_depth(factor=1.2)

    def get_recommendation(self) -> dict:
        """Get token usage recommendations"""
        recommendations = []

        for tier, usage in self.usage.items():
            budget = self.daily_budget * self.tier_allocations[tier]
            percentage = (usage / budget) * 100

            if percentage > 90:
                recommendations.append({
                    'tier': tier,
                    'status': 'critical',
                    'action': f'Reduce {tier} frequency immediately'
                })
            elif percentage > 75:
                recommendations.append({
                    'tier': tier,
                    'status': 'warning',
                    'action': f'Monitor {tier} usage closely'
                })

        return recommendations
```

---

## Cost Optimization Strategies

### 1. Scout Caching (60% token reduction)

```python
class ScoutCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 3600  # 1 hour

    def should_scan(self, source_url: str, last_modified: str) -> bool:
        cache_key = f"{source_url}:{last_modified}"

        if cache_key in self.cache:
            cached_time = self.cache[cache_key]
            if time.time() - cached_time < self.ttl:
                return False  # Skip, already scanned recently

        return True

    def record_scan(self, source_url: str, last_modified: str):
        cache_key = f"{source_url}:{last_modified}"
        self.cache[cache_key] = time.time()
```

**Impact:** Reduces Scout tokens from 540K to ~220K/day

### 2. Analyst Batching (40% token reduction)

```python
class AnalystBatchProcessor:
    def __init__(self):
        self.batch_size = 5
        self.batch = []

    async def add_pattern(self, pattern: Pattern):
        self.batch.append(pattern)

        if len(self.batch) >= self.batch_size:
            await self.process_batch()

    async def process_batch(self):
        # Analyze 5 patterns in one context window
        # Compare patterns to each other (more efficient)
        analysis = await self.analyze_patterns(self.batch)

        # Clear batch
        self.batch = []

        return analysis
```

**Impact:** Reduces Analyst tokens from 240K to ~144K/day

### 3. Pre-Filtering (50% token reduction)

```python
class PatternFilter:
    def should_analyze(self, pattern: Pattern) -> bool:
        # Simple heuristics (no LLM tokens)
        if pattern.confidence < 0.7:
            return False

        if pattern.source_quality < 0.6:
            return False

        if self.is_duplicate(pattern):
            return False

        if len(pattern.description) < 100:
            return False

        return True
```

**Impact:** Filters out 50% before Analyst, saves 120K tokens/day

### 4. Planner Caching (30% token reduction)

```python
class PlannerCache:
    def __init__(self):
        self.plan_cache = {}

    def get_plan(self, pattern: Pattern) -> Optional[TaskPlan]:
        # Find similar patterns
        for cached_pattern, plan in self.plan_cache.items():
            if self.similarity(pattern, cached_pattern) > 0.85:
                return self.adapt_plan(plan, pattern)

        return None

    def cache_plan(self, pattern: Pattern, plan: TaskPlan):
        self.plan_cache[pattern] = plan
```

**Impact:** Reduces Planner tokens from 12.5K to ~8.7K/day

### 5. Executor Checkpointing (20% token reduction)

```python
class ExecutorCheckpoint:
    def __init__(self, interval_minutes=15):
        self.interval = interval_minutes
        self.last_checkpoint = None

    async def execute_with_checkpoints(self, task: Task):
        while not task.complete:
            # Execute for 15 minutes
            result = await self.execute_for_duration(task, self.interval)

            # Save checkpoint
            self.save_checkpoint(task)

            if result.status == "failed":
                # Resume from checkpoint instead of restart
                task = self.load_checkpoint(task.id)
                continue
```

**Impact:** Reduces Executor tokens from 18K to ~14.4K/day

---

## Total Optimized Budget

| Strategy | Original | Optimized | Savings |
|----------|----------|-----------|---------|
| Scout Caching | 540K | 220K | 320K (59%) |
| Analyst Batching | 240K | 144K | 96K (40%) |
| Pre-Filtering | 240K | 120K | 120K (50%) |
| Planner Caching | 12.5K | 8.7K | 3.8K (30%) |
| Executor Checkpointing | 18K | 14.4K | 3.6K (20%) |
| **TOTAL** | **1.05M** | **507K** | **543K (52%)** |

**Result:** System runs within 1M token budget with 493K buffer (49%)

---

## Monitoring & Alerts

### Token Usage Metrics

```yaml
metrics:
  - name: daily_token_usage
    type: counter
    labels: [agent_type, tier]

  - name: token_efficiency
    type: gauge
    labels: [agent_type]
    # value_discovered / tokens_used

  - name: budget_remaining
    type: gauge
    labels: [tier]

  - name: agent_throttle_events
    type: counter
    labels: [agent_type, reason]
```

### Alert Thresholds

```yaml
alerts:
  - name: budget_critical
    condition: tier_usage > 95%
    action: throttle_agents(tier)

  - name: budget_warning
    condition: tier_usage > 80%
    action: notify_ops_channel()

  - name: efficiency_low
    condition: token_efficiency < 0.5
    action: review_agent_configuration()

  - name: backlog_high
    condition: analyst_backlog > 100
    action: increase_analyst_frequency()
```

---

## Recommendations

### Immediate Actions

1. **Implement Scout caching first** - Biggest impact (320K savings)
2. **Deploy Analyst batching** - Second biggest impact (96K savings)
3. **Add pre-filtering** - Easy win (120K savings)
4. **Set up monitoring** - Track before optimizing further

### Long-term Optimizations

1. **ML-based filtering** - Train model to predict pattern value (reduce Analyst load)
2. **Adaptive frequencies** - Auto-adjust based on backlog and quality
3. **Cross-agent learning** - Executor feedback improves Analyst rankings
4. **Token prediction** - Predict token usage before running agents

---

## Conclusion

With these optimizations:
- **Total daily tokens:** ~507K (50% of budget)
- **Buffer for spikes:** 493K (49% of budget)
- **Agent ratio:** 10:2:0.2:0.1 (Scout:Analyst:Planner:Executor)
- **Funnel efficiency:** 100 → 20 → 4 → 2

The system is sustainable and leaves room for growth.

---

*Document version 1.0 - Update as system evolves*
