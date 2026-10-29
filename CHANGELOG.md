# Changelog

All notable changes to this project are listed here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each version is a tag on the `live/production` branch.

## [Unreleased]

### Added

- Nothing yet.

## [1.0.0] - 2026-10-29

First public release.

### Added

- A README with a demo GIF, setup steps, deploy steps and a versions table.
- `CONTRIBUTING.md`, `SECURITY.md`, issue templates, a pull request template and Dependabot updates.

## [0.5.0] - 2026-10-29

### Added

- A CI workflow: lint, then tests with coverage on Python 3.10 to 3.13.
- A deploy workflow that publishes the `docs/` folder to GitHub Pages from `live/production`.
- Tests that check both workflow files.

## [0.4.0] - 2026-10-29

### Added

- A one-page portfolio-style website in `docs/` with a red gradient accent and the ZH. logo.
- `docs/config.js`, one file for the name and the links. Links that are not set yet stay hidden.
- A demo GIF drawn by `scripts/make_demo_gif.py`.
- Tests that check the page: sections, links, images, and the local files it uses.

## [0.3.0] - 2026-10-29

### Added

- A pytest suite with a fake API client, so tests need no key and no network.
- A coverage gate at 95%, and `ruff` linting.

