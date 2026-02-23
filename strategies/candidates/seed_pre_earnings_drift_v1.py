"""
Seed Strategy: Pre-Earnings Drift with Signal Confluence
Trades the pre-earnings drift pattern when multiple confirming signals align.

Strategy Logic:
- Enter 3-5 days before earnings if:
  1. Analyst estimate revisions trending up (or down for short)
  2. Unusual call (or put) buying detected
  3. No insider selling in prior 30 days
  4. Implied volatility is not excessively high (IV rank < 80)
- Exit: Before earnings announcement (avoid binary event risk)
- Stop-loss: -2.5%, Take-profit: +5%
- Holding period: 3-5 trading days

Feature Map Position:
- holding_period: 3-5 days (bin ~9)
- target_sharpe: 1.0~1.8
- max_drawdown: < 10%
- win_rate: ~57%
- asset_class: equity (bin 0)
- archetype: event_driven (bin 3)
"""

STRATEGY_META = {
    "id": "seed_pre_earnings_drift_v1",
    "name": "Pre-Earnings Drift with Signal Confluence",
    "version": "1.0.0",
    "archetype": "event_driven",
    "asset_class": "equity",
    "holding_period_minutes": [1440, 2400],  # 3-5 trading days
    "symbols": "dynamic",  # determined by earnings calendar
    "signal_sources": ["event", "options_flow", "corporate_insider", "fundamental"],
    "params": {
        "entry_days_before_earnings": 5,
        "exit_days_before_earnings": 0,  # exit before announcement
        "iv_rank_max": 80,
        "min_confirming_signals": 2,
        "stop_loss_pct": -0.025,
        "take_profit_pct": 0.05,
        "max_position_pct": 0.03,
    },
}


def evaluate_pre_earnings_setup(symbol, earnings_date, market_data, params=None):
    """
    Evaluate whether a pre-earnings trade setup exists.

    Args:
        symbol: stock ticker
        earnings_date: datetime of earnings announcement
        market_data: dict with keys:
            - analyst_revision_trend: "up" | "down" | "flat"
            - unusual_options_signal: "bullish" | "bearish" | "neutral"
            - insider_selling_30d: bool
            - iv_rank: float (0-100)
            - price_bars: list of price bars
        params: strategy parameters

    Returns:
        dict: { signal: BUY|SELL|HOLD, confidence: float, confirming_signals: list, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    confirming_bullish = []
    confirming_bearish = []
    conflicts = []

    # Signal 1: Analyst revisions
    revision = market_data.get("analyst_revision_trend", "flat")
    if revision == "up":
        confirming_bullish.append("analyst_revisions_up")
    elif revision == "down":
        confirming_bearish.append("analyst_revisions_down")

    # Signal 2: Unusual options
    options_signal = market_data.get("unusual_options_signal", "neutral")
    if options_signal == "bullish":
        confirming_bullish.append("unusual_call_buying")
    elif options_signal == "bearish":
        confirming_bearish.append("unusual_put_buying")

    # Signal 3: No insider selling (bullish) or insider selling (bearish)
    if not market_data.get("insider_selling_30d", False):
        confirming_bullish.append("no_insider_selling")
    else:
        confirming_bearish.append("insider_selling_detected")
        conflicts.append("insider_selling")

    # Signal 4: IV rank check
    iv_rank = market_data.get("iv_rank", 50)
    if iv_rank > params["iv_rank_max"]:
        conflicts.append(f"iv_rank_high_{iv_rank:.0f}")

    # Determine direction
    bullish_count = len(confirming_bullish)
    bearish_count = len(confirming_bearish)

    if bullish_count >= params["min_confirming_signals"] and bullish_count > bearish_count:
        confidence = 0.55 + min(0.3, bullish_count * 0.1) - len(conflicts) * 0.15
        return {
            "signal": "BUY",
            "confidence": round(max(0.5, min(0.85, confidence)), 2),
            "confirming_signals": confirming_bullish,
            "conflicts": conflicts,
            "reason": f"Pre-earnings bullish setup: {', '.join(confirming_bullish)}",
        }
    elif bearish_count >= params["min_confirming_signals"] and bearish_count > bullish_count:
        confidence = 0.55 + min(0.3, bearish_count * 0.1) - len(conflicts) * 0.15
        return {
            "signal": "SELL",
            "confidence": round(max(0.5, min(0.85, confidence)), 2),
            "confirming_signals": confirming_bearish,
            "conflicts": conflicts,
            "reason": f"Pre-earnings bearish setup: {', '.join(confirming_bearish)}",
        }

    return {
        "signal": "HOLD",
        "confidence": 0.0,
        "confirming_signals": [],
        "conflicts": conflicts,
        "reason": f"Insufficient confluence: {bullish_count} bullish, {bearish_count} bearish signals",
    }


def generate_signal(bars, earnings_setup=None, params=None):
    """
    Generate trading signal for pre-earnings drift.

    Args:
        bars: list of price bars
        earnings_setup: dict from evaluate_pre_earnings_setup()
        params: strategy parameters

    Returns:
        dict: { action: BUY|SELL|HOLD, confidence: float, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    if not earnings_setup or earnings_setup["signal"] == "HOLD":
        return {"action": "HOLD", "confidence": 0.0, "reason": "No pre-earnings setup"}

    return {
        "action": earnings_setup["signal"],
        "confidence": earnings_setup["confidence"],
        "reason": earnings_setup["reason"],
    }
