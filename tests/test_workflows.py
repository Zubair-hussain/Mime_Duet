"""Checks the GitHub Actions workflows: valid YAML, and the settings the project relies on."""

from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"


def load(name):
    """Parse a workflow file. PyYAML reads the key `on` as True, so put it back."""
    workflow = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    workflow["on"] = workflow.pop(True, workflow.get("on"))
    return workflow


