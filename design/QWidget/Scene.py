from typing import List, Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene

from ..Inspector import LabelInspector
from ..Label import QLabelGraphicItem, LabelManipulator, LabelItem


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
        self.label_inspector.current_changed = self._update_current

    @property
    def current_label(self):
        return self._current_label

    def mouseMoveEvent(self, event):
        pass

    def select_current(self) -> LabelManipulator:
        if self._current_label and not isinstance(self._current_label, LabelManipulator):
            self.removeItem(self._current_label)
            self._current_label = LabelManipulator(self._current_label)
            self.addItem(self._current_label)
        return self._current_label

    def unselect_current(self):
        if self._current_label and isinstance(self._current_label, LabelManipulator):
            self._current_label: LabelManipulator
            self.removeItem(self._current_label)
            self._current_label = self._current_label.graphic_label
            self.addItem(self._current_label)

    def _find_label(self, label: LabelItem) -> Optional[QLabelGraphicItem]:
        for i, graphic_label in enumerate(self.items()):
            if not isinstance(graphic_label, QLabelGraphicItem):
                continue
            if label == graphic_label.label:
                return graphic_label
        return None

    def _update_current(self):
        if self.label_inspector.current_label:
            self._current_label = self._find_label(self.label_inspector.current_label)
            if not self._current_label:
                self._current_label = QLabelGraphicItem(self.label_inspector.current_label)
                self.addItem(self._current_label)
            return
        if (self._current_label and
                (self._current_label.label not in self.label_inspector.labels and
                 self._find_label(self._current_label.label))):
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

