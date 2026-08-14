import json
import os

import requests
from dotenv import load_dotenv


# 从项目根目录的 .env 加载配置
load_dotenv()


SYSTEM_PROMPT = (
    "You are a Houdini Python assistant. "
    "Output only executable Houdini Python code."
)


def request_chat_completion(
    prompt: str,
    *,
    api_url: str,
    api_key: str,
    model: str,
    temperature: float = 0.1,
) -> str:
    """Call an OpenAI-compatible Chat Completions API."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": temperature,
        "max_tokens": 6000,
        "stream": False,
    }

    response = requests.post(
        api_url,
        headers=headers,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()

    print("Full JSON response:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    choices = data.get("choices")

    if not choices:
        raise RuntimeError("The model response contains no choices.")

    first_choice = choices[0]
    finish_reason = first_choice.get("finish_reason")

    if finish_reason not in {"stop", None}:
        raise RuntimeError(
            f"Model generation ended unexpectedly: {finish_reason}"
        )

    content = first_choice.get("message", {}).get("content")

    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("The model returned empty content.")

    return content.strip()


def ask_local_model(prompt: str) -> str:
    """Call the local llama.cpp Qwen server."""

    return request_chat_completion(
        prompt,
        api_url=os.getenv(
            "LOCAL_API_URL",
            "http://127.0.0.1:8080/v1/chat/completions",
        ),
        api_key=os.getenv("LOCAL_API_KEY", "12345"),
        model=os.getenv(
            "LOCAL_MODEL",
            "Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
        ),
        temperature=0.1,
    )


def ask_deepseek_model(prompt: str) -> str:
    """Call the DeepSeek cloud API."""

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY is missing from the environment."
        )

    return request_chat_completion(
        prompt,
        api_url=os.getenv(
            "DEEPSEEK_API_URL",
            "https://api.deepseek.com/chat/completions",
        ),
        api_key=api_key,
        model=os.getenv(
            "DEEPSEEK_MODEL",
            "deepseek-v4-flash",
        ),
        temperature=0.1,
    )


def ask_model(
    prompt: str,
    provider: str | None = None,
) -> str:
    """Select a model provider and return its response."""

    prompt = prompt.strip()

    if not prompt:
        raise ValueError("prompt cannot be empty.")

    if provider is None:
        provider = os.getenv(
            "MODEL_PROVIDER",
            "local",
        )

    provider = provider.lower().strip()

    print(f"Model provider: {provider}")

    if provider == "local":
        return ask_local_model(prompt)

    if provider == "deepseek":
        return ask_deepseek_model(prompt)

    raise ValueError(
        f"Unsupported model provider: {provider}"
    )