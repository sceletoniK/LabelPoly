from typing import List, Callable, Optional
from ..Label import LabelItem


class LabelInspector:

    def __init__(self, class_names: List[str]):
        self.labels: List[LabelItem] = []
        self.label_classes: List[str] = class_names
        self._current_label: LabelItem = None
        self._current_class: int = None
        self.labels_changed: List[Callable] = []
        self.current_changed: List[Callable] = []

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

    def set_current(self, item: Optional[LabelItem]):
        self._current_label = item
        for handler in self.current_changed:
            handler()

    def remove_current(self):
        if self.current_label:  # and self.current_label.is_finished == False:
            self._current_label = None
        for handler in self.current_changed:
            handler()

    def add_label(self, label: LabelItem):
        if label:
            self.labels.append(label)
            for handler in self.labels_changed:
                handler()

    def delete_label(self, label: LabelItem):
        if label:
            if label == self.current_label:
                self.remove_current()
            self.labels.remove(label)
            for handler in self.labels_changed:
                handler()

    def set_point(self, x: int, y: int, limit: int = 20):
        if self.current_label:
            self.current_label.add_point(x, y, limit)
            # self.add_label()
            # self.set_current(self._current_label)
        else:
            if self._current_class is None:
                raise Exception("Label class dont set")
            label = LabelItem(self._current_class, x, y)
            self.add_label(label)
            self.set_current(label)

    def clear(self):
        self.labels.clear()
        for handler in self.labels_changed:
            handler()
