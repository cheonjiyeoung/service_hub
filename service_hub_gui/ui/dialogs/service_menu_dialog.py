from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTextBrowser, QApplication, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal
import sys

from service_hub_icp.utils import (disable_service, restart_service, start_service,
                   stop_service, stream_logs, unregister_service,
                   enable_service, modify_service_file)

from core.event_bus import event_bus
from css.css import BUTTON, TITLE_BUTTON

class FileViewerDialog(QDialog):
    def __init__(self, path: str, file_text: str):
        super().__init__()
        self.setWindowTitle(f"{path}")
        self.setMinimumSize(600, 500)
        self.setWindowFlags(Qt.Window)
        self.path = path

        layout = QVBoxLayout(self)

        self.viewer = QTextEdit()
        self.viewer.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 13px;")
        self.viewer.setText(file_text)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.on_click)

        layout.addWidget(self.viewer)
        layout.addWidget(btn_ok)

    def on_click(self):
        content = self.viewer.toPlainText()
        modify_service_file(self.path, content)
        self.accept()

# -------------------------
# Log Streaming Thread
# -------------------------
class LogStreamThread(QThread):
    log_received = Signal(str)

    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
        self.running = True
        self.process = None

    def run(self):
        for line in stream_logs(self.service_name):
            if not self.running:
                break
            log = line.get("log")
            if log:
                self.log_received.emit(log)
            

    def stop(self):
        self.running = False

# -------------------------
# ServiceMenuDialog with Resize + Move
# -------------------------
class ServiceMenuDialog(QDialog):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

        # 프레임 제거 + 커스텀 UI
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet("background-color: #2f2f2f; color: white; font-family: 'Inter'; font-size: 12px;")

        # self.resize(600, 400)

        # State
        self._old_pos = None
        self.resize_margin = 8
        self.resizing = False
        self.resize_edge = []
        self.logs_shown = False
        self.log_thread = None

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(8)

        # -------------------------
        # Title Bar
        # -------------------------
        title_bar = QWidget()
        title_bar.setFixedHeight(38)
        title_bar.setStyleSheet("background-color: #353535; border-radius: 4px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        title_label = QLabel(f"Service Manager — {self.service_name}")
        title_label.setStyleSheet("color: white; font-size: 10px;")

        close_btn = QPushButton("✕")
        close_btn.setStyleSheet(TITLE_BUTTON)
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        self.layout.addWidget(title_bar)

        # -------------------------
        # Service Controls
        # -------------------------
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        start_button = QPushButton("Start")
        start_button.clicked.connect(lambda: start_service(self.service_name))
        
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(lambda: stop_service(self.service_name))
        
        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(lambda: restart_service(self.service_name))

        enable_button = QPushButton("Enable")
        enable_button.clicked.connect(lambda: enable_service(self.service_name))

        disable_button = QPushButton("Disable")
        disable_button.clicked.connect(lambda: disable_service(self.service_name))
        
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_service)
        
        logs_button = QPushButton("View Logs")
        logs_button.clicked.connect(self.open_log_stream)

        modify_button = QPushButton("Modify")
        modify_button.clicked.connect(self.modify_system_file)
        

        for btn in (start_button, stop_button, restart_button, disable_button,
                    remove_button, logs_button, enable_button, modify_button):
            btn.setStyleSheet(BUTTON)

        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)
        control_layout.addWidget(restart_button)
        control_layout.addWidget(enable_button)
        control_layout.addWidget(disable_button)
        control_layout.addWidget(remove_button)
        control_layout.addWidget(modify_button)
        control_layout.addWidget(logs_button)

        self.layout.addLayout(control_layout)
        # self.layout.addStretch(0)

    # -------------------------
    # Log Stream UI
    # -------------------------
    def open_log_stream(self):
        if self.logs_shown:
            return

        self.logs_shown = True

        self.log_viewer = QTextBrowser()
        self.log_viewer.setStyleSheet("background-color: #1f1f1f; padding: 6px; border-radius: 6px;")
        self.log_viewer.setMinimumHeight(250)

        self.layout.addWidget(self.log_viewer)

        self.log_thread = LogStreamThread(self.service_name)
        self.log_thread.log_received.connect(self.append_log)
        self.log_thread.start()

    def append_log(self, msg):
        self.log_viewer.append(msg)
        sb = self.log_viewer.verticalScrollBar()
        sb.setValue(sb.maximum())

    def remove_service(self):
        unregister_service(self.service_name)
        event_bus.service_changed.emit()

    # -------------------------
    # Close Event (Stop thread)
    # -------------------------
    def closeEvent(self, event):
        if self.log_thread:
            self.log_thread.stop()
        super().closeEvent(event)

    # -------------------------
    # Window Dragging
    # -------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edges = self._detect_edge(event.position().toPoint())
            if edges:
                self.resizing = True
                self.resize_edge = edges
            else:
                self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        edges = self._detect_edge(pos)

        # 1) 커서 모양
        if not self.resizing:
            self._update_cursor(edges)

        # 2) Resize 동작
        if self.resizing:
            self._perform_resize(event)
            return

        # 3) Move 동작
        if self._old_pos:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resize_edge = None
        self._old_pos = None
        self.setCursor(Qt.ArrowCursor)

    # -------------------------
    # Resize Logic
    # -------------------------
    def _detect_edge(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self.resize_margin

        edges = []
        if x <= m: edges.append("left")
        if x >= w - m: edges.append("right")
        if y <= m: edges.append("top")
        if y >= h - m: edges.append("bottom")
        return edges

    def _update_cursor(self, edges):
        if "left" in edges and "top" in edges: self.setCursor(Qt.SizeFDiagCursor)
        elif "right" in edges and "bottom" in edges: self.setCursor(Qt.SizeFDiagCursor)
        elif "right" in edges and "top" in edges: self.setCursor(Qt.SizeBDiagCursor)
        elif "left" in edges and "bottom" in edges: self.setCursor(Qt.SizeBDiagCursor)
        elif "left" in edges or "right" in edges: self.setCursor(Qt.SizeHorCursor)
        elif "top" in edges or "bottom" in edges: self.setCursor(Qt.SizeVerCursor)
        else: self.setCursor(Qt.ArrowCursor)

    def _perform_resize(self, event):
        rect = self.geometry()
        pos = event.globalPosition().toPoint()

        min_w, min_h = 400, 200

        if "right" in self.resize_edge:
            new_w = max(pos.x() - rect.x(), min_w)
            rect.setWidth(new_w)

        if "bottom" in self.resize_edge:
            new_h = max(pos.y() - rect.y(), min_h)
            rect.setHeight(new_h)

        if "left" in self.resize_edge:
            diff = pos.x() - rect.x()
            if rect.width() - diff > min_w:
                rect.setX(pos.x())
                rect.setWidth(rect.width() - diff)

        if "top" in self.resize_edge:
            diff = pos.y() - rect.y()
            if rect.height() - diff > min_h:
                rect.setY(pos.y())
                rect.setHeight(rect.height() - diff)

        self.setGeometry(rect)

    def modify_system_file(self):
        path = f"/etc/systemd/system/{self.service_name}.service"
        try:
            with open(path, "r") as f:
                data = f.read()
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "파일 오류", str(e))
            return

        # 읽은 내용 새 창에 띄우기
        dialog = FileViewerDialog(path, data)
        dialog.exec()
            





# -------------------------
# Test Run
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = ServiceMenuDialog("ssh")
    dlg.show()   # 모델리스
    sys.exit(app.exec())
