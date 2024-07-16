from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent

from .Strategy import LabelStrategy
from ..Label import QLabelGraphicItem, LabelManipulator


class SelectStrategy(LabelStrategy):

    def _find_label(self, pos: QPoint) -> Optional[QLabelGraphicItem]:
        labels = [x for x in self.scene.items(pos) if isinstance(x, (QLabelGraphicItem, LabelManipulator))]
        return labels[0] if labels else None

    def keyReleaseEvent(self, event: QKeyEvent):
        print("key")
        return

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        print('move')
        if isinstance(self.scene.current_label, LabelManipulator) and \
                event.buttons() == Qt.LeftButton:
            self.scene.current_label.mouseMoveEvent(event)
        self.scene.update()
        print('end move')

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print('press')
        item = self._find_label(event.scenePos())
        if not item:
            self.scene.unselect_current()
            self.scene.label_inspector.set_current(None)
        else:
            item: QLabelGraphicItem
            self.scene.label_inspector.set_current(item.label)
            item: LabelManipulator = self.scene.select_current()
            item.mousePressEvent(event)
        self.scene.update()
        print('end press')

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        print('release')
        if isinstance(self.scene.current_label, LabelManipulator):
            self.scene.current_label.mouseReleaseEvent(event)
        self.scene.update()
        print('end release')
