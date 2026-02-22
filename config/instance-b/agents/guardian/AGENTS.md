# Guardian Behavior Rules

## Real-Time Monitoring (Every 5 Minutes During Trading Hours)

### Monitoring Metrics and Thresholds

| Metric | Calculation Method | WARNING | CRITICAL | HALT |
|---|---|---|---|---|
| Intraday P&L | Realized + Unrealized | -3% | -5% | -8% |
| Single Strategy DD | Peak to Current | -10% | -15% | -20% |
| Portfolio VaR 95% | Historical Simulation | > 3% | > 5% | > 8% |
| Inter-Strategy Correlation | Rolling 30d | avg > 0.5 | avg > 0.7 | - |
| Position Concentration | Largest Single Asset % | > 8% | > 12% | > 15% |
| Total Exposure | Total Market Value / Net Value | > 70% | > 80% | > 90% |

### Alert Output (Published to `#b-risk`)
```json
{
  "alert_id": "alert_YYYYMMDD_HHMM_NNN",
  "timestamp": "ISO8601",
  "level": "INFO | WARNING | CRITICAL | HALT",
  "metric": "daily_pnl",
  "current_value": -0.032,
  "threshold": -0.03,
  "message": "Intraday P&L has reached -3.2%, approaching CRITICAL",
  "action_required": "none | reduce_exposure | halt_trading",
  "affected_strategies": ["strategy_name_v1"]
}
```

### Alert Level Actions
- **INFO**: Log only, no notification
- **WARNING**: Publish to `#b-risk`, Operator receives notification
- **CRITICAL**: Publish to `#b-risk` + `#b-ops`, require Operator to evaluate exposure reduction
- **HALT**: Publish to `#b-risk` + `#b-desk` + `#b-ops`, Trader stops immediately

### HALT Execution Flow
1. Publish HALT alert to all System B channels
2. Trader cancels all pending orders
3. Wait for Operator or admin to issue RESUME instruction
4. No new trades allowed before RESUME

## Performance Collection

### Real-Time (Every 5 Minutes)
- Read Alpaca account and position data
- Calculate real-time P&L, position distribution
- Write to GitHub `trading/metrics/realtime/`

### Daily Report Data (After Market Close)
- Aggregate all trades for the day
- Calculate daily Sharpe, daily DD, strategy attribution
- Write to GitHub `trading/metrics/daily/YYYY-MM-DD.json`

### Position Snapshot (Hourly)
- Details of all current positions
- Write to GitHub `trading/positions/YYYY-MM-DD-HH.json`

## Constraints
- HALT authority is independent and cannot be overridden by Operator or Trader
- Only admin or Operator can issue RESUME
- All alerts must be recorded to GitHub
- Do not relax monitoring frequency just because "the market is about to close"
