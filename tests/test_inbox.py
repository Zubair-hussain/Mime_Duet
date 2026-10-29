"""Tests for duet.inbox."""

import json
from pathlib import Path

import pytest

from duet.inbox import DEFAULT_INBOX, load_inbox, validate_inbox


def test_no_path_returns_a_copy_of_the_demo_inbox():
    inbox = load_inbox()
    assert inbox == DEFAULT_INBOX
    assert inbox is not DEFAULT_INBOX


def test_missing_file_returns_the_demo_inbox(tmp_path):
    assert load_inbox(tmp_path / "none.json") == DEFAULT_INBOX


def test_reads_messages_from_a_file(tmp_path):
    messages = [{"from": "A", "subject": "B", "body": "C"}]
    file = tmp_path / "inbox.json"
    file.write_text(json.dumps(messages))
    assert load_inbox(file) == messages


def test_invalid_json_raises(tmp_path):
    file = tmp_path / "inbox.json"
    file.write_text("oops")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_inbox(file)


