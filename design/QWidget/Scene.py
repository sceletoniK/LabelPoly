from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene

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

    @property
    def current_label(self):
        return self._current_label

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
