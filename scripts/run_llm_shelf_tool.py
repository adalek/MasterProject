# create new shelf tool in Houdini, choose Pyhton as script language
import traceback

script_path = "/home/s5803453/Desktop/MasterProject/python/houdini_run_llm.py"

try:
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    exec(code)

except Exception:
    traceback.print_exc()