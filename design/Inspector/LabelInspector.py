from typing import List, Callable, Optional
from ..Label import LabelItem


class LabelInspector:

    def __init__(self, class_names: List[str]):
        self.labels: List[LabelItem] = []
        self.label_classes: List[str] = class_names
        self._current_label: Optional[LabelItem] = None
        self._current_class: Optional[int] = None
        self.labels_changed: List[Callable] = []
        self.current_changed: List[Callable] = []
        self.labels_classes_changed: List[Callable] = []

    @property
    def current_label(self):
        return self._current_label

    @property
    def current_class(self):
        return self.label_classes[self._current_class] if \
            (self.label_classes and self._current_class is not None) \
            else None

    def change_label_class(self, label_class: Optional[str]):
        if self.current_label and label_class in self.label_classes:
            self.current_label.class_index = self.label_classes.index(label_class)
            for handler in self.labels_changed:
                handler()
        self._current_class = self.label_classes.index(label_class) if label_class else None

    def add_label_class(self, label: str) -> bool:
        if label not in self.label_classes:
            self.label_classes.append(label)
            for handler in self.labels_classes_changed:
                handler()
            return True
        return False

    def add_label_classes(self, labels: List[str], inplace: bool = False):
        if labels:
            if inplace:
                self.label_classes = labels
            else:
                self.label_classes = list(set(self.label_classes + labels))
            for handler in self.labels_classes_changed:
                handler()

    def delete_label_class(self, label_class: str) -> bool:
        if label_class in self.label_classes:
            index = self.label_classes.index(label_class)
            for label_item in [x for x in self.labels if x.class_index == index]:
                self.delete_label(label_item)
            self.label_classes.remove(label_class)
            self.change_label_class(None)
            for handler in self.labels_classes_changed:
                handler()
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
