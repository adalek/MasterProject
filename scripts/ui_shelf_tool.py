import sys
import importlib

PROJECT_ROOT = "/home/s5803453/Desktop/MasterProject"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import src.ui
importlib.reload(src.ui)

src.ui.show_window()