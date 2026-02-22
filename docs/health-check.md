# Health Check Definitions

## Check Frequency
- System A: At the end of each micro-cycle (~every 2h)
- System B: Every 30min during trading sessions, every 4h during non-trading sessions
- Results are published to the `#admin` channel

## Health Check Message Format

```json
{
  "type": "HEALTH_CHECK",
  "system": "A | B",
  "timestamp": "ISO8601",
  "status": "HEALTHY | DEGRADED | CRITICAL",
  "agents": {
    "explorer": { "status": "ok | timeout | error", "last_active": "ISO8601" },
    "critic": { "status": "ok | timeout | error", "last_active": "ISO8601" },
    "evolver": { "status": "ok | timeout | error", "last_active": "ISO8601" }
  },
  "services": {
    "github": { "status": "ok | error", "last_commit": "ISO8601" },
    "discord": { "status": "ok | error" },
    "llm_api": { "status": "ok | rate_limited | error", "requests_remaining": 1000 }
  },
  "metrics": {
    "cycles_last_24h": 12,
    "avg_cycle_duration_min": 105,
    "feature_map_coverage": 0.0048
  }
}
```

## System A Check Items

| Check Item | Healthy | Degraded | Critical |
|---|---|---|---|
| Explorer Response | Active within last 2h | Inactive for 2-4h | Inactive for >4h |
| Critic Response | Active within last 2h | Inactive for 2-4h | Inactive for >4h |
| Evolver Response | Active within last 2h | Inactive for 2-4h | Inactive for >4h |
| GitHub Connection | Push/pull normal | Occasional timeouts | Persistent failures |
| LLM API | Normal response | Occasional rate limiting | Persistent rate limiting/errors |
| Micro-cycle Frequency | >=10 cycles/day | 6-10 cycles/day | <6 cycles/day |
| Feature Map | Continuously growing | Stagnant for >24h | Data corrupted |

## System B Check Items

| Check Item | Healthy | Degraded | Critical |
|---|---|---|---|
| Alpaca Connection | API normal | Occasional timeouts | Persistent failures |
| Trader Response | Signals generated on time | Occasionally skipped | Persistently no signals |
| Guardian Response | Monitoring on time | Occasionally skipped | Persistently no monitoring |
| Operator Response | Normal scheduling | Delayed | No response |
| Position Consistency | Local = Alpaca | Occasional discrepancies | Persistently inconsistent |
| Daily Report Generation | Published on time | Delayed <1h | Not published |

## Degradation Handling

- **DEGRADED**: Publish WARNING in `#admin`, continue running
- **CRITICAL**: Publish CRITICAL in `#admin`, notify administrators
  - System A: Pause evolution cycle, wait for recovery
  - System B: Operator issues a precautionary HALT
