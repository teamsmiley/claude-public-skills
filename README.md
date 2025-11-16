# claude code skill

## slack

### Setup

```bash
# 1. Configure .env
cd ~/.claude/skills/slack/scripts
cp .env.example .env
vi .env

SLACK_USER_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=xxx  # Optional default channel

# 2. Install
cd ~/.claude/skills/slack/scripts
uv sync
```
