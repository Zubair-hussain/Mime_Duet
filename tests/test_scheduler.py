"""Tests for duet.scheduler."""

import pytest

from duet.scheduler import run_forever


def test_runs_the_requested_number_of_times():
    calls = []
    runs = run_forever(lambda: calls.append(1), 5, sleep=lambda seconds: None, max_runs=3)
    assert runs == 3
    assert len(calls) == 3


