# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: 2026-07-03
# Prompt: unknown
# Use: Initial implementation of Markdown code-fence removal before executing
# generated code.

def clean_code(text: str) -> str:
    text = text.strip()

    if text.startswith("```python"):
        text = text[len("```python"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text

