# Error Recovery Procedures

## 1. Agent Unresponsive (Timeout)

**Detection**: Evolver sends a message in `#a-arena` and receives no response within 20 minutes.

**Recovery**:
1. Evolver sends `TIMEOUT_PING` to `#a-arena`
2. Wait 10 minutes
3. Still no response -> Skip the current round, log to `#admin`
4. Trigger the next micro-cycle
5. If 3 consecutive rounds time out -> Send CRITICAL alert to administrators in `#admin`

**System B**: When Operator detects Trader or Guardian is unresponsive:
1. Send alert in `#b-ops`
2. If Trader is unresponsive -> Do not generate new signals, existing positions are maintained
3. If Guardian is unresponsive -> Operator issues a precautionary HALT

## 2. GitHub Unavailable

**Detection**: Git push/pull fails.

**Recovery**:
1. Retry 3 times with 30-second intervals
2. Still failing -> Temporarily store data in the Agent's local memory/
3. Send alert in `#admin`
4. Evolution cycle continues running (using locally cached Feature Map)
5. After GitHub recovers, batch-sync the temporarily stored data

**System B**:
- Trader continues execution using locally cached strategies
- Guardian temporarily stores performance data locally
- Operator notifies administrators in `#b-ops`

## 3. Alpaca API Unavailable

**Detection**: API calls return 5xx or time out.

**Recovery**:
1. Retry 3 times with 10-second intervals
2. Still failing -> Trader stops generating new signals
3. Guardian issues WARNING (unable to obtain real-time data)
4. Operator notifies administrators in `#b-ops`
5. Do not cancel existing orders (they may have already been executed on the Alpaca side)
6. After API recovers, Trader syncs position state before resuming signal generation

## 4. LLM API Rate Limiting

**Detection**: 429 Too Many Requests.

**Recovery**:
1. Wait according to the `Retry-After` value returned by the API
2. If one Agent is rate-limited, it does not affect other Agents (independent keys)
3. The rate-limited Agent skips its current task during the wait period
4. Log the rate-limiting event in `#admin`
5. If rate limiting is frequent -> Consider downgrading to Kimi K2.5 for low-priority tasks

## 5. Strategy Execution Anomaly

**Detection**: Trader throws an exception while executing strategy code.

**Recovery**:
1. Log the exception to `#b-desk` and `trading/logs/`
2. Skip the current signal for that strategy
3. If the same strategy throws exceptions 3 consecutive times -> Operator automatically revokes the strategy
4. Notify `#b-ops` and `#admin`
5. Feed exception information back to GitHub `memory/reflections/` for System A to learn from

## 6. Data Inconsistency

**Detection**: Feature Map version conflict, position data inconsistent with Alpaca.

**Recovery**:
- Feature Map: The latest version on GitHub takes precedence, local cache is invalidated
- Positions: Alpaca API response takes precedence, overwriting local records
- Log the inconsistency event in `#admin`
