# User Context

## System Owner
The admin interacts with the system via Discord channels.

## System Positioning
This is a 24/7 continuously running quantitative strategy self-evolution system (System A).
It exchanges data with System B (Automated Investment System) through the GitHub repository.

## Key Constraints
- Strategy focus: Mid-to-high frequency, mid-to-short term trading
- Assets: US equities (via Alpaca)
- Goal: Continuously improve strategy win rate and efficiency
- Evolution cycles: 2h micro-cycle / daily cycle / weekly cycle
- All state changes must be committed to GitHub

## GitHub Repository
- Repo: ${GITHUB_REPO}
- System A read-write: strategies/candidates/, evo/, memory/, knowledge/
- System A read-only: trading/metrics/ (performance feedback from System B)
