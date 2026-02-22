# Dual OpenClaw Instance · Self-Evolution + Automated Investment · System Architecture Design

## 0. Design Constraints Review

| Constraint | Design Response |
|---|---|
| Dual-instance physical isolation | OpenClaw A / B independent processes, independent configs, independent bot tokens |
| Intra-instance Agent isolation | Each Agent has independent API Key, independent workspace, independent session |
| Minimalist and flat | A = 3 agents, B = 3 agents, 6 total |
| No self-dealing | 3-agent triangular game: Propose → Challenge → Adjudicate, forced trial-and-error |
| Bootstrapping | 3 agents supervise each other, cyclically driven, runs continuously without external triggers |
| Multi-frequency reporting | 2h micro-cycle report / daily summary / weekly strategy |
| DC channels = event bus + human-machine interaction | Agents listen/write to channels, admins can intervene at any time |
| GitHub = cloud storage + state machine | All state changes = git commit, sole cross-system sync channel |
| Each Agent has independent API Key | Prevents rate limit conflicts, costs are trackable, context isolation |

---

## 1. Overall Topology

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Discord Server                                │
│                                                                      │
│  ┌─── OpenClaw A (Self-Evolution) ─┐     ┌─── OpenClaw B (Investment) ─┐  │
│  │                           │         │                         │  │
│  │  Explorer ←──┐            │         │  Operator               │  │
│  │     │        │            │         │    │  ▲                 │  │
│  │     ▼        │            │         │    ▼  │                 │  │
│  │  Critic ─────┤  Triangular│         │  Trader  Guardian      │  │
│  │     │        │  Game      │         │                        │  │
│  │     ▼        │            │         │                         │  │
│  │  Evolver ────┘            │         └────────┬────────────────┘  │
│  │     │                     │                  │                   │
│  └─────┼─────────────────────┘                  │                   │
│        │                                        │                   │
│        │    ┌──────────────────────┐             │                   │
│        └───►│   GitHub Repository  │◄────────────┘                   │
│             │  (Single Source of   │                                │
│             │   Truth)             │                                │
│             └──────────────────────┘                                 │
└──────────────────────────────────────────────────────────────────────┘
```

**The two OpenClaw instances run completely independently, exchanging data only through the GitHub repository.**
**Discord serves as the human-machine interaction interface + Agent internal communication bus, but cross-system communication does not go through Discord.**

---

## 2. Agent Definitions (6 total, minimalist)

### OpenClaw A: Self-Evolution System (3 Agents)

The triangular game is the core mechanism. The three Agents have opposing personalities and keep each other in check:

| Agent | Codename | Personality | Model | Core Responsibility |
|---|---|---|---|---|
| Explorer | Explorer | Aggressive, divergent, alpha-seeking | GPT-5.3 Codex (Key A1) | Research papers/news → propose strategy hypotheses → discover new factors |
| Critic | Critic | Conservative, adversarial, safety-seeking | GPT-5.3 Codex (Key A2) | Stress testing → find vulnerabilities → prevent overfitting → veto inferior strategies |
| Evolver | Evolver | Rational, holistic, evolution-seeking | GPT-5.3 Codex (Key A3) | Adjudicate debates → execute backtests → manage evolution cycles → push results |

**Triangular Game Flow:**
```
Explorer proposes hypothesis
    │
    ▼
Critic challenges ──► Explorer responds with rebuttal
    │
    ▼
Critic final evaluation
    │
    ▼
Evolver comprehensive adjudication ──► APPROVE → Backtest → Push to GitHub
                                   ──► REJECT → Record reflection → Next round
                                   ──► REVISE → Send back to Explorer for revision
    │
    ▼
Evolver publishes cycle report → Triggers next round of Explorer research
    │
    ▼
(Loop, bootstrapping, never stops)
```

### OpenClaw B: Automated Investment System (3 Agents)

Modeled after the front-office / middle-office / back-office separation architecture of mature quantitative firms:

```
Quantitative Firm Analogy:
  Portfolio Manager (PM/CIO)  ←→  Operator
  Execution Desk              ←→  Trader
  Risk Management             ←→  Guardian
