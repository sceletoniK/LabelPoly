from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..QWidget import QLabelGraphicScene


class LabelStrategy:

    def __init__(self):
        pass

    def keyReleaseEvent(self, event: QKeyEvent,
                        scene: QLabelGraphicScene):
        raise NotImplemented

    def mouseMoveEvent(self, event: QMouseEvent,
                       scene: QLabelGraphicScene,
                       scene_point: QPointF):
        raise NotImplemented

    def mousePressEvent(self, event: QMouseEvent,
                        scene: QLabelGraphicScene,
                        scene_point: QPointF):
        raise NotImplemented

    def mouseReleaseEvent(self, event: QMouseEvent,
                          scene: QLabelGraphicScene,
                          scene_point: QPointF):
        raise NotImplemented
