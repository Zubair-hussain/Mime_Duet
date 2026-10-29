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


def steps_text(workflow):
    """All the step commands and actions in a workflow, as one string."""
    chunks = []
    for job in workflow["jobs"].values():
        for step in job["steps"]:
            chunks.append(str(step.get("run", "")) + " " + str(step.get("uses", "")))
    return " ".join(chunks)


