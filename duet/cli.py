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


