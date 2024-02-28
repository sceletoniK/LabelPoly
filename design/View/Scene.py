from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QApplication

from ..Inspector import LabelInspector
from ..Label import QLabelGraphicItem


class QLabelGraphicScene(QGraphicsScene):

    def __init__(self, label_inspector: LabelInspector):
        super().__init__()
        self.label_inspector = label_inspector
        self._current_label: QLabelGraphicItem = None
        self.image = QPixmap()
        self.setSceneRect(
            self.image.rect().x(),
            self.image.rect().y(),
            self.image.rect().width(),
            self.image.rect().height()
        )
        self.setBackgroundBrush(QBrush(QColor.fromRgb(180, 180, 180)))
        self.label_inspector.current_changed = self.update_current

    def keyReleaseEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if (modifiers != Qt.ControlModifier or
                not self._current_label or
                event.key() != Qt.Key_D):
            super().keyReleaseEvent(event)
            return
        self.label_inspector.remove_current()

    def mouseMoveEvent(self, event):
        if self._current_label:
            dx = abs(self._current_label.label.points[-1].x - event.scenePos().x())
            dy = abs(self._current_label.label.points[-1].y - event.scenePos().y())
            if dx < dy:
                self._current_label.mouse_point = QPoint(self._current_label.label.points[-1].x,
                                                         event.scenePos().y())
            else:
                self._current_label.mouse_point = QPoint(event.scenePos().x(),
                                                         self._current_label.label.points[-1].y)
            self.update()

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):

        if event.scenePos().x() < 0 or \
                event.scenePos().x() >= self.image.width() or \
                event.scenePos().y() < 0 or \
                event.scenePos().y() >= self.image.height():
            return

        if not self.label_inspector.current_class:
            return

        if event.button() == Qt.LeftButton:
            if self.label_inspector.current_label:
                self.label_inspector.set_point(self._current_label.mouse_point.x(),
                                               self._current_label.mouse_point.y())
            else:
                self.label_inspector.set_point(event.scenePos().x(), event.scenePos().y())
        elif event.button() == Qt.RightButton:
            self.label_inspector.remove_current()
        self.update()

    def update_current(self):
        if self.label_inspector.current_label:
            self._current_label = QLabelGraphicItem(self.label_inspector.current_label)
            if self._current_label not in self.items():
                self.addItem(self._current_label)
            return
        if (self._current_label.label not in self.label_inspector.labels and
                self._current_label in self.items()):
            self.removeItem(self._current_label)
        self._current_label = None

    def changeImage(self, path: str):
        self.clear()
        self.image = QPixmap(path)
        self.addPixmap(self.image)
        self.setSceneRect(
            self.image.rect().x(),
            self.image.rect().y(),
            self.image.rect().width(),
            self.image.rect().height()
        )
