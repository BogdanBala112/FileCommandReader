"""
test_storage.py

LEARN: testing JSON round-trips, asserting file contents.
"""
import json

import pytest

from src.reader.models import ApiResult
from src.reader.storage import load_results, save_results


def _make_result(path: str = "doc.md") -> ApiResult:
    return ApiResult(
        document_path=path,
        analysis={"word_count": 10, "line_count": 3, "char_count": 42, "headings": ["# Hello"]},
    )


def test_save_creates_json_file(tmp_path):
    results = [_make_result("a.md"), _make_result("b.md")]
    out = tmp_path / "out" / "results.json"

    returned_path = save_results(results, out)

    assert returned_path == out
    assert out.exists()


def test_saved_json_is_valid(tmp_path):
    result = _make_result("x.md")
    out = tmp_path / "r.json"
    save_results([result], out)

    raw = json.loads(out.read_text())
    assert isinstance(raw, list)
    assert raw[0]["document_path"] == "x.md"
    assert raw[0]["analysis"]["word_count"] == 10


def test_load_results_round_trip(tmp_path):
    results = [_make_result("a.md")]
    out = tmp_path / "r.json"
    save_results(results, out)

    loaded = load_results(out)
    assert loaded[0]["document_path"] == "a.md"
    assert loaded[0]["analysis"]["headings"] == ["# Hello"]


def test_load_results_missing_file():
    with pytest.raises(FileNotFoundError):
        load_results("/tmp/no_such_file_xyz.json")


def test_load_results_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json {{")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_results(bad)
