from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction

class SystemTray:
    def __init__(self, app, window):
        self.app = app
        self.window = window

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("/usr/share/service-hub/assets/icon.png"))
        self.tray.setVisible(True)

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

        self.tray.setContextMenu(self.menu)

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
