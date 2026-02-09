# Decisions - TASK-1769955705

## Decision 1: YAML-Based Registry Storage

**Context:** Need persistent storage for skill registry with metadata, effectiveness scores, and usage tracking.

**Options Considered:**
1. SQLite database
2. JSON files
3. YAML files
4. PostgreSQL database

**Selected:** YAML files (`skill-registry.yaml`)

**Rationale:**
- **Simplicity:** Human-readable, easy to edit manually if needed
- **Git-friendly:** Changes tracked in version control
- **No dependencies:** PyYAML already in use, no new infrastructure
- **Sufficient scale:** Handles < 1000 skills easily (current: 23)
- **Easy migration:** Can migrate to DB later if needed
- **Backup:** Simple file copy for backup

**Trade-offs:**
- **Pro:** No external dependencies, simple deployment
- **Pro:** Easy to debug (open file in text editor)
- **Pro:** Git tracks all changes automatically
- **Con:** Slower than DB for large datasets (> 10K skills)
- **Con:** No query language (must load entire file)

**Reversibility:** LOW
- Easy to migrate to SQLite/PostgreSQL later
- Schema is well-defined (Skill dataclass)
- Migration script would be straightforward

**Alternatives Rejected:**
- SQLite: More complex infrastructure, overkill for < 1000 skills
- JSON: Less human-readable than YAML, no comments
- PostgreSQL: External dependency, overkill for current scale

---

## Decision 2: Exponential Moving Average for Effectiveness Tracking

**Context:** Need to track skill effectiveness over time, balancing recent performance with historical data.

**Options Considered:**
1. Simple average (successes / total)
2. Exponential moving average (EMA)
3. Weighted moving average (custom weights)
4. Bayesian inference

**Selected:** Exponential Moving Average with alpha=0.3

**Formula:**
```
new_score = alpha * outcome + (1 - alpha) * old_score
```

Where:
- `outcome` = 1.0 for success, 0.0 for failure
- `alpha` = 0.3 (learning rate)
- `old_score` = previous effectiveness score

**Rationale:**
- **Recent performance weighted more heavily:** alpha=0.3 gives 30% weight to latest outcome
- **Smooths one-off failures:** Single failure doesn't tank the score
- **Standard formula:** Well-established in time series analysis
- **Adaptable:** Score converges to true performance over time
- **Simple:** No complex state management

**Example:**
- Initial score: 0.5 (neutral)
- After 1st success: 0.5 * 0.7 + 1.0 * 0.3 = 0.65
- After 2nd success: 0.65 * 0.7 + 1.0 * 0.3 = 0.755
- After 3rd success: 0.755 * 0.7 + 1.0 * 0.3 = 0.8285

**Trade-offs:**
- **Pro:** Adapts to skill improvements/degradations
- **Pro:** Not overly sensitive to one-off failures
- **Pro:** Mathematically sound (standard formula)
- **Con:** Requires tuning alpha (0.3 is reasonable default)
- **Con:** Slower to converge than simple average

**Reversibility:** LOW
- Can adjust alpha based on performance
- Can switch to simple average if EMA doesn't work well
- No data migration needed (both use same inputs)

**Alternatives Rejected:**
- Simple average: Too sensitive to early failures, doesn't adapt
- Weighted moving average: More complex, no clear benefit over EMA
- Bayesian inference: Overkill for this use case

---

## Decision 3: 70% Default Confidence Threshold

**Context:** Need threshold for automatic skill invocation during executor's Step 2.5 (skill checking).

**Options Considered:**
1. 50% (majority)
2. 60% (default)
3. 70% (matches skill-selection.yaml)
4. 80% (high confidence)
5. 90% (very high confidence)

**Selected:** 70% confidence threshold

**Rationale:**
- **Matches existing framework:** skill-selection.yaml uses 70% default
- **Balances automation vs quality:** High enough to avoid false positives, low enough to be useful
- **Empirically validated:** BMAD framework uses this threshold successfully
- **Configurable:** Can be adjusted per task if needed
- **Reasonable confidence:** 70% = "likely correct" without requiring certainty

**Trade-offs:**
- **Pro:** Consistent with existing skill-selection.yaml
- **Pro:** High enough to avoid most false positives
- **Pro:** Low enough for recommendations to be useful
- **Pro:** Configurable (can override per task)
- **Con:** May miss some relevant skills (false negatives)
- **Con:** Requires tuning based on real-world usage

**Reversibility:** LOW
- Threshold is configurable (not hardcoded everywhere)
- Can adjust based on metrics (false positive/negative rates)
- Easy to A/B test different thresholds

**Alternatives Rejected:**
- 50%: Too many false positives (low quality)
- 60%: Lower than skill-selection.yaml default (inconsistent)
- 80%: Too high, may miss useful skills
- 90%: Far too high, recommendations rarely used

