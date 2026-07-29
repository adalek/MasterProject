from src.ask_model import ask_model
from src.clean_code import clean_code


def generate(user_prompt: str) -> str:
    """
    Generate executable Houdini Python code without RAG.

    Args:
        user_prompt:
            The original Houdini task description.

    Returns:
        Cleaned Houdini Python code.

    Raises:
        ValueError:
            If the prompt is empty or the model returns empty content.
        RuntimeError:
            If code generation fails.
    """

    user_prompt = user_prompt.strip()

    if not user_prompt:
        raise ValueError("user_prompt cannot be empty.")

    try:
        raw_response = ask_model(user_prompt)
    except Exception as error:
        raise RuntimeError(
            f"Failed to request code from the model: {error}"
        ) from error

    if not raw_response or not raw_response.strip():
        raise ValueError("The model returned an empty response.")

    generated_code = clean_code(raw_response)

    if not generated_code.strip():
        raise ValueError(
            "The model response became empty after code cleaning."
        )

    return generated_code


def main() -> None:
    """
    CLI entry point for testing generation without RAG.
    """

    try:
        user_prompt = input("Enter a Houdini request: ").strip()

        generated_code = generate(user_prompt)

        print("\nGenerated Houdini Python:\n")
        print(generated_code)

    except KeyboardInterrupt:
        print("\nGeneration cancelled.")

    except Exception as error:
        print(f"\nError: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()