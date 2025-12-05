from PySide6.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QHBoxLayout, QMessageBox, QVBoxLayout
from PySide6.QtCore import Qt, QPoint

from add_service_dialog import ServicePathDialog, ServiceNameDialog
from service_profile import ServiceProfile
from css import BUTTON, apply_frameless_style, enable_drag_move
from utils import return_config, register_service
import sys


class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 레이아웃 구성
        self.layout_service_list = QVBoxLayout()
        self.init_ui()
        self.initialize()

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

    def initialize(self):
        config = return_config()
        sections = config.sections()  # 서비스 이름 리스트

        for service_name in sections:
            profile = ServiceProfile(service_name)
            profile.init_ui()
            self.layout_service_list.addWidget(profile)

    def on_add_service(self):
        # 1단계: 서비스 이름 입력
        name_dialog = ServiceNameDialog()
        if name_dialog.exec() != QDialog.Accepted:
            return

        service_name = name_dialog.get_service_name()
        if not service_name:
            return  # 빈 입력이면 취소 처리

        # 2단계: sh 파일 경로 입력
        path_dialog = ServicePathDialog(service_name)
        if path_dialog.exec() != QDialog.Accepted:
            return

        service_path = path_dialog.get_service_path()
        if not (service_path and service_path.endswith(".sh")):
            return  # 안전성 체크

        # 최종적으로 서비스 등록 로직 호출
        try:
            register_service(service_name, service_path)
            print(f"Success: {service_name} -> {service_path}")
        except Exception as e:
            QMessageBox.warning(self, "Failed", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())
