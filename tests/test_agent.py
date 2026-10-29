"""Tests for duet.agent: the agent loop."""

from duet.agent import (
    CHECK_IN_PROMPT,
    FALLBACK_BETA,
    build_request,
    check_in,
    extract_text,
    run_tool_calls,
)
from duet.config import Settings
from duet.tools import DECLINED, TOOLS
from helpers import FakeClient, always, response, text_block, tool_use_block


def test_build_request_uses_the_settings(settings):
    request = build_request(settings, [])
    assert request["model"] == "claude-opus-5-5"
    assert request["max_tokens"] == 16000
    assert request["system"] == settings.system
    assert request["tools"] is TOOLS
    assert request["output_config"] == {"effort": "medium"}
    assert request["betas"] == [FALLBACK_BETA]
    assert request["fallbacks"] == "default"


def test_build_request_respects_custom_settings():
    custom = Settings(model="other-model", effort="high", max_tokens=5, system="Be brief.")
    request = build_request(custom, [{"role": "user", "content": "hi"}])
    assert request["model"] == "other-model"
    assert request["output_config"] == {"effort": "high"}
    assert request["max_tokens"] == 5
    assert request["system"] == "Be brief."
    assert request["messages"] == [{"role": "user", "content": "hi"}]


def test_extract_text_joins_text_blocks_only():
    reply = response(
        "end_turn", text_block("a"), tool_use_block("t", "read_inbox"), text_block("b")
    )
    assert extract_text(reply) == "a\nb"


def test_tool_results_match_their_tool_use_ids(inbox):
    reply = response(
        "tool_use",
        tool_use_block("t1", "read_inbox"),
        text_block("thinking out loud"),
        tool_use_block("t2", "nope"),
    )
    results = run_tool_calls(reply, inbox, always(True), out=lambda text: None)
    assert [result["tool_use_id"] for result in results] == ["t1", "t2"]
    assert all(result["type"] == "tool_result" for result in results)
    assert results[1]["content"] == "Unknown tool: nope"


def test_a_check_in_without_tools_returns_the_brief(settings, inbox):
    client = FakeClient(response("end_turn", text_block("All quiet.")))
    printed = []
    brief = check_in(client, settings, inbox, always(True), printed.append)
    assert brief == "All quiet."
    assert len(client.calls) == 1
    assert client.calls[0]["messages"][0] == {"role": "user", "content": CHECK_IN_PROMPT}
    assert "All quiet." in printed[-1]


def test_a_check_in_runs_the_whole_tool_loop(settings, inbox):
    client = FakeClient(
        response("tool_use", tool_use_block("t1", "read_inbox")),
        response("tool_use", tool_use_block("t2", "send_message", {"to": "Sara", "text": "Hi"})),
        response("end_turn", text_block("Done.")),
    )
    brief = check_in(client, settings, inbox, always(True), lambda text: None)
    assert brief == "Done."
    assert len(client.calls) == 3
    final_messages = client.calls[2]["messages"]
    assert [message["role"] for message in final_messages] == [
        "user",
        "assistant",
        "user",
        "assistant",
        "user",
    ]
    assert final_messages[-1]["content"][0]["tool_use_id"] == "t2"
    assert final_messages[-1]["content"][0]["content"] == "Sent."


def test_a_declined_message_is_reported_back_to_the_model(settings, inbox):
    client = FakeClient(
        response("tool_use", tool_use_block("t1", "send_message", {"to": "Sara", "text": "Hi"})),
        response("end_turn", text_block("Okay, not sent.")),
    )
    check_in(client, settings, inbox, always(False), lambda text: None)
    assert client.calls[1]["messages"][-1]["content"][0]["content"] == DECLINED


def test_a_refusal_returns_none_and_says_so(settings, inbox):
    client = FakeClient(response("refusal"))
    printed = []
    assert check_in(client, settings, inbox, always(True), printed.append) is None
    assert printed == ["Mini Duet declined this check-in."]


def test_every_request_carries_the_tools_and_the_fallback(settings, inbox):
    client = FakeClient(
        response("tool_use", tool_use_block("t1", "read_inbox")),
        response("end_turn", text_block("Done.")),
    )
    check_in(client, settings, inbox, always(True), lambda text: None)
    for call in client.calls:
        assert call["tools"] == TOOLS
        assert call["fallbacks"] == "default"


def test_the_default_approval_is_the_interactive_one(settings, inbox, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    client = FakeClient(
        response("tool_use", tool_use_block("t1", "send_message", {"to": "Sara", "text": "Hi"})),
        response("end_turn", text_block("Done.")),
    )
    check_in(client, settings, inbox)
    assert client.calls[1]["messages"][-1]["content"][0]["content"] == DECLINED
    assert "Mini Duet wants to send to Sara" in capsys.readouterr().out
