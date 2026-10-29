"""Tests for duet.scheduler."""

import pytest

from duet.scheduler import run_forever


def test_runs_the_requested_number_of_times():
    calls = []
    runs = run_forever(lambda: calls.append(1), 5, sleep=lambda seconds: None, max_runs=3)
    assert runs == 3
    assert len(calls) == 3


def test_sleeps_between_runs_but_not_after_the_last_one():
    sleeps = []
    run_forever(lambda: None, 7, sleep=sleeps.append, max_runs=3)
    assert sleeps == [7, 7]


def test_zero_runs_does_nothing():
    def fail():
        raise AssertionError("should not run")

    assert run_forever(fail, 1, sleep=lambda seconds: None, max_runs=0) == 0


def test_an_endless_loop_stops_when_interrupted():
    sleeps = []

    def interrupt_on_third_sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) == 3:
            raise KeyboardInterrupt

    calls = []
    with pytest.raises(KeyboardInterrupt):
        run_forever(lambda: calls.append(1), 2, sleep=interrupt_on_third_sleep)
    assert len(calls) == 3
    assert sleeps == [2, 2, 2]
