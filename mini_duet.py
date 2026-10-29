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


def run_tool(name, args):
    if name == "read_inbox":
        return json.dumps(INBOX)
    if name == "send_message":
        if ask_approval(args["to"], args["text"]):
            print("Sent.")  # call your real email API here
            return "Sent."
        return "The user declined. Do not send this message."
    return f"Unknown tool: {name}"


def check_in():
    messages = [{"role": "user", "content": "Time for a check-in. What needs my attention?"}]
    while True:  # the agent loop
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            tools=tools,
            messages=messages,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",  # safety net if a request is declined
        )
        if response.stop_reason != "tool_use":
            break
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                })
        messages.append({"role": "user", "content": results})

    if response.stop_reason == "refusal":
        print("Mini Duet declined this check-in.")
        return
    for block in response.content:
        if block.type == "text":
            print("\n--- Your brief ---\n" + block.text)


if __name__ == "__main__":
    while True:
        check_in()
        time.sleep(CHECK_EVERY_SECONDS)
