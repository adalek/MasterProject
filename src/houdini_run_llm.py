import json
import sys
from pathlib import Path
from urllib import error, request

import hou


PROJECT_ROOT = Path(
    "/home/s5803453/Desktop/MasterProject"
)

PROMPT_PATH = (
    PROJECT_ROOT
    / "prompts"
    / "exp06_staircase.md"
)

RAG_SERVER_URL = "http://127.0.0.1:8000/generate"


def request_rag_code(
    prompt: str,
    top_k: int = 1,
) -> str:
    """Request generated Houdini code from the external RAG server."""

    payload = json.dumps(
        {
            "prompt": prompt,
            "top_k": top_k,
        }
    ).encode("utf-8")

    http_request = request.Request(
        RAG_SERVER_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(
            http_request,
            timeout=180,
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

    except error.HTTPError as http_error:
        response_body = http_error.read().decode(
            "utf-8",
            errors="replace",
        )

        raise RuntimeError(
            f"RAG server returned HTTP "
            f"{http_error.code}: {response_body}"
        ) from http_error

    except error.URLError as connection_error:
        raise RuntimeError(
            "Could not connect to the RAG server. "
            "Start it with: "
            "uv run uvicorn src.rag_server:app "
            "--host 127.0.0.1 --port 8000"
        ) from connection_error

    code = result.get("code")

    if not isinstance(code, str) or not code.strip():
        raise RuntimeError(
            "RAG server returned no generated code."
        )

    return code.strip()


prompt = PROMPT_PATH.read_text(
    encoding="utf-8"
).strip()

if not prompt:
    raise RuntimeError(
        f"Prompt file is empty: {PROMPT_PATH}"
    )

code = request_rag_code(
    prompt=prompt,
    top_k=1,
)

blocked_words = [
    "subprocess",
    "os.system",
    "shutil",
    "deleteItems",
]

detected_words = [
    word
    for word in blocked_words
    if word in code
]

if detected_words:
    raise RuntimeError(
        "Blocked unsafe generated code: "
        + ", ".join(detected_words)
    )

exec(
    code,
    {
        "__builtins__": __builtins__,
        "hou": hou,
    },
)