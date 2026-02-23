"""
Seed Strategy: Unusual Options Flow Momentum
Trades in the direction of large unusual options activity.

Strategy Logic:
- When a stock has unusual options activity (sweep orders >$500K premium,
  volume >10x open interest on a single strike)
- AND the options are directional (single-leg calls or puts, not spreads)
- AND the activity is in short-dated options (< 30 DTE)
- Enter in the direction of the flow (calls = long, puts = short)
- Stop-loss: -3%, Take-profit: +5%
- Holding period: 1-5 trading days
- Exit if opposing flow detected (large put sweeps after entering long)

Feature Map Position:
- holding_period: 1-5 days (bin ~8)
- target_sharpe: 1.2~2.0
- max_drawdown: < 12%
- win_rate: ~55%
- asset_class: equity (bin 0)
- archetype: options_flow (bin 5)
"""

STRATEGY_META = {
    "id": "seed_options_flow_v1",
    "name": "Unusual Options Flow Momentum",
    "version": "1.0.0",
    "archetype": "options_flow",
    "asset_class": "equity",
    "holding_period_minutes": [480, 2400],  # 1-5 trading days
    "symbols": "dynamic",  # determined by options activity
    "signal_sources": ["options_flow", "technical"],
    "params": {
        "min_premium_usd": 500000,
        "min_volume_oi_ratio": 10,
        "max_dte": 30,
        "min_trades": 2,  # at least 2 unusual trades same direction
        "stop_loss_pct": -0.03,
        "take_profit_pct": 0.05,
        "max_position_pct": 0.03,
        "max_holding_days": 5,
    },
}


def analyze_options_flow(flow_data, symbol, params=None):
    """
    Analyze unusual options flow for a given symbol.

    Args:
        flow_data: list of dicts with keys: symbol, option_type (call/put),
                   strike, expiry, premium, volume, open_interest, trade_type (sweep/block)
        symbol: stock ticker
        params: strategy parameters

    Returns:
        dict: { signal: str (bullish/bearish/neutral), strength: float, details: list }
    """
    if params is None:
        params = STRATEGY_META["params"]

    from datetime import datetime, timedelta
    max_expiry = datetime.now() + timedelta(days=params["max_dte"])

    unusual = [
        f for f in flow_data
        if f["symbol"] == symbol
        and f["premium"] >= params["min_premium_usd"]
        and f["volume"] / max(f["open_interest"], 1) >= params["min_volume_oi_ratio"]
        and datetime.fromisoformat(f["expiry"]) <= max_expiry
        and f["trade_type"] in ("sweep", "block")
    ]

    if len(unusual) < params["min_trades"]:
        return {"signal": "neutral", "strength": 0.0, "details": []}

    call_premium = sum(f["premium"] for f in unusual if f["option_type"] == "call")
    put_premium = sum(f["premium"] for f in unusual if f["option_type"] == "put")
    total_premium = call_premium + put_premium

    if total_premium == 0:
        return {"signal": "neutral", "strength": 0.0, "details": unusual}

    call_ratio = call_premium / total_premium

    if call_ratio > 0.7:
        return {"signal": "bullish", "strength": call_ratio, "details": unusual}
    elif call_ratio < 0.3:
        return {"signal": "bearish", "strength": 1 - call_ratio, "details": unusual}
    else:
        return {"signal": "neutral", "strength": 0.0, "details": unusual}


def generate_signal(bars, flow_analysis=None, params=None):
    """
    Generate trading signal based on unusual options flow + price confirmation.

    Args:
        bars: list of dicts with keys: timestamp, open, high, low, close, volume
        flow_analysis: dict from analyze_options_flow()
        params: strategy parameters

    Returns:
        dict: { action: BUY|SELL|HOLD, confidence: float, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    if not flow_analysis or flow_analysis["signal"] == "neutral":
        return {"action": "HOLD", "confidence": 0.0, "reason": "No unusual options signal"}

    if len(bars) < 20:
        return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient price data"}

    closes = [b["close"] for b in bars]
    current_price = closes[-1]
    sma_20 = sum(closes[-20:]) / 20

    signal = flow_analysis["signal"]
    strength = flow_analysis["strength"]
    num_trades = len(flow_analysis["details"])
    total_premium = sum(f["premium"] for f in flow_analysis["details"])

    # Confidence based on flow strength and number of trades
    base_confidence = 0.55 + min(0.25, (strength - 0.7) * 0.5)
    trade_bonus = min(0.1, (num_trades - 2) * 0.02)
    confidence = min(0.85, base_confidence + trade_bonus)

    if signal == "bullish":
        # Price confirmation: prefer if price is near or above SMA (trend alignment)
        if current_price < sma_20 * 0.97:
            confidence -= 0.1  # reduce confidence if against trend
        return {
            "action": "BUY",
            "confidence": round(max(0.5, confidence), 2),
            "reason": (f"Bullish options flow: {num_trades} unusual trades, "
                       f"${total_premium/1000:.0f}K total premium, "
                       f"call ratio {strength:.0%}"),
        }
    elif signal == "bearish":
        if current_price > sma_20 * 1.03:
            confidence -= 0.1
        return {
            "action": "SELL",
            "confidence": round(max(0.5, confidence), 2),
            "reason": (f"Bearish options flow: {num_trades} unusual trades, "
                       f"${total_premium/1000:.0f}K total premium, "
                       f"put ratio {strength:.0%}"),
        }

    return {"action": "HOLD", "confidence": 0.0, "reason": "Mixed options flow"}
