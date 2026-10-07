# FileCommandReader

FileCommandReader is a command-line tool that reads documentation files,
sends their content to a language model API for summarization, and saves
the results as structured JSON.

## Features

- Reads .md, .txt, .rst, and .py files
- Concurrent API calls via asyncio
- JSON output with timestamps
- Credentials stored in environment variables

## Usage

    python main.py docs/intro.md
    python main.py docs/ --dir --recursive --output results/summary.json
