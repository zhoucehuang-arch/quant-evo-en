# Tool Notes

## Alpaca API
- Base URL: ${ALPACA_BASE_URL}
- Always verify account status before submitting orders
- Use limit orders by default; market orders only when strategy explicitly requires
- Never submit orders within 15min of market open/close

## GitHub
- Read strategies/production/ and strategies/staging/ for active strategies
- Write to trading/logs/ for execution records
