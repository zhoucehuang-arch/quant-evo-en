# Discussion & Deliberation Rules

This document defines all structured discussion, debate, reflection, and escalation mechanisms across both systems.

---

## 1. System A: Extended Debate Protocol

### 1.1 Standard Debate (2 Rounds) — Unchanged
The default micro-cycle debate remains 2 rounds as defined in `orchestration.md`.

### 1.2 REVISE Workflow (Post-Verdict Branch)

When Evolver issues a `REVISE` verdict, the following workflow activates:

```
Evolver VERDICT (REVISE)
    │
    ├── Evolver posts REVISE_REQUEST to #a-arena with:
    │   - specific_issues: what needs fixing
    │   - suggested_direction: hints for improvement
    │   - max_revision_rounds: 1 (default)
    │
    ▼
Explorer reads REVISE_REQUEST → produces REVISED_HYPOTHESIS (within 15min)
    │
    ▼
Critic performs abbreviated assessment (1 round, 10min) → RISK_ASSESSMENT (revision)
    │
    ▼
Evolver issues FINAL_VERDICT:
    - APPROVE → proceed to backtest
    - REJECT → record to memory/reflections/, move on
    - (No second REVISE allowed — prevents infinite loops)
```

**REVISE_REQUEST schema:**
```json
{
  "type": "REVISE_REQUEST",
  "hypothesis_id": "hyp_YYYYMMDD_HHMM",
  "specific_issues": ["Issue 1", "Issue 2"],
  "suggested_direction": "Consider adjusting...",
  "max_revision_rounds": 1,
  "deadline_min": 15
}
```

**Time budget:** REVISE adds ~30min to the cycle. If the cycle would exceed 2.5h total, skip REVISE and force REJECT.

### 1.3 Dynamic Round Extension

In rare cases where both sides present strong but conflicting evidence, Evolver may extend the debate:

**Trigger condition:** Both `alpha_argument_score` and `risk_argument_score` are between 0.55-0.75 (genuine uncertainty).

**Extension rules:**
- Evolver posts `EXTEND_DEBATE` to `#a-arena` with `extra_rounds: 1`
- Explorer and Critic each get one additional exchange (Round 3)
- Maximum total rounds: 3 (hard cap)
- Extension adds ~20min to the cycle

### 1.4 Convergence Criteria
A debate ends when ANY of these conditions are met:
1. Fixed round count reached (2 standard, 3 if extended)
2. Critic's confidence exceeds 0.85 in either direction (clear signal)
3. Explorer concedes (publishes `CONCEDE` instead of `REBUTTAL`)
4. Timeout (20min + 10min grace per agent)

---

## 2. System A: Reflection & Learning Loops

### 2.1 Principle Synthesis (Daily — Evolver's Responsibility)

During the daily cycle, Evolver performs a reflection synthesis:

```
1. Read all entries in memory/causal/ from the past 24h
2. Read all entries in memory/reflections/ from the past 24h
3. Identify recurring patterns (≥3 similar failures = pattern)
4. Synthesize into a new principle or update existing one
5. Write to memory/principles/ with evidence count and confidence
6. Post synthesis summary to #a-report
```

**Principle format:**
```json
{
  "principle_id": "prin_NNN",
  "statement": "Momentum strategies underperform in low-VIX regimes",
  "evidence_count": 5,
  "confidence": 0.78,
  "source_reflections": ["ref_001", "ref_003", "ref_005"],
  "created": "ISO8601",
  "last_validated": "ISO8601"
}
```

### 2.2 Critic Threshold Adaptation (Weekly)

During the weekly cycle, Evolver reviews Critic's performance:

```
1. Count: how many REJECT verdicts were later proven wrong
   (strategy was re-proposed with minor changes and succeeded)
2. Count: how many APPROVE verdicts led to backtest failures
3. If false-negative rate > 30%: suggest Critic lower thresholds by 10%
4. If false-positive rate > 40%: suggest Critic raise thresholds by 10%
5. Post adaptation recommendation to #a-arena as THRESHOLD_REVIEW
6. Critic reads and adjusts internal thresholds for next week
```

### 2.3 Meta-Reflection (Weekly — Part of Weekly Cycle)

Evolver generates a meta-reflection analyzing the debate process itself:

```json
{
  "type": "META_REFLECTION",
  "period": "YYYY-Www",
  "total_debates": 84,
  "verdict_distribution": { "APPROVE": 25, "REJECT": 45, "REVISE": 14 },
  "avg_debate_quality": 0.72,
  "explorer_win_rate": 0.30,
  "critic_override_rate": 0.15,
  "recommendations": ["Explorer should diversify research sources", "..."]
}
```

---

## 3. System A: Weekly Architecture Debate

### 3.1 Format
- **Trigger:** Saturday 15:00 UTC, special `CYCLE_TRIGGER` with `mode: "architecture"`
- **Participants:** All three agents (Explorer proposes, Critic challenges, Evolver arbitrates)
- **Scope:** System-level improvements, NOT individual strategy parameters
  - Examples: new data sources, new strategy archetypes, memory structure changes, risk model upgrades
- **Rounds:** 2 standard rounds (same as micro-cycle debate)
- **Output:** `ARCHITECTURE_VERDICT` with actionable items

