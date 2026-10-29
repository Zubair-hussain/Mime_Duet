# Contributing to Mini Duet

Thanks for helping out. This is a small project, so the process is small too.

## Set up

```bash
python -m venv .venv
```

Turn the environment on (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` on macOS and Linux), then:

```bash
pip install -r requirements-dev.txt
```

You do **not** need an API key to run the tests.

## Run the checks

```bash
ruff check .
```

```bash
python -m pytest --cov
```

Both must pass before you open a pull request. Coverage must stay at or above 95%.

## Project layout

- `duet/` is the tested package. Put new logic here.
- `mini_duet.py` is the single-file version shown in the video. Keep it matching the video.
- `tests/` mirrors the package: `duet/agent.py` is tested in `tests/test_agent.py`.
- `docs/` is the static website. `docs/config.js` holds the personal details.

