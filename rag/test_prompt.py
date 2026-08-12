from rag.prompt_builder import build_prompt
from rag.retrieve import retrieve


def main() -> None:
    user_prompt = (
        "Create a spiral staircase"
    )

    documents = retrieve(user_prompt, top_k=5)
    final_prompt = build_prompt(user_prompt, documents)

    # print(final_prompt)
    for r in documents:
        print(r.source, r.distance)


if __name__ == "__main__":
    main()