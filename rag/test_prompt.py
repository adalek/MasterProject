from rag.prompt_builder import build_prompt
from rag.retrieve import retrieve


def main() -> None:
    user_prompt = (
        "Create a procedural staircase with 12 steps."
    )

    documents = retrieve(user_prompt, top_k=1)
    final_prompt = build_prompt(user_prompt, documents)

    print(final_prompt)


if __name__ == "__main__":
    main()