### 3.2 Architecture Verdict Schema
```json
{
  "type": "ARCHITECTURE_VERDICT",
  "period": "YYYY-Www",
  "proposals_evaluated": 3,
  "approved_changes": [
    {
      "change_id": "arch_NNN",
      "description": "Add sentiment analysis data source",
      "priority": "high | medium | low",
      "implementation_notes": "...",
      "assigned_to": "explorer | evolver"
    }
  ],
  "deferred": ["..."],
  "rejected": ["..."]
}
```

---

## 4. System B: Deliberation Mechanisms

### 4.1 Strategy Deployment Deliberation

When Operator detects a new strategy in `staging/`, instead of unilateral deployment:

```
Operator: POST DEPLOY_PROPOSAL to #b-ops
    │
    ├── strategy_id, backtest_metrics, risk_profile
    │
    ▼
Guardian: Reviews risk profile within 10min
    │
    ├── DEPLOY_REVIEW to #b-ops:
    │   - risk_assessment: "acceptable | elevated | excessive"
    │   - concerns: [list]
    │   - recommended_position_limit: X%
    │
    ▼
Trader: Reviews executability within 10min
    │
    ├── DEPLOY_REVIEW to #b-ops:
    │   - executability: "ready | needs_adjustment"
    │   - liquidity_concern: true/false
    │   - suggested_order_type: "market | limit"
    │
    ▼
Operator: Synthesizes reviews → DEPLOY_DECISION
    - All clear → deploy with agreed parameters
    - Guardian "excessive" → reject, feedback to System A
    - Trader "needs_adjustment" → deploy with modified params
    - Disagreement → escalate to admin
```

### 4.2 WARNING Response Deliberation

When Guardian issues a WARNING (not HALT):

```
Guardian: WARNING alert to #b-risk
    │
    ▼
Operator: Reads WARNING, posts RISK_DISCUSSION to #b-ops
    │
    ├── proposed_action: "reduce_exposure | hold | monitor"
    │
    ▼
Guardian: Responds with risk projection (10min)
    │
    ├── If risk is increasing → recommend reduce
    │   If risk is stable → recommend monitor
    │
    ▼
Trader: Confirms execution feasibility
    │
    ▼
Operator: Final decision → execute or continue monitoring
```

### 4.3 Strategy Promotion Deliberation

Before promoting a strategy from staging to production:

```
Operator: POST PROMOTION_PROPOSAL to #b-ops
    │
    ├── strategy_id, paper_trading_metrics (5+ days)
    │
    ▼
Guardian: Reviews live risk metrics → PROMOTION_REVIEW
Trader: Reviews execution quality → PROMOTION_REVIEW
    │
    ▼
Operator: PROMOTION_DECISION
    - Both approve → promote to production/
    - Either objects → extend validation period by 3 days
    - Strong objection → reject, feedback to System A
```

---

## 5. Human Escalation Rules

### 5.1 Automatic Escalation Triggers

The system escalates to admin (via `#admin`) when:

| Condition | System | Escalation Action |
|---|---|---|
| 3 consecutive timeouts from same agent | A or B | CRITICAL alert + suggest restart |
| REVISE issued 3+ times for same hypothesis | A | Flag as "deadlocked", ask admin |
| Guardian HALT triggered | B | Immediate admin notification |
| Daily P&L exceeds -5% | B | CRITICAL + suggest manual review |
| No successful APPROVE in 24h | A | Suggest admin review research direction |
| Deployment deliberation disagreement | B | Escalate to admin for final call |
| Weekly meta-reflection shows <20% approve rate | A | Suggest system parameter review |

### 5.2 Escalation Message Format
```json
{
  "type": "ESCALATION",
  "level": "ATTENTION | DECISION_NEEDED | URGENT",
  "system": "A | B",
  "trigger": "Description of what triggered escalation",
  "context": "Relevant data summary",
  "suggested_actions": ["Option 1", "Option 2"],
  "auto_resolution_timeout": "4h (if no response, system takes conservative action)"
}
```

### 5.3 Auto-Resolution
If admin does not respond within 4 hours:
- System A: Continue with conservative defaults (REJECT uncertain hypotheses)
- System B: Reduce exposure by 50%, continue monitoring

---

## 6. Cross-System Discussion (via GitHub + #bridge)

### 6.1 Performance Feedback Loop
When System A reads poor performance data from `trading/metrics/`:

```
Evolver: Detects strategy underperformance
    │
    ▼
Posts PERFORMANCE_FEEDBACK to #bridge:
    - strategy_id
    - expected_vs_actual metrics
    - proposed_adjustment
    │
    ▼
Operator (B): Reads feedback, evaluates
    - Agrees → adjust or withdraw strategy
    - Disagrees → posts counter-evidence to #bridge
    │
    ▼
Evolver (A): Reads counter-evidence in next cycle
    - Incorporates into memory/causal/
```

### 6.2 Strategy Recall Request
If a production strategy consistently underperforms:

```
Guardian: Flags strategy in DAILY_TRADING_REPORT
    │
    ▼
Operator: Posts RECALL_REQUEST to #bridge
    │
    ▼
Evolver (A): Reads in next cycle
    - Marks strategy for re-evaluation
    - Adds to memory/reflections/ with live performance data
```
