# Decisions - TASK-1769952154

**Task:** Implement Feature F-004 (Automated Testing Framework)
**Run Number:** 170
**Date:** 2026-02-01

---

## Decision 1: Test Framework Choice (pytest vs unittest)

**Context:**
Need to choose a Python testing framework for RALF. Options include pytest (industry standard), unittest (built-in), and nose2 (deprecated).

**Selected:** pytest

**Rationale:**
- **Industry standard:** pytest is the de facto standard for Python testing
- **Powerful fixture system:** Fixtures are more powerful than unittest setUp/tearDown
- **Excellent assertion introspection:** Clear error messages show exactly what failed
- **Less boilerplate:** Tests are more concise and readable
- **Great plugin ecosystem:** pytest-cov, pytest-mock, pytest-xdist, etc.
- **Community support:** Large community, extensive documentation

**Alternatives Considered:**
1. **unittest:**
   - Pros: Built into Python, no installation needed
   - Cons: Verbose, less powerful, more boilerplate
   - Rejected: Too much ceremony for common cases

2. **nose2:**
   - Pros: Compatible with unittest tests
   - Cons: Deprecated, unmaintained, smaller community
   - Rejected: No longer actively maintained

**Reversibility:** LOW
- Adopting pytest is a long-term commitment
- Migrating from pytest to another framework would be expensive
- **Decision is final** - pytest is the right choice for RALF

---

## Decision 2: Test Structure (Flat vs Nested)

**Context:**
Need to organize test files. Options include flat structure (all tests in tests/) or nested structure (tests/unit/, tests/integration/, tests/fixtures/).

**Selected:** Nested structure (tests/unit/, tests/integration/, tests/fixtures/)

**Rationale:**
- **Clear separation:** Unit tests (fast, isolated) vs integration tests (slower, interactions)
- **Easy to run specific types:** `pytest tests/unit/` for fast feedback
- **Scalable:** Structure scales as test suite grows
- **Industry best practice:** Matches how most large projects organize tests
- **Facilitates test markers:** Natural mapping to pytest markers (@pytest.mark.unit, @pytest.mark.integration)

**Alternatives Considered:**
1. **Flat structure (tests/):**
   - Pros: Simpler, fewer directories
   - Cons: Doesn't scale well, unclear organization, hard to run specific test types
   - Rejected: Would become unmanageable as test suite grows

2. **Component-based structure (tests/config_manager/, tests/roadmap/):**
   - Pros: Groups tests by component
   - Cons: Hard to separate unit from integration, unclear where integration tests go
   - Rejected: Doesn't facilitate test type separation

**Reversibility:** LOW
- Structural change affects all existing tests and future test organization
- Migrating from nested to flat (or vice versa) is expensive
- **Decision is final** - nested structure scales best

---

## Decision 3: Test Utilities Location

**Context:**
Need to decide where to place test utilities (test_utils.py). Options include tests/lib/ (project root), 2-engine/tests/lib/, or lib/tests/.

**Selected:** 2-engine/tests/lib/test_utils.py

**Rationale:**
- **Proximity to tests:** Utilities are close to tests that use them
- **Follows existing structure:** 2-engine/tests/ already exists with some tests
- **Consistent with RALF architecture:** Engine code in 2-engine/, tests in 2-engine/tests/
- **Clear ownership:** Test utilities belong with test infrastructure

**Alternatives Considered:**
1. **tests/lib/ (project root):**
   - Pros: At top level, easy to find
   - Cons: Generic, less clear ownership, mixes with other test dirs
   - Rejected: Less clear organization

2. **lib/tests/ (under lib):**
   - Pros: Near production code
   - Cons: Mixes test and production code, unconventional
   - Rejected: Violates separation of concerns

**Reversibility:** MEDIUM
- Can move lib/ directory if needed
- Python path updates would be required in all test files
- Moderate effort to relocate (~30 minutes)
- **Decision is likely final** - location makes sense

---

## Decision 4: Coverage Target (40% vs 60% vs 80%)

**Context:**
Need to set test coverage target for MVP. Options include 40% (critical paths only), 60% (good coverage), or 80% (comprehensive).

**Selected:** 40-50% for MVP (critical paths only)

**Rationale:**
- **Focus on high-value tests:** Test critical libraries (ConfigManager, RoadmapSync) first
- **Avoid diminishing returns:** Last 20% of coverage costs 80% of effort
- **Enable iterative improvement:** Can increase coverage over time
- **Realistic for 2-hour budget:** 40-50% achievable in MVP timeframe
- **Quality over quantity:** Better to have 40% of excellent tests than 80% of brittle tests

**Alternatives Considered:**
1. **80% coverage:**
   - Pros: Comprehensive coverage, high confidence
   - Cons: Too ambitious for MVP, delays feature delivery, diminishing returns
   - Rejected: Would take 6+ hours, not realistic for quick win

2. **60% coverage:**
   - Pros: Good coverage, balance between effort and benefit
   - Cons: Still ambitious for MVP timeline
   - Rejected: Target for next phase, not MVP

**Reversibility:** LOW (for target), HIGH (for implementation)
- Coverage target is a goal, not a hard constraint
- Can increase target over time (40% → 60% → 80%)
- Tests written for 40% target still valuable at 80%
- **Decision is flexible** - target can be increased

---

## Decision 5: Mock Strategy (pytest-mock vs unittest.mock)

