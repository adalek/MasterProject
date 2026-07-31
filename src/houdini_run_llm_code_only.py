import sys
from pathlib import Path

import hou


PROJECT_ROOT = Path("/home/s5803453/Desktop/MasterProject")

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.generate import generate


PROMPT_PATH = PROJECT_ROOT / "prompts" / "exp05_staircase.md"

prompt = PROMPT_PATH.read_text(encoding="utf-8")

code = generate(prompt)


blocked_words = [
    "subprocess",
    "os.system",
    "shutil",
    "deleteItems",
]

if any(word in code for word in blocked_words):
    raise RuntimeError("Blocked unsafe generated code.")

exec(code, {"hou": hou})