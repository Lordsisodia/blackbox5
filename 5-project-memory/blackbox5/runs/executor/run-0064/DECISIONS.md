# Decisions - TASK-1769958231

## Decision 1: YAML Storage vs SQLite for Time-Series Data

**Context:** Need to store performance metrics from 1000+ runs for historical analysis and trend detection.

**Options:**
1. **YAML files** - Human-readable, no dependencies, simple
2. **SQLite** - ACID compliant, efficient queries, standard database

**Selected:** YAML files

**Rationale:**
- **Simplicity:** YAML files require no additional dependencies or database setup
- **Human-readable:** Easy to inspect and debug metrics data manually
- **Sufficient performance:** At ~1KB per run, 1000 runs = ~1MB, which is trivial for YAML
- **Easy migration:** Can migrate to SQLite later if performance issues arise
- **Portable:** Single file format, easy to backup and transfer

**Trade-offs:**
- **Pros:** Simple, readable, no dependencies, easy to debug
- **Cons:** Slower for large datasets (> 10,000 runs), no SQL queries

**Reversibility:** HIGH - Can migrate to SQLite by writing a simple migration script. Data structure is flat and well-defined.

**Evidence from feature spec:** "Start with YAML files (simpler, human-readable). Migrate to SQLite if performance issues at 1000+ runs."

---

## Decision 2: Hybrid Anomaly Detection (Statistical + Rule-Based)

**Context:** Need to detect performance anomalies (slowdowns, errors, bottlenecks) in RALF runs.

**Options:**
1. **Statistical only** - Z-score, IQR, percentiles
2. **Rule-based only** - Fixed thresholds (e.g., duration > 10 minutes)
3. **Hybrid** - Combine both approaches

**Selected:** Hybrid (Statistical + Rule-Based)

**Rationale:**
- **Statistical detection** catches outliers relative to baseline (e.g., 3σ from mean)
- **Rule-based detection** catches absolute violations (e.g., duration > 10 minutes)
- **Combined coverage:** Different failure modes detected by different methods
- **Reduced false positives:** Both methods must agree for critical alerts
- **Flexibility:** Can tune each method independently

**Implementation:**
- **Statistical:** Z-score > 3.0 (critical), > 2.5 (warning)
- **Rule-based:** Duration > 2x baseline average (critical), > 1.5x (warning)
- **Severity classification:** critical, warning, info

**Reversibility:** MEDIUM - Can adjust thresholds or disable one method via config. Core architecture supports both.

**Validation:** Detected 1 critical duration anomaly in 48 runs (2% anomaly rate, reasonable).

---

## Decision 3: Alert Channels: Log + Dashboard (No Webhook Initially)

**Context:** Need to notify operators when anomalies detected or thresholds exceeded.

**Options:**
1. **Log file only** - Simple, always available
2. **Dashboard only** - Real-time visibility
3. **Log + Dashboard** - Redundant, comprehensive
4. **Log + Dashboard + Webhook** - Full integration (Slack, Discord, email)

**Selected:** Log + Dashboard (Webhook infrastructure in place, disabled by default)

**Rationale:**
- **Log file:** Always available, no setup required, works offline
- **Dashboard:** Real-time visibility, integrates with F-008, already working via events.yaml
- **Webhook:** Future enhancement (need endpoint configuration, error handling)
- **Incremental rollout:** Start simple, add webhook when needed

**Implementation:**
- **Log channel:** Python logging (INFO, WARNING, ERROR)
- **Dashboard channel:** Write to events.yaml (already consumed by F-008 dashboard)
- **Webhook channel:** Stub implementation, configurable URL

**Reversibility:** HIGH - Channels are configurable in alert-config.yaml. Can enable/disable independently.

**User impact:** Operators see alerts in dashboard and logs immediately. Webhook can be enabled later for Slack/Discord.

---

## Decision 4: Retention Policy: 1000 Runs

**Context:** How much historical data to keep for performance monitoring.

**Options:**
1. **100 runs** - ~1 week of data
2. **500 runs** - ~3-5 days of data
3. **1000 runs** - ~1-2 weeks of data
4. **Unlimited** - Keep all data

**Selected:** 1000 runs (configurable)

**Rationale:**
- **Storage cost:** At ~1KB per run, 1000 runs = ~1MB (negligible)
- **Analysis value:** 1000 runs provides sufficient baseline for statistical analysis
- **Time coverage:** At current velocity (0.32 runs/hour), 1000 runs = ~50 days of data
- **Performance:** YAML can handle 1000+ records without performance issues
- **Configurable:** Can increase/decrease via alert-config.yaml if needed

**Trade-offs:**
- **Pros:** Sufficient data for trends, minimal storage, fast queries
- **Cons:** Limited long-term historical analysis (e.g., month-over-month)

