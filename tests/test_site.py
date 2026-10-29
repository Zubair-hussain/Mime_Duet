"""Checks that the static site is complete and links to nothing that does not exist."""

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "docs"
REQUIRED_SECTIONS = ["how", "steps", "features", "demo", "quality", "portfolio"]
CONFIG_KEYS = ["ownerName", "portfolioUrl", "githubUrl", "contactEmail"]
EXTERNAL = ("http://", "https://", "mailto:", "data:", "#")


