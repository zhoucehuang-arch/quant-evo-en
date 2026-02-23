"""
Seed Strategy: RSI Momentum Reversal
This is the system's first cold-start strategy, used to fill the first cell of the Feature Map.
All subsequent strategies will evolve based on this seed.

Strategy Logic:
- Buy when RSI(14) < 30 AND price is above 20-day SMA (oversold bounce)
- Sell when RSI(14) > 70 OR price drops below 20-day SMA
- Holding period: 30 minutes ~ 4 hours (intraday)
- Stop-loss: -3%, Take-profit: +6%

Feature Map Position:
- holding_period: 30min~4h (bin ~4)
- target_sharpe: 1.0~1.5
- max_drawdown: < 10%
- win_rate: ~55%
- asset_class: equity (bin 0)
- archetype: momentum (bin 0)
"""

STRATEGY_META = {
    "id": "seed_momentum_rsi_v1",
    "name": "RSI Momentum Reversal",
    "version": "1.0.0",
    "archetype": "momentum",
    "asset_class": "equity",
    "holding_period_minutes": [30, 240],
    "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
    "signal_sources": ["technical"],
    "params": {
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "sma_period": 20,
        "stop_loss_pct": -0.03,
        "take_profit_pct": 0.06,
        "max_position_pct": 0.05,
    },
}


def compute_rsi(prices, period=14):
    """Calculate RSI indicator."""
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def compute_sma(prices, period=20):
    """Calculate simple moving average."""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def generate_signal(bars, params=None):
    """
    Generate trading signal.

    Args:
        bars: list of dicts with keys: timestamp, open, high, low, close, volume
        params: strategy parameters (defaults to STRATEGY_META["params"])

    Returns:
        dict: { action: BUY|SELL|HOLD, confidence: float, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    if len(bars) < max(params["rsi_period"] + 1, params["sma_period"]):
        return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient data"}

    closes = [b["close"] for b in bars]
    current_price = closes[-1]

    rsi = compute_rsi(closes, params["rsi_period"])
    sma = compute_sma(closes, params["sma_period"])

    if sma is None:
        return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient SMA data"}

    # Buy condition: RSI oversold + price above SMA
    if rsi < params["rsi_oversold"] and current_price > sma:
        confidence = min(0.9, (params["rsi_oversold"] - rsi) / params["rsi_oversold"] + 0.5)
        return {
            "action": "BUY",
            "confidence": round(confidence, 2),
            "reason": f"RSI={rsi:.1f} oversold bounce, price {current_price:.2f} > SMA{params['sma_period']} {sma:.2f}",
        }

    # Sell condition: RSI overbought or price below SMA
    if rsi > params["rsi_overbought"]:
        return {
            "action": "SELL",
            "confidence": 0.8,
            "reason": f"RSI={rsi:.1f} overbought, take profit",
        }

    if current_price < sma * 0.99:  # 1% below SMA
        return {
            "action": "SELL",
            "confidence": 0.7,
            "reason": f"Price {current_price:.2f} broke below SMA{params['sma_period']} {sma:.2f}",
        }

    return {"action": "HOLD", "confidence": 0.0, "reason": f"RSI={rsi:.1f}, no signal"}
