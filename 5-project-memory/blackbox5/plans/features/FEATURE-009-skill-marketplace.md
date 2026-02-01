# Feature Specification: F-009 Skill Marketplace & Discovery System

**Version:** 1.0.0
**Status:** planned
**Created:** 2026-02-01
**Task:** TASK-1769955705
**Priority:** HIGH (Score: 3.5)
**Estimated:** 180 minutes (~3 hours)
**Value Score:** 7/10
**Category:** Infrastructure

---

## Executive Summary

Implement a Skill Marketplace & Discovery System to enable RALF agents to discover, share, and version skills collaboratively. The system provides a centralized skill registry with metadata, search functionality, versioning support, and automatic skill recommendations based on task patterns.

**Strategic Value:**
- **Discoverability:** Skills are easy to find and search
- **Collaboration:** Agents can contribute and share new skills
- **Quality:** Skill versioning prevents breaking changes
- **Intelligence:** Automatic recommendations reduce manual skill selection
- **Scalability:** Registry grows with the system

---

## User Value

**Who:** RALF agents (executor, planner) and operators

**Problem:**
- Current skills are hard to discover (file-based, no central registry)
- No skill metadata (author, version, description, tags)
- Skill versioning is manual and error-prone (no semantic versioning)
- No automatic skill recommendations based on task patterns
- Agents cannot easily find or contribute new skills
- skill-usage.yaml exists but no integration with actual skill loading

**Value:**
- **Centralized registry:** All skills tracked with metadata in one place
- **Search and discovery:** Find skills by keyword, domain, or tag
- **Version management:** Semantic versioning (MAJOR.MINOR.PATCH) prevents breaking changes
- **Automatic recommendations:** Suggest relevant skills based on task context
- **Contribution workflow:** Easy to add new skills to the marketplace
- **Quality tracking:** Skill effectiveness monitoring

**Use Cases:**
1. **Skill Discovery:** Executor searches for "testing" skills, finds bmad-qa
2. **Version Check:** Before using skill, check if version 2.0 introduces breaking changes
3. **Automatic Recommendation:** Task mentions "API design", system suggests bmad-architect
4. **Skill Contribution:** Developer creates new skill, registers in marketplace
5. **Effectiveness Tracking:** Track how often bmad-pm successfully completes requirements tasks

---

## MVP Scope

**What's Included (MVP):**
1. **Skill Registry** (`skill_registry.py`)
   - Register skills with metadata (name, version, domain, author, description, tags)
   - Search skills by keyword, domain, tag
   - List all skills with filtering
   - Get skill metadata by name
   - YAML-based storage (registry.yaml)

2. **Skill Versioning** (`skill_versioning.py`)
   - Semantic versioning (MAJOR.MINOR.PATCH)
   - Version comparison (greater than, less than, equal)
   - Version migration scripts
   - Breaking change detection

3. **Skill Recommendation Engine** (`skill_recommender.py`)
   - Pattern matching based on task keywords
   - Domain-based recommendations
   - Confidence scoring (0-100%)
   - Top-N recommendations

4. **Skill Selection Integration** (Step 2.5 enhancement)
   - Integrate registry into executor's skill checking workflow
   - Auto-recommend skills during task execution
   - Confidence-based skill invocation

5. **Documentation**
   - Operations guide: skill-marketplace-guide.md
   - Skill contribution workflow
   - CLI usage examples
   - API reference

6. **Registry Storage**
   - File: `2-engine/.autonomous/config/skill-registry.yaml`
   - Schema: name, version, domain, author, description, tags, created_at, effectiveness_score

**What's Excluded (Future Phases):**
- Skill dependency management (skills requiring other skills)
- Skill deprecation warnings and lifecycle management
- Skill analytics dashboard (visualization of usage patterns)
- Integration with external skill repositories (GitHub, npm-style)
- Skill rating and review system (community feedback)
- Machine learning for recommendation accuracy

---

## Success Criteria