---

## Decision 4: Weighted Confidence Calculation

**Context:** Need formula to calculate recommendation confidence based on multiple factors.

**Options Considered:**
1. Equal weights (all factors equal)
2. Keyword-only matching (simple)
3. Machine learning model (complex)
4. Weighted sum (selected)

**Selected:** Weighted sum with custom weights:
- 40% keyword overlap
- 30% domain match
- 20% effectiveness score
- 10% usage frequency

**Rationale:**
- **Keyword overlap is primary signal:** Direct match between task and skill
- **Domain match provides context:** Task type matters (implement vs analyze)
- **Effectiveness ensures quality:** Historical success predicts future success
- **Usage favors proven skills:** Frequently used skills are more reliable
- **Transparent:** Easy to understand and debug
- **Tunable:** Weights can be adjusted based on performance

**Formula:**
```python
confidence = (
    0.40 * keyword_score +
    0.30 * domain_score +
    0.20 * effectiveness_score +
    0.10 * usage_score
)
```

**Trade-offs:**
- **Pro:** Balances multiple signals (not just keywords)
- **Pro:** Transparent (can explain why skill was recommended)
- **Pro:** Tunable (adjust weights based on metrics)
- **Pro:** Simple (no ML model needed)
- **Con:** Requires weight tuning
- **Con:** Linear combination may miss interactions

**Reversibility:** LOW
- Weights are configurable (stored in `SkillRecommender.weights`)
- Can adjust based on A/B testing
- Can switch to ML model if needed (Phase 3)

**Alternatives Rejected:**
- Equal weights: Doesn't prioritize keyword match (most important signal)
- Keyword-only: Ignores quality (effectiveness) and context (domain)
- ML model: Overkill for MVP, requires training data and infrastructure

---

## Decision 5: Semantic Versioning (MAJOR.MINOR.PATCH)

**Context:** Need versioning scheme for skills that prevents breaking changes while allowing evolution.

**Options Considered:**
1. Calendar versioning (YYYY.MM.DD)
2. Sequential versioning (1, 2, 3...)
3. Semantic versioning (MAJOR.MINOR.PATCH)
4. Custom scheme

**Selected:** Semantic Versioning (semver.org standard)

