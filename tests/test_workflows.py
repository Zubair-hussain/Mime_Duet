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


def test_deploy_publishes_the_docs_folder():
    steps = load("deploy.yml")["jobs"]["deploy"]["steps"]
    upload = next(step for step in steps if "upload-pages-artifact" in step.get("uses", ""))
    assert upload["with"]["path"] == "docs"


def test_deploy_can_be_started_by_hand():
    assert "workflow_dispatch" in load("deploy.yml")["on"]


def test_ci_tests_on_several_python_versions():
    matrix = load("ci.yml")["jobs"]["test"]["strategy"]["matrix"]["python-version"]
    assert len(matrix) >= 3


def test_ci_runs_the_tests_with_coverage():
    text = steps_text(load("ci.yml"))
    assert "pytest" in text
    assert "--cov" in text


def test_ci_lints_with_ruff():
    assert "ruff check" in steps_text(load("ci.yml"))


def test_workflows_run_on_the_production_branch():
    for name in ("ci.yml", "deploy.yml"):
        assert load(name)["on"]["push"]["branches"] == ["live/production"]


def test_dependabot_skips_pillow_13():
    config = yaml.safe_load((WORKFLOWS.parent / "dependabot.yml").read_text(encoding="utf-8"))
    pip = next(u for u in config["updates"] if u["package-ecosystem"] == "pip")
    assert {"dependency-name": "pillow", "versions": [">=13"]} in pip["ignore"]
