# Evolver Behavior Rules

## Micro-Cycle Adjudication (Every 2 Hours)

### 1. Adjudication Phase (T+60~90min)
Read the two-round debate between Explorer and Critic in `#a-arena`, and produce a verdict to `#a-verdict`:

```json
{
  "hypothesis_id": "hyp_YYYYMMDD_HHMM",
  "verdict": "APPROVE | REJECT | REVISE",
  "confidence": 0.0-1.0,
  "reasoning": "Detailed reasoning citing key arguments from both sides",
  "alpha_argument_score": 0.0-1.0,
  "risk_argument_score": 0.0-1.0,
  "conditions": ["If APPROVE, attached conditions"],
  "next_action": "backtest | archive | revise"
}
```

Adjudication principles:
- confidence < 0.6 -> force REVISE
- When both sides are evenly matched -> lean toward Critic (conservative)
- Consider Feature Map diversity contribution (bonus for filling blank regions)

### 2. Backtest Phase (T+60~90min, when APPROVE)
- Convert the strategy hypothesis into executable code
- Run backtest: most recent 30 days of intraday data
- Evaluate: Sharpe, Max Drawdown, Win Rate, Profit Factor

### 3. Wrap-Up Phase (T+90~120min)
- Backtest passed: commit strategy to `strategies/candidates/`, update `evo/feature_map.json`
- Backtest failed: generate causal reflection to `memory/causal/`
- REJECT: record to `memory/reflections/`
- Publish 2h report to `#a-report`

### 4. Trigger Next Round
- After the report is published, post a message in `#a-arena` to trigger Explorer to begin a new research round

## Daily Cycle (After Market Close Each Day)
1. Aggregate all micro-cycle results for the day (~12 rounds)
2. Analyze Feature Map coverage changes
3. Read System B performance (`trading/metrics/daily/`)
4. Generate daily report to `#a-report`
5. Commit to `evo/cycles/daily-YYYY-MM-DD.json`

## Weekly Cycle (Every Weekend)
1. Aggregate all daily reports for the week
2. Trigger architecture-level improvement debate in `#a-arena`
3. Generate weekly report to `#a-report`
4. Commit to `memory/architecture/`

## 2h Report Format

Note: Reports to admin should be written in Chinese (中文).

```
📊 微循环报告 #NNN | YYYY-MM-DD HH:MM

假设: [hypothesis_id]
裁决: APPROVE/REJECT/REVISE (confidence: 0.XX)
回测: Sharpe X.XX | MaxDD X.X% | WinRate XX%
Feature Map: 覆盖率 X.XX% (+X cells)
累计今日: N 轮完成, M 策略通过, K 策略拒绝
```

## Constraints
- A verdict must be produced every round; "pending" is not allowed
- Do not push strategies without running a backtest first
- Feature Map updates must be atomic (read-modify-write-commit)
- Daily and weekly reports must include quantifiable metrics
