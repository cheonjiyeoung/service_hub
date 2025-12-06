from PySide6.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QHBoxLayout, QMessageBox, QVBoxLayout

from ui.dialogs.add_service_dialog import ServicePathDialog, ServiceNameDialog
from ui.service_profile import ServiceProfile
from css.css import BUTTON, apply_frameless_style, enable_drag_move
from service_hub_ipc.utils import (
    list_services,
    register_service,
)
import sys
from core.event_bus import event_bus

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_service_list = QVBoxLayout()
        self.init_ui()
        self.refresh()
        event_bus.service_changed.connect(self.refresh)

    def init_ui(self):
        layout_main = apply_frameless_style(self)
        enable_drag_move(self)

        layout_btns = QHBoxLayout()
        btn_add_service = QPushButton("Add")
        btn_add_service.setStyleSheet(BUTTON)
        btn_add_service.clicked.connect(self.on_add_service)
        layout_btns.addWidget(btn_add_service)

        layout_main.addLayout(self.layout_service_list)
        layout_main.addLayout(layout_btns)
        layout_main.addStretch(0)

    def refresh(self):
        while self.layout_service_list.count():
            item = self.layout_service_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        resp = list_services()
        services = resp.get("services", [])

        for svc in services:
            name = svc["name"]
            profile = ServiceProfile(name)
            profile.init_ui()
            self.layout_service_list.addWidget(profile)

    def on_add_service(self):
        name_dialog = ServiceNameDialog()
        if name_dialog.exec() != QDialog.Accepted:
            return

        service_name = name_dialog.get_service_name()
        if not service_name:
            return

        path_dialog = ServicePathDialog(service_name)
        if path_dialog.exec() != QDialog.Accepted:
            return

        service_path = path_dialog.get_service_path()
        if not (service_path and service_path.endswith(".sh")):
            return

        resp = register_service(service_name, service_path)

        if resp.get("error"):
            QMessageBox.warning(self, "Failed", str(resp["error"]))
            return

        print(f"[IPC] Registered: {service_name} -> {service_path}")

        self.refresh()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

if __name__ == "__main__":
    from ui.system_tray import SystemTray
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()

    tray = SystemTray(app, window)

    sys.exit(app.exec())
