# Strategy Philosophy & Guiding Principles

This document defines the core investment philosophy that ALL agents must respect.
Strategy evolution, optimization, and testing must stay aligned with these principles.
**This file is read-only for all agents — only the admin can modify it.**

---

## Core Philosophy

We are an **aggressive, mid-short term, mid-high frequency** quantitative trading system.
We seek alpha through **information asymmetry** and **speed of reaction**, not through
long-term fundamental value investing.

### Non-Negotiable Principles

1. **Short holding periods**: Minutes to days, rarely weeks. We do not hold positions for
   fundamental value to "play out." If the edge hasn't materialized within the expected
   window, we exit.

2. **Tight risk control**: Small stop-losses, quick take-profits. We prefer many small wins
   over occasional large wins. A 2:1 or 3:1 reward/risk ratio is the baseline.

3. **Information edge over model edge**: Our primary alpha comes from alternative data
   (politician trades, insider buying, unusual options flow, dark pool activity) and
   event catalysts — not from building the most sophisticated mathematical model.
   Models are tools to systematize the edge, not the edge itself.

4. **Multi-signal confluence**: We never trade on a single signal. The more independent
   confirming signals, the higher our conviction and position size. Conflicting signals
   reduce conviction or cancel the trade entirely.

5. **Pre-earnings is a first-class strategy**: Analyzing whether earnings are already
   priced in (IV vs historical vol, pre-earnings drift, insider activity, options
   positioning) is a core competency, not an afterthought.

6. **Event-driven speed**: Product launches, conferences, FDA decisions, macro releases —
   these create short windows of opportunity. We must be positioned before or react
   within minutes of the event.

7. **Continuous evolution, not revolution**: The system improves incrementally. Each cycle
   tests one hypothesis, learns from the result, and feeds back. We do not throw away
   what works to chase what's new.

---

## What We Are NOT

- We are NOT a long-term value investor (no multi-month holds based on DCF)
- We are NOT a pure HFT system (no sub-second latency requirements)
- We are NOT a passive index tracker
- We are NOT risk-averse — we accept higher drawdowns in exchange for higher returns,
  within defined limits

---

## Strategy Priority Order

When Explorer generates hypotheses, prioritize in this order:

1. **Alternative data + technical confluence** (insider/politician + price action)
   — Highest expected edge, hardest to crowd
2. **Event-driven catalysts** (earnings, launches, macro)
   — Time-bounded, high reward/risk when timed correctly
3. **Unusual options flow** (large sweeps, volume spikes)
   — Fast-decaying signal, requires quick execution
4. **Statistical arbitrage** (pairs, mean reversion)
   — Reliable but lower per-trade alpha
5. **Pure technical momentum**
   — Baseline strategy, always running, but lowest priority for new research

---

## Testing & Reflection Requirements

Every strategy, whether new or evolved, must go through rigorous testing:

1. **Backtest is necessary but not sufficient**: A good backtest does not guarantee live
   performance. Always assume 30-50% performance decay from backtest to live.

2. **Paper trading validation**: Every strategy must survive 5+ trading days of paper
   trading before promotion to production. No exceptions.

3. **Failure is expected and valuable**: Most hypotheses will be rejected. This is by
   design. Each rejection generates a causal reflection that improves future hypotheses.

4. **No strategy is sacred**: Even production strategies must be continuously monitored.
   If a strategy's rolling 30-day Sharpe drops below 0.2, it should be flagged for
   review. If it drops below 0 for 10 consecutive days, it should be withdrawn.

5. **Reflect on the process, not just the outcome**: A strategy that made money by luck
   (e.g., unexpected news moved the stock in our direction) is not a good strategy.
   Evolver's meta-reflection must distinguish between skill and luck.

6. **Test assumptions explicitly**: If a strategy assumes "insider buying predicts
   positive returns within 20 days," that assumption must be backtested independently
   before being used as a signal.

---

## Evolution Guardrails

To prevent the system from drifting away from these principles:

- **Evolver must read this file** at the start of every weekly cycle and verify that
  the current strategy portfolio is aligned with the priority order above.
- **Explorer must not propose** strategies with holding periods > 20 trading days
  unless explicitly approved by admin.
- **Critic must flag** any hypothesis that relies on a single signal source without
  confluence as CONDITIONAL_PASS at best.
- **If the system's overall win rate drops below 45% for a full week**, Evolver must
  trigger a special "philosophy alignment" debate to diagnose whether the system has
  drifted from these principles.
