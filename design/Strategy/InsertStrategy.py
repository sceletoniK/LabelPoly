from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent

from .Strategy import LabelStrategy


class InsertStrategy(LabelStrategy):

    def keyReleaseEvent(self, event: QKeyEvent):
        if not self.scene.image.width():
            return
        modifiers = event.modifiers()
        if (modifiers != Qt.ControlModifier or
                not self.scene.current_label or
                event.key() != Qt.Key_D):
            return
        self.scene.label_inspector.delete_label(self.scene.label_inspector.current_label)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.scene.current_label:
            dx = abs(self.scene.current_label.label.points[-1].x - event.scenePos().x())
            dy = abs(self.scene.current_label.label.points[-1].y - event.scenePos().y())
            if dx < dy:
                self.scene.current_label.mouse_point = QPoint(self.scene.current_label.label.points[-1].x,
                                                              event.scenePos().y())
            else:
                self.scene.current_label.mouse_point = QPoint(event.scenePos().x(),
                                                              self.scene.current_label.label.points[-1].y)
        self.scene.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        pass

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if event.scenePos().x() < 0 or \
                event.scenePos().x() >= self.scene.image.width() or \
                event.scenePos().y() < 0 or \
                event.scenePos().y() >= self.scene.image.height():
            return

        if not self.scene.label_inspector.current_class:
            return

        if event.button() == Qt.RightButton:
            self.scene.label_inspector.delete_label(self.scene.label_inspector.current_label)
            self.scene.update()
            return

        if event.button() == Qt.LeftButton:
            if self.scene.label_inspector.current_label and \
                    not self.scene.label_inspector.current_label.is_finished:
                self.scene.label_inspector.set_point(self.scene.current_label.mouse_point.x(),
                                                     self.scene.current_label.mouse_point.y())
            else:
                if self.scene.label_inspector.current_label and \
                        self.scene.label_inspector.current_label.is_finished:
                    self.scene.label_inspector.set_current(None)
                self.scene.label_inspector.set_point(event.scenePos().x(), event.scenePos().y())
            self.scene.update()
