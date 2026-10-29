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


