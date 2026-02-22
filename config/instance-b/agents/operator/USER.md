# User Context

## System Owner
The admin interacts with the system via Discord channels.

## System Positioning
This is the Automated Investment System (System B), interfacing with Alpaca for mid-to-high frequency, mid-to-short term paper trading.
It only receives mature strategies pushed by System A (Self-Evolution System) via GitHub.

## Key Constraints
- Trading: Alpaca Paper Trading (simulated)
- Strategy source: Read only from GitHub strategies/production/
- Risk control: Guardian holds independent HALT authority
- Performance data must be written back to GitHub trading/metrics/ for System A to learn from

## GitHub Repository
- Repo: ${GITHUB_REPO}
- System B read-write: strategies/staging/, strategies/production/, trading/
- System B read-only: strategies/candidates/, config/risk-params.json

## Alpaca Configuration
- Base URL: ${ALPACA_BASE_URL}
- Mode: Paper Trading (simulated)
