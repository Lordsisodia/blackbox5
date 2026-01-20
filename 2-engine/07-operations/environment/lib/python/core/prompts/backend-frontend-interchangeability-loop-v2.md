# Backend↔Frontend Interchangeability + Scalability — V2 (Assumption-Driven Loops)

**Problem with V1:** 50 prompts in one session = exhaustion without validation
**Fix:** 10 separate assumption-validation loops (5 prompts each)

---

## How This Works

Each mini-loop validates **ONE assumption** about the architecture:

1. **Assume** something is true (e.g., "UI doesn't directly access vendors")
2. **Gather evidence** (find files that prove/disprove it)
3. **Make ONE change** to fix it if needed
4. **Measure** if the change helps

After each loop: **STOP**. Decide whether to continue based on what you learned.

---

## The 10 Core Assumptions

### Loop 1: Vendor Boundary Assumption
**Assumption:** UI/domains don't directly access vendor APIs (Shopify, Stripe, etc.)

**What to do:**
- Prompt 1: Search for direct vendor imports (`@shopify/*`, `@stripe/*`, `shopifyClient`, `stripe`)
- Prompt 2: For each finding, trace the call path (UI → vendor vs UI → adapter → vendor)
- Prompt 3: Count violations by file type (components vs services vs adapters)
- Prompt 4: If violations exist, create adapter interface for ONE vendor
- Prompt 5: Measure: Did this reduce direct access? (count before/after)

**Exit criteria:** Direct vendor access quantified, one adapter created if needed

---

### Loop 2: Database Boundary Assumption
**Assumption:** Supabase access is behind a stable interface (not direct UI queries)

**What to do:**
- Prompt 1: Search for `createClient`, `supabase.from`, `@supabase/supabase-js` in UI code
- Prompt 2: Find RLS policy bypasses (`service_role` in client code)
- Prompt 3: Map query patterns (which tables accessed from where)
- Prompt 4: If direct access exists, create ONE API endpoint for a common query
- Prompt 5: Measure: Fewer direct Supabase calls from UI?

**Exit criteria:** Direct DB access mapped, one endpoint created if needed

---

### Loop 3: Tenancy Assumption
**Assumption:** Code doesn't assume single-tenant (no hardcoded tenant IDs)

**What to do:**
- Prompt 1: Search for `storeId`, `organizationId`, `workspaceId` literals
- Prompt 2: Find where context is lost (no tenant in function params)
- Prompt 3: Identify "single tenant" patterns (global state, hardcoded IDs)
- Prompt 4: If issues exist, add tenant context to ONE function call chain
- Prompt 5: Measure: Function chain now tenant-aware?

**Exit criteria:** Tenant assumptions mapped, one function fixed if needed

---

### Loop 4: API Boundary Assumption
**Assumption:** Backend has stable `/api/*` surface (not scattered endpoints)

**What to do:**
- Prompt 1: List all API route definitions (`app.get`, `app.post`, etc.)
- Prompt 2: Categorize by path prefix (`/api/*` vs others)
- Prompt 3: Find endpoints that should be under `/api/*` but aren't
- Prompt 4: If scattered endpoints exist, move ONE to `/api/*` structure
- Prompt 5: Measure: More organized API surface?

**Exit criteria:** API surface mapped, one endpoint reorganized if needed

---

### Loop 5: Error Handling Assumption
**Assumption:** Errors are classified and actionable (not random failures)

**What to do:**
- Prompt 1: Find all `throw new Error`, `res.status(500)`, unhandled rejections
- Prompt 2: Categorize errors (auth, validation, vendor, system)
- Prompt 3: Find unclassified errors (generic messages, no error codes)
- Prompt 4: If unclassified errors exist, add error codes to ONE error path
- Prompt 5: Measure: More debuggable errors?

**Exit criteria:** Error patterns mapped, one error classified if needed

---

### Loop 6: Identifier Boundary Assumption
**Assumption:** Vendor IDs don't leak past adapters (no raw `shopifyProductId` in UI)

**What to do:**
- Prompt 1: Search for `shopifyProductId`, `stripeCustomerId`, `shopifyOrder` in UI code
- Prompt 2: Find where vendor IDs cross adapter boundaries
- Prompt 3: Map which adapters properly hide vendor IDs vs leak them
- Prompt 4: If leaks exist, add ID abstraction to ONE adapter
- Prompt 5: Measure: Fewer exposed vendor IDs?

**Exit criteria:** Vendor ID leaks mapped, one adapter fixed if needed

---

### Loop 7: Performance Assumption
**Assumption:** Critical paths don't have N+1 queries or excessive data fetching

**What to do:**
- Prompt 1: Find database calls in loops (`.map` with DB query, `for` with DB fetch)
- Prompt 2: Identify hot functions (cart, product lists, checkout flows)
- Prompt 3: Count query patterns (single vs batch vs parallel)
- Prompt 4: If N+1 queries exist, batch ONE query pattern
- Prompt 5: Measure: Fewer DB calls?

**Exit criteria:** Performance issues mapped, one query optimized if needed

---

### Loop 8: Security Assumption
**Assumption:** Auth/tenancy checks are at boundaries (not scattered everywhere)

**What to do:**
- Prompt 1: Find auth checks (`requireAuth`, `getUser`, session validation)
- Prompt 2: Map where auth happens (middleware vs route vs function)
- Prompt 3: Find functions that should check auth but don't
- Prompt 4: If missing auth exists, add ONE auth check
- Prompt 5: Measure: More consistent auth?

**Exit criteria:** Auth patterns mapped, one check added if needed

---

### Loop 9: Caching Assumption
**Assumption:** Repeated data is cached (not re-fetched every request)

