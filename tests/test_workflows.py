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


@pytest.mark.parametrize("name", ["ci.yml", "deploy.yml"])
def test_workflows_are_valid_yaml_with_jobs(name):
    workflow = load(name)
    assert workflow["name"]
    assert workflow["on"]
    assert workflow["jobs"]


def test_deploy_uses_the_official_pages_actions():
    text = steps_text(load("deploy.yml"))
    for action in ("configure-pages", "upload-pages-artifact", "deploy-pages"):
        assert f"actions/{action}" in text


def test_deploy_has_the_permissions_pages_needs():
    permissions = load("deploy.yml")["permissions"]
    assert permissions["pages"] == "write"
    assert permissions["id-token"] == "write"


