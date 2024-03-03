from typing import List

from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsSceneMouseEvent

from .Items import LabelItem, QLabelGraphicItem


class Handler:

    def __init__(self, item: LabelItem, current_index: int):
        self._target_point = item.points[current_index]
        self._label_item = item
        self._current_index = current_index
        self._move_border = 5
        self.active: bool = False
        self.size = 10

    def touch(self, point: QPoint) -> bool:
        if self._target_point.x + self.size <= point.x() <= self._target_point.x - self.size and \
                self._target_point.y + self.size <= point.y() <= self._target_point.y - self.size:
            return True
        return False

    def paint(self,
              painter: QPainter,
              option,
              widget=...):
        view: QGraphicsView = widget.parent()
        scale = 1
        if isinstance(view, QGraphicsView):
            scale = 1 / view.transform().m11() if 1 / view.transform().m11() > 1 else 1
        rect = QRect(
            QPoint(self._target_point.x - self.size * scale, self._target_point.y - self.size * scale),
            QPoint(self._target_point.x + self.size * scale, self._target_point.y + self.size * scale)
        )
        if self.active:
            painter.setBrush(QColor.fromRgb(80, 80, 80, 100))
            painter.drawEllipse(rect)
        pen = QPen(QColor.fromRgb(100, 100, 100), 3 * scale, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawEllipse(rect)

    def move(self, new_point: QPoint):
        delta_point: QPoint = new_point - self._target_point
        if (delta_point.x() > self._move_border and
                delta_point.y() > self._move_border):
            return

        if delta_point.x() > delta_point.y():

            self._target_point.x = new_point.x()

            for i in (1, -1):
                if self._label_item.points[self._current_index + i].y == self._target_point.y:
                    self._label_item.points[self._current_index + i].x = new_point.x()
        else:

            self._target_point.y = new_point.y()

            for i in (1, -1):
                if self._label_item.points[self._current_index + i].x == self._target_point.x:
                    self._label_item.points[self._current_index + i].y = new_point.y()


class LabelManipulator(QLabelGraphicItem):

    def __init__(self, graphic_label: QLabelGraphicItem):
        super().__init__(graphic_label.label)
        if isinstance(graphic_label, LabelManipulator):
            raise Exception("Manipulator's recursion")
        self.graphic_label = graphic_label
        self.handlers: List[Handler] = [
            Handler(graphic_label.label, i) for i, n in enumerate(graphic_label.label.points)]
        self.active: bool = False
        self._active_handler: Handler = None

    @property
    def active_handler(self):
        return self._active_handler

    @active_handler.setter
    def active_handler(self, value: Handler):
        if self._active_handler:
            self._active_handler.active = False

        self._active_handler = value
        if self._active_handler:
            self._active_handler.active = True

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        #for handler in self.handlers:
        #    if handler.touch(event.scenePos()):
        #        self.active_handler = handler
        #        self.active = False
        #        return
        self.active = True

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.active = False
        self.active_handler = None

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.active:
            delta_point = event.scenePos() - event.lastScenePos()
            print(delta_point)
            self.graphic_label.label.move(delta_point)
            return
        if self._active_handler:
            self._active_handler.move(event.scenePos())

    def paint(self, painter, option, widget=...):
        if self.active:
            painter.setBrush(QColor.fromRgb(80, 80, 80, 100))
            points = [QPoint(t.x, t.y) for t in self.graphic_label.label.points]
            painter.drawPolygon(points)
        super().paint(painter, option, widget)
        #for handler in self.handlers:
        #    handler.paint(painter, option, widget)
