"""
server/app.py — FastAPI server that analyzes text documents.

Run with:
    uvicorn server.app:app --reload

Then open http://localhost:8000/docs to see the auto-generated API docs.

LEARN: FastAPI, Pydantic models, HTTP endpoints, request/response shapes.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Document Analyzer")


# --- Request and response shapes ---
# Pydantic models validate incoming JSON automatically.
# If the client sends the wrong shape, FastAPI returns a clear 422 error.

class DocumentIn(BaseModel):
    """What the client must send."""
    filename: str
    content: str



class AnalysisOut(BaseModel):
    """What the server sends back."""
    filename: str
    word_count: int
    line_count: int
    char_count: int
    headings: list[str]
    preview: str


# --- Endpoints ---

@app.get("/")
def root() -> dict:
    return {"status": "ok", "docs": "/docs"}


@app.post("/analyze", response_model=AnalysisOut)
def analyze(doc: DocumentIn) -> AnalysisOut:
    """
    Receive a document and return basic stats about it.

    LEARN: FastAPI reads the JSON body, validates it against DocumentIn,
    and passes it as a Python object. You just work with doc.filename,
    doc.content, etc. — no manual json.loads() needed.
    """
    lines = doc.content.splitlines()
    words = doc.content.split()
    # list comprehension: keep only lines that start with a markdown heading
    headings = [line.strip() for line in lines if line.startswith("#")]

    return AnalysisOut(
        filename=doc.filename,
        word_count=len(words),
        line_count=len(lines),
        char_count=len(doc.content),
        headings=headings,
        preview=doc.content,
    )
