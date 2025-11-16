#!/usr/bin/env python3
"""
Slack API Module
Core Slack API functionality for fetching and posting messages
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
  from slack_sdk import WebClient
  from slack_sdk.errors import SlackApiError
except ImportError:
  print("Error: slack-sdk is not installed.")
  print("Install it with: pip install slack-sdk")
  sys.exit(1)


def load_env():
  """Load environment variables from .env file if exists"""
  # Check skill directory first
  skill_dir = Path(__file__).parent.parent
  env_file = skill_dir / 'assets' / '.env'

  # Fallback to script directory
  if not env_file.exists():
    env_file = Path(__file__).parent / '.env'

  if env_file.exists():
    with open(env_file) as f:
      for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
          key, value = line.split('=', 1)
          os.environ[key.strip()] = value.strip()


def get_slack_client():
  """Initialize and return Slack client"""
  load_env()

  token = os.getenv('SLACK_USER_TOKEN')
  if not token:
    raise EnvironmentError(
        "SLACK_USER_TOKEN environment variable not set.\n"
        "Set it with: export SLACK_USER_TOKEN='xoxb-your-token'\n"
        "Or create ~/.claude/skills/slack2/assets/.env file"
    )

  return WebClient(token=token)


def get_channel_id():
  """Get channel ID from environment"""
  load_env()

  channel_id = os.getenv('SLACK_CHANNEL_ID')
  if not channel_id:
    raise EnvironmentError(
        "SLACK_CHANNEL_ID environment variable not set.\n"
        "Set it with: export SLACK_CHANNEL_ID='C1234567890'\n"
        "Or create ~/.claude/skills/slack2/assets/.env file"
    )

  return channel_id


def fetch_messages(channel_id=None, limit=10):
  """
  Fetch latest messages from Slack channel

  Args:
      channel_id: Slack channel ID (e.g., 'C1234567890', 'G016KSW5GA1')
      limit: Number of messages to fetch (default: 10)

  Returns:
      list: List of message dictionaries with user, text, timestamp
  """
  client = get_slack_client()
  if channel_id is None:
    channel_id = get_channel_id()

  try:
    result = client.conversations_history(
        channel=channel_id,
        limit=limit
    )

    messages = []
    for msg in result['messages']:
      user_id = msg.get('user', 'Unknown')
      text = msg.get('text', '')
      timestamp = msg.get('ts', '')

      # Get user info
      try:
        user_info = client.users_info(user=user_id)
        username = user_info['user']['real_name'] or user_info['user']['name']
      except:
        username = user_id

      # Convert timestamp
      try:
        dt = datetime.fromtimestamp(float(timestamp))
        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
      except:
        time_str = timestamp

      messages.append({
          'user': username,
          'text': text,
          'timestamp': time_str
      })

    # Reverse to show oldest first (chronological order)
    return list(reversed(messages))

  except SlackApiError as e:
    raise Exception(f"Error fetching messages: {e.response['error']}")


def post_message(text, channel_id=None):
  """
  Post a message to Slack channel

  Args:
      text: Message text to post
      channel_id: Slack channel ID (e.g., 'C1234567890', 'G016KSW5GA1')

  Returns:
      dict: Response with timestamp and channel info
  """
  client = get_slack_client()
  if channel_id is None:
    channel_id = get_channel_id()

  try:
    result = client.chat_postMessage(
        channel=channel_id,
        text=text
    )

    return {
        'success': True,
        'timestamp': result['ts'],
        'channel': result['channel']
    }

  except SlackApiError as e:
    raise Exception(f"Error posting message: {e.response['error']}")


def list_channels():
  """
  List available channels

  Returns:
      list: List of channel dictionaries with name and id
  """
  client = get_slack_client()

  try:
    result = client.conversations_list(
        types="public_channel,private_channel"
    )

    channels = []
    for channel in result['channels']:
      channels.append({
          'name': channel['name'],
          'id': channel['id']
      })

    return channels

  except SlackApiError as e:
    raise Exception(f"Error listing channels: {e.response['error']}")
