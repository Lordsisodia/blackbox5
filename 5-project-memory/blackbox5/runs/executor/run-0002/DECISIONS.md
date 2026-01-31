# Decisions - TASK-1769892001

## Decision 1: Initialize All Metrics to Null/Zero

**Context:** When creating the skill usage tracking file, I had to decide whether to seed with historical data or start fresh.

**Selected:** Initialize all metrics to null/0 for clean baseline

**Rationale:**
1. No reliable historical data exists on actual skill usage
2. Starting fresh ensures accurate tracking from this point forward
3. Historical guesses would introduce bias and inaccuracy
4. Clean baseline makes patterns more obvious over time
5. Null values clearly indicate "no data yet" vs "zero usage"

**Reversibility:** HIGH - Can manually add historical data if needed, but starting clean is preferable for data accuracy

---

## Decision 2: Include Notes Field in Schema

**Context:** The task requirements didn't explicitly ask for a notes field, but qualitative data is valuable.

**Selected:** Added `notes` field to each skill entry

**Rationale:**
1. Quantitative metrics (usage count, success rate) don't tell the whole story
2. Notes can capture context: why a skill failed, what it's good at, known issues
3. Supports the "truth-seeking" philosophy - capture observations, not just numbers
4. Helps identify patterns that pure metrics miss (e.g., "good for X but not Y")
5. Low overhead - optional field, doesn't complicate automated tracking

**Reversibility:** LOW - Removing field would break backward compatibility, but field is harmless if unused

---

## Decision 3: Skill Categorization Structure

**Context:** Needed to organize 25 skills in a way that supports IG-004's goal of optimizing skill usage.

**Selected:** Use 5 categories matching skills/README.md structure (agent, protocol, utility, core, infrastructure)

**Rationale:**
1. Maintains consistency with existing documentation
2. Categories align with skill purposes:
   - agent skills (BMAD team) - Complex multi-step tasks
   - protocol skills - Framework-based workflows
   - utility skills - Specific capabilities (search, nav, db)
   - core skills - System operations (git, state, tasks)
   - infrastructure skills - Cloud/agent spawning
3. Enables category-level analysis (e.g., "are agent skills overused?")
4. Supports consolidation goals by grouping similar skills

**Reversibility:** MEDIUM - Re-categorizing would require updates but is straightforward YAML editing

---

## Decision 4: Integration Guide Embedded in File

**Context:** Task required documentation on how to update tracking. Had to choose between separate doc file or embedded comments.

**Selected:** Embedded comprehensive integration guide in skill-usage.yaml comments

**Rationale:**
1. Documentation co-located with data = harder to get out of sync
2. YAML files are human-readable, comments are standard practice
3. Single source of truth - no need to reference separate file
4. Editors can view guide alongside data structure
5. Supports self-documenting system philosophy

**Reversibility:** LOW - Could extract to separate file, but embedded is more convenient for users

---

## Decision 5: Success Rate Calculation Method

**Context:** Needed to define how success_rate is calculated and updated.

**Selected:** Track as percentage (0-100), calculated as (success_count / total_count) * 100

**Rationale:**
1. Percentage is intuitive and universally understood
2. Enables quick assessment (100% = perfect, 0% = never works, 50% = coin flip)
3. Formula documented in integration guide for consistency
4. Stored value vs calculated: Store to avoid recomputation, update on each execution
5. Aligns with IG-004 success criteria of "lower false-positive rate"

**Reversibility:** LOW - Changing formula would require backfilling all entries, but current approach is standard

---

## Decision 6: Timestamp Format

**Context:** Needed consistent timestamp format for last_used field across all skills.

**Selected:** ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) with UTC timezone

**Rationale:**
1. ISO 8601 is international standard, unambiguous
2. Sortable as strings (chronological order = lexicographical order)
3. Compatible with most programming languages and tools
4. Includes timezone (Z = UTC) for consistency across distributed systems
5. Human-readable while being machine-parseable

**Reversibility:** LOW - Changing format would break sorting/parsing, but ISO 8601 is the correct choice
