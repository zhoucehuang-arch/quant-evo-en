# Cycle Orchestration Rules

## Core Principles
- **Event-driven**: Agents act by listening to Discord channel messages; no external cron dependency
- **Self-driving loop**: Evolver's periodic reports automatically trigger Explorer's next round, forming a perpetual loop
- **Message as trigger**: Messages with specific `type` fields trigger specific Agent actions

---

## System A: Evolution Cycle Orchestration

### Micro-Cycle (2 hours)

```
Timeline        Channel         Message Type              Triggered Agent
────────────────────────────────────────────────────────────────
T+0min     #a-arena     CYCLE_TRIGGER           → Explorer begins research
T+0~30min  (Explorer internal work: scan papers, read memory, sample parent strategies)
T+30min    #a-arena     HYPOTHESIS (round 1)    → Critic begins assessment
T+30~45min (Critic internal work: stress testing)
T+45min    #a-arena     RISK_ASSESSMENT (r1)    → Explorer prepares response
T+45~55min (Explorer internal work: prepare rebuttal)
T+55min    #a-arena     REBUTTAL (round 2)      → Critic final assessment
T+55~70min (Critic internal work: final assessment)
T+70min    #a-arena     RISK_ASSESSMENT (r2)    → Evolver begins verdict
T+70~90min (Evolver internal work: verdict + backtest)
T+90min    #a-verdict   VERDICT                 → (recorded)
T+100min   #a-report    MICRO_CYCLE_REPORT      → (reported)
T+105min   #a-arena     CYCLE_TRIGGER           → Explorer begins next round
────────────────────────────────────────────────────────────────
Total duration: ~105 minutes, with 15-minute buffer = 2-hour cycle
```

### Trigger Chain
```
Evolver CYCLE_TRIGGER → Explorer HYPOTHESIS → Critic RISK_ASSESSMENT(r1)
→ Explorer REBUTTAL → Critic RISK_ASSESSMENT(r2) → Evolver VERDICT
→ Evolver MICRO_CYCLE_REPORT → Evolver CYCLE_TRIGGER → (loop)
```

### Timeout Handling
- If an Agent does not respond within the expected time (exceeds 20 minutes):
  - Evolver sends a `TIMEOUT_PING` message in `#a-arena`
  - If still no response after another 10 minutes, Evolver skips the current round
  - The timeout event is logged to `#admin` and `memory/reflections/`
  - The next round is triggered

### Daily Cycle Trigger
- Evolver internal timer: when UTC time = 22:00 (EST 17:00)
- After completing the current micro-cycle, insert daily report generation
- Normal micro-cycles resume after the daily report is complete

### Weekly Cycle Trigger
- Evolver internal timer: when UTC time = Saturday 15:00 (EST 10:00)
- Pause normal micro-cycles
- Initiate architecture-level improvement debate (special CYCLE_TRIGGER with `mode: "architecture"`)
- Normal micro-cycles resume after the weekly report is complete

---

## System B: Trading Cycle Orchestration

### Trading Day Flow

```
Time (EST)    Channel       Action                      Agent
────────────────────────────────────────────────────────────
09:15      #b-ops      PRE_MARKET_CHECK             Operator
09:30      #b-desk     Begin signal generation loop  Trader (every 15min)
09:30      #b-risk     Begin risk monitoring loop    Guardian (every 5min)
Every 15m  #b-desk     SIGNAL + EXECUTION           Trader
Every 5m   #b-risk     RISK_ALERT (if needed)       Guardian
Every 2h   #b-report   TRADING_SUMMARY              Operator
16:00      #b-ops      MARKET_CLOSE                 Operator
16:15      #b-desk     Stop signal generation        Trader
16:30      #b-report   DAILY_TRADING_REPORT         Operator
16:30      (GitHub)    commit trading/metrics/       Guardian
────────────────────────────────────────────────────────────
```

### Non-Trading Day Flow
```
Every 4h       #b-ops      CHECK_NEW_STRATEGIES     Operator (check GitHub)
Every 12h      #b-risk     OVERNIGHT_RISK_CHECK     Guardian
Sat 10:00      #b-report   WEEKLY_TRADING_REPORT    Operator
```

### HALT Recovery Flow
```
Guardian HALT → Trader stops → Operator notifies admin
    │
    ▼
Wait for RESUME (from admin or Operator)
    │
    ▼
Operator RESUME → Guardian confirms → Trader resumes
```

---

## Cross-System Orchestration (via GitHub)

```
A: Evolver commit → strategies/candidates/
    │
    ▼
GitHub Actions CI → Validation passes → strategies/staging/
    │
    ▼
B: Operator detects (every 15min on trading days, every 4h on non-trading days) → Assigns to Trader
    │
    ▼
B: Guardian collects performance → trading/metrics/
    │
    ▼
A: Evolver reads (during each micro-cycle's research phase) → Feeds back into evolution loop
```

**Polling Frequency:**
- Operator checks staging for new strategies: every 15min on trading days, every 4h on non-trading days
- Evolver reads trading/metrics: every micro-cycle (every 2h)
- Guardian writes metrics: every 5min on trading days (realtime), after market close (daily)