**Context:**
Need to choose a mocking strategy. Options include pytest-mock (mocker fixture) or unittest.mock (Mock, patch).

**Selected:** pytest-mock (mocker fixture)

**Rationale:**
- **Cleaner API:** mocker.patch() is cleaner than mock.patch()
- **Better pytest integration:** mocker fixture is native to pytest
- **Easier to read:** Less verbose, more Pythonic
- **Automatic cleanup:** Mocks automatically undone after test
- **Consistency:** Use pytest throughout, why not for mocking too?

**Alternatives Considered:**
1. **unittest.mock:**
   - Pros: Built into Python standard library
   - Cons: Verbose, less Pythonic, manual cleanup required
   - Rejected: pytest-mock is superior in every way except stdlib inclusion

2. **No mocking (use real objects):**
   - Pros: Simpler, no learning curve
   - Cons: Slower tests, external dependencies, brittle tests
   - Rejected: Mocking is essential for fast, isolated tests

**Reversibility:** MEDIUM
- Can migrate from pytest-mock to unittest.mock if needed
- Would require updating all mock calls (~10-20 tests affected)
- Moderate effort to switch (~1 hour)
- **Decision is likely final** - pytest-mock is superior

---

## Decision 6: Test Discovery Strategy (Explicit vs Implicit)

**Context:**
Need to decide how tests are discovered. Options include explicit test lists (slow) or pytest's automatic discovery (fast).

**Selected:** pytest's automatic discovery

**Rationale:**
- **Zero configuration:** pytest automatically finds test_*.py files
- **Convention over configuration:** Follow naming conventions, tests are discovered
- **Fast:** No manual test list maintenance
- **Industry standard:** How pytest is designed to be used
- **Scalable:** New test files automatically included

**Alternatives Considered:**
1. **Explicit test lists:**
   - Pros: Explicit control over what tests run
   - Cons: Manual maintenance, doesn't scale, error-prone
   - Rejected: Too much overhead for no benefit

**Reversibility:** LOW
- Switching from automatic to explicit discovery is easy
- Switching from explicit to automatic is tedious
- **Decision is final** - automatic discovery is correct choice

---

## Decision 7: Fixture Granularity (Fine-grained vs Coarse-grained)

**Context:**
Need to decide fixture granularity. Options include fine-grained fixtures (one per attribute) or coarse-grained fixtures (complete objects).

**Selected:** Mixed approach (both fine and coarse)

**Rationale:**
- **Fine-grained for specific needs:** temp_dir, temp_config_file for custom setups
- **Coarse-grained for common cases:** sample_task, sample_event for ready-to-use objects
- **Flexibility:** Test author chooses right tool for the job
- **Efficiency:** Reuse coarse fixtures when possible, fine-grained when needed

**Alternatives Considered:**
1. **Only fine-grained fixtures:**
   - Pros: Maximum flexibility, test author has full control
   - Cons: Verbose, repetitive, test setup is lengthy
   - Rejected: Too much boilerplate

2. **Only coarse-grained fixtures:**
   - Pros: Concise, quick test setup
   - Cons: Inflexible, can't customize when needed
   - Rejected: Doesn't handle edge cases

**Reversibility:** LOW
- Can add more fixtures of either granularity
- Fixtures are additive, not mutually exclusive
- **Decision is final** - mixed approach is best

---

## Decision 8: Test Runner Implementation (Reuse vs Create New)

**Context:**
Need to decide whether to reuse existing test runner (bin/run-tests.sh from F-007) or create a new one.

**Selected:** Reuse existing test runner

**Rationale:**
- **Already exists:** bin/run-tests.sh from F-007 is comprehensive
- **Feature overlap:** F-007 (CI/CD) already delivered test runner
- **Accelerates delivery:** Saves ~15 minutes of implementation time
- **Consistency:** Single test runner for all testing needs
- **Tested:** Existing runner is already validated

**Alternatives Considered:**
1. **Create new test runner:**
   - Pros: Customized for F-004 needs
   - Cons: Duplicate effort, maintenance burden, confusion (which runner to use?)
   - Rejected: Unnecessary duplication

**Reversibility:** MEDIUM
- Could create new runner if F-004 needs diverge significantly
- Would cause confusion (two runners for same purpose)
- **Decision is final** - reuse is correct approach

---

## Summary of Decisions

| Decision | Choice | Reversibility | Rationale |
|----------|--------|---------------|-----------|
| 1. Test Framework | pytest | LOW | Industry standard, powerful, less boilerplate |
| 2. Test Structure | Nested | LOW | Scalable, clear separation, industry practice |
| 3. Utilities Location | 2-engine/tests/lib/ | MEDIUM | Proximity to tests, follows existing structure |
| 4. Coverage Target | 40-50% | LOW (target) HIGH (impl) | Focus on high-value, avoid diminishing returns |
| 5. Mock Strategy | pytest-mock | MEDIUM | Cleaner API, better pytest integration |
| 6. Test Discovery | Automatic | LOW | Zero config, convention over configuration |
| 7. Fixture Granularity | Mixed | LOW | Flexibility for all use cases |
| 8. Test Runner | Reuse existing | MEDIUM | Already exists, accelerates delivery |

**Overall Approach:** Use industry standards (pytest), follow best practices (nested structure, automatic discovery), leverage existing infrastructure (test runner, testing guide), and focus on high-value tests (40-50% coverage, critical paths only).

---

**End of Decisions**
