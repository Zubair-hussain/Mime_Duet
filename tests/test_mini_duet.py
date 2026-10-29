"""Tests for mini_duet.py, the single-file version shown in the video."""

import json
from types import SimpleNamespace

import pytest

import mini_duet
from helpers import FakeClient, response, text_block, tool_use_block


