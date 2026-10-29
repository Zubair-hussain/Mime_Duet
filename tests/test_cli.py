"""Tests for duet.cli."""

import json
import runpy
import sys

import anthropic
import pytest

from duet import __version__
from duet.cli import AUTH_HELP, main
from helpers import FakeClient, response, text_block, tool_use_block


def quiet_client():
    return FakeClient(response("end_turn", text_block("All quiet.")))


