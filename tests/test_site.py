"""Checks that the static site is complete and links to nothing that does not exist."""

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "docs"
REQUIRED_SECTIONS = ["how", "steps", "features", "demo", "quality", "portfolio"]
CONFIG_KEYS = ["ownerName", "portfolioUrl", "githubUrl", "contactEmail"]
EXTERNAL = ("http://", "https://", "mailto:", "data:", "#")


class Page(HTMLParser):
    """Collects the parts of the page the tests care about."""

    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self.meta = {}
        self.ids = set()
        self.anchors = []
        self.assets = []
        self.images = []
        self.scripts = []
        self.config_refs = []
        self.h1_count = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and "name" in attrs:
            self.meta[attrs["name"]] = attrs.get("content", "")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if tag == "img":
            self.images.append(attrs)
        if tag == "script" and "src" in attrs:
            self.scripts.append(attrs["src"])
        for source in (attrs.get("src"), attrs.get("href")):
            if source and not source.startswith(EXTERNAL):
                self.assets.append(source)
        for name, value in attrs.items():
            if name.startswith("data-config-"):
                self.config_refs.append(value)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


