"""Command line entry point: python -m duet"""

from __future__ import annotations

import argparse
import time
from collections.abc import Callable, Sequence

import anthropic

from . import __version__
from .agent import check_in
from .config import load_settings
from .inbox import load_inbox
from .scheduler import run_forever

AUTH_HELP = "No API key found. Set ANTHROPIC_API_KEY (see the README, Step 3)."


def build_parser() -> argparse.ArgumentParser:
    """The command line options."""
    parser = argparse.ArgumentParser(
        prog="duet", description="Mini Duet: a proactive assistant built on Claude."
    )
    parser.add_argument("--config", help="path to a settings JSON file (default: duet.config.json)")
    parser.add_argument("--inbox", help="path to an inbox JSON file (overrides the settings)")
    parser.add_argument("--once", action="store_true", help="run one check-in and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(
    argv: Sequence[str] | None = None,
    client_factory: Callable[[], object] = anthropic.Anthropic,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Run Mini Duet. Returns the exit code: 0 ok, 1 auth problem, 2 bad config."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(args.config)
        inbox = load_inbox(args.inbox or settings.inbox_path)
    except (FileNotFoundError, ValueError) as err:
        print(f"Config error: {err}")
        return 2
    client = client_factory()

    def check() -> None:
        check_in(client, settings, inbox)

    try:
        if args.once:
            check()
        else:
            run_forever(check, settings.check_every_seconds, sleep=sleep)
    except anthropic.AuthenticationError:
        print("Authentication failed. Check your API key (see the README, Step 1).")
        return 1
    except TypeError as err:  # the SDK raises this when no key is set at all
        if "authentication" not in str(err).lower():
            raise
        print(AUTH_HELP)
        return 1
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0
