# Discord Channel Permissions Matrix

## Bot A (QuantEvo-A) Permissions

| Channel | Read | Write | Manage Messages |
|---|---|---|---|
| #a-arena | ✅ | ✅ | ❌ |
| #a-verdict | ✅ | ✅ | ❌ |
| #a-research | ✅ | ✅ | ❌ |
| #a-report | ✅ | ✅ | ❌ |
| #b-ops | ❌ | ❌ | ❌ |
| #b-desk | ❌ | ❌ | ❌ |
| #b-risk | ❌ | ❌ | ❌ |
| #b-report | ❌ | ❌ | ❌ |
| #bridge | ✅ | ✅ | ❌ |
| #admin | ✅ | ✅ | ❌ |

## Bot B (QuantEvo-B) Permissions

| Channel | Read | Write | Manage Messages |
|---|---|---|---|
| #a-arena | ❌ | ❌ | ❌ |
| #a-verdict | ❌ | ❌ | ❌ |
| #a-research | ❌ | ❌ | ❌ |
| #a-report | ❌ | ❌ | ❌ |
| #b-ops | ✅ | ✅ | ❌ |
| #b-desk | ✅ | ✅ | ❌ |
| #b-risk | ✅ | ✅ | ❌ |
| #b-report | ✅ | ✅ | ❌ |
| #bridge | ✅ | ✅ | ❌ |
| #admin | ✅ | ✅ | ❌ |

## Admin (Human) Permissions

| Channel | Read | Write | Manage Messages |
|---|---|---|---|
| All channels | ✅ | ✅ | ✅ |

## Discord Server Setup Commands

```bash
# After creating the server and channels, set permissions via Discord UI:
# 1. Server Settings → Roles → Create "Bot-A" and "Bot-B" roles
# 2. For each channel, set role-specific permissions:
#    - Bot-A role: deny all on #b-* channels
#    - Bot-B role: deny all on #a-* channels
#    - Both bots: allow read+write on #bridge and #admin
# 3. Assign Bot-A role to QuantEvo-A bot
# 4. Assign Bot-B role to QuantEvo-B bot
```

## Agent-to-Channel Binding (Within Each Bot)

### Bot A Internal Routing
| Agent | Primary Channel | Secondary Channels |
|---|---|---|
| Explorer | #a-arena | #a-research |
| Critic | #a-arena | — |
| Evolver | #a-verdict | #a-report, #a-arena (triggers only) |

### Bot B Internal Routing
| Agent | Primary Channel | Secondary Channels |
|---|---|---|
| Operator | #b-ops | #b-report, #bridge |
| Trader | #b-desk | — |
| Guardian | #b-risk | — |

Note: Agent routing is handled by OpenClaw's binding configuration in openclaw.json, not by Discord permissions. Discord permissions control which BOT can access which channel; bindings control which AGENT within a bot handles messages from which channel.
