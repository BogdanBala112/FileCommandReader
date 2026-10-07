"""
file_handler.py — read documentation files from disk.

LEARN: file handling, exceptions, lists, comprehensions, pathlib.
"""
from pathlib import Path

from .models import Document


class FileReadError(Exception):
    """Raised when a file cannot be read."""


SUPPORTED_EXTENSIONS: list[str] = [".txt", ".md", ".rst", ".py"]


def read_file(path: str | Path) -> Document:
    """
    Read a single file and return a Document.

    Raises FileReadError if the file is missing or unreadable.
    """
    p = Path(path)

    if not p.exists():
        raise FileReadError(f"File not found: {p}")

    if p.suffix not in SUPPORTED_EXTENSIONS:
        raise FileReadError(
            f"Unsupported file type '{p.suffix}'. "
            f"Allowed: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    try:
        content = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise FileReadError(f"Could not read {p}: {exc}") from exc

    return Document(path=str(p), content=content)


def read_files(paths: list[str | Path]) -> list[Document]:
    """
    Read multiple files. Skips unreadable ones and prints a warning.

    LEARN: list comprehension with error handling inside a loop.
    """
    documents: list[Document] = []

    for path in paths:
        try:
            doc = read_file(path)
            documents.append(doc)
        except FileReadError as exc:
            print(f"[warning] Skipping {path}: {exc}")

    return documents


def collect_files(directory: str | Path, recursive: bool = False) -> list[Path]:
    """
    Find all supported files in a directory.

    LEARN: pathlib glob, list comprehension with filter.
    """
    d = Path(directory)
    if not d.is_dir():
        raise FileReadError(f"Not a directory: {d}")

    pattern = "**/*" if recursive else "*"
    # comprehension: filter by extension
    return [
        p for p in d.glob(pattern)
        if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
    ]
