# FileCommandReader

A small CLI tool that reads documentation files, calls an HTTP API to summarize them,
and saves the result as JSON. Every file is annotated with the Python concept it teaches.

---

## Project layout

```
FileCommandReader/
  main.py                   # CLI entry point (argparse)
  pyproject.toml            # project metadata + dependencies (uv)
  uv.lock                   # auto-generated lockfile — commit this
  .env.example              # credential template
  docs/                     # sample input files
  src/reader/
    models.py               # LEARN: classes, dataclasses, type hints
    file_handler.py         # LEARN: file I/O, exceptions, lists, comprehensions
    api_client.py           # LEARN: HTTP requests, async/await, env vars, dicts
    storage.py              # LEARN: JSON, pathlib, file handling
  tests/
    test_file_handler.py    # LEARN: pytest, fixtures, asserting exceptions
    test_storage.py         # LEARN: JSON round-trip tests
```

---

## Setup (do this once)

```bash
# 0. Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 1. Create a virtual environment and install all dependencies in one step
uv sync

# 2. Set up credentials
cp .env.example .env
# Open .env and paste your OpenAI API key
```

`uv sync` reads `pyproject.toml`, creates `.venv/` automatically, and writes
`uv.lock` — a fully pinned lockfile you should commit so every machine gets
identical versions.

To add a new package:
```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev-only (e.g. a linter)
```

---

## Run

```bash
# Summarize one file
uv run python main.py docs/intro.md

# Summarize a whole directory
uv run python main.py docs/ --dir

# Choose output path and model
uv run python main.py docs/intro.md --output output/intro_summary.json --model gpt-4o-mini
```

`uv run` activates the project's virtual environment automatically — no need
to `source .venv/bin/activate` first.

---

## Test

```bash
uv run pytest -v
```

No API key needed for tests — they never hit the network.

---

## Python concepts covered (with file locations)

| Concept | Where |
|---|---|
| Functions | Every module |
| Lists & comprehensions | `file_handler.py` — `collect_files`, `read_files` |
| Dictionaries | `api_client.py` — `_build_headers`, `_build_payload` |
| Type hints | All files — `def foo(x: str) -> list[Document]` |
| Modules & imports | `main.py` imports from `src.reader.*` |
| Classes & dataclasses | `models.py` — `Document`, `SummaryResult` |
| Custom exceptions | `file_handler.py` — `FileReadError`; `api_client.py` — `ApiError` |
| File handling | `file_handler.py`, `storage.py` |
| JSON | `storage.py` — `json.dump` / `json.load` |
| HTTP requests | `api_client.py` — `httpx.AsyncClient` |
| Environment variables | `api_client.py` — `os.environ.get(...)` |
| Virtual environments + uv | This README — setup section |
| Async / concurrent calls | `api_client.py` — `asyncio.gather` |
| Basic tests | `tests/` — pytest |

---

## Reading a traceback (quick guide)

When Python crashes you see something like:

```
Traceback (most recent call last):
  File "main.py", line 42, in main
    results = run_summarize(documents, model=args.model)
  File "src/reader/api_client.py", line 68, in run_summarize
    return asyncio.run(summarize_all(documents, model))
  ...
ApiError: OPENAI_API_KEY is not set.
```

Read it **bottom-up**:
1. The last line is the error type and message — start here.
2. The line above it is where the error was raised.
3. Work upward to find where in *your* code the call chain started.


**Further Improvements Incoming**