```

| Agent | Codename | Quant Firm Analogy | Personality | Model | Core Responsibility |
|---|---|---|---|---|---|
| Operator | Operator | PM / COO | Holistic vision, coordination-oriented, external interface | GPT-5.3 Codex (Key B1) | A↔B liaison · strategy deployment management · task scheduling · human-machine interaction · reporting |
| Trader | Trader | Execution Desk | Disciplined, precise, execution-oriented | GPT-5.3 Codex (Key B2) | Signal generation · order execution · position management |
| Guardian | Guardian | Risk Manager | Vigilant, conservative, risk-first | GPT-5.3 Codex (Key B3) | Real-time risk control · HALT authority · performance collection · compliance checks |

> Low-risk repetitive tasks (log archiving, scheduled snapshots, formatted reports) can be downgraded to Kimi K2.5 within the Agent internally to save costs.

**B System Triangular Division:**

```
                    ┌─────────────┐
                    │  Operator   │  ◄── Admin commands (DC #b-ops)
                    │             │  ──► Admin reports (DC #b-report)
                    └──┬──────┬───┘
                       │      │
            Strategy   │      │  Risk parameters
            deployment │      │  Performance summary
            Task sched │      │
                       ▼      ▼
              ┌────────┐      ┌──────────┐
              │ Trader │◄────►│ Guardian │
              │        │      │          │
              └───┬────┘      └────┬─────┘
                  │                │
                  ▼                ▼
             Alpaca API      trading/metrics/
             (Order exec)    (Performance written to GitHub)
```

**Operator's Core Responsibilities Expanded:**

1. **A↔B Liaison (Strategy Deployment Pipeline)**
   - Monitor GitHub `strategies/staging/` for new strategies
   - Validate strategy completeness (code is executable, risk parameters are complete)
   - Assign strategies to Trader for execution
   - Monitor staging strategy paper trading performance, trigger promotion to `production/` when criteria are met
   - Aggregate B system performance data, ensure A system can read it

2. **Task Scheduling and Coordination**
   - Trading hours: Ensure Trader and Guardian are running normally
   - Non-trading hours: Trigger Guardian to generate daily reports, archive logs
   - Exception handling: Coordinate recovery process after Guardian issues HALT

3. **Human-Machine Interaction (Admin Interface)**
   - Receive admin commands (manual deploy/withdraw strategies, adjust risk parameters, HALT/RESUME)
   - Generate structured reports (2h trading summary / daily report / weekly report)
   - Proactively notify admin on anomalies

**B System Complete Flow:**
```
GitHub strategies/production/ (Mature strategies pushed by A)
    │
    ▼
Operator: Pull new strategies → Validate → Assign to Trader
    │
    ▼
Trader: Read strategy → Get market data (Alpaca) → Generate signals → Execute orders
    │                                                │
    ▼                                                ▼
Trader → #b-desk: Signals + execution logs    Alpaca: Orders filled
    │
    ▼
Guardian: Real-time monitoring of positions/P&L/VaR/correlations
    │
    ├── Normal → Continue
    ├── WARNING → #b-risk alert, Operator notified
    └── HALT → #b-risk emergency stop, Trader cancels all pending
    │
    ▼
Guardian: Performance data commit → GitHub trading/metrics/
    │
    ▼
Operator: Aggregate performance → #b-report to admin
    │
    ▼
(A system's Evolver reads trading/metrics/, feeds back into evolution cycle)
```

---

## 3. Discord Channel Architecture

### Design Principles
- Each channel is bound to a specific Agent and data flow direction
- Admins can intervene by posting in any channel
- Minimize channel count: A system 4, B system 4, shared 2 = 10 total

### Channel List

**OpenClaw A Channels (Bot Token A):**

| Channel | Bound Agent | Purpose | Admin Can |
|---|---|---|---|
| `#a-arena` | Explorer + Critic | Debate arena: hypothesis proposal, challenges, responses | Observe debates, insert opinions |
| `#a-verdict` | Evolver | Adjudication results + backtest reports + strategy push notifications | Approve/reject strategy pushes |
| `#a-research` | Explorer | Paper/news discoveries, study notes | Specify research directions |
| `#a-report` | Evolver | 2h/daily/weekly reports | View progress, adjust priorities |

**OpenClaw B Channels (Bot Token B):**

Modeled after the front/middle/back-office channel isolation of quantitative firms:

| Channel | Bound Agent | Quant Firm Analogy | Purpose | Admin Can |
|---|---|---|---|---|
| `#b-ops` | Operator | PM Office | Strategy deployment notifications · A↔B sync status · task scheduling | Manually deploy/withdraw strategies, adjust parameters |
| `#b-desk` | Trader | Trading Desk | Trading signals · execution logs · position changes | Manual orders, close position commands |
| `#b-risk` | Guardian | Risk Desk | Risk alerts · HALT/RESUME · limit status | Manual HALT/RESUME, adjust limits |
| `#b-report` | Operator | Management Reporting | Performance daily report · strategy attribution · system status | View P&L, request special reports |

**Shared Channels (Both Bots can write):**

| Channel | Purpose | Admin Can |
|---|---|---|
| `#bridge` | Cross-system status sync notifications (strategy deployment/performance feedback) | View sync status |
| `#admin` | System health + admin global commands | Global HALT, system restart, priority adjustments |

---

## 4. GitHub Repository Structure (Single Source of Truth)

```
quant-evo/
│
├── strategies/
│   ├── candidates/        # Candidate strategies that passed Evolver backtests
│   ├── staging/           # CI validated, awaiting paper trading verification
│   └── production/        # Live, read and executed by Trader
│
├── evo/
│   ├── feature_map.json   # MAP-Elites feature map (versioned)
│   ├── cycles/            # Complete record of each micro-cycle
│   │   └── YYYY-MM-DD-HHMM.json
│   └── debates/           # Debate record archives
│       └── debate-NNNN.json
│
├── memory/
│   ├── principles/        # Validated effective strategy principles
│   ├── causal/            # Causal relationship memory (CLIN pattern)
│   ├── reflections/       # Failure reflections
│   └── architecture/      # System architecture improvement records
│
├── knowledge/
│   ├── papers/            # Paper extractions (structured JSON)
│   ├── market/            # Market regime classification
│   └── sources/           # Monitored information source list
│
├── trading/
│   ├── metrics/           # Performance data (written by Guardian)
│   │   ├── daily/
│   │   └── realtime/
│   ├── logs/              # Execution logs
│   └── positions/         # Position snapshots
│
├── config/
│   ├── instance-a/        # A instance config backup
│   ├── instance-b/        # B instance config backup
│   └── risk-params.json   # Risk parameters (shared by both systems)
│
└── .github/
    └── workflows/
        ├── validate-strategy.yml
        ├── promote-staging.yml
        └── daily-report.yml
```

**Permission Isolation:**
- A instance (GitHub PAT-A): Read/write `strategies/candidates/`, `evo/`, `memory/`, `knowledge/`; read-only `trading/metrics/`
- B instance (GitHub PAT-B): Read/write `strategies/staging/`, `strategies/production/`, `trading/`, `config/risk-params.json`; read-only `strategies/candidates/`
- GitHub Actions: Responsible for CI validation of `candidates/ → staging/`; `staging/ → production/` is actively triggered by Operator

---

## 5. Evolution Cycle Design

### 5.1 Micro-Cycle (2 Hours)

This is the system's heartbeat. Every 2 hours produces a quantifiable evolution outcome.

```
[T+0min] Evolver publishes previous round summary to #a-report
         Simultaneously triggers Explorer to begin new round
              │
[T+0~30min] Explorer research phase
         - Scan arXiv/SSRN/quant blogs for new publications
         - Read memory/principles/ and memory/causal/
         - Read trading/metrics/ (B system feedback)
         - Sample parent strategies from Feature Map
         - Generate strategy hypotheses, publish to #a-arena
              │
[T+30~60min] Debate phase (2 rounds)
         - Critic challenges in #a-arena (Round 1)
         - Explorer responds in #a-arena (Round 1)
         - Critic final evaluation in #a-arena (Round 2)
              │
[T+60~90min] Adjudication + Backtest phase
         - Evolver reads debate, produces adjudication to #a-verdict
         - If APPROVE: Execute backtest (30-day intraday data)
         - If REJECT: Record reflection to memory/reflections/
              │
[T+90~120min] Wrap-up phase
         - Backtest passed: commit to strategies/candidates/ + update Feature Map
         - Backtest failed: Generate causal reflection to memory/causal/
         - Evolver publishes 2h report to #a-report
         - Trigger next round
```

### 5.2 Daily Cycle (After Market Close Each Day)

```
Evolver aggregates all micro-cycle results for the day (~12 rounds)
    │
    ▼
Analyze Feature Map change trends
    │
    ▼
Read B system daily performance (trading/metrics/daily/)
    │
    ▼
Generate daily report to #a-report:
  - Today's evolution results: N new strategies, M parameter optimizations
  - Feature Map coverage changes
  - Live trading performance feedback summary
  - Suggested priority directions for tomorrow
    │
    ▼
commit daily report to evo/cycles/daily-YYYY-MM-DD.json
```

### 5.3 Weekly Cycle (Every Weekend)

```
Evolver aggregates all daily reports for the week
    │
    ▼
Explorer proposes architecture-level improvement hypotheses (not just strategy parameters, but system capability upgrades)
    │
    ▼
Triangular game (targeting architecture improvements)
    │
    ▼
Evolver produces weekly report to #a-report:
  - Weekly evolution summary
  - Strategy library quality changes
  - System architecture improvement suggestions
  - Strategic direction for next week
    │
    ▼
commit to memory/architecture/
```

---

## 6. Cross-System Integration: A → GitHub → Operator → B

Operator is B system's external interface, responsible for managing the entire strategy deployment pipeline:

```
A System (Evolver)                  GitHub                    B System (Operator → Trader)
     │                              │                           │
     ├── Strategy passes backtest ──────────► candidates/xxx.py            │
     │                              │                           │
     │                    GitHub Actions CI:                     │
     │                    - lint + syntax check                 │
     │                    - 6-month out-of-sample backtest      │
     │                    - Risk parameter validation           │
     │                              │                           │
     │                    CI passes → auto-merge                │
     │                    to staging/xxx.py ────────────────► Operator detects new strategy
     │                              │                           │
     │                              │                    Operator validates completeness
     │                              │                    Assigns to Trader for execution
     │                              │                    Notifies #b-ops
     │                              │                           │
     │                    Paper trading verification N days      │
     │                    (Guardian writes performance)          │
     │                              │                           │
     │                    Operator evaluates performance         │
     │                    Meets criteria → promote to production/│
     │                    Fails criteria → withdraw + feedback   │
     │                              │                           │
     │◄──── Performance feedback ◄──────── trading/metrics/ ◄──────────────┤
     │   (Evolver reads,                                  (Guardian collects,
     │    feeds back to evolution cycle)                   Operator aggregates)
```

**Key Change: Operator replaces some of GitHub Actions' automatic promotion functions.**
Promotion from staging → production is actively decided by Operator based on actual paper trading performance, rather than purely rule-triggered.
This more closely resembles the real process of a PM approving strategy go-live at a quantitative firm.

---

## 7. API Key Isolation Scheme

All Agents default to GPT-5.3 Codex; only low-risk repetitive subtasks (log archiving, formatted snapshots) are downgraded to Kimi K2.5.

| Agent | Instance | Default Model | API Key | Core Usage |
|---|---|---|---|---|
| Explorer | A | GPT-5.3 Codex | `OPENAI_KEY_A1` | Research + strategy generation (high creativity) |
| Critic | A | GPT-5.3 Codex | `OPENAI_KEY_A2` | Stress testing + risk analysis (high reasoning) |
| Evolver | A | GPT-5.3 Codex | `OPENAI_KEY_A3` | Adjudication + backtesting + reporting (high synthesis) |
| Operator | B | GPT-5.3 Codex | `OPENAI_KEY_B1` | Strategy deployment + task scheduling + reporting (high coordination) |
| Trader | B | GPT-5.3 Codex | `OPENAI_KEY_B2` | Signal generation + execution (high precision) |
| Guardian | B | GPT-5.3 Codex | `OPENAI_KEY_B3` | Risk monitoring + performance collection (high vigilance) |

Auxiliary model (on-demand downgrade):
| Model | Key | Usage |
|---|---|---|
| Kimi K2.5 | `KIMI_KEY_SHARED` | Log archiving, scheduled snapshots, formatted reports, and other low-risk tasks |

Each Key has independent billing, independent rate limits, independent context.
One Agent being rate-limited does not affect other Agents.

---

## 8. Autonomous Learning Capability Design

Explorer's learning pipeline (embedded in the micro-cycle research phase):

```
Source                      Processing Method                Storage Location
─────────────────────────────────────────────────────────────
arXiv RSS               Auto-scan + relevance scoring    knowledge/papers/
  (q-fin, cs.AI,        relevance > 0.5 → deep parsing
   cs.LG, cs.MA)        Extract factor formulas + pseudocode

SSRN                    Same as above                    knowledge/papers/

Quant blogs             Periodic scanning                knowledge/sources/
  (AQR, Two Sigma,      Extract strategy ideas +
   Man Group, DE Shaw)   market views

B system performance    Evolver reads                    Feeds back to memory/
  (Operator aggregates   Analyze strategy live            principles/ or
   writes to GitHub)     performance vs backtest          causal/
                        expectation deviation

Market data             Trader obtains via Alpaca        knowledge/market/
                        regime classification (trend/    (Operator aggregates
                        oscillation/high vol/low vol)    and writes)
```

**Learning is not a separate pipeline, but embedded in each micro-cycle's research phase.**
Explorer checks for new information every round, ensuring 24/7 continuous learning.

---

## 9. File Structure Overview

```
d:/hadan/openclaw/
├── openclaw/                    # Original framework (do not modify)
├── research report.md           # Research report
│
└── deploy/                      # All deployment configurations
    ├── instance-a/              # OpenClaw A Self-Evolution System
    │   ├── openclaw.json        # A instance main config
    │   ├── .env.template        # A instance environment variable template
    │   └── agents/
    │       ├── explorer/
    │       │   └── SOUL.md
    │       ├── critic/
    │       │   └── SOUL.md
    │       └── evolver/
    │           └── SOUL.md
    │
    ├── instance-b/              # OpenClaw B Automated Investment System
    │   ├── openclaw.json        # B instance main config
    │   ├── .env.template        # B instance environment variable template
    │   └── agents/
    │       ├── operator/
    │       │   └── SOUL.md
    │       ├── trader/
    │       │   └── SOUL.md
    │       └── guardian/
    │           └── SOUL.md
    │
    └── github-repo/             # GitHub repository content (pushed to remote)
        ├── strategies/
        │   ├── candidates/
        │   ├── staging/
        │   └── production/
        ├── evo/
        │   ├── feature_map.json
        │   ├── cycles/
        │   └── debates/
        ├── memory/
        │   ├── principles/
        │   ├── causal/
        │   ├── reflections/
        │   └── architecture/
        ├── knowledge/
        │   ├── papers/
        │   ├── market/
        │   └── sources/
        ├── trading/
        │   ├── metrics/
        │   ├── logs/
        │   └── positions/
        ├── config/
        │   └── risk-params.json
        └── .github/
            └── workflows/
```
