# Setup Guide: Deploying with OpenClaw

## Prerequisites

- Node.js >= 22
- Two machines (or two separate OpenClaw config directories on one machine)
- Discord server with bot tokens
- GitHub PAT for both instances
- OpenAI API keys (6 total, one per agent)
- Alpaca Paper Trading account (for System B)

## Step 1: Install OpenClaw

```bash
npm install -g openclaw@latest

# Run the onboarding wizard
openclaw onboard --install-daemon
```

## Step 2: Create Discord Server & Bots

### 2.1 Create Discord Server
Create a Discord server (e.g., "Quant-Evo") with these channels:

**System A channels:**
- `#a-arena` — Debate arena (Explorer + Critic)
- `#a-verdict` — Verdicts and backtest results (Evolver)
- `#a-research` — Research notes (Explorer)
- `#a-report` — Multi-frequency reports (Evolver)

**System B channels:**
- `#b-ops` — Operations and deployment (Operator)
- `#b-desk` — Trading signals and execution (Trader)
- `#b-risk` — Risk alerts and HALT (Guardian)
- `#b-report` — Performance reports (Operator)

**Shared channels:**
- `#bridge` — Cross-system sync notifications
- `#admin` — System health and admin commands

### 2.2 Create Two Discord Bots

Go to [Discord Developer Portal](https://discord.com/developers/applications):

1. Create **Bot A** (e.g., "QuantEvo-A"):
   - Enable "Message Content Intent" in Bot settings
   - Copy the bot token → save as `DISCORD_TOKEN_A`
   - Invite to your server with permissions: Send Messages, Read Message History, Manage Messages

2. Create **Bot B** (e.g., "QuantEvo-B"):
   - Same settings as above
   - Copy the bot token → save as `DISCORD_TOKEN_B`
   - Invite to your server

### 2.3 Get Channel & Guild IDs
Enable Developer Mode in Discord (Settings → Advanced → Developer Mode).
Right-click your server → Copy Server ID → this is your `GUILD_ID`.
Right-click each channel → Copy Channel ID.

## Step 3: Configure Instance A (Self-Evolution System)

### 3.1 Set Up Config Directory

```bash
# Create Instance A config directory
mkdir -p ~/.openclaw-a

# Clone the GitHub repo as reference
git clone https://github.com/zhoucehuang-arch/quant-evo-en.git ~/quant-evo

# Create workspace directories for each agent
mkdir -p ~/.openclaw-a/workspace-explorer
mkdir -p ~/.openclaw-a/workspace-critic
mkdir -p ~/.openclaw-a/workspace-evolver
```

### 3.2 Copy Agent Files to Workspaces

```bash
# Explorer
cp ~/quant-evo/config/instance-a/agents/explorer/SOUL.md ~/.openclaw-a/workspace-explorer/
cp ~/quant-evo/config/instance-a/agents/explorer/AGENTS.md ~/.openclaw-a/workspace-explorer/
cp ~/quant-evo/config/instance-a/agents/explorer/IDENTITY.md ~/.openclaw-a/workspace-explorer/
cp ~/quant-evo/config/instance-a/agents/explorer/USER.md ~/.openclaw-a/workspace-explorer/

# Critic
cp ~/quant-evo/config/instance-a/agents/critic/SOUL.md ~/.openclaw-a/workspace-critic/
cp ~/quant-evo/config/instance-a/agents/critic/AGENTS.md ~/.openclaw-a/workspace-critic/
cp ~/quant-evo/config/instance-a/agents/critic/IDENTITY.md ~/.openclaw-a/workspace-critic/
cp ~/quant-evo/config/instance-a/agents/critic/USER.md ~/.openclaw-a/workspace-critic/

# Evolver
cp ~/quant-evo/config/instance-a/agents/evolver/SOUL.md ~/.openclaw-a/workspace-evolver/
cp ~/quant-evo/config/instance-a/agents/evolver/AGENTS.md ~/.openclaw-a/workspace-evolver/
cp ~/quant-evo/config/instance-a/agents/evolver/IDENTITY.md ~/.openclaw-a/workspace-evolver/
cp ~/quant-evo/config/instance-a/agents/evolver/USER.md ~/.openclaw-a/workspace-evolver/
```

### 3.3 Create openclaw.json for Instance A

Create `~/.openclaw-a/openclaw.json`:

```json
{
  "providers": [
    {
      "id": "openai-codex-a1",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_A1}"
    },
    {
      "id": "openai-codex-a2",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_A2}"
    },
    {
      "id": "openai-codex-a3",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_A3}"
    },
    {
      "id": "kimi-fallback",
      "type": "openai-compatible",
      "model": "kimi-k2.5",
      "apiKey": "${KIMI_KEY_SHARED}",
      "baseUrl": "https://api.moonshot.cn/v1"
    }
  ],
  "agents": {
    "list": [
      {
        "id": "explorer",
        "name": "Explorer",
        "workspace": "~/.openclaw-a/workspace-explorer",
        "provider": "openai-codex-a1"
      },
      {
        "id": "critic",
        "name": "Critic",
        "workspace": "~/.openclaw-a/workspace-critic",
        "provider": "openai-codex-a2"
      },
      {
        "id": "evolver",
        "name": "Evolver",
        "workspace": "~/.openclaw-a/workspace-evolver",
        "provider": "openai-codex-a3"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "explorer",
      "match": { "channel": "discord", "channelId": "<#a-arena-channel-id>" }
    },
    {
      "agentId": "explorer",
      "match": { "channel": "discord", "channelId": "<#a-research-channel-id>" }
    },
    {
      "agentId": "critic",
      "match": { "channel": "discord", "channelId": "<#a-arena-channel-id>" }
    },
    {
      "agentId": "evolver",
      "match": { "channel": "discord", "channelId": "<#a-verdict-channel-id>" }
    },
    {
      "agentId": "evolver",
      "match": { "channel": "discord", "channelId": "<#a-report-channel-id>" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "token": "${DISCORD_TOKEN_A}",
      "groupPolicy": "allowlist",
      "guilds": {
        "<your-guild-id>": {
          "requireMention": false,
          "channels": {
            "<#a-arena-channel-id>": { "allow": true },
            "<#a-verdict-channel-id>": { "allow": true },
            "<#a-research-channel-id>": { "allow": true },
            "<#a-report-channel-id>": { "allow": true },
            "<#bridge-channel-id>": { "allow": true },
            "<#admin-channel-id>": { "allow": true }
          }
        }
      }
    }
  },
  "heartbeat": {
    "interval": 7200000
  }
}
```

### 3.4 Set Environment Variables for Instance A

Create `~/.openclaw-a/.env`:

```bash
OPENAI_KEY_A1=sk-your-key-1
OPENAI_KEY_A2=sk-your-key-2
OPENAI_KEY_A3=sk-your-key-3
KIMI_KEY_SHARED=your-kimi-key
DISCORD_TOKEN_A=your-discord-bot-a-token
GITHUB_TOKEN=ghp_your-github-pat
GITHUB_REPO=zhoucehuang-arch/quant-evo-en
```

### 3.5 Start Instance A

```bash
# Set config directory
export OPENCLAW_CONFIG_DIR=~/.openclaw-a

# Start the gateway
openclaw gateway run --port 18789 --verbose
```

## Step 4: Configure Instance B (Automated Investment System)

### 4.1 Set Up Config Directory

```bash
mkdir -p ~/.openclaw-b
mkdir -p ~/.openclaw-b/workspace-operator
mkdir -p ~/.openclaw-b/workspace-trader
mkdir -p ~/.openclaw-b/workspace-guardian
```

### 4.2 Copy Agent Files to Workspaces

```bash
# Operator
cp ~/quant-evo/config/instance-b/agents/operator/SOUL.md ~/.openclaw-b/workspace-operator/
cp ~/quant-evo/config/instance-b/agents/operator/AGENTS.md ~/.openclaw-b/workspace-operator/
cp ~/quant-evo/config/instance-b/agents/operator/IDENTITY.md ~/.openclaw-b/workspace-operator/
cp ~/quant-evo/config/instance-b/agents/operator/USER.md ~/.openclaw-b/workspace-operator/

# Trader
cp ~/quant-evo/config/instance-b/agents/trader/SOUL.md ~/.openclaw-b/workspace-trader/
cp ~/quant-evo/config/instance-b/agents/trader/AGENTS.md ~/.openclaw-b/workspace-trader/
cp ~/quant-evo/config/instance-b/agents/trader/IDENTITY.md ~/.openclaw-b/workspace-trader/
cp ~/quant-evo/config/instance-b/agents/trader/USER.md ~/.openclaw-b/workspace-trader/

# Guardian
cp ~/quant-evo/config/instance-b/agents/guardian/SOUL.md ~/.openclaw-b/workspace-guardian/
cp ~/quant-evo/config/instance-b/agents/guardian/AGENTS.md ~/.openclaw-b/workspace-guardian/
cp ~/quant-evo/config/instance-b/agents/guardian/IDENTITY.md ~/.openclaw-b/workspace-guardian/
cp ~/quant-evo/config/instance-b/agents/guardian/USER.md ~/.openclaw-b/workspace-guardian/
```

### 4.3 Create openclaw.json for Instance B

Create `~/.openclaw-b/openclaw.json`:

```json
{
  "providers": [
    {
      "id": "openai-codex-b1",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_B1}"
    },
    {
      "id": "openai-codex-b2",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_B2}"
    },
    {
      "id": "openai-codex-b3",
      "type": "openai",
      "model": "gpt-5.3-codex",
      "apiKey": "${OPENAI_KEY_B3}"
    },
    {
      "id": "kimi-fallback",
      "type": "openai-compatible",
      "model": "kimi-k2.5",
      "apiKey": "${KIMI_KEY_SHARED}",
      "baseUrl": "https://api.moonshot.cn/v1"
    }
  ],
  "agents": {
    "list": [
      {
        "id": "operator",
        "name": "Operator",
        "workspace": "~/.openclaw-b/workspace-operator",
        "provider": "openai-codex-b1"
      },
      {
        "id": "trader",
        "name": "Trader",
        "workspace": "~/.openclaw-b/workspace-trader",
        "provider": "openai-codex-b2"
      },
      {
        "id": "guardian",
        "name": "Guardian",
        "workspace": "~/.openclaw-b/workspace-guardian",
        "provider": "openai-codex-b3"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "operator",
      "match": { "channel": "discord", "channelId": "<#b-ops-channel-id>" }
    },
    {
      "agentId": "operator",
      "match": { "channel": "discord", "channelId": "<#b-report-channel-id>" }
    },
    {
      "agentId": "trader",
      "match": { "channel": "discord", "channelId": "<#b-desk-channel-id>" }
    },
    {
      "agentId": "guardian",
      "match": { "channel": "discord", "channelId": "<#b-risk-channel-id>" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "token": "${DISCORD_TOKEN_B}",
      "groupPolicy": "allowlist",
      "guilds": {
        "<your-guild-id>": {
          "requireMention": false,
          "channels": {
            "<#b-ops-channel-id>": { "allow": true },
            "<#b-desk-channel-id>": { "allow": true },
            "<#b-risk-channel-id>": { "allow": true },
            "<#b-report-channel-id>": { "allow": true },
            "<#bridge-channel-id>": { "allow": true },
            "<#admin-channel-id>": { "allow": true }
          }
        }
      }
    }
  },
  "heartbeat": {
    "interval": 300000
  }
}
```

### 4.4 Set Environment Variables for Instance B

Create `~/.openclaw-b/.env`:

```bash
OPENAI_KEY_B1=sk-your-key-4
OPENAI_KEY_B2=sk-your-key-5
OPENAI_KEY_B3=sk-your-key-6
KIMI_KEY_SHARED=your-kimi-key
DISCORD_TOKEN_B=your-discord-bot-b-token
GITHUB_TOKEN=ghp_your-github-pat
GITHUB_REPO=zhoucehuang-arch/quant-evo-en
ALPACA_KEY_ID=your-alpaca-key-id
ALPACA_SECRET_KEY=your-alpaca-secret-key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### 4.5 Start Instance B

```bash
export OPENCLAW_CONFIG_DIR=~/.openclaw-b
openclaw gateway run --port 18790 --verbose
```

## Step 5: Clone the Shared GitHub Repo

Both instances need access to the shared repo for data exchange:

```bash
# Clone on Instance A's machine
git clone https://github.com/zhoucehuang-arch/quant-evo-en.git ~/quant-evo-workspace

# Clone on Instance B's machine (if different)
git clone https://github.com/zhoucehuang-arch/quant-evo-en.git ~/quant-evo-workspace
```

The agents will read/write to this repo according to their permissions defined in USER.md.

## Step 6: Verify Setup

```bash
# Check Instance A
OPENCLAW_CONFIG_DIR=~/.openclaw-a openclaw doctor
OPENCLAW_CONFIG_DIR=~/.openclaw-a openclaw agents list --bindings
OPENCLAW_CONFIG_DIR=~/.openclaw-a openclaw channels status --probe

# Check Instance B
OPENCLAW_CONFIG_DIR=~/.openclaw-b openclaw doctor
OPENCLAW_CONFIG_DIR=~/.openclaw-b openclaw agents list --bindings
OPENCLAW_CONFIG_DIR=~/.openclaw-b openclaw channels status --probe
```

## Step 7: Bootstrap the System

Once both gateways are running and connected to Discord:

1. Go to `#a-report` channel in Discord
2. Send a message to Evolver: "Read BOOTSTRAP-A.md from the GitHub repo and begin your first micro-cycle"
3. Evolver will read the bootstrap guide and start the self-evolution loop
4. Go to `#b-ops` channel
5. Send a message to Operator: "Read BOOTSTRAP-B.md from the GitHub repo and begin monitoring"
6. Operator will initialize and start watching for strategies

## Architecture Recap

```
Instance A (port 18789)          Instance B (port 18790)
├── Explorer → #a-arena          ├── Operator → #b-ops, #b-report
├── Critic   → #a-arena          ├── Trader   → #b-desk
├── Evolver  → #a-verdict,       ├── Guardian → #b-risk
│              #a-report          │
└── Shared: #bridge, #admin      └── Shared: #bridge, #admin

         ↕ GitHub Repo (quant-evo-en) ↕
         strategies/ evo/ memory/ trading/
```

## Troubleshooting

- **Bot not responding**: Check `openclaw channels status --probe` and ensure Message Content Intent is enabled
- **Agent not routing**: Verify channel IDs in bindings match actual Discord channel IDs
- **API rate limits**: Each agent has its own API key, so rate limits are isolated
- **GitHub sync issues**: Check GITHUB_TOKEN permissions (needs repo read/write)
- **Alpaca connection**: Verify ALPACA_KEY_ID and ALPACA_SECRET_KEY are for paper trading
