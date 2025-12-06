from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction

class SystemTray:
    def __init__(self, app, window):
        self.app = app
        self.window = window

        # 트레이 아이콘 생성
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("/usr/share/service-hub/assets/icon.png"))
        self.tray.setVisible(True)

        # 메뉴 생성 (멤버 변수로 유지해야 GC 안 됨)
        self.menu = QMenu()

        self.action_show = QAction("Open Service Hub")
        self.action_show.triggered.connect(self.show_window)

        self.action_hide = QAction("Hide")
        self.action_hide.triggered.connect(self.hide_window)

        self.action_quit = QAction("Quit")
        self.action_quit.triggered.connect(self.app.quit)

        self.menu.addAction(self.action_show)
        self.menu.addAction(self.action_hide)
        self.menu.addSeparator()
        self.menu.addAction(self.action_quit)

        # 메뉴 설정
        self.tray.setContextMenu(self.menu)

        # 클릭 이벤트도 연결할 수 있음
        self.tray.activated.connect(self.on_activated)

    def show_window(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def hide_window(self):
        self.window.hide()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # left click
            self.show_window()