### Must-Have (P0)
- [ ] Skill registry tracks all skills with metadata (at least 10 skills registered)
- [ ] Search/find skills by keyword/domain functional (find "bmad-qa" via "testing" keyword)
- [ ] Skill versioning system implemented (semantic versioning with comparison)
- [ ] Recommendations appear based on task patterns (confidence >= 70%)
- [ ] Integration with existing skill-usage.yaml (registry enhances, not replaces)

### Should-Have (P1)
- [ ] Skill contribution workflow (add new skills to registry)
- [ ] Skill effectiveness tracking (success rate per skill)
- [ ] Skill rating/review system (manual feedback)
- [ ] CLI interface for skill marketplace (python -m skill_registry search <keyword>)

### Nice-to-Have (P2)
- [ ] Skill dependency management (skill A requires skill B)
- [ ] Skill deprecation warnings (old skills marked as deprecated)
- [ ] Skill analytics dashboard (visualize usage patterns)
- [ ] Integration with external skill repositories (GitHub-based skill sharing)

---

## Technical Approach

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Task Execution                          │
│                  (RALF-Executor)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────────┐
│              Step 2.5: Skill Checking                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Skill Recommendation Engine (skill_recommender.py)  │  │
│  │  - Analyze task context                              │  │
│  │  - Match patterns in registry                        │  │
│  │  - Calculate confidence                              │  │
│  │  - Return top recommendations                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
│                              v                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Skill Registry (skill_registry.py)                │  │
│  │  - Search by keyword/domain/tag                      │  │
│  │  - Get skill metadata                                │  │
│  │  - List all skills                                   │  │
│  │  - Register new skills                               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│                         v                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Storage: skill-registry.yaml                        │  │
│  │  - All skill metadata                                │  │
│  │  - Version information                               │  │
│  │  - Effectiveness scores                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────────┐
│              Decision: Invoke Skill?                        │
│              If confidence >= 70%: YES                      │
│              Else: Standard execution                       │
└─────────────────────────────────────────────────────────────┘
```

### Components

#### 1. Skill Registry (`skill_registry.py`)

**Purpose:** Central registry for all skills with metadata

**Key Functions:**
```python
def register_skill(name: str, version: str, domain: str, author: str,
                   description: str, tags: List[str]) -> Skill
def search_skills(keyword: str, domain: str = None) -> List[Skill]
def get_skill_metadata(name: str) -> Optional[Skill]
def list_skills(domain: str = None, tag: str = None) -> List[Skill]
def update_skill_effectiveness(name: str, success: bool)
```

**Data Structures:**
```python
@dataclass
class Skill:
    name: str
    version: str  # Semantic versioning (MAJOR.MINOR.PATCH)
    domain: str
    author: str
    description: str
    tags: List[str]
    created_at: str
    effectiveness_score: float  # 0.0 to 1.0
    usage_count: int
```

**Storage:** `2-engine/.autonomous/config/skill-registry.yaml`

#### 2. Skill Versioning (`skill_versioning.py`)

**Purpose:** Manage skill versions with semantic versioning

**Key Functions:**
```python
def parse_version(version: str) -> Tuple[int, int, int]
def compare_versions(v1: str, v2: str) -> int  # -1, 0, 1
def is_compatible(required: str, current: str) -> bool
def migrate_skill(name: str, old_version: str, new_version: str)
def detect_breaking_changes(old_version: str, new_version: str) -> bool
```

**Semantic Versioning:**
- MAJOR: Incompatible API changes
- MINOR: New functionality (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

#### 3. Skill Recommender (`skill_recommender.py`)

**Purpose:** Recommend skills based on task context

**Key Functions:**
```python
def recommend_skills(task_context: Dict[str, Any]) -> List[Recommendation]
def analyze_task_patterns(task_description: str, task_type: str) -> List[str]
def calculate_confidence(skill: Skill, task_context: Dict) -> float
def get_top_recommendations(task_context: Dict, n: int = 3) -> List[Recommendation]
```

**Data Structures:**
```python
@dataclass
class Recommendation:
    skill: Skill
    confidence: float  # 0.0 to 1.0
    matched_keywords: List[str]
    rationale: str
