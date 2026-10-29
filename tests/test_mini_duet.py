"""Tests for mini_duet.py, the single-file version shown in the video."""

import json
from types import SimpleNamespace

import pytest

import mini_duet
from helpers import FakeClient, response, text_block, tool_use_block


def test_settings_match_the_video():
    assert mini_duet.MODEL == "claude-opus-5-5"
    assert mini_duet.CHECK_EVERY_SECONDS == 3 * 60 * 60


def test_two_tools_are_defined():
    assert [tool["name"] for tool in mini_duet.tools] == ["read_inbox", "send_message"]


