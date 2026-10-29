"""Mini Duet: a tiny proactive assistant built on Claude Opus 5.5.
It checks your inbox on a schedule, writes you a short brief,
and asks for your approval before it sends anything."""
import json
import time

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from your environment

MODEL = "claude-opus-5-5"
CHECK_EVERY_SECONDS = 3 * 60 * 60  # every 3 hours, like Duet's periodic checks

SYSTEM = (
    "You are Mini Duet, a proactive assistant. Read the user's inbox, "
    "write a short brief of what needs attention, and draft replies where useful. "
    "Use send_message only for replies that are clearly helpful."
)

# Pretend data source. Swap this for a real email or calendar API later.
INBOX = [
    {"from": "Sara (client)", "subject": "Invoice #42?", "body": "Hi! Did you send invoice #42?"},
    {"from": "Calendar", "subject": "Dentist at 4:30 PM today", "body": ""},
]

tools = [
    {
        "name": "read_inbox",
        "description": "Return the user's unread messages as JSON.",
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        "strict": True,
    },
    {
        "name": "send_message",
        "description": "Send a message on the user's behalf. The user must approve it first.",
        "input_schema": {
            "type": "object",
            "properties": {"to": {"type": "string"}, "text": {"type": "string"}},
            "required": ["to", "text"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def ask_approval(to, text):
    """Human in the loop: nothing is sent until you type y."""
    print(f"\nMini Duet wants to send to {to}:\n  {text}")
    return input("Approve? (y/n) ").strip().lower() == "y"


