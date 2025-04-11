# frontend.py
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QTextEdit, QPushButton, QMessageBox
)

class CodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Code Generator")
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.prompt_label = QLabel("Describe your task in English:")
        self.prompt_input = QTextEdit()
        self.generate_button = QPushButton("Generate Code")
        self.result_label = QLabel("Generated Code:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect the generate button to the function
        self.generate_button.clicked.connect(self.generate_code)

    def generate_code(self):
        """
        Fetch generated code from the Flask backend based on English task description.
        """
        prompt = self.prompt_input.toPlainText()
        if not prompt.strip():
            QMessageBox.warning(self, "Input Error", "Task description cannot be empty!")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/generate",
                json={"prompt": prompt, "max_length": 150, "temperature": 0.7}
            )
            response_data = response.json()

            if "error" in response_data:
                QMessageBox.critical(self, "Error", response_data["error"])
                return

            generated_code = response_data["generated_code"]
            self.result_output.setText(generated_code)

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Unable to connect to the backend server.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeGeneratorApp()
    window.show()
    sys.exit(app.exec_())
