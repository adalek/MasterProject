# create new shelf tool in Houdini, choose Pyhton as script language
# AI-assisted implementation.
# Tool: OpenAI ChatGPT
# Date: unknown
# Prompt: "现在在python shell 里 read houdini_run文件太麻烦了，怎么做成shelf tool点击运行"
# Use: Initial implementation of a Houdini Shelf Tool launcher that reads and
# executes the project runner.

import traceback

script_path = "/home/s5803453/Desktop/MasterProject/python/houdini_run_llm.py"

try:
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    exec(code)

except Exception:
    traceback.print_exc()
