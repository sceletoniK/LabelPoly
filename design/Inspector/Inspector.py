from typing import List, Tuple, Callable
from ..Label import LabelItem


class LabelInspector:

    def __init__(self, class_names: List[str]):
        self.labels: List[LabelItem] = []
        self.label_classes: List[str] = class_names
        self._current_label: LabelItem = None
        self._current_class: int = None
        self.labels_changed: Callable = None
        self.current_changed: Callable = None

    @property
    def current_label(self):
        return self._current_label

    @property
    def current_class(self):
        return self.label_classes[self._current_class] if \
            (self.label_classes and self._current_class is not None) \
            else None

    def change_label_class(self, label_class: str):
        if not self.current_label:
            if label_class not in self.label_classes:
                raise Exception('Unknown class')
            self._current_class = self.label_classes.index(label_class)
            return True
        self.current_label.class_index = self.label_classes.index(label_class)

    def add_label_class(self, label: str) -> bool:
        if label not in self.label_classes:
            self.label_classes.append(label)
            return True
        return False

    def remove_label_class(self, label: str) -> bool:
        if label in self.label_classes:
            index = self.label_classes.index(label)
            self.labels = [x for x in self.labels if x.class_index != index]
            return True
        return False

    def set_current(self, item: LabelItem):
        self._current_label = item
        if self.current_changed:
            self.current_changed()

    def remove_current(self):
        if self.current_label:  # and self.current_label.is_finished == False:
            self._current_label = None
        if self.current_changed:
            self.current_changed()

    def add_label(self):
        self.labels.append(self.current_label)
        if self.labels_changed:
            self.labels_changed()

    def delete_label(self, label: LabelItem):
        self.labels.remove(label)
        if self.labels_changed:
            self.labels_changed()

    def set_point(self, x: int, y: int, limit: int = 20):
        if self.current_label:
            if self.current_label.add_point(x, y, limit):
                self.add_label()
                self.remove_current()
        else:
            if self._current_class is None:
                raise Exception("Label class dont set")
            self.set_current(LabelItem(self._current_class, x, y))

    def clear(self):
        self.labels.clear()
        if self.labels_changed:
            self.labels_changed()
