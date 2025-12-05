from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer
from utils import return_service_state
# from css import BUTTON

BUTTON = """
    QPushButton {
        background-color: transparent;
        color: white;
        border: none;
        text-align: right;
    }
    QPushButton:hover {
        background-color: #505050;
    }
"""

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
        self.timer.setInterval(1000)            # 1초 주기
        self.timer.timeout.connect(self._update_status)
        self.init_ui()

    def _update_status(self):
        try:
            # 실제 systemctl 조회 대신 임시 랜덤 상태 사용
            # service_state = self.temp()
            # self.label_status.setText(service_state)
            # return

            # 실제 systemctl 기반 사용할 경우:
            result = return_service_state(self.service_name)
            state = result.stdout.strip()
            
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
        # 상태 인디케이터 (왼쪽)
        self.label_status = QLabel(self.status)
        self.label_status.setStyleSheet("font-size: 20px; padding: 0px; margin: 0px;")

        # 서비스 이름 버튼 (왼쪽 정렬 유지)
        self.service_button = QPushButton(self.service_name)
        self.service_button.setStyleSheet(BUTTON)
        self.service_button.clicked.connect(self.on_click)

        # 레이아웃 ← 인디케이터 → 버튼 순서
        self.layout_main.addWidget(self.label_status)   # 왼쪽 끝
        self.layout_main.addWidget(self.service_button) # 그 오른쪽

        self.timer.start()

    def temp(self):
        import random
        states = [ACTIVE, INACTIVE, ERROR]
        return random.choice(states)
    
    def on_click(self):
        from service_menu_dialog import ServiceMenuDialog
        self.dialog = ServiceMenuDialog(self.service_name)  # 인스턴스 변수로 저장
        self.dialog.show()  #


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)

    test_window = QWidget()
    layout = QVBoxLayout(test_window)

    # 테스트용 서비스 목록
    services = [
        "ssh",
        "cron",
        "NetworkManager",
    ]

    for svc in services:
        widget = ServiceProfile(svc)
        widget.init_ui()
        layout.addWidget(widget)

    test_window.setStyleSheet("background-color: #3a3a3a;")  # 테스트용 배경색
    test_window.show()

    sys.exit(app.exec())