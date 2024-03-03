from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QSize, Qt, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QKeyEvent
from PyQt5.QtWidgets import QAction, QFileDialog, QWidget, QApplication

from ..Inspector import LabelInspector


class QLabelList(QtWidgets.QListView):
    def __init__(self, parent: QWidget, label_inspector: LabelInspector):
        super().__init__(parent)
        self.label_inspector = label_inspector
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.object_list_model = QStandardItemModel()
        self.setModel(self.object_list_model)
        self.clicked[QModelIndex].connect(self.change_label)
        self.label_inspector.labels_changed.append(self.update_label_list)
        self.setObjectName("objectList")

    def change_label(self, index):
        item: QStandardItem = self.object_list_model.itemFromIndex(index)
        self.label_inspector.set_current(item.data())

    def update_label_list(self):
        self.object_list_model.clear()
        for i in self.label_inspector.labels:
            item = QStandardItem(self.label_inspector.label_classes[i.class_index])
            item.setData(i)
            item.setEditable(False)
            self.object_list_model.appendRow(item)
            if i == self.label_inspector.current_label:
                self.selectionModel().select(item.index(), QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def keyReleaseEvent(self, event: Optional[QKeyEvent]):
        modifiers = QApplication.keyboardModifiers()
        if (modifiers != Qt.ControlModifier or
                not self.label_inspector.current_label or
                event.key() != Qt.Key_D):
            return
        self.label_inspector.delete_label(self.label_inspector.current_label)
        self.update_label_list()
