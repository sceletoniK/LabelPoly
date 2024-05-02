import os
import numpy as np
from pathlib import Path
from typing import List, Optional, Callable

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect

from .LabelInspector import LabelInspector
from ..Label import LabelItem, LabelPoint


class ImageItem:

    def __init__(self,
                 image_path: Path):
        self.pixmap = QPixmap(str(image_path))
        self.labels_file = image_path.parent / (image_path.stem + '.txt')
        if not self.labels_file.exists():
            with open(self.labels_file, mode='a'):
                pass


def label_to_yolo_str(item: LabelItem, image_rect: QRect) -> str:
    return ' '.join([str(item.class_index)] +
                    [f'{round(p.x / image_rect.width(), 6)} '
                     f'{round(p.y / image_rect.height(), 6)}' for p in item.points]) + '\n'


def yolo_str_to_label(value: str, image_rect: QRect) -> LabelItem:
    label_index = int(value.split()[0])
    str_points = value.split()[1:]
    points = [[round(float(x[0]) * image_rect.width()),
               round(float(x[1]) * image_rect.height())]
              for x in np.reshape(str_points, (int(len(str_points) / 2), 2))]
    item = LabelItem(
        label_index,
        points[0][0],
        points[0][1]
    )

    item.points = [LabelPoint(x[0], x[1]) for x in points]
    item.is_finished = True

    return item


class ImageInspector:

    def __init__(self, label_inspector: LabelInspector):
        self.images: List[ImageItem] = []
        self.label_inspector = label_inspector
        self._current: Optional[ImageItem] = None
        self.current_changed: List[Callable] = []
        self.images_changed: List[Callable] = []

    @property
    def current_index(self):
        return -1 if not self._current else self.images.index(self._current)

    @property
    def next(self):
        if not self._current:
            return None
        index = self.current_index
        if index == len(self.images) - 1:
            return None
        return self.images[index + 1]

    @property
    def prev(self):
        if not self._current:
            return None
        index = self.current_index
        if index == 0:
            return None
        return self.images[index - 1]

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value: ImageItem):
        if self._current:
            with open(self._current.labels_file, mode='w') as file:
                file.truncate(0)
                for label in self.label_inspector.labels:
                    file.write(label_to_yolo_str(label,
                                                 self._current.pixmap.rect()))

        self._current = value
        self.label_inspector.clear()
        if self._current:
            with open(self._current.labels_file, mode='r') as file:
                for line in file.readlines():
                    self.label_inspector.add_label(yolo_str_to_label(line,
                                                                     self._current.pixmap.rect()))
        for handler in self.current_changed:
            handler()

    def get_images(self, path_value: str) -> List[ImageItem]:
        self.images.clear()

        path = Path(path_value)
        if path.is_file():
            self.images.append(ImageItem(path))
        elif path.is_dir():
            for filename in os.listdir(path):
                sub_path = path / filename
                if sub_path.suffix in ('.png', '.jpg', '.jpeg'):
                    self.images.append(ImageItem(sub_path))

        for handler in self.images_changed:
            handler()
        if self.images:
            self.current = self.images[0]
        else:
            self.current = None
        return self.images
