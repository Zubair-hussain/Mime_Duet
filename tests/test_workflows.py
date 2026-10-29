"""Checks the GitHub Actions workflows: valid YAML, and the settings the project relies on."""

from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"


