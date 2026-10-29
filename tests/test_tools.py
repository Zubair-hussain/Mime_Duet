"""Tests for duet.tools."""

import json

from duet.tools import DECLINED, TOOLS, run_tool
from helpers import always


def test_the_two_tools_are_defined():
    assert [tool["name"] for tool in TOOLS] == ["read_inbox", "send_message"]


