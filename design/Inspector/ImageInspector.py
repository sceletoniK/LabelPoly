import os
from pathlib import Path
from typing import List, Optional, Callable

from PyQt5.QtGui import QPixmap

from .LabelInspector import LabelInspector


class ImageItem:

    def __init__(self,
                 image_path: Path):
        self.pixmap = QPixmap(str(image_path))
        self.labels_file = image_path.parent / (image_path.stem + '.txt')
        if not self.labels_file.exists():
            with open(self.labels_file, mode='a'):
                pass


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
                    file.writelines(label.to_yolo_format())

        self._current = value
        for handler in self.current_changed:
            handler()

    def get_images(self, path_value: str) -> List[ImageItem]:
        self.images.clear()
        for handler in self.images_changed:
            handler()

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
        return self.images
