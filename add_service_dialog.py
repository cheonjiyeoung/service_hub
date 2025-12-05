from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog
)
from css import BUTTON, enable_drag_move, apply_frameless_style

class ServiceNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        # layout = QVBoxLayout(self)
        layout = apply_frameless_style(self)
        enable_drag_move(self)

        self.label = QLabel("Input your service name:")
        layout.addWidget(self.label)

        self.edit = QLineEdit()
        layout.addWidget(self.edit)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_ok.setStyleSheet(BUTTON)
        layout.addWidget(btn_ok)

    def get_service_name(self):
        return self.edit.text().strip()

class ServicePathDialog(QDialog):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
        layout = apply_frameless_style(self)
        enable_drag_move(self)

        # layout = QVBoxLayout(self)

        self.label = QLabel("Input target file(.sh):")
        layout.addWidget(self.label)

        self.edit = QLineEdit()
        layout.addWidget(self.edit)

        btn_select = QPushButton("Browse")
        btn_select.setStyleSheet(BUTTON)
        btn_select.clicked.connect(self.select_file)
        btn_select.setStyleSheet(BUTTON)
        layout.addWidget(btn_select)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "shell script file for register",
            "",
            "Shell Script (*.sh)"
        )
        if file_path:
            self.edit.setText(file_path)

    def get_service_path(self):
        return self.edit.text().strip()
