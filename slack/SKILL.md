---
name: slack
description: Use this skill to read Slack messages and translate them to Korean, or translate Korean messages to English and post them to Slack. Activates for requests like "show me latest Slack messages in Korean", "translate and send to Slack", "Slack 메시지 가져와줘", or "슬랙에 보내줘".
---

# Slack Translation Integration

## Core Workflows

### 1. Fetch & Translate (English → Korean)

**Steps:**

1. Look up channel ID from "Available Channels" section (e.g., ni = G016KSW5GA1)
2. Run: `cd ~/.claude/skills/slack/scripts && uv run message_handler.py fetch -c CHANNEL_ID --json`
3. Parse JSON output (user, text, timestamp)
4. Translate text to Korean preserving technical terms
5. Present as: `[시간] 사용자: 번역된 메시지`
6. 내 이름은 byung yong kim 입니다

### 2. Translate & Post (Korean → English)

**Steps:**

1. Translate Korean text to natural, professional English
2. Look up channel ID from "Available Channels" section
3. Run: `cd ~/.claude/skills/slack/scripts && uv run message_handler.py post -c CHANNEL_ID "Translated text"`
4. Confirm success

## Available Channels

**Channel Name to ID Mapping:**

- **ni**: G016KSW5GA1
- **netops**: C0117N64B47
- **test**: C02NE1CNQLS

**Usage:**

```bash
# Fetch from ni channel
uv run message_handler.py fetch -c G016KSW5GA1 --json

# Post to netops channel
uv run message_handler.py post -c C0117N64B47 "Message"

# List all available channels
uv run message_handler.py channels
```

## Translation Guidelines

**Korean → English:**

- Professional, clear business language
- Adapt honorifics to English professional tone
- Preserve technical terms

**English → Korean:**

- Use 존댓말 for professional context
- Keep technical jargon in English (API, server, etc.)
- Maintain natural conversational tone

## Setup

```bash
# 1. Configure .env
SLACK_USER_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=C1234567890  # Optional default channel

# 2. Install
cd ~/.claude/skills/slack/scripts
uv sync
```

## Error Handling

- **not_in_channel**: Invite bot with `/invite @BotName`
- **invalid_auth**: Check `.env` token
- **channel_not_found**: Run `channels` command to list available

## Notes

- Messages displayed in chronological order (oldest first)
- Bot must be channel member to access messages
- Use `--json` flag for JSON output, omit for human-readable format
