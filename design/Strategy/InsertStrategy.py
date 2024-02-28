from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication

from .Strategy import LabelStrategy
from ..QWidget import QLabelGraphicScene


class InsertStrategy(LabelStrategy):

    def keyReleaseEvent(self, event: QKeyEvent,
                        scene: QLabelGraphicScene):
        if not scene.image.width():
            return
        modifiers = QApplication.keyboardModifiers()
        if (modifiers != Qt.ControlModifier or
                not scene.current_label or
                event.key() != Qt.Key_D):
            scene.keyReleaseEvent(event)
            return
        scene.label_inspector.remove_current()

    def mouseMoveEvent(self, event: QMouseEvent,
                       scene: QLabelGraphicScene,
                       scene_point: QPoint):
        if scene.current_label:
            dx = abs(scene.current_label.label.points[-1].x - scene_point.x())
            dy = abs(scene.current_label.label.points[-1].y - scene_point.y())
            if dx < dy:
                scene.current_label.mouse_point = QPoint(scene.current_label.label.points[-1].x,
                                                         scene_point.y())
            else:
                scene.current_label.mouse_point = QPoint(scene_point.x(),
                                                         scene.current_label.label.points[-1].y)
        scene.update()

    def mousePressEvent(self, event: QMouseEvent,
                        scene: QLabelGraphicScene,
                        scene_point: QPoint):
        pass

    def mouseReleaseEvent(self, event: QMouseEvent,
                          scene: QLabelGraphicScene,
                          scene_point: QPoint):
        if scene_point.x() < 0 or \
                scene_point.x() >= scene.image.width() or \
                scene_point.y() < 0 or \
                scene_point.y() >= scene.image.height():
            return

        if not scene.label_inspector.current_class:
            return

        if event.button() == Qt.LeftButton:
            if scene.label_inspector.current_label:
                scene.label_inspector.set_point(scene.current_label.mouse_point.x(),
                                                scene.current_label.mouse_point.y())
            else:
                scene.label_inspector.set_point(scene_point.x(), scene_point.y())
        elif event.button() == Qt.RightButton:
            scene.label_inspector.remove_current()
        scene.update()
