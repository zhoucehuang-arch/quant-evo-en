# Communication Protocol: Message Schemas

All messages passed between Agents via Discord channels must strictly follow the JSON Schemas below.
Free-form messages are only allowed in the `#admin` channel (human-agent interaction).

---

## System A Messages

### #a-arena: Strategy Hypothesis (Explorer → Critic)
```json
{
  "type": "HYPOTHESIS",
  "hypothesis_id": "hyp_20260223_1030",
  "round": 1,
  "statement": "One-sentence core hypothesis",
  "rationale": "Theoretical basis",
  "expected_traits": {
    "holding_period_minutes": [30, 240],
    "target_sharpe": 1.5,
    "max_drawdown": 0.10,
    "win_rate": 0.55,
    "asset_class": "equity",
    "archetype": "momentum"
  },
  "evidence": ["Reference 1", "Reference 2"],
  "parent_strategy_id": "seed_momentum_rsi_v1",
  "feature_map_target": [3, 5, 2, 4, 0, 1]
}
```

### #a-arena: Risk Assessment (Critic → Evolver)
```json
{
  "type": "RISK_ASSESSMENT",
  "hypothesis_id": "hyp_20260223_1030",
  "round": 1,
  "risk_rating": "PASS | CONDITIONAL_PASS | REJECT",
  "scores": {
    "tail_risk": 0.3,
    "overfitting": 0.4,
    "execution_risk": 0.2,
    "correlation_risk": 0.5
  },
  "conditions": ["Position must not exceed 3% of portfolio"],
  "fatal_flaws": [],
  "reasoning": "Detailed reasoning"
}
```

### #a-arena: Debate Rebuttal (Explorer Round 2)
```json
{
  "type": "REBUTTAL",
  "hypothesis_id": "hyp_20260223_1030",
  "round": 2,
  "responses": [
    { "critique_point": "Tail risk", "response": "Rebuttal content", "evidence": "Supporting evidence" }
  ],
  "modifications": ["Modification 1"]
}
```

### #a-verdict: Verdict (Evolver)
```json
{
  "type": "VERDICT",
  "hypothesis_id": "hyp_20260223_1030",
  "verdict": "APPROVE | REJECT | REVISE",
  "confidence": 0.82,
  "reasoning": "Reasoning citing arguments from both sides",
  "alpha_score": 0.8,
  "risk_score": 0.7,
  "conditions": ["Position limit 3%", "Stop-loss -5%"],
  "next_action": "backtest | archive | revise",
  "backtest_result": {
    "sharpe": 1.45,
    "max_drawdown": 0.08,
    "win_rate": 0.57,
    "total_trades": 142,
    "profit_factor": 1.8
  },
  "feature_map_cell": [3, 5, 2, 4, 0, 1],
  "feature_map_updated": true,
  "committed_to": "strategies/candidates/hyp_20260223_1030.py"
}
```

### #a-report: Micro-Cycle Report (Evolver, every 2h)
```json
{
  "type": "MICRO_CYCLE_REPORT",
  "cycle_id": "cycle_20260223_1030",
  "timestamp": "2026-02-23T10:30:00Z",
  "hypothesis_id": "hyp_20260223_1030",
  "verdict": "APPROVE",
  "confidence": 0.82,
  "backtest_sharpe": 1.45,
  "feature_map_coverage_pct": 0.0012,
  "feature_map_delta_cells": 1,
  "daily_summary": {
    "cycles_completed": 5,
    "strategies_approved": 2,
    "strategies_rejected": 3
  },
  "next_cycle_trigger": "EXPLORER_START"
}
```

### #a-report: Daily Report (Evolver, daily at 17:00 EST)
```json
{
  "type": "DAILY_REPORT",
  "date": "2026-02-23",
  "cycles_completed": 12,
  "strategies_approved": 4,
  "strategies_rejected": 7,
  "strategies_revised": 1,
  "feature_map_coverage_pct": 0.0048,
  "feature_map_delta_cells": 4,
  "top_strategy": { "id": "hyp_20260223_1030", "sharpe": 1.45 },
  "trading_feedback": {
    "production_strategies": 2,
    "daily_pnl_pct": 0.012,
    "feedback_insights": ["Strategy X outperformed expectations under high-volatility regime"]
  },
  "tomorrow_priority": "Explore stat_arb types; Feature Map has gaps in that region"
}
```

