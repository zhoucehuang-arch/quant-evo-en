# Strategy Frameworks Reference

This document serves as a knowledge base for Explorer to reference when generating strategy hypotheses.
It codifies proven quantitative frameworks aligned with our core philosophy:
**mid-short term, mid-high frequency, aggressive, tight stop-loss/take-profit**.

---

## 1. Alternative Data Strategies (Highest Priority)

### 1a. Congressional / Politician Trade Following
- **Edge**: Politicians trade on committee-level information asymmetry (legal gray area, but public data)
- **Signal**: Buy within 1-3 days of politician disclosure (STOCK Act requires 45-day disclosure)
- **Filters**: Committee relevance (defense committee + defense stock = strong), cluster buys (3+ politicians same ticker in 7 days), position size > 5% of net worth
- **Holding period**: 5-20 trading days (information diffusion period)
- **Historical edge**: ~7% excess return over 12 months (academic studies), but decaying as more people follow
- **Risk**: Disclosure delay (up to 45 days), crowding, regulatory changes
- **Combination**: Strongest when combined with technical momentum or insider buying

### 1b. Corporate Insider Buying
- **Edge**: Insiders know their company better than anyone
- **Signal**: CEO/CFO open-market purchase (not option exercise), cluster buys (3+ insiders in 30 days)
- **Filters**: Buy during price weakness (insider buying the dip), large purchases relative to salary, no recent insider selling
- **Holding period**: 5-30 trading days
- **Historical edge**: ~5-8% excess return over 6 months
- **Risk**: Insiders can be wrong, some buys are cosmetic (small amounts for optics)
- **Combination**: Strongest when combined with unusual options activity

### 1c. Unusual Options Flow
- **Edge**: Large options trades often precede significant price moves (informed trading)
- **Signal**: Sweep orders >$500K premium, call/put ratio spike >3x normal, short-dated OTM calls with volume >10x open interest
- **Filters**: Exclude known hedging activity (paired with stock positions), focus on single-leg directional bets
- **Holding period**: 1-5 trading days (options are time-sensitive)
- **Historical edge**: ~3-5% over 5 days for high-conviction sweeps
- **Risk**: Not all unusual activity is informed (could be hedging), rapid decay
- **Combination**: Strongest when combined with insider buying or pre-earnings setup

---

## 2. Event-Driven Strategies

### 2a. Pre-Earnings Momentum / Fade
- **Edge**: Stocks often drift in the direction of the eventual earnings surprise before the announcement
- **Pre-earnings drift strategy**: Enter 3-5 days before earnings if: (1) analyst revisions trending up, (2) unusual call buying, (3) insider buying in prior 30 days. Exit before announcement.
- **Post-earnings gap strategy**: Enter after earnings gap if: (1) gap aligns with pre-earnings signals, (2) volume confirms, (3) gap doesn't fill within first 30 minutes. Ride the drift for 1-3 days.
- **Fade strategy**: If IV >> historical realized vol AND no confirming alternative data signals, sell premium (straddle/strangle) or fade the expected move.
- **Holding period**: 1-5 days (pre) or 1-3 days (post)
- **Risk**: Binary event, gap risk, IV crush

### 2b. Catalyst Event (Product Launch / Conference / FDA)
- **Edge**: Short-window information asymmetry during live events
- **Signal**: Enter at the start of a known catalyst event (e.g., Apple WWDC keynote, NVIDIA GTC, FDA advisory committee meeting)
- **Execution**: Monitor real-time news/social sentiment during the event. Enter on first significant positive/negative signal. Tight stop-loss (-1.5%), quick take-profit (+3-5%).
- **Holding period**: Minutes to hours (intraday)
- **Risk**: Extremely fast-moving, requires low-latency execution
- **Combination**: Pre-position based on options flow before the event, then adjust during

### 2c. Macro Event Trading
- **Edge**: FOMC, CPI, NFP releases create predictable volatility patterns
- **Signal**: Trade the reaction pattern (e.g., initial spike → reversal → trend continuation)
- **Execution**: Wait for the initial 5-minute reaction, then enter in the direction of the 15-minute trend
- **Holding period**: 30 minutes to 4 hours
- **Risk**: Whipsaw, false breakouts

