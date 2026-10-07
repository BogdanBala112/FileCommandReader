"""
storage.py — save and load results as JSON.

LEARN: json module, pathlib, file handling, dictionaries.
"""
import json
from pathlib import Path

from .models import ApiResult


def save_results(results: list[ApiResult], output_path: str | Path) -> Path:
    """
    Serialize results to JSON and write to disk.

    Returns the path that was written.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # list comprehension: convert each dataclass to a plain dict
    payload = [r.to_dict() for r in results]

    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return out


def load_results(input_path: str | Path) -> list[dict]:
    """
    Read a previously saved JSON file back into a list of dicts.

    LEARN: json.load, exception handling for bad files.
    """
    p = Path(input_path)

    if not p.exists():
        raise FileNotFoundError(f"Results file not found: {p}")

    with open(p, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {p}: {exc}") from exc

    return data


def print_results(results: list[ApiResult]) -> None:
    """Pretty-print results to the terminal."""
    for r in results:
        a = r.analysis
        print(f"\n--- {r.document_path} ---")
        print(f"  Words    : {a.get('word_count')}")
        print(f"  Lines    : {a.get('line_count')}")
        print(f"  Chars    : {a.get('char_count')}")
        headings = a.get("headings", [])
        if headings:
            print(f"  Headings : {', '.join(headings)}")
        print(f"  Preview  :\n{a.get('preview', '')}")


def print_result(result: dict) -> None:
    """Pretty-print a single result dict loaded from results.json."""
    a = result.get("analysis", {})
    print(f"\n--- {result['document_path']} ---")
    print(f"  Saved at : {result.get('timestamp')}")
    print(f"  Words    : {a.get('word_count')}")
    print(f"  Lines    : {a.get('line_count')}")
    print(f"  Chars    : {a.get('char_count')}")
    headings = a.get("headings", [])
    if headings:
        print(f"  Headings : {', '.join(headings)}")
    print(f"\n  Content  :\n")
    print(a.get("preview", ""))
