"""
api_client.py — HTTP requests to the local FastAPI server.

LEARN: HTTP requests with httpx, async/await, dictionaries, type hints,
       custom exceptions, environment variables.
"""
import asyncio
import os

import httpx
from dotenv import load_dotenv

from .models import ApiResult, Document

load_dotenv()

# Base URL is read from .env so you can point the client at any server
# without changing code. Defaults to the local dev server.
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8000")


class ApiError(Exception):
    """Raised when the API returns an error or is unreachable."""


def _build_payload(doc: Document) -> dict:
    """
    Build the JSON body we POST to /analyze.

    LEARN: dictionaries — key/value pairs.
    The server expects exactly these keys (defined by DocumentIn in server/app.py).
    """
    return {
        "filename": doc.path,
        "content": doc.content,
    }


async def post_document(doc: Document, client: httpx.AsyncClient) -> ApiResult:
    """
    POST one document to /analyze and return the result.

    LEARN: async def, await, httpx.AsyncClient, raising exceptions.
    """
    payload = _build_payload(doc)

    try:
        response = await client.post(
            f"{SERVER_URL}/analyze",
            json=payload,
            timeout=10.0,
        )
        response.raise_for_status()  # raises on 4xx / 5xx
    except httpx.HTTPStatusError as exc:
        raise ApiError(f"Server returned {exc.response.status_code}: {exc.response.text}") from exc
    except httpx.RequestError as exc:
        raise ApiError(f"Could not reach server at {SERVER_URL}: {exc}") from exc

    return ApiResult(
        document_path=doc.path,
        analysis=response.json(),
    )


async def post_all(documents: list[Document]) -> list[ApiResult]:
    """
    POST all documents concurrently.

    LEARN: asyncio.gather fires all requests at the same time instead of
    one-by-one. If you have 5 files, total time ≈ slowest single request,
    not the sum of all of them.
    """
    async with httpx.AsyncClient() as client:
        tasks = [post_document(doc, client) for doc in documents]
        results: list[ApiResult] = await asyncio.gather(*tasks)
    return list(results)


def run_post(documents: list[Document]) -> list[ApiResult]:
    """Synchronous entry point — wraps the async function for CLI use."""
    return asyncio.run(post_all(documents))