---

## 3. Technical / Quantitative Strategies

### 3a. Momentum (RSI + MACD + Volume)
- **Edge**: Trend continuation after oversold/overbought conditions with volume confirmation
- **Entry**: RSI < 30 + MACD golden cross + volume spike > 2x average
- **Exit**: RSI > 70 or MACD death cross or stop-loss hit
- **Holding period**: 30 minutes to 4 hours
- **Enhancement**: Add alternative data confirmation (insider buying + oversold = high conviction)

### 3b. Mean Reversion (Bollinger Bands + Z-Score)
- **Edge**: Prices revert to mean after extreme deviations
- **Entry**: Price touches lower Bollinger Band (2σ) + z-score < -2 + no fundamental catalyst for the move
- **Exit**: Price returns to middle band or stop-loss hit
- **Holding period**: 1-4 hours
- **Risk**: Trend continuation (mean reversion fails in trending markets)

### 3c. Statistical Arbitrage (Pairs Trading)
- **Edge**: Cointegrated pairs revert to their historical spread
- **Entry**: Spread z-score > 2 (or < -2), enter long the underperformer and short the outperformer
- **Exit**: Spread returns to 0 or stop-loss at z-score > 3
- **Pairs selection**: Same sector, high historical correlation (>0.8), confirmed cointegration (Engle-Granger test p < 0.05)
- **Holding period**: 1-5 days
- **Risk**: Pair breakdown (structural change), short squeeze on the short leg

### 3d. Multi-Factor Model
- **Edge**: Combining multiple orthogonal factors reduces noise and improves signal quality
- **Factors**: Momentum (12-1 month), Value (P/E, P/B), Quality (ROE, debt/equity), Size (small cap premium), Volatility (low vol anomaly)
- **Scoring**: Rank stocks by composite factor score, go long top decile, short bottom decile
- **Rebalance**: Weekly
- **Holding period**: 5-20 trading days
- **Enhancement**: Weight factors dynamically based on current regime (momentum works in trending markets, value works in mean-reverting markets)

---

## 4. Execution Frameworks

### 4a. Position Sizing (Kelly Criterion Variant)
- **Formula**: f = (p * b - q) / b, where p = win rate, b = avg win / avg loss, q = 1 - p
- **Apply half-Kelly** for safety: actual position = f / 2
- **Cap**: Never exceed 5% of portfolio per trade, 10% per ticker

### 4b. Stop-Loss / Take-Profit Rules
- **Default**: Stop-loss -3%, Take-profit +6% (2:1 reward/risk)
- **Aggressive (event-driven)**: Stop-loss -1.5%, Take-profit +3-5%
- **Trailing stop**: After +3% gain, trail stop at -1.5% from high
- **Time-based exit**: If no significant move within expected holding period, exit at market

### 4c. Entry Timing
- **Avoid**: First 15 minutes and last 15 minutes of trading session (high noise)
- **Prefer**: 10:00-11:30 AM and 2:00-3:30 PM EST (highest liquidity, clearest trends)
- **Event-driven exception**: Enter immediately when catalyst fires, regardless of time

---

## 5. Signal Confluence Matrix

| Confluence Level | Signals Required | Max Position Size | Confidence Range |
|---|---|---|---|
| Weak | 1 signal | 2% of portfolio | 0.5-0.6 |
| Moderate | 2 confirming signals | 3% of portfolio | 0.6-0.75 |
| Strong | 3+ confirming signals | 5% of portfolio | 0.75-0.9 |
| Conflicting | Any conflicting signal | Reduce by 50% | -0.15 per conflict |

**Best combinations (historically):**
1. Insider buying + unusual options + technical oversold → strongest long signal
2. Politician cluster buy + momentum breakout → strong long signal
3. Pre-earnings drift + unusual call buying + analyst upgrades → strong pre-earnings long
4. Dark pool selling + insider selling + technical breakdown → strong short signal
