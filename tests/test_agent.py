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


