# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: "我现在的文件是houdini_run_llm.py, 这些prompt 单独建立md文件吗，怎么读取"
# Use: Modification of prompt organization to load prompts from separate
# Markdown files with pathlib.

# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: 2026-07-03
# Prompt: unknown
# Use: Initial implementation of Markdown code-fence removal before executing
# generated code.

# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: 2026-07-03
# Prompt: "我现在有test_llm_request.py文件，里面有ask_modelfunction，现在我想要在Houdini中能够直接获取并执行返回的python代码，该怎么做"
# Use: Initial design and implementation of the Houdini-to-ask_model-to-generated-code execution flow.

import sys
import hou



PROJECT_PYTHON_PATH = "/home/s5803453/Desktop/MasterProject/src"

if PROJECT_PYTHON_PATH not in sys.path:
    sys.path.append(PROJECT_PYTHON_PATH)

from test_llm_request import ask_model


from pathlib import Path

prompt_path = Path("/home/s5803453/Desktop/MasterProject/prompts/exp01_box.md")

prompt = prompt_path.read_text(encoding="utf-8")


def clean_code(text: str) -> str:
    text = text.strip()

    if text.startswith("```python"):
        text = text[len("```python"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


# prompt = """
# Generate only executable Houdini Python code.
# Do not use markdown code fences.

# Create:
# - one geometry container under /obj
# - one box SOP inside it
# - layout the SOP nodes

# Rules:
# - Do not call setNextInput on the geometry container.
# - Only connect SOP nodes inside the geometry container.
# - Use layoutChildren().
# """

code = ask_model(prompt)

# print("Raw code:")
# print(code)

code = clean_code(code)

# print("Cleaned code:")
# print(code)

# exec(code, {"hou": hou})
# 
blocked_words = ["subprocess", "os.system", "shutil", "deleteItems"]

if any(word in code for word in blocked_words):
    print("Blocked unsafe code")
else:
    exec(code, {"hou": hou})
