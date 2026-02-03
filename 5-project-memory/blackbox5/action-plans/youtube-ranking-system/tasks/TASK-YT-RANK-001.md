# TASK-YT-RANK-001: Create Channel Scoring Module

**Status:** in_progress
**Priority:** HIGH
**Phase:** 1 - Core Scoring Engine
**Estimated Hours:** 1.5

## Objective

Implement the core scoring engine that calculates composite scores for YouTube channels based on multiple weighted dimensions.

## Success Criteria

- [ ] `scripts/scoring/engine.py` created with scoring functions
- [ ] All 6 scoring dimensions implemented
- [ ] Weight system configurable
- [ ] Unit tests pass

## Implementation Details

### Scoring Formula
```python
Channel Score =
    (Knowledge × 0.25) +
    (Engagement × 0.20) +
    (Consistency × 0.20) +
    (Quality × 0.15) +
    (Impact × 0.15) +
    (Novelty × 0.05)
```

### File Structure
```
scripts/scoring/
├── __init__.py
├── engine.py          # Main scoring logic
├── weights.py         # Weight configuration
└── tests/
    └── test_engine.py
```

## Acceptance Criteria

1. Can calculate score for any channel with available data
2. All scores normalized to 0-100 range
3. Weights are configurable via config file
4. Handles missing data gracefully (uses defaults)

## Output

- `scripts/scoring/engine.py` - Main module
- `scripts/scoring/weights.py` - Configuration
- `tests/test_engine.py` - Unit tests
