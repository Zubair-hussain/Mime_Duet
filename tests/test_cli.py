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


def write_json(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


class RaisingClient:
    """A client whose requests fail with whatever error we give it."""

    def __init__(self, error):
        self.beta = type(
            "Beta", (), {"messages": type("Messages", (), {"create": self._create})()}
        )()
        self._error = error

    def _create(self, **kwargs):
        raise self._error


class FakeAuthError(anthropic.AuthenticationError):
    """An authentication error we can build without a real HTTP response."""

    def __init__(self):
        Exception.__init__(self, "invalid x-api-key")


