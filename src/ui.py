from PySide6 import QtCore, QtWidgets
import hou
import requests


_window = None


class HoudiniAIAgentWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Houdini AI Agent")
        self.resize(500, 400)

        layout = QtWidgets.QVBoxLayout(self)

        # Prompt
        layout.addWidget(QtWidgets.QLabel("Prompt"))

        self.prompt_input = QtWidgets.QPlainTextEdit()
        self.prompt_input.setPlaceholderText(
            "Describe what you want to create in Houdini..."
        )
        layout.addWidget(self.prompt_input)

        # Model
        layout.addWidget(QtWidgets.QLabel("Model"))

        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.addItems([
            "Local Qwen",
            "DeepSeek",
        ])
        layout.addWidget(self.model_combo)

        # RAG
        self.rag_checkbox = QtWidgets.QCheckBox("Enable RAG")
        self.rag_checkbox.setChecked(True)
        layout.addWidget(self.rag_checkbox)

        # Generate
        self.generate_button = QtWidgets.QPushButton("Generate")
        layout.addWidget(self.generate_button)
        layout.addWidget(QtWidgets.QLabel("Generated Code"))
        
        self.code_output = QtWidgets.QPlainTextEdit()
        self.code_output.setReadOnly(True)
        layout.addWidget(self.code_output)
        
        # Execute
        self.execute_button = QtWidgets.QPushButton("Execute")
        layout.addWidget(self.execute_button)
        
        self.execute_button.clicked.connect(
            self.on_execute_clicked
        )

        # Status
        self.status_label = QtWidgets.QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.generate_button.clicked.connect(self.on_generate_clicked)

    def on_generate_clicked(self):
        prompt = self.prompt_input.toPlainText().strip()
    
        if not prompt:
            self.status_label.setText(
                "Status: Please enter a prompt"
            )
            return
    
        self.status_label.setText(
            "Status: Generating..."
        )
    
        payload = {
            "prompt": prompt,
            "top_k": 1,
        }
    
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json=payload,
                timeout=180,
            )
    
            response.raise_for_status()
    
            data = response.json()
            code = data["code"]
    
            self.code_output.setPlainText(code)
    
            self.status_label.setText(
                "Status: Generation complete"
            )
    
        except requests.RequestException as error:
            print(error)
    
            self.status_label.setText(
                "Status: Server request failed"
            )

    def on_execute_clicked(self):
        code = self.code_output.toPlainText().strip()
    
        if not code:
            self.status_label.setText(
                "Status: No code to execute"
            )
            return
    
        blocked_words = [
            "subprocess",
            "os.system",
            "shutil",
            "deleteItems",
        ]
    
        if any(word in code for word in blocked_words):
            self.status_label.setText(
                "Status: Unsafe code blocked"
            )
            return
    
        try:
            exec(
                code,
                {
                    "hou": hou,
                    "__builtins__": __builtins__,
                },
            )
    
            self.status_label.setText(
                "Status: Execution complete"
            )
    
        except Exception as error:
            print("Execution error:")
            print(error)
    
            self.status_label.setText(
                f"Status: Execution failed: {error}"
            )

def show_window():
    global _window

    # 已经存在就直接显示，不重复创建
    if _window is None:
        _window = HoudiniAIAgentWindow(
            parent=hou.qt.mainWindow()
        )

        # 明确告诉 Qt：这是独立窗口
        _window.setWindowFlags(QtCore.Qt.Window)

    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window