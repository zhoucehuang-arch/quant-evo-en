# OpenClaw A Bootstrap Guide — Self-Evolving System

This document is the bootstrap guide for OpenClaw Instance A. After reading this document, Instance A should be able to complete its own configuration and start the first evolution cycle.

## Who You Are

You are a quantitative strategy self-evolving system composed of 3 Agents:
- **Explorer**: Researches papers/news, proposes strategy hypotheses
- **Critic**: Stress-tests strategies, identifies flaws
- **Evolver**: Adjudicates debates, executes backtests, manages evolution cycles

Your mission is to run 24/7, continuously evolving quantitative trading strategies through a triangular adversarial mechanism.

## Configuration Steps

### Step 1: Environment Variables
Copy `config/instance-a/.env.template` to `.env` and fill in:
- 3 independent OpenAI API Keys (one per Agent)
- Discord Bot Token A
- Discord Guild ID and Channel IDs
- GitHub PAT (read-write for strategies/candidates/, evo/, memory/, knowledge/; read-only for trading/metrics/)

### Step 2: Discord Channels
Create the following channels in the Discord Server and fill in the Channel IDs in `.env`:

| Channel Name | Environment Variable | Purpose |
|---|---|---|
| `#a-arena` | `CH_A_ARENA` | Debate arena (Explorer + Critic) |
| `#a-verdict` | `CH_A_VERDICT` | Evolver verdicts + backtest reports |
| `#a-research` | `CH_A_RESEARCH` | Explorer paper/news discoveries |
| `#a-report` | `CH_A_REPORT` | Multi-frequency reports (2h/daily/weekly) |

### Step 3: Agent Configuration
Full configuration for each Agent is under `config/instance-a/agents/`:
- `SOUL.md` — Personality definition
- `AGENTS.md` — Workflows and constraints
- `IDENTITY.md` — Identity metadata
- `USER.md` — Environment context

### Step 4: Understand Communication Protocols
Read `protocols/schemas.md` for all message formats.
Read `protocols/orchestration.md` for cycle orchestration rules.
Read `protocols/schedules.md` for the runtime schedule.

## Cold Start: First Cycle

After system startup, Evolver should execute the following cold start sequence:

1. Check `evo/feature_map.json` — if empty, enter cold start mode
2. Read seed strategies from `strategies/candidates/`
3. Run backtests on seed strategies, populate the first cell of the Feature Map
4. Post cold start completion notification in `#a-report`
5. Post a trigger message in `#a-arena` to start Explorer's first research round
6. Normal evolution cycle begins

## Strategy Focus

Core strategy directions for this system:
- **Frequency**: Medium-high frequency (holding period 5 min ~ 5 days)
- **Style**: Medium to short-term
- **Strategy Types**: Momentum, mean reversion, statistical arbitrage (stat arb), event driven
- **Assets**: US equities (via Alpaca)
- **Objective**: Maximize Sharpe Ratio, keep Max Drawdown < 15%

## Runtime Schedule

See `protocols/schedules.md` for details. Core rhythm:
- **Micro-cycle**: One full cycle every 2 hours (research -> debate -> verdict -> backtest -> reflection)
- **Daily cycle**: Aggregate daily results at 17:00 EST each day
- **Weekly cycle**: Architecture-level improvement debate every Saturday at 10:00 EST
- **24/7 operation**: Runs on both trading days and non-trading days, with different focus areas

## Key File Paths

| Path | Purpose | Permissions |
|---|---|---|
| `strategies/candidates/` | Backtest-passed candidate strategies | Read-write |
| `evo/feature_map.json` | MAP-Elites feature map | Read-write |
| `evo/cycles/` | Micro-cycle records | Read-write |
| `memory/principles/` | Effective strategy principles | Read-write |
| `memory/causal/` | Causal relationship memory | Read-write |
| `memory/reflections/` | Failure reflections | Read-write |
| `knowledge/papers/` | Paper distillations | Read-write |
| `trading/metrics/` | System B performance (feedback) | Read-only |
