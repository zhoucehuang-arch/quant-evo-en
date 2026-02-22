"""
种子策略: RSI 动量反转
这是系统冷启动的第一个策略，用于填充 Feature Map 的第一个 cell。
后续所有策略将基于此种子进化。

策略逻辑:
- 当 RSI(14) < 30 且价格在 20日均线之上时买入 (超卖反弹)
- 当 RSI(14) > 70 或价格跌破 20日均线时卖出
- 持仓周期: 30分钟 ~ 4小时 (日内)
- 止损: -3%, 止盈: +6%

Feature Map 定位:
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
    """计算 RSI 指标"""
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
    """计算简单移动平均"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def generate_signal(bars, params=None):
    """
    生成交易信号

    Args:
        bars: list of dicts with keys: timestamp, open, high, low, close, volume
        params: 策略参数 (默认使用 STRATEGY_META["params"])

    Returns:
        dict: { action: BUY|SELL|HOLD, confidence: float, reason: str }
    """
    if params is None:
        params = STRATEGY_META["params"]

    if len(bars) < max(params["rsi_period"] + 1, params["sma_period"]):
        return {"action": "HOLD", "confidence": 0.0, "reason": "数据不足"}

    closes = [b["close"] for b in bars]
    current_price = closes[-1]

    rsi = compute_rsi(closes, params["rsi_period"])
    sma = compute_sma(closes, params["sma_period"])

    if sma is None:
        return {"action": "HOLD", "confidence": 0.0, "reason": "SMA 数据不足"}

    # 买入条件: RSI 超卖 + 价格在均线之上
    if rsi < params["rsi_oversold"] and current_price > sma:
        confidence = min(0.9, (params["rsi_oversold"] - rsi) / params["rsi_oversold"] + 0.5)
        return {
            "action": "BUY",
            "confidence": round(confidence, 2),
            "reason": f"RSI={rsi:.1f} 超卖反弹, 价格 {current_price:.2f} > SMA{params['sma_period']} {sma:.2f}",
        }

    # 卖出条件: RSI 超买 或 价格跌破均线
    if rsi > params["rsi_overbought"]:
        return {
            "action": "SELL",
            "confidence": 0.8,
            "reason": f"RSI={rsi:.1f} 超买, 获利了结",
        }

    if current_price < sma * 0.99:  # 跌破均线 1%
        return {
            "action": "SELL",
            "confidence": 0.7,
            "reason": f"价格 {current_price:.2f} 跌破 SMA{params['sma_period']} {sma:.2f}",
        }

    return {"action": "HOLD", "confidence": 0.0, "reason": f"RSI={rsi:.1f}, 无信号"}
