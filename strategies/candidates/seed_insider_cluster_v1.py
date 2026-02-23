"""
Seed Strategy: Insider Cluster Buy Following
Tracks corporate insider and politician cluster buying patterns.

Strategy Logic:
- When 3+ insiders buy the same stock within 30 days (cluster buy signal)
- AND the stock is not at 52-week high (buying the dip, not chasing)
- AND RSI(14) < 60 (not overbought)
- Enter long with 3% position size
- Stop-loss: -5%, Take-profit: +10%
- Holding period: 5-20 trading days
- Exit if insider selling detected during holding period

Feature Map Position:
- holding_period: 5-20 days (bin ~10)
- target_sharpe: 1.0~2.0
- max_drawdown: < 15%
- win_rate: ~58%
- asset_class: equity (bin 0)
- archetype: insider_following (bin 4)
"""

STRATEGY_META = {
    "id": "seed_insider_cluster_v1",
    "name": "Insider Cluster Buy Following",
    "version": "1.0.0",
    "archetype": "insider_following",
    "asset_class": "equity",
    "holding_period_minutes": [2400, 9600],  # 5-20 trading days
    "symbols": "dynamic",  # determined by insider activity
    "signal_sources": ["corporate_insider", "politician_trading", "technical"],
    "params": {
        "min_insiders": 3,
        "cluster_window_days": 30,
        "max_pct_from_52w_high": 0.90,  # must be below 90% of 52w high
        "rsi_max": 60,
        "rsi_period": 14,
        "stop_loss_pct": -0.05,
        "take_profit_pct": 0.10,
        "max_position_pct": 0.03,
        "max_holding_days": 20,
    },
}


def check_insider_cluster(insider_filings, symbol, params=None):
    """
    Check if a stock has a cluster insider buy signal.

    Args:
        insider_filings: list of dicts with keys: symbol, insider_name, transaction_type,
                        shares, price, date, insider_title
        symbol: stock ticker to check
        params: strategy parameters

    Returns:
        dict: { signal: bool, insider_count: int, details: list }
    """
    if params is None:
        params = STRATEGY_META["params"]

    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=params["cluster_window_days"])

    recent_buys = [
        f for f in insider_filings
        if f["symbol"] == symbol
        and f["transaction_type"] == "BUY"
        and datetime.fromisoformat(f["date"]) >= cutoff
    ]

    unique_insiders = set(f["insider_name"] for f in recent_buys)

    return {
        "signal": len(unique_insiders) >= params["min_insiders"],
        "insider_count": len(unique_insiders),
        "details": [
            {"name": f["insider_name"], "title": f["insider_title"],
             "shares": f["shares"], "price": f["price"], "date": f["date"]}
            for f in recent_buys
        ],
    }


def generate_signal(bars, insider_data=None, params=None):
    """
    Generate trading signal based on insider cluster + technical confirmation.

    Args:
        bars: list of dicts with keys: timestamp, open, high, low, close, volume
        insider_data: dict from check_insider_cluster()
        params: strategy parameters

    Returns:
        dict: { action: BUY|SELL|HOLD, confidence: float, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    if not insider_data or not insider_data.get("signal"):
        return {"action": "HOLD", "confidence": 0.0, "reason": "No insider cluster signal"}

    if len(bars) < params["rsi_period"] + 1:
        return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient data"}

    closes = [b["close"] for b in bars]
    current_price = closes[-1]
    high_52w = max(b["high"] for b in bars[-252:]) if len(bars) >= 252 else max(b["high"] for b in bars)

    # Check not at 52-week high
    if current_price > high_52w * params["max_pct_from_52w_high"]:
        return {"action": "HOLD", "confidence": 0.0,
                "reason": f"Price {current_price:.2f} too close to 52w high {high_52w:.2f}"}

    # Calculate RSI
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    period = params["rsi_period"]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    rsi = 100.0 if avg_loss == 0 else 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))

    if rsi > params["rsi_max"]:
        return {"action": "HOLD", "confidence": 0.0,
                "reason": f"RSI={rsi:.1f} > {params['rsi_max']}, overbought"}

    # Confidence based on insider count
    insider_count = insider_data["insider_count"]
    base_confidence = 0.6 + min(0.25, (insider_count - 3) * 0.05)
    # Bonus if price is significantly below 52w high (buying the dip)
    dip_bonus = min(0.1, (1 - current_price / high_52w) * 0.5)
    confidence = min(0.9, base_confidence + dip_bonus)

    return {
        "action": "BUY",
        "confidence": round(confidence, 2),
        "reason": (f"{insider_count} insiders bought in {params['cluster_window_days']}d, "
                   f"RSI={rsi:.1f}, price {current_price:.2f} is "
                   f"{(1 - current_price/high_52w)*100:.1f}% below 52w high"),
    }
