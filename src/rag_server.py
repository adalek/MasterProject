# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: GUI/server integration, model-provider selection, and RAG on/off routing.
# Use: Modification and debugging assistance for the FastAPI generation endpoint.

# AI-assisted architecture/design.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: Houdini GUI to FastAPI generation flow with provider and RAG selection.
# Use: Design of the MVP integration boundary and server-side generation routing.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.generate import generate
from src.generate_with_rag import generate_with_rag


app = FastAPI(
    title="Houdini RAG Server",
    version="0.1.0",
)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    top_k: int = Field(default=1, ge=1, le=10)
    provider: str = Field(default="local")
    rag_enabled: bool = True


class RetrievedSource(BaseModel):
    source: str
    distance: float | None


class GenerateResponse(BaseModel):
    code: str
    retrieved_sources: list[RetrievedSource]


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the RAG service is running."""

    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate_code(request: GenerateRequest) -> GenerateResponse:
    """Generate executable Houdini Python code."""

    try:
        if request.rag_enabled:
            code, documents = generate_with_rag(
                user_prompt=request.prompt,
                top_k=request.top_k,
                provider=request.provider,
            )

        else:
            code = generate(
                user_prompt=request.prompt,
                provider=request.provider,
            )

            documents = []

        if not code.strip():
            raise RuntimeError("The model returned empty code.")

        return GenerateResponse(
            code=code,
            retrieved_sources=[
                RetrievedSource(
                    source=document.source,
                    distance=document.distance,
                )
                for document in documents
            ],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error
