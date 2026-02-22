# Runtime Schedules

## System A: Self-Evolution System (24/7 Operation)

### Trading Days (Mon-Fri, US stock market open days)

| Time (EST) | Cycle | Content |
|---|---|---|
| 00:00-09:00 | Micro-cycle x4-5 | Normal evolution cycles (focus on paper research, historical data backtesting) |
| 09:00-09:30 | Micro-cycle | Pre-market: Explorer monitors market expectations and earnings calendar for the day |
| 09:30-16:00 | Micro-cycle x3 | Market hours: Explorer may reference real-time market data |
| 16:00-17:00 | Daily cycle | Evolver aggregates the day's results + reads System B performance |
| 17:00 | Daily report | Evolver publishes daily report to `#a-report` |
| 17:00-24:00 | Micro-cycle x3-4 | After-hours: Normal evolution cycles |

**Daily average: ~12 micro-cycles**

### Non-Trading Days (Weekends, US stock market holidays)

| Time (EST) | Cycle | Content |
|---|---|---|
| All day | Micro-cycle x12 | Normal evolution cycles (focus on in-depth paper analysis, architecture improvements) |
| Sat 10:00 | Weekly cycle | Architecture-level improvement debate + weekly report |
| Sunday | Micro-cycle x12 | Preparation for next week: monitor upcoming earnings, economic data releases |

**Non-trading day focus:**
- More time for in-depth paper analysis (Explorer research phase extended)
- Architecture-level improvement debate (Saturday)
- Backtesting with longer historical data windows

### Reporting Frequency

> **Note:** All reports sent to the admin (`#admin` channel) must be written in Chinese (中文).

| Frequency | Time | Content | Channel |
|---|---|---|---|
| Every 2h | End of micro-cycle | Hypotheses / verdicts / backtest results / Feature Map changes | `#a-report` |
| Daily | 17:00 EST | Daily evolution results summary + System B performance feedback | `#a-report` |
| Weekly | Sat 10:00 | Weekly summary + architecture improvements + next week direction | `#a-report` |

---

## System B: Automated Investment System

### Trading Days

| Time (EST) | Agent | Frequency | Content |
|---|---|---|---|
| 09:15 | Operator | 1x | Pre-market check: Alpaca connection, strategy readiness, risk parameters |
| 09:30-16:00 | Trader | Every 15min | Signal generation + execution |
| 09:30-16:00 | Guardian | Every 5min | Real-time risk monitoring |
| 09:30-16:00 | Operator | Every 15min | Check GitHub for new strategies |
| Every 2h (market hours) | Operator | 3x | Trading summary to `#b-report` |
| 16:00 | Operator | 1x | Market close procedure: stop signals, aggregate data |
| 16:15 | Guardian | 1x | Commit daily performance data to GitHub |
| 16:30 | Operator | 1x | Daily report to `#b-report` |

### Non-Trading Days

| Time (EST) | Agent | Frequency | Content |
|---|---|---|---|
| Every 4h | Operator | 6x/day | Check GitHub for new strategies |
| Every 12h | Guardian | 2x/day | Overnight risk check (position exposure) |
| Sat 10:00 | Operator | 1x | Weekly report to `#b-report` |

### Reporting Frequency

> **Note:** All reports sent to the admin (`#admin` channel) must be written in Chinese (中文).

| Frequency | Time | Content | Channel |
|---|---|---|---|
| Every 2h (market hours) | Trading session | Trading summary: P&L, trade count, risk status | `#b-report` |
| Daily | 16:30 EST | Daily report: P&L, Sharpe, strategy attribution, staging status | `#b-report` |
| Weekly | Sat 10:00 | Weekly report: cumulative performance, strategy ranking, risk review | `#b-report` |

---

## Strategy Validation Periods (Operator Decision Criteria)

| Strategy Archetype | Typical Holding Period | Minimum Validation | Standard Validation | Promotion Criteria |
|---|---|---|---|---|
| High-frequency momentum | 5min-1h | 1 trading day | 2-3 trading days | Sharpe>0.3, DD<15%, >20 trades |
| Intraday mean reversion | 30min-4h | 2 trading days | 3-5 trading days | Sharpe>0.3, DD<15%, >10 trades |
| Short-term trend | 4h-2d | 3 trading days | 5-7 trading days | Sharpe>0.3, DD<20%, >5 trades |
| Medium-term event-driven | 1d-5d | 5 trading days | 7-10 trading days | Sharpe>0.2, DD<20%, >3 trades |

---

## US Stock Market Holidays (2026)

The system must recognize the following dates as non-trading days:
- 2026-01-01 New Year's Day
- 2026-01-19 MLK Day
- 2026-02-16 Presidents' Day
- 2026-04-03 Good Friday
- 2026-05-25 Memorial Day
- 2026-07-03 Independence Day (observed)
- 2026-09-07 Labor Day
- 2026-11-26 Thanksgiving
- 2026-12-25 Christmas

The exact trading calendar can be obtained via the Alpaca API `GET /v2/calendar`.
