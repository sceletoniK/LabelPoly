from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeyEvent
from PyQt5.QtWidgets import QApplication

from design import QWidget
from design.Inspector import LabelInspector


class QLabelClassList(QtWidgets.QListView):
    def __init__(self, parent: QWidget, label_inspector: LabelInspector):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.clicked[QModelIndex].connect(self.changeCurrentLabelClass)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.setObjectName("classesList")
        self.label_inspector = label_inspector
        self.label_inspector.labels_classes_changed.append(self.updateLabelClassList)

    def addLabelClass(self, event):
        name, done = QtWidgets.QInputDialog.getText(
            self, 'Adding label class', 'Enter label class name:')
        if done and name:
            added = self.label_inspector.add_label_class(name)
            if not added:
                warning_dialog = QtWidgets.QMessageBox()
                warning_dialog.setText("Label with that name already exist")
                warning_dialog.setWindowTitle("Warning")
                warning_dialog.exec()
            self.updateLabelClassList()

    def changeCurrentLabelClass(self, index):
        item = self.model.itemFromIndex(index)
        self.label_inspector.change_label_class(item.text())

    def updateLabelClassList(self):
        self.model.clear()
        for i in self.label_inspector.label_classes:
            self.model.appendRow(QStandardItem(i))

    def keyReleaseEvent(self, event: Optional[QKeyEvent]):
        modifiers = QApplication.keyboardModifiers()
        if (modifiers != Qt.ControlModifier or
                not self.label_inspector.current_class or
                event.key() != Qt.Key_D):
            return
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.text() == self.label_inspector.current_class:
                self.label_inspector.delete_label_class(item.text())
                self.updateLabelClassList()
                break
