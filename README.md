# Quant-Evo: Dual OpenClaw Self-Evolving Quantitative Trading System

A self-evolving quantitative trading system built on two independent OpenClaw instances. System A runs 24/7 strategy research, debate, and evolution; System B handles Alpaca paper trading execution and risk management. The two systems exchange data exclusively through this GitHub repository and use Discord channels for internal communication and human interaction.

## Architecture

```
OpenClaw A (Evolution)           GitHub (this repo)           OpenClaw B (Trading)
  Explorer ←┐                         │                      Operator
  Critic ───┤ Triangle Debate   strategies/candidates/ ──►      │
  Evolver ──┘                   strategies/production/ ──►   Trader
       │                        trading/metrics/ ◄──────   Guardian
       └──── evo/ memory/ knowledge/ ──────────────────────────┘
```

**6 Agents, 2 Instances, 10 Discord Channels, 1 GitHub Repository.**

## Core Features

- **Triangle Debate Evolution**: Explorer (aggressive) vs Critic (conservative) → Evolver (arbiter). Forced adversarial testing, no self-validation.
- **2-Hour Micro-Cycles**: Complete research → debate → verdict → backtest → reflection loop every 2 hours.
- **Multi-Frequency Reporting**: 2h / daily / weekly reports. Different schedules for trading days vs non-trading days. Reports to admin in Chinese.
- **Autonomous Learning**: Continuous scanning of arXiv, SSRN, quant blogs for new factors and strategies.
- **MAP-Elites Diversity**: Feature Map ensures behavioral diversity across the strategy library.
- **Strategy Focus**: Mid-to-high frequency, mid-to-short term. Momentum, mean reversion, statistical arbitrage, event-driven.

## Quick Start

### 1. Fork this repository
```bash
gh repo fork your-username/quant-evo --clone
```

### 2. Deploy OpenClaw A (Evolution System)
Read [BOOTSTRAP-A.md](BOOTSTRAP-A.md) — first boot guide for Instance A.

### 3. Deploy OpenClaw B (Trading System)
Read [BOOTSTRAP-B.md](BOOTSTRAP-B.md) — first boot guide for Instance B.

### 4. Create Discord Channels
Create 10 channels in your Discord Server. Fill Channel IDs into each instance's `.env`.

### 5. Launch
Once both instances start, Evolver will automatically trigger the first evolution cycle.

## Project Structure

```
quant-evo/
├── BOOTSTRAP-A.md           # Instance A first boot guide
├── BOOTSTRAP-B.md           # Instance B first boot guide
├── ARCHITECTURE.md          # Full architecture design
├── strategies/              # Strategy lifecycle management
│   ├── candidates/          # Backtest-passed candidates from System A
│   ├── staging/             # CI-validated, under paper trade verification
│   └── production/          # Live strategies executed by System B
├── evo/                     # Evolution state
│   ├── feature_map.json     # MAP-Elites feature map
│   ├── cycles/              # Micro-cycle records
│   └── debates/             # Debate archives
├── memory/                  # System memory
│   ├── principles/          # Validated strategy principles
│   ├── causal/              # Causal relationship memory
│   ├── reflections/         # Failure reflections
│   └── architecture/        # Architecture improvement records
├── knowledge/               # External knowledge
│   ├── papers/              # Distilled paper insights
│   ├── market/              # Market regime data
│   └── sources/             # Monitored information sources
├── trading/                 # Trading data
│   ├── metrics/             # Performance metrics
│   ├── logs/                # Execution logs
│   └── positions/           # Position snapshots
├── protocols/               # Communication protocols
│   ├── schemas.md           # Message JSON schemas
│   ├── orchestration.md     # Cycle orchestration rules
│   └── schedules.md         # Runtime schedules
├── config/                  # Shared configuration
│   ├── risk-params.json     # Risk parameters
│   ├── instance-a/          # Instance A config
│   └── instance-b/          # Instance B config
├── scripts/                 # Utility scripts
│   └── run_backtest.py      # Backtest runner
├── docs/                    # Operations docs
│   ├── error-recovery.md    # Error recovery procedures
│   └── health-check.md      # Health check definitions
└── .github/workflows/       # CI/CD
```
