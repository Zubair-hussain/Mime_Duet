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


@pytest.fixture(scope="module")
def page():
    parsed = Page()
    parsed.feed((DOCS / "index.html").read_text(encoding="utf-8"))
    return parsed


@pytest.fixture(scope="module")
def config_js():
    return (DOCS / "config.js").read_text(encoding="utf-8")


def test_the_page_has_a_language_title_and_description(page):
    assert page.lang == "en"
    assert 10 < len(page.title.strip()) <= 70
    assert 50 <= len(page.meta["description"]) <= 300


def test_the_page_is_mobile_friendly(page):
    assert "width=device-width" in page.meta["viewport"]


def test_there_is_exactly_one_h1(page):
    assert page.h1_count == 1


@pytest.mark.parametrize("section", REQUIRED_SECTIONS)
def test_every_required_section_exists(page, section):
    assert section in page.ids


def test_in_page_links_point_at_real_ids(page):
    missing = [anchor for anchor in page.anchors if anchor and anchor not in page.ids]
    assert missing == []


