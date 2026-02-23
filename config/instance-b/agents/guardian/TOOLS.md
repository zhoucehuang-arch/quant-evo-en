# Tool Notes

## Alpaca API
- Read-only: positions, account, orders for monitoring
- Never submit or cancel orders directly (that's Trader's job, except during HALT)

## GitHub
- Write to trading/metrics/ for performance data
- Write to trading/positions/ for position snapshots
- Read config/risk-params.json for threshold values
