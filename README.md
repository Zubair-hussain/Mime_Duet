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

## What you need

- A computer or laptop (Windows, macOS or Linux)
- [Python 3.10 or newer](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/) with the **Python** extension
- An Anthropic Console account and an API key

## Step 1: Get your API key (you do this yourself)

1. Go to **[console.anthropic.com](https://console.anthropic.com)** and sign in.
2. Open **Billing** and add a small amount of credit.
3. Open **API keys** and click **Create key**. Give it a name.
4. **Copy the key now.** You will not be able to see it again. Keep it somewhere safe.

Never share your key, and never paste it into your code.

## Step 2: Get the code and set up the project

Download the project and open it in VS Code:

```bash
git clone https://github.com/Zubair-hussain/Mime_Duet.git
cd Mime_Duet
code .
```

Then open the terminal (**Ctrl + `**).

Create a virtual environment and turn it on:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install the packages:

```bash
pip install -r requirements.txt
```

## Step 3: Set your API key

Store the key in an **environment variable**, so it never ends up in your code or on GitHub.

Windows (PowerShell):

```powershell
$env:ANTHROPIC_API_KEY = "your-key-here"
```

macOS / Linux:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

This lasts for the current terminal only. Set it again if you open a new one.

## Step 4: Run it

```bash
python -m duet --once
```

Mini Duet reads the inbox, drafts a reply, and asks:

```
Mini Duet wants to send to Sara (client):
  Hi Sara! Yes, invoice #42 went out this morning.
Approve? (y/n)
```

Type `y` to send it or `n` to decline. Then it prints your brief.

Leave off `--once` and it checks in again every 3 hours. Press **Ctrl + C** to stop it.

The single-file version from the video still works exactly as shown:

```bash
python mini_duet.py
```

## Command line options

| Option | What it does |
|---|---|
| `--once` | Run one check-in and exit |
| `--config PATH` | Use a different settings file (default: `duet.config.json`) |
| `--inbox PATH` | Use a different inbox file (overrides the settings) |
| `--version` | Print the version |

Exit codes: `0` ok, `1` API key problem, `2` bad config or inbox file.

## Custom files

You can change how Mini Duet behaves without editing any Python.

| File | What it controls |
|---|---|
| `duet.config.json` | Model, effort, `max_tokens`, how often it checks in, the inbox path, the system prompt |
| `data/inbox.json` | The messages Mini Duet reads. Each message needs `from`, `subject` and `body` |

Example `duet.config.json`:

```json
{
  "model": "claude-opus-5-5",
  "effort": "medium",
  "max_tokens": 16000,
  "check_every_seconds": 10800,
  "inbox_path": "data/inbox.json"
}
```

`effort` can be `low`, `medium`, `high`, `xhigh` or `max`. Mistakes in these files give a clear error and exit code `2`.

## Project structure

```
Mime_Duet/
├── mini_duet.py          the single-file version from the video
├── duet/                 the same logic as a tidy, tested package
│   ├── config.py         settings and the JSON config loader
│   ├── inbox.py          loads and checks the inbox
│   ├── approval.py       the human-in-the-loop prompt
│   ├── tools.py          the tools Claude may ask for
│   ├── agent.py          the agent loop
│   ├── scheduler.py      the every-few-hours schedule
│   └── cli.py            the command line
├── duet.config.json      custom settings
├── data/inbox.json       custom inbox
├── tests/                pytest suite (fake API client, no key needed)
├── docs/                 the static website (deployed to GitHub Pages)
├── scripts/              helper scripts (demo GIF)
└── .github/              CI, deploy workflow, issue and PR templates
```

## How it works

| Part | What it does |
|---|---|
| `SYSTEM` | Claude's job description: who it is and how to behave |
| `INBOX` | A pretend inbox for the demo. Swap it for a real email API later |
| `tools` | Actions Claude may **ask** for: `read_inbox` and `send_message` |
| `ask_approval()` | Human in the loop: nothing is sent until you type `y` |
| `run_tool()` | Runs the tool Claude asked for and returns the result |
| `check_in()` | The **agent loop**: ask Claude, run its tool calls, send back the results, repeat until it is done |

The model is `claude-opus-5-5` with `effort: "medium"`. `fallbacks="default"` is a safety net: if a request is ever declined, the API can retry it on a backup model.

## Tests and coverage

The tests use a fake API client, so they need no API key, cost nothing and never touch the network.

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest
```

Run them with a coverage report:

```bash
python -m pytest --cov
```

Check the code style:

```bash
ruff check .
```

Coverage is checked on every push, and the build fails if it drops below 95%. The tests also check that the website is complete, that every link and image on it exists, and that the workflow files are valid.

## Deploy the website

The page in `docs/` is plain HTML, CSS and JavaScript, so GitHub Pages can host it for free.

1. Push this folder to your GitHub repository (this project lives at `Zubair-hussain/Mime_Duet`).
2. In the repository, open **Settings > Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to `live/production`, or open **Actions > Deploy site > Run workflow**. The workflow in `.github/workflows/deploy.yml` publishes `docs/`.
5. After about a minute your site is live at `https://zubair-hussain.github.io/Mime_Duet/`.
6. Optional: add your own domain under **Settings > Pages > Custom domain**.

The production branch is `live/production`. GitHub only lets Pages deploy from branches its `github-pages` environment allows, so either make `live/production` the default branch (**Settings > Branches**) or add it under **Settings > Environments > github-pages > Deployment branches and tags**. Every deployment also appears under **Deployments** on the repository's home page.

## Make the site yours

Everything personal lives in one file, so you never have to touch the HTML.

1. Open [`docs/config.js`](docs/config.js).
2. Check `ownerName` and `portfolioUrl`. Set `contactEmail` if you want the "Get in touch" button. `githubUrl` already points at this repository.
3. Save, commit and push to `live/production`. The site redeploys on its own.

A link that is still a placeholder (it contains `YOUR-` or `example.com`) stays hidden on the page until you set it, so visitors never see a broken button.

To change the logo, replace `docs/assets/zh-mark.svg` (the header and footer) and `docs/assets/favicon.svg` (the tab icon and the About section).

## Versions and tags

Releases are tagged on the `live/production` branch. See the [Tags page](https://github.com/Zubair-hussain/Mime_Duet/tags) and the [CHANGELOG](CHANGELOG.md).

| Tag | What it adds |
|---|---|
| `v0.1.0` | The single-file assistant from the video |
| `v0.2.0` | The modular `duet` package, custom config and inbox files |
| `v0.3.0` | The pytest suite and the coverage gate |
| `v0.4.0` | The one-page portfolio website |
| `v0.5.0` | CI and GitHub Pages deployment |
| `v1.0.0` | Docs, templates and the first public release |

Check out any version with `git checkout v0.2.0`.

## Common errors

| Error | Fix |
|---|---|
| `No API key found` or `AuthenticationError` | Your API key is not set in this terminal. Repeat Step 3. |
| `ModuleNotFoundError: anthropic` | Your virtual environment is not on. Activate `.venv` and run `pip install -r requirements.txt`. |
| `RateLimitError` | Too many requests. Wait a moment and try again. |
| `Config error: ...` | Check `duet.config.json` and `data/inbox.json`. The message says what is wrong. |

