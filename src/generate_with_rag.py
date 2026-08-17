# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: Integrate GUI-selected model provider with RAG and non-RAG generation.
# Use: Modification of the generation pipeline to propagate the selected provider.

from rag.prompt_builder import build_prompt
from rag.retrieve import retrieve

# 按你当前文件中的实际位置修改这个 import
from src.ask_model import ask_model
from src.clean_code import clean_code


def generate_with_rag(
    user_prompt: str,
    top_k: int = 1,
    provider: str | None = None,
) -> str:
    """Retrieve Houdini references and generate Houdini Python code."""

    documents = retrieve(user_prompt, top_k=top_k)
    final_prompt = build_prompt(user_prompt, documents)

    print("Retrieved sources:")
    for document in documents:
        print(
            f"- {document.source}, "
            f"distance={document.distance:.4f}"
            if document.distance is not None
            else f"- {document.source}"
        )
    
    raw_response = ask_model(final_prompt, provider=provider)
    code = clean_code(raw_response)

    if not code:
        raise ValueError(
            "The model response was empty after cleaning."
        )

    return code, documents


def main() -> None:
    user_prompt = input("Enter a Houdini request: ").strip()

    if not user_prompt:
        raise ValueError("Prompt cannot be empty.")

    generated_code = generate_with_rag(user_prompt)

    print("\nGenerated Houdini Python:\n")
    print(generated_code)


if __name__ == "__main__":
    main()
