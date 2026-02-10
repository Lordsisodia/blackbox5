# API Selector Agent

## Purpose
Analyzes task requirements and automatically selects the optimal API provider for BlackBox5.

## Features
- Task requirement analysis (context length, task type, capabilities needed)
- Provider selection based on capability, priority, cost, and availability
- Automatic fallback and retry logic
- Health monitoring and provider status tracking
- Cost optimization based on task criticality

## Usage
```python
from agents.api_selector import APISelector

selector = APISelector()

# Get best provider for a task
provider = selector.select_provider(
    task_type="coding",
    context_length=50000,
    required_capabilities=["coding", "reasoning"],
    criticality="medium"
)
```

## Task Types Supported
- `long_context` - Tasks requiring large context windows
- `coding` - Programming and code-related tasks
- `reasoning` - Complex analytical tasks
- `video_processing` - Video analysis tasks
- `vision` - Image analysis tasks
- `general` - Default tasks
