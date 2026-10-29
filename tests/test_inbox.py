"""Tests for duet.inbox."""

import json
from pathlib import Path

import pytest

from duet.inbox import DEFAULT_INBOX, load_inbox, validate_inbox


