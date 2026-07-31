from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.generate_with_rag import generate_with_rag


app = FastAPI(
    title="Houdini RAG Server",
    version="0.1.0",
)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    top_k: int = Field(default=1, ge=1, le=10)


class GenerateResponse(BaseModel):
    code: str


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the RAG service is running."""

    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate_code(request: GenerateRequest) -> GenerateResponse:
    """Retrieve Houdini knowledge and generate executable Python code."""

    try:
        code = generate_with_rag(
            user_prompt=request.prompt,
            top_k=request.top_k,
        )

        if not code.strip():
            raise RuntimeError("The model returned empty code.")

        return GenerateResponse(code=code)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error