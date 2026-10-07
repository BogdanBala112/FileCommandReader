"""
picker.py — interactive file selection in the terminal.

LEARN: while loops, enumerate, input(), list indexing, error handling.
"""
from pathlib import Path

from .file_handler import SUPPORTED_EXTENSIONS, FileReadError


def pick_files(start_dir: str | Path = ".") -> list[Path]:
    """
    Show the user a numbered list of supported files and let them pick one or more.

    Returns the selected paths.
    """
    start = Path(start_dir).resolve()
    if not start.is_dir():
        raise FileReadError(f"Not a directory: {start}")

    # Collect all supported files recursively
    all_files: list[Path] = sorted(
        p for p in start.rglob("*")
        if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
    )

    if not all_files:
        raise FileReadError(f"No supported files found under {start}")

    # Print numbered list
    print(f"\nFiles found under {start}:\n")
    for i, path in enumerate(all_files, start=1):
        # Show path relative to start_dir for readability
        print(f"  [{i}] {path.relative_to(start)}")

    print()
    print("Enter number(s) to select files, separated by spaces (e.g. 1 3).")
    print("Press Enter with no input to select all.\n")

    # Keep asking until the user gives a valid answer
    while True:
        raw = input("Your choice: ").strip()

        # Empty input = select all
        if not raw:
            return all_files

        try:
            # Parse space-separated numbers
            chosen_indices = [int(x) for x in raw.split()]
        except ValueError:
            print("Please enter numbers only, e.g. 1 3")
            continue

        # Validate range
        invalid = [i for i in chosen_indices if i < 1 or i > len(all_files)]
        if invalid:
            print(f"Invalid selection(s): {invalid}. Choose between 1 and {len(all_files)}.")
            continue

        # Return the selected paths (convert 1-based index to 0-based)
        return [all_files[i - 1] for i in chosen_indices]


def pick_result(results: list[dict]) -> dict:
    """
    Show a numbered list of saved results and let the user pick one to view.

    Returns the selected result dict.
    """
    if not results:
        raise ValueError("No results to display.")

    print("\nSaved results:\n")
    for i, r in enumerate(results, start=1):
        print(f"  [{i}] {r['document_path']}  ({r['timestamp']})")

    print()

    while True:
        raw = input("Pick a result to view: ").strip()

        try:
            index = int(raw)
        except ValueError:
            print("Please enter a single number.")
            continue

        if index < 1 or index > len(results):
            print(f"Choose between 1 and {len(results)}.")
            continue

        return results[index - 1]
