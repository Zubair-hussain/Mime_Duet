"""Tests for duet.tools."""

import json

from duet.tools import DECLINED, TOOLS, run_tool
from helpers import always


def test_the_two_tools_are_defined():
    assert [tool["name"] for tool in TOOLS] == ["read_inbox", "send_message"]


def test_every_tool_is_strict_with_a_closed_schema():
    for tool in TOOLS:
        assert tool["strict"] is True
        assert tool["input_schema"]["type"] == "object"
        assert tool["input_schema"]["additionalProperties"] is False


