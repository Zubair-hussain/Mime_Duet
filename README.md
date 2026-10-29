# Mini Duet

[![CI](https://github.com/Zubair-hussain/Mime_Duet/actions/workflows/ci.yml/badge.svg)](https://github.com/Zubair-hussain/Mime_Duet/actions/workflows/ci.yml)
[![Deploy site](https://github.com/Zubair-hussain/Mime_Duet/actions/workflows/deploy.yml/badge.svg)](https://github.com/Zubair-hussain/Mime_Duet/actions/workflows/deploy.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-c8141e)
![Model](https://img.shields.io/badge/model-claude--opus--5--5-0a0a0a)

**Build your own small, proactive AI assistant with Claude Opus 5.5, running on your own computer.**

Mini Duet checks an inbox on a schedule, writes you a short brief of what needs your attention, drafts replies, and **asks for your approval before it sends anything**.

> **Note:** This is **not** Anthropic's official Claude Duet app. Claude Duet is Anthropic's own product and it has no public API. Mini Duet is a small do-it-yourself version that talks to Claude through the [Anthropic API](https://docs.claude.com).

## Demo

![Mini Duet demo: it drafts a reply, asks for approval, and prints a brief](docs/assets/demo.gif)

*A sample run with the demo inbox. This GIF is an illustration, drawn by `scripts/make_demo_gif.py`.*

## Live site

A one-page site for this project lives in [`docs/`](docs/) and deploys to GitHub Pages. See [Deploy the website](#deploy-the-website) for the steps. Once Pages is on, it is live at **https://zubair-hussain.github.io/Mime_Duet/**.

## The fastest way: let an AI build it for you

You do not have to write any code. Give this README to **Claude** or **Codex** and say:

> "Build this project for me on my computer, following the README step by step."

It will create the files, set up the virtual environment and install the packages.

**The one step you must do yourself is getting your API key** (Step 1). No AI can do that for you.

