"""Tests for duet.inbox."""

import json
from pathlib import Path

import pytest

from duet.inbox import DEFAULT_INBOX, load_inbox, validate_inbox


def test_no_path_returns_a_copy_of_the_demo_inbox():
    inbox = load_inbox()
    assert inbox == DEFAULT_INBOX
    assert inbox is not DEFAULT_INBOX


