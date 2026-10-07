"""
main.py — CLI entry point.

LEARN: argparse for CLI parsing, bringing modules together.

Usage examples:
    python main.py docs/intro.md
    python main.py docs/ --dir --recursive
    python main.py docs/intro.md --output results/out.json
    python main.py --interactive
    python main.py --interactive /Users/bogdan/Documents
"""
import argparse
import sys
from pathlib import Path

from src.reader.api_client import SERVER_URL, ApiError, run_post
from src.reader.file_handler import FileReadError, collect_files, read_files
from src.reader.picker import pick_files, pick_result
from src.reader.storage import load_results, print_result, print_results, save_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reader",
        description="Read documentation files, POST to local server, save JSON.",
    )
    parser.add_argument(
        "input",
        nargs="?",                  # optional when --interactive is used
        help="Path to a file or directory of files to send.",
    )
    parser.add_argument(
        "--dir",
        action="store_true",
        help="Treat INPUT as a directory and process all supported files in it.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="When --dir is set, also search sub-directories.",
    )
    parser.add_argument(
        "--interactive", "-i",
        nargs="?",
        const=".",                  # default to current directory if no path given
        metavar="DIR",
        help="Pick files interactively from DIR (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default="output/results.json",
        help="Where to write the JSON output (default: output/results.json).",
    )
    parser.add_argument(
        "--view",
        action="store_true",
        help="Browse and view a saved result from the output file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # --- View mode: browse saved results ---
    if args.view:
        try:
            results = load_results(args.output)
            selected = pick_result(results)
            print_result(selected)
        except (FileNotFoundError, ValueError) as exc:
            print(f"[error] {exc}")
            return 1
        except KeyboardInterrupt:
            print("\nCancelled.")
        return 0

    # --- 1. Collect files ---
    try:
        if args.interactive is not None:
            # Let the user pick from a numbered list
            paths = pick_files(args.interactive)
        elif args.dir:
            paths = collect_files(args.input, recursive=args.recursive)
            if not paths:
                print(f"No supported files found in {args.input}")
                return 1
        elif args.input:
            paths = [Path(args.input)]
        else:
            parser.print_help()
            return 1
    except FileReadError as exc:
        print(f"[error] {exc}")
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 0

    # --- 2. Read files ---
    documents = read_files(paths)
    if not documents:
        print("[error] No documents could be read.")
        return 1

    print(f"\nRead {len(documents)} document(s). Sending to {SERVER_URL}/analyze...")

    # --- 3. POST to API ---
    try:
        results = run_post(documents)
    except ApiError as exc:
        print(f"[error] {exc}")
        return 1

    # --- 4. Save + display ---
    out_path = save_results(results, args.output)
    # print_results(results)
    print(f"\nSaved {len(results)} result(s) to {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
