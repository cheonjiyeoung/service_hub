from PySide6.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QHBoxLayout, QMessageBox, QVBoxLayout
from PySide6.QtCore import QTimer

from add_service_dialog import ServicePathDialog, ServiceNameDialog
from service_profile import ServiceProfile
from css import BUTTON, apply_frameless_style, enable_drag_move
# IPC 클라이언트 모듈
from service_hub_icp.utils import (
    list_services,
    register_service,
)
import sys
from event_bus import event_bus

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 레이아웃 구성
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

        # 전체 레이아웃
        layout_main.addLayout(self.layout_service_list)
        layout_main.addLayout(layout_btns)
        layout_main.addStretch(0)

    def refresh(self):
        # 기존 UI 제거
        while self.layout_service_list.count():
            item = self.layout_service_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 데몬에서 목록 받아오기
        resp = list_services()
        services = resp.get("services", [])

        for svc in services:
            name = svc["name"]
            profile = ServiceProfile(name)
            profile.init_ui()
            self.layout_service_list.addWidget(profile)

    def on_add_service(self):
        # Step 1: 서비스 이름
        name_dialog = ServiceNameDialog()
        if name_dialog.exec() != QDialog.Accepted:
            return

        service_name = name_dialog.get_service_name()
        if not service_name:
            return

        # Step 2: 파일 경로
        path_dialog = ServicePathDialog(service_name)
        if path_dialog.exec() != QDialog.Accepted:
            return

        service_path = path_dialog.get_service_path()
        if not (service_path and service_path.endswith(".sh")):
            return

        # IPC로 데몬에 등록 요청
        resp = register_service(service_name, service_path)

        if resp.get("error"):
            QMessageBox.warning(self, "Failed", str(resp["error"]))
            return

        print(f"[IPC] Registered: {service_name} -> {service_path}")

        # UI 갱신
        self.refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())
