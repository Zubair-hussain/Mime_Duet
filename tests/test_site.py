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


def test_every_local_file_the_page_uses_exists(page):
    missing = [asset for asset in page.assets if not (DOCS / asset).is_file()]
    assert missing == []


def test_every_image_has_alt_text_and_a_size(page):
    assert page.images
    for image in page.images:
        assert image.get("alt"), image
        assert image.get("width") and image.get("height"), image


def test_no_third_party_scripts_are_loaded(page):
    assert page.scripts
    assert all(not source.startswith(("http://", "https://")) for source in page.scripts)


def test_config_defines_every_key_the_page_needs(config_js):
    for key in CONFIG_KEYS:
        assert re.search(rf"\b{key}\s*:", config_js), key


def test_every_config_reference_in_the_html_exists_in_config(page, config_js):
    for reference in page.config_refs:
        assert re.search(rf"\b{reference}\s*:", config_js), reference


def test_the_portfolio_link_is_set(config_js):
    match = re.search(r'portfolioUrl:\s*"([^"]+)"', config_js)
    assert match
    assert match.group(1).startswith("https://")
    assert "YOUR-" not in match.group(1)


def test_the_github_link_points_at_the_repo(config_js):
    match = re.search(r'githubUrl:\s*"([^"]+)"', config_js)
    assert match
    assert match.group(1).startswith("https://github.com/")
    assert "YOUR-" not in match.group(1)


def test_the_demo_is_a_real_gif():
    assert (DOCS / "assets" / "demo.gif").read_bytes()[:4] == b"GIF8"


@pytest.mark.parametrize("name", ["zh-mark.svg", "favicon.svg"])
def test_the_logo_files_are_svg(name):
    assert (DOCS / "assets" / name).read_text(encoding="utf-8").lstrip().startswith("<svg")


@pytest.mark.parametrize("name", ["style.css", "script.js"])
def test_braces_are_balanced(name):
    text = (DOCS / name).read_text(encoding="utf-8")
    assert text.count("{") == text.count("}")
