from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent

from ..QWidget import QLabelGraphicScene


class LabelStrategy:

    def __init__(self, scene: QLabelGraphicScene):
        self.scene: QLabelGraphicScene = scene

    def apply(self):
        self.scene.unselect_current()
        self.scene.label_inspector.remove_current()
        self.scene.keyReleaseEvent = self.keyReleaseEvent
        self.scene.mouseMoveEvent = self.mouseMoveEvent
        self.scene.mousePressEvent = self.mousePressEvent
        self.scene.mouseReleaseEvent = self.mouseReleaseEvent

    def keyReleaseEvent(self, event: QKeyEvent):
        raise NotImplemented

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        raise NotImplemented

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        raise NotImplemented

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        raise NotImplemented
