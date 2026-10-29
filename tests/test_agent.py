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