**Reversibility:** HIGH - Just change `max_metrics_records` in alert-config.yaml. No code changes needed.

**Future enhancement:** Implement archival system for older data (compress or migrate to cold storage).

---

## Decision 5: Report Formats: Markdown + JSON + CSV

**Context:** Generate performance reports for different use cases (human reading, automation, spreadsheets).

**Options:**
1. **Markdown only** - Human-readable
2. **JSON only** - Machine-readable
3. **Markdown + JSON** - Cover both human and machine
4. **Markdown + JSON + CSV** - Cover all use cases

**Selected:** Markdown + JSON + CSV

**Rationale:**
- **Markdown:** Ideal for human reading, GitHub display, documentation
- **JSON:** Ideal for APIs, automation, custom analysis tools
- **CSV:** Ideal for spreadsheets, Excel, business users
- **Comprehensive coverage:** All major use cases addressed
- **Minimal overhead:** Only 3 formats, easy to maintain

**Implementation:**
- **Daily/Weekly reports:** Markdown + JSON generated automatically
- **Custom reports:** User selects format via `--format` flag
- **Export:** CSV export for spreadsheet analysis

**Reversibility:** LOW - Would need to remove format generators. But no downside to supporting all 3.

**User benefit:** Users can choose format based on their needs (executives → Markdown, engineers → JSON, analysts → CSV).

---

## Decision 6: Alert Threshold Defaults

**Context:** Set default thresholds for alerting to avoid false positives while catching real issues.

**Parameters:**
- Duration: critical_seconds, warning_seconds
- Success rate: critical_percent, warning_percent
- Queue depth: critical, warning
- Agent timeout: seconds

**Selected Thresholds:**

| Metric | Critical | Warning | Rationale |
|--------|----------|---------|-----------|
| Duration | 600s (10 min) | 300s (5 min) | Based on observed data (avg 11324s is outlier) |
| Success Rate | 50% | 80% | 95% is typical (93.8% observed), 80% = warning |
| Queue Depth | 0 (empty) | 2 (low) | Queue should have 3-5 tasks ideally |
| Agent Timeout | 120s (2 min) | N/A | Heartbeat every 30s, 120s = 4 missed beats |

**Rationale:**
- **Duration:** Most runs complete in 300-600s. 600s = clearly slow. 300s = worth investigating.
- **Success rate:** 93.8% observed. 80% = significant drop. 50% = critical issue.
- **Queue depth:** 3-5 tasks is healthy. 2 = low. 0 = empty (executor idle).
- **Agent timeout:** Heartbeat every 30s. 120s = 4 missed heartbeats = likely dead.

**Reversibility:** HIGH - All thresholds configurable in alert-config.yaml. No code changes needed.

**Validation:** With these thresholds, 1 critical alert in 48 runs (2% alert rate). Reasonable false positive rate.

---

## Decision 7: BMAD Skill Selection (bmad-dev at 90% confidence)

**Context:** Task requires implementing 5 new libraries for performance monitoring system.

**Skill Evaluation:**
- **bmad-dev:** Implementation, coding, testing (confidence: 90%)
- **bmad-analyst:** Research, analysis (confidence: 60%)
- **bmad-architect:** System design (confidence: 40%)

**Selected:** bmad-dev

**Confidence Calculation:**
- Keyword match: 40% (task type = "implement")
- Type alignment: 30% (coding task)
- Complexity fit: 20% (medium-high complexity)
- **Total: 90%**

**Rationale:**
- **Implementation task:** Creating 5 new libraries with ~2,360 lines of code
- **Clear requirements:** Feature spec provides detailed implementation guide
- **Testing needed:** All libraries must be tested and validated
- **bmad-dev workflow:** DS (Develop Story) is perfect fit

**Reversibility:** N/A - Skill choice influences execution approach, not reversible. But confidence was high (90%), so low risk.

**Outcome:** Successful execution following DS workflow. All components delivered and validated.

---

## Summary of Key Decisions

| Decision | Selection | Reversibility | Impact |
|----------|-----------|---------------|--------|
| Storage format | YAML files | HIGH | Simple, readable, easy to debug |
| Anomaly detection | Hybrid (statistical + rules) | MEDIUM | Comprehensive coverage |
| Alert channels | Log + Dashboard | HIGH | Immediate visibility |
| Retention policy | 1000 runs | HIGH | Sufficient data, minimal storage |
| Report formats | Markdown + JSON + CSV | LOW | All use cases covered |
| Alert thresholds | Conservative defaults | HIGH | Low false positive rate |
| BMAD skill | bmad-dev (90% confidence) | N/A | Structured execution |

**Overall Approach:** Incremental, conservative, reversible decisions. Start simple, add complexity when needed. Prioritize user experience and operational simplicity.