```

**Recommendation Algorithm:**
1. Extract keywords from task (type, description, approach)
2. Match against skill registry (name, description, tags, domain)
3. Calculate confidence based on:
   - Keyword overlap (40% weight)
   - Domain match (30% weight)
   - Historical effectiveness (20% weight)
   - Usage frequency (10% weight)
4. Return top-N skills with confidence >= threshold

#### 4. Skill Selection Integration

**Enhancement:** Add to executor's Step 2.5 (Skill Checking)

**New Workflow:**
```python
# Step 2.5: Skill Checking
task_context = extract_task_context(task_file)
recommendations = recommend_skills(task_context)

if recommendations and recommendations[0].confidence >= 0.7:
    skill = recommendations[0].skill
    invoke_skill(skill)
else:
    proceed_with_standard_execution()
```

### File Structure

```
2-engine/.autonomous/
├── lib/
│   ├── skill_registry.py        # NEW: Skill registry
│   ├── skill_versioning.py      # NEW: Skill versioning
│   └── skill_recommender.py     # NEW: Skill recommendation
├── config/
│   ├── skill-registry.yaml      # NEW: Registry storage
│   └── skill-usage.yaml         # ENHANCE: Add effectiveness tracking
└── prompts/
    └── ralf-executor.md         # UPDATE: Add Step 2.5 enhancement

operations/.docs/
└── skill-marketplace-guide.md   # NEW: User guide
```

### Data Schemas

**skill-registry.yaml:**
```yaml
registry_version: "1.0.0"
last_updated: "2026-02-01T14:35:00Z"
skills:
  - name: bmad-pm
    version: "1.0.0"
    domain: "Product Management"
    author: "John"
    description: "Product Manager - PRD creation and requirements"
    tags: ["prd", "requirements", "product", "feature"]
    created_at: "2026-01-01T00:00:00Z"
    effectiveness_score: 0.85
    usage_count: 12
    last_used: "2026-02-01T14:00:00Z"
