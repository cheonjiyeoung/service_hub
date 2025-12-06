from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer
from ui.dialogs.service_menu_dialog import ServiceMenuDialog
from service_hub_ipc.utils import return_service_state
from css.css import BUTTON

ACTIVE = "🟢"
INACTIVE = "🔴"
ERROR = "⚠️"
INIT = "⏳"

class ServiceProfile(QWidget):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
        self.status = INIT

        self.layout_main = QHBoxLayout(self)
        self.setStyleSheet("font-family: 'Inter'; font-size: 12px;")

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update_status)

    def _update_status(self):
        try:
            state = return_service_state(self.service_name).get("state")
            
            if state == "active":
                self.status = ACTIVE
            elif state == "inactive":
                self.status = INACTIVE
            elif state == "failed":
                self.status = ERROR
            else:
                self.status = ERROR
            
            self.label_status.setText(self.status)

        except Exception:
            self.label_status.setText(ERROR)

    def init_ui(self):
        self.label_status = QLabel(self.status)
        self.label_status.setStyleSheet("font-size: 20px; padding: 0px; margin: 0px;")

        self.service_button = QPushButton(self.service_name)
        self.service_button.setStyleSheet(BUTTON)
        self.service_button.clicked.connect(self.on_click)

        self.layout_main.addWidget(self.label_status)
        self.layout_main.addWidget(self.service_button)

        self.timer.start()

    def on_click(self):
        self.dialog = ServiceMenuDialog(self.service_name)
        self.dialog.show()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)

    test_window = QWidget()
    layout = QVBoxLayout(test_window)

    services = [
        "ssh",
        "cron",
        "NetworkManager",
    ]

    for svc in services:
        widget = ServiceProfile(svc)
        widget.init_ui()
        layout.addWidget(widget)

    test_window.setStyleSheet("background-color: #3a3a3a;")
    test_window.show()

    sys.exit(app.exec())