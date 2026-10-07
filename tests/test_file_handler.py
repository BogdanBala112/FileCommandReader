"""
test_file_handler.py

LEARN: pytest basics — fixtures, tmp_path, asserting exceptions.
"""
import pytest

from src.reader.file_handler import FileReadError, collect_files, read_file, read_files
from src.reader.models import Document


def test_read_file_returns_document(tmp_path):
    """tmp_path is a pytest fixture that gives us a fresh temporary directory."""
    doc_file = tmp_path / "hello.md"
    doc_file.write_text("# Hello\nThis is a test.", encoding="utf-8")

    doc = read_file(doc_file)

    assert isinstance(doc, Document)
    assert doc.char_count == len("# Hello\nThis is a test.")
    assert "Hello" in doc.content


def test_read_file_missing_raises():
    """Expect FileReadError when the file does not exist."""
    with pytest.raises(FileReadError, match="File not found"):
        read_file("/tmp/does_not_exist_xyz.md")


def test_read_file_unsupported_extension(tmp_path):
    bad_file = tmp_path / "data.csv"
    bad_file.write_text("a,b,c")

    with pytest.raises(FileReadError, match="Unsupported file type"):
        read_file(bad_file)


def test_read_files_skips_bad_files(tmp_path):
    """read_files should skip unreadable files and return the rest."""
    good = tmp_path / "good.txt"
    good.write_text("content", encoding="utf-8")

    docs = read_files([good, "/nonexistent/file.txt"])

    assert len(docs) == 1
    assert docs[0].path == str(good)


def test_collect_files_finds_supported(tmp_path):
    (tmp_path / "a.md").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "c.csv").write_text("c")  # unsupported

    found = collect_files(tmp_path)

    names = {p.name for p in found}
    assert "a.md" in names
    assert "b.txt" in names
    assert "c.csv" not in names


def test_collect_files_recursive(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "deep.md").write_text("deep")

    # non-recursive: should NOT find it
    assert not any(p.name == "deep.md" for p in collect_files(tmp_path, recursive=False))

    # recursive: should find it
    assert any(p.name == "deep.md" for p in collect_files(tmp_path, recursive=True))
