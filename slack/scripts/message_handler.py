#!/usr/bin/env python3
"""
Slack Message Handler
CLI tool for fetching and posting Slack messages
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path to import slack_api
sys.path.insert(0, str(Path(__file__).parent))

try:
  import slack_api
except ImportError:
  print("Error: Could not import slack_api module")
  sys.exit(1)


def cmd_fetch(args):
  """Fetch messages from Slack"""
  try:
    messages = slack_api.fetch_messages(
        channel_id=args.channel,
        limit=args.limit
    )

    if args.format == 'json':
      print(json.dumps(messages, ensure_ascii=False, indent=2))
    else:
      # Human-readable format
      print(f"\n📬 Latest {len(messages)} messages:\n")
      for i, msg in enumerate(messages, 1):
        print(f"{i}. [{msg['timestamp']}] {msg['user']}:")
        print(f"   {msg['text']}\n")

  except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)


def cmd_post(args):
  """Post a message to Slack"""
  try:
    # Get message from args or stdin
    if args.message:
      message = ' '.join(args.message)
    else:
      print("Enter message (Ctrl+D to send):")
      message = sys.stdin.read().strip()

    if not message:
      print("❌ Error: No message provided", file=sys.stderr)
      sys.exit(1)

    result = slack_api.post_message(
        text=message,
        channel_id=args.channel
    )

    print(f"✅ Message posted successfully!")
    print(f"   Timestamp: {result['timestamp']}")
    print(f"   Channel: {result['channel']}")

  except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)


def cmd_channels(args):
  """List available channels"""
  try:
    channels = slack_api.list_channels()

    if args.format == 'json':
      print(json.dumps(channels, ensure_ascii=False, indent=2))
    else:
      print(f"\n📋 Available channels ({len(channels)}):\n")
      for ch in channels:
        print(f"  • {ch['name']}: {ch['id']}")

  except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)


def main():
  parser = argparse.ArgumentParser(
      description='Slack message handler for Claude Code',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog="""
Examples:
  %(prog)s fetch                         # Fetch from default channel
  %(prog)s fetch -c G016KSW5GA1          # Fetch from ni channel
  %(prog)s fetch -c C0117N64B47 -n 10    # Fetch 10 from netops
  %(prog)s fetch --json                  # Output as JSON
  %(prog)s post "Hello"                  # Post to default channel
  %(prog)s post -c G016KSW5GA1 "Hello"   # Post to ni channel
  %(prog)s channels                      # List all channels
        """
  )

  subparsers = parser.add_subparsers(dest='command', help='Command to execute')

  # Fetch command
  fetch_parser = subparsers.add_parser('fetch', help='Fetch latest messages')
  fetch_parser.add_argument('-n', '--limit', type=int, default=10,
                            help='Number of messages to fetch (default: 10)')
  fetch_parser.add_argument('-c', '--channel', default=None,
                            help='Channel ID (e.g., G016KSW5GA1, C0117N64B47)')
  fetch_parser.add_argument('--json', dest='format', action='store_const',
                            const='json', default='human',
                            help='Output as JSON')
  fetch_parser.set_defaults(func=cmd_fetch)

  # Post command
  post_parser = subparsers.add_parser('post', help='Post a message')
  post_parser.add_argument('message', nargs='*',
                           help='Message to post (reads from stdin if not provided)')
  post_parser.add_argument('-c', '--channel', default=None,
                           help='Channel ID (e.g., G016KSW5GA1, C0117N64B47)')
  post_parser.set_defaults(func=cmd_post)

  # Channels command
  channels_parser = subparsers.add_parser('channels', help='List available channels')
  channels_parser.add_argument('--json', dest='format', action='store_const',
                               const='json', default='human',
                               help='Output as JSON')
  channels_parser.set_defaults(func=cmd_channels)

  args = parser.parse_args()

  if not args.command:
    parser.print_help()
    sys.exit(1)

  # Execute command
  args.func(args)


if __name__ == '__main__':
  main()
