from typing import Optional

from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene

from ..Inspector import LabelInspector, ImageInspector, ImageItem
from ..Label import QLabelGraphicItem, LabelManipulator, LabelItem


class QLabelGraphicScene(QGraphicsScene):

    def __init__(self, label_inspector: LabelInspector, image_inspector: ImageInspector):
        super().__init__()
        self.label_inspector = label_inspector
        self.image_inspector = image_inspector
        self._current_label: QLabelGraphicItem = None
        self.image: Optional[ImageItem] = None
        self.setBackgroundBrush(QBrush(QColor.fromRgb(180, 180, 180)))
        self.label_inspector.current_changed.append(self._update_current)
        self.label_inspector.labels_changed.append(self._update_labels)
        self.image_inspector.current_changed.append(self.change_image)
        self.image_inspector.images_changed.append(self.change_image)

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

    def _update_labels(self):
        for label in [x for x in self.items() if isinstance(x, (QLabelGraphicItem, LabelManipulator))]:
            self.removeItem(label)
        for label in self.label_inspector.labels:
            item = QLabelGraphicItem(label)
            item.setZValue(100)
            self.addItem(item)
        self._update_current()

    def _update_current(self):
        if self._current_label:
            self._current_label.active = False
        self._current_label = self._find_label(self.label_inspector.current_label)
        if self._current_label:
            self._current_label.active = True
        self.update()

    def change_image(self):
        self.clear()
        self.image = self.image_inspector.current
        if self.image:
            item = self.addPixmap(self.image.pixmap)
            item.setZValue(0)
            self.setSceneRect(
                self.image.pixmap.rect().x(),
                self.image.pixmap.rect().y(),
                self.image.pixmap.rect().width(),
                self.image.pixmap.rect().height()
            )
        self._update_labels()