**Format:** `MAJOR.MINOR.PATCH`
- MAJOR: Incompatible API changes
- MINOR: New functionality (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

**Examples:**
- `1.0.0` → `1.0.1` (PATCH): Bug fix
- `1.0.0` → `1.1.0` (MINOR): New feature
- `1.0.0` → `2.0.0` (MAJOR): Breaking changes

**Compatibility Rule:**
- MAJOR must match exactly (prevents breaking changes)
- MINOR can be greater or equal (new features OK)
- PATCH can be greater or equal (bug fixes OK)

**Rationale:**
- **Industry standard:** Widely adopted (npm, Python, Go, etc.)
- **Clear semantics:** Version number communicates impact
- **Compatibility checking:** Easy to implement (MAJOR match)
- **Prevents breakage:** MAJOR mismatch = incompatible
- **Well-documented:** semver.org has clear specification

**Trade-offs:**
- **Pro:** Clear communication (developers understand version numbers)
- **Pro:** Compatibility checking (prevent breaking changes)
- **Pro:** Industry standard (low learning curve)
- **Pro:** Tooling support (libraries for parsing/comparison)
- **Con:** Requires discipline (developers must follow convention)
- **Con:** Can be confusing for beginners (what's a "breaking change"?)

**Reversibility:** LOW
- Standard is well-established (unlikely to change)
- Can migrate to calendar versioning if needed (straightforward)
- Compatibility logic is isolated in skill_versioning.py

**Alternatives Rejected:**
- Calendar versioning: Doesn't communicate breaking changes clearly
- Sequential versioning: No compatibility information
- Custom scheme: Non-standard, harder to understand

---

## Decision 6: Auto-Population from skills/ Directory

**Context:** Need to register existing skills in the marketplace without manual data entry.

**Options Considered:**
1. Manual registration (enter each skill by hand)
2. Auto-population from skills/ directory
3. Import from skill-usage.yaml
4. Web scraping (external repositories)

**Selected:** Auto-population from skills/ directory

**Implementation:**
- Scan `2-engine/.autonomous/skills/` for subdirectories
- Look for `SKILL.md` or `skill.md` in each directory
- Extract metadata from YAML frontmatter (description, agent, role)
- Register skill with default values (version="1.0.0", tags=[])

**Rationale:**
- **Zero manual effort:** 23 skills auto-registered in seconds
- **Leverages existing structure:** Skills already organized in folders
- **Incremental enhancement:** Users can improve metadata over time
- **Idempotent:** Can re-run to update registry
- **Fallback:** Manual registration still available via register_skill()

**Trade-offs:**
- **Pro:** Immediate value (23 skills registered on first run)
- **Pro:** No manual data entry (error-prone, tedious)
- **Pro:** Uses existing file structure (no new convention)
- **Pro:** Enhanceable (users can improve metadata later)
- **Con:** Initial metadata is sparse (tags empty, domains extracted)
- **Con:** Requires skills to follow folder structure (already true)

**Reversibility:** LOW
- Manual registration always available
- Can re-run auto-populate to refresh
- Registry can be edited manually (YAML file)

**Alternatives Rejected:**
- Manual registration: Too tedious (23 skills × 5 minutes = 2 hours)
- Import from skill-usage.yaml: Different schema, incomplete data
- Web scraping: Overkill, no external repositories yet

---

## Decision 7: CLI Interfaces for All Libraries

**Context:** Need user-friendly interfaces for common operations (search, compare, recommend).

**Options Considered:**
1. Python API only (library usage)
2. Web UI (dashboard)
3. CLI interfaces (command line)
4. REST API

**Selected:** CLI interfaces using `python -m` pattern

**Implementation:**
- `python -m lib.skill_registry` (search, list, get, auto-populate)
- `python -m lib.skill_versioning` (compare, compatible, increment, validate, next)
- `python -m lib.skill_recommender` (analyze, recommend)

**Rationale:**
- **Immediate usability:** No need to write Python code for common tasks
- **Low overhead:** Uses existing Python runtime (no new dependencies)
- **Scriptable:** Easy to use in shell scripts and automation
- **Fast development:** ~50 lines per CLI (simple argument parsing)
- **Documentation-friendly:** CLI examples are easy to understand

**Trade-offs:**
- **Pro:** No installation (uses existing Python)
- **Pro:** Scriptable (can use in bash scripts)
- **Pro:** Fast to develop (no web framework needed)
- **Pro:** Low overhead (no web server)
- **Con:** Less discoverable than web UI
- **Con:** Requires terminal usage (not GUI-friendly)

**Reversibility:** LOW
- Python API still available (CLI is thin wrapper)
- Can add web UI later (Phase 2: analytics dashboard)
- Can add REST API later (Phase 3: external repositories)

**Alternatives Rejected:**
- Python API only: Less accessible (requires writing code)
- Web UI: Overkill for MVP (requires framework, hosting)
- REST API: Overkill for local operations (no network needed)

---

## Decision 8: Domain Keyword Mappings

**Context:** Need to map task keywords to skill domains for recommendation scoring.

**Options Considered:**
1. No domain mapping (keyword-only matching)
2. Manual domain mapping (hardcoded lists)
3. ML-based classification
4. Taxonomy/ontology

**Selected:** Manual domain mapping with 8 predefined domains

**Domains:**
1. Product Management (PM)
2. Architecture & Design
3. Implementation
4. Testing
5. Analysis
6. Documentation
7. Process
8. UX

**Keywords per domain:** 10-15 representative keywords

**Rationale:**
- **Improves accuracy:** Domain match provides context beyond keywords
- **Simple:** Hardcoded lists, easy to understand and debug
- **Extensible:** Can add more domains/keywords as needed
- **Transparent:** Clear why a task matches a domain
- **Fast:** No ML model inference required

**Trade-offs:**
- **Pro:** Improves recommendation accuracy (30% weight in confidence)
- **Pro:** Easy to maintain (add keywords to lists)
- **Pro:** Transparent (can explain domain matches)
- **Pro:** Fast (simple string matching)
- **Con:** Manual maintenance (add keywords for new patterns)
- **Con:** Brittle (misses synonyms not in lists)

**Reversibility:** LOW
- Domain lists are easily edited
- Can migrate to ML-based classification (Phase 3)
- System works without domain mapping (just lower accuracy)

**Alternatives Rejected:**
- No domain mapping: Loses 30% of confidence signal
- ML-based classification: Overkill for MVP (requires training data)
- Taxonomy/ontology: Over-engineered for 23 skills

---

## Summary of Decisions

| Decision | Selection | Reversibility | Rationale |
|----------|-----------|---------------|-----------|
| Storage | YAML files | LOW | Simple, git-friendly, no dependencies |
| Effectiveness | EMA (α=0.3) | LOW | Adapts to performance, smooths failures |
| Threshold | 70% | LOW | Matches skill-selection.yaml, balanced |
| Confidence | Weighted sum | LOW | Transparent, tunable, multi-factor |
| Versioning | Semver | LOW | Industry standard, prevents breakage |
| Population | Auto from skills/ | LOW | Zero manual effort, immediate value |
| Interface | CLI | LOW | Fast to develop, scriptable |
| Domains | Manual mapping | LOW | Improves accuracy, transparent |

**All decisions are LOW reversibility** - easy to change or migrate if needed based on real-world usage.

---

**End of Decisions**
