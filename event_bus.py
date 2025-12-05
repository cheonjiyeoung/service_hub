from PySide6.QtCore import QObject, Signal

class EventBus(QObject):
    service_changed = Signal()

event_bus = EventBus()