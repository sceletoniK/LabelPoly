from typing import List, Tuple

from PyQt5.QtCore import QPoint, QRectF, Qt, QLine, QRect
from PyQt5.QtGui import QColor, QPen, QMouseEvent, QCursor, QImage, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QStyle, QGraphicsView, QApplication
from PyQt5.uic.properties import QtGui

from LabelInspector import LabelInspector, LabelItem


class QLabelGraphicItem(QGraphicsItem):
    label_colors: List[QColor] = [
        QColor.fromRgb(255, 0, 0),
        QColor.fromRgb(0, 255, 0),
        QColor.fromRgb(0, 0, 255)
    ]

    def __init__(self, label: LabelItem = None):
        super().__init__()
        self.label: LabelItem = label
        self.mouse_point: QPoint = QPoint(label.points[0].x,
                                          label.points[0].y)
        self.limit = 20

    def paint(self, painter, option, widget=...):
        view: QGraphicsView = widget.parent()
        scale = 1
        if isinstance(view, QGraphicsView):
            scale = 1 / view.transform().m11() if 1 / view.transform().m11() > 1 else 1
        pen = QPen(QLabelGraphicItem.label_colors[self.label.class_index % len(self.label_colors)],
                   3 * scale, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        points = [QPoint(t.x, t.y) for t in self.label.points]
        if not self.label.is_finished:
            painter.drawPolyline(points)
            pen.setColor(QColor.fromRgb(100, 100, 100))
            pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawLine(QLine(points[-1], self.mouse_point))
            if (abs(self.mouse_point.x() - points[0].x()) +
                    abs(self.mouse_point.y() - points[0].y()) <= self.limit):
                painter.drawEllipse(
                    QRect(
                        QPoint(points[0].x() - 10 * scale, points[0].y() - 10 * scale),
                        QPoint(points[0].x() + 10 * scale, points[0].y() + 10 * scale)
                    )
                )
        else:
            painter.drawPolygon(points)

    def boundingRect(self):
        return QRectF(*self.label.get_bound())


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
        self.label_inspector.current_changed = self.set_current

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
                if not self.label_inspector.current_label:
                    self._current_label = None
            else:
                self.label_inspector.set_point(event.scenePos().x(), event.scenePos().y())
        elif event.button() == Qt.RightButton:
            self.label_inspector.remove_current()
            self.removeItem(self._current_label)
            self._current_label = None
        self.update()

    def set_current(self):
        if not self.label_inspector.current_label:
            return
        self._current_label = QLabelGraphicItem(self.label_inspector.current_label)
        if self._current_label not in self.items():
            self.addItem(self._current_label)

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


class QLabelGraphicView(QGraphicsView):

    def __init__(self, parent, label_inspector: LabelInspector):
        super().__init__(parent)
        self.setScene(QLabelGraphicScene(label_inspector))
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        scene: QLabelGraphicScene = self.scene()
        if not scene.image:
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
