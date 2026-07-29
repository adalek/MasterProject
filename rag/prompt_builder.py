from rag.retrieve import RetrievedDocument, format_retrieved_context


SYSTEM_INSTRUCTIONS = """You are a Houdini Python code generator.

Generate only executable Python code for Houdini.
Do not use Markdown code fences.
Do not explain the solution.
Use the hou Python API.
Create SOP nodes inside a Geometry container under /obj.
Use explicit node variables and explicit setInput calls.
Set display and render flags on the intended final SOP node.
Layout the created nodes when appropriate.
"""


def build_prompt(
    user_prompt: str,
    retrieved_documents: list[RetrievedDocument],
) -> str:
    """Build the final prompt sent to the code-generation model."""

    user_prompt = user_prompt.strip()

    if not user_prompt:
        raise ValueError("user_prompt cannot be empty.")

    context = format_retrieved_context(retrieved_documents)

    return f"""{SYSTEM_INSTRUCTIONS}

The following references contain verified Houdini patterns.
Use them as guidance when they are relevant.
Do not copy irrelevant parts.
The user's current request has priority over reference-specific values.

<retrieved_context>
{context}
</retrieved_context>

<user_request>
{user_prompt}
</user_request>

Return only executable Houdini Python code.
"""