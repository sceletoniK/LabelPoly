from typing import List, Tuple, Callable


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


class LabelItem:

    def __init__(self, class_index: int, x: int, y: int):
        self.points: List[LabelPoint] = [LabelPoint(x, y)]
        self.is_finished = False
        self.class_index = class_index

    def add_point(self, x: int, y: int, limit: int = 100) -> bool:
        if self.is_finished:
            raise Exception('Try add point to finished poly')

        new_point = LabelPoint(x, y)
        if self.points[-1].range_poly(new_point):
            raise Exception("Non poly figure")

        if len(self.points) > 1 and self.points[-1].range(new_point) <= limit:
            return self.is_finished

        if len(self.points) > 1 and self.points[0].range(new_point) <= limit:
            diff0 = self.points[-1].diff(self.points[0])
            diff1 = self.points[-1].diff(self.points[1])

            if abs(diff0[0]) <= abs(diff0[1]):
                self.points[-1].x = self.points[0].x
            else:
                self.points[-1].y = self.points[0].y
            self.is_finished = True
            return self.is_finished

        self.points.append(new_point)
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
