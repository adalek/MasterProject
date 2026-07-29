from rag.prompt_builder import build_prompt
from rag.retrieve import retrieve

# 按你当前文件中的实际位置修改这个 import
from src.test_llm_request import ask_model


def generate_with_rag(
    user_prompt: str,
    top_k: int = 1,
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

    return ask_model(final_prompt)


def main() -> None:
    user_prompt = input("Enter a Houdini request: ").strip()

    if not user_prompt:
        raise ValueError("Prompt cannot be empty.")

    generated_code = generate_with_rag(user_prompt)

    print("\nGenerated Houdini Python:\n")
    print(generated_code)


if __name__ == "__main__":
    main()