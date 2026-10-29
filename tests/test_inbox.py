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


def test_rejects_a_non_list():
    with pytest.raises(ValueError, match="JSON list"):
        validate_inbox({"a": 1})


def test_rejects_messages_that_are_not_objects():
    with pytest.raises(ValueError, match="must be an object"):
        validate_inbox(["hello"])


def test_rejects_messages_with_missing_keys():
    with pytest.raises(ValueError, match="missing: subject, body"):
        validate_inbox([{"from": "A"}])


def test_valid_inbox_is_returned_unchanged():
    items = [{"from": "A", "subject": "B", "body": "C"}]
    assert validate_inbox(items) is items


def test_the_bundled_inbox_file_is_valid():
    bundled = Path(__file__).resolve().parent.parent / "data" / "inbox.json"
    assert load_inbox(bundled) == DEFAULT_INBOX
