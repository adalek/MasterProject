#!/usr/bin/env python3

# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: unknown
# Use: Initial implementation of HTTP communication with the local llama.cpp
# OpenAI-compatible API, JSON response parsing, and model-output extraction.

import json
import requests

API_URL = "http://127.0.0.1:8080/v1/chat/completions"
API_KEY = "12345"


def ask_model(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
        "messages": [
            {
                "role": "system",
                "content": "You are a Houdini Python assistant. Output only code.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.1,
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()

    print("Full JSON response:")
    print(json.dumps(data, indent=2))

    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    prompt = "Generate Houdini Python code that creates a box node under /obj."
    result = ask_model(prompt)

    print("\nModel content:")
    print(result)
