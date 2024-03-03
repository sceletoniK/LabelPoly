from typing import List, Tuple

from PyQt5.QtCore import QPoint, Qt, QLine, QRect, QRectF
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView


class LabelPoint:

    def __init__(self, x: int, y: int):
        self.x = round(x)
        self.y = round(y)

    def range_poly(self, another):
        return (self.x - another.x) * (self.y - another.y)

    def range(self, another):
        return abs(self.x - another.x) + abs(self.y - another.y)

    def diff(self, another) -> Tuple[int, int]:
        return self.x - another.x, self.y - another.y


class LabelBoundException(Exception):
    pass


class LabelItem:

    def __init__(self, class_index: int, x: int, y: int):
        self.points: List[LabelPoint] = [LabelPoint(x, y)]
        self.is_finished = False
        self.class_index = class_index

    def move(self, delta_point: QPoint):
        for point in self.points:
            point.x += delta_point.x()
            point.y += delta_point.y()

    def _optimize(self) -> List[LabelPoint]:
        new_points: List[LabelPoint] = [] #self.points[:-2]
        if len(self.points) < 3:
            return self.points
        # if self.points[-1].x == self.points[-2].x == self.points[-3].x or \
        #        self.points[-1].y == self.points[-2].y == self.points[-3].y:
        #    new_points += self.points[-1:]
        # else:
        #    new_points += self.points[-2:]
        # return new_points
        for i, point in enumerate(self.points):
            if self.points[i - 1].x == point.x == self.points[(i + 1) % len(self.points)].x:
                print(i)
                continue
            if self.points[i - 1].y == point.y == self.points[(i + 1) % len(self.points)].y:
                print(i)
                continue
            new_points.append(point)
        if len(new_points) < 4 and self.is_finished:
            raise LabelBoundException("No rect label")
        if not new_points:
            new_points = [self.points[0], self.points[-1]]
        return new_points

    def add_point(self, x: int, y: int, limit: int = 100) -> bool:
        if self.is_finished:
            raise Exception('Try add point to finished poly')

        new_point = LabelPoint(x, y)
        if self.points[-1].range_poly(new_point):
            raise Exception("Non poly figure")

        if len(self.points) > 1 and self.points[-1].range(new_point) <= limit:
            return self.is_finished

        if len(self.points) > 1 and self.points[0].range(new_point) <= limit:
            self.points.append(new_point)
            self.points = self._optimize()[:-1]

            diff0 = self.points[-1].diff(self.points[0])

            if abs(diff0[0]) <= abs(diff0[1]):
                self.points[-1].x = self.points[0].x
            else:
                self.points[-1].y = self.points[0].y
            self.points = self._optimize()
            self.is_finished = True
            return self.is_finished

        self.points.append(new_point)
        #self.points = self._optimize()
        return self.is_finished

    def get_bound(self) -> Tuple[int, int, int, int]:

        x = min([t.x for t in self.points])
        y = min([t.y for t in self.points])

        return (
            x,
            y,
            max([t.x for t in self.points]) - x,
            max([t.y for t in self.points]) - y
        )

    def to_yolo_format(self):
        pass


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
        self.active: bool = False

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
            if self.active:
                painter.setBrush(QColor.fromRgb(60, 60, 60, 80))
                painter.drawPolygon(points)
            painter.drawPolygon(points)
            for point in points:
                painter.drawEllipse(
                    QRect(
                        QPoint(point.x() - 3, point.y() - 3),
                        QPoint(point.x() + 3, point.y() + 3)
                    )
                )

    def boundingRect(self):
        return QRectF(*self.label.get_bound())