**What to do:**
- Prompt 1: Find repeated fetches (same query in multiple functions)
- Prompt 2: Identify cacheable data (product lists, config, metadata)
- Prompt 3: Map cache strategy (edge vs API vs client vs none)
- Prompt 4: If uncached repeated data exists, add cache to ONE path
- Prompt 5: Measure: Fewer redundant fetches?

**Exit criteria:** Cache opportunities mapped, one cache added if needed

---

### Loop 10: Observability Assumption
**Assumption:** Failures are diagnosable (logs, metrics, traces exist)

**What to do:**
- Prompt 1: Find silent failures (empty `catch {}`, swallowed errors)
- Prompt 2: Map what gets logged (errors, requests, timing)
- Prompt 3: Identify critical paths with no observability
- Prompt 4: If blind spots exist, add logging to ONE critical path
- Prompt 5: Measure: More observable failures?

**Exit criteria:** Observability gaps mapped, one log added if needed

---

## How to Use This

### Option A: Run All Loops Sequentially
```bash
for loop in {1..10}; do
  echo "Starting Loop $loop..."
  # Run 5 prompts for this loop
  # STOP and review results
  read -p "Continue to next loop? (y/n) " -n 1 -r
  echo
done
```

### Option B: Run High-Value Loops First
Based on Ralph's findings, prioritize:
- Loop 2 (Database Boundary) - P1 issue
- Loop 7 (Performance) - P3 mixed sync/async
- Loop 8 (Security) - Critical path

### Option C: Run One Loop Per Day
```bash
# Day 1: Loop 1 (Vendor Boundary)
# Day 2: Loop 2 (Database Boundary)
# etc.
```

---

## Output Format

Each loop produces:

### 1. `assumption-{N}-findings.md`
```markdown
# Assumption {N}: {title}

## What We Assumed
{original assumption}

## Evidence Gathered
- Found X files that violate this
- Locations: {list}
- Severity: {P1/P2/P3}

## What We Did
{change made, if any}

## Before vs After
- Before: {metric}
- After: {metric}
- Improvement: {X%}

## Validated?
- ✅ ASSUMPTION TRUE (no changes needed)
- ❌ ASSUMPTION FALSE (fixed issue)
- ⚠️ PARTIAL (some issues remain)

## Next Steps
{what to do next, if anything}
```

### 2. `assumption-{N}-change.md` (if changes made)
```markdown
# Change for Assumption {N}

## File Changed
{path}

## What Changed
{diff summary}

## Why This Helps
{rationale}

## How to Verify
{test steps}
```

---

## Why This Is Better Than V1

| V1 (50 prompts) | V2 (10 loops × 5 prompts) |
|-----------------|----------------------------|
| One 6-10h session | Ten 30-60m sessions |
| Exhausting | Manageable |
| No validation until end | Validation after each loop |
| Hard to track progress | Clear progress (10 assumptions) |
| All or nothing | Can stop anytime |
| Theoretical | Evidence-based |

---

## Go/No-Go Gates

After each loop, ask:

1. **Did we learn something new?** (yes → continue, no → skip next)
2. **Is this blocking other work?** (yes → fix now, no → document and defer)
3. **Do we need more research?** (yes → run loop again with different focus, no → move on)

If any answer is "no": **STOP**. Don't run the next loop blindly.

---

## Example Session

```
=== Loop 1: Vendor Boundary ===

Prompt 1: Searching for direct vendor imports...
  Found: src/ui/components/ProductCard.tsx uses @shopify/admin-api
  Found: src/pages/Checkout.tsx uses Stripe()
  Found: src/services/shopifyAdapter.ts (good - this is correct)

Prompt 2: Tracing call paths...
  ProductCard.tsx → directly imports shopify (BAD)
  Checkout.tsx → directly creates Stripe (BAD)
  shopifyAdapter.ts → imports shopify (GOOD - this is the adapter)

Prompt 3: Counting violations...
  UI components: 8 violations
  Services: 1 correct usage
  Adapters: 1 correct usage
  Severity: P2 (not blocking, but should fix)

Prompt 4: Creating adapter interface for ONE vendor...
  Created: src/services/IVendorProduct.ts
  Updated: ProductCard.tsx to use adapter instead of direct import

Prompt 5: Measuring impact...
  Before: 8 direct vendor imports
  After: 7 direct vendor imports (1 fixed)
  Improvement: 12.5% reduction
  Validated: ❌ ASSUMPTION FALSE

=== GO/NO-GATE ===

✅ Did we learn something new? YES - UI directly accesses vendors
✅ Is this blocking? NO - system works, just not ideal
✅ Need more research? NO - pattern is clear

Decision: Continue to next loop

=== Loop 2: Database Boundary ===
...
```

---

## Success Metrics

After running all 10 loops:

- **Assumptions Validated:** 10/10 (100%)
- **Changes Made:** X/10 (measured impact)
- **Architecture Documented:** YES (findings from all loops)
- **Next Priorities:** Clear (based on severity counts)

---

## Template for Each Loop

Copy this for each assumption:

```markdown
# Loop {N}: {assumption title}

## Assumption
{what we believe is true}

## Validation Plan
1. Search for {pattern}
2. Analyze findings
3. Count violations
4. Fix ONE issue if needed
5. Measure impact

## Prompts
1. {search command}
2. {analysis command}
3. {counting command}
4. {fix command}
5. {measure command}

## Exit Criteria
- Evidence gathered: YES/NO
- Changes made: YES/NO
- Impact measured: YES/NO
```

---

**This replaces the original 50-prompt monolith with 10 focused, assumption-driven mini-loops.**
