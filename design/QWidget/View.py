from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QApplication

from .Scene import QLabelGraphicScene
from ..Inspector import LabelInspector
from ..Strategy import LabelStrategy, InsertStrategy


class QLabelGraphicView(QGraphicsView):

    def __init__(self, parent, label_inspector: LabelInspector):
        super().__init__(parent)
        self.setScene(QLabelGraphicScene(label_inspector))
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.strategy: LabelStrategy = InsertStrategy()
        self.inspector = label_inspector

    @property
    def scene(self) -> QLabelGraphicScene:
        return super().scene()

    def keyReleaseEvent(self, event):
        if self.strategy:
            self.strategy.keyReleaseEvent(event, self.scene)

    def mouseMoveEvent(self, event):
        if self.strategy:
            self.strategy.mouseMoveEvent(event, self.scene, self.mapToScene(event.pos()))

    def mousePressEvent(self, event):
        if self.strategy:
            self.strategy.mousePressEvent(event, self.scene, self.mapToScene(event.pos()))

    def mouseReleaseEvent(self, event):
        if self.strategy:
            self.strategy.mouseReleaseEvent(event, self.scene, self.mapToScene(event.pos()))

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