```

---

## Implementation Plan

### Phase 1: Core Registry (P0)
- [ ] Create skill_registry.py with register, search, get, list functions
- [ ] Create skill-registry.yaml storage schema
- [ ] Implement skill metadata dataclass
- [ ] Write tests for registry functions

### Phase 2: Versioning (P0)
- [ ] Create skill_versioning.py with semantic versioning
- [ ] Implement version parsing, comparison, compatibility check
- [ ] Add breaking change detection
- [ ] Write tests for versioning functions

### Phase 3: Recommendation Engine (P0)
- [ ] Create skill_recommender.py with pattern matching
- [ ] Implement keyword extraction from tasks
- [ ] Implement confidence calculation
- [ ] Add top-N recommendation function
- [ ] Write tests for recommendation engine

### Phase 4: Integration (P0)
- [ ] Update executor prompt (Step 2.5 enhancement)
- [ ] Integrate recommendation engine into executor workflow
- [ ] Test end-to-end skill recommendation
- [ ] Verify confidence threshold works correctly

### Phase 5: Documentation (P1)
- [ ] Create skill-marketplace-guide.md
- [ ] Document skill contribution workflow
- [ ] Add CLI usage examples
- [ ] Create API reference

### Phase 6: Enhancement (P1)
- [ ] Implement skill effectiveness tracking
- [ ] Add CLI interface (python -m skill_registry)
- [ ] Create skill contribution script
- [ ] Add auto-update on skill load

---

## Rollout Plan

### Step 1: Deploy to Executor (Loop 59)
- Add skill marketplace libraries to codebase
- Update executor prompt with Step 2.5 enhancement
- Test with existing tasks (should not break)

### Step 2: Populate Registry (Loop 59)
- Scan existing skills in `2-engine/.autonomous/skills/`
- Auto-register all skills with metadata
- Initialize skill-registry.yaml

### Step 3: Monitor Recommendations (Loops 60-65)
- Track recommendation accuracy (manual review)
- Collect confidence scores
- Adjust algorithm if needed

### Step 4: Iterate Based on Feedback (Loop 66+)
- Refine recommendation algorithm
- Add more metadata fields if needed
- Implement Phase 2 features (effectiveness tracking, CLI)

---

## Testing Strategy

### Unit Tests
- Test skill registry functions (register, search, get, list)
- Test versioning functions (parse, compare, compatibility)
- Test recommendation engine (pattern matching, confidence calculation)

### Integration Tests
- Test end-to-end skill recommendation during task execution
- Test registry persistence (YAML save/load)
- Test version compatibility checks

### Manual Testing
- [ ] Register a new skill: `python -m skill_registry register`
- [ ] Search for skills: `python -m skill_registry search testing`
- [ ] Get recommendations for a task: `python -m skill_recommender analyze <task-file>`
- [ ] Verify executor uses recommendations (check THOUGHTS.md)

### Success Metrics
- Skill discoverability: Time to find skill < 30 seconds
- Recommendation accuracy: > 70% (relevant skills in top-3)
- Skill versioning adoption: > 80% of active skills use semantic versioning

---

## Risks & Mitigations

### Risk 1: Registry Staleness
**Problem:** Registry becomes outdated as skills are added/removed
**Mitigation:** Auto-update registry on skill load, periodic refresh

### Risk 2: Versioning Complexity
**Problem:** Semantic versioning introduces bugs (comparison errors)
**Mitigation:** Simple implementation, extensive tests, deferred dependency resolution

### Risk 3: Poor Recommendation Accuracy
**Problem:** Wrong skills recommended, executor ignores recommendations
**Mitigation:** Start with keyword matching (high precision), evolve to ML later

### Risk 4: Breaking Changes to Executor
**Problem:** Step 2.5 enhancement breaks existing workflow
**Mitigation:** Backwards compatible, recommendations are optional (confidence < 70% → skip)

---

## Future Enhancements

**Phase 2 (P1):**
- Skill effectiveness tracking (success rate per skill)
- CLI interface for marketplace operations
- Skill contribution script (auto-generate skill metadata)

**Phase 3 (P2):**
- Skill dependency management (skills requiring other skills)
- Skill deprecation warnings and lifecycle
- Analytics dashboard (visualization of usage patterns)

**Phase 4 (P2):**
- Machine learning for recommendation accuracy
- Integration with external skill repositories (GitHub-based sharing)
- Community feedback system (ratings, reviews)

---

## Dependencies

**Internal:**
- `skill-usage.yaml` (operations/) - Source of skill metadata
- `2-engine/.autonomous/skills/` - Folder-based skill structure
- `ralf-executor.md` - Executor prompt (Step 2.5 location)

**External:**
- PyYAML - YAML parsing for registry storage
- dataclasses - Data structures

**No Breaking Changes:** This feature enhances, not replaces, existing skill infrastructure.

---

## Open Questions

1. **Q:** Should registry be auto-populated or manual?
   **A:** Auto-populate from existing skills, then manual contributions

2. **Q:** What's the confidence threshold for skill invocation?
   **A:** 70% (matches skill-selection.yaml default)

3. **Q:** Should skills require versioning to be registered?
   **A:** No, default to "1.0.0" if not specified

4. **Q:** How often should effectiveness scores update?
   **A:** After each task completion (auto-update in RESULTS.md processing)

---

## References

- Task File: `.autonomous/tasks/active/TASK-1769955705-implement-feature-f009.md`
- Skill Selection: `operations/skill-selection.yaml`
- Skill Usage: `operations/skill-usage.yaml`
- Existing Skills: `2-engine/.autonomous/skills/`

---

**End of Feature Specification**