### #a-report: Weekly Report (Evolver, every Saturday)
```json
{
  "type": "WEEKLY_REPORT",
  "week": "2026-W08",
  "total_cycles": 84,
  "strategies_approved": 28,
  "feature_map_coverage_pct": 0.034,
  "best_strategy_sharpe": 2.1,
  "architecture_improvements": ["Improved backtest data source"],
  "next_week_direction": "Focus on exploring event-driven strategies"
}
```

---

## System B Messages

### #b-ops: Deployment Notice (Operator)
```json
{
  "type": "DEPLOY_NOTICE",
  "action": "STAGE | PROMOTE | WITHDRAW",
  "strategy_id": "hyp_20260223_1030",
  "from": "candidates",
  "to": "staging",
  "validation_period_days": 3,
  "reason": "CI validation passed; starting paper-trading validation"
}
```

### #b-desk: Trading Signal (Trader)
```json
{
  "type": "SIGNAL",
  "signal_id": "sig_20260223_1031_001",
  "strategy_id": "hyp_20260223_1030",
  "symbol": "AAPL",
  "action": "BUY | SELL | HOLD",
  "quantity": 100,
  "order_type": "market | limit",
  "limit_price": 185.50,
  "confidence": 0.85,
  "reason": "RSI oversold bounce + MACD golden cross",
  "risk_params": {
    "stop_loss_pct": -0.03,
    "take_profit_pct": 0.06,
    "max_position_pct": 0.05
  }
}
```

### #b-desk: Execution Log (Trader)
```json
{
  "type": "EXECUTION",
  "execution_id": "exec_20260223_1031_001",
  "signal_id": "sig_20260223_1031_001",
  "symbol": "AAPL",
  "action": "BUY",
  "qty_filled": 100,
  "avg_price": 185.52,
  "slippage_bps": 1.08,
  "status": "filled | partial | cancelled | rejected",
  "alpaca_order_id": "xxx"
}
```

### #b-risk: Risk Alert (Guardian)
```json
{
  "type": "RISK_ALERT",
  "alert_id": "alert_20260223_1035_001",
  "level": "INFO | WARNING | CRITICAL | HALT",
  "metric": "daily_pnl",
  "current_value": -0.032,
  "threshold": -0.03,
  "message": "Intraday P&L has reached -3.2%",
  "action_required": "none | reduce_exposure | halt_trading",
  "affected_strategies": ["hyp_20260223_1030"]
}
```

### #b-report: Trading Summary (Operator, every 2h during trading session)
```json
{
  "type": "TRADING_SUMMARY",
  "period": "10:00-12:00 EST",
  "pnl_usd": 523.40,
  "pnl_pct": 0.0052,
  "trades": 8,
  "wins": 5,
  "losses": 3,
  "active_strategies": ["strategy_a", "strategy_b"],
  "risk_status": "NORMAL | WARNING | CRITICAL | HALTED"
}
```

### #b-report: Daily Report (Operator, daily at 16:30 EST)
```json
{
  "type": "DAILY_TRADING_REPORT",
  "date": "2026-02-23",
  "pnl_usd": 1247.80,
  "pnl_pct": 0.0125,
  "cumulative_pnl_pct": 0.034,
  "sharpe_30d": 1.82,
  "max_dd_30d": 0.045,
  "total_trades": 24,
  "win_rate": 0.625,
  "strategy_attribution": [
    { "id": "strategy_a", "pnl_pct": 0.008, "trades": 15 },
    { "id": "strategy_b", "pnl_pct": 0.0045, "trades": 9 }
  ],
  "staging_strategies": [
    { "id": "hyp_20260223_1030", "days_in_staging": 2, "staging_sharpe": 0.45 }
  ]
}
```

---

## Trigger Messages (Cycle Orchestration)

### Evolver → Explorer: Trigger New Round
```json
{
  "type": "CYCLE_TRIGGER",
  "trigger": "EXPLORER_START",
  "cycle_id": "cycle_20260223_1230",
  "context": {
    "last_verdict": "APPROVE",
    "feature_map_gaps": ["Low coverage in stat_arb region"],
    "priority_direction": "Explore statistical arbitrage strategies",
    "available_parents": ["seed_momentum_rsi_v1", "hyp_20260223_1030"]
  }
}
```

### Explorer → Critic: Trigger Assessment
Critic listens on `#a-arena` and automatically begins assessment upon receiving a `type: "HYPOTHESIS"` message.

### Critic → Evolver: Trigger Verdict
Evolver listens on `#a-arena` and begins verdict upon receiving a `round: 2` `RISK_ASSESSMENT`.
