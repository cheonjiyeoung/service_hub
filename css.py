from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

BUTTON = """
    QPushButton {
        background-color: transparent;
        color: white;
        border: none;
    }
    QPushButton:hover {
        background-color: #505050;
    }
"""

def apply_frameless_style(target):
    """QWidget 또는 QDialog 에 프레임리스 UI를 적용 (함수 기반 Mixin)"""

    target._old_pos = None

    # 공통 스타일
    target.setStyleSheet("background-color: #3c3c3c; color: white; font-family: 'Inter'; font-size: 12px;")
    target.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

    # 메인 레이아웃 생성 (대부분 QWidget/QDialog 모두 setLayout 가능)
    main_layout = QVBoxLayout(target)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # -----------------------------
    # Title Bar
    # -----------------------------
    title_bar = QWidget()
    title_bar.setFixedHeight(35)
    title_bar.setStyleSheet("background-color: #2f2f2f;")

    close_btn = QPushButton("✕")
    close_btn.setFixedSize(35, 35)
    close_btn.setStyleSheet(BUTTON)
    close_btn.clicked.connect(target.close)

    minimize_btn = QPushButton("−")
    minimize_btn.setFixedSize(35, 35)
    minimize_btn.setStyleSheet(BUTTON)

    # showMinimized 가 없는 Dialog에서는 대응하지 않음
    if hasattr(target, "showMinimized"):
        minimize_btn.clicked.connect(target.showMinimized)

    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(0, 0, 0, 0)
    title_layout.addStretch()
    title_layout.addWidget(minimize_btn)
    title_layout.addWidget(close_btn)

    main_layout.addWidget(title_bar)

    # Body Layout – 이후 실제 UI는 이 레이아웃 아래에 추가
    body_layout = QVBoxLayout()
    body_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.addLayout(body_layout)

    # body 레이아웃을 반환해서 자식이 더 붙일 수 있도록 한다
    return body_layout


# -------------------------------------------------------------
# 공통 드래그 이동 이벤트 (함수로 적용)
# -------------------------------------------------------------
def enable_drag_move(target):
    """마우스 드래그 이동 기능을 target 객체에 주입"""

    def mousePressEvent(event):
        if event.button() == Qt.LeftButton:
            target._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(event):
        if target._old_pos is not None:
            delta = event.globalPosition().toPoint() - target._old_pos
            target.move(target.x() + delta.x(), target.y() + delta.y())
            target._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(event):
        target._old_pos = None

    target.mousePressEvent = mousePressEvent
    target.mouseMoveEvent = mouseMoveEvent
    target.mouseReleaseEvent = mouseReleaseEvent