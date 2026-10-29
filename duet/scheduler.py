"""Run a check-in on a schedule, like Duet's every-few-hours checks."""

from __future__ import annotations

import time
from collections.abc import Callable


def run_forever(
    check: Callable[[], object],
    every_seconds: float,
    sleep: Callable[[float], None] = time.sleep,
    max_runs: int | None = None,
) -> int:
    """Call check(), wait, and repeat. max_runs=None means keep going until stopped.

    Returns how many times check() ran.
    """
    runs = 0
    while max_runs is None or runs < max_runs:
        check()
        runs += 1
        if max_runs is not None and runs >= max_runs:
            break
        sleep(every_seconds)
    return runs
