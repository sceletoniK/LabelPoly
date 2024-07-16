from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QApplication

from .Scene import QLabelGraphicScene


class QLabelGraphicView(QGraphicsView):

    def __init__(self, parent, scene: QLabelGraphicScene):
        super().__init__(parent)
        self.setScene(scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    @property
    def scene(self) -> QLabelGraphicScene:
        return super().scene()

    def wheelEvent(self, event):
        if not self.scene.image:
            return
        modifiers = QApplication.keyboardModifiers()
        if modifiers != Qt.ShiftModifier:
            super().wheelEvent(event)
            return

        y_delta = (event.angleDelta() / 8).y()

        if y_delta > 0:
            self.scale(1.1, 1.1)
        elif y_delta < 0:
            self.scale(0.9, 0.9)
