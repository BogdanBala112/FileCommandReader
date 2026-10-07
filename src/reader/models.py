"""
models.py — data classes used throughout the app.

LEARN: classes, type hints, __repr__, dataclass decorator.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Document:
    """Represents a file that was read from disk."""
    path: str
    content: str
    char_count: int = field(init=False)

    def __post_init__(self) -> None:
        # field computed after __init__ runs
        self.char_count = len(self.content)

    def __repr__(self) -> str:
        return f"Document(path={self.path!r}, chars={self.char_count})"

    def preview(self, n: int = 200) -> str:
        """Return the first n characters of content."""
        return self.content[:n]


@dataclass
class ApiResult:
    """Represents the server's analysis response for one document."""
    document_path: str
    analysis: dict          # the JSON object returned by the server
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        """Serialize to a plain dict (for JSON storage)."""
        return {
            "document_path": self.document_path,
            "analysis": self.analysis,
            "timestamp": self.timestamp,
        }
