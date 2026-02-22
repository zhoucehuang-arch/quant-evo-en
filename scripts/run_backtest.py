"""
回测运行器
用于微循环/宏循环的策略回测验证。
支持从 Alpaca 获取历史数据或使用本地 CSV。
"""
import json
import importlib.util
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path


def load_strategy(strategy_path: str):
    """动态加载策略模块"""
    spec = importlib.util.spec_from_file_location("strategy", strategy_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def simulate_bars(symbol: str, days: int = 30, freq_minutes: int = 15):
    """
    生成模拟 K 线数据 (冷启动用)
    生产环境应替换为 Alpaca API 调用:
    GET https://data.alpaca.markets/v2/stocks/{symbol}/bars
    """
    import random
    random.seed(42)
    bars = []
    price = 150.0
    t = datetime.utcnow() - timedelta(days=days)
    for _ in range(days * (390 // freq_minutes)):  # 390 min per trading day
        change = random.gauss(0, 0.002)
        price *= (1 + change)
        bars.append({
            "timestamp": t.isoformat() + "Z",
            "open": round(price * (1 - abs(change) / 2), 2),
            "high": round(price * (1 + abs(change)), 2),
            "low": round(price * (1 - abs(change)), 2),
            "close": round(price, 2),
            "volume": random.randint(10000, 500000),
        })
        t += timedelta(minutes=freq_minutes)
    return bars


def run_backtest(strategy_path: str, days: int = 30, initial_capital: float = 100000.0):
    """执行回测"""
    module = load_strategy(strategy_path)
    meta = module.STRATEGY_META
    params = meta["params"]
    symbol = meta["symbols"][0]

    bars = simulate_bars(symbol, days)
    if len(bars) < 50:
        return {"status": "error", "message": "数据不足"}

    capital = initial_capital
    position = 0
    entry_price = 0.0
    trades = []
    equity_curve = [capital]

    for i in range(50, len(bars)):
        window = bars[i - 50 : i + 1]
        signal = module.generate_signal(window, params)
        current_price = bars[i]["close"]

        if signal["action"] == "BUY" and position == 0 and signal["confidence"] >= 0.5:
            qty = int(capital * params["max_position_pct"] / current_price)
            if qty > 0:
                position = qty
                entry_price = current_price
                capital -= qty * current_price

        elif signal["action"] == "SELL" and position > 0:
            pnl = position * (current_price - entry_price)
            capital += position * current_price
            trades.append({
                "entry": entry_price,
                "exit": current_price,
                "pnl": round(pnl, 2),
                "pnl_pct": round((current_price - entry_price) / entry_price, 4),
            })
            position = 0

        # 止损/止盈
        elif position > 0:
            pnl_pct = (current_price - entry_price) / entry_price
            if pnl_pct <= params["stop_loss_pct"] or pnl_pct >= params["take_profit_pct"]:
                pnl = position * (current_price - entry_price)
                capital += position * current_price
                trades.append({
                    "entry": entry_price,
                    "exit": current_price,
                    "pnl": round(pnl, 2),
                    "pnl_pct": round(pnl_pct, 4),
                })
                position = 0

        total_value = capital + position * current_price
        equity_curve.append(total_value)

    # 计算指标
    if not trades:
        return {"status": "no_trades", "message": "回测期间无交易"}

    wins = [t for t in trades if t["pnl"] > 0]
    total_return = (equity_curve[-1] - initial_capital) / initial_capital
    max_dd = 0.0
    peak = equity_curve[0]
    for v in equity_curve:
        peak = max(peak, v)
        dd = (peak - v) / peak
        max_dd = max(max_dd, dd)

    returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
               for i in range(1, len(equity_curve)) if equity_curve[i-1] > 0]
    avg_ret = sum(returns) / len(returns) if returns else 0
    std_ret = (sum((r - avg_ret)**2 for r in returns) / len(returns))**0.5 if returns else 1
    sharpe = (avg_ret / std_ret) * (252 * 26)**0.5 if std_ret > 0 else 0  # annualized

    return {
        "status": "success",
        "strategy_id": meta["id"],
        "backtest_days": days,
        "initial_capital": initial_capital,
        "final_value": round(equity_curve[-1], 2),
        "total_return": round(total_return, 4),
        "sharpe_ratio": round(sharpe, 2),
        "max_drawdown": round(max_dd, 4),
        "total_trades": len(trades),
        "win_rate": round(len(wins) / len(trades), 2) if trades else 0,
        "profit_factor": round(
            sum(t["pnl"] for t in wins) / abs(sum(t["pnl"] for t in trades if t["pnl"] < 0))
            if any(t["pnl"] < 0 for t in trades) else 999, 2
        ),
        "avg_pnl_pct": round(sum(t["pnl_pct"] for t in trades) / len(trades), 4),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def main():
    parser = argparse.ArgumentParser(description="Strategy Backtest Runner")
    parser.add_argument("strategy", help="Path to strategy .py file")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--capital", type=float, default=100000.0)
    parser.add_argument("--output", default=None, help="Output JSON path")
    args = parser.parse_args()

    result = run_backtest(args.strategy, args.days, args.capital)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(output)

    return 0 if result.get("status") == "success" and result.get("sharpe_ratio", 0) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
